"""
inspect_sales_totals.py

Inspects Store 205 sales total rows before building dashboard-facing
sales analytics.

Run from project root:
    python analytics/inspect_sales_totals.py
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import fetch_all  # noqa: E402


def main() -> None:
    """Inspect Store 205 sales rows grouped by row type and period."""
    rows = fetch_all(
        """
        SELECT
            reporting_periods.period_type,
            sales_metrics.row_type,
            COUNT(*) AS row_count,
            SUM(sales_metrics.sales_amount) AS total_sales,
            SUM(sales_metrics.transaction_count) AS total_transactions,
            SUM(sales_metrics.service_plan_sales) AS service_plan_sales,
            SUM(sales_metrics.eset_quantity) AS eset_quantity,
            SUM(sales_metrics.office_quantity) AS office_quantity
        FROM sales_metrics
        JOIN reporting_periods
            ON sales_metrics.period_id = reporting_periods.period_id
        WHERE sales_metrics.store_id = 205
        GROUP BY
            reporting_periods.period_type,
            sales_metrics.row_type
        ORDER BY
            reporting_periods.period_type,
            sales_metrics.row_type;
        """
    )

    print("Store 205 Sales Totals Inspection")
    print("---------------------------------")

    for row in rows:
        print(
            f"{row['period_type']} | "
            f"{row['row_type']} | "
            f"Rows: {row['row_count']} | "
            f"Sales: ${row['total_sales'] or 0:,.2f} | "
            f"Transactions: {row['total_transactions'] or 0} | "
            f"SP Sales: ${row['service_plan_sales'] or 0:,.2f} | "
            f"ESET Qty: {row['eset_quantity'] or 0} | "
            f"Office Qty: {row['office_quantity'] or 0}"
        )


if __name__ == "__main__":
    main()