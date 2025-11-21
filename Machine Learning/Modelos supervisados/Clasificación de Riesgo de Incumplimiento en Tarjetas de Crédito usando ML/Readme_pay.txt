# Proyecto: Predicción de impago de tarjetas (Default Payment)

## Contexto
Este proyecto busca construir un modelo que prediga si un cliente incumplirá el pago de su tarjeta de crédito el siguiente mes ("default payment next month"). Se usa un dataset de entrenamiento (`train_p3.csv`) y un conjunto de prueba (`test_p3.csv`). El flujo incluye análisis exploratorio, preprocesamiento, creación de features, balanceo de clases, evaluación con validación cruzada y generación de un pipeline final serializado para inferencia.

## Descripción de los datos
Columnas principales:
- ID: identificador del cliente.
- LIMIT_BAL: límite de crédito.
- SEX, EDUCATION, MARRIAGE, AGE: variables demográficas.
- PAY_1..PAY_6: historial de pagos (retrasos).
- BILL_AMT1..BILL_AMT6: montos de factura mensuales.
- PAY_AMT1..PAY_AMT6: montos pagados mensuales.
- default payment next month: variable objetivo (0 = No, 1 = Sí).

## Qué se realiza en el notebook
1. Lectura y exploración de los datos (EDA) con estadísticas, histogramas, boxplots y heatmaps de correlación.
2. Limpieza básica:
    - Renombrado de `PAY_0` a `PAY_1`.
    - Reemplazo de categorías raras en `EDUCATION` y `MARRIAGE`.
    - Detección de nulos y duplicados.
3. Tratamiento de outliers:
    - Recorte por IQR (clip) en variables numéricas.
4. Ingeniería de features:
    - Nuevas variables: `TOTAL_PAYMENTS`, `AVG_BILL_AMT`, `AVG_PAY_AMT`, `TOTAL_BILL`.
    - Indicadores: `IS_CONSISTENT_PAYER`, `AVG_PAY_DELAY`, `MAX_PAY_DELAY`, `NUM_LATE_PAYMENTS`, `PAYMENT_TREND`.
    - Eliminación de columnas altamente correlacionadas (se conserva `BILL_AMT1`).
5. Balanceo y escalado:
    - SMOTE para balancear clases.
    - StandardScaler para normalizar características.
6. Modelado y evaluación:
    - Evaluación con StratifiedKFold, métricas (accuracy, precision, recall, f1, ROC AUC), matriz de confusión y curvas ROC.
    - Modelos probados: Logistic Regression, KNN, SVM, Decision Tree, LDA.
    - Búsqueda de hiperparámetros con GridSearch para algunos modelos.
    - Uso de pipelines con PCA + clasificador para comparar rendimiento.
7. Pipeline final:
    - Se crea un pipeline (ImbPipeline) que incluye `OutlierClipper`, `CustomFeatures`, `StandardScaler`, `SMOTE` y KNN (configurado con los mejores hiperparámetros).
    - El pipeline se entrena con el dataset original (`aux`) y se guarda en `pipeline_final.pkl`.

## Archivos generados / necesarios
- `train_p3.csv` (entrada).
- `test_p3.csv` (ejemplo para inferencia).
- `CDD_G29_M2_P3_Kevin_Perez_Alvarez_custom_class.py` (definición de `OutlierClipper` y `CustomFeatures` si se usa externamente).
- `pipeline_final.pkl` (pipeline serializado).
- `predicciones_p3.csv` (salida de ejemplo tras inferencia).

## Uso rápido (inferencias)
Se incluye la función `predecir_y_guardar(model_path, test_csv_path, output_csv)` que:
- Carga el CSV de test.
- Carga el pipeline serializado (`pipeline_final.pkl`).
- Genera probabilidades `y_hat = pipeline.predict_proba(df)[:, 1]`.
- Guarda un CSV con columnas `ID` y `y_hat`.

Ejemplo de llamada en el notebook: