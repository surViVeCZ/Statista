import dash
from dash import html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from flask import Flask
import logging
from threading import Thread
import os
from flask import send_file, abort
import dash_daq as daq
from dash import html



# Import your script's methods
from scraper import setup_driver, login_with_selenium, search_topic, scrape_topic, get_files_to_be_downloaded

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.config.suppress_callback_exceptions = True  # Allow callbacks for dynamically created components
server = app.server

# Global variables
log_data = []
driver = None
session_topics = []
selected_topic_url = None  # To store the URL of the selected topic

#downloads
downloaded_files = []  # List of downloaded files
failed_downloads = [] 
files_to_be_downloaded = 0  # Global variable to track the total number of files

# Directory to save downloaded files
DOWNLOAD_DIR = os.path.abspath("statista_data")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# Track the initial set of files when the app starts
initial_files = set()  # Files already in the directory at app start
new_files = set()  # Files added during runtime

# Populate initial_files at startup
for root, _, filenames in os.walk(DOWNLOAD_DIR):
    for filename in filenames:
        relative_path = os.path.relpath(os.path.join(root, filename), DOWNLOAD_DIR)
        initial_files.add(relative_path)

# Configure logging
class DashLogger(logging.Handler):
    """Custom logging handler to send logs to the global log_data list."""
    def emit(self, record):
        global log_data
        log_entry = self.format(record)
        log_data.append(log_entry)
        if len(log_data) > 1000:  # Limit the number of logs
            log_data = log_data[-1000:]

dash_handler = DashLogger()
dash_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(dash_handler)
logging.getLogger().setLevel(logging.INFO)

# Define styles for active and inactive cards
active_card_style = {
    "opacity": "1",
    "pointer-events": "auto",
    "filter": "none",
    "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",  # Stronger shadow for active cards
    "border-radius": "12px",  # Smoother corners
    "background": "linear-gradient(to bottom, #ffffff, #f9f9f9)",  # Subtle gradient
    "transition": "all 0.7s ease-in-out",  # Smooth animation
}

inactive_card_style = {
    "opacity": "0.5",
    "pointer-events": "none",
    "filter": "grayscale(80%)",
    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",  # Minimal shadow for inactive cards
    "border-radius": "12px",
    "background-color": "#e0e0e0",
    "border": "1px solid #cccccc",
    "transition": "all 0.5s ease-in-out",  # Smooth animation
    "transform": "scale(1)",  # No scale for inactive
    #add blur effect
    "filter": "blur(1.3px)",
}

# Define a darker style for card headers with better visual contrast
darker_header_style = {
    "background-color": "#1A1A19",  # Darker background
    "color": "#ffffff",  # White text for better readability
    "padding": "10px",
    "border-radius": "10px 10px 0 0",  # Smoothly rounded top corners
    "font-weight": "bold",
    "text-align": "center",
}


# Add hover effect for cards to lift slightly
modern_card_hover_effect = {
    ":hover": {
        "transform": "translateY(-5px)",  # Slightly move up on hover
        "box-shadow": "0 6px 10px rgba(0, 0, 0, 0.15)",  # Enhance shadow on hover
    }
}

# Merge hover effect into active_card_style
active_card_style.update(modern_card_hover_effect)

# Update app layout
app.layout = dbc.Container([
    dcc.Store(id="login-state", data=False),  # Tracks login state
    dcc.Store(id="files-to-download", data=0),  # Tracks total files to download for progress bar

    # Background Pattern
    html.Div(
        style={
            "background-image": "url('/assets/lakmoos_brand_pattern.svg')",  # Path to the SVG file
            "background-repeat": "no-repeat",
            "background-size": "cover",
            "opacity": "0.2",  # Set transparency
            "position": "absolute",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "z-index": "0",  # Place it under the cards
            "pointer-events": "none",  # Allow clicks to pass through
        }
    ),

    # Header
dbc.Row([
    dbc.Col([
        html.Div([
            html.H1(
                children=[
                    "Statista Scraper Dashboard ",
                    html.Span("by ", style={"font-size": "28px", "font-weight": "normal"}),  # Adjusted font size for "by"
                    html.Img(
                        src="assets/logo_cropped.png",  # Path to the logo file
                        style={
                            "height": "2.4em",
                            "vertical-align": "middle",
                            "margin-left": "2px"
                        }
                    ),
                ],
                className="text-center my-1",  # Reduced vertical spacing
                style={
                    "display": "inline-block",
                    "font-size": "46px",
                    "margin-bottom": "0px",  # No space below the header
                }
            ),
        ], style={"text-align": "center", "margin-bottom": "0px"}),  # No space below the container
    ]),
], style={"margin-bottom": "2px", "margin-top":"15px"}),  # Slight spacing under the row if needed


    # Tabs Section
    dbc.Tabs(
        id="main-tabs",
        active_tab="collection",
        style={"padding-left": "20px"},  
        children=[
            # Tab 1: Data Collection
            dbc.Tab(
                label="Data Collection",
                tab_id="collection",
                label_style={
                    "font-weight": "bold",
                    "font-size": "16px",
                    "padding": "12px 20px",
                },
                tab_style={
                    "border-radius": "12px 12px 0 0",
                    "background": "linear-gradient(to bottom, #ffffff, #f2f2f2)",
                    "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                    "transition": "all 0.3s ease",
                    "margin-right": "5px",
                },
                active_label_style={
                    "background": "linear-gradient(to bottom, #007bff, #0056b3)",
                    "color": "#ffffff",
                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.3)",
                },
                children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Login", style={
                                    "background-color": "#1A1A19", "color": "#ffffff",
                                    "padding": "10px", "font-weight": "bold", "text-align": "center",
                                    "border-radius": "10px 10px 0 0"
                                }),
                                dbc.CardBody([
                                    html.Div("Manage your login process here.", className="mb-2"),
                                    dbc.Button("Login", id="login-button", color="primary", className="mb-3"),
                                    html.Div(id="login-status", children="Not logged in.", className="text-danger")
                                ])
                            ], id="login-card", style={
                                "opacity": "1", "pointer-events": "auto", "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",
                                "border-radius": "12px", "background": "linear-gradient(to bottom, #ffffff, #f9f9f9)",
                                "transition": "all 0.7s ease-in-out"
                            })
                        ], width=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Topic Search", style={
                                    "background-color": "#1A1A19", "color": "#ffffff",
                                    "padding": "10px", "font-weight": "bold", "text-align": "center",
                                    "border-radius": "10px 10px 0 0"
                                }),
                                dbc.CardBody([
                                    dcc.Input(
                                        id="topic-input",
                                        placeholder="Enter a topic...",
                                        type="text",
                                        className="mb-2 form-control",
                                    ),
                                    dbc.Button(
                                        "Search",
                                        id="search-button",
                                        color="success",
                                        className="mb-3",
                                        style={"display": "inline-block"}
                                    ),
                                    dcc.Loading(
                                        id="loading-indicator",
                                        type="circle",
                                        children=html.Div(
                                            id="search-results-container",
                                            style={
                                                "height": "300px", "overflow-y": "auto", "border": "1px solid #ddd",
                                                "padding": "10px", "background-color": "#f9f9f9", "border-radius": "8px",
                                            },
                                        ),
                                    )
                                ])
                            ], id="search-card", style={
                                "opacity": "0.5", "pointer-events": "none", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                "border-radius": "12px", "background-color": "#e0e0e0",
                                "filter": "blur(1.3px)", "transition": "all 0.5s ease-in-out"
                            })
                        ], width=8)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Scraping", style={
                                    "background-color": "#1A1A19", "color": "#ffffff",
                                    "padding": "10px", "font-weight": "bold", "text-align": "center",
                                    "border-radius": "10px 10px 0 0"
                                }),
                                dbc.CardBody([
                                dbc.Button(
                                    "Start Scraping",
                                    id="scrape-button",
                                    color="warning",
                                    className="mb-3",
                                    disabled=True
                                ),
                                html.Div(
                                    id="scrape-status",
                                    children="No scraping started.",
                                    className="text-warning"
                                ),
                                html.Hr(),
                                html.Div("Downloaded Files:", className="mb-2"),
                                html.Ul(
                                    id="downloaded-files-container",
                                    style={
                                        "height": "250px",
                                        "overflow-y": "auto",
                                        "border": "1px solid #ddd",
                                        "padding": "10px",
                                        "background-color": "#f9f9f9",
                                        "font-family": "monospace",
                                    },
                                ),
                                # Re-add the progress summary text
                                html.Div(
                                    id="progress-summary",
                                    className="mb-2",
                                    style={
                                        "text-align": "center",
                                        "font-size": "1rem",
                                        "font-weight": "bold",
                                        "color": "#555",
                                    },
                                ),
                                dbc.Progress(
                                    id="progress-bar",
                                    striped=True,
                                    animated=True,
                                    value=0,
                                    style={"height": "20px", "background-color": "#d3d3d3"},
                                    className="progress-bar-custom"
                                ),
                                html.Div(
                                    id="failed-downloads-container",
                                    style={
                                        "color": "red",
                                        "font-weight": "bold",
                                        "margin-top": "20px",
                                        "padding": "10px",
                                        "background-color": "#fff5f5",
                                        "border": "1px solid #f5c2c2",
                                        "border-radius": "8px",
                                    },
                                    children="No failed downloads yet."
                                ),

                            ])

                            ], id="scrape-card", style={
                                "opacity": "0.5", "pointer-events": "none",
                                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                "border-radius": "12px",
                                "background-color": "#e0e0e0",
                                "filter": "blur(1.3px)",
                                "transition": "all 0.5s ease-in-out"
                            })
                        ], width=4),
                        dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Logs", style={
                                            "background-color": "#1A1A19", "color": "#ffffff",
                                            "padding": "10px", "font-weight": "bold", "text-align": "center",
                                            "border-radius": "10px 10px 0 0"
                                        }),
                                        dbc.CardBody([
                                            html.Div("Logs will appear below in real-time:", className="mb-2"),
                                            html.Pre(id="log-window", className="log-window", style={
                                                "height": "479px", "overflow-y": "auto", "border": "1px solid #ddd",
                                                "padding": "10px", "background-color": "#f9f9f9",
                                                "font-family": "monospace", "border-radius": "8px"
                                            })
                                        ])
                                    ], style={
                                        "opacity": "1", "pointer-events": "auto", "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",
                                        "border-radius": "12px", "background": "linear-gradient(to bottom, #ffffff, #f9f9f9)",
                                        "transition": "all 0.7s ease-in-out"
                                    })
                                ], width=8)
                    ], style={"margin-top": "20px"})
                ]
            ),
            # Tab 2: Data Transformation
            dbc.Tab(
                label="Data Transformation",
                tab_id="transformation",
                label_style={
                    "font-weight": "bold",
                    "font-size": "16px",
                    "padding": "12px 20px",
                },
                tab_style={
                    "border-radius": "12px 12px 0 0",
                    "background": "linear-gradient(to bottom, #ffffff, #f2f2f2)",
                    "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                    "transition": "all 0.3s ease",
                },
                active_label_style={
                    "background": "linear-gradient(to bottom, #007bff, #0056b3)",
                    "color": "#ffffff",
                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.3)",
                },
                children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Data Transformation", style={
                                    "background-color": "#1A1A19", "color": "#ffffff",
                                    "padding": "10px", "font-weight": "bold", "text-align": "center",
                                    "border-radius": "10px 10px 0 0"
                                }),
                                dbc.CardBody([
                                    dbc.Button("Transform Data", id="transform-button", color="info"),
                                    html.Div(id="transformation-status", children="No transformation started."),
                                    html.Div("Transformation Output:", style={"margin-top": "20px"}),
                                    html.Pre(id="transformation-output", style={"height": "300px", "overflow-y": "auto"})
                                ])
                            ])
                        ])
                    ])
                ]
            ),
        ]
    ),

    # Footer
    html.Footer(
        html.Div(
            [
                html.P(
                    "Written by the almighty Petr AI/DS because manual data scraping sucks",
                    className="mb-0",
                    style={"color": "#ffffff", "text-align": "center", "font-weight": "bold"}
                ),
                html.Div(
                    [
                        html.Span(
                            "Data Source: ",
                            style={"font-weight": "bold", "color": "#ffffff"}
                        ),
                        html.A(
                            "Statista.com",
                            href="https://www.statista.com",
                            target="_blank",
                            style={"color": "#007bff", "text-decoration": "none", "margin-right": "15px"}
                        ),
                        html.Span(
                            "| Dashboard made by: ",
                            style={"font-weight": "bold", "color": "#ffffff"}
                        ),
                        html.A(
                            "Lakmoos AI",
                            href="https://lakmoos.com",
                            target="_blank",
                            style={"color": "#007bff", "text-decoration": "none"}
                        )
                    ],
                    style={"text-align": "center", "margin-top": "10px"}
                )
            ],
            style={
                "background-color": "#1A1A19",
                "padding": "20px",
                "border-top": "1px solid #4b4b4b",
                "color": "#ffffff",
                "width": "100%",
                "text-align": "center"
            }
        ),
        style={
            "margin-top": "auto",  # Ensure footer sticks to bottom
            "padding-top": "15px",
            "margin-left": "-12px",
            "margin-right": "-12px",
            "z-index": "10",  # Bring the footer above the background
            "position": "relative",  # Ensure stacking context is established
        }
    ),

    # Refresh Intervals
    dcc.Interval(id="log-interval", interval=500, n_intervals=0),
    dcc.Interval(id="file-interval", interval=500, n_intervals=0)
], fluid=True,
    style={
        "display": "flex",
        "flex-direction": "column",
        "min-height": "100vh"  # Ensure full height layout
    },
)


# Login callback
@app.callback(
    [Output("login-status", "children"),
     Output("login-status", "className"),
     Output("login-state", "data")],
    [Input("login-button", "n_clicks")],
    prevent_initial_call=True
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
@app.callback(
    Output("search-card", "style"),
    [Input("login-state", "data")]
)
def activate_search_card(is_logged_in):
    if is_logged_in:
        return active_card_style
    return inactive_card_style

# Combined callback for handling search, selection, and scraping
@app.callback(
    [
        Output("search-results-container", "children"),
        Output("scrape-card", "style"),
        Output("scrape-button", "disabled"),
        Output("scrape-status", "children"),
        Output("search-button", "disabled"),
        Output("files-to-download", "data"),  # Update total files dynamically
    ],
    [
        Input("search-button", "n_clicks"),
        Input({"type": "search-result", "index": dash.ALL}, "n_clicks"),
        Input("scrape-button", "n_clicks"),
    ],
    [
        State("topic-input", "value"),
        State("search-results-container", "children"),
    ],
    prevent_initial_call=True,
)
def handle_search_selection_scraping(search_click, result_clicks, scrape_click, topic_input, current_results):
    global session_topics, selected_topic_url, selected_topic_name, files_to_be_downloaded

    # Handle search
    if ctx.triggered_id == "search-button":
        topics = search_topic(topic_input)
        session_topics = topics or []

        if not topics:
            logging.warning(f"No topics found for '{topic_input}'.")
            return (
                "No topics found.",
                inactive_card_style,
                True,
                "No topic selected.",
                False,  # Search button remains enabled
                0,  # Reset files-to-download
            )

        logging.info(f"Found {len(topics)} topics for '{topic_input}'.")
        result_cards = [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H6(name, className="card-title"),
                        html.Button(
                            "Select",
                            id={"type": "search-result", "index": idx},
                            className="btn btn-outline-primary",
                            style={"float": "right", "margin-top": "-32px"},
                        ),
                    ]
                ),
                id={"type": "result-card", "index": idx},  # Add ID to card for tracking
                style={"margin-bottom": "10px", "padding": "8px"},
            )
            for idx, (name, _) in enumerate(session_topics)
        ]
        return (
            result_cards,
            inactive_card_style,
            True,
            "No topic selected.",
            False,  # Search button remains enabled
            0,  # Reset files-to-download
        )

    # Handle selection
    if ctx.triggered_id and "search-result" in str(ctx.triggered_id):
        triggered_id = ctx.triggered_id
        selected_index = triggered_id["index"]
        selected_topic_name, topic_url = session_topics[selected_index]
        selected_topic_url = topic_url  # Keep track of the URL internally
        logging.info(f"Selected topic: {selected_topic_name}")

        # Get the number of files to be downloaded for the selected topic
        files_to_be_downloaded = get_files_to_be_downloaded(selected_topic_url) + 2  # Add extra for report and sections overview

        # Update card styles and buttons
        updated_results = []
        for idx, card in enumerate(current_results):
            card_style = {
                "margin-bottom": "10px",
                "padding": "8px",
                "box-shadow": "0 0 8px rgba(0, 0, 0, 0.3)"
                if idx == selected_index
                else "0 4px 8px rgba(0, 0, 0, 0.1)",
                "background-color": "#f9f9f9",
                "border": "1px solid #ddd",
                "transition": "box-shadow 0.3s ease-in-out",
            }
            button_text = "Selected" if idx == selected_index else "Select"
            button_color = "success" if idx == selected_index else "outline-primary"
            updated_results.append(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6(session_topics[idx][0], className="card-title"),
                            html.Button(
                                button_text,
                                id={"type": "search-result", "index": idx},
                                className=f"btn btn-{button_color}",
                                style={"float": "right", "margin-top": "-32px"},
                            ),
                        ]
                    ),
                    style=card_style,
                )
            )

        # Update the Scraping card to display the number of files to be downloaded
        scrape_topic_text = f"Selected Topic: {selected_topic_name} | Files to download: " \
                            f"<span style='font-size: 1.2rem; font-weight: bold; color: #007bff;'>{files_to_be_downloaded}</span>"

        return (
            updated_results,
            active_card_style,
            False,
            f"Selected Topic: {selected_topic_name} | Files to download: {files_to_be_downloaded}",
            True,  # Disable the Search button after selection
            0,  # Reset files-to-download
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
                False,  # Search button remains enabled
                0,  # Reset files-to-download
            )

        logging.info(f"Starting scraping for topic: {selected_topic_name}")
        scrape_thread = Thread(target=scrape_topic, args=(selected_topic_url,))
        scrape_thread.start()

        return (
            dash.no_update,
            dash.no_update,
            dash.no_update,
            f"Scraping started for topic: {selected_topic_name}.",
            True,  # Keep the search button disabled
            files_to_be_downloaded,  # Pass the total files count to the GUI
        )

    return (
        dash.no_update,
        inactive_card_style,
        True,
        "No topic selected.",
        False,  # Search button remains enabled
        0,  # Reset files-to-download
    )


@app.callback(
    [
        Output("downloaded-files-container", "children"),
        Output("progress-bar", "value"),
        Output("progress-summary", "children"),
        Output("progress-bar", "className"),  # Bounce effect
        Output("failed-downloads-container", "children"),  # Display failed downloads
    ],
    Input("file-interval", "n_intervals"),
)
def refresh_files_and_update_progress(n_intervals):
    """Update the file list and progress bar, and display failed downloads."""
    global files_to_be_downloaded, failed_downloads
    try:
        # Ensure files_to_be_downloaded is initialized
        if files_to_be_downloaded is None or files_to_be_downloaded == 0:
            return (
                [html.Div("No files available yet.", style={"color": "gray", "text-align": "center"})],
                0,
                "No files to download yet.",
                "",
                [html.Div("No failed downloads.", style={"color": "gray", "text-align": "center"})],
            )

        # Get the current files in the directory
        current_files = set()
        for root, _, filenames in os.walk(DOWNLOAD_DIR):
            for filename in filenames:
                relative_path = os.path.relpath(os.path.join(root, filename), DOWNLOAD_DIR)
                current_files.add(relative_path)

        # Identify files added after app start
        downloaded_files = current_files - initial_files

        # Exclude files starting with `study_id` or `statistic_id`
        valid_files = [
            file for file in downloaded_files
            if not os.path.basename(file).startswith(("study_id", "statistic_id"))
        ]

        # Filter out unwanted files
        meaningful_extensions = {".xlsx", ".pdf", ".txt", ".csv"}
        renamed_files = [
            file for file in valid_files
            if os.path.splitext(file)[1] in meaningful_extensions
        ]

        # Update progress
        downloaded_count = len(renamed_files)
        failed_count = len(failed_downloads)
        total_processed = downloaded_count + failed_count

        if files_to_be_downloaded > 0:
            progress = (total_processed / files_to_be_downloaded) * 100
            progress = min(progress, 100)  # Cap progress at 100%
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

        # Progress text
        progress_text = f"{downloaded_count} succeeded, {failed_count} failed, {total_processed}/{files_to_be_downloaded} processed ({int(progress)}%)."

        # Styled list of failed downloads
        failed_links = [
            html.Div(
                f"Failed to download: {url}",
                style={"color": "red", "font-weight": "bold", "margin-bottom": "5px"}
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
                failed_links or [html.Div("No failed downloads.", style={"color": "gray", "text-align": "center"})],
            )

        # Return updated values for non-100% progress
        return (
            styled_links,
            progress,
            progress_text,
            "",
            failed_links or [html.Div("No failed downloads.", style={"color": "gray", "text-align": "center"})],
        )

    except Exception as e:
        logging.error(f"Error updating files and progress: {e}")
        return (
            [html.Div("Error loading files.", style={"color": "red", "text-align": "center"})],
            0,
            "Error calculating progress.",
            "",
            [html.Div("Error displaying failed downloads.", style={"color": "red", "text-align": "center"})],
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
@app.callback(
    Output("log-window", "children"),
    Input("log-interval", "n_intervals")
)
def update_logs(n_intervals):
    """
    Update the log window with segmented log messages for better readability.
    """
    segmented_logs = []
    segment_delimiter = "\n" + "=" * 80 + "\n"  # Define a visual delimiter
    
    # Group related log messages into segments
    current_segment = []
    for log_entry in log_data:
        # Check if the log entry starts a new segment (e.g., certain keywords like "Starting" or "Selected")
        if "Starting" in log_entry or "Selected" in log_entry or "Analyzing" in log_entry:
            if current_segment:
                segmented_logs.append("\n".join(current_segment))
                segmented_logs.append(segment_delimiter)  # Add a delimiter between segments
                current_segment = []
        
        # Add the log entry to the current segment
        current_segment.append(log_entry)
    
    # Append the final segment if not empty
    if current_segment:
        segmented_logs.append("\n".join(current_segment))
    
    return "\n".join(segmented_logs)


if __name__ == "__main__":
    app.run_server(debug=True)