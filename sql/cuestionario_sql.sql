DROP VIEW IF EXISTS old_database.pregunta1;
DROP VIEW IF EXISTS old_database.pregunta2;
DROP VIEW IF EXISTS old_database.pregunta3;
DROP VIEW IF EXISTS old_database.pregunta4;
DROP VIEW IF EXISTS old_database.pregunta5;
DROP VIEW IF EXISTS old_database.pregunta6;

CREATE VIEW old_database.pregunta1 AS
WITH depuracion AS (
    SELECT
        r.hotel_id,
        r.score_overall,
        CASE
            WHEN r.review_date < u.join_date THEN 'fecha'
            WHEN ROW_NUMBER() OVER (
                PARTITION BY r.user_id, r.hotel_id, r.review_date
                ORDER BY r.review_id DESC
            ) > 1 THEN 'duplicado'
            ELSE 'valida'
        END AS estado
    FROM old_database.reviews r
    LEFT JOIN users u ON r.user_id = u.user_id
),
ranking AS (
    SELECT
        h.hotel_id,
        h.hotel_name,
        SUM(CASE WHEN d.estado = 'fecha' THEN 1 ELSE 0 END) AS desc_fecha,
        SUM(CASE WHEN d.estado = 'duplicado' THEN 1 ELSE 0 END) AS desc_duplicado,
        ROUND(100.0 * SUM(CASE WHEN d.estado <> 'valida' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_descartado,
        AVG(d.score_overall) AS prom_original,
        AVG(CASE WHEN d.estado = 'valida' THEN d.score_overall END) AS prom_depurado,
        RANK() OVER (ORDER BY AVG(d.score_overall) DESC) AS puesto_original,
        RANK() OVER (
            ORDER BY AVG(CASE WHEN d.estado = 'valida' THEN d.score_overall END) DESC
        ) AS puesto_depurado
    FROM depuracion d
    JOIN old_database.hotels h ON d.hotel_id = h.hotel_id
    GROUP BY h.hotel_id, h.hotel_name
)
SELECT
    hotel_id AS id_hotel,
    hotel_name AS hotel,
    desc_fecha AS descartadas_por_fecha,
    desc_duplicado AS descartadas_por_duplicado,
    pct_descartado AS porcentaje_descartado,
    ROUND(prom_original, 2) AS promedio_original,
    ROUND(prom_depurado, 2) AS promedio_depurado,
    puesto_original,
    puesto_depurado,
    puesto_original - puesto_depurado AS desplazamiento
FROM ranking
WHERE puesto_original <> puesto_depurado
ORDER BY ABS(puesto_original - puesto_depurado) DESC, puesto_depurado ASC;

CREATE VIEW old_database.pregunta2 AS
WITH dimensiones_largas AS (
    SELECT
        u.traveller_type AS tipo_viajero,
        r.hotel_id,
        'Limpieza' AS dimension,
        r.score_cleanliness AS puntaje
    FROM reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Confort', r.score_comfort
    FROM old_database.reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Instalaciones', r.score_facilities
    FROM old_database.reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Ubicación', r.score_location
    FROM old_database.reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Personal', r.score_staff
    FROM reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Relación calidad-precio', r.score_value_for_money
    FROM old_database.reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL
),
metricas_globales AS (
    SELECT DISTINCT
        tipo_viajero,
        dimension,
        AVG(puntaje) OVER (PARTITION BY tipo_viajero, dimension) AS promedio_segmento,
        AVG(puntaje) OVER (PARTITION BY dimension) AS promedio_general,
        (
            (AVG(puntaje) OVER (PARTITION BY tipo_viajero, dimension)
             - AVG(puntaje) OVER (PARTITION BY dimension)) * 100.0
            / NULLIF(AVG(puntaje) OVER (PARTITION BY dimension), 0)
        ) AS desvio_porcentual
    FROM dimensiones_largas
),
ranking_segmento AS (
    SELECT
        tipo_viajero,
        dimension,
        promedio_segmento,
        promedio_general,
        desvio_porcentual,
        ROW_NUMBER() OVER (
            PARTITION BY tipo_viajero
            ORDER BY desvio_porcentual ASC, dimension ASC
        ) AS puesto_bajo,
        ROW_NUMBER() OVER (
            PARTITION BY tipo_viajero
            ORDER BY desvio_porcentual DESC, dimension ASC
        ) AS puesto_alto
    FROM metricas_globales
),
seleccion_segmento AS (
    SELECT
        tipo_viajero,
        dimension,
        promedio_segmento,
        promedio_general,
        desvio_porcentual,
        CASE
            WHEN puesto_bajo IN (1, 2) THEN 'Más crítico'
            ELSE 'Más benévolo'
        END AS clasificacion,
        CASE
            WHEN puesto_bajo IN (1, 2) THEN puesto_bajo
            ELSE puesto_alto
        END AS puesto,
        CASE
            WHEN puesto_bajo = 1 THEN 'CRITICO'
            WHEN puesto_alto = 1 THEN 'BENEVOLO'
            ELSE NULL
        END AS rol_extremo
    FROM ranking_segmento
    WHERE puesto_bajo IN (1, 2)
       OR puesto_alto = 1
),
promedios_por_hotel AS (
    SELECT
        h.hotel_id,
        d.dimension,
        AVG(d.puntaje) AS prom_general_hotel
    FROM old_database.hotels h
    INNER JOIN dimensiones_largas d ON h.hotel_id = d.hotel_id
    GROUP BY h.hotel_id, d.dimension
),
desvio_por_hotel_segmento AS (
    SELECT
        d.tipo_viajero,
        d.hotel_id,
        d.dimension,
        (
            (AVG(d.puntaje) - ph.prom_general_hotel) * 100.0
            / NULLIF(ph.prom_general_hotel, 0)
        ) AS desvio_hotel
    FROM dimensiones_largas d
    INNER JOIN promedios_por_hotel ph
        ON d.hotel_id = ph.hotel_id
       AND d.dimension = ph.dimension
    GROUP BY d.tipo_viajero, d.hotel_id, d.dimension, ph.prom_general_hotel
),
extremos_por_hotel AS (
    SELECT
        tipo_viajero,
        hotel_id,
        dimension,
        ROW_NUMBER() OVER (
            PARTITION BY tipo_viajero, hotel_id
            ORDER BY desvio_hotel ASC, dimension ASC
        ) AS rn_critico_hotel,
        ROW_NUMBER() OVER (
            PARTITION BY tipo_viajero, hotel_id
            ORDER BY desvio_hotel DESC, dimension ASC
        ) AS rn_benevolo_hotel
    FROM desvio_por_hotel_segmento
),
replicas_por_hotel AS (
    SELECT
        tipo_viajero,
        dimension,
        SUM(CASE WHEN rn_critico_hotel = 1 THEN 1 ELSE 0 END) AS hoteles_critica,
        SUM(CASE WHEN rn_benevolo_hotel = 1 THEN 1 ELSE 0 END) AS hoteles_benevola
    FROM extremos_por_hotel
    GROUP BY tipo_viajero, dimension
)
SELECT
    s.tipo_viajero AS "Tipo de viajero",
    s.dimension AS "Dimensión",
    s.promedio_segmento AS "Promedio del segmento",
    s.promedio_general AS "Promedio general",
    s.desvio_porcentual AS "Desvío porcentual",
    s.clasificacion AS "Clasificación",
    s.puesto AS "Puesto",
    CASE
        WHEN s.rol_extremo = 'CRITICO' THEN r.hoteles_critica
        WHEN s.rol_extremo = 'BENEVOLO' THEN r.hoteles_benevola
        ELSE NULL
    END AS "Hoteles donde se replica"
FROM seleccion_segmento s
LEFT JOIN replicas_por_hotel r
    ON s.tipo_viajero = r.tipo_viajero
   AND s.dimension = r.dimension
ORDER BY
    s.tipo_viajero ASC,
    CASE WHEN s.clasificacion = 'Más crítico' THEN 1 ELSE 2 END ASC,
    s.puesto ASC;

CREATE VIEW old_database.pregunta3 AS
WITH promedios_anuales AS (
        SELECT
            r.hotel_id,
            CAST(EXTRACT(YEAR FROM r.review_date) AS INTEGER) AS anio,
            AVG(r.score_overall) AS puntaje_promedio
        FROM old_database.reviews AS r
        GROUP BY r.hotel_id, EXTRACT(YEAR FROM r.review_date)
    ),
    rankings_anuales AS (
        SELECT
            hotel_id,
            anio,
            puntaje_promedio,
            RANK() OVER (PARTITION BY anio ORDER BY puntaje_promedio DESC) AS puesto
        FROM promedios_anuales
    ),
    cambios_de_puesto AS (
        SELECT
            hotel_id,
            anio,
            puesto,
            LAG(puesto) OVER (PARTITION BY hotel_id ORDER BY anio) AS puesto_anterior
        FROM rankings_anuales
    ),
    movimientos AS (
        SELECT
            hotel_id,
            anio,
            puesto,
            puesto_anterior,
            CASE
                WHEN puesto_anterior IS NOT NULL AND puesto < puesto_anterior
                THEN puesto_anterior - puesto
            END AS posiciones_ganadas,
            CASE
                WHEN puesto_anterior IS NOT NULL AND puesto > puesto_anterior
                THEN puesto - puesto_anterior
            END AS posiciones_perdidas
        FROM cambios_de_puesto
    ),
    mayor_ascenso AS (
        SELECT hotel_id, anio, posiciones_ganadas
        FROM (
            SELECT
                hotel_id,
                anio,
                posiciones_ganadas,
                ROW_NUMBER() OVER (
                    PARTITION BY hotel_id
                    ORDER BY posiciones_ganadas DESC, anio ASC
                ) AS rn
            FROM movimientos
            Where posiciones_ganadas IS NOT NULL
        )
        WHERE rn = 1
    ),
    mayor_caida AS (
        SELECT hotel_id, anio, posiciones_perdidas
        FROM (
            SELECT
                hotel_id,
                anio,
                posiciones_perdidas,
                ROW_NUMBER() OVER (
                    PARTITION BY hotel_id
                    ORDER BY posiciones_perdidas DESC, anio ASC
                ) AS rn
            FROM movimientos
            WHERE posiciones_perdidas IS NOT NULL
        )
        WHERE rn = 1
    ),
    resumen_por_hotel AS (
        SELECT
            hotel_id,
            COUNT(CASE WHEN puesto <= 5 THEN 1 END) AS anios_en_top5,
            MIN(puesto) AS mejor_puesto,
            MAX(puesto) AS peor_puesto,
            MAX(puesto) - MIN(puesto) AS amplitud
        FROM rankings_anuales
        GROUP BY hotel_id
    )

    SELECT
        h.hotel_id,
        h.hotel_name AS nombre_hotel,
        s.anios_en_top5 AS anios_top5,
        s.mejor_puesto,
        s.peor_puesto,
        s.amplitud,
        ma.anio AS anio_mayor_ascenso,
        ma.posiciones_ganadas,
        mc.anio AS anio_mayor_caida,
        mc.posiciones_perdidas
    FROM resumen_por_hotel AS s
    JOIN hotels AS h
        ON h.hotel_id = s.hotel_id
    LEFT JOIN mayor_ascenso AS ma
        ON ma.hotel_id = s.hotel_id
    LEFT JOIN mayor_caida AS mc
        ON mc.hotel_id = s.hotel_id
    WHERE s.amplitud >= 2
    ORDER BY s.amplitud DESC;

CREATE VIEW old_database.pregunta4 AS
WITH ctx AS (
    SELECT
        u.traveller_type,
        r.score_overall,
        r.score_cleanliness,
        r.score_comfort,
        r.score_facilities,
        r.score_location,
        r.score_staff,
        r.score_value_for_money
    FROM old_database.reviews r
    JOIN old_database.users u ON u.user_id = r.user_id
),
base AS (
    SELECT traveller_type, 'Limpieza' AS dimension, score_cleanliness AS puntaje, score_overall FROM ctx
    UNION ALL SELECT traveller_type, 'Confort', score_comfort, score_overall FROM ctx
    UNION ALL SELECT traveller_type, 'Instalaciones', score_facilities, score_overall FROM ctx
    UNION ALL SELECT traveller_type, 'Ubicación', score_location, score_overall FROM ctx
    UNION ALL SELECT traveller_type, 'Personal', score_staff, score_overall FROM ctx
    UNION ALL SELECT traveller_type, 'Relación calidad-precio', score_value_for_money, score_overall FROM ctx
),
segmento_medias AS (
    SELECT
        traveller_type,
        dimension,
        AVG(puntaje) AS media_puntaje,
        AVG(score_overall) AS media_overall
    FROM base
    GROUP BY traveller_type, dimension
),
segmento AS (
    SELECT
        b.traveller_type,
        b.dimension,
        POWER(SUM((b.puntaje - m.media_puntaje) * (b.score_overall - m.media_overall)), 2)
            / NULLIF(
                SUM(POWER(b.puntaje - m.media_puntaje, 2))
                * SUM(POWER(b.score_overall - m.media_overall, 2)),
                0
            ) AS coeficiente
    FROM base b
    JOIN segmento_medias m
      ON m.traveller_type = b.traveller_type AND m.dimension = b.dimension
    GROUP BY b.traveller_type, b.dimension
),
general_medias AS (
    SELECT
        dimension,
        AVG(puntaje) AS media_puntaje,
        AVG(score_overall) AS media_overall
    FROM base
    GROUP BY dimension
),
general AS (
    SELECT
        b.dimension,
        POWER(SUM((b.puntaje - m.media_puntaje) * (b.score_overall - m.media_overall)), 2)
            / NULLIF(
                SUM(POWER(b.puntaje - m.media_puntaje, 2))
                * SUM(POWER(b.score_overall - m.media_overall, 2)),
                0
            ) AS coeficiente
    FROM base b
    JOIN general_medias m ON m.dimension = b.dimension
    GROUP BY b.dimension
),
general_rank AS (
    SELECT
        *,
        RANK() OVER (ORDER BY coeficiente DESC) AS puesto_general
    FROM general
),
rankeado AS (
    SELECT
        s.traveller_type,
        s.dimension,
        s.coeficiente,
        g.coeficiente AS coeficiente_general,
        g.puesto_general,
        RANK() OVER (PARTITION BY s.traveller_type ORDER BY s.coeficiente DESC) AS puesto_segmento,
        FIRST_VALUE(s.dimension) OVER (
            PARTITION BY s.traveller_type
            ORDER BY s.coeficiente DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS dimension_top
    FROM segmento s
    JOIN general_rank g ON g.dimension = s.dimension
)
SELECT
    traveller_type AS tipo_viajero,
    dimension,
    ROUND(CAST(coeficiente AS DECIMAL(18,6)), 4) AS coeficiente_segmento,
    puesto_segmento,
    puesto_general,
    ROUND(CAST(coeficiente - coeficiente_general AS DECIMAL(18,6)), 4) AS diferencia,
    dimension_top,
    CASE WHEN puesto_segmento = puesto_general THEN 'Coincide' ELSE 'Difiere' END AS coincide
FROM rankeado
ORDER BY traveller_type, puesto_segmento;

CREATE VIEW old_database.pregunta5 AS
WITH publicados AS (
    SELECT hotel_id, hotel_name, 'Limpieza' AS dimension, cleanliness_base AS puntaje FROM old_database.hotels
    UNION ALL SELECT hotel_id, hotel_name, 'Confort', comfort_base FROM old_database.hotels
    UNION ALL SELECT hotel_id, hotel_name, 'Instalaciones', facilities_base FROM old_database.hotels
    UNION ALL SELECT hotel_id, hotel_name, 'Ubicación', location_base FROM old_database.hotels
    UNION ALL SELECT hotel_id, hotel_name, 'Personal', staff_base FROM old_database.hotels
    UNION ALL SELECT hotel_id, hotel_name, 'Relación calidad-precio', value_for_money_base FROM old_database.hotels
),
ctx AS (
    SELECT
        r.hotel_id,
        r.score_cleanliness,
        r.score_comfort,
        r.score_facilities,
        r.score_location,
        r.score_staff,
        r.score_value_for_money
    FROM old_database.reviews r
),
observados AS (
    SELECT hotel_id, 'Limpieza' AS dimension, AVG(score_cleanliness) AS puntaje FROM ctx GROUP BY hotel_id
    UNION ALL SELECT hotel_id, 'Confort', AVG(score_comfort) FROM ctx GROUP BY hotel_id
    UNION ALL SELECT hotel_id, 'Instalaciones', AVG(score_facilities) FROM ctx GROUP BY hotel_id
    UNION ALL SELECT hotel_id, 'Ubicación', AVG(score_location) FROM ctx GROUP BY hotel_id
    UNION ALL SELECT hotel_id, 'Personal', AVG(score_staff) FROM ctx GROUP BY hotel_id
    UNION ALL SELECT hotel_id, 'Relación calidad-precio', AVG(score_value_for_money) FROM ctx GROUP BY hotel_id
),
comparado AS (
    SELECT
        p.hotel_id,
        p.hotel_name,
        p.dimension,
        p.puntaje AS publicado,
        o.puntaje AS observado,
        o.puntaje - p.puntaje AS brecha
    FROM publicados p
    JOIN observados o ON o.hotel_id = p.hotel_id AND o.dimension = p.dimension
),
con_puestos AS (
    SELECT
        *,
        RANK() OVER (PARTITION BY hotel_id ORDER BY publicado DESC) AS puesto_publicado,
        RANK() OVER (PARTITION BY hotel_id ORDER BY observado DESC) AS puesto_observado
    FROM comparado
),
extremos AS (
    SELECT
        *,
        MIN(puesto_publicado) OVER (PARTITION BY hotel_id) AS mejor_publicado,
        MAX(puesto_publicado) OVER (PARTITION BY hotel_id) AS peor_publicado,
        MIN(puesto_observado) OVER (PARTITION BY hotel_id) AS mejor_observado,
        MAX(puesto_observado) OVER (PARTITION BY hotel_id) AS peor_observado
    FROM con_puestos
),
resumen AS (
    SELECT
        hotel_id,
        hotel_name,
        STRING_AGG(dimension, ', ' ORDER BY dimension) FILTER (WHERE puesto_publicado = mejor_publicado) AS mejor_publicada,
        STRING_AGG(dimension, ', ' ORDER BY dimension) FILTER (WHERE puesto_publicado = peor_publicado) AS peor_publicada,
        STRING_AGG(dimension, ', ' ORDER BY dimension) FILTER (WHERE puesto_observado = mejor_observado) AS mejor_observada,
        STRING_AGG(dimension, ', ' ORDER BY dimension) FILTER (WHERE puesto_observado = peor_observado) AS peor_observada,
        CASE WHEN MIN(brecha) < 0 THEN (ARRAY_AGG(dimension ORDER BY brecha ASC, dimension))[1] END AS mayor_caida,
        CASE WHEN MIN(brecha) < 0 THEN -MIN(brecha) END AS magnitud_caida,
        AVG(ABS(brecha)) AS brecha_absoluta_media,
        COUNT(*) FILTER (WHERE puesto_publicado <> puesto_observado) AS dimensiones_que_cambian,
        CASE
            WHEN BOOL_OR(puesto_observado = mejor_observado AND puesto_publicado = mejor_publicado)
             AND BOOL_OR(puesto_observado = peor_observado AND puesto_publicado = peor_publicado)
            THEN 'Alineado'
            ELSE 'Desalineado'
        END AS alineacion
    FROM extremos
    GROUP BY hotel_id, hotel_name
)
SELECT
    hotel_id,
    hotel_name AS hotel,
    mejor_publicada,
    peor_publicada,
    mejor_observada,
    peor_observada,
    mayor_caida,
    ROUND(CAST(magnitud_caida AS DECIMAL(18,6)), 4) AS magnitud_caida,
    ROUND(CAST(brecha_absoluta_media AS DECIMAL(18,6)), 4) AS brecha_absoluta_media,
    dimensiones_que_cambian,
    alineacion
FROM resumen
ORDER BY brecha_absoluta_media DESC;
