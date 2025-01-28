import os
import pandas as pd


def tr12_transform_to_probability(selected_files, base_dir="statista_data"):
    """
    Convert occurrences in columns to percentages relative to their corresponding "_ Base" column.
    """

    def process_function(xls):
        sheet_data = {}

        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet, header=1)

            # Identify "_ Base" columns
            base_columns_corrected = [col for col in df.columns if "_ Base" in col]

            # Convert all relevant columns to numeric where possible (ignoring non-numeric data)
            data_numeric = df.apply(pd.to_numeric, errors="coerce")

            # Process each "_ Base" column group again with numeric values
            for i, base_col in enumerate(base_columns_corrected):
                # Get the base column values
                base_values_corrected = data_numeric[base_col]

                # Determine the range of columns to process (between consecutive "_ Base" columns)
                if i < len(base_columns_corrected) - 1:
                    group_columns_corrected = data_numeric.columns[
                        data_numeric.columns.get_loc(base_col)
                        + 1 : data_numeric.columns.get_loc(
                            base_columns_corrected[i + 1]
                        )
                    ]
                else:
                    group_columns_corrected = data_numeric.columns[
                        data_numeric.columns.get_loc(base_col) + 1 :
                    ]

                # Convert occurrences to percentages
                for col in group_columns_corrected:
                    data_numeric[col] = (
                        data_numeric[col] / base_values_corrected
                    ) * 100

            # Store the transformed DataFrame for this sheet
            sheet_data[sheet] = data_numeric

        return sheet_data

    def process_files(files, base_dir, process_function):
        all_data = {}

        for file in files:
            file_path = os.path.join(base_dir, file)

            if os.path.exists(file_path):
                with pd.ExcelFile(file_path) as xls:
                    print(f"Processing file: {file}")
                    all_data[file] = process_function(xls)
            else:
                print(f"File not found: {file_path}")

        return all_data

    # Process only files with "adv" in their filenames
    advanced_files = [
        file for file in selected_files if "adv" in os.path.basename(file).lower()
    ]
    return process_files(advanced_files, base_dir, process_function)


# Main program
if __name__ == "__main__":
    input_file = "European Football Benchmark in Italy 2023 adv.xlsx"
    base_directory = "statista_data"  # Adjust this if needed

    # Ensure the base directory exists
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # Move the input file to the base directory if needed
    input_file_path = os.path.join(base_directory, input_file)
    if not os.path.exists(input_file_path):
        print(f"Error: File '{input_file}' not found in directory '{base_directory}'.")
    else:
        # Process the file
        processed_data = tr12_transform_to_probability(
            [input_file], base_dir=base_directory
        )

        # Save processed data
        for file, sheets in processed_data.items():
            output_dir = os.path.join(base_directory, "processed")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for sheet_name, df in sheets.items():
                output_file = os.path.join(
                    output_dir, f"{os.path.splitext(file)[0]}_{sheet_name}.csv"
                )
                df.to_csv(output_file, index=False)
                print(f"Saved processed sheet '{sheet_name}' to '{output_file}'")
