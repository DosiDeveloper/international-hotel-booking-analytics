import duckdb
import streamlit as st
from scipy import stats

st.set_page_config(page_title="Recomendador", page_icon="🎯", layout="wide")

PERFILES = {
    "Solo": "Solo",
    "Couple": "Pareja",
    "Business": "Negocios",
    "Family": "Familia",
}
DIMENSIONES = {
    "limpieza": "Limpieza",
    "confort": "Confort",
    "instalaciones": "Instalaciones",
    "ubicacion": "Ubicación",
    "personal": "Personal",
    "valor": "Calidad-precio",
}


@st.cache_resource
def init_connection():
    token = st.secrets["MOTHERDUCK_TOKEN"]

    return duckdb.connect(f"md:my_db?motherduck_token={token}")


@st.cache_data(ttl=3600)
def cargar_datos():
    query = """
        SELECT
            h.hotel_name,
            h.city,
            h.country AS hotel_country,
            h.star_rating,
            u.traveller_type AS user_type,
            u.country AS user_country,
            r.score_overall,
            r.score_cleanliness,
            r.score_comfort,
            r.score_facilities,
            r.score_location,
            r.score_staff,
            r.score_value_for_money
        FROM analytics.fact_reviews r
        JOIN analytics.dim_hotels h ON r.hotel_id = h.hotel_id
        JOIN analytics.dim_users u ON r.user_id = u.user_id
    """

    return init_connection().sql(query).df()


st.title("🎯 Recomendador de hoteles")
st.caption(
    "Combina el ranking bayesiano (objetivo 1) con el modelo de regresión "
    "(objetivo 3) para ordenar los hoteles según la percepción del perfil elegido."
)

df = cargar_datos()
df["perfil"] = df["user_type"].map(PERFILES).fillna(df["user_type"])
df["turismo"] = (df["user_country"] == df["hotel_country"]).map(
    {True: "Turismo Interno", False: "Turismo Receptivo"}
)

# --- filtros ---
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    perfil = st.selectbox("Perfil de viajero", ["Todos"] + sorted(df["perfil"].unique()))
with col_f2:
    turismo = st.selectbox("Modalidad", ["Todas", "Turismo Interno", "Turismo Receptivo"])
with col_f3:
    categorias = sorted(df["star_rating"].dropna().unique())
    categoria = st.selectbox("Categoría", ["Todas"] + [f"{int(c)} Estrellas" for c in categorias])
with col_f4:
    pais = st.selectbox("País del hotel", ["Todos"] + sorted(df["hotel_country"].unique()))

df_f = df
if perfil != "Todos":
    df_f = df_f[df_f["perfil"] == perfil]
if turismo != "Todas":
    df_f = df_f[df_f["turismo"] == turismo]
if categoria != "Todas":
    df_f = df_f[df_f["star_rating"] == int(categoria.split()[0])]
if pais != "Todos":
    df_f = df_f[df_f["hotel_country"] == pais]

if len(df_f) < 3:
    st.warning("No hay reseñas suficientes para los filtros seleccionados.")
    st.stop()

# --- modelo: percepcion de calidad-precio a partir de la calificacion general ---
modelo = stats.linregress(df_f["score_overall"], df_f["score_value_for_money"])

st.subheader("Modelo del perfil seleccionado")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Pendiente", f"{modelo.slope:,.3f}".replace(".", ","))
col_m2.metric("Intercepto", f"{modelo.intercept:,.3f}".replace(".", ","))
col_m3.metric("R cuadrado", f"{modelo.rvalue**2:,.3f}".replace(".", ","))
col_m4.metric("Valor P (pendiente)", f"{modelo.pvalue:.2e}")

calificacion_objetivo = st.slider(
    "Calificación general esperada del hotel:", 1.0, 10.0, 8.0, 0.1
)
proyeccion_objetivo = modelo.intercept + modelo.slope * calificacion_objetivo
st.info(
    f"Con una calificación general de **{calificacion_objetivo:.1f}**, el modelo "
    f"proyecta una percepción de calidad-precio de **{proyeccion_objetivo:.2f}** "
    f"para {perfil.lower() if perfil != 'Todos' else 'el conjunto filtrado'}."
)

# --- agregados por hotel + promedio bayesiano ---
resumen = (
    df_f.groupby(["hotel_name", "city", "hotel_country"])
    .agg(
        v=("score_overall", "size"),
        R=("score_overall", "mean"),
        proyectado=("score_overall", "mean"),
        limpieza=("score_cleanliness", "mean"),
        confort=("score_comfort", "mean"),
        instalaciones=("score_facilities", "mean"),
        ubicacion=("score_location", "mean"),
        personal=("score_staff", "mean"),
        valor=("score_value_for_money", "mean"),
    )
    .reset_index()
)

C = resumen["v"].quantile(0.50)
m = resumen["R"].mean()
resumen["bayesiano"] = (resumen["v"] * resumen["R"] + C * m) / (resumen["v"] + C)
resumen["proyectado"] = modelo.intercept + modelo.slope * resumen["R"]

criterios = {
    "Ranking bayesiano": "bayesiano",
    "Calidad-precio observada": "valor",
    "Calidad-precio proyectada": "proyectado",
}
col_c1, col_c2 = st.columns([2, 1])
with col_c1:
    etiqueta_criterio = st.selectbox("Criterio de ordenamiento", list(criterios))
with col_c2:
    top_n = st.slider("Hoteles a mostrar", 5, min(20, len(resumen)), 8)

columna_criterio = criterios[etiqueta_criterio]
ranking = resumen.sort_values(columna_criterio, ascending=False).reset_index(drop=True)

st.subheader(f"Ranking por {etiqueta_criterio.lower()}")
for posicion, fila in ranking.head(top_n).iterrows():
    col_nombre, col_datos, col_puntaje = st.columns([3, 2, 1])
    col_nombre.markdown(f"**{posicion + 1}. {fila['hotel_name']}**")
    col_nombre.caption(f"{fila['city']}, {fila['hotel_country']}")
    col_datos.caption(
        f"{fila['v']:,.0f} reseñas | promedio simple {fila['R']:.2f} | "
        f"bayesiano {fila['bayesiano']:.2f}".replace(",", ".")
    )
    col_puntaje.markdown(f"**{fila[columna_criterio]:.2f}**")
    st.progress(min(int(round(fila[columna_criterio] * 10)), 100))

# --- ficha del hotel ---
st.subheader("Ficha del hotel")
hotel = st.selectbox(
    "Elegir hotel",
    ranking["hotel_name"],
    index=0,
)
fila = ranking[ranking["hotel_name"] == hotel].iloc[0]

col_ficha1, col_ficha2 = st.columns([1, 2])
with col_ficha1:
    st.metric("Promedio bayesiano", f"{fila['bayesiano']:.2f}")
    st.metric("Promedio simple", f"{fila['R']:.2f}")
    st.metric("Calidad-precio proyectada", f"{fila['proyectado']:.2f}")
    st.caption(f"{fila['v']:,.0f} reseñas del perfil y filtros elegidos".replace(",", "."))

with col_ficha2:
    for columna, etiqueta in DIMENSIONES.items():
        st.caption(f"{etiqueta}: {fila[columna]:.2f}")
        st.progress(min(int(round(fila[columna] * 10)), 100))

with st.expander("📖 Cómo se construye la recomendación"):
    st.markdown(
        f"""
        1. **Ranking bayesiano:** el promedio de cada hotel se corrige hacia la media
        global ponderando por su volumen de reseñas, con lo que un hotel con pocas
        evaluaciones no lidera el ranking por azar.

        2. **Regresión lineal:** sobre las reseñas del perfil seleccionado se ajusta
        `calidad-precio = {modelo.slope:.3f} x calificación general + {modelo.intercept:.3f}`
        (R² = {modelo.rvalue**2:.3f}, p = {modelo.pvalue:.2e}). La calidad-precio
        proyectada de cada hotel usa su calificación general promedio.

        3. **Ordenamiento:** el criterio elegido define la posición final; las barras
        comparan cada hotel contra el máximo de la escala (10 puntos).

        **Limitaciones:** el modelo asume una relación lineal y predice la
        calidad-precio desde la calificación general (no al revés). Además, cada
        ciudad y cada país del conjunto tienen un único hotel y todos son de 5
        estrellas, por lo que el ranking de destinos y la comparación por categoría
        no aportan información en estos datos.
        """
    )
