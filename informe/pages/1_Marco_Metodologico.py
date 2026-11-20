.import streamlit as st
import pandas as pd

st.title("Marco Metodológico")
st.caption("Diseño de investigación, arquitectura analítica y procedimientos estadísticos aplicados sobre el conjunto de purado de reseñas hoteleras (data/clean).")

st.header("1. Enfoque y Diseño de la Investigación")
st.write(
  "El estudio se desarrolla bajo un enfoque cuantitativo de carácter obsrvacional, descriptivo, comparativo y correlacional/regresivo, aplicado a datos de reseñas y reservas"
  "hoteleras medidas en una escala de 1 a 10. El análisis se sustenta sobre la base depurada (data/clean), conformada por 49.993 reseñas, 25 hoteles (con cobertura de un"
  "establecimiento por ciudad y país) y 2.000 usuarios."
)
st.write(
  "La estructura analítica aborda los datos a nivel global, por conglomerado de hotel (25 agrupaciones) y mediante segmentaciones clave según el perfil de viajero (Solo," 
  "Pareja, Familia y Negocios), la modalidad de turismo (Todos, Turismo Interno y Turismo Receptivo) y la categoría de alojamiento por estrellas."
)

st. subheader("Nota sobre el alcance geográfico")
st.info(
  "Dado que el mapa de ubicación describe la distribución espacial de los 25 establecimientos (un hotel por ciudad y país) y no múltiples hoteles dentro de un mismo destino,"
  "su alcance es descriptivo de la cobertura muestral y no permite estimar un efecto geográfico causal entre ciudades o paises."
)

st.subheader("Resumen de dimensiones metodológicas")
data = {
  "Dimensión Metodológica": [
    "Enfoque y diseño",
    "Base analítica (data/clean)",
    "Variables principales",
    "Criterios de segmentación"
  ],
  "Especificación en el Estudio": [
    "Cuantitativo observacional; descriptivo; comparativo y correlacional/regresivo.",
    "49.993 reseñas limpias, 25 hoteles (conglomerados) y 2.000 usuarios.",
    "Calificación general (X, escala 1-10) y calidad-precio percibida (Y, escala 1-10).",
    "Perfil de viajero (Solo, Pareja, Familia, Negocios), modalidad turística y estrellas."
  ]
}
df = pd.DataFrame(data)
st.table(df)

st.header("2. Preparación de Datos, Arquitectura Analítica y Visualización")
st.write(
  "El flujo de trabajo técnico abarca desde la depuración y estructuración relacional/dimensional hasta el despliegue de interfaces interactivas de consulta y simulación."
)

st.markdown("""
- **Limpieza y estructuración dimensional:** Se parte de los registros depurados (data/clean, n = 49.993) organizados en un esquema analítico en estrella que integra la tabla 
de hechos de evaluaciones (FACT_REVIEWS) con las tablas de dimensiones de hoteles (DIM_HOTELS), usuarios (DIM_USERS) y tiempo (DIM_TIEMPO), además de las tablas de resultados 
de modelos y simulación.
- **Procesamiento y aplicación web en Streamlit:** El procesamiento de datos y cálculos estadísticos se apoya en Python, SQLite3 y DuckDB / MotherDuck, exponiendo los resultados 
en una aplicación multi página en Streamlit con filtros dinámicos por perfil de viajero, modalidad turística y categoría.
- **Dashboard interactivo en PowerBI:** Se desarroló un informe de inteligencia de negocios compuesto por cuatro páginas (Portada/Rankings Hoteleros, Ranking y Bayes, Perfil y
Modelado, Modelado Predictivo) con navegación interna y segmentadores temporales y demográficos para contrastar rankings, evaluar percepciones por segmento y operar el simulador predictivo.
""")


