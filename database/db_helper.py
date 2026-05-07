"""
db_helper.py

Centralized database utilities for the Store 205 dashboard project.

Purpose:
- Provide reusable database connection logic.
- Prevent duplicated SQLite connection code.
- Improve maintainability and consistency across the project.

Design philosophy:
- All database access should go through this module.
- Business logic should NOT directly manage SQLite connections.
- Queries should remain readable and centralized.
"""

import sqlite3
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "store205.db"


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.

    Returns:
        sqlite3.Connection: Active SQLite connection object.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    # Enables dictionary-style row access.
    connection.row_factory = sqlite3.Row

    # Ensure foreign keys are enforced.
    connection.execute("PRAGMA foreign_keys = ON;")

    return connection


def execute_query(
    query: str,
    parameters: tuple[Any, ...] = ()
) -> None:
    """
    Execute INSERT, UPDATE, DELETE, or schema modification queries.

    Args:
        query:
            SQL query string.

        parameters:
            Tuple of parameter values for the query.
    """
    with get_connection() as connection:
        connection.execute(query, parameters)
        connection.commit()


def fetch_all(
    query: str,
    parameters: tuple[Any, ...] = ()
) -> list[sqlite3.Row]:
    """
    Execute a SELECT query and return all rows.

    Args:
        query:
            SQL SELECT query.

        parameters:
            Tuple of parameter values for the query.

    Returns:
        List of SQLite rows.
    """
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchall()


def fetch_one(
    query: str,
    parameters: tuple[Any, ...] = ()
) -> sqlite3.Row | None:
    """
    Execute a SELECT query and return a single row.

    Args:
        query:
            SQL SELECT query.

        parameters:
            Tuple of parameter values for the query.

    Returns:
        Single SQLite row or None.
    """
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchone()
    
def execute_many(
    query: str,
    parameter_list: list[tuple[Any, ...]]
) -> None:
    """
    Execute the same SQL query for multiple rows.

    Args:
        query:
            SQL query string.

        parameter_list:
            List of parameter tuples.
    """
    with get_connection() as connection:
        connection.executemany(query, parameter_list)
        connection.commit()