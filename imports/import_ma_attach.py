"""
import_ma_attach.py

Imports MA Attach workbook sheets into ma_attach_metrics.

Sheets imported:
- MA Attach Yesterday
- MA Attach PPTD
- MA Attach MTD

Run from project root:
    python imports/import_ma_attach.py
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from excel_reader import load_excel_workbook

import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import execute_query, fetch_one  # noqa: E402


WORKBOOK_NAME = "Store-Daily-Sales.xlsx"

MA_ATTACH_SHEETS = {
    "MA Attach Yesterday": "daily",
    "MA Attach PPTD": "pay_period_to_date",
    "MA Attach MTD": "month_to_date",
}

REPORT_DATE = "2026-04-30"


def safe_number(value: Any) -> float:
    """Convert workbook numeric values safely."""
    if value is None:
        return 0

    return float(value)


def safe_integer(value: Any) -> int:
    """Convert workbook integer values safely."""
    if value is None:
        return 0

    return int(value)


def try_parse_store_id(value: Any) -> int | None:
    """
    Convert workbook location values into store IDs.

    Returns None for non-store rows.
    """
    if value is None:
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def get_or_create_store(store_id: int) -> None:
    """Ensure a store exists before importing metrics."""
    existing_store = fetch_one(
        """
        SELECT store_id
        FROM stores
        WHERE store_id = ?;
        """,
        (store_id,),
    )

    if existing_store:
        return

    district_number = 3 if store_id == 205 else None

    execute_query(
        """
        INSERT INTO stores (
            store_id,
            store_name,
            district_number,
            store_type
        )
        VALUES (?, ?, ?, ?);
        """,
        (
            store_id,
            f"Store {store_id}",
            district_number,
            "Retail",
        ),
    )


def get_or_create_period(period_type: str) -> int:
    """Get or create reporting period row."""
    existing_period = fetch_one(
        """
        SELECT period_id
        FROM reporting_periods
        WHERE report_date = ?
          AND period_type = ?;
        """,
        (REPORT_DATE, period_type),
    )

    if existing_period:
        return existing_period["period_id"]

    execute_query(
        """
        INSERT INTO reporting_periods (
            report_date,
            period_type
        )
        VALUES (?, ?);
        """,
        (REPORT_DATE, period_type),
    )

    new_period = fetch_one(
        """
        SELECT period_id
        FROM reporting_periods
        WHERE report_date = ?
          AND period_type = ?;
        """,
        (REPORT_DATE, period_type),
    )

    return new_period["period_id"]


def get_or_create_associate(
    first_name: str | None,
    last_name: str | None,
) -> int | None:
    """
    Create or retrieve an associate by first and last name.

    MA Attach sheets do not appear to provide employee codes.
    """
    if not first_name or not last_name:
        return None

    existing_associate = fetch_one(
        """
        SELECT associate_id
        FROM associates
        WHERE first_name = ?
          AND last_name = ?
          AND employee_code IS NULL;
        """,
        (first_name, last_name),
    )

    if existing_associate:
        return existing_associate["associate_id"]

    execute_query(
        """
        INSERT INTO associates (
            first_name,
            last_name,
            employee_code
        )
        VALUES (?, ?, NULL);
        """,
        (first_name, last_name),
    )

    new_associate = fetch_one(
        """
        SELECT associate_id
        FROM associates
        WHERE first_name = ?
          AND last_name = ?
          AND employee_code IS NULL;
        """,
        (first_name, last_name),
    )

    return new_associate["associate_id"]


def create_import_batch(
    sheet_name: str,
    period_type: str,
) -> int:
    """Create import batch tracking row."""
    execute_query(
        """
        INSERT INTO import_batches (
            source_file_name,
            source_sheet_name,
            report_date,
            period_type,
            notes
        )
        VALUES (?, ?, ?, ?, ?);
        """,
        (
            WORKBOOK_NAME,
            sheet_name,
            REPORT_DATE,
            period_type,
            "Imported by import_ma_attach.py",
        ),
    )

    batch = fetch_one(
        """
        SELECT import_batch_id
        FROM import_batches
        ORDER BY import_batch_id DESC
        LIMIT 1;
        """
    )

    return batch["import_batch_id"]


def normalize_row_type(value: Any) -> str:
    """
    Normalize the workbook row type.

    Column 19 usually contains values such as Associate.
    """
    if value is None:
        return "unknown"

    return str(value).strip().lower().replace(" ", "_")


def import_ma_attach_sheet(
    sheet_name: str,
    period_type: str,
) -> int:
    """Import one MA Attach sheet."""
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    period_id = get_or_create_period(period_type)
    import_batch_id = create_import_batch(sheet_name, period_type)

    imported_rows = 0

    # Rows 1-5 are titles/group headers. Data starts at row 6.
    for row_number in range(6, worksheet.max_row + 1):
        store_value = worksheet.cell(row=row_number, column=1).value
        store_id = try_parse_store_id(store_value)

        if store_id is None:
            continue

        last_name = worksheet.cell(row=row_number, column=2).value
        first_name = worksheet.cell(row=row_number, column=3).value
        row_type_value = worksheet.cell(row=row_number, column=19).value

        get_or_create_store(store_id)

        associate_id = get_or_create_associate(
            first_name,
            last_name,
        )

        execute_query(
            """
            INSERT INTO ma_attach_metrics (
                import_batch_id,
                store_id,
                associate_id,
                period_id,
                row_type,
                computers,
                upt,
                attach_revenue,
                attach_gm,
                eset_quantity,
                office_quantity,
                service_plan_quantity,
                eset_attach_revenue_per_pc,
                office_attach_revenue_per_pc,
                service_plan_attach_revenue_per_pc,
                attach_gm_percentile,
                eset_percentile,
                office_percentile,
                service_plan_percentile
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?
            );
            """,
            (
                import_batch_id,
                store_id,
                associate_id,
                period_id,
                normalize_row_type(row_type_value),
                safe_integer(worksheet.cell(row=row_number, column=4).value),
                safe_number(worksheet.cell(row=row_number, column=5).value),
                safe_number(worksheet.cell(row=row_number, column=6).value),
                safe_number(worksheet.cell(row=row_number, column=7).value),
                safe_integer(worksheet.cell(row=row_number, column=8).value),
                safe_integer(worksheet.cell(row=row_number, column=9).value),
                safe_integer(worksheet.cell(row=row_number, column=10).value),
                safe_number(worksheet.cell(row=row_number, column=11).value),
                safe_number(worksheet.cell(row=row_number, column=12).value),
                safe_number(worksheet.cell(row=row_number, column=13).value),
                safe_number(worksheet.cell(row=row_number, column=14).value),
                safe_number(worksheet.cell(row=row_number, column=15).value),
                safe_number(worksheet.cell(row=row_number, column=16).value),
                safe_number(worksheet.cell(row=row_number, column=17).value),
            ),
        )

        imported_rows += 1

    execute_query(
        """
        UPDATE import_batches
        SET row_count = ?
        WHERE import_batch_id = ?;
        """,
        (imported_rows, import_batch_id),
    )

    return imported_rows


def main() -> None:
    """Import all MA Attach workbook sheets."""
    start_time = datetime.now()

    print("Starting MA Attach import...\n")

    for sheet_name, period_type in MA_ATTACH_SHEETS.items():
        row_count = import_ma_attach_sheet(sheet_name, period_type)
        print(f"{sheet_name}: imported {row_count} rows")

    elapsed_time = datetime.now() - start_time

    print("\nMA Attach import complete.")
    print(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()