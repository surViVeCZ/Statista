# ===========================
# IMPORTS
# ===========================
import os
import logging
from threading import Thread
from flask import Flask, send_file, abort

# Dash imports
import dash
from dash import html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State, MATCH, ALL

import plotly.express as px

# Application-specific imports
from app_layout import (
    app_layout,
    active_card_style,
    inactive_card_style,
    modern_card_hover_effect,
)
from advanced_search import (
    extract_report_results,
    download_reports,
    get_failed_reports_downloads,
)
from scraper import (
    setup_driver,
    login_with_selenium,
    search_topic,
    scrape_topic,
    get_files_to_be_downloaded,
    get_failed_downloads,
)
from transform import (
    pipeline_transform,
    tr1_remove_sheets,
    tr2_remove_header_and_empty_column,
    tr3_remove_metadata,
    tr4_reduce_empty_lines,
    tr5_removing_total_percentages_income_demography,
    tr6_append_questions,
    tr7_merging_sheets,
    tr8_join_tables,
    tr9_transpose_table,
    tr10_map_age,
    tr11_filter_advanced_files,
    tr12_transform_to_probability,
)
from metrics import calculate_sheet_score

# ===========================
# GLOBAL VARIABLES
# ===========================
log_data = []  # Log messages stored in memory
driver = None  # Web driver for scraper
session_topics = []  # Topics for the current session
selected_topic_url = None  # URL of the selected topic
selected_topic_name = None  # Name of the selected topic
downloaded_files = []  # List of downloaded files
failed_downloads = []  # List of failed downloads
files_to_be_downloaded = 0  # Count of files to download
advanced_matches = 0  # Count of advanced matches
advanced_reports = None  # Placeholder for advanced reports

# Directory for downloads
DOWNLOAD_DIR = os.path.abspath("statista_data")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize initial files at app start
initial_files = {
    os.path.relpath(os.path.join(root, filename), DOWNLOAD_DIR)
    for root, _, filenames in os.walk(DOWNLOAD_DIR)
    for filename in filenames
}

# ===========================
# HELPER FUNCTIONS
# ===========================


def SelectedTopicComponent():
    """Create the selected topic information component."""
    return html.Div(
        id="selected-topic-info",
        children="Selected Topic: None | Files to Download: 0",
        style={"margin-top": "10px", "font-weight": "bold"},
    )


def initialize_driver():
    """Initialize the Selenium web driver."""
    global driver
    driver = setup_driver()


def populate_initial_files():
    """Populate the initial files from the download directory."""
    for root, _, filenames in os.walk(DOWNLOAD_DIR):
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(root, filename), DOWNLOAD_DIR)
            initial_files.add(relative_path)


def determine_match_type(input_topic, result_topic):
    """Classify the match type based on topic similarity."""
    input_topic_lower = input_topic.lower()
    result_topic_lower = result_topic.lower()

    if input_topic_lower == result_topic_lower:
        return "Exact match"
    elif (
        input_topic_lower in result_topic_lower
        or result_topic_lower in input_topic_lower
    ):
        return "Close match"
    else:
        return "Somewhat match"


# ===========================
# CUSTOM LOGGING HANDLER
# ===========================


class DashLogger(logging.Handler):
    """Custom logging handler to store logs in the global log_data list."""

    def emit(self, record):
        global log_data
        log_data.append(self.format(record))
        if len(log_data) > 1000:  # Limit the number of logs
            log_data = log_data[-1000:]


# Configure logging
dash_handler = DashLogger()
dash_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(dash_handler)
logging.getLogger().setLevel(logging.INFO)

# ===========================
# DASH APP CONFIGURATION
# ===========================

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.config.prevent_initial_callbacks = "initial_duplicate"
app.config.suppress_callback_exceptions = (
    True  # Allow callbacks for dynamically created components
)
server = app.server

# Merge hover effect into active_card_style
active_card_style.update(modern_card_hover_effect)

# Set app layout
app.layout = app_layout

# ===========================
# INITIALIZATION LOGIC
# ===========================

# Create directories and populate initial files
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
populate_initial_files()


@app.callback(
    Output("region-selector-container", "style"),
    Input("main-tabs", "active_tab"),
)
def toggle_region_selector(active_tab):
    if active_tab == "collection":
        # Normal styling when enabled
        return {
            "display": "block",
            "opacity": "1",  # Fully visible
            "pointer-events": "auto",  # Interactive
            "filter": "none",  # No blur
            "transition": "all 0.3s ease",  # Smooth transition
        }
    elif active_tab == "transformation" or active_tab == "overview":
        # Greyed out and blurred styling when disabled
        return {
            "display": "block",
            "opacity": "0.5",  # Semi-transparent
            "pointer-events": "none",  # Non-interactive
            "filter": "blur(1px)",  # Add slight blur effect
            "transition": "all 0.3s ease",  # Smooth transition
        }
    else:
        # Hide the container for other tabs
        return {"display": "none"}


@app.callback(
    Output("region-flag-container", "children"),  # Update the flag container
    Input("region-selector", "value"),  # Watch for region selector changes
)
def update_region_flag(selected_region):
    """
    Update the flag (emoji or SVG) based on the selected region.
    """
    if selected_region == "global":
        return "Statista version🌍"  # Emoji for global
    else:
        # Return an SVG image for specific regions
        return html.Div(
            [
                "Statista version ",
                html.Img(
                    src=f"/assets/{selected_region}.svg",
                    style={
                        "height": "24px",
                        "width": "24px",
                        "margin-left": "5px",
                    },
                ),
            ],
            style={"display": "flex", "align-items": "center"},
        )


# Login callback
@app.callback(
    [
        Output("login-status", "children"),
        Output("login-status", "className"),
        Output("login-state", "data"),
    ],
    [Input("login-button", "n_clicks")],
    prevent_initial_call=True,
)
def login_action(n_clicks):
    global driver

    driver = setup_driver()

    def login_task():
        if login_with_selenium(driver):
            logging.info("Login successful.")
            return True
        else:
            logging.error("Login failed.")
            return False

    thread = Thread(target=login_task)
    thread.start()
    thread.join()

    if driver is not None:
        return "Logged in successfully.", "text-success", True
    return "Login failed.", "text-danger", False


# Activate Search card after login
@app.callback(Output("search-card", "style"), [Input("login-state", "data")])
def activate_search_card(is_logged_in):
    if is_logged_in:
        return active_card_style
    return inactive_card_style


@app.callback(
    Output("files-to-download-store", "data"),
    [
        Input("advanced-scraping-checkbox", "value"),
        State("advanced-matches-store", "data"),
        State("files-to-download-store", "data"),
    ],
    prevent_initial_call=True,
)
def handle_checkbox_toggle(checkbox_value, advanced_matches, files_to_be_downloaded):
    """
    Handle the advanced scraping checkbox toggle.
    Advanced matches are only subtracted when the checkbox changes from enabled to disabled.
    """
    checkbox_enabled = "enabled" in checkbox_value if checkbox_value else False

    # Maintain state of the checkbox between callbacks
    if not hasattr(handle_checkbox_toggle, "previous_checkbox_enabled"):
        handle_checkbox_toggle.previous_checkbox_enabled = False

    if checkbox_enabled and not handle_checkbox_toggle.previous_checkbox_enabled:
        # Checkbox was just enabled
        files_to_be_downloaded += advanced_matches
    elif not checkbox_enabled and handle_checkbox_toggle.previous_checkbox_enabled:
        # Checkbox was just disabled
        files_to_be_downloaded -= advanced_matches

    # Update the previous state
    handle_checkbox_toggle.previous_checkbox_enabled = checkbox_enabled

    return files_to_be_downloaded


@app.callback(
    Output("files-to-download-display", "children"),
    Input("files-to-download-store", "data"),
)
def update_files_to_download_display(files_to_be_downloaded):
    return f"Files to Download: {files_to_be_downloaded}"


@app.callback(
    [
        Output("search-results-container", "children"),
        Output("scrape-card", "style"),
        Output("scrape-button", "disabled"),
        Output("scrape-status", "children"),
        Output("search-button", "disabled"),
        Output("advanced-matches-store", "data"),  # Update advanced_matches
        Output("files-to-download-store", "data", allow_duplicate=True),
    ],
    [
        Input("search-button", "n_clicks"),
        Input({"type": "search-result", "index": dash.ALL}, "n_clicks"),
        Input("scrape-button", "n_clicks"),
    ],
    [
        State("topic-input", "value"),
        State("search-results-container", "children"),
        State("files-to-download-store", "data"),
        State("advanced-scraping-checkbox", "value"),
    ],
    prevent_initial_call=True,
)
def handle_search_selection_scraping(
    search_click,
    result_clicks,
    scrape_click,
    topic_input,
    current_results,
    files_to_be_downloaded,
    checkbox_value,
):
    global session_topics, selected_topic_url, selected_topic_name, driver, advanced_reports
    checkbox_enabled = "enabled" in checkbox_value if checkbox_value else False

    # Handle search
    if ctx.triggered_id == "search-button":
        topics = search_topic(topic_input)
        advanced_reports, advanced_matches = extract_report_results(driver, topic_input)
        session_topics = topics or []

        if not topics:
            logging.warning(f"No topics found for '{topic_input}'.")
            return (
                "No topics found.",
                inactive_card_style,
                True,
                "No topic selected.",
                False,
                0,  # Reset advanced_matches
                0,  # Reset files_to_be_downloaded
            )

        logging.info(f"🎉 Found {len(topics)} topics for '{topic_input}'.")

        # Sort topics by match priority
        match_priority_map = {"Exact match": 1, "Close match": 2, "Somewhat match": 3}
        temp_topics = [
            (name, url, determine_match_type(topic_input, name)) for name, url in topics
        ]
        sorted_topics = sorted(temp_topics, key=lambda x: match_priority_map[x[2]])
        session_topics = [(name, url) for (name, url, mtype) in sorted_topics]

        # Create result cards
        result_cards = []
        for idx, (name, url, match_type) in enumerate(sorted_topics):
            match_color = {
                "Exact match": "#28a745",
                "Close match": "#ffc107",
                "Somewhat match": "#dc3545",
            }.get(match_type, "#6c757d")

            result_cards.append(
                dbc.Card(
                    dbc.CardBody(
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            name,
                                            className="card-title",
                                            style={
                                                "font-weight": "bold",
                                                "font-size": "1.1em",
                                                "margin-bottom": "5px",
                                            },
                                        ),
                                        html.Div(
                                            match_type,
                                            style={
                                                "color": match_color,
                                                "font-weight": "bold",
                                                "font-size": "0.9em",
                                            },
                                        ),
                                    ],
                                    style={"flex": "1", "padding-right": "10px"},
                                ),
                                html.Div(
                                    html.Button(
                                        "Select",
                                        id={"type": "search-result", "index": idx},
                                        className="btn btn-outline-primary",
                                    ),
                                    style={"align-self": "center"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                                "justify-content": "space-between",
                            },
                        )
                    ),
                    id={"type": "result-card", "index": idx},
                    style={"margin-bottom": "10px", "padding": "8px"},
                )
            )

        return (
            result_cards,
            inactive_card_style,
            True,
            "No topic selected.",
            False,
            advanced_matches,
            0,  # Reset files_to_be_downloaded
        )

    # Handle selection
    if ctx.triggered_id and "search-result" in str(ctx.triggered_id):
        selected_index = ctx.triggered_id["index"]
        selected_topic_name, selected_topic_url = session_topics[selected_index]
        files_to_be_downloaded = get_files_to_be_downloaded(selected_topic_url) + 2
        logging.info(f"Selected topic: {selected_topic_name}")
        return (
            current_results,
            active_card_style,
            False,
            f"Selected Topic: {selected_topic_name}",
            True,
            dash.no_update,  # Keep advanced_matches unchanged
            files_to_be_downloaded,  # Update files-to-download-store
        )

    # Handle scraping
    if ctx.triggered_id == "scrape-button":
        if not selected_topic_url:
            logging.error("No topic selected for scraping.")
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                "Error: No topic selected for scraping.",
                False,
                dash.no_update,
                dash.no_update,
            )
        logging.info(f"Starting scraping for topic: {selected_topic_name}")
        scrape_topic(selected_topic_url)
        if checkbox_enabled:
            logging.info("Triggering report download due to checkbox being enabled.")
            download_reports(driver, advanced_reports, selected_topic_name)

        return (
            dash.no_update,
            dash.no_update,
            dash.no_update,
            f"Scraping started for topic: {selected_topic_name}.",
            True,
            dash.no_update,
            dash.no_update,
        )

    return (
        dash.no_update,
        inactive_card_style,
        True,
        "No topic selected.",
        False,
        dash.no_update,
        dash.no_update,
    )


@app.callback(
    [
        Output("downloaded-files-container", "children"),
        Output("progress-bar", "value"),
        Output("progress-summary", "children"),
        Output("progress-bar", "className"),
        Output("failed-downloads-container", "children"),
    ],
    [Input("file-interval", "n_intervals")],
    [State("files-to-download-store", "data")],
)
def refresh_files_and_update_progress(n_intervals, files_to_be_downloaded):
    try:
        # Ensure files_to_be_downloaded is initialized
        if files_to_be_downloaded is None or files_to_be_downloaded == 0:
            return (
                [
                    html.Div(
                        "No files available yet.",
                        style={"color": "gray", "text-align": "center"},
                    )
                ],
                0,
                "No files to download yet.",
                "",
                [
                    html.Div(
                        "No failed downloads.",
                        style={"color": "gray", "text-align": "center"},
                    )
                ],
            )

        # Get the current files in the directory, including the advanced_reports folder
        current_files = set()
        for root, _, filenames in os.walk(DOWNLOAD_DIR):
            for filename in filenames:
                relative_path = os.path.relpath(
                    os.path.join(root, filename), DOWNLOAD_DIR
                )
                current_files.add(relative_path)

        # Detect newly downloaded files
        downloaded_files = current_files - initial_files
        meaningful_extensions = {".xlsx", ".pdf", ".txt", ".csv"}
        renamed_files = [
            file
            for file in downloaded_files
            if os.path.splitext(file)[1] in meaningful_extensions
        ]

        # Include advanced files in renamed_files
        advanced_folder_path = os.path.join(DOWNLOAD_DIR, "advanced_reports")
        advanced_files = []
        if os.path.exists(advanced_folder_path):
            for root, _, filenames in os.walk(advanced_folder_path):
                for filename in filenames:
                    relative_path = os.path.relpath(
                        os.path.join(root, filename), DOWNLOAD_DIR
                    )
                    advanced_files.append(relative_path)

        renamed_files.extend(advanced_files)

        # Update progress and styled links
        downloaded_count = len(renamed_files)
        failed_count = get_failed_downloads() + get_failed_reports_downloads()

        total_processed = downloaded_count + failed_count

        if files_to_be_downloaded > 0:
            progress = (total_processed / files_to_be_downloaded) * 100
            progress = min(progress, 100)
        else:
            progress = 0

        # Format the display for downloaded files
        file_type_descriptions = {
            ".txt": "text file",
            ".pdf": "pdf report",
            ".csv": "excel table",
            ".xlsx": "excel table",
        }
        styled_links = []
        for relative_path in renamed_files:
            filename = os.path.basename(relative_path)
            file_extension = os.path.splitext(filename)[1]
            file_description = (
                "report"
                if filename.endswith("adv.xlsx")
                else file_type_descriptions.get(file_extension, "file")
            )

            # Set text color for reports to gray
            text_color = "#6c757d" if file_description == "report" else "#007bff"

            styled_links.append(
                html.Div(
                    [
                        html.A(
                            filename,
                            href=f"/download/{relative_path}",
                            target="_blank",
                            style={
                                "text-decoration": "none",
                                "color": text_color,
                                "white-space": "nowrap",
                                "overflow": "hidden",
                                "text-overflow": "ellipsis",
                                "flex": "2",
                            },
                        ),
                        html.Span(
                            f" | {file_description}",
                            style={
                                "color": "#6c757d",
                                "margin-left": "10px",
                                "font-size": "0.9em",
                                "white-space": "nowrap",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                        "align-items": "center",
                        "padding": "8px",
                        "border": "1px solid #ddd",
                        "border-radius": "8px",
                        "background-color": "#f9f9f9",
                        "font-family": "Arial, sans-serif",
                        "margin-bottom": "5px",
                    },
                )
            )

        # Progress text
        progress_text = f"{downloaded_count} succeeded, {failed_count} failed, {total_processed}/{files_to_be_downloaded} processed ({int(progress)}%)."
        failed_links = [
            html.Div(
                f"Failed to download: {url}",
                style={"color": "red", "font-weight": "bold", "margin-bottom": "5px"},
            )
            for url in failed_downloads
        ]

        return (
            styled_links,
            progress,
            progress_text,
            "bounce" if progress == 100 else "",
            failed_links
            or [
                html.Div(
                    "No failed downloads.",
                    style={"color": "gray", "text-align": "center"},
                )
            ],
        )

    except Exception as e:
        logging.error(f"Error updating files and progress: {e}")
        return (
            [
                html.Div(
                    "Error loading files.",
                    style={"color": "red", "text-align": "center"},
                )
            ],
            0,
            "Error calculating progress.",
            "",
            [
                html.Div(
                    "Error displaying failed downloads.",
                    style={"color": "red", "text-align": "center"},
                )
            ],
        )


@server.route("/download/<path:filepath>")
def download_file(filepath):
    """Serve files from the dynamically constructed paths."""
    file_path = os.path.join(DOWNLOAD_DIR, filepath)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        logging.error(f"File not found: {file_path}")
        return abort(404, description="File not found.")


# Update logs
@app.callback(Output("log-window", "children"), Input("log-interval", "n_intervals"))
def update_logs(n_intervals):
    """
    Update the log window with segmented log messages for better readability.
    """
    segmented_logs = []
    segment_delimiter = "\n" + "=" * 80 + "\n"

    # Group related log messages into segments
    current_segment = []
    for log_entry in log_data:
        if (
            "Starting" in log_entry
            or "Selected" in log_entry
            or "Analyzing" in log_entry
        ):
            if current_segment:
                segmented_logs.append("\n".join(current_segment))
                segmented_logs.append(
                    segment_delimiter
                )  # Add a delimiter between segments
                current_segment = []

        # Add the log entry to the current segment
        current_segment.append(log_entry)

    if current_segment:
        segmented_logs.append("\n".join(current_segment))

    return "\n".join(segmented_logs)


@app.callback(
    Output("transform-log-window", "children"),
    Input("log-interval", "n_intervals"),
)
def update_transform_logs(n_intervals):
    """
    Update the transform log window with segmented log messages for better readability.
    """
    segmented_logs = []
    segment_delimiter = "\n" + "=" * 80 + "\n"

    # Group related log messages into segments
    current_segment = []
    for log_entry in log_data:
        if (
            "Starting" in log_entry
            or "Selected" in log_entry
            or "Analyzing" in log_entry
        ):
            if current_segment:
                segmented_logs.append("\n".join(current_segment))
                segmented_logs.append(
                    segment_delimiter
                )  # Add a delimiter between segments
                current_segment = []

        # Add the log entry to the current segment
        current_segment.append(log_entry)

    if current_segment:
        segmented_logs.append("\n".join(current_segment))

    return "\n".join(segmented_logs)


@app.callback(
    [Output("file-tree", "children"), Output("selected-files-store", "data")],
    [
        Input("refresh-files-button", "n_clicks"),
        Input({"type": "file-entry", "file": ALL}, "n_clicks"),
        Input({"type": "folder-entry", "folder": ALL}, "n_clicks"),
    ],
    State("selected-files-store", "data"),
)
def update_file_tree_and_toggle_selection(
    refresh_clicks, file_clicks, folder_clicks, selected_files
):
    ctx = dash.callback_context
    selected_files = selected_files or []

    if not ctx.triggered:
        return parse_tree(DOWNLOAD_DIR, selected_files), selected_files

    triggered_id = ctx.triggered_id

    # Handle folder selection
    if isinstance(triggered_id, dict) and triggered_id["type"] == "folder-entry":
        folder_path = triggered_id["folder"]
        folder_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(folder_path)
            for file in files
        ]

        if all(file in selected_files for file in folder_files):
            # Deselect all files in the folder
            selected_files = [
                file for file in selected_files if file not in folder_files
            ]
        else:
            # Select all files in the folder
            selected_files.extend(
                file for file in folder_files if file not in selected_files
            )

    # Handle individual file selection
    elif isinstance(triggered_id, dict) and triggered_id["type"] == "file-entry":
        clicked_file = triggered_id["file"]
        if clicked_file in selected_files:
            selected_files.remove(clicked_file)
        else:
            selected_files.append(clicked_file)

    return parse_tree(DOWNLOAD_DIR, selected_files), selected_files


def parse_tree(path, selected_files, level=0):
    """Recursively parse folders and files, handling transformed folder and unclickable files."""
    items = []

    folder_name = os.path.basename(path)
    is_transformed_folder = folder_name.lower() == "transformed"
    is_excluded_folder = folder_name.lower() in [
        "topic sections",
        "statista_data",
        "advanced_reports",
    ]

    # Determine if all files in the folder are selected
    folder_files = [
        os.path.join(root, file) for root, _, files in os.walk(path) for file in files
    ]
    is_folder_selected = all(file in selected_files for file in folder_files)

    # Folder entry styling
    folder_style = {
        "margin-left": f"{level * 60}px",
        "padding": "5px",
        "background-color": "transparent",
        "border-radius": "5px",
        "font-weight": "bold",
        "cursor": "pointer" if not is_transformed_folder else "not-allowed",
        "display": "flex",
        "align-items": "center",
    }

    folder_children = [
        html.Span(
            "📂",
            style={
                "margin-right": "10px",
                "font-size": "1.2em",
                "color": "#007bff" if is_folder_selected else "#333",
            },
        ),
        html.Span(folder_name),
    ]

    # Add "Select All" button only if the folder is not excluded
    if not is_transformed_folder and not is_excluded_folder:
        folder_children.append(
            html.Button(
                "Select All" if not is_folder_selected else "Deselect All",
                id={"type": "folder-entry", "folder": path},
                style={
                    "margin-left": "10px",
                    "background-color": (
                        "#007bff" if not is_folder_selected else "#dc3545"
                    ),
                    "color": "white",
                    "border": "none",
                    "cursor": "pointer",
                    "border-radius": "5px",
                    "padding": "5px 10px",
                    "font-size": "0.9em",
                },
            )
        )

    items.append(html.Div(folder_children, style=folder_style))

    # Add files and subfolders
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            # Recursively parse subfolders
            items.extend(parse_tree(item_path, selected_files, level=level + 1))
        else:
            # Check if the file is in the transformed folder or unclickable
            file_extension = os.path.splitext(item)[1].lower()
            is_unclickable = (
                is_transformed_folder
                or item.endswith("sections.txt")
                or file_extension == ".pdf"
            )

            css_class = "transformed" if is_transformed_folder else "normal"
            is_selected = not is_unclickable and item_path in selected_files
            selected_class = "selected" if is_selected else ""

            file_style = {
                "margin-left": f"{(level + 1) * 60}px",
                "cursor": "not-allowed" if is_unclickable else "pointer",
                "padding": "5px",
                "color": (
                    "#155724"
                    if is_transformed_folder
                    else ("#aaaaaa" if is_unclickable else "#007bff")
                ),
                "opacity": (
                    "1.0"
                    if is_transformed_folder
                    else "0.6" if is_unclickable else "1.0"
                ),
            }

            if is_unclickable:
                # Add unclickable file
                items.append(
                    html.Div(
                        [
                            html.Span(
                                "📄",
                                style={"margin-right": "10px", "font-size": "1.2em"},
                            ),
                            html.Span(item),
                        ],
                        className=f"file-tree-item {css_class}",
                        style=file_style,
                    )
                )
            else:
                # Add clickable file with selection handling
                items.append(
                    html.Div(
                        [
                            html.Span(
                                "📄",
                                style={"margin-right": "10px", "font-size": "1.2em"},
                            ),
                            html.Span(item),
                        ],
                        id={"type": "file-entry", "file": item_path},
                        className=f"file-tree-item {css_class} {selected_class}",
                        style=file_style,
                    )
                )

    return items


@app.callback(
    Output("transformability-score", "children"),
    Input("selected-files-store", "data"),
    prevent_initial_call=True,
)
def update_score(selected_files):
    if selected_files is None or not selected_files:  # No files selected
        return "0 files selected."  # Default score if no file uploaded

    # Get the number of files (assuming selected_files is a list)
    total_score = 0.0
    num_files = len(selected_files)

    for selected_file in selected_files:
        file_score = calculate_sheet_score(selected_file)  # Example: 10 points per file
        total_score += file_score

    file_text = "file" if num_files == 1 else "files"

    return f"{(total_score/num_files)*100:.1f}% ({num_files} {file_text})"


@app.callback(
    Output("selected-region", "children"),
    Input("region-selector", "value"),
)
def update_region(selected_region):
    logging.info(f"Region selected: {selected_region}")
    return f"Currently selected region: {selected_region}"


def pipeline_transform(selected_files, base_dir="statista_data"):
    global pipeline_progress

    steps = [
        ("Removing Overview sheets", tr1_remove_sheets),
        ("Removing header rows and empty columns", tr2_remove_header_and_empty_column),
        ("Removing metadata rows", tr3_remove_metadata),
        ("Reducing empty lines", tr4_reduce_empty_lines),
        (
            "Removing columns with 'Grand Total' and 'in %'",
            tr5_removing_total_percentages_income_demography,
        ),
        ("Appending questions to options", tr6_append_questions),
        ("Merging sheets", tr7_merging_sheets),
        ("Joining tables", tr8_join_tables),
        ("Transposing tables", tr9_transpose_table),
        ("Mapping age categories", tr10_map_age),
        ("Filtering advanced files", tr11_filter_advanced_files),
        ("Transforming to probability", tr12_transform_to_probability),
    ]

    total_steps = len(steps)

    for i, (step_name, transformation) in enumerate(steps):
        try:
            # Perform transformation step
            selected_files = transformation(selected_files, base_dir)

            # Update progress and status
            progress = int(((i + 1) / total_steps) * 100)
            pipeline_progress["progress"] = progress
            pipeline_progress["status"].append(f"✅ {step_name} completed")

        except Exception as e:
            # Handle errors and stop the pipeline
            pipeline_progress["status"].append(f"❌ {step_name} failed: {str(e)}")
            pipeline_progress["progress"] = 100  # End progress on failure
            break
    # Ensure progress is set to 100 on successful completion
    pipeline_progress["progress"] = 100
    pipeline_progress["status"].append("✅ Transformation pipeline completed")


@app.callback(
    [Output(f"step-{i}", "className") for i in range(12)]
    + [
        Output("progress-bar-transform", "value"),
        Output("progress-bar-transform", "className"),
        Output("transformation-status", "children"),
        Output("progress-interval", "disabled"),
    ],
    [Input("transform-button", "n_clicks"), Input("progress-interval", "n_intervals")],
    [State("selected-files-store", "data")],
    prevent_initial_call=True,
)
def handle_progress_and_steps(n_clicks, n_intervals, selected_files):
    global pipeline_progress

    total_steps = 12  # Number of steps (circles)
    step_progress = 100 / (total_steps - 1)  # Percentage per step

    # Handle pipeline start
    if ctx.triggered_id == "transform-button":
        pipeline_progress = {"progress": 0, "status": []}  # Reset progress state

        if not selected_files or len(selected_files) == 0:
            return ["progress-step"] * total_steps + [
                0,
                "progress-bar-custom",
                "⚠️ No files selected for transformation.",
                True,
            ]

        # Start the pipeline in a separate thread
        def run_pipeline():
            pipeline_transform(selected_files, base_dir="statista_data")

        Thread(target=run_pipeline).start()
        return ["progress-step"] * total_steps + [
            0,
            "progress-bar-custom",
            "🔄 Starting transformation...",
            False,
        ]

    # Handle progress updates
    if ctx.triggered_id == "progress-interval":
        # Calculate the progress percentage
        progress = pipeline_progress["progress"]
        completed_steps = int(
            progress / step_progress
        )  # Number of fully completed steps
        step_classes = []

        # Update step classes based on completion
        for i in range(total_steps):
            if progress >= 100:
                step_classes.append("progress-step completed")
            elif i < completed_steps:
                step_classes.append("progress-step completed")
            elif i == completed_steps:
                step_classes.append("progress-step active")
            else:
                step_classes.append("progress-step")

        status = [html.Div(step) for step in pipeline_progress["status"]]

        # Progress bar value aligns with step positions
        progress_value = completed_steps * step_progress

        # Stop interval when transformation is complete
        if progress >= 100:
            logging.info("✅ Transformation pipeline completed!")
            return step_classes + [
                100,  # Full progress bar
                "progress-bar-custom progress-bar-completed",  # Completed bar styling
                status,
                True,  # Stop interval
            ]

        return step_classes + [
            progress_value,  # Progress bar aligned to circles
            "progress-bar-custom",  # Ongoing bar styling
            status,
            False,  # Continue interval
        ]

    return (
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
    )


@app.callback(
    Output("downloaded-topics-container", "children"),
    Input("refresh-files-button", "n_clicks"),
)
def update_downloaded_topics(n_clicks):
    topic_dir = os.path.join(DOWNLOAD_DIR)
    if not os.path.exists(topic_dir):
        return html.Div("No topics available.", style={"color": "gray"})

    topics = sorted(
        [
            folder
            for folder in os.listdir(topic_dir)
            if os.path.isdir(os.path.join(topic_dir, folder))
        ]
    )

    if not topics:
        return html.Div("No topics downloaded yet.", style={"color": "gray"})

    # Save the topics in a global variable for selection callback
    global session_topics
    session_topics = topics

    # Calculate metrics
    total_files = 0
    total_size = 0
    for root, _, files in os.walk(topic_dir):
        total_files += len(files)
        total_size += sum(os.path.getsize(os.path.join(root, file)) for file in files)

    total_size_mb = total_size / (1024 * 1024)  # Convert to MB

    # Header with metrics
    header = html.Div(
        [
            html.H5(
                [
                    "Number of Topics: ",
                    html.Span(
                        len(topics),
                        style={"color": "#007bff", "font-weight": "bold"},  # Blue color
                    ),
                ],
                style={"margin-bottom": "10px", "font-weight": "bold"},
            ),
            html.H5(
                [
                    "Total Files: ",
                    html.Span(
                        total_files,
                        style={"color": "#007bff", "font-weight": "bold"},  # Blue color
                    ),
                ],
                style={"margin-bottom": "10px", "font-weight": "bold"},
            ),
            html.H5(
                [
                    "Total Size: ",
                    html.Span(
                        f"{total_size_mb:.2f} MB",
                        style={"color": "#007bff", "font-weight": "bold"},  # Blue color
                    ),
                ],
                style={"margin-bottom": "10px", "font-weight": "bold"},
            ),
        ],
        style={
            "margin-bottom": "20px",
            "padding": "15px",
            "background-color": "#f7f7f7",
            "border-radius": "8px",
            "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
        },
    )

    # Modern topic buttons with hover effect
    topic_buttons = [
        dbc.Card(
            dbc.CardBody(
                html.Div(
                    [
                        html.Span(
                            topic,
                            style={
                                "font-size": "16px",
                                "font-weight": "bold",
                                "color": "#333",
                                "margin-right": "10px",
                            },
                        ),
                        dbc.Badge(
                            "View Details",
                            id={"type": "topic-item", "index": idx},  # Add unique id
                            color="info",
                            className="ms-1",
                            style={"cursor": "pointer"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "space-between",
                    },
                )
            ),
            style={
                "margin-bottom": "10px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "transition": "all 0.3s ease",
            },
            className="topic-card",
        )
        for idx, topic in enumerate(topics)
    ]

    return html.Div([header] + topic_buttons)


@app.callback(
    [
        Output("selected-topic", "children"),  # Display the selected topic name
        Output("topic-visualization-container", "children"),  # Update visualizations
    ],
    Input({"type": "topic-item", "index": ALL}, "n_clicks"),  # Track topic clicks
    prevent_initial_call=True,
)
def handle_topic_selection(n_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update

    triggered_id = ctx.triggered_id
    if isinstance(triggered_id, dict) and "index" in triggered_id:
        topic_index = triggered_id["index"]
        topic_name = session_topics[topic_index]
        topic_path = os.path.join(DOWNLOAD_DIR, topic_name)

        # Count file types and calculate total size
        file_types = {}
        total_files = 0
        total_size = 0
        for root, _, files in os.walk(topic_path):
            total_files += len(files)
            total_size += sum(
                os.path.getsize(os.path.join(root, file)) for file in files
            )
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                file_types[ext] = file_types.get(ext, 0) + 1

        total_size_mb = total_size / (1024 * 1024)  # Convert to MB

        # Check for the existence of "advanced reports" folder
        advanced_reports_folder = os.path.join(topic_path, "advanced_reports")
        is_advanced_search = os.path.exists(advanced_reports_folder) and any(
            os.scandir(advanced_reports_folder)
        )  # Check if the folder has files

        # Header with metrics for selected topic
        header = html.Div(
            [
                html.H5(
                    [
                        "Selected Topic: ",
                        html.Span(
                            topic_name,
                            style={
                                "color": "#007bff",
                                "font-weight": "bold",
                            },  # Blue color
                        ),
                    ],
                    style={"margin-bottom": "10px", "font-weight": "bold"},
                ),
                html.H5(
                    [
                        "Total Files: ",
                        html.Span(
                            total_files,
                            style={
                                "color": "#007bff",
                                "font-weight": "bold",
                            },  # Blue color
                        ),
                    ],
                    style={"margin-bottom": "10px", "font-weight": "bold"},
                ),
                html.H5(
                    [
                        "Total Size: ",
                        html.Span(
                            f"{total_size_mb:.2f} MB",
                            style={
                                "color": "#007bff",
                                "font-weight": "bold",
                            },  # Blue color
                        ),
                    ],
                    style={"margin-bottom": "10px", "font-weight": "bold"},
                ),
                html.H5(
                    [
                        "Advanced Search: ",
                        html.Span(
                            "True" if is_advanced_search else "False",
                            style={
                                "color": "#007bff",
                                "font-weight": "bold",
                            },  # Blue color
                        ),
                    ],
                    style={"margin-bottom": "10px", "font-weight": "bold"},
                ),
            ],
            style={
                "margin-bottom": "20px",
                "padding": "15px",
                "background-color": "#f7f7f7",
                "border-radius": "8px",
                "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
            },
        )

        # Create data for visualization
        file_type_labels = list(file_types.keys())
        file_type_counts = list(file_types.values())

        # Generate Plotly figure
        fig = px.pie(
            values=file_type_counts,
            names=file_type_labels,
            title=f"File Type Distribution for {topic_name}",
            hole=0.4,  # Donut chart
        )
        fig.update_layout(
            title_x=0.5,
            title_font_size=18,
            legend_title="File Types",
            margin=dict(t=40, b=20, l=20, r=20),
        )

        # Return header and visualization
        return (
            header,  # Updated header for selected topic
            dcc.Graph(figure=fig),  # Visualization
        )

    return dash.no_update, dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
