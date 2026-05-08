"""
rebuild_and_validate.py

Rebuilds the Store 205 analytics database from scratch, imports workbook data,
and runs validation/test scripts in the correct order.

Run from project root:
    python scripts/rebuild_and_validate.py
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "store205.db"


COMMANDS = [
    ["python", "database/create_database.py"],
    ["python", "database/seed_database.py"],
    ["python", "imports/import_sales_metrics.py"],
    ["python", "imports/import_systems_rpu.py"],
    ["python", "imports/import_ma_attach.py"],
    ["python", "database/verify_database.py"],
    ["python", "database/validate_sales_import.py"],
    ["python", "database/validate_systems_rpu_import.py"],
    ["python", "database/validate_ma_attach_import.py"],
    ["python", "analytics/test_sales_analytics.py"],
    ["python", "analytics/test_systems_analytics.py"],
    ["python", "analytics/test_ma_attach_analytics.py"],
]


def run_command(command: list[str]) -> None:
    """Run one project command and stop if it fails."""
    print("\n" + "=" * 80)
    print(f"Running: {' '.join(command)}")
    print("=" * 80)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=False,
    )

    if result.returncode != 0:
        print("\nERROR: Command failed.")
        print(f"Failed command: {' '.join(command)}")
        sys.exit(result.returncode)


def delete_existing_database() -> None:
    """Delete existing SQLite database if present."""
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
        print(f"Deleted existing database: {DATABASE_PATH}")
    else:
        print("No existing database found. Creating a fresh one.")


def main() -> None:
    """Run full rebuild, import, validation, and analytics test pipeline."""
    print("Store 205 Rebuild and Validation Pipeline")
    print("-----------------------------------------")

    delete_existing_database()

    for command in COMMANDS:
        run_command(command)

    print("\n" + "=" * 80)
    print("Rebuild and validation completed successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main()