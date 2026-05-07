"""
inspect_workbook.py

Inspects the Store Daily Sales workbook before import.

Purpose:
- Confirm workbook sheets.
- Confirm headers.
- Preview sample rows.
- Prevent incorrect column mapping before importing data.
"""

from excel_reader import load_excel_workbook


WORKBOOK_NAME = "Store-Daily-Sales.xlsx"

SALES_SHEETS = [
    "Daily",
    "PPTD",
    "MTD",
    "QTD",
]


def print_sheet_preview(sheet_name: str) -> None:
    """
    Print header and first few data rows from a workbook sheet.

    Args:
        sheet_name:
            Name of the worksheet to inspect.
    """
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    print(f"\n=== {sheet_name} ===")
    print(f"Rows: {worksheet.max_row}")
    print(f"Columns: {worksheet.max_column}")

    print("\nTitle Row:")
    print([worksheet.cell(row=1, column=column).value for column in range(1, 23)])

    print("\nHeader Row:")
    print([worksheet.cell(row=2, column=column).value for column in range(1, 23)])

    print("\nSample Data Rows:")
    for row_number in range(3, 8):
        row_values = [
            worksheet.cell(row=row_number, column=column).value
            for column in range(1, 23)
        ]
        print(row_values)


def main() -> None:
    """
    Inspect all sales-related workbook sheets.
    """
    for sheet_name in SALES_SHEETS:
        print_sheet_preview(sheet_name)


if __name__ == "__main__":
    main()