import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import scipy.stats as stats

st.set_page_config(
    page_title="Recomendador y Ranking Hotelero",
    page_icon="🏨",
    layout="wide"
)

MOTHERDUCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imp1ZWdvc2FuZ2VsckBnbWFpbC5jb20iLCJtZFJlZ2lvbiI6ImF3cy11cy1lYXN0LTEiLCJzZXNzaW9uIjoianVlZ29zYW5nZWxyLmdtYWlsLmNvbSIsInBhdCI6InZ4bmtaVkFwWFl3eTdRU2wyWkhCcWdQd2J4ZVFNYTlSZ1poQTFFWnQ3TDgiLCJ1c2VySWQiOiI2OGYyZmI0MS05YzhmLTRmMDItODgwMS1kYzMyMTVlZjQ4MmIiLCJpc3MiOiJtZF9wYXQiLCJyZWFkT25seSI6ZmFsc2UsInRva2VuVHlwZSI6InJlYWRfd3JpdGUiLCJpYXQiOjE3OTIyNzIzNjd9.URvhBHKmsMPblQtp-1Ky41hrupzP6_Df7SJ8dkGEvpc"

@st.cache_resource
def init_connection():
    return duckdb.connect(
        f"md:my_db?motherduck_token={MOTHERDUCK_TOKEN}"
        )

con = init_connection()


st.markdown("""
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
""", unsafe_allow_html=True)

# Sidebar
st.markdown("""
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
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Filtros")
    
    st.subheader("Perfil de Viajero:")
    perfil_viajero = st.selectbox(
        "Seleccionar perfil:", 
        ["Todos los perfiles", "Solo", "Pareja", "Familia", "Negocios"]
    )
    
    st.subheader("Modalidad de Turismo:")
    tipo_turismo = st.radio(
        "Tipo:", 
        ["Todos", "Turismo Interno", "Turismo Receptivo"]
    )
    
    st.subheader("Categoría:")
    categoria = st.selectbox(
        "Estrellas:", 
        ["Todas las categorías", "3 Estrellas", "4 Estrellas", "5 Estrellas"]
    )

# pestañas principales
tab_dashboard, tab_equipo = st.tabs(["📊 Dashboard Interactivo", "👥 Presentación del Equipo y Créditos"])


#pestaña 1 
with tab_dashboard:
    st.title("Dashboard: Recomendador y Ranking Hotelero")
    st.caption("Bosquejo visual interactivo para el análisis y recomendación de alojamientos.")

    st.markdown("---")

    st.subheader(f"Métricas para: {tipo_turismo} | {categoria}")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label=f"Total Evaluaciones ({perfil_viajero})", 
            value="0"
        )
    with col2:
        st.metric(
            label=f"Promedio Simple ({categoria})", 
            value="0.00"
        )
    with col3:
        st.metric(
            label=f"Promedio Bayesiano ({categoria})", 
            value="0.00"
        )
    with col4:
        st.metric(
            label="Factor Bayesiano", 
            value="0.0"
        )
    with col5:
        st.metric(
            label=" Desviación Ránking", 
            value="0"
        )

    st.markdown("---")

    st.warning(
        f" **Vista Seleccionada:** Perfil **{perfil_viajero}** | Modalidad **{tipo_turismo}** | Categoría **{categoria}**."
    )

    st.markdown("---")

    st.subheader("Análisis de Objetivos de Investigación")

    col_g1, col_g2 = st.columns(2)

    #objetivo 1
    with st.container(border=True):
        st.markdown("### 📊 Obj. 1: Ranking Bayesiano (Corrección por Volumen)")
        st.caption("Clasificación de hoteles basada en el promedio bayesiano.")
        
        try:
            query_o1 = """
                SELECT 
                    h.hotel_name,
                    COUNT(f.review_id) AS n_reviews,
                    AVG(f.score_overall) AS simple_avg
                FROM REVIEWS f
                JOIN HOTELES h ON f.hotel_id = h.hotel_id
                GROUP BY h.hotel_name
            """
            df_o1 = con.execute(query_o1).fetchdf()
            
            if not df_o1.empty:
                m = df_o1['simple_avg'].mean()
                C = 5
                df_o1['bayesian_avg'] = (C * m + df_o1['n_reviews'] * df_o1['simple_avg']) / (C + df_o1['n_reviews'])
                
                # Ordenamos para que los mejores hoteles queden arriba
                df_o1_top = df_o1.sort_values(by='bayesian_avg', ascending=True).tail(8)
                
                # Paleta exclusiva de tonos azules, rojos y naranjas
                paleta_pro = ["#0088BC", "#FF4B4B", "#FFA500", "#29B5E8", "#FF6C6C", "#FFB84D", "#005C8A", "#D32F2F"]
                
                fig_o1 = px.bar(
                    df_o1_top, 
                    y="hotel_name", 
                    x="bayesian_avg", 
                    orientation="h",
                    labels={"bayesian_avg": "Promedio Bayesiano", "hotel_name": "Hotel"},
                    color="hotel_name",
                    color_discrete_sequence=paleta_pro
                )
                
                fig_o1.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#FAFAFA', size=12),
                    margin=dict(t=20, b=20, l=20, r=20),
                    height=400,
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
                    yaxis=dict(showgrid=False),
                    showlegend=False
                )
                st.plotly_chart(fig_o1, use_container_width=True)
                st.info("💡 **Hallazgo:** El promedio bayesiano penaliza establecimientos con pocas reseñas, ofreciendo un ranking robusto y con una línea visual coherente.")
            else:
                st.warning("No se encontraron registros en la tabla REVIEWS.")
        except Exception as e:
            st.error(f"Error en Objetivo 1: {e}")



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
            st.image("https://via.placeholder.com/300", use_container_width=True)
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
                st.image("https://via.placeholder.com/300", use_container_width=True)
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
                st.image("https://via.placeholder.com/300", use_container_width=True)
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