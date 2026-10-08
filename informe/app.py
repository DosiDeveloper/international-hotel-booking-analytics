import streamlit as st

# 1. Configuración de pantalla ancha
st.set_page_config(
    page_title="Recomendador y Ranking Hotelero",
    page_icon="🏨",
    layout="wide"
)

##barra con letras blancas
st.markdown("""
    <style>
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="select"] div {
        color: #0088BC !important;
        font-weight: bold !important;
    }

    
    [data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: #0088BC !important;
    }

    div[role="listbox"] div {
        color: #111827 !important;
    }
    </style>
""", unsafe_allow_html=True)


#sidebar
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
    
    st.markdown("---")
    st.caption("🔵 Proyecto de Recomendación y Ranking Hotelero")

#cuerpo del dashboard

st.title("Dashboard: Recomendador y Ranking Hotelero")
st.caption("Bosquejo visual interactivo para el análisis y recomendación de alojamientos.")

st.markdown("---")

#el tttulo del bloque cambia dinámicamente segun la categoria y el turismo seleccionado
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

#caja informativa dinnmica
st.warning(
    f"🟡 **Vista Seleccionada:** Perfil **{perfil_viajero}** | Modalidad **{tipo_turismo}** | Categoría **{categoria}**."
)

st.markdown("---")

#Análisis
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