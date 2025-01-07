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

# dashboard visualization
from app_layout import (
    app_layout,
    active_card_style,
    inactive_card_style,
    modern_card_hover_effect,
)
from advanced_search import extract_report_results

# Scraper script's methods
from scraper import (
    setup_driver,
    login_with_selenium,
    search_topic,
    scrape_topic,
    get_files_to_be_downloaded,
    get_failed_downloads,
)

from transform import remove_overview, remove_header_and_empty_column


def SelectedTopicComponent():
    return html.Div(
        id="selected-topic-info",
        children="Selected Topic: None | Files to Download: 0",
        style={"margin-top": "10px", "font-weight": "bold"},
    )


# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.config.prevent_initial_callbacks = "initial_duplicate"
app.config.suppress_callback_exceptions = (
    True  # Allow callbacks for dynamically created components
)
server = app.server

# Global variables
log_data = []
driver = None
session_topics = []
selected_topic_url = None
downloaded_files = []  # List of downloaded files
failed_downloads = []
files_to_be_downloaded = 0
advanced_matches = 0

# Directory for downloads
DOWNLOAD_DIR = os.path.abspath("statista_data")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize initial files at app start
initial_files = {
    os.path.relpath(os.path.join(root, filename), DOWNLOAD_DIR)
    for root, _, filenames in os.walk(DOWNLOAD_DIR)
    for filename in filenames
}


class DashLogger(logging.Handler):
    """Custom logging handler to store logs in the global `log_data` list."""

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


# Helper function: Initialize driver
def initialize_driver():
    global driver
    driver = setup_driver()


# Helper function: Populate files in a directory
def populate_initial_files():
    for root, _, filenames in os.walk(DOWNLOAD_DIR):
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(root, filename), DOWNLOAD_DIR)
            initial_files.add(relative_path)


# Create directories and populate initial files
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
populate_initial_files()


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


# Merge hover effect into active_card_style
active_card_style.update(modern_card_hover_effect)

# Update app layout
app.layout = app_layout


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
    elif active_tab == "transformation":
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
        Input("advanced-matches-store", "data"),
        Input("files-to-download-store", "data"),
    ],
)
def handle_checkbox_toggle(checkbox_value, advanced_matches, files_to_be_downloaded):
    checkbox_enabled = "enabled" in checkbox_value if checkbox_value else False
    if checkbox_enabled:
        files_to_be_downloaded = max(files_to_be_downloaded + advanced_matches, 0)
    else:
        files_to_be_downloaded = max(files_to_be_downloaded - advanced_matches, 0)
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
        Output(
            "files-to-download-store", "data", allow_duplicate=True
        ),  # Allow duplicate
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
):
    global session_topics, selected_topic_url, selected_topic_name, driver

    # Handle search
    if ctx.triggered_id == "search-button":
        topics = search_topic(topic_input)
        advanced_matches = extract_report_results(driver, topic_input)
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
        files_to_be_downloaded = get_files_to_be_downloaded(selected_topic_url)
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
        scrape_thread = Thread(target=scrape_topic, args=(selected_topic_url,))
        scrape_thread.start()

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

        # Get the current files in the directory
        current_files = set()
        for root, _, filenames in os.walk(DOWNLOAD_DIR):
            for filename in filenames:
                relative_path = os.path.relpath(
                    os.path.join(root, filename), DOWNLOAD_DIR
                )
                current_files.add(relative_path)

        # Identify files added after app start
        downloaded_files = current_files - initial_files
        valid_files = [
            file
            for file in downloaded_files
            if not os.path.basename(file).startswith(("study_id", "statistic_id"))
        ]

        # Filter out unwanted files
        meaningful_extensions = {".xlsx", ".pdf", ".txt", ".csv"}
        renamed_files = [
            file
            for file in valid_files
            if os.path.splitext(file)[1] in meaningful_extensions
        ]

        # Update progress
        downloaded_count = len(renamed_files)
        failed_count = get_failed_downloads()
        total_processed = downloaded_count + failed_count

        if files_to_be_downloaded > 0:
            progress = (total_processed / files_to_be_downloaded) * 100
            progress = min(progress, 100)
        else:
            progress = 0

        # Define descriptions for file types
        file_type_descriptions = {
            ".txt": "text file",
            ".pdf": "pdf report",
            ".csv": "excel table",
            ".xlsx": "excel table",
        }

        # Create styled list items for renamed files
        styled_links = []
        for relative_path in renamed_files:
            filename = os.path.basename(relative_path)
            file_extension = os.path.splitext(filename)[1]
            file_description = file_type_descriptions.get(file_extension, "file")

            styled_links.append(
                html.Div(
                    [
                        html.A(
                            filename,
                            href=f"/download/{relative_path}",
                            target="_blank",
                            style={
                                "text-decoration": "none",
                                "color": "#007bff",
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
                        "box-shadow": "0 1px 3px rgba(0, 0, 0, 0.1)",
                        "margin-bottom": "5px",
                    },
                )
            )
        # print(f"Failed inside gui: {failed_count}")
        # Progress text
        progress_text = f"{downloaded_count} succeeded, {failed_count} failed, {total_processed}/{files_to_be_downloaded} processed ({int(progress)}%)."
        failed_links = [
            html.Div(
                f"Failed to download: {url}",
                style={"color": "red", "font-weight": "bold", "margin-bottom": "5px"},
            )
            for url in failed_downloads
        ]

        # If progress reaches 100%, add bounce effect
        if progress == 100:
            return (
                styled_links,
                progress,
                f"Download Complete! {int(progress)}%",
                "bounce",
                failed_links
                or [
                    html.Div(
                        "No failed downloads.",
                        style={"color": "gray", "text-align": "center"},
                    )
                ],
            )

        # Return updated values for non-100% progress
        return (
            styled_links,
            progress,
            progress_text,
            "",
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
    ],
    State("selected-files-store", "data"),
)
def update_file_tree_and_toggle_selection(refresh_clicks, file_clicks, selected_files):
    """Update the file tree and handle file selection."""
    ctx = dash.callback_context

    if not ctx.triggered:
        # Default case when nothing is triggered
        selected_files = selected_files or []
        return parse_tree(DOWNLOAD_DIR, selected_files), selected_files

    triggered_id = ctx.triggered_id

    # Handle refresh button
    if triggered_id == "refresh-files-button":
        selected_files = selected_files or []
        return parse_tree(DOWNLOAD_DIR, selected_files), selected_files

    # Handle file selection
    if isinstance(triggered_id, dict) and triggered_id["type"] == "file-entry":
        clicked_file = triggered_id["file"]
        if clicked_file in selected_files:
            selected_files.remove(clicked_file)
        else:
            selected_files.append(clicked_file)

    return parse_tree(DOWNLOAD_DIR, selected_files), selected_files


def parse_tree(path, selected_files, level=0, is_topic_section=False):
    """Recursively parse folders and files, with specific logic for 'topic_sections'."""
    items = []

    # Check if the current folder is 'topic_sections'
    folder_name = os.path.basename(path)
    is_topic_section = is_topic_section or (folder_name.lower() == "topic sections")

    folder_style = {
        "margin-left": f"{level * 40}px",
        "padding": "5px",
        "background-color": "transparent",
        "border-radius": "5px",
        "font-weight": "bold",
        "display": "flex",
        "align-items": "center",
    }
    items.append(
        html.Div(
            [
                html.Span(
                    "📂",
                    style={
                        "margin-right": "10px",
                        "font-size": "1.2em",
                        "color": "#333",
                    },
                ),
                html.Span(folder_name),
            ],
            style=folder_style,
        )
    )

    # Add files and subfolders
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)

        # Exclude the 'transformed' folder
        if os.path.basename(item_path).lower() == "transformed":
            continue

        if os.path.isdir(item_path):
            # Recursively parse subfolders
            items.extend(
                parse_tree(
                    item_path,
                    selected_files,
                    level=level + 1,
                    is_topic_section=is_topic_section,
                )
            )
        else:
            is_selected = item_path in selected_files
            if is_topic_section:
                file_style = {
                    "margin-left": f"{(level + 1) * 40}px",
                    "cursor": "pointer",
                    "padding": "5px",
                    "background-color": "#e6f7ff" if is_selected else "transparent",
                    "border-radius": "5px",
                    "color": "#007bff" if is_selected else "black",
                    "display": "flex",
                    "align-items": "center",
                }
                items.append(
                    html.Div(
                        [
                            html.Span(
                                "📄",
                                style={
                                    "margin-right": "10px",
                                    "font-size": "1.2em",
                                    "color": "#007bff" if is_selected else "#333",
                                },
                            ),
                            html.Span(item),
                        ],
                        id={"type": "file-entry", "file": item_path},
                        style=file_style,
                    )
                )
            else:
                # Non-clickable files
                file_style = {
                    "margin-left": f"{(level + 1) * 40}px",
                    "cursor": "not-allowed",
                    "padding": "5px",
                    "background-color": "#f5f5f5",
                    "border-radius": "5px",
                    "color": "#aaaaaa",
                    "display": "flex",
                    "align-items": "center",
                    "opacity": "0.6",
                }
                items.append(
                    html.Div(
                        [
                            html.Span(
                                "📄",
                                style={
                                    "margin-right": "10px",
                                    "font-size": "1.2em",
                                    "color": "#aaaaaa",
                                },
                            ),
                            html.Span(item),
                        ],
                        style=file_style,
                    )
                )

    return items


@app.callback(
    Output("selected-region", "children"),
    Input("region-selector", "value"),
)
def update_region(selected_region):
    logging.info(f"Region selected: {selected_region}")
    return f"Currently selected region: {selected_region}"


@app.callback(
    Output("transformation-status", "children"),
    Input("transform-button", "n_clicks"),
    State("selected-files-store", "data"),
    prevent_initial_call=True,
)
def transform_files(n_clicks, selected_files):
    """Handle transformation of selected files."""
    if not selected_files:
        return "⚠️ No files selected for transformation."

    base_dir = DOWNLOAD_DIR

    transformations = [
        {"name": "Removing overview sheet", "function": remove_overview},
        {
            "name": "Removing header rows and empty first column",
            "function": remove_header_and_empty_column,
        },
    ]

    transformation_status = []
    total_steps = len(transformations)

    try:
        for idx, transformation in enumerate(transformations, start=1):
            step = (
                f"🔄 Transformation {idx}/{total_steps}: {transformation['name']}... "
            )
            try:
                transformation["function"](
                    selected_files, base_dir
                )  # Call the transformation function
                step += "✅ Completed"
            except Exception as e:
                step += f"❌ Failed ({str(e)})"
            transformation_status.append(html.Div(step, style={"margin-bottom": "5px"}))

        # Add final status summary
        transformation_status.append(
            html.Div(
                "🎉 All transformations completed.",
                style={"color": "green", "font-weight": "bold"},
            )
        )
    except Exception as e:
        logging.error(f"Error during transformation: {e}")
        return f"❌ Transformation process failed: {e}"

    return transformation_status


if __name__ == "__main__":
    app.run_server(debug=True)
