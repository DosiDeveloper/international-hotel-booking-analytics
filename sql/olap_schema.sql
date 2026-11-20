CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS analytics_models;

DROP TABLE IF EXISTS analytics_models.hotel_traveller_profiles;
DROP TABLE IF EXISTS analytics_models.hotel_bayesian_inputs;
DROP TABLE IF EXISTS analytics.fact_reviews;
DROP TABLE IF EXISTS analytics.dim_hotels;
DROP TABLE IF EXISTS analytics.dim_users;
DROP TABLE IF EXISTS analytics.dim_tiempo;

CREATE TABLE analytics.dim_hotels (
    hotel_id BIGINT PRIMARY KEY,
    hotel_name VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    star_rating INTEGER NOT NULL,
    lat DOUBLE NOT NULL,
    lon DOUBLE NOT NULL
);

CREATE TABLE analytics.dim_users (
    user_id BIGINT PRIMARY KEY,
    user_gender VARCHAR NOT NULL CHECK (user_gender IN ('Male', 'Female', 'Other')),
    country VARCHAR NOT NULL,
    age_group VARCHAR NOT NULL CHECK (age_group IN ('18-24', '25-34', '35-44', '45-54', '55+')),
    traveller_type VARCHAR NOT NULL CHECK (traveller_type IN ('Solo', 'Couple', 'Family', 'Business')),
    user_join_date DATE NOT NULL
);

CREATE TABLE analytics.dim_tiempo (
    date_id INTEGER PRIMARY KEY,
    review_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_week VARCHAR NOT NULL,
    quarter INTEGER NOT NULL
);

CREATE TABLE analytics.fact_reviews (
    review_id BIGINT PRIMARY KEY,
    hotel_id BIGINT NOT NULL REFERENCES analytics.dim_hotels(hotel_id),
    user_id BIGINT NOT NULL REFERENCES analytics.dim_users(user_id),
    date_id INTEGER NOT NULL REFERENCES analytics.dim_tiempo(date_id),
    review_date DATE NOT NULL,
    score_overall DOUBLE NOT NULL,
    score_cleanliness DOUBLE NOT NULL,
    score_comfort DOUBLE NOT NULL,
    score_facilities DOUBLE NOT NULL,
    score_location DOUBLE NOT NULL,
    score_staff DOUBLE NOT NULL,
    score_value_for_money DOUBLE NOT NULL
);

CREATE TABLE analytics_models.hotel_bayesian_inputs (
    hotel_id BIGINT PRIMARY KEY,
    hotel_name VARCHAR NOT NULL,
    star_rating INTEGER NOT NULL,
    total_reviews BIGINT NOT NULL,
    avg_hotel_score DOUBLE,
    global_avg_score DOUBLE NOT NULL
);

CREATE TABLE analytics_models.hotel_traveller_profiles (
    hotel_id BIGINT PRIMARY KEY,
    hotel_name VARCHAR NOT NULL,
    star_rating INTEGER NOT NULL,
    score_solo DOUBLE,
    score_family DOUBLE,
    score_couple DOUBLE,
    score_business DOUBLE,
    score_general DOUBLE
);
