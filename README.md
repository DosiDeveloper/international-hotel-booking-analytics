# Corrección Probabilística en Rankings Hoteleros: Promedios Bayesianos y Sistemas de Recomendación Adaptativos según el Perfil del Viajero


## Planteamiento del Problema
En la industria hotelera contemporánea, las calificaciones de los usuarios son el principal motor para la toma de decisiones de nuevos clientes; sin embargo, las métricas tradicionales de evaluación presentan sesgos analíticos importantes. En primer lugar, los rankings basados en promedios aritméticos simples son altamente susceptibles al volumen muestral, permitiendo que destinos u hoteles con un número ínfimo de reseñas (ej. calificaciones perfectas de 5.0 con solo 2 o 3 evaluaciones) desplacen injustamente a establecimientos con un desempeño consistente a lo largo de cientos de reseñas.

En segundo lugar, la métrica de "relación calidad-precio" suele tratarse como un indicador universal, ignorando que la percepción de valor es inherentemente subjetiva y heterogénea. Esta percepción está condicionada por características demográficas, el propósito del viaje, la expectativa generada por la categoría del hotel y barreras socioculturales o económicas reflejadas en la condición del turista. Ignorar esta varianza estadística conduce a conclusiones sesgadas sobre el desempeño real del mercado hotelero.

Finalmente, los sistemas de búsqueda actuales suelen ofrecer listados estáticos que no se adaptan a las prioridades multidimensionales de cada segmento. Un viajero de negocios no pondera la ubicación y las instalaciones de la misma manera que un viajero de ocio o una familia. Por lo tanto, existe la necesidad de desarrollar un marco analítico que corrija las distorsiones métricas mediante inferencia bayesiana, valide estadísticamente las diferencias de percepción entre nichos de viajeros y proponga un sistema de recomendación dinámico basado en vectores de similitud y ponderaciones adaptativas.

## Objetivo General
Desarrollar un marco analítico integral para la evaluación y recomendación de alojamientos hoteleros, aplicando técnicas de corrección probabilística, pruebas de hipótesis y sistemas de similitud vectorial para optimizar la comprensión de la percepción de valor y mejorar la toma de decisiones de distintos perfiles de viajeros.

## Objetivos Específicos
- Construir y contrastar modelos de ranking de destinos y hoteles en función de su relación precio-calidad, implementando el cálculo de promedios bayesianos para penalizar estadísticamente a los establecimientos con bajo volumen de evaluaciones frente a los promedios simples.

- Determinar la existencia de diferencias estadísticamente significativas en la percepción de valor de los usuarios aplicando pruebas de varianza (ANOVA o Kruskal-Wallis, según la normalidad de los datos) y análisis de tamaño de efecto, segmentando la muestra por categoría del hotel, tipo de viajero, grupo etario y el contraste de turismo interno vs. receptivo.

- Diseñar la arquitectura matemática de un recomendador descriptivo que ordene los hoteles de un destino mediante un puntaje ponderado dinámico, donde los pesos de dimensiones específicas se calculen empíricamente según las preferencias históricas y el perfil del viajero.

- Implementar un motor de sugerencia de "hoteles similares" basado en el cálculo de similitud coseno, comparando los vectores n-dimensionales de las sub-calificaciones de cada establecimiento para ofrecer alternativas de alojamiento altamente correlacionadas a las preferencias del usuario.
