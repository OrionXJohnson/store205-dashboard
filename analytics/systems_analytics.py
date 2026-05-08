"""
systems_analytics.py

Dashboard-ready analytics for Systems RPU metrics.

Important:
- Store KPI cards use workbook store_total rows.
- Associate rankings use associate rows.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import fetch_all, fetch_one  # noqa: E402


def get_store_systems_summary(store_id: int, period_type: str) -> dict:
    """
    Return workbook-aligned Systems summary metrics for one store.

    This uses row_type = 'store_total' so dashboard KPI cards match
    the workbook’s store-level totals instead of averaging associates.
    """
    row = fetch_one(
        """
        SELECT
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
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        WHERE systems_rpu_metrics.store_id = ?
          AND reporting_periods.period_type = ?
          AND systems_rpu_metrics.row_type = 'store_total'
        LIMIT 1;
        """,
        (store_id, period_type),
    )

    if row is None:
        return {
            "store_id": store_id,
            "period_type": period_type,
            "found": False,
        }

    return {
        "store_id": store_id,
        "period_type": period_type,
        "found": True,
        "primary_units": row["primary_units"] or 0,
        "asp": row["asp"] or 0,
        "rpu": row["rpu"] or 0,
        "total_attach_units": row["total_attach_units"] or 0,
        "total_attach_rpu": row["total_attach_rpu"] or 0,
        "service_plans_attach_percent": row["service_plans_attach_percent"] or 0,
        "eset_attach_percent": row["eset_attach_percent"] or 0,
        "office_attach_percent": row["office_attach_percent"] or 0,
        "monitors_attach_percent": row["monitors_attach_percent"] or 0,
        "mice_keyboard_attach_percent": row["mice_keyboard_attach_percent"] or 0,
        "all_other_attach_percent": row["all_other_attach_percent"] or 0,
    }

def get_top_rpu_associates(
    store_id: int,
    period_type: str,
    limit: int = 10,
) -> list[dict]:
    """
    Return top Systems associates by RPU for one store and period.

    This uses row_type = 'associate' because leaderboards should be based
    on individual associate performance, not store totals.
    """
    rows = fetch_all(
        """
        SELECT
            associates.first_name,
            associates.last_name,
            systems_rpu_metrics.primary_units,
            systems_rpu_metrics.asp,
            systems_rpu_metrics.rpu,
            systems_rpu_metrics.total_attach_rpu,
            systems_rpu_metrics.service_plans_attach_percent,
            systems_rpu_metrics.eset_attach_percent,
            systems_rpu_metrics.office_attach_percent
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        JOIN associates
            ON systems_rpu_metrics.associate_id = associates.associate_id
        WHERE systems_rpu_metrics.store_id = ?
          AND reporting_periods.period_type = ?
          AND systems_rpu_metrics.row_type = 'associate'
          AND systems_rpu_metrics.primary_units > 0
        ORDER BY systems_rpu_metrics.rpu DESC
        LIMIT ?;
        """,
        (store_id, period_type, limit),
    )

    return [
        {
            "associate_name": f"{row['first_name']} {row['last_name']}",
            "primary_units": row["primary_units"] or 0,
            "asp": row["asp"] or 0,
            "rpu": row["rpu"] or 0,
            "total_attach_rpu": row["total_attach_rpu"] or 0,
            "service_plans_attach_percent": row["service_plans_attach_percent"] or 0,
            "eset_attach_percent": row["eset_attach_percent"] or 0,
            "office_attach_percent": row["office_attach_percent"] or 0,
        }
        for row in rows
    ]

def get_top_attach_rpu_associates(
    store_id: int,
    period_type: str,
    limit: int = 10,
    minimum_primary_units: int = 3,
) -> list[dict]:
    """
    Return top Systems associates by attach RPU.

    Args:
        store_id:
            Store number.

        period_type:
            Reporting period type.

        limit:
            Maximum number of associates to return.

        minimum_primary_units:
            Minimum primary units required to appear in the ranking.
            This prevents very low-volume associates from skewing results.
    """
    rows = fetch_all(
        """
        SELECT
            associates.first_name,
            associates.last_name,
            systems_rpu_metrics.primary_units,
            systems_rpu_metrics.asp,
            systems_rpu_metrics.rpu,
            systems_rpu_metrics.total_attach_rpu,
            systems_rpu_metrics.service_plans_attach_percent,
            systems_rpu_metrics.eset_attach_percent,
            systems_rpu_metrics.office_attach_percent,
            systems_rpu_metrics.monitors_attach_percent
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        JOIN associates
            ON systems_rpu_metrics.associate_id = associates.associate_id
        WHERE systems_rpu_metrics.store_id = ?
          AND reporting_periods.period_type = ?
          AND systems_rpu_metrics.row_type = 'associate'
          AND systems_rpu_metrics.primary_units >= ?
        ORDER BY systems_rpu_metrics.total_attach_rpu DESC
        LIMIT ?;
        """,
        (
            store_id,
            period_type,
            minimum_primary_units,
            limit,
        ),
    )

    return [
        {
            "associate_name": f"{row['first_name']} {row['last_name']}",
            "primary_units": row["primary_units"] or 0,
            "asp": row["asp"] or 0,
            "rpu": row["rpu"] or 0,
            "total_attach_rpu": row["total_attach_rpu"] or 0,
            "service_plans_attach_percent": row["service_plans_attach_percent"] or 0,
            "eset_attach_percent": row["eset_attach_percent"] or 0,
            "office_attach_percent": row["office_attach_percent"] or 0,
            "monitors_attach_percent": row["monitors_attach_percent"] or 0,
        }
        for row in rows
    ]

def get_store_rpu_comparison(
    period_type: str,
    limit: int = 20,
) -> list[dict]:
    """
    Return store-level Systems RPU comparison for a reporting period.

    Uses row_type = 'store_total' so each store is compared using the
    workbook's official store-level totals.
    """
    rows = fetch_all(
        """
        SELECT
            systems_rpu_metrics.store_id,
            stores.store_name,
            systems_rpu_metrics.primary_units,
            systems_rpu_metrics.asp,
            systems_rpu_metrics.rpu,
            systems_rpu_metrics.total_attach_rpu,
            systems_rpu_metrics.service_plans_attach_percent,
            systems_rpu_metrics.eset_attach_percent,
            systems_rpu_metrics.office_attach_percent
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        JOIN stores
            ON systems_rpu_metrics.store_id = stores.store_id
        WHERE reporting_periods.period_type = ?
          AND systems_rpu_metrics.row_type = 'store_total'
          AND systems_rpu_metrics.primary_units > 0
        ORDER BY systems_rpu_metrics.rpu DESC
        LIMIT ?;
        """,
        (period_type, limit),
    )

    return [
        {
            "store_id": row["store_id"],
            "store_name": row["store_name"],
            "primary_units": row["primary_units"] or 0,
            "asp": row["asp"] or 0,
            "rpu": row["rpu"] or 0,
            "total_attach_rpu": row["total_attach_rpu"] or 0,
            "service_plans_attach_percent": row["service_plans_attach_percent"] or 0,
            "eset_attach_percent": row["eset_attach_percent"] or 0,
            "office_attach_percent": row["office_attach_percent"] or 0,
        }
        for row in rows
    ]

def get_store_systems_rank(
    store_id: int,
    period_type: str,
    metric: str = "rpu",
) -> dict:
    """
    Return a store's rank for a Systems metric.

    Args:
        store_id:
            Store number to rank.

        period_type:
            Reporting period type.

        metric:
            Metric to rank by.
            Supported values:
            - rpu
            - total_attach_rpu
            - asp
            - primary_units
    """
    allowed_metrics = {
        "rpu",
        "total_attach_rpu",
        "asp",
        "primary_units",
    }

    if metric not in allowed_metrics:
        raise ValueError(
            f"Unsupported metric: {metric}. "
            f"Allowed metrics: {sorted(allowed_metrics)}"
        )

    rows = fetch_all(
        f"""
        SELECT
            systems_rpu_metrics.store_id,
            systems_rpu_metrics.{metric} AS metric_value
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        WHERE reporting_periods.period_type = ?
          AND systems_rpu_metrics.row_type = 'store_total'
          AND systems_rpu_metrics.primary_units > 0
        ORDER BY systems_rpu_metrics.{metric} DESC;
        """,
        (period_type,),
    )

    total_stores = len(rows)

    for index, row in enumerate(rows, start=1):
        if row["store_id"] == store_id:
            return {
                "store_id": store_id,
                "period_type": period_type,
                "metric": metric,
                "rank": index,
                "total_stores": total_stores,
                "metric_value": row["metric_value"] or 0,
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