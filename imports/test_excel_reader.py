"""
test_excel_reader.py

Tests workbook loading utilities.
"""

from excel_reader import (
    get_sheet_names,
    load_excel_workbook,
)


def main() -> None:
    """
    Load workbook and print sheet names.
    """
    workbook = load_excel_workbook(
        "Store-Daily-Sales.xlsx"
    )

    sheet_names = get_sheet_names(workbook)

    print("Workbook loaded successfully.\n")

    print("Sheets:")
    for sheet_name in sheet_names:
        print(f"- {sheet_name}")


if __name__ == "__main__":
    main()