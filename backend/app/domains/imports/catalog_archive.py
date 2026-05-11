from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from zipfile import ZipFile

CATALOG_PRODUCTS_CSV = "products_catalog.csv"
CATALOG_PRODUCTS_JSON = "products_final.json"
CATALOG_REPORT = "REPORT.txt"

IMPORT_FIELDNAMES = (
    "entity_type",
    "source_id",
    "name",
    "slug",
    "price",
    "source_url",
    "media_url",
    "price_raw",
    "is_hit",
    "in_stock",
    "availability",
    "description",
    "seo_title",
    "seo_description",
)

TOTAL_PRODUCTS_RE = re.compile(r"Total products parsed:\s*([0-9,]+)")


@dataclass(frozen=True)
class CatalogArchiveSummary:
    products_csv_rows: int
    products_json_rows: int
    report_total_products: int | None
    report_images_downloaded: int | None


def build_catalog_import_csv(zip_path: Path) -> tuple[str, CatalogArchiveSummary]:
    with ZipFile(zip_path) as archive:
        csv_text = _read_archive_text(archive, CATALOG_PRODUCTS_CSV)
        json_rows = _read_products_json(archive)
        report_text = _read_archive_text(archive, CATALOG_REPORT)

    csv_rows = list(csv.DictReader(io.StringIO(csv_text)))
    report_total_products, report_images_downloaded = _parse_report_counts(report_text)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=IMPORT_FIELDNAMES)
    writer.writeheader()

    for raw_row in csv_rows:
        source_id = raw_row["ID"].strip()
        extra = json_rows.get(source_id, {})
        writer.writerow(_build_import_row(raw_row, extra))

    summary = CatalogArchiveSummary(
        products_csv_rows=len(csv_rows),
        products_json_rows=len(json_rows),
        report_total_products=report_total_products,
        report_images_downloaded=report_images_downloaded,
    )
    _validate_summary(summary)
    return output.getvalue(), summary


def _read_archive_text(archive: ZipFile, name: str) -> str:
    return archive.read(name).decode("utf-8-sig")


def _read_products_json(archive: ZipFile) -> dict[str, dict[str, object]]:
    rows = json.loads(_read_archive_text(archive, CATALOG_PRODUCTS_JSON))
    return {str(row["id"]): row for row in rows}


def _parse_report_counts(report_text: str) -> tuple[int | None, int | None]:
    total_products_match = TOTAL_PRODUCTS_RE.search(report_text)
    total_products = (
        int(total_products_match.group(1).replace(",", "")) if total_products_match else None
    )

    images_downloaded = None
    for line in report_text.splitlines():
        if line.startswith("Images downloaded:"):
            images_value = line.split(":", 1)[1].strip().split(" files", 1)[0]
            images_downloaded = int(images_value.replace(",", ""))
            break

    return total_products, images_downloaded


def _validate_summary(summary: CatalogArchiveSummary) -> None:
    if (
        summary.report_total_products is not None
        and summary.report_total_products != summary.products_csv_rows
    ):
        raise ValueError(
            "Archive report count does not match catalog CSV row count: "
            f"{summary.report_total_products} != {summary.products_csv_rows}"
        )

    if summary.products_json_rows != summary.products_csv_rows:
        raise ValueError(
            "products_final.json row count does not match products_catalog.csv row count: "
            f"{summary.products_json_rows} != {summary.products_csv_rows}"
        )


def _build_import_row(
    raw_row: dict[str, str],
    extra: dict[str, object],
) -> dict[str, str]:
    source_id = raw_row["ID"].strip()
    name = raw_row["Name"].strip()
    price = raw_row["Price (₽)"].strip()
    source_url = _string_value(extra.get("url")) or raw_row["Product URL"].strip()
    media_url = _string_value(extra.get("thumbnail")) or raw_row["Image URL"].strip()
    description = _string_value(extra.get("description")) or raw_row.get("Description", "").strip()
    price_raw = _string_value(extra.get("price_raw")) or price
    is_hit = _bool_text(extra.get("is_hit"), raw_row.get("Hit", ""))
    in_stock = _bool_text(extra.get("in_stock"), raw_row.get("In Stock", ""))
    availability = _string_value(extra.get("availability")) or raw_row.get("In Stock", "").strip()
    slug = _slug_from_url(source_url) or source_id

    return {
        "entity_type": "product",
        "source_id": source_id,
        "name": name,
        "slug": slug,
        "price": price,
        "source_url": source_url,
        "media_url": media_url,
        "price_raw": price_raw,
        "is_hit": is_hit,
        "in_stock": in_stock,
        "availability": availability,
        "description": description,
        "seo_title": name,
        "seo_description": description,
    }


def _slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    match = re.search(r"/item/\d+-(.+)$", path)
    if match:
        return match.group(1)
    return path.rsplit("/", 1)[-1]


def _bool_text(*values: object) -> str:
    for value in values:
        if value is None:
            continue
        text = str(value).strip().lower()
        if not text:
            continue
        if text in {"yes", "true", "1", "да", "y"}:
            return "true"
        if text in {"no", "false", "0", "нет", "n"}:
            return "false"
    return ""


def _string_value(value: object | None) -> str:
    if value is None:
        return ""
    return str(value).strip()
