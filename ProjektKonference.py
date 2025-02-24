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

import dash_daq as daq
from use_cases import use_cases, use_cases_data
from info_sheet import info_sheet

from numpy import RankWarning
import warnings
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
                        style={"fontSize": "18px", "margin": "0px"}
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
                                        "Main Parameter:",
                                        style={"fontSize": "18px", "fontWeight": "bold", "margin": "0px"}
                                    ),
                                    dcc.RadioItems(
                                        id="parameter-dropdown",
                                        options=[
                                            {"label": "Max. Temp.", "value": "max_temp"},
                                            {"label": "Mean Temp.", "value": "mean_temp"},
                                            {"label": "Min. Temp.", "value": "min_temp"},
                                            {"label": "Acc. Precip.", "value": "acc_precip"}
                                        ],
                                        value="mean_temp",
                                        labelStyle={'display': 'block', 'fontSize': '18px', 'marginTop': "5px"}
                                    )
                                ],
                                style={"flex": "1", "margin": "10px"}
                            ),
                            # Toggle switch container
                            html.Div(
                                children=[
                                    # The toggle switch
                                    daq.BooleanSwitch(
                                        id="map-parameter-toggle",
                                        on=False,  # Set default state here
                                        color="purple",
                                        style={"verticalAlign": "middle"}
                                    ),
                                    # Label that will update based on the toggle state
                                    html.Div(
                                        id="map-parameter-toggle-label",
                                        children="Show main parameters on map",
                                        style={"fontSize": "16px", "fontWeight": "bold", "marginRight": "10px"}
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "center"}
                            ),
                            # Right side: New subparameter selection with four buttons
                            html.Div(
                                children=[
                                    html.Label(
                                        "Sub-Parameter:",
                                        style={"fontSize": "18px", "fontWeight": "bold", "margin": "0px"}
                                    ),
                                    dcc.RadioItems(
                                        id="parameter-dropdown2",
                                        options=[
                                            {"label": "Ice Days", "value": "ice_para"},
                                            {"label": "Heat. Deg. Days", "value": "heat_para"},
                                            {"label": "Summer Days", "value": "summer_para"},
                                            {"label": "Extreme Rain Days", "value": "extrain_para"}
                                        ],
                                        value="heat_para",
                                        labelStyle={'display': 'block', 'fontSize': '18px', 'marginTop': "5px"}
                                    )
                                ],
                                style={"flex": "1", "margin": "10px", "display": "flex", "flexDirection": "column"}
                            )
                        ],
                        className="parameters-wrapper"
                    ),
                    html.Label(
                        "To select regions, click on map ↓ ", 
                        style={"fontSize": "18px", "font-style": "italic", "margin": "0px"}
                    ),
                    html.Div(
                        children=[
                            # Reset Filters button (unchanged)
                            html.A(
                                html.Button(
                                    id="reset-button",
                                    style={
                                        "width": "150px",
                                        "height": "35px",
                                        "backgroundColor": "rgba(220, 220, 220, 1)",
                                        "border": "2px solid rgba(220, 220, 220, 1)",
                                        "borderRadius": "14px",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "gap": "10px",
                                        "cursor": "pointer",
                                        "padding": "6px"
                                    },
                                    n_clicks=0,
                                    title="Reset filters",
                                    children=[
                                        html.Img(
                                            src="/assets/reset.png",
                                            style={"width": "25px", "height": "25px"}
                                        ),
                                        html.Span(
                                            "Reset Filters",
                                            style={
                                                "fontFamily": "Segoe UI, sans-serif",
                                                "color": "black",
                                                "fontSize": "16px",
                                                "fontWeight": "bold"
                                            }
                                        )
                                    ]
                                ),
                                href="/",
                                style={"textDecoration": "none", "margin": "10px 6px"}
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center"}
                    )
                ], className="menu"),
                html.Button("Reset Zoom", id="reset-zoom", n_clicks=0),
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
                html.Div(
                    dcc.Checklist(
                        id="trendline-toggle",
                        options=[{"label": "Show Trendlines", "value": "show"}],
                        value=["show"],
                        labelStyle={"fontSize": "16px", "fontWeight": "bold"}
                    ),
                    style={
                        "position": "absolute",
                        "top": "5px",
                        "right": "5px",
                        "backgroundColor": "rgba(255,255,255,0.7)",
                        "padding": "5px",
                        "borderRadius": "5px",
                        "zIndex": "3"
                    }
                )
            ], className="lineChartWrapper"),
            html.Div([
            ], className="timeSlideWrapper"),
            html.Div([
                dcc.Graph(
                    id="bar_chart",
                    style={"width": "105%", "height": "100%"},
                    config={"displayModeBar": False},
                ),
                html.Label(
                    id="dynamic-label",
                    style={
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "margin": "0px",
                        "marginRight": "10px",
                        "position": "absolute",
                        "top": "5px",
                        "left": "5px"
                    }
                ),
                dcc.Checklist(
                    id="barchart-toggle",
                    options=[{"label": "Show Trendlines", "value": "show"}],
                    value=["show"],
                    labelStyle={"fontSize": "16px", "fontWeight": "bold"},
                    style={"position": "absolute", "top": "5px", "right": "5px"}
                ),
            ], className="barChartWrapper"),
        ]
        , className="rightColumn"),
    ],
    className="main"
)

# Colors for municipalities
COLOR_PALETTE = ["gold", "coral", "mediumpurple"]

@app.callback(
    Output("map-parameter-toggle-label", "children"),
    Input("map-parameter-toggle", "on")
)
def update_toggle_label(is_on):
    return "Display sub-parameters" if is_on else "Display main parameters"

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
     Input("map-parameter-toggle", "on")]
)
def update_temp_wheel(parameter, parameter2, selected_years, selected_months, toggle_state):
    selected_year_1, selected_year_2 = sorted(selected_years)
    
    if toggle_state:
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

    if toggle_state:
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
        marker=dict(colors=colors),
        hole=0.4,
        pull=highlight_pull,
        direction="clockwise")
    )

    temp_wheel.update_layout(
        font=dict(family="Segoe UI, sans-serif"),
        margin=dict(t=20, r=20, b=20, l=20),
        showlegend=False,
        paper_bgcolor="rgba(0, 0, 0, 0)"
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
     Input("map-parameter-toggle", "on")]
)
def update_trend_map(mode, parameter_main, parameter_sub, selected_years, selected_months, selected_regions, toggle_state):
    selected_year_1, selected_year_2 = sorted(selected_years)
    
    # Mapping of parameters to user-friendly names
    PARAMETERS = {
        "mean_temp": "Mean Temperature (°C)",
        "acc_precip": "Accumulated Precipitation (mm)",
        "max_temp": "Maximum Temperature (°C)",
        "min_temp": "Minimum Temperature (°C)",
        "ice_para": "Ice Days",
        "heat_para": "Heating Degree Days",
        "summer_para": "Summer days",
        "extrain_para": "Extreme Rain Days"
    }

    if toggle_state:
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
     Input("year-slider", "value"),
     Input("selected-months", "data"),
     Input("selected-regions", "data"),
     Input("visualization-mode", "value"),
     Input("trendline-toggle", "value")]
)
def update_timeline(parameter, selected_years, selected_months, selected_regions, visualization_mode, trendline_toggle):
    selected_year_1, selected_year_2 = sorted(selected_years)
    
    # Mapping for display names and units
    PARAMETER_LABELS = {
        "mean_temp": "Mean Temperature (°C)",
        "acc_precip": "Accumulated Precipitation (mm)",
        "max_temp": "Maximum Temperature (°C)",
        "min_temp": "Minimum Temperature (°C)"
    }
    parameter_name = PARAMETER_LABELS.get(parameter, parameter)
    min_value = data_grid[parameter].min()
    max_value = data_grid[parameter].max()
    
    # Filter Denmark data for the full 2011-2024 period (using selected months)
    denmark_filtered_data = data_grid[
        (data_grid["year"].between(2011, 2024)) &
        (data_grid["month"].isin(selected_months))
    ]
    trend_unit = "mm" if parameter == "acc_precip" else "°C"
    denmark_average_data = denmark_filtered_data.groupby("year")[parameter].mean().reset_index()
    
    timeline = go.Figure()
    
    min_value_precip = denmark_filtered_data["acc_precip"].min()
    max_value_precip = denmark_filtered_data["acc_precip"].max()
    
    # Add Denmark's actual data trace
    timeline.add_trace(go.Scatter(
        x=denmark_average_data["year"],
        y=denmark_average_data[parameter],
        mode="lines+markers",
        name="Denmark",
        line=dict(color="forestgreen"),
        marker=dict(size=8),
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
        full_year_range = pd.Series(range(2011, 2025))
        trend_slope, trend_intercept = np.polyfit(
            denmark_average_data["year"], denmark_average_data[parameter], 1
        )
        trendline_values = trend_slope * full_year_range + trend_intercept
        timeline.add_trace(go.Scatter(
            x=full_year_range,
            y=trendline_values,
            mode="lines",
            name="Trendline in Denmark (2011-2024)",
            line=dict(color="forestgreen", width=2, dash="dot"),
            hoverinfo="skip",
            showlegend=trendline_show_legend,
            legendgroup="Denmark",  # Assign a group
        ))
        
        # Add local trendline only if no regions are selected and the selected year range is different from the full range
        if not selected_regions and (selected_years != [2011, 2024] and len(selected_years) == 2):
            filtered_data = denmark_average_data[
                denmark_average_data["year"].between(selected_year_1, selected_year_2)
            ]
            if len(filtered_data) > 1:
                local_slope, local_intercept = np.polyfit(
                    filtered_data["year"], filtered_data[parameter], 1
                )
                local_trendline_values = local_slope * filtered_data["year"] + local_intercept
                local_trendline_color = "blue" if local_slope < 0 else "red"
                timeline.add_trace(go.Scatter(
                    x=filtered_data["year"],
                    y=local_trendline_values,
                    mode="lines",
                    name=f"Trendline in Denmark ({selected_year_1}-{selected_year_2})",
                    line=dict(color=local_trendline_color, width=2, dash="dot"),
                    hoverinfo="skip",
                    showlegend=trendline_show_legend
                ))
    
    # If regions are selected, add their data and (if toggled) their trendlines
    if selected_regions:
        combined_filtered_data = pd.concat([
            data_grid[data_grid["cell_id"].isin(selected_regions)],
            data_municipality[data_municipality["cell_id"].isin(selected_regions)]
        ])
        regions_filtered_data = combined_filtered_data[
            (combined_filtered_data["month"].isin(selected_months)) &
            (combined_filtered_data["year"].between(2011, 2024))
        ]
        
        def get_region_name(region_id):
            if visualization_mode == "municipality":
                feature = next((f for f in geojson_municipality_data["features"]
                                if f["properties"]["cell_id"] == region_id), None)
                return feature["properties"]["municipality"] if feature else f"{region_id}"
            return f"{region_id}"
        
        for idx, region in enumerate(selected_regions):
            region_data = regions_filtered_data[regions_filtered_data["cell_id"] == region]
            if not region_data.empty:
                region_timeline = region_data.groupby("year")[parameter].mean().reset_index()
                region_name = get_region_name(region)
                region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
                timeline.add_trace(go.Scatter(
                    x=region_timeline["year"],
                    y=region_timeline[parameter],
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
                if show_trendlines and len(region_timeline["year"]) > 1:
                    reg_slope, reg_intercept = np.polyfit(
                        region_timeline["year"], region_timeline[parameter], 1
                    )
                    reg_trendline_values = reg_slope * region_timeline["year"] + reg_intercept
                    timeline.add_trace(go.Scatter(
                        x=region_timeline["year"],
                        y=reg_trendline_values,
                        mode="lines",
                        name=f"{region_name} Trend",
                        line=dict(width=2, dash="dot", color=region_color),
                        hoverinfo="skip",
                        showlegend=False,
                        legendgroup=region_name,  # Link the region and its trendline
                    ))
    
    # Add vertical dashed lines for the selected years (this remains unchanged)
    for year in selected_years:
        timeline.add_shape(
            dict(
                type="line",
                x0=year, x1=year,
                y0=0, y1=1,
                xref="x", yref="paper",
                line=dict(color="grey", dash="dash", width=2)
            )
        )
    
    print(parameter)
    if parameter == "acc_precip": 
        # Update layout as before
        timeline.update_layout(
            font=dict(family="Segoe UI, sans-serif", size = 14),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                title=parameter_name if len(selected_months) == 12 else f"Average {parameter_name} for selected month(s)",
                range=[2010.5, 2024.5],
                tickmode="linear",
                tick0=2011,
                dtick=1,
                fixedrange=True,
                gridcolor="lightgrey",
                showgrid=False
            ),
            yaxis=dict(
                title=PARAMETER_LABELS.get(parameter, parameter),
                range=[min_value_precip-5, max_value_precip+5],
                gridcolor="lightgrey",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="lightgrey"
            ),
            margin={"r": 40, "t": 40, "l": 40, "b": 40},
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
    else: 
        timeline.update_layout(
            font=dict(family="Segoe UI, sans-serif", size = 14),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                title=parameter_name if len(selected_months) == 12 else f"Average {parameter_name} for selected month(s)",
                range=[2010.5, 2024.5],
                tickmode="linear",
                tick0=2011,
                dtick=1,
                fixedrange=True,
                gridcolor="lightgrey",
                showgrid=False
            ),
            yaxis=dict(
                title=PARAMETER_LABELS.get(parameter, parameter),
                range=[min_value-5, max_value+5],
                gridcolor="lightgrey",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="lightgrey"
            ),
            margin={"r": 40, "t": 40, "l": 40, "b": 40},
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
        
    return timeline

@app.callback(
    Output("overview-chart", "figure"),
    [Input("visualization-mode", "value"),
     Input("selected-regions", "data"),
     Input("parameter-dropdown", "value")]
)
def update_monthly_trend_graph(mode, selected_regions, parameter):
    # Case 1: No regions selected
    if not selected_regions:
        # Use defined climate normals (1981–2010) and Denmark data (2011–2024)
        data_denmark_2011_2024 = data_grid[(data_grid["year"] >= 2011) & (data_grid["year"] <= 2024)]

        # Aggregate Denmark data for 2011–2024
        monthly_stats_denmark = data_denmark_2011_2024.groupby("month").agg({
            "mean_temp": "mean",
            "acc_precip": "mean",
            "max_temp": "mean",
            "min_temp": "mean"
        }).reset_index()

        # Month names for x-axis
        month_map = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        monthly_stats_denmark["month_name"] = monthly_stats_denmark["month"].map(month_map)

        # Define x-axis title
        x_axis_title = "Denmark Monthly Averages (1981–2010 vs. 2011–2024)"
        
        # Climate normals data
        climate_normals = pd.DataFrame({
            "month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "mean_max_temp": [3.1, 3.2, 5.8, 10.6, 15.3, 18.1, 20.9, 20.8, 16.7, 12.1, 7.3, 4.1],
            "mean_temp": [1.1, 1.0, 2.9, 6.7, 11.2, 14.1, 16.6, 16.5, 13.1, 9.2, 5.1, 2.1],
            "mean_min_temp": [-1.3, -1.4, 0.0, 3.0, 7.0, 10.1, 12.5, 12.5, 9.6, 6.2, 2.6, -0.4],
            "mean_acc_precip": [65, 48, 52, 37, 49, 62, 63, 76, 74, 85, 70, 67]
        })
        
        # Create the figure
        fig = go.Figure()

        # Climate normals data
        fig.add_trace(go.Scatter(
            x=climate_normals["month"],
            y=climate_normals["mean_max_temp"],
            mode="lines+markers",
            name="Max. Temp. (1981–2010)",
            line=dict(color="firebrick", dash="dash", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 1981-2010<br>Parameter: Max Temp<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=climate_normals["month"],
            y=climate_normals["mean_temp"],
            mode="lines+markers",
            name="Mean Temp. (1981–2010)",
            line=dict(color="orange", dash="dash", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 1981-2010<br>Parameter: Mean Temp<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=climate_normals["month"],
            y=climate_normals["mean_min_temp"],
            mode="lines+markers",
            name="Min. Temp. (1981–2010)",
            line=dict(color="darkblue", dash="dash", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 1981-2010<br>Parameter: Min Temp<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            x=climate_normals["month"],
            y=climate_normals["mean_acc_precip"],
            name="Acc. Precipitation (1981–2010)",
            marker_color="lightblue",
            opacity=0.6,
            yaxis="y2",
            hovertemplate="Value: %{y:.2f} mm<br>Period: 1981-2010<br>Parameter: Acc. Precip.<extra></extra>"
        ))

        # Denmark 2011–2024 data
        fig.add_trace(go.Scatter(
            x=monthly_stats_denmark["month_name"],
            y=monthly_stats_denmark["max_temp"],
            mode="lines+markers",
            name="Max. Temp. (2011–2024)",
            line=dict(color="firebrick", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2024<br>Parameter: Max. Temp<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=monthly_stats_denmark["month_name"],
            y=monthly_stats_denmark["mean_temp"],
            mode="lines+markers",
            name="Mean Temp. (2011–2024)",
            line=dict(color="orange", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2024<br>Parameter: Mean Temp<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=monthly_stats_denmark["month_name"],
            y=monthly_stats_denmark["min_temp"],
            mode="lines+markers",
            name="Min. Temp. (2011–2024)",
            line=dict(color="darkblue", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2024<br>Parameter: Min. Temp<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            x=monthly_stats_denmark["month_name"],
            y=monthly_stats_denmark["acc_precip"],
            name="Acc. Precipitation (2011–2024)",
            marker_color="teal",
            opacity=0.4,
            yaxis="y2",
            hovertemplate="Value: %{y:.2f} mm <br>Period: 2011-2024<br>Parameter: Acc. Precip.<extra></extra>"
        ))
    else:
        # Case 2: Regions selected
        data = data_grid if mode == "grid" else data_municipality
        filtered_data = data[data["cell_id"].isin(selected_regions)]

        # Split data into two periods
        data_2011_2017 = filtered_data[(filtered_data["year"] >= 2011) & (filtered_data["year"] <= 2017)]
        data_2018_2024 = filtered_data[(filtered_data["year"] >= 2018) & (filtered_data["year"] <= 2024)]

        # Aggregate data for each period
        monthly_stats_2011_2017 = data_2011_2017.groupby("month").agg({
            "mean_temp": "mean",
            "acc_precip": "mean",
            "max_temp": "mean",
            "min_temp": "mean"
        }).reset_index()
        monthly_stats_2018_2024 = data_2018_2024.groupby("month").agg({
            "mean_temp": "mean",
            "acc_precip": "mean",
            "max_temp": "mean",
            "min_temp": "mean"
        }).reset_index()

        # Month names for x-axis
        month_map = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        monthly_stats_2011_2017["month_name"] = monthly_stats_2011_2017["month"].map(month_map)
        monthly_stats_2018_2024["month_name"] = monthly_stats_2018_2024["month"].map(month_map)

        # Define x-axis title
        region_names = [
            next(
                (f["properties"]["municipality"] for f in geojson_municipality_data["features"] if f["properties"]["cell_id"] == region),
                f"{region}"
            )
            for region in selected_regions
        ]
        x_axis_title = f"Monthly average across regions: {', '.join(region_names)}"

        # Create the figure
        fig = go.Figure()

        # 2011–2017 data
        fig.add_trace(go.Scatter(
            x=monthly_stats_2011_2017["month_name"],
            y=monthly_stats_2011_2017["max_temp"],
            mode="lines+markers",
            name="Max. Temp. (2011–2017)",
            line=dict(color="firebrick", dash="dash", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C <br>Period: 2011-2017<br>Parameter: Max. Temp.<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=monthly_stats_2011_2017["month_name"],
            y=monthly_stats_2011_2017["mean_temp"],
            mode="lines+markers",
            name="Mean Temp. (2011–2017)",
            line=dict(color="orange", dash="dash", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 2011-2017<br>Parameter: Mean Temp.<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=monthly_stats_2011_2017["month_name"],
            y=monthly_stats_2011_2017["min_temp"],
            mode="lines+markers",
            name="Min. Temp. (2011–2017)",
            line=dict(color="darkblue", dash="dash", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 2011-2017<br>Parameter: Min. Temp.<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            x=monthly_stats_2011_2017["month_name"],
            y=monthly_stats_2011_2017["acc_precip"],
            name="Acc. Precipitation (2011–2017)",
            marker_color="lightblue",
            opacity=0.4,
            yaxis="y2",
            hovertemplate="Value: %{y:.2f} mm<br>Period: 2011-2017<br>Parameter: Acc. Precip.<extra></extra>"
        ))

        # 2018–2024 data
        fig.add_trace(go.Scatter(
            x=monthly_stats_2018_2024["month_name"],
            y=monthly_stats_2018_2024["max_temp"],
            mode="lines+markers",
            name="Max. Temp. (2018-2024)",
            line=dict(color="firebrick", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 2018-2024<br>Parameter: Max. Temp.<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=monthly_stats_2018_2024["month_name"],
            y=monthly_stats_2018_2024["mean_temp"],
            mode="lines+markers",
            name="Mean Temp. (2018-2024)",
            line=dict(color="orange", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 2018-2024<br>Parameter: Mean Temp.<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=monthly_stats_2018_2024["month_name"],
            y=monthly_stats_2018_2024["min_temp"],
            mode="lines+markers",
            name="Min. Temp. (2018-2024)",
            line=dict(color="darkblue", width=3),
            yaxis="y1",
            hovertemplate="Value: %{y:.2f} °C<br>Period: 2018-2024<br>Parameter: Min. Temp.<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            x=monthly_stats_2018_2024["month_name"],
            y=monthly_stats_2018_2024["acc_precip"],
            name="Acc. Precipitation (2018-2024)",
            marker_color="teal",
            opacity=0.4,
            yaxis="y2",
            hovertemplate="Value: %{y:.2f} mm<br>Period: 2018-2024<br>Parameter: Acc. Precip.<extra></extra>"
        ))

    # Update layout
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif", size = 14),
        xaxis=dict(title=x_axis_title),
        yaxis=dict(
            title="Temperature (°C)",
            side="left",
            gridcolor="lightgrey",
            range=[-15,35],
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

    return fig


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
    # Set a top margin to move the chart a bit up (and remove an overall title)
    layout_margins = dict(t=50)
    
    # Define parameters for the bar charts
    PARAMETERS = {
        "ice_para": "Ice Days",
        "heat_para": "Heating Degree Days",
        "summer_para": "Summer Days",
        "extrain_para": "Extreme Rain Days"
    }
    
    # If Denmark / Region POV
    if len(selected_regions) <= 1:
        if len(selected_regions) == 0:
            # Save POV
            selected_region_or_parameter = "Denmark"

            # Save data (mode)            
            filtered_data = parameter_grid[
                (parameter_grid["year"].between(2011, 2024))
            ]
            region_color = "forestgreen"
            
        else:
            # Save POV
            selected_region_or_parameter = selected_regions[0]
            
            # Save data (mode)
            if mode == "grid":
                filtered_data = parameter_grid[
                    (parameter_grid["cell_id"] == selected_region_or_parameter) &
                    (parameter_grid["year"].between(2011, 2024))
                ]
            else:
                filtered_data = parameter_municipality[
                    (parameter_municipality["cell_id"] == selected_region_or_parameter) &
                    (parameter_municipality["year"].between(2011, 2024))
                ]
            try:
                idx = selected_regions.index(selected_region_or_parameter)
                region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
            except ValueError:
                region_color = COLOR_PALETTE[0]
        
        # Save data (distribution)
        if selected_year == None:
            filtered_data = filtered_data[(filtered_data["month"].isin(selected_months))]
            yearly_data = filtered_data.groupby("year")[list(PARAMETERS.keys())].sum().reset_index()
            bar_data = yearly_data
            bar_dis = "year"
        else:
            filtered_data = filtered_data[filtered_data["year"] == selected_year]
            monthly_data = filtered_data.groupby("month")[list(PARAMETERS.keys())].sum().reset_index()
            bar_data = monthly_data
            bar_dis = "month"

        # Save Subtitles
        subplot_titles = [f"Aggregate {label}" for label in PARAMETERS.values()]
                    
        # Create figure layout
        fig = make_subplots(
            rows=4, cols=1, shared_xaxes=True,
            subplot_titles=subplot_titles
        )

        for idx, (param, label) in enumerate(PARAMETERS.items(), start=1):
            fig.add_trace(
                go.Bar(
                    x=bar_data[bar_dis],
                    y=bar_data[param],
                    marker_color=region_color,
                    name=label
                ),
                row=idx, col=1
            )
            if barchart_toggle and selected_year == None:
                x = bar_data[bar_dis]
                y = bar_data[param]
                
                slope, intercept = np.polyfit(x, y, 1)
                trend_y = slope * x + intercept
                
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=trend_y,
                        mode="lines",
                        name=label,
                        line=dict(dash="dot", color="red")
                        ),
                    row=idx, col=1
                    )
        
        
    else: # If parameter POV / more than 1 selected region
        # Save POV
        selected_region_or_parameter = selected_parameter
        
        # Save titles for the subplots
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
        
        ################ ADD DK ################
        # Filter for Denmark (national-level data)
        filtered_data = parameter_grid[
            (parameter_grid["year"].between(2011, 2024))
        ]
  
        # Save data (distribution)
        if selected_year == None:
            filtered_data = filtered_data[(filtered_data["month"].isin(selected_months))]
            yearly_data = filtered_data.groupby("year")[selected_region_or_parameter].sum().reset_index()
            bar_data = yearly_data
            bar_dis = "year"
        else:
            filtered_data = filtered_data[filtered_data["year"] == selected_year]
            monthly_data = filtered_data.groupby("month")[selected_region_or_parameter].sum().reset_index()
            bar_data = monthly_data
            bar_dis = "month"
      
        # Initialize subplots with custom titles
        fig = make_subplots(
            rows=len(selected_regions) + 1, cols=1, shared_xaxes=True,
            subplot_titles=subplot_titles
        )
        
        # Add Denmark's bar chart (color: forestgreen)
        fig.add_trace(
            go.Bar(
                x=bar_data[bar_dis],
                y=bar_data[selected_region_or_parameter],
                marker_color="forestgreen"
            ),
            row=1, col=1
        )
        
        if barchart_toggle and selected_year == None:
            x = bar_data[bar_dis]
            y = bar_data[selected_region_or_parameter]
            
            slope, intercept = np.polyfit(x, y, 1)
            trend_y = slope * x + intercept
            
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=trend_y,
                    mode="lines",
                    line=dict(dash="dot", color="red")
                    ),
                row=1, col=1
                )
        
        ################ ADD REGIONS ################
        # Add selected region data with colors from COLOR_PALETTE
        combined_filtered_data = pd.concat([
            parameter_grid[parameter_grid["cell_id"].isin(selected_regions)],
            parameter_municipality[parameter_municipality["cell_id"].isin(selected_regions)]
        ])
        
        # Save data (distribution) v1
        regions_filtered_data = combined_filtered_data[
            (combined_filtered_data["year"].between(2011, 2024))
        ]
        
        for idx, region in enumerate(selected_regions):
            region_data = regions_filtered_data[regions_filtered_data["cell_id"] == region]
            if not region_data.empty:
                # Save data (distribution) v2
                if selected_year == None:
                    region_data = region_data[(region_data["month"].isin(selected_months))]
                    yearly_data = region_data.groupby("year")[selected_region_or_parameter].sum().reset_index()
                    bar_data = yearly_data
                    bar_dis = "year"
                else:
                    region_data = region_data[region_data["year"] == selected_year]
                    monthly_data = region_data.groupby("month")[selected_region_or_parameter].sum().reset_index()
                    bar_data = monthly_data
                    bar_dis = "month"
                
                region_color = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
                
                # (The trace's name is still used for the legend; it doesn't affect the subplot title)
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
        
                fig.add_trace(
                    go.Bar(
                        x=bar_data[bar_dis],
                        y=bar_data[selected_region_or_parameter],
                        marker_color=region_color,
                        name=region_name  # This controls the legend, not the subplot title.
                    ),
                    row=idx+2, col=1
                )
                if barchart_toggle and selected_year == None:
                    x = bar_data[bar_dis]
                    y = bar_data[selected_region_or_parameter]
                    
                    slope, intercept = np.polyfit(x, y, 1)
                    trend_y = slope * x + intercept
                    
                    fig.add_trace(
                        go.Scatter(
                            x=x,
                            y=trend_y,
                            mode="lines",
                            name=region_name,
                            line=dict(dash="dot", color="red")
                            ),
                        row=idx+2, col=1
                        )
        # Compute a global maximum for all region bar traces, excluding Denmark's bar (assumed to be the first bar)
        global_max = 0
        first_bar_found = False
        for trace in fig.data:
            if trace.type == 'bar':
                if not first_bar_found:
                    # Skip Denmark's bar
                    first_bar_found = True
                    continue
                trace_max = max(trace.y)
                if trace_max > global_max:
                    global_max = trace_max
        
        # Optionally add a margin
        global_max *= 1.1
        
        # Set the same y-axis limit for all subplots (including Denmark's, to compare)
        num_rows = len(selected_regions) + 1  # 1 for Denmark plus one per region
        for row in range(2, num_rows + 1):
            fig.update_yaxes(range=[0, global_max], row=row, col=1)

        
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
    Output("dynamic-label", "children"),
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
        "extrain_para": "Extreme Rain Days"
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
    app.run_server(debug=True, port=80, host='0.0.0.0')  