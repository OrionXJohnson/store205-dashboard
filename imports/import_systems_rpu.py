"""
import_systems_rpu.py

Imports MS RPU workbook sheets into systems_rpu_metrics.

Sheets imported:
- MS RPU Yesterday
- MS RPU MTD
- MS RPU PPTD

Purpose:
- Preserve associate-level Systems performance metrics.
- Preserve workbook row types where possible.
- Support future Systems dashboard analytics.

Run from project root:
    python imports/import_systems_rpu.py
"""

from datetime import datetime
from pathlib import Path
import sys

from excel_reader import load_excel_workbook
from import_helpers import (
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

MS_RPU_SHEETS = {
    "MS RPU Yesterday": "daily",
    "MS RPU MTD": "month_to_date",
    "MS RPU PPTD": "pay_period_to_date",
}

REPORT_DATE = "2026-04-30"


def get_or_create_associate(
    first_name: str | None,
    last_name: str | None,
    employee_code: str | None,
) -> int | None:
    """
    Create or retrieve associate record.
    """
    if not first_name or not last_name:
        return None

    existing_associate = fetch_one(
        """
        SELECT associate_id
        FROM associates
        WHERE employee_code = ?;
        """,
        (employee_code,),
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
        VALUES (?, ?, ?);
        """,
        (
            first_name,
            last_name,
            employee_code,
        ),
    )

    new_associate = fetch_one(
        """
        SELECT associate_id
        FROM associates
        WHERE employee_code = ?;
        """,
        (employee_code,),
    )

    return new_associate["associate_id"]


def get_row_type(last_name: str | None) -> str:
    """
    Determine workbook row type.
    """
    if not last_name:
        return "unknown"

    value = str(last_name).strip().lower()

    if value == "goal":
        return "goal"

    if value == "minimum":
        return "minimum"

    if value == "total":
        return "store_total"

    return "associate"


def import_ms_rpu_sheet(
    sheet_name: str,
    period_type: str,
) -> int:
    """
    Import one MS RPU sheet.
    """
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    period_id = get_or_create_period(period_type)

    import_batch_id = create_import_batch(
        sheet_name=sheet_name,
        period_type=period_type,
        importer_name="import_systems_rpu.py",
    )

    imported_rows = 0

    for row_number in range(4, worksheet.max_row + 1):
        store_value = worksheet.cell(row=row_number, column=9).value

        store_id = try_parse_store_id(store_value)

        # Skip workbook-wide goal/minimum rows for now.
        if store_id is None:
            continue

        last_name = worksheet.cell(row=row_number, column=10).value
        first_name = worksheet.cell(row=row_number, column=11).value
        employee_code = worksheet.cell(row=row_number, column=12).value

        row_type = get_row_type(last_name)

        get_or_create_store(store_id)

        associate_id = get_or_create_associate(
            first_name,
            last_name,
            employee_code,
        )

        execute_query(
            """
            INSERT INTO systems_rpu_metrics (
                import_batch_id,
                store_id,
                associate_id,
                period_id,
                row_type,
                primary_units,
                asp,
                rpu,
                total_attach_units,
                total_attach_rpu,
                service_plans_attach_percent,
                eset_attach_percent,
                office_attach_percent,
                monitors_attach_percent,
                mice_keyboard_attach_percent,
                all_other_attach_percent
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            );
            """,
            (
                import_batch_id,
                store_id,
                associate_id,
                period_id,
                row_type,
                safe_integer(
                    worksheet.cell(row=row_number, column=14).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=15).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=17).value
                ),
                safe_integer(
                    worksheet.cell(row=row_number, column=19).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=20).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=23).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=27).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=31).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=35).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=39).value
                ),
                safe_number(
                    worksheet.cell(row=row_number, column=43).value
                ),
            ),
        )

        imported_rows += 1

    execute_query(
        """
        UPDATE import_batches
        SET row_count = ?
        WHERE import_batch_id = ?;
        """,
        (
            imported_rows,
            import_batch_id,
        ),
    )

    return imported_rows


def main() -> None:
    """
    Import all MS RPU workbook sheets.
    """
    start_time = datetime.now()

    print("Starting MS RPU import...\n")

    for sheet_name, period_type in MS_RPU_SHEETS.items():
        row_count = import_ms_rpu_sheet(
            sheet_name,
            period_type,
        )

        print(f"{sheet_name}: imported {row_count} rows")

    elapsed_time = datetime.now() - start_time

    print("\nMS RPU import complete.")
    print(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()