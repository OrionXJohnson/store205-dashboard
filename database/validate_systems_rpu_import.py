"""
validate_systems_rpu_import.py

Validates imported MS RPU data.

Run from project root:
    python database/validate_systems_rpu_import.py
"""

from db_helper import fetch_all, fetch_one


def print_total_rows() -> None:
    row = fetch_one(
        """
        SELECT COUNT(*) AS row_count
        FROM systems_rpu_metrics;
        """
    )

    print(f"Total MS RPU rows: {row['row_count']}")


def print_rows_by_period() -> None:
    rows = fetch_all(
        """
        SELECT
            reporting_periods.period_type,
            COUNT(*) AS row_count
        FROM systems_rpu_metrics
        JOIN reporting_periods
            ON systems_rpu_metrics.period_id = reporting_periods.period_id
        GROUP BY reporting_periods.period_type
        ORDER BY reporting_periods.period_type;
        """
    )

    print("\nRows by period:")
    for row in rows:
        print(f"- {row['period_type']}: {row['row_count']}")


def print_rows_by_type() -> None:
    rows = fetch_all(
        """
        SELECT
            row_type,
            COUNT(*) AS row_count
        FROM systems_rpu_metrics
        GROUP BY row_type
        ORDER BY row_type;
        """
    )

    print("\nRows by type:")
    for row in rows:
        print(f"- {row['row_type']}: {row['row_count']}")


def print_store205_summary() -> None:
    row = fetch_one(
        """
        SELECT
            COUNT(*) AS row_count,
            SUM(primary_units) AS total_primary_units,
            AVG(asp) AS average_asp,
            AVG(rpu) AS average_rpu,
            AVG(total_attach_rpu) AS average_attach_rpu
        FROM systems_rpu_metrics
        WHERE store_id = 205
          AND row_type = 'associate';
        """
    )

    print("\nStore 205 associate MS RPU summary:")
    print(f"- Rows: {row['row_count']}")
    print(f"- Primary units: {row['total_primary_units'] or 0}")
    print(f"- Average ASP: ${row['average_asp'] or 0:,.2f}")
    print(f"- Average RPU: ${row['average_rpu'] or 0:,.2f}")
    print(f"- Average attach RPU: ${row['average_attach_rpu'] or 0:,.2f}")


def print_import_batches() -> None:
    rows = fetch_all(
        """
        SELECT
            import_batch_id,
            source_sheet_name,
            period_type,
            row_count,
            imported_at
        FROM import_batches
        WHERE source_sheet_name LIKE 'MS RPU%'
        ORDER BY import_batch_id;
        """
    )

    print("\nMS RPU import batches:")
    for row in rows:
        print(
            f"- Batch {row['import_batch_id']}: "
            f"{row['source_sheet_name']} | "
            f"{row['period_type']} | "
            f"{row['row_count']} rows | "
            f"{row['imported_at']}"
        )


def main() -> None:
    print("MS RPU Import Validation")
    print("------------------------")

    print_total_rows()
    print_rows_by_period()
    print_rows_by_type()
    print_store205_summary()
    print_import_batches()


if __name__ == "__main__":
    main()