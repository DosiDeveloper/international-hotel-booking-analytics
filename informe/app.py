import duckdb
import plotly.express as px
import streamlit as st
from scipy import stats

st.set_page_config(
    page_title="Recomendador y Ranking Hotelero", page_icon="🏨", layout="wide"
)


def render_bloque_principal():
    hero_html = """
    <style>
    .welcome-container {
        background: linear-gradient(135deg, #383838 0%, #2b2b2b 100%);
        padding: 60px 20px;
        border-radius: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        border-left: 5px solid #f39c12;
    }

    .glass-card {
        background: rgba(40, 40, 40, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 40px 50px;
        max-width: 850px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    .eyebrow {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #f39c12;
        margin-bottom: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 24px;
        color: #ffffff;
        line-height: 1.2;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .description {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #d1d5db;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 0;
    }
    </style>

    <div class="welcome-container">
        <div class="glass-card">
            <div class="eyebrow">Dashboard</div>
            <div class="main-title">Bienvenidos a el analisis de rankings hoteleros</div>
            <div class="description">
                Aqui pondriamos.... (por definir)
            </div>
        </div>
    </div>
    """

    st.markdown(hero_html, unsafe_allow_html=True)


render_bloque_principal()


@st.cache_resource
def init_connection():
    token = st.secrets["MOTHERDUCK_TOKEN"]

    return duckdb.connect(f"md:my_db?motherduck_token={token}")


con = init_connection()


st.markdown(
    """
    <style>
    /* efecto flotante de las columnas */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important;
    }


    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-6px) !important;
        box-shadow: 0 12px 24px rgba(0, 136, 188, 0.25) !important;
        border-color: #0088BC !important;
    }

    /* fotos */
    div[data-testid="stImage"] img {
        border-radius: 10px !important;
        object-fit: cover !important;
        aspect-ratio: 1 / 1 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar
st.markdown(
    """
    <style>
    /* menu */
    [data-testid="stSidebarNav"]::before {
        content: " Menú ";
        font-size: 1.25rem;
        font-weight: bold;
        color: #FFFFFF;
        display: block;
        padding: 1rem 0rem 0.5rem 0.5rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Filtros")

    st.subheader("Perfil de Viajero:")
    perfil_viajero = st.selectbox(
        "Seleccionar perfil:",
        ["Todos los perfiles", "Solo", "Pareja", "Familia", "Negocios"],
    )

    st.subheader("Modalidad de Turismo:")
    tipo_turismo = st.radio("Tipo:", ["Todos", "Turismo Interno", "Turismo Receptivo"])

    st.subheader("Categoría:")
    categoria = st.selectbox(
        "Estrellas:",
        ["Todas las categorías", "3 Estrellas", "4 Estrellas", "5 Estrellas"],
    )

# pestañas principales
tab_dashboard, tab_equipo = st.tabs(
    ["📊 Dashboard Interactivo", "👥 Presentación del Equipo y Créditos"]
)


# pestaña 1
with tab_dashboard:
    st.title("Dashboard: Recomendador y Ranking Hotelero")
    st.caption(
        "Bosquejo visual interactivo para el análisis y recomendación de alojamientos."
    )
    st.markdown("---")

    try:
        query = """
            SELECT
                h.hotel_name,
                h.star_rating AS hotel_category,
                h.country AS hotel_country,
                u.traveller_type AS user_type,
                u.country AS user_country,
                r.score_overall
            FROM 'data/clean/reviews_limpio.csv' r
            JOIN 'data/clean/hotels_limpio.csv' h ON r.hotel_id = h.hotel_id
            JOIN 'data/clean/users_limpio.csv' u ON r.user_id = u.user_id
        """
        df_raw = con.sql(query).df()

        if perfil_viajero != "Todos los perfiles":
            df_raw = df_raw[df_raw["user_type"] == perfil_viajero]

        if categoria != "Todas las categorías":
            estrellas = int(categoria.split()[0])
            df_raw = df_raw[df_raw["hotel_category"] == estrellas]

        if tipo_turismo == "Turismo Interno":
            df_raw = df_raw[df_raw["user_country"] == df_raw["hotel_country"]]
        elif tipo_turismo == "Turismo Receptivo":
            df_raw = df_raw[df_raw["user_country"] != df_raw["hotel_country"]]

        st.subheader(f"Métricas para: {tipo_turismo} | {categoria}")

        if df_raw is not None and not df_raw.empty:
            df_stats = (
                df_raw.groupby("hotel_name")
                .agg(v=("score_overall", "count"), R=("score_overall", "mean"))
                .reset_index()
            )

            m = df_stats["R"].mean()
            C = df_stats["v"].quantile(0.50)

            df_stats["bayesian_avg"] = ((df_stats["v"] * df_stats["R"]) + (C * m)) / (
                df_stats["v"] + C
            )

            total_evaluaciones = df_stats["v"].sum()
            promedio_simple_global = m
            promedio_bayesiano_global = df_stats["bayesian_avg"].mean()
            desviacion_ranking = (df_stats["R"] - df_stats["bayesian_avg"]).abs().mean()

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric(
                label="Total Eval. ({perfil_viajero})",
                value=f"{total_evaluaciones:,.0f}",
            )
            col2.metric(label="Prom. Simple", value=f"{promedio_simple_global:.2f}")
            col3.metric(
                label="Prom. Bayesiano", value=f"{promedio_bayesiano_global:.2f}"
            )
            col4.metric(label="Factor (C)", value=f"{C:.1f}")
            col5.metric(label="Desviación Ránking", value=f"{desviacion_ranking:.2f}")

            st.markdown("---")
            st.warning(
                f" **Vista Seleccionada:** Perfil **{perfil_viajero}** | Modalidad **{tipo_turismo}** | Categoría **{categoria}**."
            )
            st.markdown("---")

            st.subheader("Análisis de Objetivos de Investigación")
            with st.container(border=True):
                st.markdown("### Ranking Bayesiano Interactivo")
                st.caption(
                    "Clasificación de hoteles penalizando el bajo volumen de evaluaciones frente al promedio simple."
                )

                col_filtros1, col_filtros2 = st.columns(2)
                with col_filtros1:
                    top_n = st.slider(
                        "Numero de hoteles a mostrar :",
                        min_value=5,
                        max_value=20,
                        value=8,
                        step=1,
                    )
                with col_filtros2:
                    st.write("")
                    mostrar_tabla = st.toggle("Mostrar tablla detallada")

                df_top = df_stats.sort_values(by="bayesian_avg", ascending=True).tail(
                    top_n
                )

                fig_o1 = px.bar(
                    df_top,
                    y="hotel_name",
                    x="bayesian_avg",
                    orientation="h",
                    hover_data={"R": ":.2f", "v": True, "bayesian_avg": ":.2f"},
                    labels={
                        "bayesian_avg": "Prom. Bayesiano",
                        "hotel_name": "Hotel",
                        "R": "Promedio Simple",
                        "v": "Total de Reseñas",
                    },
                    color="bayesian_avg",
                    color_continuous_scale="Oryel",
                )

                fig_o1.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#FAFAFA", size=12),
                    margin=dict(t=20, b=20, l=20, r=20),
                    height=450,
                    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
                    yaxis=dict(showgrid=False),
                    coloraxis_showscale=False,
                )

                st.plotly_chart(fig_o1, width="stretch")

                if mostrar_tabla:
                    st.markdown("#### Desglose Estadístico")
                    df_tabla = df_top.sort_values(by="bayesian_avg", ascending=False)[
                        ["hotel_name", "v", "R", "bayesian_avg"]
                    ]
                    df_tabla.columns = [
                        "Nombre del Hotel",
                        "Volumen de Reseñas",
                        "Promedio Simple",
                        "Promedio Bayesiano",
                    ]
                    st.dataframe(df_tabla, width="stretch", hide_index=True)

        else:
            st.warning(
                "No se encontraron registros para la combinación de filtros seleccionada."
            )

        # para el objetivo 2 (percecpcion calidad'precio)
        st.markdown("---")
        st.subheader("Objetivo 2: Percepción de Calidad-Precio")

        usuarios_percepcion = """
            SELECT u.traveller_type, r.score_value_for_money
            FROM 'data/clean/reviews_limpio.csv' r
            JOIN 'data/clean/users_limpio.csv' u ON r.user_id = u.user_id
            WHERE r.score_value_for_money IS NOT NULL
        """
        df_obj2 = con.sql(usuarios_percepcion).df()

        if df_obj2 is not None and not df_obj2.empty:
            fig2 = px.box(
                df_obj2,
                x="traveller_type",
                y="score_value_for_money",
                color="traveller_type",
            )
            st.plotly_chart(fig2, width="stretch")

            tipos = df_obj2["traveller_type"].unique()
            grupos = [
                df_obj2[df_obj2["traveller_type"] == t]["score_value_for_money"]
                for t in tipos
            ]

            h_stat, p_val = stats.kruskal(*grupos)

            st.write(f"**Valor P (Kruskal-Wallis):** {p_val:.5f}")

            if p_val < 0.05:
                st.success(
                    "Conclusión: Sí hay diferencias significativas en cómo califican la calidad-precio los distintos viajeros."
                )
            else:
                st.info(
                    "Conclusión: No hay diferencias significativas entre los viajeros."
                )
        else:
            st.warning(
                "No se encontraron datos de calidad-precio para realizar la prueba."
            )

    except Exception as e:
        st.error(f"Error en el procesamiento de datos: {e}")

# pestaña 2 / presentacion del equipo
with tab_equipo:
    st.title("Equipo de investigación y recomendación hotelera")
    st.subheader("Comité de desarrollo y algoritmos de recomendación")
    st.write("trivago de temu")

    st.markdown("---")

    st.markdown("### Integrantes del grupo:")

    # douglas
    with st.container(border=True):
        c_img, c_txt = st.columns([1, 3])
        with c_img:
            st.image("imagenes/douglas.jpg", use_container_width=True)
        with c_txt:
            st.markdown("### Douglas Barreto")
            st.caption("**Rol:** ...")
            st.markdown("""
            **Encargado de:**
            * ..
            * ..
            * ..
            """)

    st.write("")

    # eymi
    with st.container(border=True):
        c_img, c_txt = st.columns([1, 3])
        with c_img:
            st.image("imagenes/eymi2.jpg", use_container_width=True)
        with c_txt:
            st.markdown("### Eymi Borjas")
            st.caption("**Rol:** ...")
            st.markdown("""
            **Encargado de:**
            * ..
            * ..
            * ..
            """)

    st.write("")

    # angel
    with st.container(border=True):
        c_img, c_txt = st.columns([1, 3])
        with c_img:
            st.image("https://via.placeholder.com/300", width="stretch")
        with c_txt:
            st.markdown("### Angel Reina")
            st.caption("**Rol:** ...")
            st.markdown("""
            **Encargado de:**
            * ..
            * ..
            * ..
            """)

    st.write("")

    # andres
    with st.container(border=True):
        c_img, c_txt = st.columns([1, 3])
        with c_img:
            st.image("https://via.placeholder.com/300", width="stretch")
        with c_txt:
            st.markdown("### Andres Ortega")
            st.caption("**Rol:** ...")
            st.markdown("""
                **Encargado de:**
                * ..
                * ..
                * ..
                """)

    st.write("")

    # gabriel
    with st.container(border=True):
        c_img, c_txt = st.columns([1, 3])
        with c_img:
            st.image("https://via.placeholder.com/300", width="stretch")
        with c_txt:
            st.markdown("### Gabriel Guevara")
            st.caption("**Rol:** ...")
            st.markdown("""
                **Encargado de:**
                * ..
                * ..
                * ..
                """)

    st.markdown("---")
