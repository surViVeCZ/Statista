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
    download_xlsx,
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
    tr13_generate_clone_attributes,
)
from metrics import calculate_sheet_score

# ===========================
# GLOBAL VARIABLES
# ===========================
log_data = []  # Log messages stored in memory
driver = None  # Web driver for scraper
session_topics = []  # Topics for the current session
session_sorted_topics = []  # Sorted topics with match types for current session
selected_topics = []  # List of selected topics (name, url)
selected_topic_names = []  # List of selected topic names for easy comparison
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


def determine_multi_country_match_type(input_topic, result_topic, selected_countries):
    """Classify match type for multi-country searches based on exact topic match."""
    import re

    input_topic_lower = input_topic.lower().strip()
    result_topic_lower = result_topic.lower().strip()

    # Country name mappings to handle variations
    country_variants = {
        "czech republic": ["czech", "czech republic", "czechia"],
        "germany": ["germany", "german"],
        "spain": ["spain", "spanish"],
        "uk": ["uk", "united kingdom", "britain", "british"],
        "france": ["france", "french"],
        "italy": ["italy", "italian"],
    }

    # Build pattern to match exact topic + country variations
    country_patterns = []
    for country in selected_countries:
        country_names = country_variants.get(country, [country])
        for country_name in country_names:
            # Exact match patterns like "internet usage in germany" or "internet usage - germany"
            patterns = [
                f"{input_topic_lower} in {country_name.lower()}",
                f"{input_topic_lower} - {country_name.lower()}",
                f"{input_topic_lower} in the {country_name.lower()}",
                f"{input_topic_lower} ({country_name.lower()})",
            ]
            country_patterns.extend(patterns)

    # Check for exact matches
    for pattern in country_patterns:
        if pattern == result_topic_lower or result_topic_lower.startswith(pattern):
            return "Exact match"

    # Check if the input topic is contained in the result (close match)
    if input_topic_lower in result_topic_lower:
        return "Close match"

    # Otherwise, it's a somewhat match (should rarely happen with our filtering)
    return "Somewhat match"


def get_topic_file_details(topic_url):
    """Get detailed file information for a topic including names for duplicate analysis."""
    try:
        from bs4 import BeautifulSoup
        from urllib.parse import urljoin
        import requests

        response = requests.get(topic_url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        sources_section = soup.find("section", id="statisticChapter")
        if not sources_section:
            return []

        file_details = []
        for chapter in sources_section.find_all("div", class_="statisticChapter"):
            for item in chapter.find_all("li", class_="statisticChapter__item"):
                link = item.find("a")
                if link:
                    file_name = link.get_text(strip=True)
                    file_url = urljoin("https://www.statista.com", link["href"])
                    file_details.append({"name": file_name, "url": file_url})

        return file_details
    except Exception as e:
        logging.error(f"Error getting file details for {topic_url}: {e}")
        return []


def get_common_files_across_topics(selected_topics_with_urls):
    """Get files that exist in ALL selected topics."""
    if len(selected_topics_with_urls) < 2:
        return []

    # Get file details for each topic
    topic_files = {}
    for topic_name, topic_url in selected_topics_with_urls:
        file_details = get_topic_file_details(topic_url)
        topic_files[topic_name] = file_details

    # Find files that exist in ALL topics
    all_file_names = {}
    for topic_name, files in topic_files.items():
        for file_info in files:
            file_name = file_info["name"].lower().strip()
            if file_name not in all_file_names:
                all_file_names[file_name] = []
            all_file_names[file_name].append(
                {
                    "topic": topic_name,
                    "url": file_info["url"],
                    "original_name": file_info["name"],
                }
            )

    # Return only files that appear in ALL topics
    common_files = []
    for file_name, file_instances in all_file_names.items():
        if len(file_instances) == len(selected_topics_with_urls):
            # This file exists in all topics
            common_files.append(
                {
                    "name": file_instances[0][
                        "original_name"
                    ],  # Use original name from first instance
                    "urls": [instance["url"] for instance in file_instances],
                    "topics": [instance["topic"] for instance in file_instances],
                }
            )

    return common_files


def analyze_duplicate_files(selected_topics_with_urls):
    """Analyze files across multiple topics to find duplicates by name."""
    if len(selected_topics_with_urls) < 2:
        return {"total_unique": 0, "total_duplicates": 0, "duplicate_details": []}

    # Get file details for each topic
    topic_files = {}
    for topic_name, topic_url in selected_topics_with_urls:
        file_details = get_topic_file_details(topic_url)
        topic_files[topic_name] = file_details

    # Find duplicates by comparing file names
    all_file_names = {}
    for topic_name, files in topic_files.items():
        for file_info in files:
            file_name = file_info["name"].lower().strip()
            if file_name not in all_file_names:
                all_file_names[file_name] = []
            all_file_names[file_name].append(topic_name)

    # Identify duplicates (files that appear in multiple topics)
    duplicate_files = {
        name: topics for name, topics in all_file_names.items() if len(topics) > 1
    }

    # Calculate statistics
    total_files = sum(len(files) for files in topic_files.values())
    unique_files = len(all_file_names)
    duplicate_count = sum(len(topics) - 1 for topics in duplicate_files.values())

    duplicate_details = [
        {"file_name": file_name, "topics": topics, "count": len(topics)}
        for file_name, topics in duplicate_files.items()
    ]

    return {
        "total_files": total_files,
        "total_unique": unique_files,
        "total_duplicates": duplicate_count,
        "duplicate_details": duplicate_details,
        "topics_analyzed": list(topic_files.keys()),
    }


def generate_result_cards(sorted_topics, current_selected_topics):
    """Generate result cards with proper styling based on selected topics."""
    result_cards = []
    # Handle both single topic (string) and multiple topics (list) for backward compatibility
    if isinstance(current_selected_topics, str):
        current_selected_topics = (
            [current_selected_topics] if current_selected_topics else []
        )
    elif current_selected_topics is None:
        current_selected_topics = []

    for idx, (name, url, match_type) in enumerate(sorted_topics):
        match_color = {
            "Exact match": "#28a745",
            "Close match": "#ffc107",
            "Somewhat match": "#dc3545",
        }.get(match_type, "#6c757d")

        # Check if this topic is currently selected
        topic_name = name.split(" -")[0]
        is_selected = topic_name in current_selected_topics

        # Define different styles for selected vs unselected topics
        card_style = {
            "margin-bottom": "10px",
            "padding": "8px",
            "border": "2px solid #007bff" if is_selected else "1px solid #dee2e6",
            "background-color": "#e7f3ff" if is_selected else "white",
            "box-shadow": (
                "0 4px 8px rgba(0, 123, 255, 0.3)"
                if is_selected
                else "0 2px 4px rgba(0,0,0,0.1)"
            ),
            "transform": "scale(1.02)" if is_selected else "scale(1)",
            "transition": "all 0.3s ease",
        }

        button_text = "Remove" if is_selected else "Add"
        button_class = "btn btn-danger" if is_selected else "btn btn-outline-primary"

        result_cards.append(
            dbc.Card(
                dbc.CardBody(
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        topic_name,
                                        className="card-title",
                                        style={
                                            "font-weight": "bold",
                                            "font-size": "1.1em",
                                            "margin-bottom": "5px",
                                            "color": (
                                                "#0056b3" if is_selected else "inherit"
                                            ),
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
                                    button_text,
                                    id={"type": "search-result", "index": idx},
                                    className=button_class,
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
                style=card_style,
            )
        )
    return result_cards


def search_multi_country_topics(
    driver,
    topic_input,
    selected_countries,
    all_countries_checkbox,
    strict_match_checkbox,
    max_results_input,
):
    """Search for topics across multiple countries and optionally filter for topics present in all countries."""
    if not topic_input or topic_input.strip() == "":
        logging.warning("Empty topic input provided to search_multi_country_topics")
        return []

    if not selected_countries:
        # If no countries selected, perform regular search
        return search_topic(
            driver, topic_input, strict_match_checkbox, max_results_input
        )

    # Country name mappings to handle variations
    country_variants = {
        "czech republic": ["czech", "czech republic", "czechia"],
        "germany": ["germany", "german"],
        "spain": ["spain", "spanish"],
        "uk": ["uk", "united kingdom", "britain", "british"],
        "france": ["france", "french"],
        "italy": ["italy", "italian"],
    }

    all_results = {}  # Dictionary to store results by country
    topic_counts = {}  # Count how many countries each topic appears in

    # First, do a broad search with just the topic to get a good pool of results
    logging.info(f"🔍 Searching for broad topic: '{topic_input}'")
    broad_results = search_topic(
        driver, topic_input, False, max_results_input * 5
    )  # Use non-strict for broader search

    # Also try searching with each country name to ensure we get country-specific results
    for country in selected_countries:
        country_names = country_variants.get(country, [country])
        for country_name in country_names[:2]:  # Try top 2 variants
            country_query = f"{topic_input} {country_name}"
            logging.info(f"🔍 Additional search for: '{country_query}'")
            additional_results = search_topic(
                driver, country_query, False, max_results_input
            )
            broad_results.extend(additional_results)

    # Remove duplicates from broad results
    seen_urls = set()
    unique_broad_results = []
    for topic_name, topic_url in broad_results:
        if topic_url not in seen_urls:
            seen_urls.add(topic_url)
            unique_broad_results.append((topic_name, topic_url))

    logging.info(f"📊 Total unique results to filter: {len(unique_broad_results)}")

    # Filter results for each selected country
    for country in selected_countries:
        country_results = []
        country_names = country_variants.get(country, [country])

        logging.info(f"🔍 Filtering results for {country.title()}: {country_names}")

        for topic_name, topic_url in unique_broad_results:
            topic_name_lower = topic_name.lower()

            # Check if any variant of the country name appears in the topic
            found_match = False
            for country_variant in country_names:
                if country_variant.lower() in topic_name_lower:
                    # Make sure it's not a substring of another word
                    import re

                    pattern = r"\b" + re.escape(country_variant.lower()) + r"\b"
                    if re.search(pattern, topic_name_lower):
                        country_results.append((topic_name, topic_url))
                        found_match = True
                        break

            if found_match:
                logging.info(f"  ✅ Found match for {country}: {topic_name}")

        logging.info(f"🎯 Found {len(country_results)} results for {country.title()}")
        all_results[country] = country_results

        # Count topic occurrences across countries for the "all countries" feature
        for topic_name, topic_url in country_results:
            # Create a normalized topic key (remove country-specific parts)
            normalized_topic = topic_input.lower()
            if normalized_topic not in topic_counts:
                topic_counts[normalized_topic] = {
                    "count": 0,
                    "entries": [],
                    "countries": set(),
                }
            if country not in topic_counts[normalized_topic]["countries"]:
                topic_counts[normalized_topic]["count"] += 1
                topic_counts[normalized_topic]["countries"].add(country)
            topic_counts[normalized_topic]["entries"].append(
                (topic_name, topic_url, country)
            )

    # Filter results based on the "all countries" checkbox
    final_results = []
    if all_countries_checkbox:
        # Only include topics that appear in ALL selected countries
        required_count = len(selected_countries)
        for topic_key, data in topic_counts.items():
            if data["count"] >= required_count:
                # Add all variations of this topic from different countries
                for topic_name, topic_url, country in data["entries"]:
                    final_results.append((f"{topic_name}", topic_url))
    else:
        # Include all topics from all selected countries
        for country, country_results in all_results.items():
            for topic_name, topic_url in country_results:
                final_results.append((topic_name, topic_url))

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for topic_name, topic_url in final_results:
        if topic_url not in seen:
            seen.add(topic_url)
            unique_results.append((topic_name, topic_url))

    logging.info(
        f"🎉 Found {len(unique_results)} matching topics across {len(selected_countries)} countries"
    )
    return unique_results


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
        Output("login-button", "disabled"),
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
        return "Logged in successfully.", "text-success text-center", True, True
    return "Login failed.", "text-danger text-center", False, False


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
    Output("duplicate-files-display", "children"),
    [
        Input("show-duplicates-checkbox", "value"),
        Input("selected-topic-name-store", "data"),
    ],
    prevent_initial_call=True,
)
def update_duplicate_files_display(show_common_files_value, selected_topics):
    """Update the common files display based on checkbox and selected topics."""
    global session_topics

    # Check if the checkbox is enabled
    checkbox_enabled = (
        "enabled" in show_common_files_value if show_common_files_value else False
    )

    if not checkbox_enabled:
        return ""

    # Check if we have multiple topics selected
    if (
        not selected_topics
        or not isinstance(selected_topics, list)
        or len(selected_topics) < 2
    ):
        return "Select at least 2 topics to download only common files."

    try:
        # Get URLs for selected topics
        selected_topics_with_urls = []
        for topic_name in selected_topics:
            for name, url in session_topics:
                if name.split(" -")[0] == topic_name:
                    selected_topics_with_urls.append((topic_name, url))
                    break

        if len(selected_topics_with_urls) < 2:
            return "Could not find URLs for selected topics."

        # Perform duplicate analysis to find common files
        duplicate_analysis = analyze_duplicate_files(selected_topics_with_urls)

        # Count files that exist in ALL selected topics
        common_files = [
            detail
            for detail in duplicate_analysis["duplicate_details"]
            if detail["count"] == len(selected_topics)
        ]

        common_count = len(common_files)

        if common_count == 0:
            return f"⚠️ No common files found across all {len(selected_topics)} topics. Regular download will include all files."

        return f"✅ {common_count} common file{'s' if common_count != 1 else ''} will be downloaded (present in all {len(selected_topics)} topics)"

    except Exception as e:
        logging.error(f"Error in common files analysis: {e}")
        return f"Error analyzing common files: {str(e)}"


@app.callback(
    [
        Output("search-results-container", "children"),
        Output("scrape-card", "style"),
        Output("scrape-button", "disabled"),
        Output("scrape-status", "children"),
        Output("search-button", "disabled"),
        Output("advanced-matches-store", "data"),  # Update advanced_matches
        Output("files-to-download-store", "data", allow_duplicate=True),
        Output("selected-topic-name-store", "data"),  # Update selected topic
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
        State("strict-match-checkbox", "value"),
        State("max-results-input", "value"),
        State("include-reports-checkbox", "value"),
        State("country-selection", "value"),
        State("all-countries-checkbox", "value"),
        State("selected-topic-name-store", "data"),  # Current selected topics
        State("show-duplicates-checkbox", "value"),  # Common files only checkbox
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
    strict_match_checkbox,
    max_results_input,
    include_reports_checkbox,
    selected_countries,
    all_countries_checkbox,
    current_selected_topics,
    common_files_checkbox,
):
    global session_topics, session_sorted_topics, selected_topics, selected_topic_names, driver, advanced_reports
    checkbox_enabled = "enabled" in checkbox_value if checkbox_value else False

    advanced_reports = []
    advanced_matches = 0

    # Handle search
    if ctx.triggered_id == "search-button":
        # Check if topic_input is provided
        if not topic_input or topic_input.strip() == "":
            return (
                current_results,
                inactive_card_style,
                True,
                "Please enter a search topic.",
                False,
                advanced_matches,
                files_to_be_downloaded,
                current_selected_topics,
            )

        # Use multi-country search if countries are selected, otherwise use regular search
        if selected_countries:
            topics = search_multi_country_topics(
                driver,
                topic_input,
                selected_countries,
                all_countries_checkbox,
                strict_match_checkbox,
                max_results_input,
            )
        else:
            topics = search_topic(
                driver, topic_input, strict_match_checkbox, max_results_input
            )

        if include_reports_checkbox:
            advanced_reports, advanced_matches = extract_report_results(
                driver, topic_input
            )
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

        # For multi-country searches, use specialized match type logic
        if selected_countries:
            temp_topics = [
                (
                    name,
                    url,
                    determine_multi_country_match_type(
                        topic_input, name, selected_countries
                    ),
                )
                for name, url in topics
            ]
        else:
            temp_topics = [
                (name, url, determine_match_type(topic_input, name.split(" -")[0]))
                for name, url in topics
            ]

        sorted_topics = sorted(temp_topics, key=lambda x: match_priority_map[x[2]])
        session_topics = [(name, url) for (name, url, mtype) in sorted_topics]
        session_sorted_topics = sorted_topics  # Store for later use in selection

        # Create result cards using helper function
        result_cards = generate_result_cards(sorted_topics, current_selected_topics)

        return (
            result_cards,
            inactive_card_style,
            True,
            "No topic selected.",
            False,
            advanced_matches,
            0,  # Reset files_to_be_downloaded
            current_selected_topics,  # Keep current selected topics
        )

    # Handle selection (toggle topics)
    if ctx.triggered_id and "search-result" in str(ctx.triggered_id):
        selected_index = ctx.triggered_id["index"]
        selected_topic_name, selected_topic_url = session_topics[selected_index]
        topic_name = selected_topic_name.split(" -")[0]

        if not isinstance(current_selected_topics, list):
            current_selected_topics = (
                [current_selected_topics] if current_selected_topics else []
            )

        if topic_name in current_selected_topics:
            current_selected_topics.remove(topic_name)
            logging.info(f"Removed topic: {topic_name}")
            status_message = f"Removed: {topic_name}"
        else:
            current_selected_topics.append(topic_name)
            logging.info(f"Added topic: {topic_name}")
            status_message = f"Added: {topic_name}"

        try:
            selected_topics_with_urls = []
            for topic_name_calc in current_selected_topics:
                for name, url in session_topics:
                    if name.split(" -")[0] == topic_name_calc:
                        selected_topics_with_urls.append((topic_name_calc, url))
                        break

            total_files = 0
            for topic_name_selected in current_selected_topics:
                for name, url in session_topics:
                    if name.split(" -")[0] == topic_name_selected:
                        total_files += get_files_to_be_downloaded(url) + 2
                        break

        except Exception as e:
            logging.error(f"Error calculating file count: {e}")
            total_files = 0

        updated_result_cards = generate_result_cards(
            session_sorted_topics, current_selected_topics
        )

        selected_count = len(current_selected_topics)
        if selected_count == 0:
            final_status = "No topics selected."
            card_style = inactive_card_style
            scrape_disabled = True
        else:
            final_status = f"{selected_count} topic{'s' if selected_count != 1 else ''} selected. {status_message}"
            card_style = active_card_style
            scrape_disabled = False

        return (
            updated_result_cards,  # Updated cards with new styling
            card_style,
            scrape_disabled,
            final_status,
            False,
            dash.no_update,
            total_files,
            current_selected_topics,
        )

    # Handle scraping
    if ctx.triggered_id == "scrape-button":
        if not current_selected_topics or len(current_selected_topics) == 0:
            logging.error("No topics selected for scraping.")
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                "Error: No topics selected for scraping.",
                False,
                dash.no_update,
                dash.no_update,
                current_selected_topics,
            )
        # Check if common files only mode is enabled
        common_files_enabled = (
            "enabled" in common_files_checkbox if common_files_checkbox else False
        )

        if common_files_enabled and len(current_selected_topics) >= 2:
            # scrape only common files across all topics
            logging.info(
                "Common files mode enabled - analyzing common files across topics"
            )

            # Get URLs for selected topics
            selected_topics_with_urls = []
            for topic_name in current_selected_topics:
                for name, url in session_topics:
                    if name.split(" -")[0] == topic_name:
                        selected_topics_with_urls.append((topic_name, url))
                        break

            # Get common files
            common_files = get_common_files_across_topics(selected_topics_with_urls)

            if not common_files:
                status_msg = f"No common files found across {len(current_selected_topics)} topics. No scraping performed."
            else:
                # Scrape only the common files
                scraped_files = []
                for common_file in common_files:
                    try:
                        # Use the first URL (from the first topic) to download the file
                        file_url = common_file["urls"][0]
                        topic_name = current_selected_topics[
                            0
                        ]  # Use first topic name for folder structure
                        logging.info(
                            f"Scraping common file: {common_file['name']} from {file_url}"
                        )

                        # Create a base folder for common files
                        base_folder = os.path.join(
                            "statista_data",
                            f"common_files_{'-'.join(current_selected_topics)}",
                        )

                        # Download the individual file
                        from tqdm import tqdm

                        with tqdm(
                            total=1, desc=f"Downloading {common_file['name']}"
                        ) as pbar:
                            download_xlsx(
                                file_url, base_folder, pbar, subfolder="common_files"
                            )

                        scraped_files.append(common_file["name"])
                        logging.info(
                            f"Successfully downloaded common file: {common_file['name']}"
                        )

                    except Exception as e:
                        logging.error(
                            f"Error downloading common file {common_file['name']}: {e}"
                        )

                status_msg = f"Downloaded {len(scraped_files)} common files across {len(current_selected_topics)} topics"

        else:
            # Regular scraping: scrape all files from all selected topics
            scraped_topics = []
            for topic_name_selected in current_selected_topics:
                # Find the URL for this topic name
                for name, url in session_topics:
                    if name.split(" -")[0] == topic_name_selected:
                        logging.info(f"Starting scraping for topic: {name}")
                        scrape_topic(url)
                        scraped_topics.append(name)

                        if checkbox_enabled:
                            logging.info(
                                f"Triggering report download for topic: {name}"
                            )
                            download_reports(driver, advanced_reports, name)
                        break

            topic_count = len(scraped_topics)
            status_msg = f"Scraping started for {topic_count} topic{'s' if topic_count != 1 else ''}: {', '.join([t.split(' -')[0] for t in scraped_topics])}"

        return (
            dash.no_update,
            dash.no_update,
            dash.no_update,
            status_msg,
            True,
            dash.no_update,
            dash.no_update,
            current_selected_topics,
        )

    return (
        dash.no_update,
        inactive_card_style,
        True,
        "No topic selected.",
        False,
        dash.no_update,
        dash.no_update,
        current_selected_topics,
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
        ("Generating clone.py", tr13_generate_clone_attributes),
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
    [Output(f"step-{i}", "className") for i in range(13)]
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

    total_steps = 13  # Number of steps (circles)
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
    Output("topic-details-container", "children"),
    Input({"type": "topic-item", "index": dash.dependencies.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def display_topic_details(n_clicks):

    ctx = dash.callback_context

    if not ctx.triggered:

        return dash.no_update

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    topic_index = int(eval(button_id)["index"])

    if topic_index >= len(session_topics):

        return html.Div("Invalid topic selected.", style={"color": "red"})

    selected_topic = session_topics[topic_index]

    topic_path = os.path.join(DOWNLOAD_DIR, selected_topic)

    # Define paths

    topic_sections_path = os.path.join(topic_path, "topic sections")

    topic_sections_transformed_path = os.path.join(topic_sections_path, "transformed")

    advanced_reports_path = os.path.join(topic_path, "advanced_reports")

    advanced_reports_transformed_path = os.path.join(
        advanced_reports_path, "transformed"
    )

    all_paths = [
        (topic_sections_path, "Topic Sections"),
        (topic_sections_transformed_path, "Topic Sections (Transformed)"),
        (advanced_reports_path, "Advanced Reports"),
        (advanced_reports_transformed_path, "Advanced Reports (Transformed)"),
    ]

    file_list = []

    for path, label in all_paths:

        if os.path.exists(path):

            for file in sorted(os.listdir(path)):

                if os.path.isfile(os.path.join(path, file)):

                    # Apply effects based on folder type

                    if "advanced_reports" in path and "transformed" not in path:

                        demography_tag = html.Span(
                            " (Demography Included)",
                            style={"color": "green", "font-weight": "bold"},
                        )

                    else:

                        demography_tag = None

                    # Special effects for transformed files

                    if "transformed" in path:

                        file_item = html.Li(
                            [
                                html.Span(
                                    file,
                                    style={
                                        "font-weight": "bold",
                                        "color": "#007bff",
                                        "text-shadow": "0px 0px 6px rgba(0, 123, 255, 0.7)",
                                    },
                                ),
                                demography_tag,
                            ]
                            if demography_tag
                            else html.Span(
                                file,
                                style={
                                    "font-weight": "bold",
                                    "color": "#007bff",
                                    "text-shadow": "0px 0px 6px rgba(0, 123, 255, 0.7)",
                                },
                            )
                        )
                    else:
                        file_item = html.Li(
                            [file, demography_tag] if demography_tag else file
                        )
                    file_list.append(file_item)
    if not file_list:
        return html.Div("No files found in this topic.", style={"color": "gray"})
    return html.Div(
        [
            html.H5(f"Files in {selected_topic}", style={"font-weight": "bold"}),
            html.Ul(file_list),
        ],
        style={"padding": "10px"},
    )


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
            title_pad=dict(b=20),
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
