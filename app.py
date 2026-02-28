"""
Soccer Facility Lease Location Visualizer
A Dash app for evaluating potential indoor soccer facility lease locations
in the Baltimore/Timonium MD area.
"""

import base64
import io
from typing import Optional

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback_context, dash_table, dcc, html
from dash.exceptions import PreventUpdate

# ---------------------------------------------------------------------------
# Sample data – Baltimore / Timonium MD area
# ---------------------------------------------------------------------------
SAMPLE_DATA = [
    {
        "name": "Timonium Commerce Center",
        "address": "2000 W Padonia Rd",
        "city": "Timonium",
        "state": "MD",
        "zip": "21093",
        "lat": 39.4523,
        "lon": -76.6213,
        "square_footage": 42000,
        "monthly_rent": 28000,
        "asking_price": 336000,
        "lease_type": "NNN",
        "year_built": 1998,
        "parking_spaces": 180,
        "ceiling_height_ft": 32,
        "status": "Active",
    },
    {
        "name": "Cockeysville Industrial Park",
        "address": "10801 York Rd",
        "city": "Cockeysville",
        "state": "MD",
        "zip": "21030",
        "lat": 39.4782,
        "lon": -76.6427,
        "square_footage": 38500,
        "monthly_rent": 22500,
        "asking_price": 270000,
        "lease_type": "Gross",
        "year_built": 2004,
        "parking_spaces": 210,
        "ceiling_height_ft": 28,
        "status": "Under Review",
    },
    {
        "name": "Hunt Valley Business Center",
        "address": "11350 McCormick Rd",
        "city": "Hunt Valley",
        "state": "MD",
        "zip": "21031",
        "lat": 39.4956,
        "lon": -76.6421,
        "square_footage": 55000,
        "monthly_rent": 38500,
        "asking_price": 462000,
        "lease_type": "NNN",
        "year_built": 1995,
        "parking_spaces": 320,
        "ceiling_height_ft": 35,
        "status": "Active",
    },
    {
        "name": "Reisterstown Warehouse",
        "address": "430 Reisterstown Rd",
        "city": "Pikesville",
        "state": "MD",
        "zip": "21208",
        "lat": 39.3906,
        "lon": -76.7219,
        "square_footage": 28000,
        "monthly_rent": 15000,
        "asking_price": 180000,
        "lease_type": "Modified",
        "year_built": 1987,
        "parking_spaces": 95,
        "ceiling_height_ft": 22,
        "status": "Rejected",
    },
    {
        "name": "Owings Mills Distribution Hub",
        "address": "10202 Grand Central Ave",
        "city": "Owings Mills",
        "state": "MD",
        "zip": "21117",
        "lat": 39.4214,
        "lon": -76.7806,
        "square_footage": 47500,
        "monthly_rent": 31000,
        "asking_price": 372000,
        "lease_type": "NNN",
        "year_built": 2010,
        "parking_spaces": 260,
        "ceiling_height_ft": 30,
        "status": "Pending",
    },
    {
        "name": "Loch Raven Flex Space",
        "address": "8890 McGaw Rd",
        "city": "Columbia",
        "state": "MD",
        "zip": "21045",
        "lat": 39.3512,
        "lon": -76.8134,
        "square_footage": 33000,
        "monthly_rent": 19500,
        "asking_price": 234000,
        "lease_type": "Gross",
        "year_built": 2001,
        "parking_spaces": 140,
        "ceiling_height_ft": 26,
        "status": "Under Review",
    },
    {
        "name": "White Marsh Logistics Center",
        "address": "8115 Pepsi Pl",
        "city": "White Marsh",
        "state": "MD",
        "zip": "21236",
        "lat": 39.3763,
        "lon": -76.4581,
        "square_footage": 51000,
        "monthly_rent": 33500,
        "asking_price": 402000,
        "lease_type": "NNN",
        "year_built": 2007,
        "parking_spaces": 290,
        "ceiling_height_ft": 34,
        "status": "Active",
    },
    {
        "name": "Sparrows Point Industrial",
        "address": "3001 Eastern Blvd",
        "city": "Baltimore",
        "state": "MD",
        "zip": "21220",
        "lat": 39.2453,
        "lon": -76.4219,
        "square_footage": 60000,
        "monthly_rent": 27000,
        "asking_price": 324000,
        "lease_type": "Modified",
        "year_built": 1979,
        "parking_spaces": 380,
        "ceiling_height_ft": 38,
        "status": "Pending",
    },
    {
        "name": "Fullerton Commerce Park",
        "address": "7310 Pulaski Hwy",
        "city": "Baltimore",
        "state": "MD",
        "zip": "21237",
        "lat": 39.3421,
        "lon": -76.5012,
        "square_footage": 22000,
        "monthly_rent": 12500,
        "asking_price": 150000,
        "lease_type": "Gross",
        "year_built": 1993,
        "parking_spaces": 75,
        "ceiling_height_ft": 20,
        "status": "Rejected",
    },
    {
        "name": "Greenspring Valley Flex",
        "address": "2 Hamill Rd",
        "city": "Baltimore",
        "state": "MD",
        "zip": "21210",
        "lat": 39.3731,
        "lon": -76.6843,
        "square_footage": 35500,
        "monthly_rent": 24000,
        "asking_price": 288000,
        "lease_type": "NNN",
        "year_built": 2015,
        "parking_spaces": 155,
        "ceiling_height_ft": 29,
        "status": "Under Review",
    },
]

SAMPLE_DF = pd.DataFrame(SAMPLE_DATA)

# ---------------------------------------------------------------------------
# Constants & theming
# ---------------------------------------------------------------------------
STATUS_COLORS = {
    "Active": "#2ecc71",
    "Under Review": "#f39c12",
    "Rejected": "#e74c3c",
    "Pending": "#95a5a6",
}

STATUS_OPTIONS = [
    {"label": "Active", "value": "Active"},
    {"label": "Under Review", "value": "Under Review"},
    {"label": "Rejected", "value": "Rejected"},
    {"label": "Pending", "value": "Pending"},
]

LEASE_OPTIONS = [
    {"label": "All Lease Types", "value": "All"},
    {"label": "NNN", "value": "NNN"},
    {"label": "Gross", "value": "Gross"},
    {"label": "Modified", "value": "Modified"},
]

MAP_CENTER = {"lat": 39.43, "lon": -76.62}

CARD_STYLE = {
    "backgroundColor": "#2c2c3e",
    "border": "1px solid #444466",
    "borderRadius": "8px",
    "padding": "16px",
}

DARK_TABLE_STYLE = {
    "backgroundColor": "#1a1a2e",
    "color": "#e0e0e0",
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def build_size_scale(sqft_series: pd.Series, min_px: int = 8, max_px: int = 28) -> list:
    """Scale square footage values to marker pixel sizes."""
    lo, hi = sqft_series.min(), sqft_series.max()
    if lo == hi:
        return [18] * len(sqft_series)
    return [
        min_px + (v - lo) / (hi - lo) * (max_px - min_px) for v in sqft_series
    ]


def build_map(df: pd.DataFrame, selected_idx: Optional[int] = None) -> go.Figure:
    """Build the Plotly Scattermapbox figure."""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            mapbox=dict(style="carto-darkmatter", center=MAP_CENTER, zoom=10),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#1a1a2e",
            plot_bgcolor="#1a1a2e",
        )
        return fig

    sizes = build_size_scale(df["square_footage"])
    colors = [STATUS_COLORS.get(s, "#aaaaaa") for s in df["status"]]

    hover_texts = []
    for _, row in df.iterrows():
        ht = (
            f"<b>{row['name']}</b><br>"
            f"{row['address']}, {row['city']}, {row['state']}<br>"
            f"<br>"
            f"Status: <b>{row['status']}</b><br>"
            f"Sq Ft: <b>{row['square_footage']:,}</b><br>"
            f"Monthly Rent: <b>${row['monthly_rent']:,}</b><br>"
            f"Lease: <b>{row['lease_type']}</b><br>"
            f"Ceiling: <b>{row['ceiling_height_ft']} ft</b><br>"
            f"Parking: <b>{row['parking_spaces']} spaces</b>"
        )
        hover_texts.append(ht)

    # Build separate traces per status for a clean legend
    traces = []
    for status, color in STATUS_COLORS.items():
        mask = df["status"] == status
        if not mask.any():
            continue
        sub = df[mask]
        sub_sizes = [sizes[i] for i in sub.index - df.index[0]] if not df.index.equals(pd.RangeIndex(len(df))) else [sizes[i] for i in sub.index]

        # Recalculate sizes for filtered subset properly
        all_sizes = build_size_scale(df["square_footage"])
        sub_sizes = [all_sizes[df.index.get_loc(i)] for i in sub.index]

        sub_hover = [hover_texts[df.index.get_loc(i)] for i in sub.index]

        # Marker outlines for selected
        line_colors = []
        line_widths = []
        for i in sub.index:
            if selected_idx is not None and i == selected_idx:
                line_colors.append("#ffffff")
                line_widths.append(3)
            else:
                line_colors.append(color)
                line_widths.append(1)

        traces.append(
            go.Scattermapbox(
                lat=sub["lat"],
                lon=sub["lon"],
                mode="markers",
                marker=dict(
                    size=sub_sizes,
                    color=color,
                    opacity=0.9,
                    sizemode="diameter",
                    line=dict(color=line_colors, width=line_widths),
                ),
                text=sub_hover,
                hovertemplate="%{text}<extra></extra>",
                customdata=sub.index.tolist(),
                name=status,
            )
        )

    fig = go.Figure(data=traces)
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=MAP_CENTER,
            zoom=10,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        legend=dict(
            bgcolor="#2c2c3e",
            bordercolor="#444466",
            borderwidth=1,
            font=dict(color="#e0e0e0", size=12),
            x=0.01,
            y=0.99,
        ),
        uirevision="map",
    )
    return fig


def build_radar(scores: dict) -> go.Figure:
    """Build a radar chart from a dict of {category: score}."""
    categories = list(scores.keys())
    values = list(scores.values())
    # Close the loop
    categories_loop = categories + [categories[0]]
    values_loop = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_loop,
            theta=categories_loop,
            fill="toself",
            fillcolor="rgba(46, 204, 113, 0.25)",
            line=dict(color="#2ecc71", width=2),
            marker=dict(color="#2ecc71", size=8),
            name="Score",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="#1a1a2e",
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(color="#aaaaaa", size=10),
                gridcolor="#444466",
                linecolor="#444466",
            ),
            angularaxis=dict(
                tickfont=dict(color="#e0e0e0", size=11),
                gridcolor="#444466",
                linecolor="#444466",
            ),
        ),
        paper_bgcolor="#2c2c3e",
        plot_bgcolor="#2c2c3e",
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False,
        height=260,
    )
    return fig


def score_from_row(row: pd.Series) -> dict:
    """Derive initial location scores from property data."""
    # Ceiling height: 1–5 based on 20–40 ft range
    ceiling_score = min(5, max(1, round((row["ceiling_height_ft"] - 18) / 4.5)))
    # Parking: 1–5 based on 50–350 spaces
    parking_score = min(5, max(1, round((row["parking_spaces"] - 50) / 60)))
    # Accessibility: proxy from year_built recency
    access_score = min(5, max(1, round((row["year_built"] - 1975) / 10)))
    # Cost: inverse of rent relative to range
    cost_score = min(5, max(1, round(6 - (row["monthly_rent"] - 10000) / 7500)))
    return {
        "Ceiling": ceiling_score,
        "Parking": parking_score,
        "Accessibility": access_score,
        "Cost": cost_score,
    }


def detail_card(row: pd.Series, scores: dict) -> html.Div:
    """Build the detail panel content for a selected property."""
    badge_color = {
        "Active": "success",
        "Under Review": "warning",
        "Rejected": "danger",
        "Pending": "secondary",
    }.get(row["status"], "secondary")

    return html.Div(
        [
            # Header row
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5(row["name"], className="mb-1", style={"color": "#e0e0e0"}),
                            html.Small(
                                f"{row['address']}, {row['city']}, {row['state']} {row['zip']}",
                                style={"color": "#aaaaaa"},
                            ),
                        ],
                        width=9,
                    ),
                    dbc.Col(
                        dbc.Badge(row["status"], color=badge_color, className="fs-6 px-3 py-2"),
                        width=3,
                        className="text-end",
                    ),
                ],
                className="mb-3",
            ),
            # Key metrics row
            dbc.Row(
                [
                    _metric_col("Square Footage", f"{row['square_footage']:,} sq ft"),
                    _metric_col("Monthly Rent", f"${row['monthly_rent']:,}"),
                    _metric_col("Asking Price", f"${row['asking_price']:,}"),
                    _metric_col("Lease Type", row["lease_type"]),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    _metric_col("Year Built", str(row["year_built"])),
                    _metric_col("Parking Spaces", str(row["parking_spaces"])),
                    _metric_col("Ceiling Height", f"{row['ceiling_height_ft']} ft"),
                    _metric_col("Coordinates", f"{row['lat']:.4f}, {row['lon']:.4f}"),
                ],
                className="mb-3",
            ),
            html.Hr(style={"borderColor": "#444466"}),
            # Scoring section
            html.H6("Location Scoring", style={"color": "#aaaaaa", "textTransform": "uppercase", "letterSpacing": "1px"}),
            html.P("Adjust scores (1–5) and the radar chart updates in real time.", style={"color": "#777788", "fontSize": "12px"}),
            dbc.Row(
                [
                    _score_col("Ceiling Height", "score-ceiling", scores["Ceiling"]),
                    _score_col("Parking", "score-parking", scores["Parking"]),
                    _score_col("Accessibility", "score-access", scores["Accessibility"]),
                    _score_col("Cost", "score-cost", scores["Cost"]),
                ],
                className="mb-2",
            ),
            dcc.Graph(id="radar-chart", figure=build_radar(scores), config={"displayModeBar": False}),
        ]
    )


def _metric_col(label: str, value: str) -> dbc.Col:
    return dbc.Col(
        html.Div(
            [
                html.Div(label, style={"color": "#888899", "fontSize": "11px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                html.Div(value, style={"color": "#e0e0e0", "fontWeight": "600", "fontSize": "15px"}),
            ],
            style={"backgroundColor": "#1a1a2e", "borderRadius": "6px", "padding": "10px 12px"},
        ),
        width=3,
    )


def _score_col(label: str, component_id: str, value: int) -> dbc.Col:
    return dbc.Col(
        html.Div(
            [
                html.Label(label, style={"color": "#aaaaaa", "fontSize": "12px", "display": "block", "marginBottom": "4px"}),
                dcc.Slider(
                    id=component_id,
                    min=1,
                    max=5,
                    step=1,
                    value=value,
                    marks={i: str(i) for i in range(1, 6)},
                    tooltip={"always_visible": False},
                    className="score-slider",
                ),
            ],
            style={"backgroundColor": "#1a1a2e", "borderRadius": "6px", "padding": "10px 12px"},
        ),
        width=3,
    )


def build_table(df: pd.DataFrame, selected_idx: Optional[int] = None) -> tuple:
    """Return (columns, data, style_data_conditional) for the DataTable."""
    display_cols = [
        "name", "city", "status", "lease_type",
        "square_footage", "monthly_rent", "ceiling_height_ft", "parking_spaces",
    ]
    col_labels = {
        "name": "Property Name",
        "city": "City",
        "status": "Status",
        "lease_type": "Lease",
        "square_footage": "Sq Ft",
        "monthly_rent": "Rent/Mo",
        "ceiling_height_ft": "Ceiling (ft)",
        "parking_spaces": "Parking",
    }
    columns = [{"name": col_labels[c], "id": c, "sortable": True} for c in display_cols]

    records = df[display_cols].copy()
    records["square_footage"] = records["square_footage"].apply(lambda x: f"{x:,}")
    records["monthly_rent"] = records["monthly_rent"].apply(lambda x: f"${x:,}")
    data = records.to_dict("records")

    # Attach original index so we can identify selected row
    for i, (orig_idx, _) in enumerate(df.iterrows()):
        data[i]["_orig_idx"] = orig_idx

    conditional = [
        {
            "if": {"filter_query": f"{{status}} = '{s}'", "column_id": "status"},
            "color": STATUS_COLORS[s],
            "fontWeight": "bold",
        }
        for s in STATUS_COLORS
    ]

    if selected_idx is not None and selected_idx in df.index:
        # Find position in displayed data
        pos = df.index.tolist().index(selected_idx)
        conditional.append(
            {
                "if": {"row_index": pos},
                "backgroundColor": "#2c3e50",
                "border": "1px solid #2ecc71",
            }
        )

    return columns, data, conditional


# ---------------------------------------------------------------------------
# App layout
# ---------------------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
)
app.title = "Soccer Facility Lease Finder"
server = app.server  # For deployment

sidebar = dbc.Card(
    [
        html.H5("Filters", style={"color": "#e0e0e0", "fontWeight": "700", "marginBottom": "20px"}),

        # CSV Upload
        html.Label("Load CSV Data", style={"color": "#aaaaaa", "fontSize": "12px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag & Drop or ", html.A("Browse CSV", style={"color": "#2ecc71"})],
                style={"fontSize": "13px", "color": "#888899"},
            ),
            style={
                "width": "100%",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "6px",
                "borderColor": "#444466",
                "textAlign": "center",
                "padding": "12px",
                "marginBottom": "16px",
                "backgroundColor": "#1a1a2e",
                "cursor": "pointer",
            },
            multiple=False,
        ),
        html.Div(id="upload-status", style={"color": "#888899", "fontSize": "11px", "marginBottom": "16px"}),

        html.Hr(style={"borderColor": "#444466"}),

        # Status filter
        html.Label("Status", style={"color": "#aaaaaa", "fontSize": "12px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
        dcc.Checklist(
            id="filter-status",
            options=STATUS_OPTIONS,
            value=["Active", "Under Review", "Rejected", "Pending"],
            labelStyle={"display": "flex", "alignItems": "center", "gap": "8px", "marginBottom": "6px", "color": "#e0e0e0"},
            inputStyle={"accentColor": "#2ecc71"},
            className="mb-3",
        ),

        html.Hr(style={"borderColor": "#444466"}),

        # Square footage slider
        html.Label("Square Footage", style={"color": "#aaaaaa", "fontSize": "12px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
        dcc.RangeSlider(
            id="filter-sqft",
            min=15000,
            max=60000,
            step=500,
            value=[15000, 60000],
            marks={15000: "15k", 30000: "30k", 45000: "45k", 60000: "60k"},
            tooltip={"placement": "bottom", "always_visible": False},
            className="mb-3",
        ),

        html.Hr(style={"borderColor": "#444466"}),

        # Monthly rent slider
        html.Label("Monthly Rent ($)", style={"color": "#aaaaaa", "fontSize": "12px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
        dcc.RangeSlider(
            id="filter-rent",
            min=10000,
            max=45000,
            step=500,
            value=[10000, 45000],
            marks={10000: "$10k", 20000: "$20k", 30000: "$30k", 45000: "$45k"},
            tooltip={"placement": "bottom", "always_visible": False},
            className="mb-3",
        ),

        html.Hr(style={"borderColor": "#444466"}),

        # Lease type dropdown
        html.Label("Lease Type", style={"color": "#aaaaaa", "fontSize": "12px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
        dcc.Dropdown(
            id="filter-lease",
            options=LEASE_OPTIONS,
            value="All",
            clearable=False,
            style={"backgroundColor": "#1a1a2e", "color": "#e0e0e0"},
            className="mb-3",
        ),

        html.Hr(style={"borderColor": "#444466"}),
        html.Div(
            id="filter-count",
            style={"color": "#888899", "fontSize": "12px", "textAlign": "center"},
        ),
    ],
    style={
        "backgroundColor": "#2c2c3e",
        "border": "1px solid #444466",
        "borderRadius": "8px",
        "padding": "20px",
        "height": "100%",
    },
)

app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2(
                            "⚽ Soccer Facility Lease Finder",
                            style={"color": "#2ecc71", "fontWeight": "800", "margin": "0"},
                        ),
                        html.P(
                            "Baltimore / Timonium MD · Potential Indoor Soccer Facility Locations",
                            style={"color": "#888899", "margin": "0", "fontSize": "14px"},
                        ),
                    ],
                    style={"padding": "20px 0 12px 0"},
                )
            )
        ),

        # Stores
        dcc.Store(id="store-df", storage_type="memory"),
        dcc.Store(id="store-selected-idx", storage_type="memory"),
        dcc.Store(id="store-scores", storage_type="memory"),

        # Main layout: sidebar + map
        dbc.Row(
            [
                # Sidebar
                dbc.Col(sidebar, width=3, style={"paddingRight": "8px"}),

                # Map + detail
                dbc.Col(
                    [
                        # Map
                        dbc.Card(
                            dcc.Graph(
                                id="map-graph",
                                style={"height": "480px"},
                                config={"scrollZoom": True, "displayModeBar": True, "modeBarButtonsToRemove": ["select2d", "lasso2d"]},
                            ),
                            style={"backgroundColor": "#1a1a2e", "border": "1px solid #444466", "borderRadius": "8px", "overflow": "hidden", "marginBottom": "12px"},
                        ),

                        # Detail panel
                        dbc.Card(
                            [
                                html.Div(id="detail-panel", children=html.Div(
                                    "Click a map marker to view property details.",
                                    style={"color": "#555577", "textAlign": "center", "padding": "40px 0", "fontSize": "14px"},
                                )),
                            ],
                            style={"backgroundColor": "#2c2c3e", "border": "1px solid #444466", "borderRadius": "8px", "padding": "20px", "marginBottom": "12px"},
                        ),
                    ],
                    width=9,
                    style={"paddingLeft": "8px"},
                ),
            ],
            className="mb-3",
            align="start",
        ),

        # Summary table
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        html.H5(
                            "Summary Table",
                            style={"color": "#e0e0e0", "fontWeight": "700", "marginBottom": "12px"},
                        ),
                        dash_table.DataTable(
                            id="summary-table",
                            sort_action="native",
                            style_table={"overflowX": "auto"},
                            style_header={
                                "backgroundColor": "#1a1a2e",
                                "color": "#aaaaaa",
                                "fontWeight": "600",
                                "border": "1px solid #444466",
                                "textTransform": "uppercase",
                                "fontSize": "11px",
                                "letterSpacing": "0.5px",
                            },
                            style_cell={
                                "backgroundColor": "#2c2c3e",
                                "color": "#e0e0e0",
                                "border": "1px solid #333355",
                                "padding": "10px 14px",
                                "fontSize": "13px",
                                "textAlign": "left",
                            },
                            style_data_conditional=[],
                            page_size=10,
                        ),
                    ],
                    style={"backgroundColor": "#2c2c3e", "border": "1px solid #444466", "borderRadius": "8px", "padding": "20px"},
                )
            )
        ),

        # Footer
        dbc.Row(
            dbc.Col(
                html.P(
                    "Soccer Facility Lease Finder · Built with Dash & Plotly",
                    style={"color": "#444466", "textAlign": "center", "fontSize": "12px", "padding": "20px 0 8px 0"},
                )
            )
        ),
    ],
    fluid=True,
    style={"backgroundColor": "#1a1a2e", "minHeight": "100vh", "padding": "0 24px"},
)


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@app.callback(
    Output("store-df", "data"),
    Output("upload-status", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=False,
)
def load_data(contents, filename):
    """Load CSV data or fall back to sample data."""
    if contents is None:
        return SAMPLE_DF.to_dict("records"), "Using sample data (10 locations)"

    try:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        required = {"name", "address", "city", "state", "zip", "lat", "lon",
                    "square_footage", "monthly_rent", "asking_price",
                    "lease_type", "year_built", "parking_spaces",
                    "ceiling_height_ft", "status"}
        missing = required - set(df.columns)
        if missing:
            return SAMPLE_DF.to_dict("records"), f"CSV missing columns: {', '.join(missing)}. Using sample data."
        return df.to_dict("records"), f"Loaded {filename} ({len(df)} locations)"
    except Exception as e:
        return SAMPLE_DF.to_dict("records"), f"Error reading file: {e}. Using sample data."


@app.callback(
    Output("map-graph", "figure"),
    Output("summary-table", "columns"),
    Output("summary-table", "data"),
    Output("summary-table", "style_data_conditional"),
    Output("filter-count", "children"),
    Input("store-df", "data"),
    Input("filter-status", "value"),
    Input("filter-sqft", "value"),
    Input("filter-rent", "value"),
    Input("filter-lease", "value"),
    Input("store-selected-idx", "data"),
)
def update_map_and_table(records, statuses, sqft_range, rent_range, lease_type, selected_idx):
    """Apply filters and redraw map + table."""
    df = pd.DataFrame(records) if records else SAMPLE_DF.copy()

    # Apply filters
    mask = (
        df["status"].isin(statuses)
        & df["square_footage"].between(sqft_range[0], sqft_range[1])
        & df["monthly_rent"].between(rent_range[0], rent_range[1])
    )
    if lease_type and lease_type != "All":
        mask &= df["lease_type"] == lease_type

    filtered = df[mask].reset_index(drop=True)

    # Resolve selected index in filtered frame
    sel = selected_idx if selected_idx is not None and selected_idx < len(filtered) else None

    fig = build_map(filtered, selected_idx=sel)
    cols, data, cond = build_table(filtered, selected_idx=sel)
    count_text = f"{len(filtered)} location{'s' if len(filtered) != 1 else ''} shown"

    return fig, cols, data, cond, count_text


@app.callback(
    Output("store-selected-idx", "data"),
    Output("store-scores", "data"),
    Input("map-graph", "clickData"),
    State("store-df", "data"),
    State("filter-status", "value"),
    State("filter-sqft", "value"),
    State("filter-rent", "value"),
    State("filter-lease", "value"),
    prevent_initial_call=True,
)
def capture_map_click(click_data, records, statuses, sqft_range, rent_range, lease_type):
    """Store the index and initial scores of a clicked marker."""
    if click_data is None:
        raise PreventUpdate

    df = pd.DataFrame(records) if records else SAMPLE_DF.copy()

    # Apply same filters to get correct indices
    mask = (
        df["status"].isin(statuses)
        & df["square_footage"].between(sqft_range[0], sqft_range[1])
        & df["monthly_rent"].between(rent_range[0], rent_range[1])
    )
    if lease_type and lease_type != "All":
        mask &= df["lease_type"] == lease_type
    filtered = df[mask].reset_index(drop=True)

    point = click_data["points"][0]
    # customdata holds the original index in filtered df
    idx = point.get("customdata", 0)
    if idx >= len(filtered):
        raise PreventUpdate

    row = filtered.iloc[idx]
    scores = score_from_row(row)
    return idx, scores


@app.callback(
    Output("detail-panel", "children"),
    Input("store-selected-idx", "data"),
    Input("store-scores", "data"),
    Input("score-ceiling", "value"),
    Input("score-parking", "value"),
    Input("score-access", "value"),
    Input("score-cost", "value"),
    State("store-df", "data"),
    State("filter-status", "value"),
    State("filter-sqft", "value"),
    State("filter-rent", "value"),
    State("filter-lease", "value"),
    prevent_initial_call=True,
)
def update_detail(selected_idx, init_scores, ceiling, parking, access, cost,
                  records, statuses, sqft_range, rent_range, lease_type):
    """Render the detail card; slider changes update the radar live."""
    if selected_idx is None or init_scores is None:
        raise PreventUpdate

    df = pd.DataFrame(records) if records else SAMPLE_DF.copy()
    mask = (
        df["status"].isin(statuses)
        & df["square_footage"].between(sqft_range[0], sqft_range[1])
        & df["monthly_rent"].between(rent_range[0], rent_range[1])
    )
    if lease_type and lease_type != "All":
        mask &= df["lease_type"] == lease_type
    filtered = df[mask].reset_index(drop=True)

    if selected_idx >= len(filtered):
        raise PreventUpdate

    row = filtered.iloc[selected_idx]

    ctx = callback_context
    # Determine scores: use slider values if sliders triggered the callback
    slider_ids = {"score-ceiling", "score-parking", "score-access", "score-cost"}
    triggered = {t["prop_id"].split(".")[0] for t in ctx.triggered}

    if triggered & slider_ids:
        scores = {
            "Ceiling": ceiling if ceiling is not None else init_scores["Ceiling"],
            "Parking": parking if parking is not None else init_scores["Parking"],
            "Accessibility": access if access is not None else init_scores["Accessibility"],
            "Cost": cost if cost is not None else init_scores["Cost"],
        }
    else:
        scores = init_scores

    return detail_card(row, scores)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
