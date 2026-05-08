"""
ma_attach_analytics.py

Business analytics layer for MA Attach metrics.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import fetch_all, fetch_one  # noqa: E402


# Note:
# MA Attach percentile fields have different workbook meanings by row type.
# - associate rows store decimal percentile values from 0.0 to ~1.0
# - store rows store rank positions such as 1, 8, 20, 29
# Keep raw workbook values unchanged in the backend.

def get_ma_attach_store_summary(
    store_id: int,
    period_type: str,
) -> dict | None:
    """Return MA Attach store summary for one reporting period."""
    row = fetch_one(
        """
        SELECT
            ma_attach_metrics.computers,
            ma_attach_metrics.upt,
            ma_attach_metrics.attach_revenue,
            ma_attach_metrics.attach_gm,
            ma_attach_metrics.eset_quantity,
            ma_attach_metrics.office_quantity,
            ma_attach_metrics.service_plan_quantity,
            ma_attach_metrics.eset_attach_revenue_per_pc,
            ma_attach_metrics.office_attach_revenue_per_pc,
            ma_attach_metrics.service_plan_attach_revenue_per_pc,
            ma_attach_metrics.attach_gm_percentile,
            ma_attach_metrics.eset_percentile,
            ma_attach_metrics.office_percentile,
            ma_attach_metrics.service_plan_percentile
        FROM ma_attach_metrics
        JOIN reporting_periods
            ON ma_attach_metrics.period_id = reporting_periods.period_id
        WHERE ma_attach_metrics.store_id = ?
          AND reporting_periods.period_type = ?
          AND ma_attach_metrics.row_type = 'store';
        """,
        (store_id, period_type),
    )

    if not row:
        return None

    return {
        "store_id": store_id,
        "period_type": period_type,
        "computers": row["computers"] or 0,
        "upt": row["upt"] or 0,
        "attach_revenue": row["attach_revenue"] or 0,
        "attach_gm": row["attach_gm"] or 0,
        "eset_quantity": row["eset_quantity"] or 0,
        "office_quantity": row["office_quantity"] or 0,
        "service_plan_quantity": row["service_plan_quantity"] or 0,
        "eset_attach_revenue_per_pc": (
            row["eset_attach_revenue_per_pc"] or 0
        ),
        "office_attach_revenue_per_pc": (
            row["office_attach_revenue_per_pc"] or 0
        ),
        "service_plan_attach_revenue_per_pc": (
            row["service_plan_attach_revenue_per_pc"] or 0
        ),
        "attach_gm_percentile": row["attach_gm_percentile"] or 0,
        "eset_percentile": row["eset_percentile"] or 0,
        "office_percentile": row["office_percentile"] or 0,
        "service_plan_percentile": row["service_plan_percentile"] or 0,
    }


def get_top_ma_attach_associates(
    store_id: int,
    period_type: str,
    limit: int = 5,
    order_by: str = "attach_revenue",
    minimum_computers: int = 1,
) -> list[dict]:
    """
    Return top MA Attach associates for one store and period.

    Supported order_by values:
    - attach_revenue
    - attach_gm
    - upt
    - computers
    """
    allowed_order_fields = {
        "attach_revenue",
        "attach_gm",
        "upt",
        "computers",
    }

    if order_by not in allowed_order_fields:
        raise ValueError(
            f"Unsupported order_by value: {order_by}. "
            f"Allowed values: {sorted(allowed_order_fields)}"
        )

    rows = fetch_all(
        f"""
        SELECT
            associates.first_name,
            associates.last_name,
            ma_attach_metrics.computers,
            ma_attach_metrics.upt,
            ma_attach_metrics.attach_revenue,
            ma_attach_metrics.attach_gm,
            ma_attach_metrics.eset_quantity,
            ma_attach_metrics.office_quantity,
            ma_attach_metrics.service_plan_quantity,
            ma_attach_metrics.eset_attach_revenue_per_pc,
            ma_attach_metrics.office_attach_revenue_per_pc,
            ma_attach_metrics.service_plan_attach_revenue_per_pc,
            ma_attach_metrics.attach_gm_percentile,
            ma_attach_metrics.eset_percentile,
            ma_attach_metrics.office_percentile,
            ma_attach_metrics.service_plan_percentile
        FROM ma_attach_metrics
        JOIN reporting_periods
            ON ma_attach_metrics.period_id = reporting_periods.period_id
        JOIN associates
            ON ma_attach_metrics.associate_id = associates.associate_id
        WHERE ma_attach_metrics.store_id = ?
          AND reporting_periods.period_type = ?
          AND ma_attach_metrics.row_type = 'associate'
          AND ma_attach_metrics.computers >= ?
        ORDER BY ma_attach_metrics.{order_by} DESC
        LIMIT ?;
        """,
        (store_id, period_type, minimum_computers, limit),
    )

    return [
        {
            "associate_name": (
                f"{row['first_name']} {row['last_name']}".strip()
            ),
            "computers": row["computers"] or 0,
            "upt": row["upt"] or 0,
            "attach_revenue": row["attach_revenue"] or 0,
            "attach_gm": row["attach_gm"] or 0,
            "eset_quantity": row["eset_quantity"] or 0,
            "office_quantity": row["office_quantity"] or 0,
            "service_plan_quantity": row["service_plan_quantity"] or 0,
            "eset_attach_revenue_per_pc": (
                row["eset_attach_revenue_per_pc"] or 0
            ),
            "office_attach_revenue_per_pc": (
                row["office_attach_revenue_per_pc"] or 0
            ),
            "service_plan_attach_revenue_per_pc": (
                row["service_plan_attach_revenue_per_pc"] or 0
            ),
            "attach_gm_percentile": row["attach_gm_percentile"] or 0,
            "eset_percentile": row["eset_percentile"] or 0,
            "office_percentile": row["office_percentile"] or 0,
            "service_plan_percentile": (
                row["service_plan_percentile"] or 0
            ),
        }
        for row in rows
    ]