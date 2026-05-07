"""
verify_database.py

Checks that the Store 205 database was created and seeded correctly.

Run from the project root:
    python database/verify_database.py
"""

from db_helper import fetch_all, fetch_one


def print_table_count(table_name: str) -> None:
    """
    Print the number of records in a table.

    Args:
        table_name:
            Name of the database table to check.
    """
    query = f"SELECT COUNT(*) AS record_count FROM {table_name};"
    row = fetch_one(query)

    print(f"{table_name}: {row['record_count']} records")


def print_departments() -> None:
    """
    Print department codes and display names.
    """
    query = """
    SELECT
        department_code,
        department_display_name
    FROM departments
    ORDER BY department_code;
    """

    departments = fetch_all(query)

    print("\nDepartments:")
    for department in departments:
        display_name = department["department_display_name"] or "Unconfirmed"
        print(f"- {department['department_code']}: {display_name}")


def run_verification() -> None:
    """
    Run all database verification checks.
    """
    print("Database Verification")
    print("---------------------")

    tables = [
        "stores",
        "departments",
        "associates",
        "reporting_periods",
        "import_batches",
        "sales_metrics",
        "systems_rpu_metrics",
        "ma_attach_metrics",
    ]

    for table in tables:
        print_table_count(table)

    print_departments()


if __name__ == "__main__":
    run_verification()