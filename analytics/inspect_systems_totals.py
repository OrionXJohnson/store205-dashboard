"""
inspect_systems_totals.py

Inspects Store 205 Systems RPU store_total rows before building
dashboard-facing analytics.

Run from project root:
    python analytics/inspect_systems_totals.py
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import fetch_all  # noqa: E402


def main() -> None:
    rows = fetch_all(
        """
        SELECT
            reporting_periods.period_type,
            systems_rpu_metrics.store_id,
            systems_rpu_metrics.row_type,
            systems_rpu_metrics.primary_units,
            systems_rpu_metrics.asp,
            systems_rpu_metrics.rpu,
            systems_rpu_metrics.total_attach_units,
            systems_rpu_metrics.total_attach_rpu,
            systems_rpu_metrics.service_plans_attach_percent,
            systems_rpu_metrics.eset_attach_percent,
            systems_rpu_metrics.office_attach_percent,
            systems_rpu_metrics.monitors_attach_percent,
            systems_rpu_metrics.mice_keyboard_attach_percent,
            systems_rpu_metrics.all_other_attach_percent
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        WHERE systems_rpu_metrics.store_id = 205
          AND systems_rpu_metrics.row_type = 'store_total'
        ORDER BY reporting_periods.period_type;
        """
    )

    print("Store 205 Systems Store Total Rows")
    print("----------------------------------")

    if not rows:
        print("No store_total rows found for Store 205.")
        return

    for row in rows:
        print(f"\nPeriod: {row['period_type']}")
        print(f"Primary units: {row['primary_units']}")
        print(f"ASP: ${row['asp']:,.2f}")
        print(f"RPU: ${row['rpu']:,.2f}")
        print(f"Total attach units: {row['total_attach_units']}")
        print(f"Total attach RPU: ${row['total_attach_rpu']:,.2f}")
        print(f"Service plans attach: {row['service_plans_attach_percent']:.2%}")
        print(f"ESET attach: {row['eset_attach_percent']:.2%}")
        print(f"Office attach: {row['office_attach_percent']:.2%}")
        print(f"Monitors attach: {row['monitors_attach_percent']:.2%}")
        print(f"Mice/keyboard attach: {row['mice_keyboard_attach_percent']:.2%}")
        print(f"All other attach: {row['all_other_attach_percent']:.2%}")


if __name__ == "__main__":
    main()