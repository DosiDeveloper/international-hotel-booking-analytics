CREATE TABLE hotels (
	hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
	hotel_name TEXT,
	city TEXT,
	country VARCHAR(),
	star_rating INTEGER,
	lat REAL,
	lon REAL,
	cleanliness_base REAL,
	comfort_base REAL,
	facilities_base REAL,
	location_base REAL,
	staff_base REAL,
	value_for_money_base REAL
);
