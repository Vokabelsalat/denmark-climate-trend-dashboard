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