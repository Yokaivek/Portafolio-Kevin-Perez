# Análisis y Clustering de Jugadores — FIFA19

## Resumen / objetivo
Proyecto para explorar y segmentar jugadores del dataset "FIFA19-DS.csv" mediante técnicas de reducción de dimensionalidad y clustering. El objetivo es identificar perfiles de jugadores (roles/tipos) a partir de sus atributos y caracterizar cada grupo resultante.

## Descripción del dataset
- Archivo: `FIFA19-DS.csv`
- Cada fila representa un jugador de FIFA19 con atributos físicos, técnicos y estadísticas (edad, overall, potencial, habilidades de pase, tiro, defensa, físico, etc.).
- Se trabajó principalmente con columnas numéricas del dataset y con una codificación one-hot (dummies) de la variable categórica `Position`.

Columnas usadas (ejemplos principales):
- Atributos generales: `Age`, `Overall`, `Potential`, `Special`
- Físicos: `Height`, `Weight`, `Acceleration`, `SprintSpeed`, `Agility`, `Strength`, `Stamina`, `Jumping`
- Técnicos: `Crossing`, `Finishing`, `HeadingAccuracy`, `ShortPassing`, `Volleys`, `Dribbling`, `BallControl`, `LongPassing`, `Curve`, `FKAccuracy`, `LongShots`, `ShotPower`
- Defensivos: `Interceptions`, `Marking`, `StandingTackle`, `SlidingTackle`, `Aggression`, `Positioning`
- Otros: `Vision`, `Penalties`, `Composure`, `Reactions`
- Dummies de posición: `Position_AM`, `Position_DF`, `Position_DM`, `Position_GK`, `Position_MF`, `Position_ST`

## Qué se hizo en el notebook
1. Carga y EDA básico
    - Lectura de `FIFA19-DS.csv`.
    - Inspección con `df.info()`, `df.describe()`, histogramas y heatmap de correlaciones para columnas numéricas seleccionadas.

2. Preprocesamiento
    - Creación de dummies para `Position` y concatenación al DataFrame.
    - Selección de un subconjunto de variables representativas (ver lista de columnas usadas).
    - Normalización con `StandardScaler`.

3. Reducción de dimensionalidad
    - Aplicación de t-SNE (2 componentes) para visualizar la estructura de los datos en 2D.
    - Se exploraron varias "perplexities" (20, 30, 40, 50) para comprobar robustez visual.

4. Clustering — KMeans
    - Evaluación de KMeans variando K (2 a 4 en el flujo de ejemplo).
    - Cálculo e visualización de métricas: inercia (distorsión / elbow), Silhouette, Calinski-Harabasz y Davies-Bouldin.
    - Visualización de siluetas con Yellowbrick.
    - Asignación de clusters KMeans al DataFrame (`cluster`).

5. Clustering — Gaussian Mixture Models (GMM)
    - Evaluación de modelos GMM con distintos números de componentes (BIC y AIC para selección).
    - Experimentos mostraron valores óptimos estadísticos altos (p. ej. ~55), pero por criterios de interpretabilidad se optó por un modelo con 6 componentes.
    - Asignación de clusters GMM al DataFrame (`cluster_gm`).

6. Visualización y caracterización
    - Plot de clusters sobre el espacio t-SNE.
    - Agrupación por cluster y cálculo de medias (atributos) para caracterizar cada grupo.
    - Tabla resumen interpretativa de 6 clusters (p. ej. GK, DF, DM, MF, AM, ST / tipos: defensivos, creativos, veloces, etc.).

## Decisiones relevantes y justificación
- Aunque BIC/AIC sugirieron un número de clusters muy alto, se eligieron 6 clusters por razones de interpretabilidad y coherencia con roles futbolísticos reales (equilibrio entre ajuste estadístico y utilidad analítica).
- Uso de t-SNE para visualización (no para clustering directo) y clustering sobre atributos estandarizados.

## Dependencias principales
- numpy, pandas, matplotlib, seaborn
- scikit-learn (StandardScaler, KMeans, GaussianMixture, métricas)
- yellowbrick (SilhouetteVisualizer)
- plotly (visualizaciones interactivas opcionales)

Ejemplo (pip):
pip install numpy pandas matplotlib seaborn scikit-learn yellowbrick plotly

## Cómo reproducir
1. Colocar `FIFA19-DS.csv` en el mismo directorio del notebook.
2. Abrir y ejecutar las celdas del notebook en orden (importaciones, carga de datos, EDA, preprocesamiento, t-SNE, evaluaciones de clustering, visualizaciones y caracterización).
3. Revisar y ajustar hiperparámetros:
    - Columnas en `selected_cols`
    - Perplexity de t-SNE
    - Rango de K para KMeans y n_components para GMM
4. Guardar resultados o etiquetas de cluster en un CSV si se desea:
    df.to_csv('FIFA19_clustered.csv', index=False)

## Resultados clave
- Se obtuvieron 6 clusters interpretables que agrupan jugadores por perfiles (porteros, defensas físicos, mediocampistas defensivos, mediocampistas mixtos, mediapuntas/creativos y delanteros).
- Visualizaciones t-SNE muestran separación clara entre los grupos elegidos.

## Posibles extensiones / trabajo futuro
- Análisis jerárquico: sub-clustering dentro de cada cluster para capturar especializaciones.
- Uso de UMAP como alternativa a t-SNE para preservación de estructura global.
- Incorporar atributos específicos de portero si existen en el dataset (features GK).
- Validación cruzada de clusters con datos de rendimiento real (minutos, goles, asistencias).

---

Archivo generado por el notebook: `FIFA19-DS.csv` (entrada)  
Etiquetas de salida dentro del DataFrame: `tsne_1`, `tsne_2`, `cluster` (KMeans), `cluster_gm` (GMM)