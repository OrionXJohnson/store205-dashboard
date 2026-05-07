"""
validate_sales_import.py

Validates the imported Daily, PPTD, MTD, and QTD sales data.

Purpose:
- Confirm sales rows imported.
- Confirm Store 205 exists in the imported data.
- Confirm row types were preserved.
- Confirm reporting periods were created.
"""

from db_helper import fetch_all, fetch_one


def print_total_sales_rows() -> None:
    """
    Print total number of imported sales metric rows.
    """
    row = fetch_one(
        """
        SELECT COUNT(*) AS row_count
        FROM sales_metrics;
        """
    )

    print(f"Total sales metric rows: {row['row_count']}")


def print_rows_by_period() -> None:
    """
    Print imported row counts by reporting period.
    """
    rows = fetch_all(
        """
        SELECT
            reporting_periods.period_type,
            COUNT(*) AS row_count
        FROM sales_metrics
        JOIN reporting_periods
            ON sales_metrics.period_id = reporting_periods.period_id
        GROUP BY reporting_periods.period_type
        ORDER BY reporting_periods.period_type;
        """
    )

    print("\nRows by period:")
    for row in rows:
        print(f"- {row['period_type']}: {row['row_count']}")


def print_rows_by_type() -> None:
    """
    Print imported row counts by workbook row type.
    """
    rows = fetch_all(
        """
        SELECT
            row_type,
            COUNT(*) AS row_count
        FROM sales_metrics
        GROUP BY row_type
        ORDER BY row_type;
        """
    )

    print("\nRows by type:")
    for row in rows:
        print(f"- {row['row_type']}: {row['row_count']}")


def print_store205_summary() -> None:
    """
    Print Store 205 imported row count and total sales.
    """
    row = fetch_one(
        """
        SELECT
            COUNT(*) AS row_count,
            SUM(sales_amount) AS total_sales
        FROM sales_metrics
        WHERE store_id = 205;
        """
    )

    total_sales = row["total_sales"] or 0

    print("\nStore 205 summary:")
    print(f"- Imported rows: {row['row_count']}")
    print(f"- Total sales across imported periods: ${total_sales:,.2f}")


def print_import_batches() -> None:
    """
    Print import batch history.
    """
    rows = fetch_all(
        """
        SELECT
            import_batch_id,
            source_sheet_name,
            period_type,
            row_count,
            imported_at
        FROM import_batches
        ORDER BY import_batch_id;
        """
    )

    print("\nImport batches:")
    for row in rows:
        print(
            f"- Batch {row['import_batch_id']}: "
            f"{row['source_sheet_name']} | "
            f"{row['period_type']} | "
            f"{row['row_count']} rows | "
            f"{row['imported_at']}"
        )


def main() -> None:
    """
    Run all validation checks.
    """
    print("Sales Import Validation")
    print("-----------------------")

    print_total_sales_rows()
    print_rows_by_period()
    print_rows_by_type()
    print_store205_summary()
    print_import_batches()


if __name__ == "__main__":
    main()