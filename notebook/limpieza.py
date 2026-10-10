import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import marimo as mo

    return mo, pd


@app.cell
def _(pd):
    df_reviews = pd.read_csv('data/raw/reviews.csv')
    return (df_reviews,)


@app.cell
def _(pd):
    df_hotels = pd.read_csv('data/raw/hotels.csv')
    return (df_hotels,)


@app.cell
def _(pd):
    df_users = pd.read_csv('data/raw/users.csv')
    return (df_users,)


@app.cell(hide_code=True)
def _(df_reviews, mo):
    df = mo.sql(
        f"""
        SELECT * FROM df_reviews
        """
    )
    return (df,)


@app.cell
def _(df_hotels, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM df_hotels
        """
    )
    return


@app.cell
def _(df_users, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM df_users
        """
    )
    return


@app.cell
def _(df_reviews):
    print(df_reviews.isnull().sum())
    return


@app.cell
def _(df_hotels):
    print(df_hotels.isnull().sum())
    return


@app.cell
def _(df_users):
    print(df_users.isnull().sum())
    return


@app.cell
def _(df_reviews, pd):
    df_reviews['review_date'] = pd.to_datetime(df_reviews['review_date'])
    return


@app.cell
def _(df_users, pd):
    df_users['join_date'] = pd.to_datetime(df_users['join_date'])
    return


@app.cell
def _(df):
    df_pd = df.to_pandas()
    return


@app.cell
def _(df_reviews):
    duplicados_usuario_hotel_fecha = df_reviews[
        df_reviews.duplicated(subset=['user_id', 'hotel_id', 'review_date'], keep=False)
    ].sort_values(by=['user_id', 'hotel_id', 'review_date'])

    duplicados_usuario_hotel_fecha
    return


@app.cell
def _(df_reviews, df_users):
    df_merged = df_reviews.merge(df_users[['user_id', 'join_date']], on='user_id', how='left')

    reseñas_inconsistentes = df_merged[df_merged['review_date'] < df_merged['join_date']]

    total_inconsistentes = len(reseñas_inconsistentes)
    print(f"numero de reseñas inconsistentes: {total_inconsistentes}")

    if total_inconsistentes > 0:
        print("Hay datos inconsistentes")
        reseñas_inconsistentes.head()
    else:
        print("No hay datos inconsistentes")
    return


@app.cell
def _(df_reviews):
    df_reviews_limpio = df_reviews.drop_duplicates(subset=['user_id', 'hotel_id', 'review_date'], keep='first').copy()
    return (df_reviews_limpio,)


@app.cell
def _(df_hotels, df_users):
    df_hotels_limpio = df_hotels.drop_duplicates().copy()
    df_users_limpio = df_users.drop_duplicates().copy()
    return df_hotels_limpio, df_users_limpio


@app.cell
def _(df_hotels_limpio, df_reviews_limpio, df_users_limpio):
    df_reviews_limpio.to_csv('data/oltp/reviews_limpio.csv', index=False)
    df_hotels_limpio.to_csv('data/oltp/hotels_limpio.csv', index=False)
    df_users_limpio.to_csv('data/oltp/users_limpio.csv', index=False)
    return


if __name__ == "__main__":
    app.run()
