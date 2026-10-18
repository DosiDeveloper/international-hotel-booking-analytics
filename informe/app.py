import streamlit as st

# barra
st.set_page_config(
    page_title="Recomendador y Ranking Hotelero",
    page_icon="🏨",
    layout="wide"
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

    st.subheader("Análisis")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        with st.container(border=True):
            st.markdown(f"### Ranking ({categoria})")
            st.caption("Comparativa entre promedio simple y corregido.")
            st.info("[Gráfico]")

    with col_g2:
        with st.container(border=True):
            st.markdown(f"### Percepción ({perfil_viajero})")
            st.caption("Diferencias según perfil de viajero y tipo de turismo.")
            st.success("[Gráfico]")

    st.write("")

    with st.container(border=True):
        st.markdown("### Recomendador por Similitud Vectorial")
        st.caption("Puntajes ponderados por preferencias de usuario.")
        st.info("[Gráfico]")


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