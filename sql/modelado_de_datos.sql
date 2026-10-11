-- Creamos los esquemas a utilizar
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS analytics_models;

-- Creamos la Tabla Denormalizada 
CREATE OR REPLACE TABLE analytics.hotel_reviews_master AS
SELECT
    r.review_id,
    CAST(r.review_date AS DATE) AS review_date, 
    r.score_overall,
    r.score_cleanliness,
    r.score_comfort,
    r.score_facilities,
    r.score_location,
    r.score_staff,
    r.score_value_for_money,
    r.review_text,
    h.hotel_id,
    h.hotel_name,
    h.city,
    h.country AS hotel_country,
    h.star_rating,
    h.lat,
    h.lon,
    u.user_id,
    u.user_gender,
    u.country AS user_country,
    u.age_group,
    u.traveller_type,
    CAST(u.join_date AS DATE) AS user_join_date 
FROM main.REVIEWS r
LEFT JOIN main.HOTELES h ON r.hotel_id = h.hotel_id
LEFT JOIN main.USUARIOS u ON r.user_id = u.user_id;

-- Creamos la Tabla de Factos
CREATE OR REPLACE TABLE analytics.fact_reviews AS
SELECT 
    review_id,
    hotel_id,
    user_id,
    CAST(STRFTIME(review_date, '%Y%m%d') AS INT) AS date_id,  -- <-- Corregido
    review_date,
    score_overall,
    score_cleanliness,
    score_comfort,
    score_facilities,
    score_location,
    score_staff,
    score_value_for_money
FROM analytics.hotel_reviews_master;

-- Creamos las Tablas de Dimensiones 
CREATE OR REPLACE TABLE analytics.dim_hotels AS
SELECT DISTINCT
    hotel_id,
    hotel_name,
    city,
    hotel_country AS country,
    star_rating,
    lat,
    lon
FROM analytics.hotel_reviews_master;

CREATE OR REPLACE TABLE analytics.dim_users AS
SELECT DISTINCT
    user_id,
    user_gender,
    user_country AS country,
    age_group,
    traveller_type,
    user_join_date
FROM analytics.hotel_reviews_master;

CREATE OR REPLACE TABLE analytics.dim_tiempo AS
SELECT DISTINCT
    CAST(STRFTIME(review_date, '%Y%m%d') AS INT) AS date_id, 
    review_date,
    EXTRACT(year FROM review_date) AS year,
    EXTRACT(month FROM review_date) AS month,
    EXTRACT(day FROM review_date) AS day,
    STRFTIME(review_date, '%A') AS day_of_week, 
    EXTRACT(quarter FROM review_date) AS quarter
FROM analytics.fact_reviews;

-- Creamos las Tablas para los Análisis Estadísticos en el esquema de analytics_models
CREATE OR REPLACE TABLE analytics_models.hotel_bayesian_inputs AS
WITH global_stats AS (
    SELECT AVG(score_overall) AS global_avg_score
    FROM main.REVIEWS
)
SELECT
    h.hotel_id,
    h.hotel_name,
    h.star_rating,
    COUNT(r.review_id) AS total_reviews,      
    AVG(r.score_overall) AS avg_hotel_score,  
    g.global_avg_score                        
FROM main.HOTELES h
LEFT JOIN main.REVIEWS r ON h.hotel_id = r.hotel_id
CROSS JOIN global_stats g
GROUP BY h.hotel_id, h.hotel_name, h.star_rating, g.global_avg_score;

CREATE OR REPLACE TABLE analytics_models.hotel_traveller_profiles AS
SELECT
    h.hotel_id,
    h.hotel_name,
    h.star_rating,
    AVG(CASE WHEN u.traveller_type = 'Solo' THEN r.score_overall END) AS score_solo,
    AVG(CASE WHEN u.traveller_type = 'Family' THEN r.score_overall END) AS score_family,
    AVG(CASE WHEN u.traveller_type = 'Couple' THEN r.score_overall END) AS score_couple,
    AVG(CASE WHEN u.traveller_type = 'Business' THEN r.score_overall END) AS score_business,
    AVG(r.score_overall) AS score_general
FROM main.HOTELES h
LEFT JOIN main.REVIEWS r ON h.hotel_id = r.hotel_id
LEFT JOIN main.USUARIOS u ON r.user_id = u.user_id
GROUP BY h.hotel_id, h.hotel_name, h.star_rating;

-- Eliminamos la Tabla Denormalizada ya que no la necesitaremos más
DROP TABLE analytics.hotel_reviews_master;
