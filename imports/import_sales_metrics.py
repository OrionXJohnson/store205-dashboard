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

from excel_reader import load_excel_workbook

import sys

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


def safe_number(value: Any) -> float:
    """
    Convert Excel numeric values safely.

    Blank cells are treated as 0.
    """
    if value is None:
        return 0

    return float(value)


def safe_integer(value: Any) -> int:
    """
    Convert Excel integer values safely.

    Blank cells are treated as 0.
    """
    if value is None:
        return 0

    return int(value)

def try_parse_store_id(value: Any) -> int | None:
    """
    Convert a workbook store value into a store ID.

    Returns None when the row is not tied to a real store number,
    such as workbook-wide Total rows.
    """
    if value is None:
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def get_or_create_store(store_id: int) -> None:
    """
    Ensure a store exists before importing metrics.

    Only Store 205 has a confirmed district right now.
    Other stores are imported with unknown district values.
    """
    existing_store = fetch_one(
        "SELECT store_id FROM stores WHERE store_id = ?;",
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


def get_or_create_period(period_type: str) -> int:
    """
    Return the reporting period ID for the workbook report date.
    """
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
    Classify the workbook row type.
    """
    values = {
        str(value).strip().lower()
        for value in [department_code, first_name, last_name]
        if value is not None
    }

    if "total" in values:
        if department_code:
            return "department_total"

        return "store_total"

    if "no sales id" in values:
        return "no_sales_id"

    if "goal" in values:
        return "goal"

    if "minimum" in values:
        return "minimum"

    return "associate"


def create_import_batch(sheet_name: str, period_type: str) -> int:
    """
    Create an import batch record for auditability.
    """
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
            "Imported by import_sales_metrics.py",
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


def import_sales_sheet(sheet_name: str, period_type: str) -> int:
    """
    Import one sales sheet into sales_metrics.

    Returns:
        Number of rows imported.
    """
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    period_id = get_or_create_period(period_type)
    import_batch_id = create_import_batch(sheet_name, period_type)

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

        department_id = get_department_id(department_code)
        associate_id = get_or_create_associate(first_name, last_name)

        row_type = get_row_type(
            department_code,
            first_name,
            last_name,
        )

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