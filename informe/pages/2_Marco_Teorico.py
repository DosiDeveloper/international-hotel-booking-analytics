import streamlit as st

st.markdown("""
    <style>
        .doc-container p, .doc-container li {
            text-align: justify;
            line-height: 1.65;
        }
        .doc-container h2 {
            margin-top: 1.5rem;
            margin-bottom: 0.6rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="doc-container">', unsafe_allow_html=True)

st.title("Marco Teorico y Fundamentos Analíticos")
st.caption("Bases conceptuales, estadísticas y métricas aplicadas al ecosistema de reservas de alojamientos.")
st.markdown("---")

st.markdown(r"""
## Introducción

En la industria hotelera contemporánea, las opiniones y calificaciones de los usuarios en plataformas digitales son el factor determinante al elegir un alojamiento. Sin embargo, las métricas tradicionales que utilizan la mayoría de los sitios web presentan fallas importantes:

* **El problema de las muestras pequeñas:** Al calcular promedios aritméticos simples, se trata por igual a un hotel con cientos de evaluaciones que a uno con solo dos o tres opiniones extremas, por ejemplo, calificaciones perfectas de $5.0$. Esto genera rankings distorsionados e injustos que desplazan establecimientos con un desempeño constante a lo largo del tiempo.
* **La subjetividad de la percepción:** Indicadores como la "relación calidad-precio" suelen tratarse como universales, ignorando que el valor es heterogéneo y está condicionado por el propósito del viaje, la categoría del hotel y el perfil del viajero.
* **La rigidez de los buscadores:** Los sistemas convencionales ofrecen listados estáticos que obligan a realizar filtrados manuales, sin adaptarse de forma dinámica a las prioridades analíticas de cada usuario.

## Ranking Bayesiano

Para mitigar la volatilidad de las calificaciones con pocos registros, se implementa el Promedio Bayesiano. Este método aplica una corrección probabilística para ajustar la puntuación observada de cada alojamiento hacia una media global previa (*prior*) en función del volumen de reseñas recibidas:
""")

st.latex(r"WR = \left( \frac{v}{v + C} \right) R + \left( \frac{C}{v + C} \right) m")

st.markdown(r"""
**Definición de variables:**

* **$WR$ (*Weighted Rating*):** Puntuación bayesiana ajustada del alojamiento.
* **$R$:** Promedio aritmético simple de las calificaciones del hotel.
* **$v$:** Número total de evaluaciones registradas para ese establecimiento.
* **$m$:** Promedio global de calificaciones de todos los hoteles en el conjunto de datos.
* **$C$:** Factor de confianza o umbral mínimo de evaluaciones necesarias para que la calificación propia del hotel tenga mayor peso que la media global.

Este enfoque penaliza de forma estadística la incertidumbre, garantizando que los rankings reflejen la preferencia real de los usuarios en función del volumen y la consistencia de sus evaluaciones.

## Percepción Calidad-Precio y Pruebas de Hipotesis

La percepción de valor en servicios de alojamiento evalúa la relación entre el desembolso económico del viajero y la calidad percibida de la estancia. Analíticamente, se estudia contrastando indicadores de satisfacción frente a tarifas por noche o categorías del establecimiento.

Dado que esta percepción varía según el perfil del usuario (turismo de negocios, familias o turistas receptivos o internos), el marco metodológico se apoya en pruebas estadísticas de hipótesis, como ANOVA o Kruskal-Wallis según la normalidad de la distribución de los datos, y en el análisis de tamaño de efecto, permitiendo validar de forma rigurosa si existen diferencias estadísticamente significativas entre los distintos segmentos de la demanda.

## Modelo de Regresión lineal simple

Para superar la rigidez de los buscadores estáticos y cuantificar la relación de dependencia entre una variable predictora clave (por ejemplo, la valoración de un atributo específico del servicio) y la satisfacción global del usuario, se emplea el modelo de **Regresión Lineal Simple**:
""")

st.latex(r"Y_i = \beta_0 + \beta_1 X_{i1} + \varepsilon_i")

st.markdown(r"""
**Definición de parámetros y variables:**

* **$Y_i$:** Variable dependiente o respuesta (satisfacción global del usuario).
* **$X_{i1}$:** Variable independiente o predictora (calificación de un servicio o atributo específico del hotel).
* **$\beta_0$:** Intercepto del modelo.
* **$\beta_1$:** Coeficiente de regresión que mide el cambio esperado en $Y$ ante un incremento unitario en $X_1$.
* **$\varepsilon_i$:** Término de perturbación aleatoria o error residual.

A través de este modelo, el sistema de recomendación propuesto es capaz de predecir y sugerir alternativas de alojamiento alineadas cuantitativamente con las prioridades evaluadas de cada perfil de viajero.
""")

st.markdown('</div>', unsafe_allow_html=True)