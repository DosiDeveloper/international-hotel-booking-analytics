import os

import pandas as pd
from .setup import setup as setup_config
from supabase import Client, create_client


def load_data_to_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in the environment variables.")
    if key.startswith("sb_secret_"):
        print("Loading oltp schema")
        supabase: Client = create_client(url, key)
        sql_schema_file = setup_config.script_sql_dir / "schema.sql"
        with open(sql_schema_file, "r") as f:
            sql_schema = f.read()
            supabase.rpc("execute_sql", {"query": sql_schema}).execute()
        print("OLTP schema executed successfully")

    supabase: Client = create_client(url, key)

    df_users = pd.read_csv(setup_config.clean_data_dir /
                           "users_limpio.csv").to_dict(orient="records")
    df_hotels = pd.read_csv(setup_config.clean_data_dir /
                            "hotels_limpio.csv").to_dict(orient="records")
    df_reviews = pd.read_csv(setup_config.clean_data_dir /
                             "reviews_limpio.csv").to_dict(orient="records")
    try:
        res_user = supabase.table("users").insert(df_users).execute()
        print(f"Inserted {len(df_users)} users")
        res_hotels = supabase.table("hotels").insert(df_hotels).execute()
        print(f"Inserted {len(df_hotels)} hotels")
        res_reviews = supabase.table("reviews").insert(df_reviews).execute()
        print(f"Inserted {len(df_reviews)} reviews")
    except Exception as e:
        print(f"Error inserting data: {e}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    load_data_to_supabase()
