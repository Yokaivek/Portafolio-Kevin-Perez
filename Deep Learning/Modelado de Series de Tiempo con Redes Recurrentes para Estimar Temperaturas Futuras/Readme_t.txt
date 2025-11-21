# Proyecto: Predicción de Temperatura Diaria (LSTM)

## Resumen / Contexto
Este notebook procesa datos meteorológicos históricos (JSON + Excel) para construir un modelo LSTM que predice la temperatura media diaria del día siguiente. Se realiza limpieza e imputación, ingeniería de características temporales cíclicas (mes/día), escalado, creación de secuencias temporales y entrenamiento/validación de una red recurrente. Finalmente se generan predicciones para los siguientes 31 días y se exportan resultados.

## Origen y formato de los datos
- Archivos JSON en ./datos/históricos/ con prefijo `meteorología_*.json`. Cada JSON contiene estructura `pollutionMeasurements -> date -> <timestamp> -> <parametro> -> <estacion>`.
    - Se filtran registros para la estación objetivo: `FAC`.
    - Se crean columnas dinámicamente solo para parámetros presentes en cada archivo.
    - Se corrigen timestamps con "24:00" convirtiéndolos a "00:00" del día siguiente.
- Archivo Excel: `./meteorologia_historica_completa.xlsx` (usado como fuente principal para el análisis diario).
- Salida final de predicciones: CSV (nombre largo) y modelos guardados en `./models2/`.

## Preprocesamiento principal
1. Combina datos JSON por año y normaliza fechas.
2. Lee el Excel y agrega columnas auxiliares (`fecha_dia`, año, mes).
3. Agrupa por día y calcula estadísticas:
     - RH: mean, min, max, std
     - TMP: mean y count
     - WDR, WSP: mean, min, max
4. Filtrado e imputación:
     - Se conservan días con al menos 8 lecturas de temperatura (TMP_count >= 8).
     - Interpolación lineal limitada a intervalos pequeños (máx. 2 días consecutivos) para TMP y otras variables seleccionadas.
5. Codificación cíclica para temporalidad:
     - Mes y día convertidos a sen/cos para conservar la circularidad (mes_sin, mes_cos, dia_sin, dia_cos).
     - Estas variables no son escaladas para conservar su interpretación circular.

## Construcción del dataset para el modelo
- `df_modelo` contiene variables explicativas y la variable objetivo `TMP_prev` (temperatura del día siguiente) creada con un shift(-1).
- Separación de características cíclicas y numéricas.
- Escalado numérico con `MinMaxScaler` (las variables cíclicas se mantienen sin escalar).
- Objetivo `y` también escalado con `MinMaxScaler`.

## Secuencias temporales y particionado
- Secuencias de entrada creadas con ventana de 7 días (`n_steps = 7`).
- División train/test: 80% / 20% sobre las secuencias.
- Se eliminan muestras de test con `y` NaN.

## Arquitectura del modelo
- Modelo secuencial Keras/TensorFlow:
    - LSTM(64) (activación tanh)
    - Dropout(0.2)
    - Dense(32) + LeakyReLU (negative_slope=0.1)
    - Dense(1) salida
- Compilación: loss = MSE, optimizador = Adam
- Métricas: RMSE, MAE, MAPE
- Callbacks:
    - EarlyStopping monitor='val_mae', patience=20
    - ModelCheckpoint guarda el mejor modelo según val_mae en `./models2/model_{val_mae:.3f}.keras`

## Entrenamiento y evaluación
- Entrenamiento por hasta 100 épocas, batch_size=16.
- Se registran y trazan las métricas de entrenamiento/validación (plotly).
- Se identifica el mejor `val_mae` leyendo los archivos en `./models2/` y se carga el mejor modelo.
- Predicción sobre el conjunto de test, inversión del escalado y visualización comparativa (real vs predicho).

## Predicción futura (31 días)
- Predicción iterativa usando las últimas 7 ventanas disponibles:
    - Para cada día futuro se predice, se calcula la codificación cíclica del día siguiente y se actualiza la ventana desplazando e incorporando la predicción escalada.
- Se genera un DataFrame con fechas y `TMP_predicho` para 31 días y se grafica junto al histórico reciente.
- Se exporta el resultado a CSV.

## Salidas principales
- Modelos guardados: `./models2/model_*.keras`
- CSV de predicciones futuras: `./Equipo_Alfa_..._Del_Caldo.csv`
- Visualizaciones interactivas con Plotly (histórico vs predicción, codificación cíclica, métricas de entrenamiento).

## Dependencias principales
- Python 3.x
- pandas, numpy
- scikit-learn
- tensorflow / keras
- plotly
- matplotlib
- openpyxl (para lectura de Excel)
- pathlib, json, os, datetime

## Recomendaciones y notas
- Asegurar rutas: `./datos/históricos/` y `./meteorologia_historica_completa.xlsx` presentes.
- Crear carpeta `models2/` antes de entrenar para que ModelCheckpoint guarde modelos.
- La interpolación está limitada a breves huecos; si hay grandes lagunas conviene revisar la estrategia de imputación.
- Posibles mejoras:
    - Hiperparámetros del LSTM (número de capas, unidades, tasa de dropout).
    - Uso de features adicionales (humedad, viento) con selección/regularización.
    - Validación cruzada temporal y evaluación con métricas robustas por temporada.
    - Añadir intervalos de confianza en la predicción (ensembles, MC dropout).

## Cómo reproducir (pasos rápidos)
1. Colocar JSONs en `./datos/históricos/` y el Excel en la raíz.
2. Ejecutar celdas en orden (desde lectura hasta modelado).
3. Crear `models2/` si no existe.
4. Ejecutar entrenamiento (puede tardar según hardware).
5. Revisar `./models2/` para el mejor modelo y `CSV` de salida con predicciones.


Contactarse con el dueño del repositorio para proporcionar los datos para su replica