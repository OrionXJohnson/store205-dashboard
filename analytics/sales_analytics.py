"""
sales_analytics.py

Business analytics layer for store sales metrics.

This module contains dashboard-facing analytics queries and business
logic for overall sales performance.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import fetch_all, fetch_one  # noqa: E402


def get_store_sales_summary(
    store_id: int,
    period_type: str,
) -> dict | None:
    """
    Return overall store sales summary for one reporting period.

    Uses row_type = 'store_total' because this represents the workbook's
    official full-store totals.
    """
    row = fetch_one(
        """
        SELECT
            sales_metrics.sales_amount,
            sales_metrics.transaction_count,
            sales_metrics.service_plan_sales,
            sales_metrics.eset_quantity,
            sales_metrics.office_quantity
        FROM sales_metrics
        JOIN reporting_periods
            ON sales_metrics.period_id = reporting_periods.period_id
        WHERE sales_metrics.store_id = ?
          AND reporting_periods.period_type = ?
          AND sales_metrics.row_type = 'store_total';
        """,
        (store_id, period_type),
    )

    if not row:
        return None

    sales_amount = row["sales_amount"] or 0
    transaction_count = row["transaction_count"] or 0

    average_transaction = 0

    if transaction_count > 0:
        average_transaction = sales_amount / transaction_count

    return {
        "sales_amount": sales_amount,
        "transaction_count": transaction_count,
        "average_transaction": average_transaction,
        "service_plan_sales": row["service_plan_sales"] or 0,
        "eset_quantity": row["eset_quantity"] or 0,
        "office_quantity": row["office_quantity"] or 0,
    }

def get_department_sales_breakdown(
    store_id: int,
    period_type: str,
) -> list[dict]:
    """
    Return department-level sales breakdown for one store and period.

    Uses row_type = 'department_total' because those rows represent
    workbook department totals.
    """
    rows = fetch_all(
        """
        SELECT
            departments.department_code,
            departments.department_display_name,
            sales_metrics.sales_amount,
            sales_metrics.transaction_count,
            sales_metrics.service_plan_sales,
            sales_metrics.eset_quantity,
            sales_metrics.office_quantity
        FROM sales_metrics
        JOIN reporting_periods
            ON sales_metrics.period_id = reporting_periods.period_id
        JOIN departments
            ON sales_metrics.department_id = departments.department_id
        WHERE sales_metrics.store_id = ?
          AND reporting_periods.period_type = ?
          AND sales_metrics.row_type = 'department_total'
        ORDER BY sales_metrics.sales_amount DESC;
        """,
        (store_id, period_type),
    )

    return [
        {
            "department_code": row["department_code"],
            "department_name": (
                row["department_display_name"]
                or row["department_code"]
            ),
            "sales_amount": row["sales_amount"] or 0,
            "transaction_count": row["transaction_count"] or 0,
            "service_plan_sales": row["service_plan_sales"] or 0,
            "eset_quantity": row["eset_quantity"] or 0,
            "office_quantity": row["office_quantity"] or 0,
        }
        for row in rows
    ]

def get_no_sales_id_summary(
    store_id: int,
    period_type: str,
) -> dict | None:
    """
    Return No Sales ID / unattributed sales summary.

    This compares the no_sales_id row against the store_total row so the
    dashboard can show how much of store sales are unattributed.
    """
    row = fetch_one(
        """
        SELECT
            no_sales.sales_amount AS no_sales_amount,
            no_sales.transaction_count AS no_sales_transactions,
            store_total.sales_amount AS store_sales_amount,
            store_total.transaction_count AS store_transactions
        FROM sales_metrics AS no_sales
        JOIN reporting_periods
            ON no_sales.period_id = reporting_periods.period_id
        JOIN sales_metrics AS store_total
            ON no_sales.store_id = store_total.store_id
           AND no_sales.period_id = store_total.period_id
        WHERE no_sales.store_id = ?
          AND reporting_periods.period_type = ?
          AND no_sales.row_type = 'no_sales_id'
          AND store_total.row_type = 'store_total';
        """,
        (store_id, period_type),
    )

    if not row:
        return None

    no_sales_amount = row["no_sales_amount"] or 0
    no_sales_transactions = row["no_sales_transactions"] or 0
    store_sales_amount = row["store_sales_amount"] or 0
    store_transactions = row["store_transactions"] or 0

    sales_share = 0
    transaction_share = 0

    if store_sales_amount > 0:
        sales_share = no_sales_amount / store_sales_amount

    if store_transactions > 0:
        transaction_share = no_sales_transactions / store_transactions

    return {
        "store_id": store_id,
        "period_type": period_type,
        "no_sales_amount": no_sales_amount,
        "no_sales_transactions": no_sales_transactions,
        "store_sales_amount": store_sales_amount,
        "store_transactions": store_transactions,
        "sales_share": sales_share,
        "transaction_share": transaction_share,
    }

def get_store_sales_rank(
    store_id: int,
    period_type: str,
    metric: str = "sales_amount",
) -> dict:
    """
    Return a store's rank for a sales metric.

    Supported metrics:
    - sales_amount
    - transaction_count
    - average_transaction
    - no_sales_share

    Notes:
    - Higher sales, transactions, and average transaction rank higher.
    - Higher no_sales_share also ranks higher, but this should be interpreted
      as operational exposure, not necessarily positive performance.
    """
    allowed_metrics = {
        "sales_amount",
        "transaction_count",
        "average_transaction",
        "no_sales_share",
    }

    if metric not in allowed_metrics:
        raise ValueError(
            f"Unsupported metric: {metric}. "
            f"Allowed metrics: {sorted(allowed_metrics)}"
        )

    rows = fetch_all(
        """
        SELECT
            store_total.store_id,
            store_total.sales_amount,
            store_total.transaction_count,
            no_sales.sales_amount AS no_sales_amount
        FROM sales_metrics AS store_total
        JOIN reporting_periods
            ON store_total.period_id = reporting_periods.period_id
        LEFT JOIN sales_metrics AS no_sales
            ON store_total.store_id = no_sales.store_id
           AND store_total.period_id = no_sales.period_id
           AND no_sales.row_type = 'no_sales_id'
        WHERE reporting_periods.period_type = ?
          AND store_total.row_type = 'store_total'
          AND store_total.sales_amount > 0;
        """,
        (period_type,),
    )

    ranked_stores = []

    for row in rows:
        sales_amount = row["sales_amount"] or 0
        transaction_count = row["transaction_count"] or 0
        no_sales_amount = row["no_sales_amount"] or 0

        average_transaction = 0
        no_sales_share = 0

        if transaction_count > 0:
            average_transaction = sales_amount / transaction_count

        if sales_amount > 0:
            no_sales_share = no_sales_amount / sales_amount

        metric_values = {
            "sales_amount": sales_amount,
            "transaction_count": transaction_count,
            "average_transaction": average_transaction,
            "no_sales_share": no_sales_share,
        }

        ranked_stores.append(
            {
                "store_id": row["store_id"],
                "metric_value": metric_values[metric],
            }
        )

    ranked_stores.sort(
        key=lambda store: store["metric_value"],
        reverse=True,
    )

    total_stores = len(ranked_stores)

    for index, store in enumerate(ranked_stores, start=1):
        if store["store_id"] == store_id:
            return {
                "store_id": store_id,
                "period_type": period_type,
                "metric": metric,
                "rank": index,
                "total_stores": total_stores,
                "metric_value": store["metric_value"],
                "found": True,
            }

    return {
        "store_id": store_id,
        "period_type": period_type,
        "metric": metric,
        "rank": None,
        "total_stores": total_stores,
        "metric_value": 0,
        "found": False,
    }

def get_store_sales_comparison(
    period_type: str,
    limit: int = 10,
    order_by: str = "sales_amount",
) -> list[dict]:
    """
    Return store-level sales comparison for one reporting period.

    Args:
        period_type:
            Reporting period type.

        limit:
            Maximum number of stores to return.

        order_by:
            Metric used for sorting.
            Supported values:
            - sales_amount
            - transaction_count
            - average_transaction
            - no_sales_share
    """
    allowed_order_fields = {
        "sales_amount",
        "transaction_count",
        "average_transaction",
        "no_sales_share",
    }

    if order_by not in allowed_order_fields:
        raise ValueError(
            f"Unsupported order_by value: {order_by}. "
            f"Allowed values: {sorted(allowed_order_fields)}"
        )

    rows = fetch_all(
        """
        SELECT
            store_total.store_id,
            stores.store_name,
            store_total.sales_amount,
            store_total.transaction_count,
            store_total.service_plan_sales,
            store_total.eset_quantity,
            store_total.office_quantity,
            no_sales.sales_amount AS no_sales_amount,
            no_sales.transaction_count AS no_sales_transactions
        FROM sales_metrics AS store_total
        JOIN reporting_periods
            ON store_total.period_id = reporting_periods.period_id
        JOIN stores
            ON store_total.store_id = stores.store_id
        LEFT JOIN sales_metrics AS no_sales
            ON store_total.store_id = no_sales.store_id
           AND store_total.period_id = no_sales.period_id
           AND no_sales.row_type = 'no_sales_id'
        WHERE reporting_periods.period_type = ?
          AND store_total.row_type = 'store_total'
          AND store_total.sales_amount > 0;
        """,
        (period_type,),
    )

    store_rows = []

    for row in rows:
        sales_amount = row["sales_amount"] or 0
        transaction_count = row["transaction_count"] or 0
        no_sales_amount = row["no_sales_amount"] or 0
        no_sales_transactions = row["no_sales_transactions"] or 0

        average_transaction = 0
        no_sales_share = 0
        no_sales_transaction_share = 0

        if transaction_count > 0:
            average_transaction = sales_amount / transaction_count
            no_sales_transaction_share = (
                no_sales_transactions / transaction_count
            )

        if sales_amount > 0:
            no_sales_share = no_sales_amount / sales_amount

        store_rows.append(
            {
                "store_id": row["store_id"],
                "store_name": row["store_name"],
                "sales_amount": sales_amount,
                "transaction_count": transaction_count,
                "average_transaction": average_transaction,
                "service_plan_sales": row["service_plan_sales"] or 0,
                "eset_quantity": row["eset_quantity"] or 0,
                "office_quantity": row["office_quantity"] or 0,
                "no_sales_amount": no_sales_amount,
                "no_sales_transactions": no_sales_transactions,
                "no_sales_share": no_sales_share,
                "no_sales_transaction_share": no_sales_transaction_share,
            }
        )

    store_rows.sort(
        key=lambda store: store[order_by],
        reverse=True,
    )

    return store_rows[:limit]