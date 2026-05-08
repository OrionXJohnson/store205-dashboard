"""
audit_ma_attach_percentiles.py

Audits MA Attach percentile fields to verify whether workbook rows use
decimal percentiles, whole-number percentile ranks, or mixed formats.

Run from project root:
    python analytics/audit_ma_attach_percentiles.py
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"

sys.path.append(str(DATABASE_DIR))

from db_helper import fetch_all  # noqa: E402


PERCENTILE_FIELDS = [
    "attach_gm_percentile",
    "eset_percentile",
    "office_percentile",
    "service_plan_percentile",
]


def main() -> None:
    """Print percentile ranges by row type and period."""
    print("MA Attach Percentile Audit")
    print("--------------------------")

    rows = fetch_all(
        """
        SELECT
            reporting_periods.period_type,
            ma_attach_metrics.row_type,
            COUNT(*) AS row_count,
            MIN(attach_gm_percentile) AS min_attach_gm,
            MAX(attach_gm_percentile) AS max_attach_gm,
            MIN(eset_percentile) AS min_eset,
            MAX(eset_percentile) AS max_eset,
            MIN(office_percentile) AS min_office,
            MAX(office_percentile) AS max_office,
            MIN(service_plan_percentile) AS min_service_plan,
            MAX(service_plan_percentile) AS max_service_plan
        FROM ma_attach_metrics
        JOIN reporting_periods
            ON ma_attach_metrics.period_id = reporting_periods.period_id
        GROUP BY
            reporting_periods.period_type,
            ma_attach_metrics.row_type
        ORDER BY
            reporting_periods.period_type,
            ma_attach_metrics.row_type;
        """
    )

    for row in rows:
        print()
        print(f"Period: {row['period_type']} | Row type: {row['row_type']}")
        print(f"Rows: {row['row_count']}")
        print(
            "Attach GM percentile range: "
            f"{row['min_attach_gm']} to {row['max_attach_gm']}"
        )
        print(
            "ESET percentile range: "
            f"{row['min_eset']} to {row['max_eset']}"
        )
        print(
            "Office percentile range: "
            f"{row['min_office']} to {row['max_office']}"
        )
        print(
            "Service plan percentile range: "
            f"{row['min_service_plan']} to {row['max_service_plan']}"
        )


if __name__ == "__main__":
    main()