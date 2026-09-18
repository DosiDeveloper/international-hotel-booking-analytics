import pandas as pd
import sqlite3

with sqlite3.connect('data/raw/hotel_bookings.db') as conn:
    df = pd.read_csv('data/raw/hotel_bookings.csv')
    df.to_sql('hotel_bookings', conn, if_exists='replace', index=False)
