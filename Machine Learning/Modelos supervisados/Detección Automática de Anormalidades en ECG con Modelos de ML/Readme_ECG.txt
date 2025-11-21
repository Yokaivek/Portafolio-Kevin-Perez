# Proyecto: Detección de anomalías en ECG (NOT_NORM)

## Resumen / Contexto
Este notebook procesa señales ECG (archivos WFDB) y construye un pipeline completo para extracción de características, análisis exploratorio, modelado y evaluación de un clasificador que predice la etiqueta NOT_NORM (anormalidad). El objetivo es entrenar un modelo robusto (XGBoost en este caso) y exportar un pipeline reutilizable para inferencia sobre nuevos registros.

## Datos
- Archivos principales:
    - `train_e1.csv` — CSV de entrenamiento. Columnas esperadas (al menos):
        - `ecg_id`: identificador del registro
        - `filename_hr`: ruta/archivo WFDB del registro (usado por `wfdb.rdrecord`)
        - `age`, `sex`, `device` (o `decive` según variante), `recording_date`
        - `NOT_NORM`: etiqueta objetivo (0/1 o similar)
    - `test_e1.csv` — CSV de prueba con al menos `ecg_id` y `filename_hr`.
- Registros WFDB: ubicados en `base_dir` (ej. `records500`). Cada registro contiene canales (leads) y frecuencia de muestreo (`fs`).

## Qué se hace en el notebook
1. Lectura de `train_e1.csv` y carga de registros WFDB.
2. Extracción de características por canal (lead) para cada registro:
     - Estadísticas básicas: mean, std, min, max, median, IQR, skew, kurtosis
     - Energía y RMS
     - Entropía espectral (vía `welch`) y frecuencia dominante
     - Estimación de frecuencia cardíaca (HR) a partir de picos
     - Conteo de cruces por cero
3. Guardado de las características en `caracteristicas_ecg_extendido.csv`.
4. Limpieza y preprocesado:
     - Conversión de tipos, tratamiento de NA (imputación y/o eliminación)
     - Dummies para variables categóricas (`sex`, `decive`, `año`)
     - Escalado por `MinMaxScaler`
     - Opcional: reducción de dimensionalidad con PCA
5. Análisis exploratorio (EDA) y visualizaciones (matplotlib / plotly / seaborn).
6. Modelado:
     - Varios modelos comparados (Logistic Regression, Decision Tree, KNN, LDA, Naive Bayes, RandomForest, GradientBoosting, AdaBoost, Bagging, XGBoost).
     - Búsqueda de hiperparámetros con GridSearchCV y HalvingGridSearchCV (XGBoost).
     - Evaluación con validación cruzada estratificada (métricas: accuracy, precision, recall, f1, ROC AUC).
     - Curvas ROC y matrices de confusión.
7. Selección y ajuste final de XGBoost como modelo óptimo.
8. Evaluaciones por tiempo/periodo:
     - PSI (Population Stability Index) por mes/año comparando distribuciones de probabilidades.
     - Métricas por año (AUC, F1) y estadística KS.
9. Packaging / exportación:
     - Clase `CDD_G29_M2_E1_Kevin_Perez_Alvarez` que encapsula:
         - extracción de características,
         - preprocesado (scaler, columnas numéricas),
         - entrenamiento y predicción con XGBoost,
         - métodos `fit()`, `split_data()`, `fit_model()`, `score_auc()`, `predict_proba()`, `export_pipeline()` y `load_pipeline()`.
     - Exportación del pipeline entrenado con `joblib` (ej. `CDD_G29_M2_E1_Kevin_Perez_Alvarez.pkl`).
10. Inferencia sobre `test_e1.csv`: extracción de features, alineación de dummies, escalado y predicción probabilística; resultados guardados en CSV.

## Características extraídas (por cada canal/lead)
- mean, std, min, max, median, iqr, skew, kurtosis
- energy, rms
- spec_entropy (entropía espectral)
- dom_freq (frecuencia dominante)
- hr_est (estimación de frecuencia cardíaca)
- zero_cross (cruces por cero)

## Salidas importantes
- `caracteristicas_ecg_extendido.csv` — dataset de features generadas.
- `CDD_G29_M2_E1_Kevin_Perez_Alvarez.pkl` — pipeline/modelo exportado.
- `CDD_G29_M2_E1_Kevin_Perez_Alvarez.csv` — predicciones (ecg_id, y_hat) sobre test.
- Dataframes de métricas por año/mes (`df_metricas`, `df_psi`, etc.) mostrados en celdas de evaluación.

## Dependencias principales
Instalar (ejemplo):
pip install numpy pandas scipy scikit-learn xgboost wfdb matplotlib seaborn plotly tqdm joblib

(Las imports en el notebook incluyen también `plotly`, `wfdb`, `tqdm`, `xgboost`, etc.)

## Cómo reproducir (ejemplo rápido)
1. Ajustar rutas en el notebook: `csv_path` y `base_dir`.
2. Ejecutar celdas de extracción para generar `caracteristicas_ecg_extendido.csv`.
3. Ejecutar limpieza, EDA y modelado (celdas de gridsearch y validación).
4. Entrenar y exportar pipeline:
     - Crear instancia: `pipe = CDD_G29_M2_E1_Kevin_Perez_Alvarez(csv_path="train_e1.csv", base_dir="records500")`
     - `pipe.fit(); pipe.split_data(); pipe.fit_model(); pipe.export_pipeline("modelo.pkl")`
5. Inferencia en test:
     - Cargar pipeline: `pipe = CDD_G29_M2_E1_Kevin_Perez_Alvarez.load_pipeline("modelo.pkl")`
     - Extraer features en test, alinear columnas y usar `pipe.model.predict_proba(...)` para obtener `y_hat`.

## Consideraciones / Notas
- Asegurar que `filename_hr` en CSV apunte correctamente a archivos WFDB legibles por `wfdb.rdrecord`.
- Validar presencia de ambas clases por periodo si se calculan AUC/K-S por año/mes.
- Ajustar manejo de NA según el contexto clínico (imputación vs exclusión).
- Revisar posibles discrepancias de nombres de columna (`device` vs `decive`) y estandarizarlos.

## Contacto
Repositorio y notebook organizado para facilitar reproducción y exportación del pipeline para despliegue/inferencia.

Solicitar los datos para correr el código