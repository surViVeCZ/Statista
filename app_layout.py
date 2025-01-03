import os
from dash import html, dcc
import dash_bootstrap_components as dbc


# Define styles for active and inactive cards
active_card_style = {
    "opacity": "1",
    "pointer-events": "auto",
    "filter": "none",
    "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",
    "border-radius": "12px",
    "background": "linear-gradient(to bottom, #ffffff, #f9f9f9)",
    "transition": "all 0.7s ease-in-out",
}

inactive_card_style = {
    "opacity": "0.5",
    "pointer-events": "none",
    "filter": "grayscale(80%)",
    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
    "border-radius": "12px",
    "background-color": "#e0e0e0",
    "border": "1px solid #cccccc",
    "transition": "all 0.5s ease-in-out",
    "transform": "scale(1)",
    "filter": "blur(1.3px)",
}

# Define a darker style for card headers with better visual contrast
darker_header_style = {
    "background-color": "#1A1A19",
    "color": "#ffffff",
    "padding": "10px",
    "border-radius": "10px 10px 0 0",
    "font-weight": "bold",
    "text-align": "center",
}


# Add hover effect for cards to lift slightly
modern_card_hover_effect = {
    ":hover": {
        "transform": "translateY(-5px)",
        "box-shadow": "0 6px 10px rgba(0, 0, 0, 0.15)",
    }
}

# Merge hover effect into active_card_style
active_card_style.update(modern_card_hover_effect)

app_layout = dbc.Container(
    [
        dcc.Store(id="login-state", data=False),  # Tracks login state
        dcc.Store(
            id="files-to-download", data=0
        ),  # Tracks total files to download for progress bar
        dcc.Store(
            id="selected-files-store", data=[]
        ),  # Tracks selected files for transformation
        # Background Pattern
        html.Div(
            style={
                "background-image": "url('/assets/lakmoos_brand_pattern.svg')",
                "background-repeat": "no-repeat",
                "background-size": "cover",
                "opacity": "0.2",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "z-index": "0",
                "pointer-events": "none",
            }
        ),
        html.Div(
            [
                # Region Selector Row
                html.Div(
                    id="region-selector-container",
                    style={"display": "none"},  # Initially hidden
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(),
                                    width=True,
                                ),
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            # Hint Icon with Tooltip
                                            html.Div(
                                                [
                                                    html.Span(
                                                        "?",
                                                        id="region-hint",
                                                        style={
                                                            "color": "white",
                                                            "background-color": "#007bff",
                                                            "cursor": "pointer",
                                                            "font-weight": "bold",
                                                            "font-size": "0.9rem",
                                                            "border-radius": "50%",
                                                            "display": "inline-flex",
                                                            "justify-content": "center",
                                                            "align-items": "center",
                                                            "width": "20px",
                                                            "height": "20px",
                                                            "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                                                            "margin-right": "3px",
                                                        },
                                                    ),
                                                    dbc.Tooltip(
                                                        "Default is global Statista. Always use this unless a topic search was insufficient. Some reports are available on dedicated Statista pages only.",
                                                        target="region-hint",
                                                        placement="top",
                                                        style={"font-size": "0.9rem"},
                                                    ),
                                                ],
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                            # Region Flag and Selector
                                            dbc.InputGroupText(
                                                id="region-flag-container",
                                                children="🌍",  # Default emoji for "global"
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                    "justify-content": "center",
                                                    "font-size": "1.5rem",
                                                    "height": "35px",
                                                    "width": "220px",
                                                },
                                            ),
                                            dbc.Select(
                                                id="region-selector",
                                                options=[
                                                    {
                                                        "label": "Statista - Global",
                                                        "value": "global",
                                                    },
                                                    {
                                                        "label": "Statista - Germany",
                                                        "value": "de",
                                                    },
                                                    {
                                                        "label": "Statista - Spain",
                                                        "value": "es",
                                                    },
                                                    {
                                                        "label": "Statista - France",
                                                        "value": "fr",
                                                    },
                                                ],
                                                value="global",
                                                style={
                                                    "font-size": "1rem",
                                                    "border-radius": "15px",
                                                    "padding": "10px",
                                                    "background-color": "#f9f9f9",
                                                    "color": "#333",
                                                    "width": "180px",
                                                    "margin-left": "-10px",
                                                    "margin-top": "-5px",
                                                },
                                            ),
                                        ],
                                        size="lg",
                                        style={
                                            "max-width": "500px",
                                            "margin-top": "30px",
                                        },
                                    ),
                                    width="auto",
                                ),
                            ],
                            justify="end",
                        ),
                    ],
                ),
                # Header
                dbc.Container(
                    [
                        # Main Title Row
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H1(
                                            children=[
                                                "Statista Scraper Dashboard ",
                                                html.Span(
                                                    "by ",
                                                    style={
                                                        "font-size": "28px",
                                                        "font-weight": "normal",
                                                    },
                                                ),
                                                html.Img(
                                                    src="assets/logo_cropped.png",
                                                    style={
                                                        "height": "2.4em",
                                                        "vertical-align": "middle",
                                                        "margin-left": "2px",
                                                    },
                                                ),
                                            ],
                                            className="text-center my-1",
                                            style={
                                                "display": "inline-block",
                                                "font-size": "46px",
                                                "margin-bottom": "0px",
                                            },
                                        ),
                                    ],
                                    style={"text-align": "center"},
                                ),
                                width=12,  # Full-width for centering
                            )
                        ),
                    ],
                    fluid=True,
                    style={"margin-bottom": "20px"},
                ),
            ]
        ),
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
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    "Login",
                                                    style={
                                                        "background-color": "#1A1A19",
                                                        "color": "#ffffff",
                                                        "padding": "10px",
                                                        "font-weight": "bold",
                                                        "text-align": "center",
                                                        "border-radius": "10px 10px 0 0",
                                                    },
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(
                                                            "Manage your login process here.",
                                                            className="mb-2",
                                                        ),
                                                        dbc.Button(
                                                            "Login",
                                                            id="login-button",
                                                            color="primary",
                                                            className="mb-3",
                                                        ),
                                                        html.Div(
                                                            id="login-status",
                                                            children="Not logged in.",
                                                            className="text-danger",
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            id="login-card",
                                            style={
                                                "opacity": "1",
                                                "pointer-events": "auto",
                                                "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",
                                                "border-radius": "12px",
                                                "background": "linear-gradient(to bottom, #ffffff, #f9f9f9)",
                                                "transition": "all 0.7s ease-in-out",
                                            },
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    "Topic Search",
                                                    style={
                                                        "background-color": "#1A1A19",
                                                        "color": "#ffffff",
                                                        "padding": "10px",
                                                        "font-weight": "bold",
                                                        "text-align": "center",
                                                        "border-radius": "10px 10px 0 0",
                                                    },
                                                ),
                                                dbc.CardBody(
                                                    [
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
                                                            style={
                                                                "display": "inline-block"
                                                            },
                                                        ),
                                                        dcc.Loading(
                                                            id="loading-indicator",
                                                            type="circle",
                                                            children=html.Div(
                                                                id="search-results-container",
                                                                style={
                                                                    "height": "300px",
                                                                    "overflow-y": "auto",
                                                                    "border": "1px solid #ddd",
                                                                    "padding": "10px",
                                                                    "background-color": "#f9f9f9",
                                                                    "border-radius": "8px",
                                                                },
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            id="search-card",
                                            style={
                                                "opacity": "0.5",
                                                "pointer-events": "none",
                                                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                                "border-radius": "12px",
                                                "background-color": "#e0e0e0",
                                                "filter": "blur(1.3px)",
                                                "transition": "all 0.5s ease-in-out",
                                            },
                                        )
                                    ],
                                    width=8,
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    "Scraping",
                                                    style={
                                                        "background-color": "#1A1A19",
                                                        "color": "#ffffff",
                                                        "padding": "10px",
                                                        "font-weight": "bold",
                                                        "text-align": "center",
                                                        "border-radius": "10px 10px 0 0",
                                                    },
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        dbc.Button(
                                                            "Start Scraping",
                                                            id="scrape-button",
                                                            color="warning",
                                                            className="mb-3",
                                                            disabled=True,
                                                        ),
                                                        html.Div(
                                                            id="scrape-status",
                                                            children="No scraping started.",
                                                            className="text-warning",
                                                        ),
                                                        html.Hr(),
                                                        html.Div(
                                                            "Downloaded Files:",
                                                            className="mb-2",
                                                        ),
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
                                                            style={
                                                                "height": "20px",
                                                                "background-color": "#d3d3d3",
                                                            },
                                                            className="progress-bar-custom",
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
                                                            children="No failed downloads yet.",
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            id="scrape-card",
                                            style={
                                                "opacity": "0.5",
                                                "pointer-events": "none",
                                                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                                "border-radius": "12px",
                                                "background-color": "#e0e0e0",
                                                "filter": "blur(1.3px)",
                                                "transition": "all 0.5s ease-in-out",
                                            },
                                        )
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    "Logs",
                                                    style={
                                                        "background-color": "#1A1A19",
                                                        "color": "#ffffff",
                                                        "padding": "10px",
                                                        "font-weight": "bold",
                                                        "text-align": "center",
                                                        "border-radius": "10px 10px 0 0",
                                                    },
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(
                                                            "Logs will appear below in real-time:",
                                                            className="mb-2",
                                                        ),
                                                        html.Pre(
                                                            id="log-window",
                                                            className="log-window",
                                                            style={
                                                                "height": "479px",
                                                                "overflow-y": "auto",
                                                                "border": "1px solid #ddd",
                                                                "padding": "10px",
                                                                "background-color": "#f9f9f9",
                                                                "font-family": "monospace",
                                                                "border-radius": "8px",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            style={
                                                "opacity": "1",
                                                "pointer-events": "auto",
                                                "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",
                                                "border-radius": "12px",
                                                "background": "linear-gradient(to bottom, #ffffff, #f9f9f9)",
                                                "transition": "all 0.7s ease-in-out",
                                            },
                                        )
                                    ],
                                    width=8,
                                ),
                            ],
                            style={"margin-top": "20px"},
                        ),
                    ],
                ),
                # Tab 2: Data Transformation
                dbc.Tab(
                    label="Data Transformation",
                    tab_id="transformation",
                    label_style={
                        "font-weight": "bold",
                        "font-size": "16px",
                        "padding": "12px 20px",
                        "z-index": "200",
                    },
                    tab_style={
                        "border-radius": "12px 12px 0 0",
                        "background": "linear-gradient(to bottom, #ffffff, #f2f2f2)",
                        "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                        "transition": "all 0.3s ease",
                        "z-index": "200",
                    },
                    active_label_style={
                        "background": "linear-gradient(to bottom, #007bff, #0056b3)",
                        "color": "#ffffff",
                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.3)",
                        "z-index": "200",
                    },
                    children=[
                        dbc.Row(
                            [
                                # File Selection Section
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "File Selection",
                                                style=darker_header_style,
                                            ),
                                            dbc.CardBody(
                                                [
                                                    dbc.Button(
                                                        "Refresh Files",
                                                        id="refresh-files-button",
                                                        className="btn btn-primary",
                                                        style={"margin-bottom": "10px"},
                                                    ),
                                                    html.Div(
                                                        id="file-tree",
                                                        className="file-tree-item",
                                                        style={
                                                            "height": "300px",
                                                            "overflow-y": "auto",
                                                            "padding": "10px",
                                                            "background-color": "#f9f9f9",
                                                            "border-radius": "8px",
                                                        },
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style=active_card_style,
                                    ),
                                    width=6,
                                ),
                                # Transformation Output Section
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Transformation Output",
                                                style=darker_header_style,
                                            ),
                                            dbc.CardBody(
                                                [
                                                    dbc.Button(
                                                        "Transform Data",
                                                        id="transform-button",
                                                        color="info",
                                                        style={"margin-bottom": "10px"},
                                                    ),
                                                    html.Div(
                                                        id="transformation-status",
                                                        children="No transformation started.",
                                                        style={
                                                            "margin-top": "20px",
                                                            "color": "green",
                                                            "overflow-y": "auto",
                                                            "height": "200px",
                                                            "border": "1px solid #ddd",
                                                            "padding": "10px",
                                                            "background-color": "#f9f9f9",
                                                            "border-radius": "8px",
                                                        },
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style=active_card_style,
                                    ),
                                    width=6,
                                ),
                            ],
                            style={
                                "margin-bottom": "20px"
                            },  # Add spacing between this row and the next
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Logs", style=darker_header_style
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        "Transformation logs will appear below in real-time:",
                                                        className="mb-2",
                                                    ),
                                                    html.Pre(
                                                        id="transform-log-window",
                                                        className="log-window",
                                                        style={
                                                            "height": "479px",
                                                            "overflow-y": "auto",
                                                            "border": "1px solid #ddd",
                                                            "padding": "10px",
                                                            "background-color": "#f9f9f9",
                                                            "font-family": "monospace",
                                                            "border-radius": "8px",
                                                        },
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style=active_card_style,
                                    ),
                                    width=12,
                                )
                            ]
                        ),
                    ],
                ),
            ],
        ),
        # Footer
        html.Footer(
            html.Div(
                [
                    html.P(
                        "Written by the almighty Petr AI/DS because manual data scraping sucks",
                        className="mb-0",
                        style={
                            "color": "#ffffff",
                            "text-align": "center",
                            "font-weight": "bold",
                        },
                    ),
                    html.Div(
                        [
                            html.Span(
                                "Data Source: ",
                                style={"font-weight": "bold", "color": "#ffffff"},
                            ),
                            html.A(
                                "Statista.com",
                                href="https://www.statista.com",
                                target="_blank",
                                style={
                                    "color": "#007bff",
                                    "text-decoration": "none",
                                    "margin-right": "15px",
                                },
                            ),
                            html.Span(
                                "| Dashboard made by: ",
                                style={"font-weight": "bold", "color": "#ffffff"},
                            ),
                            html.A(
                                "Lakmoos AI",
                                href="https://lakmoos.com",
                                target="_blank",
                                style={"color": "#007bff", "text-decoration": "none"},
                            ),
                        ],
                        style={"text-align": "center", "margin-top": "10px"},
                    ),
                ],
                style={
                    "background-color": "#1A1A19",
                    "padding": "20px",
                    "border-top": "1px solid #4b4b4b",
                    "color": "#ffffff",
                    "width": "100%",
                    "text-align": "center",
                },
            ),
            style={
                "margin-top": "auto",
                "padding-top": "15px",
                "margin-left": "-12px",
                "margin-right": "-12px",
                "z-index": "10",
                "position": "relative",
            },
        ),
        # Refresh Intervals
        dcc.Interval(id="log-interval", interval=500, n_intervals=0),
        dcc.Interval(id="file-interval", interval=500, n_intervals=0),
    ],
    fluid=True,
    style={"display": "flex", "flex-direction": "column", "min-height": "100vh"},
)
