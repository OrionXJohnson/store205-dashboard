"""
inspect_total_attach_columns.py

Inspects raw Total Attach columns from the MS RPU workbook section.

Purpose:
- Confirm whether column 19 should really be treated as total attach units.
- Compare imported database values against raw workbook-like structure.

Run from project root:
    python analytics/inspect_total_attach_columns.py
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import fetch_all  # noqa: E402


def main() -> None:
    """Inspect Store 205 MS RPU Total Attach fields."""
    rows = fetch_all(
        """
        SELECT
            reporting_periods.period_type,
            associates.first_name,
            associates.last_name,
            systems_rpu_metrics.row_type,
            systems_rpu_metrics.primary_units,
            systems_rpu_metrics.total_attach_units,
            systems_rpu_metrics.total_attach_rpu,
            systems_rpu_metrics.service_plans_attach_percent,
            systems_rpu_metrics.eset_attach_percent,
            systems_rpu_metrics.office_attach_percent
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        LEFT JOIN associates
            ON systems_rpu_metrics.associate_id = associates.associate_id
        WHERE systems_rpu_metrics.store_id = 205
          AND reporting_periods.period_type = 'month_to_date'
        ORDER BY
            systems_rpu_metrics.row_type DESC,
            systems_rpu_metrics.total_attach_rpu DESC;
        """
    )

    print("Store 205 MTD Total Attach Inspection")
    print("------------------------------------")

    for row in rows:
        name = "STORE TOTAL"

        if row["first_name"] and row["last_name"]:
            name = f"{row['first_name']} {row['last_name']}"

        print(
            f"{name} | "
            f"Type: {row['row_type']} | "
            f"Primary Units: {row['primary_units']} | "
            f"Attach Units: {row['total_attach_units']} | "
            f"Attach RPU: ${row['total_attach_rpu']:,.2f} | "
            f"SP: {row['service_plans_attach_percent']:.2%} | "
            f"ESET: {row['eset_attach_percent']:.2%} | "
            f"Office: {row['office_attach_percent']:.2%}"
        )


if __name__ == "__main__":
    main()