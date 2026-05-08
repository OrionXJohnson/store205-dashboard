"""
inspect_sales_row_types.py

Inspects raw Store 205 sales workbook rows to understand how Total,
No Sales ID, and department total rows appear before import.

Run from project root:
    python imports/inspect_sales_row_types.py
"""

from excel_reader import load_excel_workbook


WORKBOOK_NAME = "Store-Daily-Sales.xlsx"

SALES_SHEETS = [
    "Daily",
    "PPTD",
    "MTD",
    "QTD",
]


def print_store205_rows(sheet_name: str) -> None:
    """Print raw Store 205 rows from one sales sheet."""
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    print(f"\n=== {sheet_name} ===")

    for row_number in range(1, worksheet.max_row + 1):
        store_value = worksheet.cell(row=row_number, column=1).value

        if store_value != 205:
            continue

        row_values = [
            worksheet.cell(row=row_number, column=column).value
            for column in range(1, 8)
        ]

        print(f"Row {row_number}: {row_values}")


def main() -> None:
    """Inspect Store 205 rows across sales sheets."""
    for sheet_name in SALES_SHEETS:
        print_store205_rows(sheet_name)


if __name__ == "__main__":
    main()