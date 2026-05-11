from __future__ import annotations

import csv
import json
from pathlib import Path
from zipfile import ZipFile

from app.domains.imports.catalog_archive import build_catalog_import_csv


def _write_fixture_archive(path: Path) -> None:
    products_csv = (
        "ID,Name,Price (₽),In Stock,Hit,Description,Image URL,Product URL\n"
        "55285732,\"Отдушка Ginger, patchouli\",170,Yes,Yes,Описание 1,https://example.test/image-1.jpg,https://www.livemaster.ru/item/55285732-materialy-dlya-tvorchestva-otdushka-ginger-patchouli\n"
        "55261186,Отдушка Розовый сироп,256,No,No,Описание 2,https://example.test/image-2.jpg,https://www.livemaster.ru/item/55261186-materialy-dlya-tvorchestva-otdushka-rozovyj-sirop\n"
    )
    products_json = [
        {
            "id": "55285732",
            "name": "Отдушка Ginger, patchouli",
            "price": "170",
            "price_raw": "170₽Отдушка Ginger, patchouli",
            "url": "https://www.livemaster.ru/item/55285732-materialy-dlya-tvorchestva-otdushka-ginger-patchouli",
            "is_hit": True,
            "in_stock": True,
            "thumbnail": "https://example.test/image-1.jpg",
            "description": "Описание 1",
            "availability": "В наличии",
        },
        {
            "id": "55261186",
            "name": "Отдушка Розовый сироп",
            "price": "256",
            "price_raw": "256₽Отдушка Розовый сироп",
            "url": "https://www.livemaster.ru/item/55261186-materialy-dlya-tvorchestva-otdushka-rozovyj-sirop",
            "is_hit": False,
            "in_stock": False,
            "thumbnail": "https://example.test/image-2.jpg",
            "description": "Описание 2",
            "availability": "Нет в наличии",
        },
    ]
    report = (
        "Total products parsed: 2\n"
        "Images downloaded: 2 files (1.0 MB)\n"
    )

    with ZipFile(path, "w") as archive:
        archive.writestr("products_catalog.csv", products_csv)
        archive.writestr("products_final.json", json.dumps(products_json, ensure_ascii=False))
        archive.writestr("REPORT.txt", report)


def test_build_catalog_import_csv_normalizes_archive_rows(tmp_path: Path) -> None:
    archive_path = tmp_path / "dobryimilnik_catalog.zip"
    _write_fixture_archive(archive_path)

    csv_content, summary = build_catalog_import_csv(archive_path)
    rows = list(csv.DictReader(csv_content.splitlines()))

    assert summary.products_csv_rows == 2
    assert summary.products_json_rows == 2
    assert summary.report_total_products == 2
    assert summary.report_images_downloaded == 2
    assert len(rows) == 2
    assert rows[0]["entity_type"] == "product"
    assert rows[0]["source_id"] == "55285732"
    assert rows[0]["source_url"].endswith("otdushka-ginger-patchouli")
    assert rows[0]["media_url"] == "https://example.test/image-1.jpg"
    assert rows[0]["is_hit"] == "true"
    assert rows[0]["in_stock"] == "true"
    assert rows[1]["name"] == "Отдушка Розовый сироп"
    assert rows[1]["availability"] == "Нет в наличии"
