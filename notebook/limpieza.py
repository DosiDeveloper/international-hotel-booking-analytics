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
def _(df_reviews, pd):
    df_reviews['review_date'] = pd.to_datetime(df_reviews['review_date'])
    return


@app.cell
def _(df):
    df_pd = df.to_pandas()
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
def _(df_hotels, df_reviews, df_users):
    df_reviews_clean = df_reviews.drop_duplicates()
    df_hotels_clean = df_hotels.drop_duplicates()
    df_users_clean = df_users.drop_duplicates()
    return


@app.cell
def _(df_hotels, df_reviews, df_users):
    df_reviews.to_csv('data/oltp/reviews_clean.csv', index=False)
    df_hotels.to_csv('data/oltp/hotels_clean.csv', index=False)
    df_users.to_csv('data/oltp/users_clean.csv', index=False)
    return


if __name__ == "__main__":
    app.run()
