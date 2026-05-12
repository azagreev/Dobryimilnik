from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.db import SessionLocal
from app.domains.imports.catalog_archive import build_catalog_import_csv
from app.domains.imports.repository import ImportsRepository
from app.domains.imports.service import ImportsService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import the Dobryimilnik catalog archive.")
    parser.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "doc" / "dobryimilnik_catalog.zip",
        help="Path to dobryimilnik_catalog.zip",
    )
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    csv_content, summary = build_catalog_import_csv(args.zip_path)

    async with SessionLocal() as session:
        service = ImportsService(ImportsRepository(session))
        batch = await service.run_csv_import(csv_content)
        await session.commit()

    print("Импорт каталога завершен")
    print(f"Архив: {args.zip_path}")
    print(
        "Источник: "
        f"{summary.products_csv_rows} товаров CSV, "
        f"{summary.products_json_rows} товаров JSON, "
        f"{summary.report_images_downloaded or 0} изображений из отчета"
    )
    print(
        "Батч: "
        f"{batch.batch_id} | status={batch.status.value} | "
        f"total={batch.total_rows} | staged={batch.staged_rows} | "
        f"failed={batch.failed_rows} | skipped={batch.skipped_rows}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
