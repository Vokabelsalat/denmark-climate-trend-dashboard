# -*- coding: utf-8 -*-
import pandas as pd
import requests
from datetime import datetime

url = "https://dmigw.govcloud.dk/v2/climateData/collections/10kmGridValue/items"
headers = {"X-Gravitee-Api-Key": "eafec8a7-1fca-4fbe-bf86-7ce81cde0446"}

# Define a helper function to fetch and process data (only for 2011-2024)
def fetch_climate_data(parameter_id, value_name):
    params = {
        "timeResolution": "month", 
        "parameterId": parameter_id,
        "limit": 300000
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()  # Return empty DataFrame if request fails
    
    data = response.json().get("features", [])
    
    # Create a DataFrame while filtering only for 2011-2024
    df = pd.DataFrame([
        {
            "cell_id": item["properties"]["cellId"],
            "year": datetime.fromisoformat(item["properties"]["from"]).year,
            "month": datetime.fromisoformat(item["properties"]["from"]).month,
            value_name: item["properties"]["value"]
        }
        for item in data
        if 2011 <= datetime.fromisoformat(item["properties"]["from"]).year <= 2024  # Filter here
    ])

    return df


def fetch_climate_data_day(parameter_id, value_name):
    all_data = []

    for year in range(2011, 2025):  # Include 2024
        params = {
            "timeResolution": "day",
            "parameterId": parameter_id,
            "limit": 300000,
            "datetime": f"{year}-01-01T00:00:00Z/{year}-12-31T23:59:59Z"
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200 or not response.text.strip():
            print(f"Error fetching data for {year}: {response.status_code}")
            continue  

        try:
            data = response.json().get("features", [])
        except ValueError:
            print(f"Error decoding JSON for {year}")
            continue

        if not data:
            print(f"No data for {year}")
            continue

        print(f"Fetched {len(data)} records for {year}")
        
        # Process and store data safely
        all_data.extend([
            {
                "cell_id": item["properties"]["cellId"],
                "date": item["properties"]["from"],
                value_name: item["properties"].get("value", 0)  # Default to 0 if missing
            }
            for item in data if "value" in item["properties"]  # Ensure "value" exists
        ])

    # Convert to DataFrame
    df = pd.DataFrame(all_data)

    # Convert date column safely
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)  # Handle errors, force UTC
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # Drop rows with missing dates
    df = df.dropna(subset=["year", "month"])

    # Group by cell_id, year, month and sum only the value column
    return df.groupby(["cell_id", "year", "month"], as_index=False)[value_name].sum()

# Fetch data
heat_df = fetch_climate_data("acc_heating_degree_days_17", "heat_para")
heat_df2 = fetch_climate_data_day("acc_heating_degree_days_17", "heat_para")
ice_df = fetch_climate_data_day("no_ice_days", "ice_para")
summer_df = fetch_climate_data_day("no_summer_days", "summer_para")
extrain_df = fetch_climate_data_day("no_days_acc_precip_10", "extrain_para")

# Merge the datasets on `cell_id`, `year`, and `month`
merged_data = ice_df
for df in [heat_df2, summer_df, extrain_df]:
    merged_data = pd.merge(merged_data, df, on=["cell_id", "year", "month"], how="outer")

# Define working directory
directory = r'/Users/lausc/OneDrive - Syddansk Universitet/Kandidat/7. semester/DM878 - Visualization/Projekt'

# Save the merged data to CSV
merged_data.to_csv(f"{directory}/climate_parameters_combined_v2.csv", index=False)