import streamlit as st

st.title("Conclusiones")
st.caption(
  "Conclusiones obtenidas de los cuatro (4) objetivos específicos de nuestro trabajo."
)
st.markdown("---")

st.subheader("Corrección de los rankings mediante la aplicación de promedios bayesianos")
st.write(
  "El trabajo confirmó que los promedios aritméticos simples tratan por igual a un hotel con"
  "cientos de reseñas que a otro con apenas dos o tres opiniones totalmente positivas, y que esa"
  "discrepancia no pasa desapercibida: afecta la visibilidad de de establecimientos con un desempeño"
  "consistente y confunde a los viajeros que buscan referencias confiables. La implementación de" 
  "promedios bayesianos permitió penalizar estadísticamente a los hoteles con bajo volumen de" 
  "evaluaciones, de modo que el ranking resultante refleja la evidencia disponible y no solo el" 
  "azar de unas pocas calificaciones altas. El contraste entre el ranking simple y el corregido" 
  "muestra que el orden cambia de forma notable, sobre todo en la parte alta de la tabla, donde" 
  "los hoteles con pocas reseñas suelen sobrerrepresentarse. Esta corrección no elimina la subjetividad"
  "de la calidad-precio, pero si logra acotar el margen de error con el que se construyen las comparaciones"
  "entre establecimientos."
)
st.subheader("Diferencias de percepción entre los perfiles de usuario")
st.write(
  "Las pruebas de hipótesis aplicadas a los segmentos de viajeros arrojaron diferencias estadísticamente significativas en la percepción de valor." 
  "La regresión por perfil es consistente con ese hallazgo: las pendientes van de 0,9342 en el perfil Solo a 0,6353 en el perfil Negocios," 
  "ya la interacción perfil por calificación general resultó significativa [F(3;49.985) = 43,26; p < 0,001]. No obstante, la robustez de esas diferencias"
  "merece matizarse, Solamente el contraste entre el perfil Solo y el de Negocios se mantuvo estable en las réplicas bootstrap" 
  "(con una diferencia de 0,145; IC95% [0,056;0,238]), mientras que el orden completo de los cuatro perfiles se reprodujo en apenas el 48,4% de las réplicas."
  "Dicho de otro modo, hay una diferencia clara entre los dos extremos, pero no una jerarquía rígida entre todos los segmentos. Reconocerlo es más honesto que"
  "presentar un orden estable el cual no se ve respaldado por los datos."
)
  
  
