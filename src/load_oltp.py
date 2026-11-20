import os
from pathlib import Path

import pandas as pd
from supabase import create_client


def _get_client_and_key():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in the environment variables."
        )
    return create_client(url, key), key


def _apply_schemas(client, key: str, script_sql_dir: Path):
    if not key.startswith("sb_secret_"):
        return

    print("Loading oltp schema")
    for sql_script in ("oltp_schema.sql", "old_schema.sql", "cuestionario_sql.sql"):
        with open(script_sql_dir / sql_script, "r") as f:
            sql_schema = f.read()
        client.rpc("execute_sql", {"query": sql_schema}).execute()
    print("OLTP schema executed successfully")


def _prepare_clean_data(clean_data_dir: Path):
    df_users = pd.read_csv(clean_data_dir / "users_limpio.csv")
    df_hotels = pd.read_csv(clean_data_dir / "hotels_limpio.csv")
    df_reviews = pd.read_csv(clean_data_dir / "reviews_limpio.csv").to_dict(
        orient="records"
    )

    df_country = (
        df_hotels[["country", "city"]]
        .drop_duplicates(subset=["country"])
        .sort_values("country")
        .reset_index(drop=True)
    )
    df_country.insert(0, "country_id", df_country.index + 1)

    country_ids = df_country.set_index("country")["country_id"]
    df_users["country"] = df_users["country"].map(country_ids).astype(int)
    df_hotels["country"] = df_hotels["country"].map(country_ids).astype(int)
    df_users = df_users.rename(columns={"country": "country_id"})
    df_hotels = df_hotels.rename(columns={"country": "country_id"})

    return df_country, df_users, df_hotels, df_reviews


def _prepare_old_data(raw_data_dir: Path):
    df_old_users = pd.read_csv(raw_data_dir / "users.csv").to_dict(orient="records")
    df_old_hotels = pd.read_csv(raw_data_dir / "hotels.csv").to_dict(orient="records")
    df_old_reviews = pd.read_csv(raw_data_dir / "reviews.csv").to_dict(orient="records")
    return df_old_users, df_old_hotels, df_old_reviews


def _insert_rows(target, table: str, rows: list[dict], label: str | None = None):
    res = target.table(table).insert(rows).execute()
    print(f"Inserted {res.count} {label or table}")


def load_data_to_supabase(
    script_sql_dir: Path, clean_data_dir: Path, raw_data_dir: Path
):
    client, key = _get_client_and_key()
    _apply_schemas(client, key, script_sql_dir)

    df_country, df_users, df_hotels, df_reviews = _prepare_clean_data(clean_data_dir)
    old_users, old_hotels, old_reviews = _prepare_old_data(raw_data_dir)

    try:
        _insert_rows(
            client, "country", df_country.to_dict(orient="records"), "countries"
        )
        _insert_rows(client, "users", df_users.to_dict(orient="records"))
        _insert_rows(client, "hotels", df_hotels.to_dict(orient="records"))
        _insert_rows(client, "reviews", df_reviews)

        print("Inserting on old database schema")
        old_database = client.schema("old_database")
        _insert_rows(old_database, "users", old_users)
        _insert_rows(old_database, "hotels", old_hotels)
        _insert_rows(old_database, "reviews", old_reviews)
    except Exception as e:
        print(f"Error inserting data: {e}")
        raise
