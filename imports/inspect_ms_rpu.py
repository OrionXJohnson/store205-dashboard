"""
inspect_ms_rpu.py

Inspects the MS RPU workbook sheets before import.

Purpose:
- Confirm sheet structure.
- Confirm headers.
- Preview sample rows.
- Prevent incorrect column mapping.
"""

from excel_reader import load_excel_workbook


WORKBOOK_NAME = "Store-Daily-Sales.xlsx"

MS_RPU_SHEETS = [
    "MS RPU Yesterday",
    "MS RPU MTD",
    "MS RPU PPTD",
]


def print_sheet_preview(sheet_name: str) -> None:
    """
    Print sheet dimensions, header rows, and sample rows.
    """
    workbook = load_excel_workbook(WORKBOOK_NAME)
    worksheet = workbook[sheet_name]

    print(f"\n=== {sheet_name} ===")
    print(f"Rows: {worksheet.max_row}")
    print(f"Columns: {worksheet.max_column}")

    print("\nRow 1:")
    print([worksheet.cell(row=1, column=column).value for column in range(1, worksheet.max_column + 1)])

    print("\nRow 2:")
    print([worksheet.cell(row=2, column=column).value for column in range(1, worksheet.max_column + 1)])

    print("\nRow 3:")
    print([worksheet.cell(row=3, column=column).value for column in range(1, worksheet.max_column + 1)])

    print("\nRow 4:")
    print([worksheet.cell(row=4, column=column).value for column in range(1, worksheet.max_column + 1)])

    print("\nRow 5:")
    print([worksheet.cell(row=5, column=column).value for column in range(1, worksheet.max_column + 1)])

    print("\nRow 6:")
    print([worksheet.cell(row=6, column=column).value for column in range(1, worksheet.max_column + 1)])
    

    print("\nSample Data Rows:")
    for row_number in range(3, min(8, worksheet.max_row + 1)):
        row_values = [
            worksheet.cell(row=row_number, column=column).value
            for column in range(1, worksheet.max_column + 1)
        ]
        print(row_values)


def main() -> None:
    """
    Inspect all MS RPU sheets.
    """
    for sheet_name in MS_RPU_SHEETS:
        print_sheet_preview(sheet_name)


if __name__ == "__main__":
    main()