"""
validate_ma_attach_import.py

Validates imported MA Attach data.

Run from project root:
    python database/validate_ma_attach_import.py
"""

from db_helper import fetch_all, fetch_one


def print_total_rows() -> None:
    """Print total imported MA Attach rows."""
    row = fetch_one(
        """
        SELECT COUNT(*) AS row_count
        FROM ma_attach_metrics;
        """
    )

    print(f"Total MA Attach rows: {row['row_count']}")


def print_rows_by_period() -> None:
    """Print MA Attach row counts by reporting period."""
    rows = fetch_all(
        """
        SELECT
            reporting_periods.period_type,
            COUNT(*) AS row_count
        FROM ma_attach_metrics
        JOIN reporting_periods
            ON ma_attach_metrics.period_id = reporting_periods.period_id
        GROUP BY reporting_periods.period_type
        ORDER BY reporting_periods.period_type;
        """
    )

    print("\nRows by period:")
    for row in rows:
        print(f"- {row['period_type']}: {row['row_count']}")


def print_rows_by_type() -> None:
    """Print MA Attach row counts by row type."""
    rows = fetch_all(
        """
        SELECT
            row_type,
            COUNT(*) AS row_count
        FROM ma_attach_metrics
        GROUP BY row_type
        ORDER BY row_type;
        """
    )

    print("\nRows by type:")
    for row in rows:
        print(f"- {row['row_type']}: {row['row_count']}")


def print_store205_summary() -> None:
    """Print Store 205 MA Attach summary."""
    row = fetch_one(
        """
        SELECT
            COUNT(*) AS row_count,
            SUM(computers) AS total_computers,
            AVG(upt) AS average_upt,
            SUM(attach_revenue) AS total_attach_revenue,
            SUM(attach_gm) AS total_attach_gm
        FROM ma_attach_metrics
        WHERE store_id = 205
          AND row_type = 'associate';
        """
    )

    print("\nStore 205 associate MA Attach summary:")
    print(f"- Rows: {row['row_count']}")
    print(f"- Computers: {row['total_computers'] or 0}")
    print(f"- Average UPT: {row['average_upt'] or 0:,.2f}")
    print(f"- Attach revenue: ${row['total_attach_revenue'] or 0:,.2f}")
    print(f"- Attach GM$: ${row['total_attach_gm'] or 0:,.2f}")


def print_import_batches() -> None:
    """Print MA Attach import batch history."""
    rows = fetch_all(
        """
        SELECT
            import_batch_id,
            source_sheet_name,
            period_type,
            row_count,
            imported_at
        FROM import_batches
        WHERE source_sheet_name LIKE 'MA Attach%'
        ORDER BY import_batch_id;
        """
    )

    print("\nMA Attach import batches:")
    for row in rows:
        print(
            f"- Batch {row['import_batch_id']}: "
            f"{row['source_sheet_name']} | "
            f"{row['period_type']} | "
            f"{row['row_count']} rows | "
            f"{row['imported_at']}"
        )


def main() -> None:
    """Run all MA Attach validation checks."""
    print("MA Attach Import Validation")
    print("---------------------------")

    print_total_rows()
    print_rows_by_period()
    print_rows_by_type()
    print_store205_summary()
    print_import_batches()


if __name__ == "__main__":
    main()