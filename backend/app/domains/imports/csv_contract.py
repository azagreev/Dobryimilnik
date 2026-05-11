from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from io import StringIO


class ImportEntityType(StrEnum):
    PRODUCT = "product"
    VARIANT = "variant"
    CATEGORY = "category"
    MEDIA = "media"
    POST = "post"
    REVIEW = "review"
    CUSTOMER = "customer"
    ORDER = "order"


REQUIRED_HEADERS = frozenset({"entity_type", "source_id"})
OPTIONAL_HEADERS = frozenset(
    {
        "parent_source_id",
        "sku",
        "slug",
        "name",
        "price",
        "stock",
        "category_path",
        "media_url",
        "seo_title",
        "seo_description",
    }
)
CSV_CONTRACT_VERSION = "livemaster-single-csv-v1"


class CsvContractError(ValueError):
    """Raised when CSV structure cannot be processed safely."""


@dataclass(frozen=True)
class CsvImportRow:
    row_number: int
    entity_type: ImportEntityType
    source_id: str
    raw: dict[str, str]
    parent_source_id: str | None = None
    normalized_payload: dict[str, str] | None = None
    content_hash: str | None = None


@dataclass(frozen=True)
class CsvRawRow:
    row_number: int
    raw: dict[str, str]


def validate_headers(headers: Iterable[str] | None) -> set[str]:
    if headers is None:
        raise CsvContractError("CSV file is missing a header row.")

    normalized = {header.strip() for header in headers if header and header.strip()}
    missing = REQUIRED_HEADERS - normalized
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise CsvContractError(f"CSV file is missing required headers: {missing_list}.")

    return normalized


def parse_csv_rows(content: str) -> list[CsvImportRow]:
    reader = csv.DictReader(StringIO(content))
    validate_headers(reader.fieldnames)

    rows: list[CsvImportRow] = []
    for index, raw_row in enumerate(reader, start=2):
        raw = {key: (value or "").strip() for key, value in raw_row.items() if key is not None}
        try:
            entity_type = ImportEntityType(raw.get("entity_type", ""))
        except ValueError as exc:
            raise CsvContractError(
                f"Unsupported entity_type at CSV row {index}: {raw.get('entity_type', '')}."
            ) from exc

        source_id = raw.get("source_id", "")
        if not source_id:
            raise CsvContractError(f"Missing source_id at CSV row {index}.")

        rows.append(build_import_row(index, raw, entity_type=entity_type, source_id=source_id))

    return rows


def parse_raw_csv_rows(content: str) -> list[CsvRawRow]:
    reader = csv.DictReader(StringIO(content))
    validate_headers(reader.fieldnames)

    return [
        CsvRawRow(
            row_number=index,
            raw={key: (value or "").strip() for key, value in raw_row.items() if key is not None},
        )
        for index, raw_row in enumerate(reader, start=2)
    ]


def build_import_row(
    row_number: int,
    raw: dict[str, str],
    *,
    entity_type: ImportEntityType,
    source_id: str,
) -> CsvImportRow:
    normalized_payload = {
        key: value.strip()
        for key, value in raw.items()
        if value is not None and value.strip()
    }
    content_hash = hashlib.sha256(
        json.dumps(normalized_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    parent_source_id = normalized_payload.get("parent_source_id") or None
    return CsvImportRow(
        row_number=row_number,
        entity_type=entity_type,
        source_id=source_id,
        raw=raw,
        parent_source_id=parent_source_id,
        normalized_payload=normalized_payload,
        content_hash=content_hash,
    )
