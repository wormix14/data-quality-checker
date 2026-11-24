from azure.identity import AzureCliCredential
import pandas as pd
import os
from deltalake import DeltaTable
from dotenv import load_dotenv

load_dotenv()

LAYERS_CONFIG = {
    "bronze_taxi": (os.getenv("BRONZE_TAXI_PATH"), "data/bronze_taxi.parquet", ["passenger_count", "total_amount", "fare_amount", "trip_distance", "tpep_pickup_datetime"]),
    "silver_taxi": (os.getenv("SILVER_TAXI_PATH"), "data/silver_taxi.parquet", ["passenger_count", "total_amount", "fare_amount", "trip_distance", "tpep_pickup_datetime", "pickup_date"]),
    "gold_taxi": (os.getenv("GOLD_TAXI_PATH"), "data/gold_taxi.parquet", ["borough", "date", "total_revenue", "avg_distance", "trip_count"])
    }

def load_df(layer: str):
    os.makedirs("data", exist_ok=True)
    abfs_path, parquet_path, cols = LAYERS_CONFIG[layer]
    
    try:
        if not abfs_path:
             raise ValueError(f"ABFS path for '{layer}' is not set")
        
        token = AzureCliCredential().get_token("https://storage.azure.com/.default").token

        df = DeltaTable(
            abfs_path,
            storage_options={"bearer_token": token, "use_fabric_endpoint": "true"}
        ).to_pandas(columns=cols)

        df.to_parquet(parquet_path, index=False)

    except Exception as e:
        print(f"Fabric unavailable ({e}), using local parquet.", flush=True)
        df = pd.read_parquet(parquet_path, columns=cols)
    
    return df
