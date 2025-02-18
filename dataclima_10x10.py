# -*- coding: utf-8 -*-

# Define working directory
directory = r'/Users/lausc/OneDrive - Syddansk Universitet/Kandidat/7. semester/DM878 - Visualization/Projekt'

#%%
# Import necessary libraries
import pandas as pd
import json
import requests
from datetime import datetime

# Define directory (update your path)
directory = r'/Users/lausc/OneDrive - Syddansk Universitet/Kandidat/7. semester/DM878 - Visualization/Projekt'

# Define headers and base URL
headers = {"X-Gravitee-Api-Key": "Insert your API key here!"}
url = "https://dmigw.govcloud.dk/v2/climateData/collections/10kmGridValue/items"

# Define a helper function to fetch and process data
def fetch_climate_data(parameter_id, value_name):
    params = {"timeResolution": "month", 
              "parameterId": parameter_id,
              "limit": 300000}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()["features"]
    # Create a DataFrame with `cell_id`, `year`, `month`, and the parameter value
    return pd.DataFrame([{
        "cell_id": item["properties"]["cellId"],
        "year": datetime.fromisoformat(item["properties"]["from"]).year,
        "month": datetime.fromisoformat(item["properties"]["from"]).month,
        value_name: item["properties"]["value"]
    } for item in data])

# Fetch data for each parameter
temps_df = fetch_climate_data("mean_temp", "mean_temp")
rains_df = fetch_climate_data("acc_precip", "acc_precip")
maxtemp_df = fetch_climate_data("max_temp_w_date", "max_temp")
mintemp_df = fetch_climate_data("min_temp", "min_temp")

# Merge the datasets on `cell_id`, `year`, and `month`
merged_data = pd.merge(temps_df, rains_df, on=["cell_id", "year", "month"], how="outer")
merged_data = pd.merge(merged_data, maxtemp_df, on=["cell_id", "year", "month"], how="outer")
merged_data = pd.merge(merged_data, mintemp_df, on=["cell_id", "year", "month"], how="outer")

# Save the merged data to CSV
merged_data.to_csv(f"{directory}/climate_data_combined_v2.csv", index=False)
