import pandas as pd


def calculate_sheet_score(file_path):
    # Read the Excel file
    lookup_sheets = [
        "overview",
        "content",
        "characteristics & demographics",
        "demographics",
    ]  # consider only 3 options
    lookup_columns = ["Age", "Gender"]

    excel_data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets

    sheet_score = 0
    column_score = 0

    # Iterate through all sheets in the Excel file
    for sheet_name, df in excel_data.items():
        # Check if the sheet name matches the lookup sheets
        if sheet_name.lower() in lookup_sheets:
            sheet_score += 1.0  # Add points for matching sheet name
            continue  # Skip to the next sheet since it matched a lookup sheet

        # If the sheet doesn't match a lookup sheet, look for columns in the table
        lookup_row = df.iloc[
            0
        ].tolist()  # Get the row under the header (assuming it's the first row after headers)

        for cell in lookup_row:
            if isinstance(cell, str):  # Ensure the cell contains a string
                for column in lookup_columns:
                    if cell.lower().startswith(
                        column.lower()
                    ):  # Compare using .startswith
                        column_score += 0.5  # Add points for matching column name
                        break  # Stop checking other columns for this cell

    num_data_sheets = len(excel_data.items()) - (len(lookup_sheets) - 1)

    total_score = (
        (sheet_score / (len(lookup_sheets) - 1)) + (column_score / num_data_sheets)
    ) / 2
    print(total_score)
    return total_score
