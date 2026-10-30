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
    tab_pregunta6,
) = st.tabs(
    ["Pregunta 1", "Pregunta 2", "Pregunta 3", "Pregunta 4", "Pregunta 5", "Pregunta 6"]
)

conn_supabase = init_connection_supabase()

with tab_pregunta1:
    query = """
select
    *
from
    hotels
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
                result = conn_supabase.table("pregunta1").select("*").limit(20).execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta2:
    query = """
select
    *
from
    hotels
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
                result = conn_supabase.table("pregunta2").select("*").limit(20).execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta3:
    query = """
select
    *
from
    users
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
                result = conn_supabase.table("pregunta3").select("*").limit(20).execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta4:
    query = """
select
    *
from
    reviews
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
                result = conn_supabase.table("pregunta4").select("*").limit(20).execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta5:
    query = """
select
    *
from
    reviews
join users using (user_id)
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
                result = conn_supabase.table("pregunta5").select("*").limit(20).execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)

with tab_pregunta6:
    query = """
select
    r.*,
    u.country as user_country,
    h.hotel_name,
    h.country as hotel_country
from
    reviews r
join users u using (user_id)
join hotels h using (hotel_id)
"""
    st.markdown("""
        Un mismo puntaje no significa lo mismo viniendo de un huésped exigente que de uno generoso. Para medir la tendencia de cada usuario hay que compararlo con el contexto de cada reseña, no con un promedio general.

        Construí un índice de indulgencia por usuario: el promedio de la diferencia entre el puntaje global que otorgó y el puntaje global medio de ese hotel en ese mismo año. Considerá solo a los usuarios con al menos quince reseñas y dividilos en quintiles según el índice.

        Para cada quintil mostrá el rango del índice que abarca y, para cada tipo de viajero presente en él, la cantidad de usuarios, su participación dentro del quintil, un índice de sobrerrepresentación —participación en el quintil sobre participación en el total de usuarios analizados— y el puesto que ocupa dentro del quintil. Ordená por quintil y puesto.
        """)
    with st.container(border=True):
        st.code(query, language="sql", line_numbers=True)
    if st.button("Correr consulta", key="p6"):
        try:
            with st.spinner("Cargando consulta"):
                result = conn_supabase.table("pregunta5").select("*").limit(20).execute()
            st.table(result.data)
        except Exception as e:
            st.error(e)
