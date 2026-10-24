import os
from pathlib import Path

import pandas as pd
from supabase import create_client


def load_data_to_supabase(script_sql_dir: Path, clean_data_dir: Path):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in the environment variables."
        )
    if key.startswith("sb_secret_"):
        print("Loading oltp schema")
        supabase_client = create_client(url, key)
        sql_schema_file = script_sql_dir / "schema.sql"
        with open(sql_schema_file, "r") as f:
            sql_schema = f.read()
            supabase_client.rpc("execute_sql", {"query": sql_schema}).execute()
        print("OLTP schema executed successfully")

    supabase_client = create_client(url, key)

    df_users = pd.read_csv(clean_data_dir / "users_limpio.csv").to_dict(
        orient="records"
    )
    df_hotels = pd.read_csv(clean_data_dir / "hotels_limpio.csv").to_dict(
        orient="records"
    )
    df_reviews = pd.read_csv(clean_data_dir / "reviews_limpio.csv").to_dict(
        orient="records"
    )
    try:
        res_user = supabase_client.table("users").insert(df_users).execute()
        print(f"Inserted {res_user.count} users")
        res_hotels = supabase_client.table(
            "hotels").insert(df_hotels).execute()
        print(f"Inserted {res_hotels.count} hotels")
        res_reviews = supabase_client.table(
            "reviews").insert(df_reviews).execute()
        print(f"Inserted {res_reviews.count} reviews")
    except Exception as e:
        print(f"Error inserting data: {e}")

