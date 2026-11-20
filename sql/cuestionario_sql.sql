DROP VIEW IF EXISTS old_database.pregunta1;
DROP VIEW IF EXISTS old_database.pregunta2;
DROP VIEW IF EXISTS old_database.pregunta3;
DROP VIEW IF EXISTS old_database.pregunta4;
DROP VIEW IF EXISTS old_database.pregunta5;
DROP VIEW IF EXISTS old_database.pregunta6;

CREATE VIEW old_database.pregunta1 AS
SELECT *
FROM old_database.hotels;

CREATE VIEW old_database.pregunta2 AS
SELECT *
FROM old_database.hotels;

CREATE VIEW old_database.pregunta3 AS
SELECT *
FROM old_database.users;

CREATE VIEW old_database.pregunta4 AS
SELECT *
FROM old_database.reviews;

CREATE VIEW old_database.pregunta5 AS
SELECT *
FROM old_database.reviews
JOIN old_database.users USING (user_id);

CREATE VIEW old_database.pregunta6 AS
SELECT
    r.*,
    u.country AS user_country,
    h.hotel_name,
    h.country AS hotel_country
FROM old_database.reviews r
JOIN old_database.users u USING (user_id)
JOIN old_database.hotels h USING (hotel_id);

GRANT SELECT ON old_database.pregunta1, old_database.pregunta2, old_database.pregunta3,
    old_database.pregunta4, old_database.pregunta5, old_database.pregunta6
TO anon, authenticated;
