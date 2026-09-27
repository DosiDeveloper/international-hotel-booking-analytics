PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS hotels;

CREATE TABLE hotels (
	hotel_id INTEGER PRIMARY KEY,
	hotel_name TEXT NOT NULL,
	city TEXT NOT NULL,
	country TEXT NOT NULL,
	star_rating INTEGER NOT NULL,
	cleanliness_base REAL NOT NULL,
	comfort_base REAL NOT NULL,
	facilities_base REAL NOT NULL,
	location_base REAL NOT NULL,
	staff_base REAL NOT NULL,
	value_for_money_base REAL NOT NULL,
	lat REAL NOT NULL,
	lon REAL NOT NULL
);

CREATE TABLE users (
	user_id INTEGER PRIMARY KEY,
	user_gender TEXT NOT NULL CHECK (user_gender IN ('Male', 'Female', 'Other')),
	country TEXT NOT NULL,
	age_group TEXT NOT NULL CHECK (age_group IN ('18-24', '25-34', '35-44', '45-54', '55+')),
	traveller_type TEXT NOT NULL CHECK (traveller_type IN ('Solo', 'Couple', 'Family', 'Business')),
	join_date TEXT NOT NULL CHECK (join_date IS date(join_date))
);

CREATE TABLE reviews (
	review_id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL REFERENCES users(user_id),
	hotel_id INTEGER NOT NULL REFERENCES hotels(hotel_id) ON DELETE CASCADE,
	review_date TEXT NOT NULL CHECK (review_date IS date(review_date)),
	score_overall REAL NOT NULL,
	score_cleanliness REAL NOT NULL,
	score_comfort REAL NOT NULL,
	score_facilities REAL NOT NULL,
	score_location REAL NOT NULL,
	score_staff REAL NOT NULL,
	score_value_for_money REAL NOT NULL,
	review_text TEXT
);
