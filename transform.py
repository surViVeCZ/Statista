import os
import pandas as pd
import logging
import warnings
import time

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),  # Console logging
        logging.FileHandler("scraper.log", mode="w", encoding="utf-8"),  # File logging
    ],
)
log = logging.getLogger()


def format_relative_path(base_dir, full_path):
    """Format and return the relative path from the base directory."""
    try:
        return os.path.relpath(full_path, base_dir)
    except ValueError:
        return full_path


def tr1_remove_sheets(selected_files, base_dir="statista_data"):
    """
    Transform selected files by removing the 'Overview' and 'Content' sheets and save the results.
    Outputs a summary log of all transformed files.
    """
    transformed_files = []  # Store paths of successfully transformed files
    errors = []  # Store paths of files with errors

    for relative_path in selected_files:
        try:
            input_path = os.path.join(base_dir, relative_path)

            if not os.path.exists(input_path):
                logging.warning(
                    f"File not found: {relative_path}. Skipping transformation."
                )
                errors.append(relative_path)
                continue

            # transformed output directory
            parent_dir = os.path.dirname(input_path)
            transformed_dir = os.path.join(parent_dir, "transformed")
            os.makedirs(transformed_dir, exist_ok=True)

            output_path = os.path.join(transformed_dir, os.path.basename(input_path))
            formatted_path = format_relative_path(base_dir, output_path)

            # check sheets
            with pd.ExcelFile(input_path) as xls:
                sheets = xls.sheet_names

                if "Overview" not in sheets and "Content" not in sheets:
                    logging.info(
                        f"'Overview' and 'Content' sheets not found in {relative_path}. Skipping file."
                    )
                    continue

                sheet_data = {
                    sheet: pd.read_excel(xls, sheet_name=sheet)
                    for sheet in sheets
                    if sheet not in ["Overview", "Content"]
                }

            # Write the transformed data to a new Excel file
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for sheet_name, data in sheet_data.items():
                    data.to_excel(writer, sheet_name=sheet_name, index=False)

            transformed_files.append(formatted_path)

        except Exception as e:
            logging.error(
                f"An error occurred while processing file {relative_path}: {e}"
            )
            errors.append(relative_path)

    time.sleep(3)
    # Log summary of the transformation
    logging.info(
        "[Remove Overview and Content] Selected files to transform: %d",
        len(selected_files),
    )
    if transformed_files:
        logging.info("[Remove Overview and Content] Successfully saved:")
        for path in transformed_files:
            logging.info(f"    {path}")
    if errors:
        logging.error(
            "[Remove Overview and Content] Errors occurred during transformation for the following files:"
        )
        for path in errors:
            logging.error(f"    {path}")

    return transformed_files  # Return the transformed files for the next step


def tr2_remove_header_and_empty_column(selected_files, base_dir="statista_data"):
    """
    Transform selected files by cleaning headers, removing metadata rows, and dropping empty columns.
    Outputs a summary log of all transformed files.
    """
    transformed_files = []
    errors = []

    for relative_path in selected_files:
        try:
            input_path = os.path.join(base_dir, relative_path)

            # Skip files containing "adv" in the name
            if "adv" in os.path.basename(input_path).lower():
                logging.info(
                    f"Skipping file {relative_path} as it contains 'adv' in the name."
                )
                transformed_files.append(format_relative_path(base_dir, input_path))
                continue

            if not os.path.exists(input_path):
                logging.warning(
                    f"File not found: {relative_path}. Skipping transformation."
                )
                errors.append(relative_path)
                continue

            # Ensure the output path does not add another 'transformed' folder
            parent_dir = os.path.dirname(input_path)
            if parent_dir.endswith("transformed"):
                transformed_dir = parent_dir  # Use the existing 'transformed' folder
            else:
                transformed_dir = os.path.join(parent_dir, "transformed")
                os.makedirs(transformed_dir, exist_ok=True)

            output_path = os.path.join(transformed_dir, os.path.basename(input_path))
            formatted_path = format_relative_path(base_dir, output_path)

            # Read and clean the data
            with pd.ExcelFile(input_path) as xls:
                sheet_data = {}
                for sheet in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet)

                    # Step 1: Remove metadata rows (rows without numeric data)
                    valid_data_start_index = df[
                        df.apply(
                            lambda col: col.map(lambda x: isinstance(x, (int, float))),
                            axis=0,
                        ).any(axis=1)
                    ].index.min()

                    df_cleaned = df.iloc[valid_data_start_index:].reset_index(drop=True)

                    # Step 2: Use the first valid row as headers
                    df_cleaned.columns = df_cleaned.iloc[0]
                    df_cleaned = df_cleaned[1:].reset_index(drop=True)

                    # Step 3: Drop entirely empty columns
                    df_cleaned = df_cleaned.dropna(axis=1, how="all")

                    # Step 4: Replace NaN or placeholder headers
                    df_cleaned.columns = [
                        f"Column_{i}" if pd.isna(col) else col
                        for i, col in enumerate(df_cleaned.columns)
                    ]

                    sheet_data[sheet] = df_cleaned

            # Save the cleaned data to a new Excel file
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for sheet_name, data in sheet_data.items():
                    data.to_excel(writer, sheet_name=sheet_name, index=False)

            transformed_files.append(formatted_path)

        except Exception as e:
            logging.error(
                f"An error occurred while processing file {relative_path}: {e}"
            )
            errors.append(relative_path)

    time.sleep(3)
    # Log summary of the transformation
    logging.info(
        "[Remove Header and Empty Column] Selected files to transform: %d",
        len(selected_files),
    )
    if transformed_files:
        logging.info("[Remove Header and Empty Column] Successfully saved:")
        for path in transformed_files:
            logging.info(f"    {path}")
    if errors:
        logging.error(
            "[Remove Header and Empty Column] Errors occurred during transformation for the following files:"
        )
        for path in errors:
            logging.error(f"    {path}")

    return transformed_files


def pipeline_transform(selected_files, base_dir="statista_data"):
    """Run the transformation pipeline."""
    logging.info("Starting the transformation pipeline...")

    # Step 1: Remove Overview
    logging.info("Step 1: Removing Overview sheets...")
    transformed_step1 = tr1_remove_sheets(selected_files, base_dir)

    if not transformed_step1:
        logging.warning("No files to process after Step 1. Exiting pipeline.")
        return

    # Step 2: Remove header and empty columns
    logging.info("Step 2: Removing header rows and empty columns...")
    transformed_step2 = tr2_remove_header_and_empty_column(transformed_step1, base_dir)

    logging.info("Transformation pipeline completed.")
    return transformed_step2
