"""
import_sales_metrics.py

Imports Daily, PPTD, MTD, and QTD sales rows from the Store Daily Sales
workbook into the sales_metrics table.

This importer preserves both:
- associate-level rows
- workbook total/special rows

Run from the project root:
    python imports/import_sales_metrics.py
"""

from datetime import datetime
from pathlib import Path
from typing import Any
import sys

from excel_reader import load_excel_workbook
from import_helpers import (
    REPORT_DATE,
    WORKBOOK_NAME,
    create_import_batch,
    get_or_create_period,
    get_or_create_store,
    safe_integer,
    safe_number,
    try_parse_store_id,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"
sys.path.append(str(DATABASE_DIR))

from db_helper import execute_query, fetch_one  # noqa: E402


WORKBOOK_NAME = "Store-Daily-Sales.xlsx"

SALES_SHEETS = {
    "Daily": "daily",
    "PPTD": "pay_period_to_date",
    "MTD": "month_to_date",
    "QTD": "quarter_to_date",
}

# The workbook is dated 04/30/26.
REPORT_DATE = "2026-04-30"


def get_department_id(department_code: str | None) -> int | None:
    """
    Return the database ID for a department code.

    Blank department cells are allowed for total/special rows.
    """
    if not department_code:
        return None

    department = fetch_one(
        """
        SELECT department_id
        FROM departments
        WHERE department_code = ?;
        """,
        (department_code,),
    )

    if department:
        return department["department_id"]

    execute_query(
        """
        INSERT INTO departments (
            department_code,
            department_display_name
        )
        VALUES (?, NULL);
        """,
        (department_code,),
    )

    new_department = fetch_one(
        """
        SELECT department_id
        FROM departments
        WHERE department_code = ?;
        """,
        (department_code,),
    )

    return new_department["department_id"]


def get_or_create_associate(
    first_name: str | None,
    last_name: str | None,
) -> int | None:
    """
    Create or find an associate by first and last name.

    Returns None for total/special rows without a normal associate name.
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


def get_row_type(
    department_code: str | None,
    first_name: str | None,
    last_name: str | None,
) -> str:
    """
    Classify the workbook row type for sales sheets.
    """
    department_value = str(department_code).strip().lower() if department_code else ""
    first_value = str(first_name).strip().lower() if first_name else ""
    last_value = str(last_name).strip().lower() if last_name else ""

    if department_value == "total":
        return "store_total"

    if last_value == "no sales id":
        return "no_sales_id"

    if first_value == "total" and not department_value:
        return "no_sales_total"

    if first_value == "total" and department_value:
        return "department_total"

    return "associate"


def import_sales_sheet(sheet_name: str, period_type: str) -> int:
    """
    Import one sales sheet into sales_metrics.

    Returns:
        Number of rows imported.
    """
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    period_id = get_or_create_period(period_type)
    import_batch_id = create_import_batch(
        sheet_name=sheet_name,
        period_type=period_type,
        importer_name="import_sales_metrics.py",
    )

    imported_rows = 0

    for row_number in range(3, worksheet.max_row + 1):
        store_value = worksheet.cell(row=row_number, column=1).value

        if store_value is None:
            continue

        store_id = try_parse_store_id(store_value)

        if store_id is None:
            continue
        department_code = worksheet.cell(row=row_number, column=2).value
        first_name = worksheet.cell(row=row_number, column=3).value
        last_name = worksheet.cell(row=row_number, column=4).value

        get_or_create_store(store_id)
        
        associate_id = get_or_create_associate(first_name, last_name)

        row_type = get_row_type(
            department_code,
            first_name,
            last_name,
        )

        department_id = None

        if row_type in {"associate", "department_total"}:
            department_id = get_department_id(department_code)

        associate_id = get_or_create_associate(first_name, last_name)

        execute_query(
            """
            INSERT INTO sales_metrics (
                import_batch_id,
                store_id,
                department_id,
                associate_id,
                period_id,
                row_type,
                sales_amount,
                transaction_count,
                service_plan_quantity,
                service_plan_sales,
                service_plan_percent,
                rank_value,
                nordvpn_quantity,
                nordvpn_sales,
                eset_quantity,
                eset_percent,
                eset_perm_gm_per_unit,
                office_quantity,
                office_ratio,
                priority_care_quantity,
                priority_care_ratio,
                service_quantity,
                service_upt,
                service_gm_per_unit
            )
            VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            );
            """,
            (
                import_batch_id,
                store_id,
                department_id,
                associate_id,
                period_id,
                row_type,
                safe_number(worksheet.cell(row=row_number, column=5).value),
                safe_integer(worksheet.cell(row=row_number, column=6).value),
                safe_integer(worksheet.cell(row=row_number, column=7).value),
                safe_number(worksheet.cell(row=row_number, column=8).value),
                safe_number(worksheet.cell(row=row_number, column=9).value),
                worksheet.cell(row=row_number, column=10).value,
                safe_integer(worksheet.cell(row=row_number, column=11).value),
                safe_number(worksheet.cell(row=row_number, column=12).value),
                safe_integer(worksheet.cell(row=row_number, column=13).value),
                safe_number(worksheet.cell(row=row_number, column=14).value),
                safe_number(worksheet.cell(row=row_number, column=15).value),
                safe_integer(worksheet.cell(row=row_number, column=16).value),
                safe_number(worksheet.cell(row=row_number, column=17).value),
                safe_integer(worksheet.cell(row=row_number, column=18).value),
                safe_number(worksheet.cell(row=row_number, column=19).value),
                safe_integer(worksheet.cell(row=row_number, column=20).value),
                safe_number(worksheet.cell(row=row_number, column=21).value),
                safe_number(worksheet.cell(row=row_number, column=22).value),
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
    """
    Import all sales metric sheets.
    """
    start_time = datetime.now()

    print("Starting sales metrics import...\n")

    for sheet_name, period_type in SALES_SHEETS.items():
        row_count = import_sales_sheet(sheet_name, period_type)
        print(f"{sheet_name}: imported {row_count} rows")

    elapsed_time = datetime.now() - start_time

    print("\nSales metrics import complete.")
    print(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()