# layout.py
from dash import html

# Side sheet
info_sheet = html.Div(
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
                    html.Button("Close", id="close-info", className="scale-on-hover", style={
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Donut Chart visualizes the yearly change in each month for the selected parameter over the range of the selected years. The twelve segments correspond to months of the year, and corresponding magnitude and direction of monthly change is displayed next to each segment. Selection and deselection of months is enabled through clicking on corresponding segments of the donut chart, which are then pulled out to highlight these. ',
                                className="paragraph-text"
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Select Year Range slider allows the choice of specific ranges of years between 2011 and 2024. To adjust to the desired range, drag the slider knobs, and relevant visualizations update accordingly to display data for the selected range.',
                                className="paragraph-text"
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Select Parameter dropdown provides the choice between four climate parameters, and selection of a parameter is enabled through clicking on the corresponding radio button. The four available parameters are “Maximum Temperature”, “Mean Temperature”, “Minimum Temperature”, and “Accumulated Precipitation”.',
                                className="paragraph-text"
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Spatial Resolution Switch provides the choice between two spatial resolutions: “Municipalities” and “10x10km Grid”. The “Municipalities” view displays the data by municipalities and presents aggregated values for each municipality. The “10x10km Grid” view displays the data in 10x10 kilometer grid cells covering Denmark.',
                                className="paragraph-text"
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Choropleth Map displays yearly changes for the selected parameter based on the spatial resolution chosen in the visualization mode selector. Colors encode values, with darker and lighter shades indicating higher or lower yearly changes, respectively. The color scale on the right of the map provides a reference for interpreting these color gradients as well as hovering over the region to get exact values. Specific regions can be selected by clicking on the map with a maximum of 3 regions allowed and these are highlighted by a bold colored outline.',
                                className="paragraph-text"
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Temporal Line Chart shows aggregated actual values for the selected parameter across chosen months from 2011-2024 in Denmark. In the base form, aggregated values for Denmark are displayed with added trendlines for the full range (2011-2024) and selected year range (visible if it is not 2011-2024) both showing the general trend of the data. If regions are selected on the choropleth map, aggregated values for those regions are displayed alongside Denmark with trendlines disappearing. The regions are color coded to match the choropleth map.',
                                className="paragraph-text"
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Comparative Overview Chart displays monthly averages for all four parameters over two periods. Solid and dashed lines represent recent and historical values, respectively. Bars are sorted to have historical values left (light blue) and recent values right (color teal). Lines correspond to the left-hand y-axis, while bars correspond to the right-hand y-axis. If no regions are selected, average values for Denmark from 1981-2010 are compared to 2011-2024. If one or more regions are selected, historical (2011-2017) and recent (2018-2024) data is compared, taking averages over all selected regions. Colors are not related to other visualizations.',
                                className="paragraph-text"
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
                                className="subtitle"
                            ),
                            html.P(
                                'The Trend Bar Chart provides an overall summary of trends for all four parameters with each group of bars corresponding to one parameter. In the base form, only yearly changes for Denmark are shown, while region-specific changes are added as regions are selected on the choropleth map. The right-most group of bars corresponds to the right-hand y-axis, while the rest correspond to the left-hand y-axis. Regions are color coded as in the line chart and choropleth map.',
                                className="paragraph-text"
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
                ]
            )