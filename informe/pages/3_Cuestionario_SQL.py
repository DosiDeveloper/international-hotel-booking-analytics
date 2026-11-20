import streamlit as st
from supabase import create_client


@st.cache_resource
def init_connection_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]

    conn_supabase = create_client(url, key)
    return conn_supabase.schema("old_database")


st.header("Cuestionario SQL")

(
    tab_pregunta1,
    tab_pregunta2,
    tab_pregunta3,
    tab_pregunta4,
    tab_pregunta5,
) = st.tabs(
    ["Pregunta 1", "Pregunta 2", "Pregunta 3", "Pregunta 4", "Pregunta 5"]
)

conn_supabase = init_connection_supabase()

with tab_pregunta1:
    query = """
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
    FROM reviews r
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
    JOIN hotels h ON d.hotel_id = h.hotel_id
    GROUP BY h.hotel_id, h.hotel_name
)
SELECT
    hotel_id AS id_hotel,
    hotel_name AS hotel,
    desc_fecha AS descartadas_por_fecha,
    desc_duplicado AS descartadas_por_duplicado,
    pct_descartado AS porcentaje_descartado,
    prom_original AS promedio_original,
    prom_depurado AS promedio_depurado,
    puesto_original,
    puesto_depurado,
    puesto_original - puesto_depurado AS desplazamiento
FROM ranking
WHERE puesto_original <> puesto_depurado
ORDER BY ABS(puesto_original - puesto_depurado) DESC, puesto_depurado ASC;

"""
    st.markdown("""
        La base arrastra dos problemas de integridad: reseñas fechadas antes de que su autor se diera de alta en la plataforma, y registros repetidos de un mismo usuario sobre un mismo hotel en la misma fecha.

        Depurá las reseñas descartando las anteriores al alta de su autor y, dentro de cada grupo repetido, conservando únicamente el registro con el identificador más alto. Si una reseña cumple ambos motivos, imputala al de la fecha. Para cada hotel calculá cuántas reseñas se descartaron por cada motivo, el porcentaje total descartado y el puntaje global promedio antes y después de la depuración.

        Rankeá los hoteles con ambos promedios y mostrá únicamente aquellos cuyo puesto cambia tras la depuración, con el puesto original, el nuevo y el desplazamiento. Ordená por magnitud del desplazamiento y luego por el puesto depurado.
        """)
    with st.container(border=True):
        st.code(query, language="sql", line_numbers=True)
    if st.button("Correr consulta", key="p1"):
        try:
            with st.spinner("Cargando consulta"):
                result = conn_supabase.table("pregunta1").select("*").execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta2:
    query = """
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
    FROM reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Instalaciones', r.score_facilities
    FROM reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Ubicación', r.score_location
    FROM reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Personal', r.score_staff
    FROM reviews r
    INNER JOIN users u ON r.user_id = u.user_id
    WHERE u.traveller_type IS NOT NULL

    UNION ALL
    SELECT u.traveller_type, r.hotel_id, 'Relación calidad-precio', r.score_value_for_money
    FROM reviews r
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
    FROM hotels h
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
"""
    st.markdown("""
        Cada tipo de viajero valora la estadía de forma distinta. Se quiere identificar, para cada segmento, en qué dimensiones es más crítico y en cuál es más benévolo que el conjunto de los huéspedes.

        Para cada tipo de viajero y cada dimensión calculá el promedio del segmento, el promedio general de la dimensión y el desvío porcentual entre ambos. Mostrá, por segmento, las dos dimensiones con el desvío más bajo y la del desvío más alto, indicando su clasificación y su puesto.

        Agregá una columna que indique en cuántos hoteles se replica el patrón: es decir, en cuántos hoteles esa misma dimensión resulta también la más crítica (o la más benévola) del segmento cuando el cálculo se hace dentro de cada hotel. La columna aplica solo a la dimensión más crítica y a la más benévola de cada segmento; en las demás filas debe quedar vacía.

        """)
    with st.container(border=True):
        st.code(query, language="sql", line_numbers=True)
    if st.button("Correr consulta", key="p2"):
        try:
            with st.spinner("Cargando consulta"):
                result = conn_supabase.table("pregunta2").select("*").execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta3:
    query = """
WITH promedios_anuales AS (
        SELECT
            r.hotel_id,
            CAST(EXTRACT(YEAR FROM r.review_date) AS INTEGER) AS anio,
            AVG(r.score_overall) AS puntaje_promedio
        FROM reviews AS r
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
"""
    st.markdown("""
        Se quiere saber cuán estable es la jerarquía de los hoteles a lo largo del tiempo.

        Para cada año, rankeá los hoteles según su puntaje global promedio. A partir de esos rankings construí, para cada hotel, un resumen con: la cantidad de años en que estuvo entre los cinco primeros, su mejor y su peor puesto, la amplitud entre ambos, el año en que logró su mayor ascenso respecto del año anterior y cuántas posiciones ganó, y el año de su mayor caída y cuántas posiciones perdió. Ante empates en la magnitud, informá el año más antiguo.

        Si un hotel nunca ascendió o nunca cayó, las columnas correspondientes deben quedar vacías, no en cero. Mostrá solo los hoteles con una amplitud de al menos dos puestos, ordenados por amplitud descendente.

        """)
    with st.container(border=True):
        st.code(query, language="sql", line_numbers=True)
    if st.button("Correr consulta", key="p3"):
        try:
            with st.spinner("Cargando consulta"):
                result = conn_supabase.table("pregunta3").select("*").execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta4:
    query = """
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
"""
    st.markdown("""
        El puntaje global de una reseña se relaciona con sus seis puntuaciones parciales, pero no todas pesan lo mismo ni del mismo modo en cada segmento de huéspedes.

        Para cada tipo de viajero y cada dimensión calculá el coeficiente de determinación (el cuadrado del coeficiente de correlación de Pearson) entre la dimensión y el puntaje global, construyéndolo a partir de la covarianza y las varianzas. Calculá también el mismo coeficiente sobre el total de las reseñas, sin segmentar.

        Para cada segmento mostrá las dimensiones ordenadas por su coeficiente, con su puesto en el segmento, el puesto que esa dimensión ocupa en el cálculo general, la diferencia de coeficiente respecto del general, el nombre de la dimensión que más explica en el segmento —repetido en todas sus filas— y una columna que indique si el puesto en el segmento coincide o difiere del general.

        """)
    with st.container(border=True):
        st.code(query, language="sql", line_numbers=True)
    if st.button("Correr consulta", key="p4"):
        try:
            with st.spinner("Cargando consulta"):
                result = conn_supabase.table("pregunta4").select("*").execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta5:
    query = """
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
"""
    st.markdown("""
        Cada hotel publica un puntaje de referencia por dimensión. Se quiere contrastarlo con lo que efectivamente califican los huéspedes.

        Para cada hotel y dimensión calculá la brecha entre el promedio observado en las reseñas y el puntaje publicado. Por hotel, identificá la mejor y la peor dimensión según lo publicado y según lo observado —si hay empate, todas las dimensiones empatadas deben listarse en una misma celda—, la dimensión con mayor caída y su magnitud, la brecha absoluta media y cuántas dimensiones cambian de puesto entre ambos ordenamientos.

        Clasificá al hotel como «Alineado» si su mejor y su peor dimensión observadas figuran, respectivamente, entre las mejores y las peores publicadas, y como «Desalineado» en caso contrario. Rankeá los hoteles por brecha absoluta media, de mayor a menor.
        """)
    with st.container(border=True):
        st.code(query, language="sql", line_numbers=True)
    if st.button("Correr consulta", key="p5"):
        try:
            with st.spinner("Cargando consulta"):
                result = conn_supabase.table("pregunta5").select("*").execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)
