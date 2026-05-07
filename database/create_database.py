"""
create_database.py

Creates the SQLite database and applies the schema for the Store 205
dashboard project.

Run from the project root:
    python database/create_database.py
"""

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "store205.db"
SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"


def read_schema() -> str:
    """
    Read the SQL schema file.

    Returns:
        The full SQL schema as a string.
    """
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    return SCHEMA_PATH.read_text(encoding="utf-8")


def create_database() -> None:
    """
    Create the SQLite database and apply the schema.

    SQLite creates the database file automatically when connecting.
    The schema file then creates all required tables if they do not exist.
    """
    DATA_DIR.mkdir(exist_ok=True)

    schema_sql = read_schema()

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.executescript(schema_sql)

    print(f"Database created and schema applied: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()