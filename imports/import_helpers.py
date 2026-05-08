"""
import_helpers.py

Shared helper functions for workbook import scripts.

Purpose:
- Reduce duplicated importer code.
- Keep import scripts easier to maintain.
- Centralize common parsing and database lookup logic.
"""

from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import execute_query, fetch_one  # noqa: E402


WORKBOOK_NAME = "Store-Daily-Sales.xlsx"
REPORT_DATE = "2026-04-30"


def safe_number(value: Any) -> float:
    """
    Safely convert workbook values to float.

    Blank cells are treated as 0.
    """
    if value is None:
        return 0

    return float(value)


def safe_integer(value: Any) -> int:
    """
    Safely convert workbook values to int.

    Blank cells are treated as 0.
    """
    if value is None:
        return 0

    return int(value)


def try_parse_store_id(value: Any) -> int | None:
    """
    Convert workbook store/location values into store IDs.

    Returns None for non-store rows such as workbook-wide goal rows.
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

    Store 205 is confirmed as District 3.
    Other stores are imported with unknown district values until verified.
    """
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
    """
    Get or create a reporting period row.

    Returns:
        period_id for the requested period type and workbook report date.
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


def create_import_batch(
    sheet_name: str,
    period_type: str,
    importer_name: str,
) -> int:
    """
    Create an import batch tracking row.

    Args:
        sheet_name:
            Workbook sheet being imported.

        period_type:
            Reporting period type.

        importer_name:
            Name of the importer script.

    Returns:
        Newly created import_batch_id.
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
            f"Imported by {importer_name}",
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