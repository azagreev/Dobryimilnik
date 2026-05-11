from __future__ import annotations

import csv
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

        rows.append(CsvImportRow(row_number=index, entity_type=entity_type, source_id=source_id, raw=raw))

    return rows
