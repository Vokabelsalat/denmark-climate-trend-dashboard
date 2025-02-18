# -*- coding: utf-8 -*-

# Define working directory
directory = r'/Users/lausc/OneDrive - Syddansk Universitet/Kandidat/7. semester/DM878 - Visualization/Projekt'

#%% Import Libraries
import pandas as pd
import json
import requests
from datetime import datetime

#%% Fetch Data from API
headers = {"X-Gravitee-Api-Key": "Insert your API key here!"}

url = "https://dmigw.govcloud.dk/v2/climateData/collections/10kmGridValue/items"

params = {"timeResolution": "month", 
          "parameterId": "mean_temp", 
          "limit": 300000}

response = requests.get(url, params=params, headers=headers)
features = response.json()["features"]

#%% Process Data into DataFrame
data = pd.DataFrame([
    {
        "geometry": feature["geometry"],
        "cell_id": feature["properties"]["cellId"],
        "value": feature["properties"]["value"],
        "year": datetime.fromisoformat(feature["properties"]["from"]).year,
        "month": datetime.fromisoformat(feature["properties"]["from"]).month,
    }
    for feature in features
])

# Save climate data (without geometry) as CSV
data.drop(columns=["geometry"]).to_csv(f"{directory}/climate_data.csv", index=False)

#%% Create Base GeoJSON
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "geometry": row["geometry"], "properties": {"cell_id": row["cell_id"]}}
        for _, row in data.drop_duplicates(subset="cell_id")[["geometry", "cell_id"]].iterrows()
    ],
}

# Save GeoJSON file
with open(f"{directory}/base_grid.geojson", "w") as f:
    json.dump(geojson_data, f)

print("GeoJSON and CSV files saved successfully.")
