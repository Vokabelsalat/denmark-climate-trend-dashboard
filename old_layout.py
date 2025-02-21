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
                children=[]
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