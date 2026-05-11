from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

import pytest

from app.domains.imports.csv_contract import ImportEntityType, parse_csv_rows
from app.domains.imports.models import ImportRowStatus
from app.domains.imports.service import ImportsService, classify_source_mapping


@dataclass
class MappingStub:
    content_hash: str | None


class BatchStub:
    def __init__(self) -> None:
        self.id = uuid.uuid4()


class IdempotencyRepository:
    def __init__(self) -> None:
        self.mappings: dict[tuple[str, str, str], MappingStub] = {}
        self.mapping_write_count: dict[tuple[str, str, str], int] = {}
        self.rows: list[tuple[str, str, ImportRowStatus]] = []
        self.errors: list[dict[str, Any]] = []

    async def create_batch(self, *, total_rows: int) -> BatchStub:
        self.total_rows = total_rows
        return BatchStub()

    async def find_source_mapping(
        self,
        *,
        source_system: str,
        entity_type: ImportEntityType,
        source_id: str,
    ) -> MappingStub | None:
        return self.mappings.get((source_system, entity_type.value, source_id))

    async def upsert_source_mapping(
        self,
        *,
        batch_id: uuid.UUID,
        entity_type: ImportEntityType,
        source_id: str,
        content_hash: str | None,
        source_system: str,
    ) -> MappingStub:
        key = (source_system, entity_type.value, source_id)
        self.mapping_write_count[key] = self.mapping_write_count.get(key, 0) + 1
        mapping = MappingStub(content_hash=content_hash)
        self.mappings[key] = mapping
        return mapping

    async def add_import_rows(
        self,
        *,
        batch_id: uuid.UUID,
        rows: list[Any],
        status: ImportRowStatus = ImportRowStatus.NEW,
    ) -> list[Any]:
        for row in rows:
            self.rows.append((row.entity_type.value, row.source_id, status))
        return rows

    async def add_error(self, **kwargs: Any) -> object:
        self.errors.append(kwargs)
        return object()


def test_source_mapping_classification_uses_identity_and_hash() -> None:
    assert classify_source_mapping(None, "hash-1") is ImportRowStatus.NEW
    assert classify_source_mapping(MappingStub("hash-1"), "hash-1") is ImportRowStatus.UNCHANGED
    assert classify_source_mapping(MappingStub("hash-1"), "hash-2") is ImportRowStatus.CHANGED


@pytest.mark.anyio
async def test_same_source_id_and_hash_is_unchanged_on_rerun() -> None:
    repository = IdempotencyRepository()
    service = ImportsService(repository)  # type: ignore[arg-type]
    content = "entity_type,source_id,name\nproduct,p-1,Soap\n"

    await service.stage_csv_content(content)
    await service.stage_csv_content(content)

    assert repository.rows == [
        ("product", "p-1", ImportRowStatus.NEW),
        ("product", "p-1", ImportRowStatus.UNCHANGED),
    ]
    assert len(repository.mappings) == 1


@pytest.mark.anyio
async def test_same_source_id_and_different_hash_is_changed_on_rerun() -> None:
    repository = IdempotencyRepository()
    service = ImportsService(repository)  # type: ignore[arg-type]

    await service.stage_csv_content("entity_type,source_id,name\nproduct,p-1,Soap\n")
    await service.stage_csv_content("entity_type,source_id,name\nproduct,p-1,Updated Soap\n")

    assert repository.rows[-1] == ("product", "p-1", ImportRowStatus.CHANGED)
    assert len(repository.mappings) == 1


@pytest.mark.anyio
async def test_new_source_id_is_classified_new() -> None:
    repository = IdempotencyRepository()
    service = ImportsService(repository)  # type: ignore[arg-type]

    await service.stage_csv_content(
        "entity_type,source_id,name\n"
        "product,p-1,Soap\n"
        "product,p-2,Other Soap\n"
    )

    assert repository.rows == [
        ("product", "p-1", ImportRowStatus.NEW),
        ("product", "p-2", ImportRowStatus.NEW),
    ]
    assert len(repository.mappings) == 2


@pytest.mark.anyio
async def test_rerun_does_not_duplicate_source_mappings_across_batches() -> None:
    repository = IdempotencyRepository()
    service = ImportsService(repository)  # type: ignore[arg-type]
    content = (
        "entity_type,source_id,name\n"
        "product,p-1,Soap\n"
        "category,c-1,Soap Category\n"
    )

    await service.stage_csv_content(content)
    await service.stage_csv_content(content)

    assert len(repository.mappings) == 2
    assert set(repository.mapping_write_count.values()) == {2}
    assert repository.rows[-2:] == [
        ("product", "p-1", ImportRowStatus.UNCHANGED),
        ("category", "c-1", ImportRowStatus.UNCHANGED),
    ]


def test_content_hash_is_deterministic_for_normalized_payload() -> None:
    first = parse_csv_rows("entity_type,source_id,name,sku\nproduct,p-1,Soap,SKU-1\n")[0]
    second = parse_csv_rows("sku,name,source_id,entity_type\nSKU-1,Soap,p-1,product\n")[0]

    assert first.content_hash == second.content_hash
