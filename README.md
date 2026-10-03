# Optimización de rankings hoteleros mediante inferencia bayesiana y similitud vectorial por perfil de usuario.

## Introducción
En la actualidad, las opiniones y calificaciones de los usuarios en plataformas digitales son el factor determinante al elegir un hotel. Sin embargo, las métricas que utilizan la mayoría de los sitios web presentan fallas importantes. Al calcular promedios aritméticos simples, se trata por igual a un hotel con cientos de evaluaciones que a uno con solo dos o tres opiniones perfectas. Esto genera rankings distorsionados e injustos, un problema que puede corregirse mediante promedios bayesianos, los cuales aplican una corrección probabilística para ajustar la puntuación según el volumen de reseñas.

La percepción de la relación calidad-precio es totalmente subjetiva. Lo que valora un viajero de negocios (como una buena conexión a internet o la ubicación) no es lo mismo que busca una familia o un turista internacional. Para demostrar estas diferencias de criterio de forma fundamentada, es necesario aplicar pruebas estadísticas de hipótesis como ANOVA o Kruskal-Wallis, analizando cómo varían las calificaciones según el perfil del usuario, la categoría del hospedaje y el tipo de turismo.

Los buscadores actuales son rígidos y muestran listas estáticas que obligan al usuario a filtrar manualmente entre cientos de opciones. Para resolver esto, este trabajo propone un sistema de recomendación adaptativo que utiliza la similitud coseno sobre vectores de calificaciones. De esta manera, es posible calcular qué tan parecidos son los hoteles entre sí y ofrecer recomendaciones personalizadas que se ajusten de forma automática a las prioridades de cada viajero.

## Planteamiento del Problema
En la industria hotelera contemporánea, las calificaciones de los usuarios son el principal motor para la toma de decisiones de nuevos clientes; sin embargo, las métricas tradicionales de evaluación presentan sesgos analíticos importantes. En primer lugar, los rankings basados en promedios aritméticos simples son altamente susceptibles al volumen muestral, permitiendo que destinos u hoteles con un número ínfimo de reseñas (ej. calificaciones perfectas de 5.0 con solo 2 o 3 evaluaciones) desplacen injustamente a establecimientos con un desempeño consistente a lo largo de cientos de reseñas.

En segundo lugar, la métrica de "relación calidad-precio" suele tratarse como un indicador universal, ignorando que la percepción de valor es inherentemente subjetiva y heterogénea. Esta percepción está condicionada por características demográficas, el propósito del viaje, la expectativa generada por la categoría del hotel y barreras socioculturales o económicas reflejadas en la condición del turista. Ignorar esta varianza estadística conduce a conclusiones sesgadas sobre el desempeño real del mercado hotelero.

Finalmente, los sistemas de búsqueda actuales suelen ofrecer listados estáticos que no se adaptan a las prioridades multidimensionales de cada segmento. Un viajero de negocios no pondera la ubicación y las instalaciones de la misma manera que un viajero de ocio o una familia. Por lo tanto, existe la necesidad de desarrollar un marco analítico que corrija las distorsiones métricas mediante inferencia bayesiana, valide estadísticamente las diferencias de percepción entre nichos de viajeros y proponga un sistema de recomendación dinámico basado en vectores de similitud y ponderaciones adaptativas.

## Justificacion del Problema

Los rankings hoteleros tradicionales basados en promedios simples generan distorsiones al igualar calificaciones de hoteles con miles de reseñas con los hoteles de apenas unas pocas. Para resolver esto, se propone el uso de promedios bayesianos, los cuales ajustan las puntuaciones con rigor estadístico para reflejar un ranking justo.

Asimismo, dado que la percepción de calidad-precio varía según el segmento de usuario (negocios, familias o turistas), el estudio utiliza pruebas estadísticas (ANOVA o Kruskal-Wallis) para validar estas diferencias por perfil.

Finalmente, para superar la rigidez de los motores de búsqueda actuales, se integra la similitud coseno vectorial, permitiendo recomendaciones adaptativas y personalizadas que simplifican la búsqueda del viajero.

## Pregunta principal de investigación

¿De qué manera un marco analítico basado en corrección probabilística bayesiana, pruebas de varianza multivariadas y sistemas de similitud vectorial permite corregir las distorsiones de evaluación y optimizar la recomendación de alojamientos según el perfil del viajero?

### Preguntas específicas de investigación

¿En qué medida el uso de promedios bayesianos altera el ordenamiento de destinos y hoteles al penalizar el bajo volumen de evaluaciones, en comparación con los modelos de ranking tradicionales basados en promedios simples?

¿Existen diferencias estadísticamente significativas en la percepción de la relación calidad-precio entre usuarios al segmentarlos por categoría del hotel, tipo de viajero, grupo etario y condición de turismo interno vs. receptivo, y cuál es la magnitud de dicho efecto? 

¿Cómo debe estructurarse la arquitectura matemática de un recomendador descriptivo para que el cálculo de puntajes ponderados refleje dinámicamente las preferencias históricas de cada perfil de viajero? 

¿Qué nivel de precisión y ajuste alcanza un motor de recomendación basado en similitud coseno sobre vectores n-dimensionales de sub-calificaciones para identificar hoteles verdaderamente similares?


## Objetivo General
Desarrollar un marco analítico integral para la evaluación y recomendación de alojamientos hoteleros, aplicando técnicas de corrección probabilística, pruebas de hipótesis y sistemas de similitud vectorial para optimizar la comprensión de la percepción de valor y mejorar la toma de decisiones de distintos perfiles de viajeros.

## Objetivos Específicos
- Construir y contrastar modelos de ranking de destinos y hoteles en función de su relación precio-calidad, implementando el cálculo de promedios bayesianos para penalizar estadísticamente a los establecimientos con bajo volumen de evaluaciones frente a los promedios simples.

- Determinar la existencia de diferencias estadísticamente significativas en la percepción de valor de los usuarios aplicando pruebas de varianza (ANOVA o Kruskal-Wallis, según la normalidad de los datos) y análisis de tamaño de efecto, segmentando la muestra por categoría del hotel, tipo de viajero, grupo etario y el contraste de turismo interno vs. receptivo.

- Diseñar la arquitectura matemática de un recomendador descriptivo que ordene los hoteles de un destino mediante un puntaje ponderado dinámico, donde los pesos de dimensiones específicas se calculen empíricamente según las preferencias históricas y el perfil del viajero.

- Implementar un motor de sugerencia de "hoteles similares" basado en el cálculo de similitud coseno, comparando los vectores n-dimensionales de las sub-calificaciones de cada establecimiento para ofrecer alternativas de alojamiento altamente correlacionadas a las preferencias del usuario.

Dataset [en kaggle](https://www.kaggle.com/datasets/alperenmyung/international-hotel-booking-analytics)
