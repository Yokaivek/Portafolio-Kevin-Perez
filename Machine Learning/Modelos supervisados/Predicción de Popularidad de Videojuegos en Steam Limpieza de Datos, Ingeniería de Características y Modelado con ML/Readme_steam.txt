# Proyecto: Análisis y Modelado de Popularidad de Juegos (Steam)

Resumen
-------
Este notebook procesa un dataset de juegos de steam (converted.csv) para crear una variable objetivo ("is_popular") basada en un score de popularidad. Se realiza limpieza, transformación, ingeniería de características, entrenamiento y evaluación de varios modelos supervisados, monitorización de drift y explicabilidad (SHAP).

Descripción de los datos
------------------------
El dataset original está en `./converted.csv`. Entre las columnas relevantes que se usan en el notebook están (no exhaustiva):
- AppID, Name, Release date, Price
- Supported languages, Genres, Categories
- Developers, Publishers, DLC count
- Average playtime forever, Median playtime forever, Average/Median playtime two weeks
- Peak CCU, User score, Metacritic score, Recommendations
- Estimated owners (rango, p.ej. "50,000 - 100,000")
- Required age, Achievements
- Positive, Negative (reseñas)
- Short description
Se eliminan columnas textuales/largas y metadatos irrelevantes para modelado.

Flujo y transformaciones realizadas
-----------------------------------
1. Lectura y limpieza
    - Lectura de `converted.csv`.
    - Conversión de AppID a string y parsing de fechas mixtas.
    - Eliminación de columnas innecesarias y filas con NaN críticas.

2. Agrupación por juego
    - Agrupación por `Name`: se toma el primer valor para columnas no-numéricas y el promedio para numéricas, con el fin de consolidar entradas duplicadas.

3. Tratamiento de texto multivalor
    - `Supported languages`, `Genres`, `Categories` se separan y se binarizan con MultiLabelBinarizer.
    - Idiomas/géneros/categorías raros se agrupan en "Other".

4. Developers / Publishers
    - Se filtran por frecuencia (umbrales) y se crean dummies para los principales; el resto se marca como "Others".

5. Limpieza adicional y categorizaciones
    - Transformación de `Estimated owners` de rango a valor medio numérico.
    - Conversión de `Required age` y `Achievements` a categorías / buckets y creación de dummies.

6. Ingeniería de la variable objetivo y features
    - Se crea `acceptance_ratio` = Positive / (Positive + Negative).
    - Normalización de features numéricas (RobustScaler).
    - Penalización de `User score` y `Metacritic score` si < 60.
    - Construcción de `popularity_score` como combinación ponderada de owners, aceptación, ccu, playtime y scores.
    - Etiquetado binario `is_popular` usando el cuartil 75 de `popularity_score`.

7. Features temporales
    - Extracción de año, mes, día y trimestre desde `Release date`.

Modelado
--------
- Se construye un pipeline con ColumnTransformer que aplica:
  - Imputación y escalado a variables numéricas.
  - TF-IDF (max_features=50) a `Short description`.
- Modelos entrenados/evaluados: RandomForest, XGBoost, LightGBM, GradientBoosting, Bagging y un VotingClassifier.
- CV: StratifiedKFold (5 splits), métricas: accuracy, precision, recall, f1, ROC AUC, matriz de confusión y curvas ROC.
- Búsqueda de hiperparámetros con GridSearchCV para varios modelos.

Selección final y análisis post-entrenamiento
--------------------------------------------
- Modelo elegido: XGBoost (pipeline completo).
- Se extraen importancias de feature desde el modelo entrenado.
- Se calcula PSI (Population Stability Index) para detectar drift entre particiones (train vs test) y por periodos.
- Se evalúan métricas por año: KS entre distribuciones de probabilidad por clase, ROC AUC, F1.
- Explicabilidad: SHAP summary (bar y beeswarm) y force plot por observación.

Visualizaciones
---------------
- Histogramas de precios y otras distribuciones (matplotlib / seaborn).
- Histogramas y gráficos interactivos por año/mes de lanzamiento (plotly).
- Gráficos de PSI y evolución temporal de métricas (plotly).
- SHAP plots (summary y force).

Dependencias principales
------------------------
Las librerías usadas (importadas en el notebook):
- pandas, numpy, collections.Counter, datetime
- matplotlib, seaborn, plotly (express, graph_objects)
- scikit-learn (model_selection, pipeline, preprocessing, metrics, impute, compose)
- xgboost, lightgbm
- scipy.stats (ks_2samp)
- shap

Instrucciones para ejecutar
---------------------------
1. Colocar `converted.csv` en la ruta `./converted.csv`.
2. Abrir y ejecutar las celdas del notebook en orden. Algunas celdas entrenan modelos y pueden tardar dependiendo del hardware.
3. Ajustar `max_features` en TF-IDF, umbrales de frecuencia (developers/publishers) y parámetros de GridSearch según tamaño de datos y recursos.

Salida esperada
---------------
- DataFrame final `df_pr` con features procesadas y etiqueta `is_popular`.
- Pipelines y grids entrenados: `grid_rf`, `grid_xgb`, `grid_lgbm`, `grid_gb`.
- Evaluaciones cross-validated (matrices, curvas ROC, métricas).
- DataFrames de drift/PSI (`psi_df`, `df_psi`) y métricas por año (`df_metricas`).
- Plots SHAP y explicabilidad.

Siguientes pasos sugeridos
-------------------------
- Afinar ingeniería de features (más texto, embeddings, interacciones).
- Balanceo de clases (SMOTE, calibración, umbral óptimo).
- Validación temporal real (si hay dependencia temporal fuerte).
- Despliegue del pipeline XGBoost y monitorización continua de PSI/KPI.
- Guardar modelos y preprocessor con joblib para producción.

Licencia y notas
----------------
- Datos originales deben revisarse por licencias externas si no son de creación propia.
- El notebook está pensado para exploración y prototipado; para producción se recomienda modularizar, tests y control de versiones del dataset.