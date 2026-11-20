import streamlit as st

st.header("Marco teórico")

st.caption(
    "Los conceptos que sostienen los tres objetivos del trabajo: el ranking bayesiano, "
    "el contraste de diferencias entre perfiles y la regresión lineal simple que alimenta "
    "el recomendador. Cada sección cierra con lo que ocurre en estos datos."
)

st.markdown(
    """
    El trabajo responde una pregunta de medición: **cómo comparar hoteles cuando las
    opiniones que los describen no son independientes ni igualmente informativas**.
    Cada sección desarrolla una pieza de esa respuesta.
    """
)

st.markdown("---")

# --------------------------------------------------------------------------- #
st.subheader("1. Promedio bayesiano y encogimiento")

st.markdown(
    """
    Un promedio aritmético trata igual una media calculada con dos mil reseñas que una
    calculada con tres. Si las verdaderas medias de los hoteles se distribuyen alrededor
    de un valor común con dispersión $\\tau^2$ y cada hotel se observa con error
    $\\sigma^2/n_i$, el modelo jerárquico normal es:
    """
)

st.latex(r"\theta_i \sim N(m,\ \tau^2), \qquad R_i \mid \theta_i \sim N(\theta_i,\ \sigma^2/n_i)")

st.markdown(
    """
    La media a posteriori combina dato y prior con pesos inversos a su varianza:
    """
)

st.latex(r"\hat{\theta}_i = \frac{n_i R_i + C\,m}{n_i + C}, \qquad C = \frac{\sigma^2}{\tau^2}")

st.markdown(
    """
    $C$ se lee como **reseñas virtuales**: cuántas observaciones «vale» el prior. El peso
    del dato es $w_i = n_i/(n_i+C)$ y la varianza posterior es $\\sigma^2/(n_i+C)$, menor
    que la de la media muestral: el encogimiento no solo reordena, también reduce la
    incertidumbre.

    Tres consecuencias que conviene tener presentes:

    1. **El encogimiento es mayor cuanto menor es $n_i$**, que es el objetivo del método.
    2. **Si todos los $n_i$ son iguales y $C$ es fijo, el orden no cambia**: $\\hat{\\theta}_i$
       es una transformación afín creciente de $R_i$. El promedio bayesiano reescala, no
       reordena.
    3. **$C$ no se elige a mano.** La versión empírica estima $\\tau^2$ como la varianza
       entre medias menos la varianza muestral promedio, y despeja $C=\\sigma^2/\\tau^2$.
       Fijar $C$ igual a la mediana de $n_i$ supone $\\tau^2 \\approx \\sigma^2/\\bar{n}$.
    """
)

st.caption(
    "En estos datos cada hotel tiene entre 1.902 y 2.103 reseñas, de modo que el volumen "
    "está equilibrado: con C = mediana(n) ≈ 1.993 el peso es ≈ 0,5 para todos los hoteles."
)

# --------------------------------------------------------------------------- #
st.subheader("2. Contraste de hipótesis y tamaño del efecto")

st.markdown(
    """
    Para comparar $k$ grupos se contrasta $H_0: \\mu_1=\\dots=\\mu_k$ frente a la
    alternativa de que al menos una media difiera. El **ANOVA de un factor** lo hace con
    el cociente entre la variación entre grupos y la variación dentro de ellos:
    """
)

st.latex(
    r"F = \frac{SSB/(k-1)}{SSW/(n-k)}, \qquad "
    r"SSB = \sum_j n_j(\bar{y}_j-\bar{y})^2, \qquad "
    r"SSW = \sum_j\sum_i (y_{ij}-\bar{y}_j)^2"
)

st.markdown(
    """
    Exige independencia, normalidad dentro de cada grupo y varianzas iguales. Con grupos
    grandes y balanceados, $F$ es robusto a la falta de normalidad; la heterocedasticidad
    y la dependencia, en cambio, no se corrigen solas.

    La alternativa no paramétrica es **Kruskal-Wallis**, que reemplaza los valores por
    rangos:
    """
)

st.latex(r"H = \frac{12}{n(n+1)}\sum_j n_j \bar{R}_j^2 - 3(n+1), \qquad H \sim \chi^2_{k-1}")

st.markdown(
    """
    Con empates, $H$ se corrige dividiendo por $1 - \\sum_t (t^3-t)/(n^3-n)$. No exige
    normalidad, pero sí que las observaciones sean intercambiables dentro del grupo,
    supuesto que la dependencia por hotel también rompe.

    El **tamaño del efecto** responde una pregunta distinta a la del p-valor: no *si*
    hay diferencia, sino *cuánto* importa. Para ANOVA se usa
    $\\eta^2 = SSB/SST$; para Kruskal-Wallis, $\\varepsilon^2 = H\\big/((n^2-1)/(n+1))$.
    La convención habitual distingue efectos pequeños (0,01), medios (0,06) y grandes
    (0,14). Con $n \\approx 50.000$ el p-valor se vuelve diminuto ante diferencias
    triviales; el tamaño del efecto es el que decide.
    """
)

# --------------------------------------------------------------------------- #
st.subheader("3. Regresión lineal simple")

st.markdown(
    """
    El modelo supone una relación lineal entre una variable explicativa $x$ y una
    respuesta $y$, más un error que recoge todo lo omitido:
    """
)

st.latex(r"y_i = \beta_0 + \beta_1 x_i + \varepsilon_i, \qquad E[\varepsilon_i \mid x_i]=0, \quad Var(\varepsilon_i \mid x_i)=\sigma^2")

st.markdown(
    """
    **Mínimos cuadrados ordinarios (MCO)** elige los coeficientes que minimizan la suma
    de residuos al cuadrado. La solución tiene forma cerrada:
    """
)

st.latex(
    r"b_1 = \frac{S_{xy}}{S_{xx}} = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sum_i (x_i-\bar{x})^2}, "
    r"\qquad b_0 = \bar{y} - b_1\bar{x}"
)

st.markdown(
    """
    La variación total se descompone en explicada y residual,
    $SST = SSR + SSE$, de donde $R^2 = SSR/SST$; en regresión simple coincide con $r^2$
    y la correlación recupera el signo de la pendiente. La varianza residual
    $s^2 = SSE/(n-2)$ alimenta el error típico y la inferencia:
    """
)

st.latex(
    r"EE(b_1) = \frac{s}{\sqrt{S_{xx}}}, \qquad "
    r"t = \frac{b_1}{EE(b_1)} \sim t_{n-2}, \qquad "
    r"IC_{95\%}: b_1 \pm t_{1-\alpha/2,\,n-2}\,EE(b_1)"
)

st.markdown(
    """
    El **teorema de Gauss-Markov** garantiza que, bajo linealidad, exogeneidad,
    homocedasticidad y ausencia de autocorrelación, MCO es insesgado y de varianza
    mínima entre los estimadores lineales. La normalidad solo hace exactos los
    contrastes en muestras pequeñas; con $n$ grande se apela al teorema central del
    límite.

    **Interpretación.** $b_1$ son unidades de $y$ por unidad de $x$; $b_0$ es el valor
    esperado en $x=0$ y casi nunca es interpretable, porque suele quedar fuera del rango
    observado. La recta describe una asociación condicional, no una relación causal:
    puede haber variables omitidas (el hotel, el usuario, el momento de la estadía) y
    ambas variables son juicios emitidos en la misma reseña.

    **Predicción.** El intervalo de confianza de la media ajustada y el de predicción
    individual no coinciden; este último es más ancho porque añade la dispersión del
    error:
    """
)

st.latex(r"\hat{y}_0 \pm t_{1-\alpha/2,\,n-2}\; s \sqrt{1 + \frac{1}{n} + \frac{(x_0-\bar{x})^2}{S_{xx}}}")

st.markdown(
    """
    **Normalidad práctica.** Con miles de observaciones, cualquier contraste formal de
    normalidad rechaza. Por eso el diagnóstico se hace con asimetría y curtosis
    estandarizadas ($|z| \\le 2$ indica desviación trivial) y con el gráfico Q-Q, que
    muestra dónde se separan las colas.
    """
)

# --------------------------------------------------------------------------- #
st.subheader("4. Observaciones agrupadas e inferencia por conglomerados")

st.markdown(
    """
    Las reseñas no son independientes: comparten hotel. Si el error tiene un componente
    propio de cada hotel, $u_{ig} = \\alpha_g + \\varepsilon_{ig}$, aparece una
    correlación intraclase
    $\\rho = \\sigma^2_\\alpha/(\\sigma^2_\\alpha+\\sigma^2_\\varepsilon) > 0$
    que el modelo clásico ignora.

    La consecuencia es que el error típico de MCO **subestima** la varianza. El factor
    de inflación (Moulton) es aproximadamente
    $1 + (\\bar{m}-1)\\rho_x\\rho_e$, con $\\bar{m}$ el tamaño medio del conglomerado y
    $\\rho_x$, $\\rho_e$ las correlaciones intraclase del regresor y del residuo. Con 25
    hoteles y unas 2.000 reseñas cada uno, el número efectivo de observaciones puede caer
    de decenas de miles a unos pocos miles.

    La corrección estándar son los **errores típicos agrupados** (sandwich CR1):
    """
)

st.latex(
    r"V = (X'X)^{-1}\Big[\sum_g X_g'\,e_g e_g'\,X_g\Big](X'X)^{-1}"
    r"\;\cdot\;\frac{G}{G-1}\;\cdot\;\frac{n-1}{n-k}"
)

st.markdown(
    """
    con $G$ conglomerados. La inferencia pasa a usar $t_{G-1}$ en lugar de $t_{n-2}$.
    Una alternativa equivalente es el **bootstrap por conglomerado**: se remuestrean
    hoteles completos, no reseñas sueltas.

    Conviene distinguir tres estimaciones que no tienen por qué coincidir:

    - **Agrupada**: mezcla la variación dentro y entre hoteles.
    - **Intra-hotel** (efectos fijos): usa solo los desvíos respecto de la media de cada
      hotel, de modo que elimina cualquier diferencia fija entre establecimientos.
    - **Entre hoteles**: se estima sobre las medias de los 25 hoteles, con 25 puntos.

    Cuando las tres difieren, la diferencia es información sobre el fenómeno, no un
    error de cálculo.
    """
)

st.caption(
    "En este trabajo el error típico agrupado de la pendiente global es 11,2 veces el "
    "clásico (0,1296 frente a 0,0115), y la pendiente entre hoteles (0,634) es menos de "
    "la mitad que la de reseñas (1,378)."
)

# --------------------------------------------------------------------------- #
st.subheader("5. Segmentación y modificación del efecto")

st.markdown(
    """
    Comparar pendientes entre perfiles es un caso de **modificación del efecto**: la
    relación entre dos variables depende de una tercera. El modelo con interacción lo
    formaliza:
    """
)

st.latex(r"y = \beta_0 + \beta_1 x + \beta_2 D + \beta_3 (x \cdot D) + \varepsilon")

st.markdown(
    """
    con $D$ un indicador de perfil. La pendiente del grupo $D=1$ es $\\beta_1+\\beta_3$,
    de modo que $\\beta_3$ mide exactamente la diferencia de pendientes, y contrastar
    $\\beta_3=0$ equivale a contrastar pendientes iguales.

    El modelo **saturado** —intercepto y pendiente propios para cada grupo— reproduce
    las regresiones separadas. Segmentar tiene sentido cuando la relación depende de una
    característica del sujeto; no cuando se estratifica solo para «ver qué sale», porque
    cada corte reduce el tamaño de muestra y multiplica los contrastes.
    """
)

# --------------------------------------------------------------------------- #
st.subheader("6. Del modelo al ranking: el recomendador descriptivo")

st.markdown(
    """
    El recomendador puntúa cada hotel con $b_0 + b_1\\bar{x}_g$, donde $\\bar{x}_g$ es su
    calificación general promedio. Como $b_1>0$, se trata de una **transformación
    monótona** de $\\bar{x}_g$: ordena igual que la calificación media. Aporta escala
    —expresa la calificación en puntos de calidad-precio— y calibración por perfil, pero
    no un orden nuevo.

    El paso de reseñas a hoteles es una **inferencia ecológica**: se aplica una pendiente
    estimada con variación dentro de los hoteles a medias calculadas entre hoteles. Si
    ambas pendientes difieren, la proyección no estima la calidad-precio del hotel, sino
    la calificación media expresada en otra escala.

    Finalmente, un ranking descriptivo no es un sistema predictivo: no modela
    preferencias individuales, no se valida fuera de muestra y no estima efectos
    causales. Su unidad es el hotel, su conclusión se limita a los 25 hoteles observados
    y su orden fino no es defendible cuando las medias difieren menos que su error.
    """
)

# --------------------------------------------------------------------------- #
st.subheader("7. Limitaciones que se desprenden del diseño")

st.markdown(
    """
    - **Un hotel por ciudad y por país**, y los 25 con la misma categoría: no permite
      comparar destinos ni estimar un efecto geográfico o de categoría.
    - **Muestra de conveniencia**: la precisión es sobre estos hoteles, no sobre «los
      hoteles del mundo».
    - **Datos observacionales**: ninguna conclusión es causal.
    - **Variables discretas**: la calificación general toma 15 valores y la
      calidad-precio, 30; eso produce el escalonamiento visible en los residuos y en la
      dispersión, y no indica un problema del modelo.
    """
)

# --------------------------------------------------------------------------- #
st.markdown("---")
st.subheader("Referencias")

st.markdown(
    """
    1. Cameron, A. C. y Miller, D. L. (2015). A practitioner's guide to cluster-robust
       inference. *Journal of Human Resources*, 50(2), 317–372.
    2. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
       (2.ª ed.). Lawrence Erlbaum.
    3. Efron, B. y Morris, C. (1975). Data analysis using Stein's estimator and its
       generalizations. *Journal of the American Statistical Association*, 70(350),
       311–319.
    4. Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A. y Rubin, D. B.
       (2013). *Bayesian Data Analysis* (3.ª ed.). CRC Press.
    5. Kelley, K. y Preacher, K. J. (2012). On effect size. *Psychological Methods*,
       17(2), 137–152.
    6. Kruskal, W. H. y Wallis, W. A. (1952). Use of ranks in one-criterion variance
       analysis. *Journal of the American Statistical Association*, 47(260), 583–621.
    7. Moulton, B. R. (1990). An illustration of a pitfall in estimating the effects of
       aggregate variables on micro units. *Review of Economics and Statistics*, 72(2),
       334–338.
    8. Wooldridge, J. M. (2020). *Introductory Econometrics: A Modern Approach*
       (7.ª ed.). Cengage Learning.
    """
)
