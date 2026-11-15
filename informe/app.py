import duckdb
import numpy as np
import plotly.express as px
import streamlit as st
from scipy import stats

st.set_page_config(
    page_title="Recomendador y Ranking Hotelero", page_icon="🏨", layout="wide"
)


def z_asimetria_curtosis(serie):
    # z estandarizados: |z| <= 2 se considera desviacion trivial de la normalidad
    n = len(serie)
    asimetria = serie.skew()
    curtosis = serie.kurt()
    se_asimetria = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
    se_curtosis = 2 * se_asimetria * np.sqrt((n**2 - 1) / ((n - 3) * (n + 5)))
    return asimetria, curtosis, asimetria / se_asimetria, curtosis / se_curtosis


def fig_qq(datos, titulo):
    osm, osr = stats.probplot(datos, dist="norm")[0]
    fig = px.scatter(
        x=osm,
        y=osr,
        opacity=0.5,
        labels={"x": "Cuantiles teoricos", "y": "Cuantiles observados"},
        color_discrete_sequence=["#256fbe"],
    )
    extremos = np.polyfit(osm, osr, 1)
    fig.add_scatter(
        x=[osm.min(), osm.max()],
        y=np.polyval(extremos, [osm.min(), osm.max()]),
        mode="lines",
        name="Referencia normal",
        line=dict(color="#ec6f0f", width=2),
    )
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=13)),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FAFAFA", size=11),
        margin=dict(t=35, b=10, l=10, r=10),
        height=280,
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
    )
    return fig


def breusch_pagan(x, residuos):
    # auxiliar: residuos al cuadrado sobre X; LM = n * R2_aux ~ chi2(1)
    x = np.asarray(x, dtype=float)
    residuos2 = np.asarray(residuos, dtype=float) ** 2
    ajuste = np.polyval(np.polyfit(x, residuos2, 1), x)
    ss_res = np.sum((residuos2 - ajuste) ** 2)
    ss_tot = np.sum((residuos2 - residuos2.mean()) ** 2)
    r2_aux = 1 - ss_res / ss_tot
    lm = len(x) * r2_aux
    p_valor = stats.chi2.sf(lm, df=1)
    return lm, p_valor


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
            <div class="main-title">Bienvenidos a...</div>
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
tab_obj1, tab_obj2, tab_obj3, tab_equipo = st.tabs(
    ["📊 Ranking Bayesiano", "Percepcion calidad-precio", "Regresion lineal", "👥 Presentación del Equipo y Créditos"]
)


# pestaña 1
with tab_obj1:
    st.title("Ranking bayesiano")
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
            FROM analytics.fact_reviews r
            JOIN analytics.dim_hotels h ON r.hotel_id = h.hotel_id
            JOIN analytics.dim_users u ON r.user_id = u.user_id
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
            col1.metric(label=f"Total Eval. ({perfil_viajero})",value=f"{total_evaluaciones:,.0f}".replace(',', '.'),)

            col2.metric(label="Prom. Simple",value=f"{promedio_simple_global:,.2f}".replace('.', ','))
        
            col3.metric(label="Prom. Bayesiano", value=f"{promedio_bayesiano_global:,.2f}".replace('.', ','))

            col4.metric(label="Factor (C)",value=f"{C:,.1f}".replace('.', ','))

            col5.metric(label="Desviación Ránking",value=f"{desviacion_ranking:,.2f}".replace('.', ','))
            

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

                fig_o1.update_xaxes(range=[8.5, 9.05])
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

    except Exception as e:
        st.error(f"Ocurrió un error en el procesamiento: {e}")
        
with tab_obj2:
        # para el objetivo 2 (percecpcion calidad-precio)
        st.title("Percepcion calidad-precio")
        st.markdown("---")
        st.subheader("Percepción de Calidad-Precio")

        usuarios_percepcion = """
            SELECT
                u.traveller_type,
                u.age_group,
                h.star_rating AS hotel_category,
                u.country AS user_country,
                h.country AS hotel_country,
                r.score_value_for_money
            FROM analytics.fact_reviews r
            JOIN analytics.dim_hotels h ON r.hotel_id = h.hotel_id
            JOIN analytics.dim_users u ON r.user_id = u.user_id
        """
        df_obj2 = con.sql(usuarios_percepcion).df()

        traduccion = {'Solo': 'Solo', 'Couple': 'Pareja', 'Business': 'Negocios', 'Family': 'Familia'}
        df_obj2['traveller_type'] = df_obj2['traveller_type'].map(traduccion).fillna(df_obj2['traveller_type'])

        # variable derivada para el contraste interno vs. receptivo del objetivo 2
        df_obj2["turismo"] = np.where(
            df_obj2["user_country"] == df_obj2["hotel_country"],
            "Turismo Interno",
            "Turismo Receptivo",
        )

        if df_obj2 is not None and not df_obj2.empty:
            # grafico
            fig2 = px.box(
                df_obj2,
                x="traveller_type",
                y="score_value_for_money",
                color="traveller_type",
                color_discrete_sequence=["#256fbe", "#ec6f0f", "#d10909", "#2A812A"],
                labels={
                    "traveller_type": "Perfil de Viajero",
                    "score_value_for_money": "Calidad-Precio (Puntuación)"
                }
            )
            fig2.update_layout(
                xaxis_title="Perfil de Viajero",
                yaxis_title="Calidad-Precio (Puntuación)"
            )
            st.plotly_chart(fig2, use_container_width=True)

            segmentaciones = {
                "Tipo de viajero": "traveller_type",
                "Grupo etario": "age_group",
                "Turismo interno vs. receptivo": "turismo",
                "Categoría del hotel": "hotel_category",
            }
            sele_segmentacion = st.selectbox(
                "Segmentar la prueba de hipótesis por:",
                list(segmentaciones.keys()),
            )
            columna_seg = segmentaciones[sele_segmentacion]

            if columna_seg == "hotel_category":
                etiquetas = df_obj2[columna_seg].map(lambda v: f"{int(v)} Estrellas")
            else:
                etiquetas = df_obj2[columna_seg].astype(str)

            tipos = etiquetas.dropna().unique()
            grupos = [
                df_obj2.loc[etiquetas == t, "score_value_for_money"].dropna()
                for t in tipos
            ]

            if len(tipos) < 2:
                st.info(
                    f"La segmentación por **{sele_segmentacion.lower()}** no es "
                    "aplicable con los datos actuales: la variable es constante "
                    f"({', '.join(tipos)}), por lo que no existen grupos que comparar."
                )
            else:
                #validacion de supuestos
                with st.expander("🔍 Verificación de Supuestos Estadísticos"):
                    st.markdown("Para determinar si se debe aplicar una prueba parametrica o no paramétrica, evaluamos los supuestos clave:")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**1. Normalidad práctica de los grupos**")
                        st.caption(
                            "Asimetría y curtosis estandarizadas ($|z| \\le 2$ indica desviación "
                            "trivial). Con n grande, los p-valores de normalidad detectan "
                            "desviaciones sin relevancia práctica."
                        )

                        desviaciones_relevantes = []
                        for t, g in zip(tipos, grupos):
                            if len(g) >= 8:
                                asim, curt, z_asim, z_curt = z_asimetria_curtosis(g)
                                st.text(
                                    f"• {t}: asimetría z = {z_asim:+.2f} | "
                                    f"curtosis z = {z_curt:+.2f}"
                                )
                                if abs(z_asim) > 2 or abs(z_curt) > 2:
                                    desviaciones_relevantes.append(t)

                        if not desviaciones_relevantes:
                            st.success(
                                "✅ Asimetría y curtosis compatibles con normalidad práctica "
                                "en todos los grupos."
                            )
                        else:
                            st.warning(
                                "⚠️ Desviación no trivial en: "
                                + ", ".join(desviaciones_relevantes)
                                + ". Junto con la escala ordinal y acotada de los datos, "
                                "esto respalda el uso de Kruskal-Wallis."
                            )

                    with col2:
                        st.markdown("**2. Homogeneidad de Varianzas**")
                        st.caption("Prueba de Levene para homocedasticidad")

                        stat_lev, p_lev = stats.levene(*grupos)
                        st.metric(label="Estadístico de Levene", value=f"{stat_lev:.4f}")
                        st.metric(label="p-valor (Levene)", value=f"{p_lev:.5f}")

                        if p_lev > 0.05:
                            st.success("✅ Se cumple la homocedasticidad (varianzas iguales).")
                        else:
                            st.warning("⚠️ Las varianzas son heterogéneas ($p \\le 0.05$).")

                    st.caption(
                        "Kruskal-Wallis se justifica por diseño: la variable es una escala "
                        "ordinal, discreta y acotada entre 1 y 10, más allá del resultado de "
                        "las pruebas de normalidad."
                    )

                #prueba de hipotesis
                st.markdown(f"### Resultado: {sele_segmentacion}")
                h_stat, p_val = stats.kruskal(*grupos)

                # tamano de efecto epsilon cuadrado (Tomczak y Tomczak, 2014)
                n_total = sum(len(g) for g in grupos)
                epsilon2 = h_stat / ((n_total**2 - 1) / (n_total + 1))
                if epsilon2 >= 0.14:
                    magnitud = "grande"
                elif epsilon2 >= 0.06:
                    magnitud = "mediano"
                elif epsilon2 >= 0.01:
                    magnitud = "pequeño"
                else:
                    magnitud = "despreciable"

                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.metric(label="Estadístico H (Kruskal-Wallis)", value=f"{h_stat:.4f}")
                with col_res2:
                    st.metric(label="Valor P", value=f"{p_val:.5f}")
                with col_res3:
                    st.metric(label="Tamaño del efecto (ε²)", value=f"{epsilon2:.4f}")

                if p_val < 0.05:
                    st.success(
                        "**Conclusión:** Sí existen diferencias estadísticamente "
                        f"significativas en la percepción de calidad-precio según "
                        f"{sele_segmentacion.lower()} ($p < 0.05$). Rechazamos la "
                        f"hipótesis nula; el tamaño del efecto es **{magnitud}** "
                        f"(ε² = {epsilon2:.4f})."
                    )
                else:
                    st.info(
                        "**Conclusión:** No se encuentran diferencias estadísticamente "
                        f"significativas en la percepción de calidad-precio según "
                        f"{sele_segmentacion.lower()} ($p \\ge 0.05$); el tamaño del "
                        f"efecto es {magnitud} (ε² = {epsilon2:.4f})."
                    )

        else:
            st.warning("No se encontraron datos de calidad-precio para realizar la prueba.")

with tab_obj3:
    # para el objetivo 3 (regresion lineal y proyeccion calidad-precio)
    st.title("Regresion lineal")
    st.markdown("---")
    st.subheader("Regresion lineal simple: calificacion general vs percepcion calidad-precio")

    st.caption(
        "Modelo que proyecta la percepcion de calidad-precio esperada de un hotel "
        "a partir de su calificacion general."
    )

    try:
        query_obj3 = """
            SELECT
                h.star_rating AS hotel_category,
                h.country AS hotel_country,
                u.traveller_type AS user_type,
                u.country AS user_country,
                r.score_overall,
                r.score_value_for_money
            FROM analytics.fact_reviews r
            JOIN analytics.dim_hotels h ON r.hotel_id = h.hotel_id
            JOIN analytics.dim_users u ON r.user_id = u.user_id
        """
        df_obj3 = con.sql(query_obj3).df()

        # mismos filtros de la vista, para coherencia con los objetivos 1 y 2
        if perfil_viajero != "Todos los perfiles":
            df_obj3 = df_obj3[df_obj3["user_type"] == perfil_viajero]

        if categoria != "Todas las categorías":
            estrellas = int(categoria.split()[0])
            df_obj3 = df_obj3[df_obj3["hotel_category"] == estrellas]

        if tipo_turismo == "Turismo Interno":
            df_obj3 = df_obj3[df_obj3["user_country"] == df_obj3["hotel_country"]]
        elif tipo_turismo == "Turismo Receptivo":
            df_obj3 = df_obj3[df_obj3["user_country"] != df_obj3["hotel_country"]]

        df_obj3 = df_obj3.dropna(subset=["score_overall", "score_value_for_money"])

        if df_obj3 is not None and not df_obj3.empty:
            x = df_obj3["score_overall"]
            y = df_obj3["score_value_for_money"]

            # modelo de regresion lineal simple
            regresion = stats.linregress(x, y)
            r2 = regresion.rvalue ** 2

            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            col_r1.metric(
                label="Pendiente",
                value=f"{regresion.slope:,.4f}".replace(".", ","),
            )
            col_r2.metric(
                label="Intercepto",
                value=f"{regresion.intercept:,.4f}".replace(".", ","),
            )
            col_r3.metric(
                label="R cuadrado",
                value=f"{r2:,.4f}".replace(".", ","),
            )
            col_r4.metric(
                label="Valor P (pendiente)",
                value=f"{regresion.pvalue:.2e}",
            )

            st.info(
                f"**Modelo:** Percepcion calidad-precio es aproximada con "
                f"{regresion.slope:,.4f} x Calificacion general + {regresion.intercept:,.4f}"
            )

            # grafico de dispersion con la recta de regresion
            if len(df_obj3) > 5000:
                df_plot = df_obj3.sample(5000, random_state=42)
            else:
                df_plot = df_obj3

            fig3 = px.scatter(
                df_plot,
                x="score_overall",
                y="score_value_for_money",
                opacity=0.4,
                labels={
                    "score_overall": "Calificacion General",
                    "score_value_for_money": "Calidad-Precio (Puntuacion)",
                },
                color_discrete_sequence=["#256fbe"],
            )

            x_line = np.linspace(
                df_obj3["score_overall"].min(), df_obj3["score_overall"].max(), 100
            )
            y_line = regresion.intercept + regresion.slope * x_line
            fig3.add_scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="Regresion lineal",
                line=dict(color="#ec6f0f", width=3),
            )

            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FAFAFA", size=12),
                margin=dict(t=20, b=20, l=20, r=20),
                height=450,
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig3, use_container_width=True)

            # verificacion de supuestos de la regresion
            with st.expander("🔍 Verificación de Supuestos de la Regresion"):
                st.markdown(
                    "Para confiar en la proyeccion evaluamos los supuestos clave del modelo:"
                )
                col_s1, col_s2 = st.columns(2)

                residuos = y - (regresion.intercept + regresion.slope * x)

                with col_s1:
                    st.markdown("**1. Normalidad práctica de los residuos**")
                    st.caption(
                        "Asimetría y curtosis estandarizadas ($|z| \\le 2$ = desviación "
                        "trivial); QQ-plot y Shapiro-Wilk como apoyo."
                    )
                    if len(residuos) >= 8:
                        asim, curt, z_asim, z_curt = z_asimetria_curtosis(residuos)
                        st.text(
                            f"Asimetría z = {z_asim:+.2f} | Curtosis z = {z_curt:+.2f}"
                        )
                        _, p_res = stats.shapiro(
                            residuos.sample(
                                min(len(residuos), 4000), random_state=42
                            )
                        )
                        st.metric(
                            label="p-valor (Shapiro, n = 4,000)", value=f"{p_res:.2e}"
                        )
                        if abs(z_asim) <= 2 and abs(z_curt) <= 2:
                            st.success(
                                "✅ Desviación trivial de la normalidad: la proyección "
                                "puntual es razonable."
                            )
                        else:
                            st.warning(
                                "⚠️ Desviación no trivial (asimetría o colas): usar la "
                                "proyección como ordenamiento relativo."
                            )
                        st.plotly_chart(
                            fig_qq(
                                residuos.sample(
                                    min(len(residuos), 5000), random_state=42
                                ),
                                "QQ-plot de los residuos",
                            ),
                            use_container_width=True,
                        )

                with col_s2:
                    st.markdown("**2. Homocedasticidad (Breusch-Pagan)**")
                    st.caption(
                        "Regresión auxiliar de los residuos al cuadrado sobre X; "
                        "$p > 0.05$ indica varianza constante."
                    )
                    lm_bp, p_bp = breusch_pagan(x, residuos)
                    st.metric(
                        label="Estadístico LM",
                        value=f"{lm_bp:,.2f}".replace(".", ","),
                    )
                    st.metric(label="p-valor (Breusch-Pagan)", value=f"{p_bp:.2e}")
                    if p_bp > 0.05:
                        st.success("✅ No se detecta heterocedasticidad.")
                    else:
                        st.warning(
                            "⚠️ Heterocedasticidad detectada: los errores estándar y "
                            "los valores p del modelo no son exactos."
                        )

                    st.markdown("**3. Significancia de la relación**")
                    st.caption("Test de significancia de la pendiente del modelo")
                    if regresion.pvalue < 0.05:
                        st.success(
                            "✅ La relación es estadísticamente significativa ($p < 0.05$)."
                        )
                    else:
                        st.warning(
                            "⚠️ No hay evidencia de relación lineal significativa ($p \\ge 0.05$)."
                        )

            st.markdown("---")
            st.markdown("### Proyeccion de Calidad-Precio")
            st.caption(
                "Ingresa una calificacion general esperada y el modelo proyecta la "
                "percepcion de calidad-precio asociada."
            )
            calificacion_proyectada = st.slider(
                "Calificacion general esperada del hotel:",
                min_value=1.0,
                max_value=10.0,
                value=8.0,
                step=0.1,
            )
            prediccion = regresion.intercept + regresion.slope * calificacion_proyectada
            st.metric(
                label="Percepcion calidad-precio proyectada",
                value=f"{prediccion:,.2f}".replace(".", ","),
            )
            if not (
                df_obj3["score_overall"].min()
                <= calificacion_proyectada
                <= df_obj3["score_overall"].max()
            ):
                st.warning(
                    "⚠️ La calificacion proyectada esta fuera del rango observado en los datos; "
                    "la estimacion es una extrapolacion."
                )

        else:
            st.warning("No se encontraron datos para construir la regresion lineal.")

    except Exception as e:
        st.error(f"Ocurrió un error en la regresion: {e}")

# pestaña 3  presentacion de nuestro equipo
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
