import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Initial setup
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Download data from kagglehub
    """)
    return


@app.cell(disabled=True)
def _():
    import kagglehub
    import pathlib

    # Download latest version
    path = pathlib.Path(kagglehub.dataset_download("alperenmyung/international-hotel-booking-analytics", output_dir="../data/raw/", force_download=True))
    return (path,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remove unused folder '_.complete/ _' and move database file to
    """)
    return


@app.cell
def _(path):
    import shutil
    import operator as op

    try:
        for f in path.iterdir():
            if op.contains(str(f), '.complete'):
                shutil.rmtree(f, ignore_errors=True)
            if op.contains(str(f), '.db') or op.contains(str(f), '.sqlite'):
                shutil.move(f, '../data/oltp/')
    except Exception as e:
        print(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Create new connection of the new SQLite database file, DuckDB database file and Original SQlite database file
    """)
    return


@app.cell
def _():
    import duckdb

    DATABASE_URL_duckdb = "data/oltp/reservation.sqlite"
    duckdb_engine = duckdb.connect(DATABASE_URL_duckdb, read_only=False)
    return


@app.cell
def _():
    import sqlalchemy

    DATABASE_URL = "sqlite:///data/oltp/booking_db.sqlite"
    sqlite_engine = sqlalchemy.create_engine(DATABASE_URL)
    return (sqlalchemy,)


@app.cell
def _(sqlalchemy):
    DATABASE_URL_new_oltp = "sqlite:///data/oltp/reservation.sqlite"
    new_sqlite_engine = sqlalchemy.create_engine(DATABASE_URL_new_oltp)
    return (new_sqlite_engine,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Load normalized schema of original database to new database
    """)
    return


@app.cell
def _(new_sqlite_engine):
    with new_sqlite_engine.begin() as conn:
        schema_file = open("sql\\schema.sql")
        conn.connection.executescript(schema_file.read())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Checking if is the schema is correctly loaded to database
    """)
    return


@app.cell
def _(mo, new_sqlite_engine, sqlite_master):
    new_db_list = mo.sql(
        f"""
        SELECT
            name
        FROM
            sqlite_master
        WHERE
            type = 'table'
        ORDER BY
            name;
        """,
        engine=new_sqlite_engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Migrate data of old database to new database
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        ATTACH 'data/oltp/booking_db.sqlite' as old_db;

        ATTACH 'data/oltp/reservation.sqlite' as new_db;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO
            new_db.main.reviews (
                SELECT
                    *
                FROM
                    old_db.main.reviews
            )
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO
            new_db.main.users (
                SELECT
                    *
                FROM
                    old_db.main.users
            )
        """
    )
    return


@app.cell(disabled=True)
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO
            new_db.main.users (
                SELECT
                    *
                FROM
                    old_db.main.users
            )
        """
    )
    return


@app.cell(disabled=True)
def _(mo):
    _df = mo.sql(
        f"""
        INSERT INTO
            new_db.main.hotels (
                SELECT
                    hotel_id,
                    hotel_name,
                    city,
                    country,
            		star_rating,
                    lat,
                    lon
                FROM
                    old_db.main.hotels
            );
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. Construir rankings de destinos y hoteles por relación precio-calidad usando promedio bayesiano (ponderado por número de reseñas) y contrastarlos con el promedio simple. Así se muestra por qué una ciudad con 12 reseñas no debería encabezar un ranking.
    """)
    return


@app.cell(hide_code=True)
def _(mo, new_sqlite_engine):
    df = mo.sql(
        f"""
        SELECT
            h.hotel_name,
            (h.country +),
            COUNT(r.review_id) as count_reviews,
            AVG(r.score_value_for_money) OVER (
                PARTITION BY
                    h.hotel_id
            ) as overall_value_money
        FROM
            reviews r
            JOIN hotels h ON r.hotel_id = h.hotel_id
        GROUP BY
            h.hotel_name
        """,
        engine=new_sqlite_engine
    )
    return (df,)


@app.cell
def _(df):
    df_hotel_value_for_money = df.to_pandas()
    m_media_global = (
        df_hotel_value_for_money["overall_value_money"]
        * df_hotel_value_for_money["count_reviews"]
    ).sum() / df_hotel_value_for_money["count_reviews"].sum()

    c_min_reviews = df_hotel_value_for_money["count_reviews"].quantile(0.25)

    def cal_bayesian_mean(f, m=m_media_global, C=c_min_reviews):
        R = f["overall_value_money"]
        v = f["count_reviews"]
        return round(((v * R) + (C * m)) / (v + C), 2)

    df_hotel_value_for_money["bayesian_mean"] = df_hotel_value_for_money.apply(
        cal_bayesian_mean, axis=1
    )

    df_hotel_value_for_money = df_hotel_value_for_money.sort_values('bayesian_mean', ascending=False).reset_index(drop=True)

    df_hotel_value_for_money[:5]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Evaluar si la percepción de valor difiere según traveller_type, age_group y viajero local vs. internacional (cuando users.country = hotels.country). Usar ANOVA o Kruskal-Wallis con post-hoc y tamaño de efecto.
    """)
    return


@app.cell
def _(mo, new_sqlite_engine, reviews):
    _df = mo.sql(
        f"""
        select * from reviews
        """,
        engine=new_sqlite_engine
    )
    return


@app.cell
def _(hotels, mo, new_sqlite_engine, reviews, users):
    df_perception = mo.sql(
        f"""
        SELECT
            h.hotel_name,
            h.star_rating,
            u.age_group,
            u.traveller_type,
            r.score_value_for_money,
            CASE 
            	WHEN u.country = h.country THEN 'Local'
            ElSE 'Internacional'
            END AS origin
        FROM
            reviews r
            JOIN hotels h ON h.hotel_id = r.hotel_id
            JOIN users u ON u.user_id = r.user_id
        """,
        engine=new_sqlite_engine
    )
    return (df_perception,)


@app.cell
def _(df_perception):
    res = []
    for factor in ['traveller_type', 'age_group', 'origin']:
        temp_df = df_perception[['']] 
    return


@app.cell(hide_code=True)
def _(mo, new_sqlite_engine, reviews):
    _df = mo.sql(
        f"""
        DELETE FROM reviews;
        """,
        engine=new_sqlite_engine
    )
    return


@app.cell(disabled=True)
def _(mo, new_sqlite_engine, users):
    _df = mo.sql(
        f"""
        DELETE FROM users;
        """,
        engine=new_sqlite_engine
    )
    return


@app.cell(disabled=True)
def _(hotels, mo, new_sqlite_engine):
    _df = mo.sql(
        f"""
        DELETE FROM hotels;
        """,
        engine=new_sqlite_engine
    )
    return


if __name__ == "__main__":
    app.run()
