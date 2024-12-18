import os
import pandas as pd

def remove_overview(selected_files, base_dir="statista_data"):
    """
    Removes the sheet named 'Overview' from the selected Excel files
    and saves the transformed files into a sibling 'transformed' folder.

    Parameters:
        selected_files (list): List of file paths relative to the base directory.
        base_dir (str): Base directory containing the files and their parent folders.
    """
    for relative_path in selected_files:
        try:
            # Construct the full input file path
            input_path = os.path.join(base_dir, relative_path)
            if not os.path.exists(input_path):
                print(f"File not found: {input_path}")
                continue

            # Identify the parent directory of the file
            parent_dir = os.path.dirname(input_path)

            # Create the "transformed" directory at the same level as "topic sections"
            transformed_dir = os.path.join(parent_dir, "transformed")
            os.makedirs(transformed_dir, exist_ok=True)

            # Construct the output file path
            output_path = os.path.join(transformed_dir, os.path.basename(input_path))

            # Load the Excel file and remove the "Overview" sheet
            with pd.ExcelFile(input_path) as xls:
                sheets = xls.sheet_names

                if "Overview" not in sheets:
                    print(f"'Overview' sheet not found in {input_path}. Skipping.")
                    continue

                # Load all sheets except "Overview"
                sheet_data = {
                    sheet: pd.read_excel(xls, sheet_name=sheet)
                    for sheet in sheets if sheet != "Overview"
                }

            # Save the modified Excel file to the transformed directory
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for sheet_name, data in sheet_data.items():
                    data.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"Transformed file saved: {output_path}")

        except Exception as e:
            print(f"Error processing {relative_path}: {e}")
