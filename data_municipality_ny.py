# -*- coding: utf-8 -*-

# Define working directory
directory = r'/Users/lausc/OneDrive - Syddansk Universitet/Kandidat/7. semester/DM878 - Visualization/Projekt'

#%% Import Libraries
import pandas as pd
import json
import requests
from datetime import datetime
import geopandas as gpd
from shapely.geometry import mapping  # Import for converting geometries to GeoJSON-compatible format

#%% Fetch Data from API
headers = {"X-Gravitee-Api-Key": "eafec8a7-1fca-4fbe-bf86-7ce81cde0446"}

url = "https://dmigw.govcloud.dk/v2/climateData/collections/municipalityValue/items"

params = {"timeResolution": "month", 
          "parameterId": "mean_temp", 
          "limit": 300000}

response = requests.get(url, params=params, headers=headers)
features = response.json()["features"]

#%% Process Data into DataFrame
data = pd.DataFrame([
    {
        "geometry": feature["geometry"],
        "cell_id": feature["properties"]["municipalityId"],
        "value": feature["properties"]["value"],
        "year": datetime.fromisoformat(feature["properties"]["from"]).year,
        "month": datetime.fromisoformat(feature["properties"]["from"]).month,
    }
    for feature in features
])

#%% Load Municipality GeoJSON
import re

# Helper function to fix corrupted UTF-8 characters
def fix_encoding(text):
    if isinstance(text, str):
        return text.encode('latin1').decode('utf-8')
    return text

# Load GeoJSON and fix strings
with open("municipalities.geojson", "r", encoding="utf-8") as f:
    geojson_raw = f.read()
    geojson_fixed = re.sub(r'Ã¸', 'ø', geojson_raw)
    geojson_fixed = re.sub(r'Ã¦', 'æ', geojson_fixed)
    geojson_fixed = re.sub(r'Ã¥', 'å', geojson_fixed)
    geojson_data = json.loads(geojson_fixed)

# Extract municipality polygons, ensuring only 2D coordinates
for feature in geojson_data["features"]:
    coords = feature["geometry"]["coordinates"]
    if feature["geometry"]["type"] == "Polygon":
        feature["geometry"]["coordinates"] = [
            [(lon, lat) for lon, lat, _ in ring] for ring in coords
        ]
    elif feature["geometry"]["type"] == "MultiPolygon":
        feature["geometry"]["coordinates"] = [
            [[(lon, lat) for lon, lat, _ in ring] for ring in polygon] for polygon in coords
        ]

municipalities = gpd.GeoDataFrame.from_features(geojson_data["features"])
municipalities = municipalities.set_crs(epsg=4326)  # Ensure CRS is WGS84

# Convert API point geometry into GeoDataFrame
data_gdf = gpd.GeoDataFrame(
    data, geometry=gpd.points_from_xy(
        [geom['coordinates'][0] for geom in data['geometry']],
        [geom['coordinates'][1] for geom in data['geometry']]
    ), crs="EPSG:4326"
)

#%% Perform Spatial Join
# Match points to municipality polygons
joined = gpd.sjoin(data_gdf, municipalities, how="left", predicate="intersects")

# Check for unmatched points
if joined["label_dk"].isnull().any():
    print("Warning: Some points could not be matched to a municipality!")

# Group by label_dk to get all polygons for each municipality
municipality_polygons = (
    municipalities.groupby("label_dk", group_keys=False)
    .agg({"geometry": lambda geoms: geoms.unary_union})  # Combine polygons for each municipality
    .reset_index()
)

# Merge the joined data with the aggregated municipality polygons
final_data = (
    joined[["cell_id", "label_dk"]]
    .drop_duplicates()  # Ensure no duplicates in the cell_id-label_dk mapping
    .merge(municipality_polygons, on="label_dk", how="left")  # Attach combined polygons
)

# Check for missing geometries
if final_data["geometry"].isnull().any():
    print("Error: Some cell_ids do not have associated geometries!")

#%% Create Final GeoJSON
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": mapping(row["geometry"]),  # Polygon geometry from municipalities
            "properties": {"cell_id": row["cell_id"], "municipality": row["label_dk"]},
        }
        for _, row in final_data.iterrows()
    ],
}

# Save GeoJSON file
with open(f"{directory}/base_grid_municipality.geojson", "w") as f:
    json.dump(geojson_data, f)

print("GeoJSON and CSV files saved successfully.")
