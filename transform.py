import os
import pandas as pd
import logging


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


def remove_overview(selected_files, base_dir="statista_data"):
    """
    Transform selected files by removing the 'Overview' sheet and save the results.
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

                if "Overview" not in sheets:
                    logging.info(
                        f"'Overview' sheet not found in {relative_path}. Skipping file."
                    )
                    continue

                sheet_data = {
                    sheet: pd.read_excel(xls, sheet_name=sheet)
                    for sheet in sheets
                    if sheet != "Overview"
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

    # Log summary of the transformation
    logging.info(
        "[Remove Overview] Selected files to transform: %d", len(selected_files)
    )
    if transformed_files:
        logging.info("[Remove Overview] Successfully saved:")
        for path in transformed_files:
            logging.info(f"    {path}")
    if errors:
        logging.error(
            "[Remove Overview] Errors occurred during transformation for the following files:"
        )
        for path in errors:
            logging.error(f"    {path}")


def remove_header_and_empty_column(selected_files, base_dir="statista_data"):
    """
    Transform selected files by removing the first header rows and the empty first column, then save the results.
    Outputs a summary log of all transformed files.
    """
    transformed_files = []
    errors = []

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

            # Read and clean the data
            with pd.ExcelFile(input_path) as xls:
                sheet_data = {}
                for sheet in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet, header=3).iloc[:, 1:]
                    sheet_data[sheet] = df

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for sheet_name, data in sheet_data.items():
                    data.to_excel(writer, sheet_name=sheet_name, index=False)

            transformed_files.append(formatted_path)

        except Exception as e:
            logging.error(
                f"An error occurred while processing file {relative_path}: {e}"
            )
            errors.append(relative_path)

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
