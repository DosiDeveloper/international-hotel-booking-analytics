from pathlib import Path

import duckdb


def load_data_to_duckdb(
    olap_data_dir: Path, script_sql_dir: Path, clean_data_dir: Path
):

    path_users_csv = clean_data_dir / "users_limpio.csv"
    path_hotels_csv = clean_data_dir / "hotels_limpio.csv"
    path_reviews_csv = clean_data_dir / "reviews_limpio.csv"
    try:
        # Loading csv on main schema
        conn = duckdb.connect(database=olap_data_dir /
                              "db.duckdb", read_only=False)
        conn.execute(
            f"CREATE OR REPLACE TABLE 'USUARIOS' AS SELECT * FROM read_csv('{path_users_csv.absolute()}')"
        )
        print(f"Inserted data from {path_users_csv} into USERS table")

        conn.execute(
            f"CREATE OR REPLACE TABLE 'HOTELES' AS SELECT * FROM '{path_hotels_csv.absolute()}'"
        )
        print(f"Inserted data from {path_hotels_csv} into HOTELES table")

        conn.execute(
            f"CREATE OR REPLACE TABLE 'REVIEWS' AS SELECT * FROM '{path_reviews_csv.absolute()}'"
        )
        print(f"Inserted data from {path_reviews_csv} into REVIEWS table")

        # loading data of star schema
        for sql_script in ("olap_schema.sql", "modelado_de_datos.sql"):
            with open(script_sql_dir / sql_script, "r") as f:
                conn.execute(f.read())
            print(f"Executed {sql_script}")
        conn.close()
    except Exception as e:
        print(e)
        raise
