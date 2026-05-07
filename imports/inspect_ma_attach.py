"""
inspect_ma_attach.py

Inspects the MA Attach workbook sheets before import.

Purpose:
- Confirm sheet structure.
- Confirm headers.
- Preview sample rows.
- Prevent incorrect column mapping before import.

Run from the project root:
    python imports/inspect_ma_attach.py
"""

from excel_reader import load_excel_workbook


WORKBOOK_NAME = "Store-Daily-Sales.xlsx"

MA_ATTACH_SHEETS = [
    "MA Attach Yesterday",
    "MA Attach PPTD",
    "MA Attach MTD",
]


def print_sheet_preview(sheet_name: str) -> None:
    """
    Print sheet dimensions, header rows, and sample rows.

    Args:
        sheet_name:
            Name of the worksheet to inspect.
    """
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    print(f"\n=== {sheet_name} ===")
    print(f"Rows: {worksheet.max_row}")
    print(f"Columns: {worksheet.max_column}")

    for row_number in range(1, 8):
        row_values = [
            worksheet.cell(row=row_number, column=column).value
            for column in range(1, worksheet.max_column + 1)
        ]

        print(f"\nRow {row_number}:")
        print(row_values)


def main() -> None:
    """
    Inspect all MA Attach sheets.
    """
    for sheet_name in MA_ATTACH_SHEETS:
        print_sheet_preview(sheet_name)


if __name__ == "__main__":
    main()