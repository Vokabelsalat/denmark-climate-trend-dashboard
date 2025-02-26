# -*- coding: utf-8 -*-

# Import necessary libraries
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from plotly.colors import sample_colorscale
from plotly.subplots import make_subplots

from use_cases import use_cases, use_cases_data
from info_sheet import info_sheet

import warnings
from numpy import RankWarning
warnings.simplefilter('ignore', RankWarning)

# File paths
geojson_grid_file = "data/base_grid.geojson"
geojson_municipality_file = "data/base_grid_municipality.geojson"
csv_grid_file = "data/climate_data_combined_v2.csv"
csv_municipality_file = "data/climate_data_municipality_combined.csv"
csv_grid_parameter_file = "data/climate_parameters_combined_v2.csv"
csv_municipality_parameter_file = "data/climate_parameters_municipality_combined_v2.csv"

# Load the GeoJSON files
with open(geojson_grid_file, "r") as f:
    geojson_grid_data = json.load(f)

with open(geojson_municipality_file, "r") as f:
    geojson_municipality_data = json.load(f)

# Load the climate data with explicit types for cell_id
data_grid = pd.read_csv(csv_grid_file)
data_municipality = pd.read_csv(csv_municipality_file, dtype={"cell_id": str})
parameter_grid = pd.read_csv(csv_grid_parameter_file)
parameter_municipality = pd.read_csv(csv_municipality_parameter_file, dtype={"cell_id": str})

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div([
            html.A(
                children=[html.Div(
                    "Denmark Climate Trend Dashboard",
                    style={
                        "margin": "0",
                        "fontSize": "xx-large",
                        "fontWeight": "bold",
                        "color": "#333333",  # Dark text for contrast
                    }
                )],
                href="/"
            ),
            # Hidden stores for selected data
            dcc.Store(id="selected-months", data=[]),
            dcc.Store(id="selected-regions", data=[]),
            dcc.Store(id="selected_year", data=None),
            dcc.Store(id="stored-selected-regions", data=[]),
            
            info_sheet,
            html.Div([
                # All the use case buttons imported from use_cases.py
                use_cases, 
                # Info button
                html.Button(
                    id="info-button",
                    className="scale-on-hover",
                    n_clicks=0,
                    title="Click for information",  # Tooltip text on hover
                    children=[
                        html.Img(
                            src="/assets/info_button.png",  # Path to the symbol image
                            style={
                                "width": "25px",
                                "height": "25px",
                            }
                        ),
                        html.Span(
                            "Dashboard Guide",
                            style={
                                "fontSize": "20px",  # Font size
                            }
                        ),
                    ]
                )
            ], style={"display": "flex", "flexDirection": "row", "gap": "10px"})
        ], className="headerWrapper"),
        html.Div([
            html.Div([
                html.Div([
                    html.Label(
                        "Select/Deselect Month(s):", 
                        style={"fontSize": "18px", "margin": "5px"}
                    ),
                    dcc.Graph(
                        id="temp-wheel", 
                        config={"displayModeBar": False}
                    ),
                    html.Div([
                        html.Label(
                            "Select Year Range:", 
                            style={"fontSize": "18px", "margin": "0px"}
                        ),
                        dcc.RangeSlider(
                            id="year-slider",
                            min=int(data_grid["year"].min()),
                            max=int(data_grid["year"].max()),
                            step=1,
                            marks={
                                int(year): {
                                    'label': str(year), 
                                    'style': {'transform': 'rotate(45deg)', 'white-space': 'nowrap'}
                                } for year in data_grid["year"].unique()
                            },
                            value=[2011, 2024],
                            allowCross=True
                        )
                    ], style={"margin": "10px 0", "display": "none"}),
                    html.Div(
                        children=[
                            # Left side: Existing parameter selection
                            html.Div(
                                children=[
                                    html.Label(
                                        [
                                            html.Div([
                                                html.Img(src="/assets/chart-line-solid.svg", height=25),
                                                html.Span("Parameter:", style={'padding-left': 5}),
                                            ], style={"display": "flex", "alignItems": "center"}),
                                            html.Div("→", style={'padding-left': 5}),
                                        ],
                                        style={ "fontWeight": "bold", "margin": "0px", "display": "flex", "alignItems": "center", "justifyContent": "space-between"}
                                    ),
                                    dcc.RadioItems(
                                        id="parameter-dropdown",
                                        options=[
                                            {"label":  [
                                                    html.Img(src="/assets/temperature-arrow-up-solid.svg", height=20),
                                                    html.Span("Max. Temp."),
                                                ], 
                                                "value": "max_temp"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/temperature-half-solid.svg", height=20),
                                                    html.Span("Mean Temp."),
                                                ], 
                                                "value": "mean_temp"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/temperature-arrow-down-solid.svg", height=20),
                                                    html.Span("Min. Temp."),
                                                ], 
                                                "value": "min_temp"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/droplet-solid.svg", height=20),
                                                    html.Span("Acc. Precip."),
                                                ], 
                                                "value": "acc_precip"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/wind-solid.svg", height=20),
                                                    html.Span("Mean Wind"),
                                                ], 
                                                "value": "mean_wind"
                                            },
                                        ],
                                        value="mean_temp",
                                        className="options",
                                        labelStyle={'display': 'block', 'fontSize': '18px', 'marginTop': "5px"}
                                    )
                                ],
                                style={"flex": "1", "margin": "10px"}
                            ),
                            # Right side: New subparameter selection with four buttons
                            html.Div(
                                children=[
                                    html.Label(
                                        [
                                            html.Img(src="/assets/chart-column-solid.svg", height=25),
                                            html.Span("Parameter:", style={'padding-left': 5}),
                                        ],
                                        style={ "fontWeight": "bold", "margin": "0px", "display": "flex", "alignItems": "center"}
                                    ),
                                    dcc.RadioItems(
                                        id="parameter-dropdown2",
                                        options=[
                                            {"label":  [
                                                    html.Img(src="/assets/snowflake-solid.svg", height=20),
                                                    html.Span("Ice Days"),
                                                ], 
                                                "value": "ice_para"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/mitten-solid.svg", height=20),
                                                    html.Span("Heat. Deg. Days"),
                                                ], 
                                                "value": "heat_para"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/sun-solid.svg", height=20),
                                                    html.Span("Summer Days"),
                                                ], 
                                                "value": "summer_para"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/cloud-showers-water-solid.svg", height=20),
                                                    html.Span("Extreme Rain Days"),
                                                ], 
                                                "value": "extrain_para"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/wind-solid.svg", height=20),
                                                    html.Span("Max. Wind"),
                                                ], 
                                                "value": "maxwind_para"
                                            },
                                            {"label":  [
                                                    html.Img(src="/assets/sun-regular.svg", height=20),
                                                    html.Span("Bright Sunshine"),
                                                ], 
                                                "value": "brightsun_para"
                                            },
                                        ],
                                        value="heat_para",
                                        labelStyle={"display": "flex", "align-items": "center", 'fontSize': '18px', 'marginTop': "5px"},
                                        className="options",
                                        style={"marginRight": "15px"}
                                        # labelStyle={'display': 'block', 'fontSize': '18px', 'marginTop': "5px"}
                                    ),
                                    html.Div("↘", style={"textAlign": "end"})
                                ],
                                style={"margin": "10px", "display": "flex", "flexDirection": "column", "alignSelf": "end"}
                            )
                        ],
                        className="parameters-wrapper"
                    ),
                    html.Label(
                        "To select regions, click on map ↓ ", 
                        style={"fontSize": "18px", "font-style": "italic", "margin": "0px", "marginLeft": "10px"}
                    ),
                    # html.Div(
                    #     children=[
                    #         # Reset Filters button (unchanged)
                    #         html.A(
                    #             html.Button(
                    #                 id="reset-button",
                    #                 style={
                    #                     "width": "150px",
                    #                     "height": "35px",
                    #                     "backgroundColor": "rgba(220, 220, 220, 1)",
                    #                     "border": "2px solid rgba(220, 220, 220, 1)",
                    #                     "borderRadius": "14px",
                    #                     "display": "flex",
                    #                     "alignItems": "center",
                    #                     "justifyContent": "center",
                    #                     "gap": "10px",
                    #                     "cursor": "pointer",
                    #                     "padding": "6px"
                    #                 },
                    #                 n_clicks=0,
                    #                 title="Reset filters",
                    #                 children=[
                    #                     html.Img(
                    #                         src="/assets/reset.png",
                    #                         style={"width": "25px", "height": "25px"}
                    #                     ),
                    #                     html.Span(
                    #                         "Reset Filters",
                    #                         style={
                    #                             "fontFamily": "Segoe UI, sans-serif",
                    #                             "color": "black",
                    #                             "fontSize": "16px",
                    #                             "fontWeight": "bold"
                    #                         }
                    #                     )
                    #                 ]
                    #             ),
                    #             href="/",
                    #             style={"textDecoration": "none", "margin": "10px 6px"}
                    #         ),
                    #     ],
                    #     style={"display": "flex", "alignItems": "center"}
                    # )
                ], className="menu"),
            ], className="menuWrapper"),
            html.Div([
                dcc.Graph(id="trend-map", style={"width": "100%", "height": "100%", "position": "relative", "z-index": "1"}, config={"displayModeBar": False},),
                    html.Div([
                        html.Label("Spatial Resolution:", style={"fontSize": "18px", "fontWeight": "bold", "marginBottom": "5px"}),
                        dcc.RadioItems(
                            id="visualization-mode",
                            options=[
                                {"label": "Municipalities", "value": "municipality"},
                                {"label": "10x10km grid", "value": "grid"}
                            ],
                            value="municipality",  # Default mode
                            labelStyle={'display': 'block', 'font-size': '18px'},
                            className="options"
                        )
                    ], style={
                        "position": "absolute",
                        "top": "21px",
                        "left": "11px",
                        "z-index": "2",
                        "background": "rgba(255, 255, 255, 0.7)",
                        "padding": "10px",
                        "border-radius": "5px",
                        "box-shadow": "0 2px 5px rgba(0,0,0,0.2)",
                    }),
                    # Toggle switch container
                    # html.Div(
                    #     children=[
                    #         # The toggle switch
                    #         daq.BooleanSwitch(
                    #             id="map-parameter-toggle",
                    #             on=False,  # Set default state here
                    #             color="purple",
                    #             style={"verticalAlign": "middle"}
                    #         ),
                    #         # Label that will update based on the toggle state
                    #         html.Div(
                    #             id="map-parameter-toggle-label",
                    #             children="Show main parameters on map",
                    #             style={"fontSize": "16px", "fontWeight": "bold", "marginRight": "10px"}
                    #         ),
                    #     ],
                    #     style={"display": "none", "alignItems": "center"}
                    # ),
                     html.Div([
                        html.Label("Parameters on map:", style={"fontSize": "18px", "fontWeight": "bold", "marginBottom": "5px"}),
                        dcc.RadioItems(
                            id="map-parameter-select",
                            options=[
                                 {"label":  [
                                        html.Img(src="/assets/chart-line-solid.svg", height=20),
                                        html.Span("Measurements"),
                                    ], 
                                    "value": "main"
                                },
                                {"label":  [
                                        html.Img(src="/assets/chart-column-solid.svg", height=20),
                                        html.Span("Derrived Params"),
                                    ], 
                                    "value": "sub"
                                },
                            ],
                            value="main",  # Default mode
                            labelStyle={'display': 'block', 'font-size': '18px'},
                            className="options"
                        )
                    ], style={
                        "position": "absolute",
                        "top": "21px",
                        "right": "110px",
                        "z-index": "2",
                        "background": "rgba(255, 255, 255, 0.7)",
                        "padding": "10px",
                        "border-radius": "5px",
                        "box-shadow": "0 2px 5px rgba(0,0,0,0.2)",
                    })
            ], className="mapWrapper"),
        ], className="leftColumn"),
        html.Div(
        [
            html.Div([
                dcc.Graph(
                    id="timeline",
                    style={"width": "100%", "height": "100%", "margin": "0px"},
                    config={"displayModeBar": False}
                ),
                html.Label(
                    id="dynamic-label-timeline",
                    className="dynamic-label",
                    style={"top": "11px"}
                ),
                html.Div([
                    dcc.Checklist(
                        id="trendline-toggle",
                        options=[{"label": "Show Trendlines", "value": "show"}],
                        value=["show"],
                        labelStyle={"fontSize": "16px", "fontWeight": "bold"}
                    ),
                    dcc.Checklist(
                        id="relative-values-toggle",
                        options=[{"label": "Use Relative Values", "value": "use"}],
                        value=[],
                        labelStyle={"fontSize": "16px", "fontWeight": "bold"}
                    )],
                    className="chartOptions"
                )
            ], className="lineChartWrapper"),
            # html.Div([
            # ], className="timeSlideWrapper"),
            html.Div([
                dcc.Graph(
                    id="bar_chart",
                    style={"width": "105%", "height": "100%"},
                    config={"displayModeBar": False},
                ),
                html.Label(
                    id="dynamic-label-barchart",
                    className="dynamic-label"
                ),
                html.Div(
                    [
                        dcc.Checklist(
                            id="barchart-toggle",
                            options=[{"label": "Show Trendlines", "value": "show"}],
                            value=["show"],
                            labelStyle={"fontSize": "16px", "fontWeight": "bold"},
                        ),
                        html.Button([
                             html.Img(
                                src="/assets/reset.png",
                                style={"width": "20px", "height": "20px"}
                            ),
                            html.Span(
                                "Reset Zoom",
                            )
                        ], id="reset-zoom", n_clicks=0, className="resetButton scale-on-hover"),
                        # dcc.Checklist(
                        #     id="relative-values-toggle-barchart",
                        #     options=[{"label": "Use Relative Values", "value": "use"}],
                        #     value=["use"],
                        #     labelStyle={"fontSize": "16px", "fontWeight": "bold"}
                        # ),
                    ],
                    className="chartOptions"
                ),
            ], className="barChartWrapper"),
        ]
        , className="rightColumn"),
    ],
    className="main"
)

# Colors for municipalities
#COLOR_PALETTE = ["gold", "coral", "mediumpurple"]
COLOR_PALETTE = ["#F2CF66", "#F2AFA0", "#BBADD9"]
DK_COLOR = "#91BF8A"

# @app.callback(
#     Output("map-parameter-toggle-label", "children"),
#     Input("map-parameter-toggle", "on")
# )
# def update_toggle_label(is_on):
#     return "Display sub-parameters" if is_on else "Display main parameters"

@app.callback(
    Output("info-sheet", "style"),
    [Input("info-button", "n_clicks"), Input("close-info", "n_clicks")],
    prevent_initial_call=True
)
def toggle_info_sheet(info_clicks, close_clicks):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "info-button":
        return {
            "position": "fixed",
            "top": "0",
            "right": "0",  # Slide into view
            "width": "30%",
            "height": "100%",
            "backgroundColor": "white",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
            "padding": "20px",
            "overflowY": "auto",
            "zIndex": "4",
            "transition": "right 0.3s ease",
        }
    elif triggered_id == "close-info":
        return {
            "position": "fixed",
            "top": "0",
            "right": "-100%",  # Slide out of view
            "width": "30%",
            "height": "100%",
            "backgroundColor": "white",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
            "padding": "20px",
            "overflowY": "auto",
            "zIndex": "4",
            "transition": "right 0.3s ease",
        }
    return dash.no_update


@app.callback(
    [Output("selected-regions", "data"),
     Output("stored-selected-regions", "data")],  # Reset stored regions after applying
    [Input("visualization-mode", "value"),
     Input("trend-map", "clickData"),
     Input("stored-selected-regions", "data")],  # Listen to stored selected regions
    [State("selected-regions", "data")]
)
def update_selected_regions(mode, trendmap_clickData, stored_regions, selected_regions):
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "visualization-mode":
        # If stored regions exist, apply them and then clear storage
        return (stored_regions if stored_regions else [], [])

    if triggered_id == "trend-map" and trendmap_clickData:
        clicked_region = trendmap_clickData["points"][0]["location"]
        if clicked_region:
            if clicked_region in selected_regions:
                selected_regions.remove(clicked_region)
            elif len(selected_regions) < 3:
                selected_regions.append(clicked_region)

    return selected_regions, dash.no_update  # Keep stored regions unchanged unless visualization mode triggers

@app.callback(
    Output("selected-months", "data"),
    Input("temp-wheel", "clickData"),
    State("selected-months", "data"),
)
def update_selected_months(tempwheel_clickData, selected_months):
    all_months = list(range(1, 13))  # Representing all 12 months

    # Default to all months for yearly average if no selection
    if selected_months is None or not selected_months:
        selected_months = all_months

    if tempwheel_clickData:
        # Handle clicks on the temp-wheel
        clicked_label = tempwheel_clickData["points"][0]["label"]
        month_name = clicked_label.split(":")[0].strip()

        # Map month names to numbers
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5,
            "June": 6, "July": 7, "August": 8, "September": 9, "October": 10,
            "November": 11, "December": 12
        }

        clicked_month = month_map.get(month_name)

        if selected_months == all_months:
            selected_months = [clicked_month]
        else:     
            if clicked_month:
                if clicked_month in selected_months:
                    # Deselect month
                    selected_months.remove(clicked_month)
                else:
                    # Select month
                    selected_months.append(clicked_month)

    # If no months remain selected, return all months (yearly average)
    if not selected_months:
        return all_months

    # Return the currently selected months, sorted
    return sorted(selected_months)

@app.callback(
    Output("temp-wheel", "figure"),
    [Input("parameter-dropdown", "value"),
     Input("parameter-dropdown2", "value"),
     Input("year-slider", "value"),
     Input("selected-months", "data"),
     Input("map-parameter-select", "value")]
)
def update_temp_wheel(parameter, parameter2, selected_years, selected_months, map_parameter):
    selected_year_1, selected_year_2 = sorted(selected_years)

    if map_parameter == "sub":
        data = parameter_grid
        parameter = parameter2
    else:
        data = data_grid
    
    trend_values = []
    for month in range(1, 13):
        monthly_data = data[
            (data["year"].between(selected_year_1, selected_year_2)) &
            (data["month"] == month)
        ]
        if len(monthly_data) > 1:
            slope, _ = np.polyfit(monthly_data["year"], monthly_data[parameter], 1)
            trend_values.append(slope)
        else:
            trend_values.append(0)

    # Fix the min and max symmetrically around zero
    max_abs = max(abs(min(trend_values)), abs(max(trend_values)))
    symmetric_min, symmetric_max = -max_abs, max_abs
    
    # Normalize trend values to the range [0, 1]
    normalized_trends = [
        (value - symmetric_min) / (symmetric_max - symmetric_min)
        if max_abs > 0 else 0.5  # Default to mid if all values are zero
        for value in trend_values
    ]

    if map_parameter == "sub":
        # Dynamically choose colorscale
        colorscale = px.colors.diverging.PiYG
        colors = sample_colorscale(colorscale, normalized_trends)
    else:
        # Dynamically choose colorscale
        colorscale = px.colors.diverging.BrBG if parameter == "acc_precip" else px.colors.diverging.RdBu_r
        colors = sample_colorscale(colorscale, normalized_trends)

    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    labels = [
        f"{month}: {'+' if value > 0 else ''}{value:.2f}"
        for month, value in zip(month_names, trend_values)
    ]

    # Adjust highlight_pull: No pull if all months are selected (yearly average)
    highlight_pull = [
        0 if selected_months == list(range(1, 13)) else (0.1 if i + 1 in selected_months else 0)
        for i in range(12)
    ]

    temp_wheel = go.Figure(go.Pie(
        labels=labels,
        values=[1] * 12,
        textinfo="label",
        hoverinfo="label",
        textposition="inside",
        insidetextorientation='radial',
        name="Test",
        marker=dict(colors=colors),
        hole=0.4,
        pull=highlight_pull,
        direction="clockwise")
    )

    PARAMETERS = {
        "mean_temp": "Mean Temperature (°C)",
        "acc_precip": "Accumulated Precipitation (mm)",
        "max_temp": "Maximum Temperature (°C)",
        "min_temp": "Minimum Temperature (°C)",
        "mean_wind": "Mean Wind Speed (m/s)",
        "ice_para": "Ice Days",
        "heat_para": "Heating Degree Days",
        "summer_para": "Summer days",
        "extrain_para": "Extreme Rain Days",
        "maxwind_para": "Max. Wind Speed 10 min. (m/s)",
        "brightsun_para": "Bright Sunshine (hr)"
    }

    temp_wheel.update_layout(
        font=dict(family="Segoe UI, sans-serif"),
        margin=dict(t=20, r=20, b=20, l=20),
        showlegend=False,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        annotations=[dict(text=PARAMETERS.get(parameter).replace(" ", "<br>"), x=0.5, y=0.5, font_size=16, showarrow=False, xanchor="center")],
    )
    
    temp_wheel.update_traces(
        marker=dict(
            line=dict(color="black", width=1.5))
    )

    return temp_wheel


@app.callback(
    Output("trend-map", "figure"),
    [Input("visualization-mode", "value"),
     Input("parameter-dropdown", "value"),
     Input("parameter-dropdown2", "value"),
     Input("year-slider", "value"),
     Input("selected-months", "data"),
     Input("selected-regions", "data"),
     Input("map-parameter-select", "value")]
)
def update_trend_map(mode, parameter_main, parameter_sub, selected_years, selected_months, selected_regions, map_parameter):
    selected_year_1, selected_year_2 = sorted(selected_years)
    
    # Mapping of parameters to user-friendly names
    PARAMETERS = {
        "mean_temp": "Mean Temperature (°C)",
        "acc_precip": "Accumulated Precipitation (mm)",
        "max_temp": "Maximum Temperature (°C)",
        "min_temp": "Minimum Temperature (°C)",
        "mean_wind": "Mean Wind Speed (m/s)",
        "ice_para": "Ice Days",
        "heat_para": "Heating Degree Days",
        "summer_para": "Summer days",
        "extrain_para": "Extreme Rain Days",
        "maxwind_para": "Max. Wind Speed 10 min. (m/s)",
        "brightsun_para": "Bright Sunshine (hr)"
    }

    if map_parameter == "sub":
        parameter = parameter_sub
        if mode == "grid":
            data = parameter_grid
            geojson_data = geojson_grid_data
            feature_id = "properties.cell_id"
            hover_info = "%{location}"
        else:
            data = parameter_municipality
            geojson_data = geojson_municipality_data
            feature_id = "properties.cell_id"
            hover_info = "%{properties.municipality}"
    
        parameter_name = PARAMETERS.get(parameter, parameter)
        filtered_data = data[data["month"].isin(selected_months)]
    
        trend_data = []
        for cell_id in filtered_data["cell_id"].unique():
            cell_data = filtered_data[filtered_data["cell_id"] == cell_id]
            yearly_data = cell_data[cell_data["year"].between(selected_year_1, selected_year_2)]
    
            aggregated = yearly_data.groupby("year", as_index=False)[parameter].sum() 
            if len(aggregated) > 1:
                slope, _ = np.polyfit(aggregated["year"], aggregated[parameter], 1)
            else:
                slope = None
            trend_data.append({"cell_id": cell_id, "trend": slope})
    
        trend_df = pd.DataFrame(trend_data)
        trend_df["trend"] = trend_df["trend"].fillna(0)
        symmetric_max = max(abs(trend_df["trend"].min()), abs(trend_df["trend"].max()))
        if parameter == "maxwind_para":
            trend_unit = "m/s per year"
        elif parameter == "brightsun_para":
            trend_unit = "hours/year"
        else:
            trend_unit = "days/year"
    
        # Initialize the figure
        trend_map = go.Figure(go.Choroplethmap(
            geojson=geojson_data,
            featureidkey=feature_id,
            locations=trend_df["cell_id"],
            z=trend_df["trend"],
            colorscale="PiYG",
            zmin=-symmetric_max,
            zmax=symmetric_max,
            marker_opacity=0.8,
            marker_line_width=0.5,
            marker_line_color="black",  # Border color for the map
            hovertemplate=(f"Location: {hover_info}<br>"
                           f"Change: %{{z:.5f}} {trend_unit}<br>"
                           # f"Year Range: {selected_year_1}-{selected_year_2}<br>"
                           "<extra></extra>")
        ))
    
        # Add custom colors for the selected regions, in order
        if selected_regions:
            for idx, region in enumerate(selected_regions):
                region_data = trend_df[trend_df["cell_id"] == region]
                # Assign the color based on its position in the selected_regions list
                region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]  # Cycle through colors
    
                trend_map.add_trace(go.Choroplethmap(
                    geojson=geojson_data,
                    featureidkey=feature_id,
                    locations=region_data["cell_id"],
                    z=[1] * len(region_data),  # Arbitrary z-values for highlighting
                    colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
                    showscale=False,
                    marker_opacity=1,
                    marker_line_width=3,  # Border thickness
                    marker_line_color=region_color,  # Apply the color to the border
                    hoverinfo="skip"
                ))
    
        # Define region names for the x-axis title
        if len(selected_months) == 12:
            map_title = f"Yearly change in {parameter_name} from {selected_year_1} to {selected_year_2}"
        else:
            map_title = f"Yearly change in {parameter_name} from {selected_year_1} to {selected_year_2} for selected month(s)"
    
        # Update map layout
        trend_map.update_layout(
            font=dict(family="Segoe UI, sans-serif"),
            map=dict(
                style="carto-positron",
                center={"lon": 11.5, "lat": 56.25},
                zoom=5.9
            ),
            annotations=[
            dict(
                x=0.5,  # Centered horizontally
                y=-0.025,  # Move the title below the map
                xanchor="center",  # Center anchor horizontally
                yanchor="top",  # Anchor it to the top
                text=map_title,  # Title text
                showarrow=False,  # No arrow
                font=dict(size=14, color="black")  # Font size and color
                )
            ],
            margin=dict(t=20, b=50, l=10)
        )
    
        return trend_map
    
    else:
        parameter = parameter_main
        if mode == "grid":
            data = data_grid
            geojson_data = geojson_grid_data
            feature_id = "properties.cell_id"
            hover_info = "%{location}"
        else:
            data = data_municipality
            geojson_data = geojson_municipality_data
            feature_id = "properties.cell_id"
            hover_info = "%{properties.municipality}"
    
        parameter_name = PARAMETERS.get(parameter, parameter)
        filtered_data = data[data["month"].isin(selected_months)]
    
        trend_data = []
        for cell_id in filtered_data["cell_id"].unique():
            cell_data = filtered_data[filtered_data["cell_id"] == cell_id]
            yearly_data = cell_data[cell_data["year"].between(selected_year_1, selected_year_2)]
    
            if len(yearly_data) > 1:
                slope, _ = np.polyfit(yearly_data["year"], yearly_data[parameter], 1)
            else:
                slope = None
            trend_data.append({"cell_id": cell_id, "trend": slope})
    
        trend_df = pd.DataFrame(trend_data)
        trend_df["trend"] = trend_df["trend"].fillna(0)
        symmetric_max = max(abs(trend_df["trend"].min()), abs(trend_df["trend"].max()))    
    
        if parameter == "acc_precip":
            trend_unit = "mm/year"
        elif parameter == "mean_wind":
            trend_unit = "m/s per year"
        else:
            trend_unit = "°C/year"
    
        # Initialize the figure
        trend_map = go.Figure(go.Choroplethmap(
            geojson=geojson_data,
            featureidkey=feature_id,
            locations=trend_df["cell_id"],
            z=trend_df["trend"],
            colorscale="BrBG" if parameter == "acc_precip" else "RdBu_r",
            zmin=-symmetric_max,
            zmax=symmetric_max,
            marker_opacity=0.8,
            marker_line_width=0.5,
            marker_line_color="black",  # Border color for the map
            hovertemplate=(f"Location: {hover_info}<br>"
                           f"Change: %{{z:.5f}} {trend_unit}<br>"
                           # f"Year Range: {selected_year_1}-{selected_year_2}<br>"
                           "<extra></extra>")
        ))
    
        # Add custom colors for the selected regions, in order
        if selected_regions:
            for idx, region in enumerate(selected_regions):
                region_data = trend_df[trend_df["cell_id"] == region]
                # Assign the color based on its position in the selected_regions list
                region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]  # Cycle through colors
    
                trend_map.add_trace(go.Choroplethmap(
                    geojson=geojson_data,
                    featureidkey=feature_id,
                    locations=region_data["cell_id"],
                    z=[1] * len(region_data),  # Arbitrary z-values for highlighting
                    colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
                    showscale=False,
                    marker_opacity=1,
                    marker_line_width=3,  # Border thickness
                    marker_line_color=region_color,  # Apply the color to the border
                    hoverinfo="skip"
                ))
    
        # Define region names for the x-axis title
        if len(selected_months) == 12:
            map_title = f"Yearly change in {parameter_name} from {selected_year_1} to {selected_year_2}"
        else:
            map_title = f"Yearly change in {parameter_name} from {selected_year_1} to {selected_year_2} for selected month(s)"
    
        # Update map layout
        trend_map.update_layout(
            font=dict(family="Segoe UI, sans-serif"),
            map=dict(
                style="carto-positron",
                center={"lon": 11.5, "lat": 56.25},
                zoom=5.9
            ),
            annotations=[
            dict(
                x=0.5,  # Centered horizontally
                y=-0.025,  # Move the title below the map
                xanchor="center",  # Center anchor horizontally
                yanchor="top",  # Anchor it to the top
                text=map_title,  # Title text
                showarrow=False,  # No arrow
                font=dict(size=14, color="black")  # Font size and color
                )
            ],
            margin=dict(t=20, b=50, l=10)
        )
    
        return trend_map

@app.callback(
    Output("timeline", "figure"),
    [Input("parameter-dropdown", "value"),
     Input("selected-months", "data"),
     Input("selected-regions", "data"),
     Input("visualization-mode", "value"),
     Input("trendline-toggle", "value"),
     Input("selected_year", "data"),
     #Input("relative-values-toggle", "data")
     ]
)
def update_timeline(parameter, selected_months, selected_regions, mode, trendline_toggle, selected_year):
    # Set a top margin to move the chart a bit up (and remove an overall title)
    layout_margins = dict(t=50)
    
    # Define parameters for the bar charts
    # Mapping for display names and units
    PARAMETERS = {
        "mean_temp": "Mean Temperature (°C)",
        "acc_precip": "Accumulated Precipitation (mm)",
        "max_temp": "Maximum Temperature (°C)",
        "min_temp": "Minimum Temperature (°C)",
        "mean_wind": "Mean Wind Speed (m/s)"
    }
    parameter_name = PARAMETERS.get(parameter, parameter)
    
    # If Denmark / Region POV
    if len(selected_regions) <= 1:
        if len(selected_regions) == 0:
            # Save data (mode)            
            filtered_data = data_grid[
                (data_grid["year"].between(2011, 2024))
            ]
            
        else:            
            # Save data (mode)
            if mode == "grid":
                filtered_data = data_grid[
                    (data_grid["cell_id"].isin(selected_regions)) &
                    (data_grid["year"].between(2011, 2024))
                ]
            else:
                filtered_data = data_municipality[
                    (data_municipality["cell_id"].isin(selected_regions)) &
                    (data_municipality["year"].between(2011, 2024))
                ]
        
        benchmark_data = filtered_data.groupby("month")[list(PARAMETERS.keys())].mean().reset_index()
        
        # Save data (distribution)
        if selected_year == None:
            filtered_data = filtered_data[(filtered_data["month"].isin(selected_months))]
            yearly_data = filtered_data.groupby("year")[list(PARAMETERS.keys())].mean().reset_index()
            line_data = yearly_data
            line_dis = "year"
        else:
            filtered_data = filtered_data[filtered_data["year"] == selected_year]
            monthly_data = filtered_data.groupby("month")[list(PARAMETERS.keys())].mean().reset_index()
            line_data = monthly_data
            line_dis = "month"
              
        # min_value = filtered_data[parameter].min()
        # max_value = filtered_data[parameter].max()
    
        # min_value_precip = filtered_data["acc_precip"].min()
        # max_value_precip = filtered_data["acc_precip"].max()
           
        # Create figure layout
        fig = go.Figure()

        # Create lines and bar      
        fig.add_trace(go.Scatter(
            x=line_data[line_dis],
            y=line_data["max_temp"],
            mode="lines+markers",
            name="Max. Temp.",
            line=dict(color="firebrick", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Parameter: Max Temp<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=line_data[line_dis],
            y=line_data["mean_temp"],
            mode="lines+markers",
            name="Mean Temp.",
            line=dict(color="orange", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Parameter: Mean Temp<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=line_data[line_dis],
            y=line_data["min_temp"],
            mode="lines+markers",
            name="Min. Temp.",
            line=dict(color="darkblue", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Parameter: Min Temp<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=line_data[line_dis],
            y=line_data["mean_wind"],
            mode="lines+markers",
            name="Mean Wind Speed",
            line=dict(color="palevioletred", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Parameter: Mean Wind<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            x=line_data[line_dis],
            y=line_data["acc_precip"],
            name="Acc. Precipitation",
            marker_color="lightblue",
            opacity=0.6,
            yaxis="y2",
            hovertemplate="Value: %{y:.2f} mm<br>Parameter: Acc. Precip.<extra></extra>"
        ))
        
        if trendline_toggle and selected_year == None:
            x = line_data[line_dis]

            # Create trendlines 
            # Max temp
            y = line_data["max_temp"]
            slope, intercept = np.polyfit(x, y, 1)
            trend_y = slope * x + intercept
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=trend_y,
                mode="lines",
                name="Trend Max. Temp.",
                line=dict(color="firebrick", dash= "dot", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Max Temp<extra></extra>"
            ))
            # Mean temp
            y = line_data["mean_temp"]
            slope, intercept = np.polyfit(x, y, 1)
            trend_y = slope * x + intercept
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=trend_y,
                mode="lines",
                name="Trend Mean Temp.",
                line=dict(color="orange", dash= "dot", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Mean Temp<extra></extra>"
            ))
            # Min temp
            y = line_data["min_temp"]
            slope, intercept = np.polyfit(x, y, 1)
            trend_y = slope * x + intercept
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=trend_y,
                mode="lines",
                name="Trend Min. Temp.",
                line=dict(color="darkblue", dash= "dot", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Min Temp<extra></extra>"
            ))
            # Mean Wind
            y = line_data["mean_wind"]
            slope, intercept = np.polyfit(x, y, 1)
            trend_y = slope * x + intercept
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=trend_y,
                mode="lines",
                name="Trend Mean Wind",
                line=dict(color="palevioletred", dash= "dot", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Mean Wind<extra></extra>"
            ))
            # Acc Precip
            y = line_data["acc_precip"]
            slope, intercept = np.polyfit(x, y, 1)
            trend_y = slope * x + intercept
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=trend_y,
                mode="lines",
                name="Trend Acc. Precip.",
                line=dict(color="teal", dash= "dot", width=3),
                yaxis="y2",
                hovertemplate="Value: %{y:.2f} mm<br>Parameter: Acc. Precip.<extra></extra>"
            ))
        if selected_year is not None:
            # Create lines and bar      
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=benchmark_data["max_temp"],
                mode="lines",
                name="Avg. Max. Temp.",
                line=dict(color="firebrick", dash="dash", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Max Temp<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=benchmark_data["mean_temp"],
                mode="lines",
                name="Avg. Mean Temp.",
                line=dict(color="orange", dash="dash", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Mean Temp<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=benchmark_data["min_temp"],
                mode="lines",
                name="Avg. Min. Temp.",
                line=dict(color="darkblue", dash="dash", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Min Temp<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=benchmark_data["mean_wind"],
                mode="lines",
                name="Avg. Mean Wind Speed",
                line=dict(color="palevioletred", dash="dash", width=3),
                yaxis="y1",
                hovertemplate="Value: %{y:.2f} °C<br>Parameter: Mean Wind<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=benchmark_data["acc_precip"],
                mode="lines",
                name="Avg. Acc. Precip.",
                line=dict(color="teal", dash="dash", width=3),
                # mode="markers",
                # name="Acc. Precipitation",
                # marker=dict(
                #     symbol="line-ew",  # Short horizontal line marker
                #     color="red",
                #     size=15,  # Adjust width of the line
                #     line=dict(width=3, color = "teal")  # Thickness of marker
                # ),
                # opacity=0.6,
                yaxis="y2",
                hovertemplate="Value: %{y:.2f} mm<br>Parameter: Acc. Precip.<extra></extra>"
            ))
        
        # Update layout
        fig.update_layout(
            font=dict(family="Segoe UI, sans-serif", size = 14),
            yaxis=dict(
                title="Temperature (°C)",
                side="left",
                gridcolor="lightgrey",
                range=[-20,30],
                #range=([min_value-1, max_value+1] if "use" in use_relatives else None),
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="lightgrey",
                dtick=5
            ),
            yaxis2=dict(
                title="Accumulated Precipitation (mm)",
                overlaying="y",
                side="right",
                range=[0,150],
                #range=([min_value_precip-5, max_value_precip+5] if "use" in use_relatives else None),
                showgrid=False,
                dtick=15
            ),
            barmode="group",
            legend=dict(
                x=0,  # Center the legend horizontally
                y=-0.15,  # Place the legend below the chart
                orientation="h",  # Horizontal layout
                xanchor="left",  # Align the legend center horizontally
                yanchor="top"  # Anchor the legend at the top
            ),
            dragmode = False,
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        
    else:
        # Filter Denmark data for the full 2011-2024 period (using selected months)
        filtered_data = data_grid[
            (data_grid["year"].between(2011, 2024))]
        
        benchmark_data = filtered_data.groupby("month")[parameter].mean().reset_index()
        
        # Save data (distribution)
        if selected_year == None:
            filtered_data = filtered_data[(filtered_data["month"].isin(selected_months))]
            yearly_data = filtered_data.groupby("year")[parameter].mean().reset_index()
            line_data = yearly_data
            line_dis = "year"
        else:
            filtered_data = filtered_data[filtered_data["year"] == selected_year]
            monthly_data = filtered_data.groupby("month")[parameter].mean().reset_index()
            line_data = monthly_data
            line_dis = "month"
        
        trend_unit = "mm" if parameter == "acc_precip" else "°C"
        
        fig = go.Figure()
        
        # Add Denmark's actual data trace
        fig.add_trace(go.Scatter(
            x=line_data[line_dis],
            y=line_data[parameter],
            mode="lines+markers",
            name="Denmark",
            line=dict(color=DK_COLOR, width=3),
            hovertemplate=(
                "Location: Denmark<br>Value: %{y:.2f} " + trend_unit +
                "<br>Year: %{x}<extra></extra>"
            ),
            legendgroup="Denmark",  # Assign a group
        ))
        
        # Determine if trendlines are toggled on
        show_trendlines = 'show' in trendline_toggle
        # If regions are selected, hide trendline legends
        trendline_show_legend = False if selected_regions else True
        
        # Add Denmark full-range trendline (always in forestgreen with dash "dot")
        if show_trendlines:
            if selected_year == None:
                full_year_range = pd.Series(range(2011, 2025))
                trend_slope, trend_intercept = np.polyfit(
                    line_data["year"], line_data[parameter], 1
                )
                trendline_values = trend_slope * full_year_range + trend_intercept
                fig.add_trace(go.Scatter(
                    x=full_year_range,
                    y=trendline_values,
                    mode="lines",
                    name="Trendline in Denmark (2011-2024)",
                    line=dict(color=DK_COLOR, width=2, dash="dot"),
                    hoverinfo="skip",
                    showlegend=trendline_show_legend,
                    legendgroup="Denmark",  # Assign a group
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=line_data[line_dis],
                    y=benchmark_data[parameter],
                    mode="lines",
                    name="Avg. Denmark",
                    line=dict(color=DK_COLOR, dash="dash", width=2),
                    hoverinfo="skip",
                    showlegend=trendline_show_legend,
                    legendgroup="Denmark",  # Assign a group
                ))
        
        
        combined_filtered_data = pd.concat([
            data_grid[data_grid["cell_id"].isin(selected_regions)],
            data_municipality[data_municipality["cell_id"].isin(selected_regions)]
        ])
        
        def get_region_name(region_id):
            if mode == "municipality":
                feature = next((f for f in geojson_municipality_data["features"]
                                if f["properties"]["cell_id"] == region_id), None)
                return feature["properties"]["municipality"] if feature else f"{region_id}"
            return f"{region_id}"
        
        for idx, region in enumerate(selected_regions):
            region_data = combined_filtered_data[combined_filtered_data["cell_id"] == region]
            benchmark_data = region_data.groupby("month")[parameter].mean().reset_index()
            
            # Save data (distribution) v2
            if selected_year == None:
                region_data = region_data[(region_data["month"].isin(selected_months))]
                yearly_data = region_data.groupby("year")[parameter].mean().reset_index()
                line_data = yearly_data
                line_dis = "year"
            else:
                region_data = region_data[region_data["year"] == selected_year]
                monthly_data = region_data.groupby("month")[parameter].mean().reset_index()
                line_data = monthly_data
                line_dis = "month"
                
            region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
            region_name = get_region_name(region)
            
            fig.add_trace(go.Scatter(
                x=line_data[line_dis],
                y=line_data[parameter],
                mode="lines+markers",
                name=region_name,
                line=dict(width=2, color=region_color),
                marker=dict(size=8),
                hovertemplate=(
                    "Location: " + region_name +
                    "<br>Value: %{y:.2f} " + trend_unit +
                    "<br>Year: %{x}<extra></extra>"
                ),
                legendgroup=region_name,  # Link the region and its trendline
            ))
            
            # Add region trendline if toggled on (with no legend)
            if show_trendlines:
                if selected_year == None:
                    reg_slope, reg_intercept = np.polyfit(
                        line_data["year"], line_data[parameter], 1
                    )
                    reg_trendline_values = reg_slope * line_data["year"] + reg_intercept
                    fig.add_trace(go.Scatter(
                        x=line_data["year"],
                        y=reg_trendline_values,
                        mode="lines",
                        name=f"{region_name} Trend",
                        line=dict(width=2, dash="dot", color=region_color),
                        hoverinfo="skip",
                        showlegend=False,
                        legendgroup=region_name,  # Link the region and its trendline
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=line_data[line_dis],
                        y=benchmark_data[parameter],
                        mode="lines",
                        name=f"Avg. {region_name}",
                        line=dict(color=region_color, dash="dash", width=2),
                        hoverinfo="skip",
                        showlegend=False,
                        legendgroup=region_name,  # Assign a group
                    ))
        
        # Update layout as before
        fig.update_layout(
            font=dict(family="Segoe UI, sans-serif", size = 14),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                #title=parameter_name if len(selected_months) == 12 else f"Average {parameter_name} for selected month(s)",
                tickmode="linear",
                dtick=1,
                fixedrange=True,
                gridcolor="lightgrey",
                showgrid=False
            ),
            yaxis=dict(
                title=PARAMETERS.get(parameter, parameter),
                fixedrange=True,
                gridcolor="lightgrey",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="lightgrey"
            ),
            margin={"r": 40, "t": 40, "l": 40, "b": 20},
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                x=0,
                y=-0.2,
                xanchor="left",
                yanchor="bottom"
            ),
            dragmode=False
        )
    if selected_year is None:
        # Force every year to show from 2011 to 2024
        fig.update_xaxes(
            tickmode='array',
            tickvals=list(range(2011, 2025)),
            ticktext=[str(year) for year in range(2011, 2025)]
        )
    else:
        # Replace month numbers with abbreviations
        fig.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        )
    return fig
# @app.callback(
#     Output("overview-chart", "figure"),
#     [Input("visualization-mode", "value"),
#      Input("selected-regions", "data"),
#      Input("parameter-dropdown", "value")]
# )
# def update_monthly_trend_graph(mode, selected_regions, parameter):
#     # Case 1: No regions selected
#     if not selected_regions:
#         # Use defined climate normals (1981–2010) and Denmark data (2011–2024)
#         data_denmark_2011_2024 = data_grid[(data_grid["year"] >= 2011) & (data_grid["year"] <= 2024)]

#         # Aggregate Denmark data for 2011–2024
#         monthly_stats_denmark = data_denmark_2011_2024.groupby("month").agg({
#             "mean_temp": "mean",
#             "acc_precip": "mean",
#             "max_temp": "mean",
#             "min_temp": "mean"
#         }).reset_index()

#         # Month names for x-axis
#         month_map = {
#             1: "January", 2: "February", 3: "March", 4: "April",
#             5: "May", 6: "June", 7: "July", 8: "August",
#             9: "September", 10: "October", 11: "November", 12: "December"
#         }
#         monthly_stats_denmark["month_name"] = monthly_stats_denmark["month"].map(month_map)

#         # Define x-axis title
#         x_axis_title = "Denmark Monthly Averages (1981–2010 vs. 2011–2024)"
        
#         # Climate normals data
#         climate_normals = pd.DataFrame({
#             "month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
#             "mean_max_temp": [3.1, 3.2, 5.8, 10.6, 15.3, 18.1, 20.9, 20.8, 16.7, 12.1, 7.3, 4.1],
#             "mean_temp": [1.1, 1.0, 2.9, 6.7, 11.2, 14.1, 16.6, 16.5, 13.1, 9.2, 5.1, 2.1],
#             "mean_min_temp": [-1.3, -1.4, 0.0, 3.0, 7.0, 10.1, 12.5, 12.5, 9.6, 6.2, 2.6, -0.4],
#             "mean_acc_precip": [65, 48, 52, 37, 49, 62, 63, 76, 74, 85, 70, 67]
#         })
        
#         # Create the figure
#         fig = go.Figure()

#         # Climate normals data
#         fig.add_trace(go.Scatter(
#             x=climate_normals["month"],
#             y=climate_normals["mean_max_temp"],
#             mode="lines+markers",
#             name="Max. Temp. (1981–2010)",
#             line=dict(color="firebrick", dash="dash", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 1981-2010<br>Parameter: Max Temp<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=climate_normals["month"],
#             y=climate_normals["mean_temp"],
#             mode="lines+markers",
#             name="Mean Temp. (1981–2010)",
#             line=dict(color="orange", dash="dash", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 1981-2010<br>Parameter: Mean Temp<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=climate_normals["month"],
#             y=climate_normals["mean_min_temp"],
#             mode="lines+markers",
#             name="Min. Temp. (1981–2010)",
#             line=dict(color="darkblue", dash="dash", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 1981-2010<br>Parameter: Min Temp<extra></extra>"
#         ))
#         fig.add_trace(go.Bar(
#             x=climate_normals["month"],
#             y=climate_normals["mean_acc_precip"],
#             name="Acc. Precipitation (1981–2010)",
#             marker_color="lightblue",
#             opacity=0.6,
#             yaxis="y2",
#             hovertemplate="Value: %{y:.2f} mm<br>Period: 1981-2010<br>Parameter: Acc. Precip.<extra></extra>"
#         ))

#         # Denmark 2011–2024 data
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_denmark["month_name"],
#             y=monthly_stats_denmark["max_temp"],
#             mode="lines+markers",
#             name="Max. Temp. (2011–2024)",
#             line=dict(color="firebrick", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2024<br>Parameter: Max. Temp<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_denmark["month_name"],
#             y=monthly_stats_denmark["mean_temp"],
#             mode="lines+markers",
#             name="Mean Temp. (2011–2024)",
#             line=dict(color="orange", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2024<br>Parameter: Mean Temp<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_denmark["month_name"],
#             y=monthly_stats_denmark["min_temp"],
#             mode="lines+markers",
#             name="Min. Temp. (2011–2024)",
#             line=dict(color="darkblue", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2024<br>Parameter: Min. Temp<extra></extra>"
#         ))
#         fig.add_trace(go.Bar(
#             x=monthly_stats_denmark["month_name"],
#             y=monthly_stats_denmark["acc_precip"],
#             name="Acc. Precipitation (2011–2024)",
#             marker_color="teal",
#             opacity=0.4,
#             yaxis="y2",
#             hovertemplate="Value: %{y:.2f} mm <br>Period: 2011-2024<br>Parameter: Acc. Precip.<extra></extra>"
#         ))
#     else:
#         # Case 2: Regions selected
#         data = data_grid if mode == "grid" else data_municipality
#         filtered_data = data[data["cell_id"].isin(selected_regions)]

#         # Split data into two periods
#         data_2011_2017 = filtered_data[(filtered_data["year"] >= 2011) & (filtered_data["year"] <= 2017)]
#         data_2018_2024 = filtered_data[(filtered_data["year"] >= 2018) & (filtered_data["year"] <= 2024)]

#         # Aggregate data for each period
#         monthly_stats_2011_2017 = data_2011_2017.groupby("month").agg({
#             "mean_temp": "mean",
#             "acc_precip": "mean",
#             "max_temp": "mean",
#             "min_temp": "mean"
#         }).reset_index()
#         monthly_stats_2018_2024 = data_2018_2024.groupby("month").agg({
#             "mean_temp": "mean",
#             "acc_precip": "mean",
#             "max_temp": "mean",
#             "min_temp": "mean"
#         }).reset_index()

#         # Month names for x-axis
#         month_map = {
#             1: "January", 2: "February", 3: "March", 4: "April",
#             5: "May", 6: "June", 7: "July", 8: "August",
#             9: "September", 10: "October", 11: "November", 12: "December"
#         }
#         monthly_stats_2011_2017["month_name"] = monthly_stats_2011_2017["month"].map(month_map)
#         monthly_stats_2018_2024["month_name"] = monthly_stats_2018_2024["month"].map(month_map)

#         # Define x-axis title
#         region_names = [
#             next(
#                 (f["properties"]["municipality"] for f in geojson_municipality_data["features"] if f["properties"]["cell_id"] == region),
#                 f"{region}"
#             )
#             for region in selected_regions
#         ]
#         x_axis_title = f"Monthly average across regions: {', '.join(region_names)}"

#         # Create the figure
#         fig = go.Figure()

#         # 2011–2017 data
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_2011_2017["month_name"],
#             y=monthly_stats_2011_2017["max_temp"],
#             mode="lines+markers",
#             name="Max. Temp. (2011–2017)",
#             line=dict(color="firebrick", dash="dash", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2017<br>Parameter: Max. Temp.<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_2011_2017["month_name"],
#             y=monthly_stats_2011_2017["mean_temp"],
#             mode="lines+markers",
#             name="Mean Temp. (2011–2017)",
#             line=dict(color="orange", dash="dash", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 2011-2017<br>Parameter: Mean Temp.<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_2011_2017["month_name"],
#             y=monthly_stats_2011_2017["min_temp"],
#             mode="lines+markers",
#             name="Min. Temp. (2011–2017)",
#             line=dict(color="darkblue", dash="dash", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 2011-2017<br>Parameter: Min. Temp.<extra></extra>"
#         ))
#         fig.add_trace(go.Bar(
#             x=monthly_stats_2011_2017["month_name"],
#             y=monthly_stats_2011_2017["acc_precip"],
#             name="Acc. Precipitation (2011–2017)",
#             marker_color="lightblue",
#             opacity=0.4,
#             yaxis="y2",
#             hovertemplate="Value: %{y:.2f} mm<br>Period: 2011-2017<br>Parameter: Acc. Precip.<extra></extra>"
#         ))

#         # 2018–2024 data
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_2018_2024["month_name"],
#             y=monthly_stats_2018_2024["max_temp"],
#             mode="lines+markers",
#             name="Max. Temp. (2018-2024)",
#             line=dict(color="firebrick", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 2018-2024<br>Parameter: Max. Temp.<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_2018_2024["month_name"],
#             y=monthly_stats_2018_2024["mean_temp"],
#             mode="lines+markers",
#             name="Mean Temp. (2018-2024)",
#             line=dict(color="orange", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 2018-2024<br>Parameter: Mean Temp.<extra></extra>"
#         ))
#         fig.add_trace(go.Scatter(
#             x=monthly_stats_2018_2024["month_name"],
#             y=monthly_stats_2018_2024["min_temp"],
#             mode="lines+markers",
#             name="Min. Temp. (2018-2024)",
#             line=dict(color="darkblue", width=3),
#             yaxis="y1",
#             hovertemplate="Value: %{y:.2f} °C<br>Period: 2018-2024<br>Parameter: Min. Temp.<extra></extra>"
#         ))
#         fig.add_trace(go.Bar(
#             x=monthly_stats_2018_2024["month_name"],
#             y=monthly_stats_2018_2024["acc_precip"],
#             name="Acc. Precipitation (2018-2024)",
#             marker_color="teal",
#             opacity=0.4,
#             yaxis="y2",
#             hovertemplate="Value: %{y:.2f} mm<br>Period: 2018-2024<br>Parameter: Acc. Precip.<extra></extra>"
#         ))

#     # Update layout
#     fig.update_layout(
#         font=dict(family="Segoe UI, sans-serif", size = 14),
#         xaxis=dict(title=x_axis_title),
#         yaxis=dict(
#             title="Temperature (°C)",
#             side="left",
#             gridcolor="lightgrey",
#             range=[-15,35],
#             zeroline=True,
#             zerolinewidth=2,
#             zerolinecolor="lightgrey",
#             dtick=5
#         ),
#         yaxis2=dict(
#             title="Accumulated Precipitation (mm)",
#             overlaying="y",
#             side="right",
#             range=[0,150],
#             showgrid=False,
#             dtick=15
#         ),
#         barmode="group",
#         legend=dict(
#             x=0,  # Center the legend horizontally
#             y=-0.15,  # Place the legend below the chart
#             orientation="h",  # Horizontal layout
#             xanchor="left",  # Align the legend center horizontally
#             yanchor="top"  # Anchor the legend at the top
#         ),
#         dragmode = False,
#         margin=dict(l=40, r=40, t=40, b=40),
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#     )

#     return fig
@app.callback(
    Output("bar_chart", "figure"),
    [Input("selected-months", "data"),
     Input("parameter-dropdown2", "value"),
     Input("selected-regions", "data"),
     Input("visualization-mode", "value"),
     Input("selected_year", "data"),
     Input("barchart-toggle", "value")]
)
def update_bar_chart(selected_months, selected_parameter, selected_regions, mode, selected_year, barchart_toggle):
    layout_margins = dict(t=50)
    
    # Define parameter labels
    PARAMETERS = {
        "ice_para": "Ice Days",
        "heat_para": "Heating Degree Days",
        "summer_para": "Summer Days",
        "extrain_para": "Extreme Rain Days",
        "maxwind_para": "Max. Wind Speed 10 min.",
        "brightsun_para": "Bright Sunshine Hours"
    }
    
    # Helper function for aggregation.
    # average_over_grids == True: for DK (national-level), where we average over grids.
    # average_over_grids == False: for a specific region (sum/average over its data).
    def aggregate_param(df, p, selected_year, selected_months, average_over_grids):
        if selected_year is None:
            # Yearly view: filter to selected months.
            df = df[df["month"].isin(selected_months)]
            # First, compute grid-level aggregation per year.
            if p == "maxwind_para":
                # For max wind: compute grid means (over selected months)
                grid_vals = df.groupby(["year", "cell_id"])[p].mean().reset_index()
            else:
                # For day counts: sum the days for the selected months per grid.
                grid_vals = df.groupby(["year", "cell_id"])[p].sum().reset_index()
            if average_over_grids:
                # For DK: average across grids.
                agg_df = grid_vals.groupby("year")[p].mean().reset_index()
            else:
                # For a single region: if more than one grid exists, sum them.
                agg_df = grid_vals.groupby("year")[p].sum().reset_index()
            x_col = "year"
        else:
            # Monthly view: filter to the selected year(s)
            if isinstance(selected_year, list):
                df = df[df["year"].isin(selected_year)]
            else:
                df = df[df["year"] == selected_year]
            if p == "maxwind_para":
                grid_vals = df.groupby(["month", "cell_id"])[p].mean().reset_index()
            else:
                grid_vals = df.groupby(["month", "cell_id"])[p].sum().reset_index()
            if average_over_grids:
                agg_df = grid_vals.groupby("month")[p].mean().reset_index()
            else:
                agg_df = grid_vals.groupby("month")[p].sum().reset_index()
            x_col = "month"
        return agg_df, x_col
    
    # ------------------------------------------------------------------
    # CASE 1: Single Region or DK (i.e. if len(selected_regions) <= 1)
    if len(selected_regions) <= 1:
        if len(selected_regions) == 0:
            # No region selected -> DK national-level: average across grids.
            selected_region = "Denmark"
            df_data = parameter_grid[parameter_grid["year"].between(2011, 2024)]
            region_color = DK_COLOR
            avg_over_grids = True
            # For monthly view, compute benchmark data: average of each parameter by month.
            if selected_year is not None:
                temp = df_data.groupby(["cell_id", "month"])[list(PARAMETERS.keys())].sum().reset_index()
                temp[list(PARAMETERS.keys())] = temp[list(PARAMETERS.keys())] / 14.0
                benchmark_data = temp.groupby("month")[list(PARAMETERS.keys())].mean().reset_index()
        else:
            # A single region is selected.
            selected_region = selected_regions[0]
            if mode == "grid":
                df_data = parameter_grid[(parameter_grid["cell_id"] == selected_region) & 
                                         (parameter_grid["year"].between(2011, 2024))]
            else:
                df_data = parameter_municipality[(parameter_municipality["cell_id"] == selected_region) & 
                                                (parameter_municipality["year"].between(2011, 2024))]
            try:
                idx = selected_regions.index(selected_region)
                region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
            except ValueError:
                region_color = COLOR_PALETTE[0]
            avg_over_grids = False
        
            # For monthly view, compute benchmark data: average of each parameter by month.
            if selected_year is not None:
                benchmark_data = (df_data.groupby("month")[list(PARAMETERS.keys())].sum() / 14).reset_index()
        
        # Create one subplot per parameter.
        n_params = len(PARAMETERS)
        fig = make_subplots(
            rows=n_params, cols=1, shared_xaxes=True,
            subplot_titles=[f"{'Average' if p=='maxwind_para' else 'Aggregate'} {PARAMETERS[p]}" for p in PARAMETERS]
        )
        # Loop over all parameters.
        for i, p in enumerate(PARAMETERS, start=1):
            agg_df, x_col = aggregate_param(df_data, p, selected_year, selected_months, avg_over_grids)
            fig.add_trace(
                go.Bar(
                    x=agg_df[x_col],
                    y=agg_df[p],
                    marker_color=region_color,
                    name=PARAMETERS[p]
                ),
                row=i, col=1
            )
            # Optionally add a trend line in yearly view.
            if barchart_toggle and selected_year is None:
                x_vals = agg_df[x_col]
                y_vals = agg_df[p]
                slope, intercept = np.polyfit(x_vals, y_vals, 1)
                trend_y = slope * np.array(x_vals) + intercept
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=trend_y,
                        mode="lines",
                        line=dict(dash="dot", color="black")
                    ),
                    row=i, col=1
                )
            # Add benchmark markers for monthly view.
            if selected_year is not None:
                fig.add_trace(
                    go.Scatter(
                        x=agg_df[x_col],
                        y=benchmark_data[p],
                        mode="markers",
                        marker=dict(
                            symbol="line-ew",
                            color="black",
                            size=15,
                            line=dict(width=3, color="black")
                        ),
                        name=f"{PARAMETERS[p]} Benchmark",
                        showlegend=True
                    ),
                    row=i, col=1
                )
    
    # ------------------------------------------------------------------
    # CASE 2: Multiple Regions Selected (Parameter POV)
    else:
        # In this case, only the chosen parameter (selected_parameter) is displayed.
        # Build subplot titles: first for DK, then one per region.
        subplot_titles = ["Denmark"]
        for region in selected_regions:
            if mode == "municipality":
                region_str = str(region)
                feature = next(
                    (f for f in geojson_municipality_data["features"] 
                     if str(f["properties"].get("cell_id", "")) == region_str),
                    None
                )
                region_title = feature["properties"].get("municipality", f"Region {region}") if feature else f"Region {region}"
            else:
                region_title = str(region)
            subplot_titles.append(region_title)
        
        n_rows = len(selected_regions) + 1
        fig = make_subplots(
            rows=n_rows, cols=1, shared_xaxes=True,
            subplot_titles=subplot_titles
        )
        # DK national-level bar (average over grids)
        df_dk = parameter_grid[parameter_grid["year"].between(2011, 2024)]
        dk_agg, x_col = aggregate_param(df_dk, selected_parameter, selected_year, selected_months, average_over_grids=True)
        fig.add_trace(
            go.Bar(
                x=dk_agg[x_col],
                y=dk_agg[selected_parameter],
                marker_color=DK_COLOR,
                name="DK"
            ),
            row=1, col=1
        )
        # For monthly view, compute DK benchmark.
        if selected_year is not None:
            temp = df_dk.groupby(["cell_id", "month"])[list(PARAMETERS.keys())].sum().reset_index()
            temp[list(PARAMETERS.keys())] = temp[list(PARAMETERS.keys())] / 14.0
            benchmark_data = temp.groupby("month")[list(PARAMETERS.keys())].mean().reset_index()
            fig.add_trace(
                go.Scatter(
                    x=dk_agg[x_col],
                    y=benchmark_data[selected_parameter],
                    mode="markers",
                    marker=dict(
                        symbol="line-ew",
                        color="black",
                        size=15,
                        line=dict(width=3, color="black")
                    ),
                    name=f"{PARAMETERS[selected_parameter]} Benchmark",
                    showlegend=True
                ),
                row=1, col=1
            )
        if barchart_toggle and selected_year is None:
            x_vals = dk_agg[x_col]
            y_vals = dk_agg[selected_parameter]
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            trend_y = slope * np.array(x_vals) + intercept
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=trend_y,
                    mode="lines",
                    line=dict(dash="dot", color="black")
                ),
                row=1, col=1
            )
        
        # Loop over each selected region.
        for idx, region in enumerate(selected_regions):
            df_region = pd.concat([
                parameter_grid[(parameter_grid["cell_id"] == region) & (parameter_grid["year"].between(2011, 2024))],
                parameter_municipality[(parameter_municipality["cell_id"] == region) & (parameter_municipality["year"].between(2011, 2024))]
            ])
            reg_agg, x_col = aggregate_param(df_region, selected_parameter, selected_year, selected_months, average_over_grids=False)
            region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
            fig.add_trace(
                go.Bar(
                    x=reg_agg[x_col],
                    y=reg_agg[selected_parameter],
                    marker_color=region_color,
                    name=str(region)
                ),
                row=idx+2, col=1
            )
            if barchart_toggle and selected_year is None:
                x_vals = reg_agg[x_col]
                y_vals = reg_agg[selected_parameter]
                slope, intercept = np.polyfit(x_vals, y_vals, 1)
                trend_y = slope * np.array(x_vals) + intercept
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=trend_y,
                        mode="lines",
                        name=str(region),
                        line=dict(dash="dot", color="black")
                    ),
                    row=idx+2, col=1
                )
            if selected_year is not None:
                # Compute benchmark for this region.
                benchmark_reg = (df_region.groupby("month")[selected_parameter].sum() / 14).reset_index()
                fig.add_trace(
                    go.Scatter(
                        x=reg_agg[x_col],
                        y=benchmark_reg[selected_parameter],
                        mode="markers",
                        marker=dict(
                            symbol="line-ew",
                            color="black",
                            size=15,
                            line=dict(width=3, color="black")
                        ),
                        name=f"{PARAMETERS[selected_parameter]} Benchmark",
                        showlegend=True
                    ),
                    row=idx+2, col=1
                )
        
        # Compute a global y-axis maximum for all subplots (including DK) and apply uniformly.
        global_max = 0
        for trace in fig.data:
            if trace.type == 'bar':
                trace_max = max(trace.y)
                if trace_max > global_max:
                    global_max = trace_max
        global_max *= 1.1
        for row in range(1, n_rows+1):
            fig.update_yaxes(range=[0, global_max], row=row, col=1)
    
    # Update x-axis ticks depending on whether we're showing years or months.
    if selected_year is None:
        fig.update_xaxes(
            tickmode='array',
            tickvals=list(range(2011, 2025)),
            ticktext=[str(year) for year in range(2011, 2025)]
        )
    else:
        fig.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        )
    
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif"),
        showlegend=False,
        margin=layout_margins,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    fig.update_yaxes(rangemode="nonnegative")
    
    return fig


@app.callback(
    Output("dynamic-label-barchart", "children"),
    [Input("parameter-dropdown2", "value"),
     Input("selected-regions", "data"),
     Input("selected_year", "data"),
     Input("visualization-mode", "value")]
)
def update_label(selected_parameter, selected_regions, selected_year, mode):
    
    # Save useful name for regions
    for region in selected_regions:
        if mode == "municipality":
            region_str = str(region)
            feature = next(
                (f for f in geojson_municipality_data["features"] 
                 if str(f["properties"].get("cell_id", "")) == region_str),
                None
            )
            region_name = feature["properties"].get("municipality", f"Region {region}") if feature else f"Region {region}"
        else:
            region_name = str(region)
    
    # Save useful name for parameters
    # Define parameters for the bar charts
    parameters = {
        "ice_para": "Ice Days",
        "heat_para": "Heating Degree Days",
        "summer_para": "Summer Days",
        "extrain_para": "Extreme Rain Days",
        "maxwind_para": "Max. Wind Speed 10 min.",
        "brightsun_para": "Bright Sunshine"
    }
    
    selected_parameter_name = parameters.get(selected_parameter)
    
    # Create text
    distribution_text = "Yearly" if selected_year == None else "Monthly"
    parameter_text = "all parameters" if len(selected_regions) <= 1 else f"{selected_parameter_name}"
    region_text = ("in Denmark" if len(selected_regions) == 0 else f"in {region_name}" if len(selected_regions) == 1 else "")
    year_text = "" if selected_year == None else f"for {selected_year}"

    return f"{distribution_text} distribution of {parameter_text} {region_text} {year_text}"

@app.callback(
    Output("dynamic-label-timeline", "children"),
    [Input("parameter-dropdown", "value"),
     Input("selected-regions", "data"),
     Input("selected_year", "data"),
     Input("visualization-mode", "value")]
)
def update_label2(selected_parameter, selected_regions, selected_year, mode):
    
    # Save useful name for regions
    for region in selected_regions:
        if mode == "municipality":
            region_str = str(region)
            feature = next(
                (f for f in geojson_municipality_data["features"] 
                 if str(f["properties"].get("cell_id", "")) == region_str),
                None
            )
            region_name = feature["properties"].get("municipality", f"Region {region}") if feature else f"Region {region}"
        else:
            region_name = str(region)
    
    # Save useful name for parameters
    # Define parameters for the bar charts
    parameters = {
        "mean_temp": "Mean Temperature (°C)",
        "acc_precip": "Accumulated Precipitation (mm)",
        "max_temp": "Maximum Temperature (°C)",
        "min_temp": "Minimum Temperature (°C)",
        "mean_wind": "Mean Wind Speed (m/s)",
    }
    
    selected_parameter_name = parameters.get(selected_parameter)
    
    # Create text
    distribution_text = "Yearly" if selected_year == None else "Monthly"
    parameter_text = "all parameters" if len(selected_regions) <= 1 else f"{selected_parameter_name}"
    region_text = ("in Denmark" if len(selected_regions) == 0 else f"in {region_name}" if len(selected_regions) == 1 else "")
    year_text = "" if selected_year == None else f"for {selected_year}"

    return f"{distribution_text} distribution of {parameter_text} {region_text} {year_text}"


@app.callback(
    Output("selected_year", "data"),
    [Input("bar_chart", "clickData"),
     Input("reset-zoom", "n_clicks")],
    State("selected_year", "data")
)
def update_selected_year(clickData, reset_n, selected_year):
    ctx = callback_context
    if not ctx.triggered:
        return selected_year
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "reset-zoom":
        return None  # Reset the zoom to the yearly view
    if clickData:
        # If no year is currently selected, store the clicked bar's x-value (assumed to be a year)
        if selected_year is None:
            return clickData["points"][0]["x"]
    return selected_year



#### USE CASES ####
preset_data = {
    "usecase-garden-filter-button": {
        "months": [2, 3, 4, 5],
        "parameter": "min_temp",
        "subparameter": "ice_para",
        "mode": "municipality",
        "regions": ["0253"]
    },
    "usecase-energy-filter-button": {
        "months": [9, 10, 11, 12],
        "parameter": "min_temp",
        "subparameter": "heat_para",
        "mode": "grid",
        "regions": ["10km_622_56"]
    },
    "usecase-farmer-filter-button": {
        "months": [5, 6, 7, 8],
        "parameter": "acc_precip",
        "subparameter": "extrain_para",
        "mode": "municipality",
        "regions": ["0580", "0550"]
    },
    "usecase-summerhouse-filter-button": {
        "months": [6, 7, 8],
        "parameter": "mean_temp",
        "subparameter": "summer_para",
        "mode": "municipality",
        "regions": ["0813", "0376", "0400"]
    }
}

@app.callback(
    [Output("selected-months", "data", allow_duplicate=True),
     Output("parameter-dropdown", "value", allow_duplicate=True),
     Output("parameter-dropdown2", "value", allow_duplicate=True),
     Output("visualization-mode", "value", allow_duplicate=True),
     Output("stored-selected-regions", "data", allow_duplicate=True)],
    [Input(button_id, "n_clicks") for button_id in preset_data.keys()],
    prevent_initial_call=True
)
def apply_preset(*args):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Identify which button was clicked
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Fetch the corresponding preset data
    if triggered_id in preset_data:
        preset = preset_data[triggered_id]
        return preset["months"], preset["parameter"], preset["subparameter"], preset["mode"], preset["regions"]

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


# Extract IDs from use_cases_data dynamically
usecase_ids = [case["id"] for case in use_cases_data]

@app.callback(
    [Output(f"{usecase_id}-sheet", "style") for usecase_id in usecase_ids],
    sum([[Input(f"{usecase_id}-button", "n_clicks"), Input(f"{usecase_id}-close", "n_clicks")] for usecase_id in usecase_ids], []),
    prevent_initial_call=True
)
def toggle_usecase_sheets(*args):
    ctx = callback_context
    if not ctx.triggered:
        return [dash.no_update] * len(usecase_ids)

    # Identify which button was clicked
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Generate a default hidden state for all sheets
    hidden_state = {
        "position": "fixed",
        "top": "-100%",  # Hide above the screen
        "left": "50%",
        "transform": "translateX(-50%)",
        "width": "50%",
        "backgroundColor": "white",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
        "padding": "20px",
        "zIndex": "5",
        "transition": "top 0.3s ease"
    }

    # Generate an open state (shown) for the triggered sheet
    open_state = hidden_state.copy()
    open_state["top"] = "0"  # Drop down from the top

    # Determine which sheet to show/hide
    output_states = []
    for usecase_id in usecase_ids:
        if triggered_id == f"{usecase_id}-button":
            output_states.append(open_state)  # Show this sheet
        else:
            output_states.append(hidden_state)  # Hide all others

    return output_states

if __name__ == "__main__":
    # app.run_server(debug=True, port=5050)
    app.run_server(debug=False, port=80, host='0.0.0.0')