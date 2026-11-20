CREATE SCHEMA IF NOT EXISTS old_database;

DROP TABLE IF EXISTS old_database.users CASCADE;
DROP TABLE IF EXISTS old_database.hotels CASCADE;
DROP TABLE IF EXISTS old_database.reviews CASCADE;

CREATE TABLE old_database.hotels (
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

CREATE TABLE old_database.users (
	user_id INTEGER PRIMARY KEY,
	user_gender TEXT NOT NULL CHECK (user_gender IN ('Male', 'Female', 'Other')),
	country TEXT NOT NULL,
	age_group TEXT NOT NULL CHECK (age_group IN ('18-24', '25-34', '35-44', '45-54', '55+')),
	traveller_type TEXT NOT NULL CHECK (traveller_type IN ('Solo', 'Couple', 'Family', 'Business')),
	join_date DATE NOT NULL
);

CREATE TABLE old_database.reviews (
	review_id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL REFERENCES old_database.users(user_id),
	hotel_id INTEGER NOT NULL REFERENCES old_database.hotels(hotel_id),
	review_date DATE NOT NULL,
	score_overall REAL NOT NULL,
	score_cleanliness REAL NOT NULL,
	score_comfort REAL NOT NULL,
	score_facilities REAL NOT NULL,
	score_location REAL NOT NULL,
	score_staff REAL NOT NULL,
	score_value_for_money REAL NOT NULL,
	review_text TEXT
);

ALTER TABLE old_database.hotels ENABLE ROW LEVEL SECURITY;
ALTER TABLE old_database.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE old_database.reviews ENABLE ROW LEVEL SECURITY;

CREATE POLICY "lectura_publica" ON old_database.hotels FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "lectura_publica" ON old_database.users FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "lectura_publica" ON old_database.reviews FOR SELECT TO anon, authenticated USING (true);

GRANT USAGE ON SCHEMA old_database TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA old_database TO anon, authenticated;
