app.layout = html.Div(
    children=[
        html.Div([ 
            # Hidden stores for selected data
            
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