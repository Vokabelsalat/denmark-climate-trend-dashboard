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

import warnings
warnings.simplefilter('ignore', np.exceptions.RankWarning)

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
    children=[
        html.Div([ 
            # Container for the text and info button
            html.Div(
                style={
                    "position": "absolute",
                    "top": "15px",
                    "right": "15px",
                    "display": "flex",  # Use flexbox to align text and button side by side
                    "alignItems": "center",  # Vertically center align the text and button
                },
                children=[
                    # use case button
                    # New Use Case button
                    html.Button(
                        id="usecase-button-summerhouse",
                        style={
                            "width": "165px",
                            "height": "45px",
                            "backgroundColor": "rgba(213, 227, 211)",
                            "border": "2px solid rgba(191, 227, 186)",
                            "borderRadius": "18px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "left",
                            "gap": "14px",
                            "cursor": "pointer",
                            "transition": "all 0.1s ease",
                            "padding": "10px",
                            "marginLeft": "10px",
                            "marginRight": "10px"
                        },
                        n_clicks=0,
                        title="Click for Information on Summerhouse Use Case",
                        children=[
                            html.Img(src="/assets/summerhouse_icon.webp", style={"width": "25px", "height": "25px"}),
                            html.Span("Summerhouse", style={
                                "fontFamily": "Times New Roman, Times, serif",
                                "color": "black",
                                "fontSize": "17px",
                                "fontWeight": "bold"
                            })
                        ]
                    ),
                    # Use Case info sheet (drops down from the top and centered)
                    html.Div(
                        id="usecase-sheet-summerhouse",
                        style={
                            "position": "fixed",
                            "top": "-100%",  # Initially hidden above the screen
                            "left": "50%",
                            "transform": "translateX(-50%)",
                            "width": "50%",
                            "backgroundColor": "white",
                            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
                            "padding": "20px",
                            "zIndex": "5",
                            "transition": "top 0.3s ease"
                        },
                        children=[
                            html.Button("Close", id="close-usecase-summerhouse", style={
                                "position": "absolute",
                                "top": "10px",
                                "right": "10px",
                                "backgroundColor": "#FF0000",
                                "color": "white",
                                "border": "none",
                                "padding": "10px",
                                "borderRadius": "5px",
                                "cursor": "pointer"
                            }),
                            html.H2("Use Case: A Family Looking for a Summerhouse", style={
                                "fontSize": "32px",
                                "fontWeight": "bold",
                                "color": "#333333",
                                "marginBottom": "5px",
                                "textAlign": "center"
                            }),
                            html.P("A family looking for a summerhouse along the Danish coast will want to know how warm and pleasant the summers have been in different regions. This view highlights June through August in Frederikshavn, Guldborgsund, and Bornholm, showing both average temperatures and the number of summer days. The data can help identify which locations have the most stable and inviting summer climate, making it easier to choose the perfect spot for a summer retreat.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("Results: Across Denmark, average summer temperatures have been rising, indicating that summers are becoming warmer. The number of summer days (above X°C) has increased, making the climate more attractive for vacationing. Among the selected locations, Bornholm stands out with the highest increase in warm summer days as well as the warmest mean temperature, making it a particularly appealing destination for those seeking consistent, warm summer weather.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.Button("Apply filters", id="summerhouse-button", n_clicks=0,
                                        style={
                                            "width": "110px",  # Adjust width to accommodate text
                                            "height": "45px",
                                            "backgroundColor": "rgba(226, 182, 247, 0.8)",  # Light purple background
                                            "border": "2px solid rgba(206, 159, 229, 0.8)",  # Slightly darker purple border
                                            "borderRadius": "18px",  # Rounded corners
                                            "display": "flex",  # Flexbox for alignment
                                            "alignItems": "center",  # Center content vertically
                                            "justifyContent": "left",  # Center content horizontally
                                            "gap": "14px",  # Space between symbol and text
                                            "cursor": "pointer",
                                            "transition": "all 0.1s ease",  # Smooth transition for hover effect
                                            "padding": "10px",  # Add padding for better spacing
                                            "margin-right": "10px",  # Space between buttons
                                            },
                                        )
                        ]
                    ),
                    
                    # New Use Case (farmer) button
                    html.Button(
                        id="usecase-button-farmer",
                        style={
                            "width": "165px",
                            "height": "45px",
                            "backgroundColor": "rgba(213, 227, 211)",
                            "border": "2px solid rgba(191, 227, 186)",
                            "borderRadius": "18px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "left",
                            "gap": "14px",
                            "cursor": "pointer",
                            "transition": "all 0.1s ease",
                            "padding": "10px",
                            "marginLeft": "10px",
                            "marginRight": "10px"
                        },
                        n_clicks=0,
                        title="Click for information on Farmer Use Case",
                        children=[
                            html.Img(src="/assets/Farmer_icon.webp", style={"width": "25px", "height": "25px"}),
                            html.Span("Farmer", style={
                                "fontFamily": "Times New Roman, Times, serif",
                                "color": "black",
                                "fontSize": "17px",
                                "fontWeight": "bold"
                            })
                        ]
                    ),
                    # Use Case info sheet (drops down from the top and centered)
                    html.Div(
                        id="usecase-sheet-farmer",
                        style={
                            "position": "fixed",
                            "top": "-100%",  # Initially hidden above the screen
                            "left": "50%",
                            "transform": "translateX(-50%)",
                            "width": "50%",
                            "backgroundColor": "white",
                            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
                            "padding": "20px",
                            "zIndex": "5",
                            "transition": "top 0.3s ease"
                        },
                        children=[
                            html.Button("Close", id="close-usecase-farmer", style={
                                "position": "absolute",
                                "top": "10px",
                                "right": "10px",
                                "backgroundColor": "#FF0000",
                                "color": "white",
                                "border": "none",
                                "padding": "10px",
                                "borderRadius": "5px",
                                "cursor": "pointer"
                            }),
                            html.H2("Use Case: A Farmer in Aabenraa and Tønder", style={
                                "fontSize": "32px",
                                "fontWeight": "bold",
                                "color": "#333333",
                                "marginBottom": "5px",
                                "textAlign": "center"
                            }),
                            html.P("A farmer located in Aabenraa or Tønder needs to keep a close eye on rainfall patterns during the growing season. This view focuses on May through August, showing both total precipitation and the number of extreme rain days. Reviewing the trends can help determine whether heavy rainfall events are becoming more frequent, which might require better drainage solutions or adjustments to irrigation planning.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("Results: The data reveals a rapid decline in total precipitation for Aabenraa and Tønder compared to the rest of Denmark. Additionally, the number of extreme rain days (above 10mm) has decreased, which could indicate that farmers may need to rely more on irrigation systems to maintain optimal soil moisture. This suggests a notable shift towards drier growing seasons, potentially impacting crop yields and requiring changes in water management strategies.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.Button("Apply filters", id="farmer-button", n_clicks=0,
                                        style={
                                            "width": "110px",  # Adjust width to accommodate text
                                            "height": "45px",
                                            "backgroundColor": "rgba(226, 182, 247, 0.8)",  # Light purple background
                                            "border": "2px solid rgba(206, 159, 229, 0.8)",  # Slightly darker purple border
                                            "borderRadius": "18px",  # Rounded corners
                                            "display": "flex",  # Flexbox for alignment
                                            "alignItems": "center",  # Center content vertically
                                            "justifyContent": "left",  # Center content horizontally
                                            "gap": "14px",  # Space between symbol and text
                                            "cursor": "pointer",
                                            "transition": "all 0.1s ease",  # Smooth transition for hover effect
                                            "padding": "10px",  # Add padding for better spacing
                                            "margin-right": "10px",  # Space between buttons
                                            },
                                        )
                        ]
                    ),
                    
                    # New Use Case (garden) button
                    html.Button(
                        id="usecase-button-garden",
                        style={
                            "width": "165px",
                            "height": "45px",
                            "backgroundColor": "rgba(213, 227, 211)",
                            "border": "2px solid rgba(191, 227, 186)",
                            "borderRadius": "18px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "left",
                            "gap": "14px",
                            "cursor": "pointer",
                            "transition": "all 0.1s ease",
                            "padding": "10px",
                            "marginLeft": "10px",
                            "marginRight": "10px"
                        },
                        n_clicks=0,
                        title="Click for information on Garden Use Case",
                        children=[
                            html.Img(src="/assets/flower_icon.webp", style={"width": "25px", "height": "25px"}),
                            html.Span("Garden", style={
                                "fontFamily": "Times New Roman, Times, serif",
                                "color": "black",
                                "fontSize": "17px",
                                "fontWeight": "bold"
                            })
                        ]
                    ),
                    # Use Case info sheet (drops down from the top and centered)
                    html.Div(
                        id="usecase-sheet-garden",
                        style={
                            "position": "fixed",
                            "top": "-100%",  # Initially hidden above the screen
                            "left": "50%",
                            "transform": "translateX(-50%)",
                            "width": "50%",
                            "backgroundColor": "white",
                            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
                            "padding": "20px",
                            "zIndex": "5",
                            "transition": "top 0.3s ease"
                        },
                        children=[
                            html.Button("Close", id="close-usecase-garden", style={
                                "position": "absolute",
                                "top": "10px",
                                "right": "10px",
                                "backgroundColor": "#FF0000",
                                "color": "white",
                                "border": "none",
                                "padding": "10px",
                                "borderRadius": "5px",
                                "cursor": "pointer"
                            }),
                            html.H2("Use Case: A Gardener in Greve", style={
                                "fontSize": "32px",
                                "fontWeight": "bold",
                                "color": "#333333",
                                "marginBottom": "5px",
                                "textAlign": "center"
                            }),
                            html.P("A gardener in Greve planning for the upcoming season needs to know when frost risks fade and planting conditions improve. This view tracks February through May, focusing on minimum temperatures and ice days. Looking at these trends can help determine whether spring is arriving earlier, allowing for an extended planting season, or if late frosts remain a concern that could impact garden planning.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("Results: The data shows that minimum temperatures in early spring have been steadily increasing, indicating a clear warming trend. At the same time, the number of ice days has decreased, suggesting that planting can now begin earlier than in previous years without significant frost risk. In particular, Greve’s frost risk in March and April has been lower compared to past years, making it possible for gardeners to extend their growing season and plant more sensitive species earlier in the year.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.Button("Apply filters", id="garden-button", n_clicks=0,
                                        style={
                                            "width": "110px",  # Adjust width to accommodate text
                                            "height": "45px",
                                            "backgroundColor": "rgba(226, 182, 247, 0.8)",  # Light purple background
                                            "border": "2px solid rgba(206, 159, 229, 0.8)",  # Slightly darker purple border
                                            "borderRadius": "18px",  # Rounded corners
                                            "display": "flex",  # Flexbox for alignment
                                            "alignItems": "center",  # Center content vertically
                                            "justifyContent": "left",  # Center content horizontally
                                            "gap": "14px",  # Space between symbol and text
                                            "cursor": "pointer",
                                            "transition": "all 0.1s ease",  # Smooth transition for hover effect
                                            "padding": "10px",  # Add padding for better spacing
                                            "margin-right": "10px",  # Space between buttons
                                            },
                                        )
                        ]
                    ),
                    
                    # New Use Case (energy) button
                    html.Button(
                        id="usecase-button-energy",
                        style={
                            "width": "165px",
                            "height": "45px",
                            "backgroundColor": "rgba(213, 227, 211)",
                            "border": "2px solid rgba(191, 227, 186)",
                            "borderRadius": "18px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "left",
                            "gap": "14px",
                            "cursor": "pointer",
                            "transition": "all 0.1s ease",
                            "padding": "10px",
                            "marginLeft": "10px",
                            "marginRight": "50px"
                        },
                        n_clicks=0,
                        title="Click for information on Energy Use Case",
                        children=[
                            html.Img(src="/assets/energy_icon.jpg", style={"width": "25px", "height": "25px"}),
                            html.Span("Energy", style={
                                "fontFamily": "Times New Roman, Times, serif",
                                "color": "black",
                                "fontSize": "17px",
                                "fontWeight": "bold"
                            })
                        ]
                    ),
                    # Use Case info sheet (drops down from the top and centered)
                    html.Div(
                        id="usecase-sheet-energy",
                        style={
                            "position": "fixed",
                            "top": "-100%",  # Initially hidden above the screen
                            "left": "50%",
                            "transform": "translateX(-50%)",
                            "width": "50%",
                            "backgroundColor": "white",
                            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
                            "padding": "20px",
                            "zIndex": "5",
                            "transition": "top 0.3s ease"
                        },
                        children=[
                            html.Button("Close", id="close-usecase-energy", style={
                                "position": "absolute",
                                "top": "10px",
                                "right": "10px",
                                "backgroundColor": "#FF0000",
                                "color": "white",
                                "border": "none",
                                "padding": "10px",
                                "borderRadius": "5px",
                                "cursor": "pointer"
                            }),
                            html.H2("Use Case: An Energy Efficiency Planner in Aarhus", style={
                                "fontSize": "32px",
                                "fontWeight": "bold",
                                "color": "#333333",
                                "marginBottom": "5px",
                                "textAlign": "center"
                            }),
                            html.P("A homeowner or building manager in Aarhus interested in energy efficiency can use this view to assess how autumn temperatures impact heating demand. Covering September through December, it displays minimum temperatures and heating degree days, helping to track whether autumns are becoming milder. Reviewing this data can provide insight into whether heating demand is decreasing over time and whether investments in insulation or energy-saving measures are needed.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.P("Results: The data shows that minimum autumn temperatures have been decreasing, meaning colder nights during the fall season. However, heating degree days have remained stable, suggesting that overall heating demand has not significantly changed. Given this stability, homeowners may not need to make additional investments in insulation, energy-efficient windows, or alternative heating sources at this time, as heating requirements have remained consistent over the years",
                                   style={
                                       "fontSize": "18px",
                                       "color": "#333333",
                                       "marginTop": "10px",
                                       "lineHeight": "1.5",
                                       "textAlign": "left"
                                   }),
                            html.Button("Apply filters", id="energy-button", n_clicks=0,
                                        style={
                                            "width": "110px",  # Adjust width to accommodate text
                                            "height": "45px",
                                            "backgroundColor": "rgba(226, 182, 247, 0.8)",  # Light purple background
                                            "border": "2px solid rgba(206, 159, 229, 0.8)",  # Slightly darker purple border
                                            "borderRadius": "18px",  # Rounded corners
                                            "display": "flex",  # Flexbox for alignment
                                            "alignItems": "center",  # Center content vertically
                                            "justifyContent": "left",  # Center content horizontally
                                            "gap": "14px",  # Space between symbol and text
                                            "cursor": "pointer",
                                            "transition": "all 0.1s ease",  # Smooth transition for hover effect
                                            "padding": "10px",  # Add padding for better spacing
                                            "margin-right": "1px",  # Space between buttons
                                            },
                                        )
                        ]
                    ),
                    
                    
                    # Info button
                    html.Button(
                        id="info-button",
                        style={
                            "width": "220px",  # Adjust width to accommodate text
                            "height": "45px",
                            "backgroundColor": "rgba(214, 234, 248, 1)",  # Light blue background
                            "border": "2px solid rgba(174, 214, 241, 1)",  # Slightly darker blue border
                            "borderRadius": "18px",  # Rounded corners
                            "display": "flex",  # Flexbox for alignment
                            "alignItems": "center",  # Center content vertically
                            "justifyContent": "left",  # Center content horizontally
                            "gap": "14px",  # Space between symbol and text
                            "cursor": "pointer",
                            "transition": "all 0.1s ease",  # Smooth transition for hover effect
                            "padding": "10px",  # Add padding for better spacing
                        },
                        n_clicks=0,
                        title="Click for information",  # Tooltip text on hover
                        children=[
                            html.Img(
                                src="/assets/info_button.png",  # Path to the symbol image
                                style={
                                    "width": "25px",
                                    "height": "25px",
                                    #"backgroundColor": "transparent",  # Ensure background is transparent
                                    #"display": "block",  # Remove extra white space around the image
                                }
                            ),
                            html.Span(
                                "Dashboard guide",
                                style={
                                    "fontFamily": "Times New Roman, Times, serif", # Font family
                                    "color": "black ",  # Text color
                                    "fontSize": "20px",  # Font size
                                    "fontWeight": "bold",  # Bold text
                                }
                            ),
                        ]
                    )
        
                ]
            ),
        
            # Side sheet
            html.Div(
                id="info-sheet",
                style={
                    "position": "fixed",
                    "top": "0",
                    "right": "-100%",  # Start hidden off-screen
                    "width": "30%",  # Adjust width as needed
                    "height": "100%",
                    "backgroundColor": "white",
                    "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
                    "padding": "20px",
                    "overflowY": "auto",
                    "zIndex": "4",
                    "transition": "right 1s ease",  # Smooth sliding effect
                },
                children=[
                    html.Button("Close", id="close-info", style={
                        "position": "absolute",
                        "top": "10px",
                        "right": "10px",
                        "backgroundColor": "#FF0000",
                        "color": "white",
                        "border": "none",
                        "padding": "10px",
                        "borderRadius": "5px",
                        "cursor": "pointer"
                    }),
                    html.H2(
                        "Dashboard Explanation", 
                        style={
                            "fontSize": "32px",  # Larger size for main title
                            "fontWeight": "bold",  # Bold text for emphasis
                            "color": "#333333",  # Dark color for text
                            "marginBottom": "5px",  # Space below the main title
                            "textAlign": "left",  # Align to the left
                        }
                    ),
        
                    # Donut Chart
                    html.Div(
                        children=[
                            html.H3(
                                "Select/Deselect Month(s) (Donut Chart)", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Donut Chart visualizes the yearly change in each month for the selected parameter over the range of the selected years. The twelve segments correspond to months of the year, and corresponding magnitude and direction of monthly change is displayed next to each segment. Selection and deselection of months is enabled through clicking on corresponding segments of the donut chart, which are then pulled out to highlight these. ',
                                style={
                                    "fontSize": "18px",  
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(
                                        src="/assets/temp_wheel.png", 
                                        style={"width": "75%", "height": "auto", "margin": "0px"}
                                    )
                                ],
                                style={"textAlign": "left"}  # Centers the image
                            )
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
                    
                    # Select Year Range
                    html.Div(
                        children=[
                            html.H3(
                                "Select Year Range Slider", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Select Year Range slider allows the choice of specific ranges of years between 2011 and 2024. To adjust to the desired range, drag the slider knobs, and relevant visualizations update accordingly to display data for the selected range.',
                                style={
                                    "fontSize": "18px",  
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(
                                        src="/assets/year_slider.png", 
                                        style={"width": "65%", "height": "auto", "margin": "0px"}
                                    )
                                ],
                                style={"textAlign": "left"}  # Centers the image
                            )
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
                    
                    # Select Parameter
                    html.Div(
                        children=[
                            html.H3(
                                "Select Parameter Dropdown", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Select Parameter dropdown provides the choice between four climate parameters, and selection of a parameter is enabled through clicking on the corresponding radio button. The four available parameters are “Maximum Temperature”, “Mean Temperature”, “Minimum Temperature”, and “Accumulated Precipitation”.',
                                style={
                                    "fontSize": "18px",  
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(
                                        src="/assets/select_parameter.png", 
                                        style={"width": "40%", "height": "auto", "margin": "0px"}
                                    )
                                ],
                                style={"textAlign": "left"}  # Centers the image
                            )
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
                    
                    # Visualization mode
                    html.Div(
                        children=[
                            html.H3(
                                "Spatial Resolution Switch", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Spatial Resolution Switch provides the choice between two spatial resolutions: “Municipalities” and “10x10km Grid”. The “Municipalities” view displays the data by municipalities and presents aggregated values for each municipality. The “10x10km Grid” view displays the data in 10x10 kilometer grid cells covering Denmark.',
                                style={
                                    "fontSize": "18px",  
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(
                                        src="/assets/visualization_mode.png", 
                                        style={"width": "40%", "height": "auto", "margin": "0px"}
                                    )
                                ],
                                style={"textAlign": "left"}  # Centers the image
                            )
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
                    
                    # Trend Map
                    html.Div(
                        children=[
                            html.H3(
                                "Choropleth Map", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Choropleth Map displays yearly changes for the selected parameter based on the spatial resolution chosen in the visualization mode selector. Colors encode values, with darker and lighter shades indicating higher or lower yearly changes, respectively. The color scale on the right of the map provides a reference for interpreting these color gradients as well as hovering over the region to get exact values. Specific regions can be selected by clicking on the map with a maximum of 3 regions allowed and these are highlighted by a bold colored outline.',
                                style={
                                    "fontSize": "18px",
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(
                                        src="/assets/trend_map.png", 
                                        style={"width": "70%", "height": "auto", "margin": "0px"}
                                    )
                                ],
                                style={"textAlign": "left"}  # Centers the image
                            )
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
                
                    # Timeline Figure
                    html.Div(
                        children=[
                            html.H3(
                                "Temporal Line Chart", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Temporal Line Chart shows aggregated actual values for the selected parameter across chosen months from 2011-2024 in Denmark. In the base form, aggregated values for Denmark are displayed with added trendlines for the full range (2011-2024) and selected year range (visible if it is not 2011-2024) both showing the general trend of the data. If regions are selected on the choropleth map, aggregated values for those regions are displayed alongside Denmark with trendlines disappearing. The regions are color coded to match the choropleth map.',
                                style={
                                    "fontSize": "18px",  
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(src="/assets/timeline_figure.png", style={"width": "50%", "height": "auto", "margin": "5px"}),
                                    html.Img(src="/assets/timeline_figure_select.png", style={"width": "50%", "height": "auto", "margin": "5px"}),
                                ],
                                style={
                                    "display": "flex",  # Arrange images side by side
                                    "flexDirection": "row",
                                    "justifyContent": "center",  # Center the images
                                    "alignItems": "left",
                                    "marginTop": "-5px",  # Add spacing above the image row
                                }
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
        
                    # Overview Chart
                    html.Div(
                        children=[
                            html.H3(
                                "Comparative Overview Chart", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Comparative Overview Chart displays monthly averages for all four parameters over two periods. Solid and dashed lines represent recent and historical values, respectively. Bars are sorted to have historical values left (light blue) and recent values right (color teal). Lines correspond to the left-hand y-axis, while bars correspond to the right-hand y-axis. If no regions are selected, average values for Denmark from 1981-2010 are compared to 2011-2024. If one or more regions are selected, historical (2011-2017) and recent (2018-2024) data is compared, taking averages over all selected regions. Colors are not related to other visualizations.',
                                style={
                                    "fontSize": "18px",  
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(
                                        src="/assets/overview_chart.png", 
                                        style={"width": "85%", "height": "auto", "margin": "0px"}
                                    )
                                ],
                                style={"textAlign": "left"}  # Centers the image
                            )
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
        
                    # Bar Chart
                    html.Div(
                        children=[
                            html.H3(
                                "Trend Bar Chart", 
                                style={
                                    "fontSize": "24px",  # Smaller size for the subtitle
                                    "fontWeight": "bold",  # Bold text for the subtitle
                                    "marginBottom": "5px",  # Space below the subtitle
                                    "textAlign": "left",  # Align to the left
                                    "color": "#555555",  # Slightly lighter color for the subtitle
                                }
                            ),
                            html.P(
                                'The Trend Bar Chart provides an overall summary of trends for all four parameters with each group of bars corresponding to one parameter. In the base form, only yearly changes for Denmark are shown, while region-specific changes are added as regions are selected on the choropleth map. The right-most group of bars corresponds to the right-hand y-axis, while the rest correspond to the left-hand y-axis. Regions are color coded as in the line chart and choropleth map.',
                                style={
                                    "fontSize": "18px",  
                                    "fontWeight": "normal",  
                                    "color": "#333333",  
                                    "marginTop": "0px",  
                                    "marginBottom": "10px",  # Space between the text and image
                                    "lineHeight": "1.5",  
                                    "textAlign": "justify",  
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Img(src="/assets/bar_chart.png", style={"width": "50%", "height": "auto", "margin": "5px", "marginBottom": "50px"}),
                                    html.Img(src="/assets/bar_chart_select.png", style={"width": "50%", "height": "auto", "margin": "5px", "marginBottom": "50px"}),
                                ],
                                style={
                                    "display": "flex",  # Arrange images side by side
                                    "flexDirection": "row",
                                    "justifyContent": "center",  # Center the images
                                    "alignItems": "left",
                                    "marginTop": "-5px",  # Add spacing above the image row
                                }
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}
                    ),
                    # Two images alongside each other example
                    # html.Div(
                    #     children=[
                    #         html.Img(src="/assets/select_parameter.png", style={"width": "40%", "height": "auto", "margin": "5px"}),
                    #         html.Img(src="/assets/visualization_mode.png", style={"width": "25%", "height": "auto", "margin": "5px"}),
                    #     ],
                    #     style={
                    #         "display": "flex",  # Arrange images side by side
                    #         "flexDirection": "row",
                    #         "justifyContent": "center",  # Center the images
                    #         "alignItems": "center",
                    #         "marginTop": "20px",  # Add spacing above the image row
                    #     }
                    # ),
                ]
            ),
        
            # Title container with greyed-out background
            html.Div(
                html.H1(
                    "Denmark Climate Trend Dashboard",
                    style={
                        "textAlign": "left",
                        "margin": "0",
                        "color": "#333333",  # Dark text for contrast
                    }
                ),
                style={
                    # Light grey background with opacity
                    "backgroundColor": "rgba(220, 220, 220, 0.5)",
                    "padding": "10px 20px",  # Padding inside the title container
                    "borderRadius": "0px",   # No rounded corners
                    "height": "auto",  # Ensure the background spans the full height of the viewport
                    "width": "100%",  # Width wraps around the title text
                    "margin": "0",  # Remove margin
                    # Optional shadow for subtle elevation
                    "boxShadow": "0 2px 5px rgba(0,0,0,0.2)",
                    "marginBottom": "5px",  # Even smaller space below the title
                    "display": "block"  # Ensures title container is inline-block, not stretching the entire width
                }
            ),
        
            # Combined temp-wheel and parameter selection layout
            html.Div([
                html.Div([
                    html.Div([
                        html.Label(
                            "Select/Deselect Month(s):", 
                            style={"fontSize": "18px", "fontWeight": "bold", "margin": "0px"}
                        ),
                        dcc.Graph(
                            id="temp-wheel", 
                            style={"width": "95%", "height": "200px", "margin": "0px 0"}, 
                            config={"displayModeBar": False}
                        ),
                        html.Div([
                            html.Label(
                                "Select Year Range:", 
                                style={"fontSize": "18px", "fontWeight": "bold", "margin": "0px"}
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
                        ], style={"margin": "10px 0"}),
                        html.Div(
                            children=[
                                # Left side: Existing parameter selection
                                html.Div(
                                    children=[
                                        html.Label(
                                            "Select Parameter:",
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
                                # Right side: New subparameter selection with four buttons
                                html.Div(
                                    children=[
                                        html.Label(
                                            "Select Subpara:",
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
                            style={"display": "flex", "flexDirection": "row", "justifyContent": "space-between"}
                        ),
                        html.Label(
                            "To select regions, click on map →", 
                            style={"fontSize": "18px", "fontWeight": "bold", "margin": "0px"}
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
                                # Toggle switch container
                                html.Div(
                                    children=[
                                        # Label that will update based on the toggle state
                                        html.Div(
                                            id="map-parameter-toggle-label",
                                            children="Show main parameters on map",
                                            style={"fontSize": "16px", "fontWeight": "bold", "marginRight": "10px"}
                                        ),
                                        # The toggle switch
                                        daq.BooleanSwitch(
                                            id="map-parameter-toggle",
                                            on=False,  # Set default state here
                                            color="purple",
                                            style={"verticalAlign": "middle"}
                                        )
                                    ],
                                    style={"display": "flex", "alignItems": "center"}
                                )
                            ],
                            style={"display": "flex", "alignItems": "center"}
                        )

                    ], style={
                        "display": "flex",
                        "flexDirection": "column",
                        "width": "100%",
                        "boxSizing": "border-box"
                    })
                ], style={
                    "width": "20%",
                    "backgroundColor": "rgba(220, 220, 220, 0.5)",
                    "padding": "10px",
                    "margin": "20px",
                    "maxHeight": "550px",
                    "display": "inline-block",
                    "verticalAlign": "top"
                }),
                # Trend map with visualization mode layered on top
                html.Div([
                    dcc.Graph(id="trend-map", style={"width": "100%", "height": "600px", "position": "relative", "z-index": "1"}, config={"displayModeBar": False},),
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
                ], style={
                    "position": "relative", 
                    "width": "45%", 
                    "display": "inline-block", 
                    "verticalAlign": "top", 
                    "margin": "0px", 
                    "padding": "0px"}),
                
            html.Div([
                dcc.Graph(
                    id="timeline",
                    style={"width": "100%", "height": "600px", "margin": "0px"},
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
                        "top": "10px",
                        "left": "10px",
                        "backgroundColor": "rgba(255,255,255,0.7)",
                        "padding": "5px",
                        "borderRadius": "5px",
                        "zIndex": "3"
                    }
                )
            ], style={"position": "relative", "display": "inline-block", "width": "35%"}),
                
            ], style={
                "display": "flex",
                "padding": "0",    # Remove padding from the parent container
                "margin": "0",     # Remove margin from the parent container
                #"height": "100vh",  # Make the container fill the entire viewport height
                "justifyContent": "center"
            }),
        
            # Hidden stores for selected data
            dcc.Store(id="selected-months", data=[]),
            dcc.Store(id="selected-regions", data=[]),
            dcc.Store(id="selected_year", data=None),
            dcc.Store(id="stored-selected-regions", data=[]),
            
            html.Button("Reset Zoom", id="reset-zoom", n_clicks=0),
        
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="overview-chart",
                        style={"width": "65%", "display": "inline-block", "height": "500px", "margin": "0px"},
                        config={"displayModeBar": False},
                    ),
                    html.Div([
                        # Container for label + dropdown (aligned horizontally)
                        html.Div(
                            [
                                html.Label(
                                    "Point-of-view:",
                                    style={
                                        "fontSize": "18px",
                                        "fontWeight": "bold",
                                        "margin": "0px",
                                        "marginRight": "10px",  # Add spacing between label and dropdown
                                    }
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",  # Vertically align items
                                "marginBottom": "5px",
                            }
                        ),
                        html.Div(
                            dcc.Checklist(
                                id="barchart-toggle",
                                options=[{"label": "Show Trendlines", "value": "show"}],
                                value=["show"],
                                labelStyle={"fontSize": "16px", "fontWeight": "bold"}
                            ),
                        ),                        
                        dcc.Graph(
                            id="bar_chart",
                            style={"width": "105%", "height": "440px"},
                            config={"displayModeBar": False},
                        ),
                        html.Div(
                            [
                                html.Img(
                                    src="/assets/DMI_kilde.png",
                                    style={"width": "45px", "height": "auto", "marginRight": "10px"}
                                ),
                                html.Div([
                                    html.Span(
                                        "Data source: ",
                                        style={"fontSize": "16px", "color": "black", "fontWeight": "bold"}
                                    ),
                                    html.A(
                                        "DMI Frie Data",
                                        href="https://www.dmi.dk/frie-data",
                                        style={"fontSize": "16px", "color": "blue", "textDecoration": "none"}
                                    )
                                ])
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "flex-end",
                                "marginTop": "-50px",  # Add some spacing above the DMI source
                                "width": "100%",  # Ensure it spans the full width of its container
                                "marginRight": "0px",  # Move left
                                "position": "absolute",  # Absolute positioning
                                "right": "30px",  # Move further left (adjust this as needed)
                                "zIndex": "100"  # Ensure it stays above bar charts
                            }
                        )
                    ], style={"width": "35%", "display": "inline-block", "height": "auto", "margin": "0px", "overflow": "hidden"})
                ], style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "margin": "0",
                    "padding": "0",
                    "width": "100%",
                    "overflow": "hidden"
                })
            ]),
        ])
    ],
    style={
        "overflowX": "hidden",  # Prevent horizontal scrolling
        "margin": "0",         # Remove unnecessary margins
        "padding": "0",        # Remove unnecessary padding
        "boxSizing": "border-box",  # Ensure all elements respect the container width
        "fontFamily": "Segoe UI, sans-serif"
    }
)

# Colors for municipalities
COLOR_PALETTE = ["gold", "coral", "mediumpurple"]
COLOR_PALETTE2 = ["gold", "coral", "mediumpurple"]

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
        height=210,
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
    
    # Filter Denmark data for the full 2011-2024 period (using selected months)
    denmark_filtered_data = data_grid[
        (data_grid["year"].between(2011, 2024)) &
        (data_grid["month"].isin(selected_months))
    ]
    trend_unit = "mm" if parameter == "acc_precip" else "°C"
    denmark_average_data = denmark_filtered_data.groupby("year")[parameter].mean().reset_index()
    
    timeline = go.Figure()
    
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
            fixedrange=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="lightgrey"
        ),
        margin={"r": 40, "t": 40, "l": 40, "b": 40},
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
# FARMER
@app.callback(
    [Output("selected-months", "data", allow_duplicate=True),
     Output("parameter-dropdown", "value"),
     Output("parameter-dropdown2", "value"),
     Output("visualization-mode", "value", allow_duplicate=True),
     Output("stored-selected-regions", "data", allow_duplicate=True)],
    Input("farmer-button", "n_clicks"),
    prevent_initial_call=True
)
def apply_preset_farmer(n_clicks):
    if n_clicks:
        # Set months to May, June, July, August
        preset_months = [5, 6, 7, 8]
        # Set the main parameter to accumulated precipitation
        preset_parameter = "acc_precip"
        # Set the sub parameter to extreme rain days
        preset_subparameter = "extrain_para"
        # Ensure visualization-mode is municipality grid
        preset_mode = "municipality"
        # Set the selected regions (Aabenraa, Tønder)
        preset_regions = ["0580", "0550"]
        return preset_months, preset_parameter, preset_subparameter, preset_mode, preset_regions
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# SUMMERHOUSE
@app.callback(
    [Output("selected-months", "data", allow_duplicate=True),
     Output("parameter-dropdown", "value", allow_duplicate=True),
     Output("parameter-dropdown2", "value", allow_duplicate=True),
     Output("visualization-mode", "value", allow_duplicate=True),
     Output("stored-selected-regions", "data", allow_duplicate=True)],
    Input("summerhouse-button", "n_clicks"),
    prevent_initial_call=True
)
def apply_preset_summerhouse(n_clicks):
    if n_clicks:
        # Set months to June, July, August
        preset_months = [6, 7, 8]
        # Set the main parameter to mean temperature
        preset_parameter = "mean_temp"
        # Set the sub parameter to summer days
        preset_subparameter = "summer_para"
        # Ensure visualization-mode is municipality grid
        preset_mode = "municipality"
        # Set the selected regions (Frederikshavn, Guldborgsund, Bornholm)
        preset_regions = ["0813", "0376", "0400"]
        return preset_months, preset_parameter, preset_subparameter, preset_mode, preset_regions
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# GARDEN
@app.callback(
    [Output("selected-months", "data", allow_duplicate=True),
     Output("parameter-dropdown", "value", allow_duplicate=True),
     Output("parameter-dropdown2", "value", allow_duplicate=True),
     Output("visualization-mode", "value", allow_duplicate=True),
     Output("stored-selected-regions", "data", allow_duplicate=True)],
    Input("garden-button", "n_clicks"),
    prevent_initial_call=True
)
def apply_preset_garden(n_clicks):
    if n_clicks:
        # Set months to Februrary, March, April, May
        preset_months = [2, 3, 4, 5]
        # Set the main parameter to minimum temperature
        preset_parameter = "min_temp"
        # Set the sub parameter to ice days
        preset_subparameter = "ice_para"
        # Ensure visualization-mode is municipality grid
        preset_mode = "municipality"
        # Set the selected regions (Greve)
        preset_regions = ["0253"]
        return preset_months, preset_parameter, preset_subparameter, preset_mode, preset_regions
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# ENERGY EFFICIENCY
@app.callback(
    [Output("selected-months", "data", allow_duplicate=True),
     Output("parameter-dropdown", "value", allow_duplicate=True),
     Output("parameter-dropdown2", "value", allow_duplicate=True),
     Output("visualization-mode", "value", allow_duplicate=True),
     Output("stored-selected-regions", "data", allow_duplicate=True)],
    Input("energy-button", "n_clicks"),
    prevent_initial_call=True
)
def apply_preset_energy(n_clicks):
    if n_clicks:
        # Set months to September, October, November, December
        preset_months = [9, 10, 11, 12]
        # Set the main parameter to minimum temperature
        preset_parameter = "min_temp"
        # Set the sub parameter to heating degree days
        preset_subparameter = "heat_para"
        # Ensure visualization-mode is 10x10 grid
        preset_mode = "grid"
        # Set the selected regions (Aarhus, 0751) vil gerne rette til 10km_622_56, trend fra, sub på map
        preset_regions = ["10km_622_56"]
        return preset_months, preset_parameter, preset_subparameter, preset_mode, preset_regions
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Callback to toggle the Use Case (Summerhouse) info sheet
@app.callback(
    Output("usecase-sheet-summerhouse", "style"),
    [Input("usecase-button-summerhouse", "n_clicks"), Input("close-usecase-summerhouse", "n_clicks")],
    prevent_initial_call=True
)
def toggle_usecase_summerhouse_sheet(usecase_summerhouse_clicks, close_clicks):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == "usecase-button-summerhouse":
        return {
            "position": "fixed",
            "top": "0",  # Drop down from the top
            "left": "50%",
            "transform": "translateX(-50%)",
            "width": "50%",
            "backgroundColor": "white",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
            "padding": "20px",
            "zIndex": "5",
            "transition": "top 0.3s ease"
        }
    elif triggered_id == "close-usecase-summerhouse":
        return {
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
    return dash.no_update

# Callback to toggle the Use Case (Farmer) info sheet
@app.callback(
    Output("usecase-sheet-farmer", "style"),
    [Input("usecase-button-farmer", "n_clicks"), Input("close-usecase-farmer", "n_clicks")],
    prevent_initial_call=True
)
def toggle_usecase_farmer_sheet(usecase_farmer_clicks, close_clicks):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == "usecase-button-farmer":
        return {
            "position": "fixed",
            "top": "0",  # Drop down from the top
            "left": "50%",
            "transform": "translateX(-50%)",
            "width": "50%",
            "backgroundColor": "white",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
            "padding": "20px",
            "zIndex": "5",
            "transition": "top 0.3s ease"
        }
    elif triggered_id == "close-usecase-farmer":
        return {
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
    return dash.no_update

# Callback to toggle the Use Case (Garden) info sheet
@app.callback(
    Output("usecase-sheet-garden", "style"),
    [Input("usecase-button-garden", "n_clicks"), Input("close-usecase-garden", "n_clicks")],
    prevent_initial_call=True
)
def toggle_usecase_garden_sheet(usecase_garden_clicks, close_clicks):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == "usecase-button-garden":
        return {
            "position": "fixed",
            "top": "0",  # Drop down from the top
            "left": "50%",
            "transform": "translateX(-50%)",
            "width": "50%",
            "backgroundColor": "white",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
            "padding": "20px",
            "zIndex": "5",
            "transition": "top 0.3s ease"
        }
    elif triggered_id == "close-usecase-garden":
        return {
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
    return dash.no_update

# Callback to toggle the Use Case info sheet
@app.callback(
    Output("usecase-sheet-energy", "style"),
    [Input("usecase-button-energy", "n_clicks"), Input("close-usecase-energy", "n_clicks")],
    prevent_initial_call=True
)
def toggle_usecase_energy_sheet(usecase_energy_clicks, close_clicks):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == "usecase-button-energy":
        return {
            "position": "fixed",
            "top": "0",  # Drop down from the top
            "left": "50%",
            "transform": "translateX(-50%)",
            "width": "50%",
            "backgroundColor": "white",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.3)",
            "padding": "20px",
            "zIndex": "5",
            "transition": "top 0.3s ease"
        }
    elif triggered_id == "close-usecase-energy":
        return {
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
    return dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True, port=80, host='0.0.0.0')     