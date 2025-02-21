# layout.py
from dash import dcc, html

use_cases_data = [
    {
        "id": "usecase-summerhouse",
        "name": "Summerhouse",
        "title": "Click for Information on Summerhouse Use Case",
        "buttonID": "summerhouse-button",
        "icon": "/assets/summerhouse_icon.png",
        "full_title": "Use Case: A Family Looking for a Summerhouse",
        "paragraphs": [
            "A family looking for a summerhouse along the Danish coast will want to know how warm and pleasant the summers have been in different regions. This view highlights June through August in Frederikshavn, Guldborgsund, and Bornholm, showing both average temperatures and the number of summer days. The data can help identify which locations have the most stable and inviting summer climate, making it easier to choose the perfect spot for a summer retreat.",
            "If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
            "Results: Across Denmark, average summer temperatures have been rising, indicating that summers are becoming warmer. The number of summer days (above X°C) has increased, making the climate more attractive for vacationing. Among the selected locations, Bornholm stands out with the highest increase in warm summer days as well as the warmest mean temperature, making it a particularly appealing destination for those seeking consistent, warm summer weather."
        ],
    },
    {
        "id": "usecase-farmer",
        "name": "Farmer",
        "title": "Click for information on Farmer Use Case",
        "buttonID": "farmer-button",
        "icon": "/assets/farmer_icon.png",
        "full_title": "Use Case: A Farmer in Aabenraa and Tønder",
        "paragraphs": [
            "A farmer located in Aabenraa or Tønder needs to keep a close eye on rainfall patterns during the growing season. This view focuses on May through August, showing both total precipitation and the number of extreme rain days. Reviewing the trends can help determine whether heavy rainfall events are becoming more frequent, which might require better drainage solutions or adjustments to irrigation planning.",
            "If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
            "Results: The data reveals a rapid decline in total precipitation for Aabenraa and Tønder compared to the rest of Denmark. Additionally, the number of extreme rain days (above 10mm) has decreased, which could indicate that farmers may need to rely more on irrigation systems to maintain optimal soil moisture. This suggests a notable shift towards drier growing seasons, potentially impacting crop yields and requiring changes in water management strategies."
        ],
    },
    {
        "id": "usecase-garden",
        "name": "Garden",
        "title": "Click for information on Garden Use Case",
        "buttonID": "garden-button",
        "icon": "/assets/flower_icon.png",
        "full_title": "Use Case: A Gardener in Greve",
        "paragraphs": [
            "A gardener in Greve planning for the upcoming season needs to know when frost risks fade and planting conditions improve. This view tracks February through May, focusing on minimum temperatures and ice days. Looking at these trends can help determine whether spring is arriving earlier, allowing for an extended planting season, or if late frosts remain a concern that could impact garden planning.",
            "If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
            "Results: The data shows that minimum temperatures in early spring have been steadily increasing, indicating a clear warming trend. At the same time, the number of ice days has decreased, suggesting that planting can now begin earlier than in previous years without significant frost risk. In particular, Greve’s frost risk in March and April has been lower compared to past years, making it possible for gardeners to extend their growing season and plant more sensitive species earlier in the year."
        ],
    },
    {
        "id": "usecase-energy",
        "name": "Energy",
        "title": "Click for information on Energy Use Case",
        "buttonID": "energy-button",
        "icon": "/assets/energy_icon.png",
        "full_title": "Use Case: An Energy Efficiency Planner in Aarhus",
        "paragraphs": [
            "A homeowner or building manager in Aarhus interested in energy efficiency can use this view to assess how autumn temperatures impact heating demand. Covering September through December, it displays minimum temperatures and heating degree days, helping to track whether autumns are becoming milder. Reviewing this data can provide insight into whether heating demand is decreasing over time and whether investments in insulation or energy-saving measures are needed.",
            "If you want to explore this data further and adjust the settings yourself, click the 'Apply Filters' button.",
            "Results: The data shows that minimum autumn temperatures have been decreasing, meaning colder nights during the fall season. However, heating degree days have remained stable, suggesting that overall heating demand has not significantly changed. Given this stability, homeowners may not need to make additional investments in insulation, energy-efficient windows, or alternative heating sources at this time, as heating requirements have remained consistent over the years"
        ],
    }
]

def create_use_button(button_data):
    return [html.Button(
        id=f"{button_data['id']}-button",
        className="usecase-button scale-on-hover",
        n_clicks=0,
        title=button_data["title"],
        children=[
            html.Img(src=button_data["icon"], style={"width": "25px", "height": "25px"}),
            html.Span(button_data["name"])
        ]
    ),
    # Use Case info sheet (drops down from the top and centered)
    html.Div(
        id=button_data["id"]+"-sheet",
        className="usecase-sheet",
        children=[
            html.Button("Close", id=button_data["id"]+"-close", className="scale-on-hover", style={
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
            html.H2(button_data["full_title"], style={
                "fontSize": "32px",
                "fontWeight": "bold",
                "color": "#333333",
                "marginBottom": "5px",
                "textAlign": "center"
            }),
            *[html.P(y, className="usecase-p") for y in button_data["paragraphs"]],
            html.Button("Apply filters!", id=button_data['id']+"button", n_clicks=0, className="filter-button scale-on-hover")
        ])
    ]

use_cases = html.Div(children=sum([create_use_button(x) for x in use_cases_data],[]), className="usecase-wrapepr")

    