import streamlit as st
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

st.subheader("Nota sobre el alcance geográfico")
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

st.header("3. Procedimientos Estadísticos por objetivo")

st.subheader("3.1 Ranking Bayesiano frente a Promedio Simple")
st.write(
  "Para evitar que establecimientos con un volumen reducido de reseñas distorsionen las posiciones frente a hoteles con un historial amplio y consistente de evaluaciones,"
  "se implementa el puntaje ponderado bayesiano (WR):"
)
st.latex(r"WR = \frac{v}{v + C} \cdot R + \frac{C}{v + C} \cdot m")
st.markdown("""
- **R:** Promedio aritmético simple del hotel.
- **v:** Número total de reseñas registradas para ese establecimiento.
- **m:** Promedio global de calificaciones de referencia en el conjunto de datos.
- **C:** Factor de confianza o umbral mínimo de ponderación (por ejemplo, C = 1.720,0 en la vista general).
""")
st.write(
  "los puntajes bayesianos obtenidos se contrastan directamente contra el promedio aritmético simple para identificar el reordenamiento de los hoteles y cuantificar la"
  "desviación de ranking generada por la penalización estadística del bajo volumen muestral."
)

st.subheader("3. Diferencias en Calidad-Precio entre Perfiles (Prueba de Kruskal-Wallis)")
st.write(
  "Con el propósito de determinar si la percepción de la relación calidad-precio varía de manera significativa entre los distintos perfiles de viajeros (Solo, Pareja, Negocio"
  "y Familia) y segmentos seleccionados:"
)
st.markdown("""
- **Exploración distribucional y supuestos:** Se examina el comportamiento de las puntuaciones de calidad-precio mediante diagramas de caja y bigotes (medianas, rangos 
intercuartílicos y valores extremos) y se verifican los supuestos de normalidad y homogeneidad de varianzas.
- **Contraste no paramétrico:** Ante la presencia de asimetrías, discretiación de escala y grandes tamaños muestrales, se aplica la prueba no paramétrica de Kruskal-Wallis 
(obteniendo un estadístico H = 24.650,8474 con p < 0,05 en la vista general), rechazando la hipótesis nula de igualdad de distribuciones entre perfiles.
""")

st.subheader("3.3 Regresión Lineal Simple, Correlación e Inferencia Robusta")
st.write(
  "Para cuantificar la relación funcional entre la calificación general del alojamiento (X, variable predictora) y la calidad-precio percibida (Y, variable dependiente),"
  "se ejecuta un protocolo estadístico en cuatro etapas:"
)
st.markdown("""
- **Estimación por Mínimos Cuadrados Ordinarios (MCO):** Se ajusta el modelo lineal simple \(Y_i = \beta_0 + \beta_1 X_i + \varepsilon_i\) tanto a nivel global como segmentado
por cada perfil de viajero, evaluando interceptos, pendientes, coeficientes de determinación (r-cuadrado) y gráficos de diagnóstico de residuos.
- **Análisis de correlación y verificación de linealidad:** Se calcula la correlación lineal de Pearson (r) acompañada de medidas no paramétricas de rango (Spearman ρ y
Kendall τ_b). Asimismo, se compara el r-cuadrado del modelo lineal fente a η-cuadrado (calculado sobre los 15 valores discretos de X) para comprobar que la especificación
lineal captura prácticamente toda la varianza explicable sin pérdida relevante por no linealidad.
- **Restricción de rango y descomposición multinivel:** Dado que la calificación general (X) se concentra en un intervalo estrecho (rango observado de 8,2 a 9,6; 95% de los
registros entre 8,2 y 9,6), se aplica la corrección de Thorndike para descartar atenuación por restricción de rango y se descompone la covarianza en su componente intra-hotel
frente a entre-hoteles.
- **Inferencia robusta por conglomerados y bootstrap:** Debido a que las reseñas emitidas sobre un mismo establecimiento comparten estructura de grupo y no son estadísticamente
independientes entre si, la inferencia principal se respalda en errores típicos agrupados por hotel (25 conglomerados) y remuestreo bootstrap, evitando subestimar los intervalos
de confianza como ocurriría bajo errores estándar clásicos.
""")

st.header("4. Limitaciones y Precauciones de Interpretación")
st.markdown("""
- **Dependencia intra-hotel:** La agrupación de reseñas dentro de 25 hoteles reduce el tamaño muestral efectivo independiente; por ello, las pruebas de significancia e intervalos
de confianza se interpretan priorizando los errores agrupados por hotel y los intervalos bootstrap.
- **Estabilidad del ordenamiento entre perfiles:** Aunque la interacción entre perfil viajero y calificación general resulta estadísticamente significativa, al evaluar la estabilidad
mediante bootstrap por hotel no todo el ordenamiento completo entre los cuatro perfiles se mantiene invariante, por lo que las diferencias intermedias deben interpretarse con cautela.
- **Carácter observacional de los datos:** Al tratarse de registros históricos recopilados en plataforma y no de un experimento aleatorio controladom, las pendientes y correlaciones
estimadas expresan asociaciones estadísticas y patrones predictivos, más no casualidad directa.
""")
