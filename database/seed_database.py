"""
seed_database.py

Seeds verified lookup data for the Store 205 dashboard database.

Purpose:
- Insert confirmed store records.
- Insert department codes found in the Store Daily Sales workbook.
- Avoid inserting fake metric data.

Important:
Metric data should come from Excel import scripts, not seed data.
"""

from db_helper import execute_query


def seed_stores() -> None:
    """
    Insert confirmed store records.

    Store 205 is confirmed as part of District 3.
    """
    stores = [
        (205, "Store 205", 3, "Retail"),
    ]

    query = """
    INSERT OR IGNORE INTO stores (
        store_id,
        store_name,
        district_number,
        store_type
    )
    VALUES (?, ?, ?, ?);
    """

    for store in stores:
        execute_query(query, store)

    print("Stores seeded successfully.")


def seed_departments() -> None:
    """
    Insert department records from the Store Daily Sales workbook.

    Unknown display names are intentionally stored as NULL.
    """
    departments = [
        ("AD", None),
        ("BS", None),
        ("BY", "Build Your Own"),
        ("CE", "Consumer Electronics"),
        ("GS", "General Sales"),
        ("MA", "Apple"),
        ("MS", "Systems"),
        ("OP", "Operations"),
        ("OPF", None),
        ("OPW", None),
        ("OTH", None),
        ("RS", None),
        ("SE", "Service"),
        ("SPU", None),
    ]

    query = """
    INSERT OR IGNORE INTO departments (
        department_code,
        department_display_name
    )
    VALUES (?, ?);
    """

    for department in departments:
        execute_query(query, department)

    print("Departments seeded successfully.")


def run_seed_operations() -> None:
    """
    Run all lookup-table seed operations.
    """
    seed_stores()
    seed_departments()

    print("Database seeding complete.")


if __name__ == "__main__":
    run_seed_operations()