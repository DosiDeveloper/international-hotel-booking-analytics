CREATE TABLE reviews (
	review_id INTEGER,
	user_id INTEGER,
	hotel_id INTEGER,
	review_date TEXT,
	score_overall REAL,
	score_cleanliness REAL,
	score_comfort REAL,
	score_facilities REAL,
	score_location REAL,
	score_staff REAL,
	score_value_for_money REAL,
	review_text TEXT
	PRIMARY KEY (review_id, user_id, hotel_id)
);
