# Simpsons - Clasificación de Personajes (Notebook)

Descripción
-----------
Este notebook prepara y entrena un clasificador CNN para reconocer personajes de *The Simpsons* a partir de imágenes. El conjunto de datos consiste en fotografías (archivos .jpg) organizadas inicialmente en una carpeta `simpsons`. El flujo general incluye limpieza/organización de archivos, particionado en train/val/test, aumento de datos, definición y entrenamiento de una red convolucional, y evaluación/inferencia sobre imágenes nuevas.

Estructura del proyecto
-----------------------
- `simpsons/` : Carpeta origen con todas las imágenes (.jpg).
- `simpsons_dataset/` : Directorio generado por el notebook con subcarpetas:
    - `train/<personaje>/`
    - `val/<personaje>/`
    - `test/<personaje>/`
- `models/` : Modelos guardados durante el entrenamiento.
- `cnn_los_simpsons.keras` : Modelo final guardado al final del notebook.
- Este notebook (Jupyter) que contiene todo el pipeline.

Qué hace el notebook (resumen por secciones)
--------------------------------------------
1. Importaciones y configuración (tensorflow, keras, PIL, numpy, pandas, matplotlib, etc.).
2. Semilla aleatoria `random_seed=333` para reproducibilidad.
3. Definición de rutas y creación de carpetas (`train`, `val`, `test`).
4. Lectura de todos los archivos en `simpsons/`, extracción de nombres de personajes y creación de carpetas por personaje.
5. División de imágenes por personaje en train/validation/test usando `train_test_split`.
6. Visualización: construcción de un mosaico con una imagen representativa por personaje (`crear_mosaico`).
7. Definición de ImageDataGenerator:
     - `dgen_train` con aumentos (rotación, shifts, zoom, brillo, flip, etc.) y reescalado.
     - `dgen_test` solo con reescalado.
8. Creación de `train_generator`, `validation_generator` y `test_generator` (target size 200x200, batch size 22).
9. Definición de la arquitectura CNN (varias capas Conv2D, BatchNorm, LeakyReLU, MaxPool, Dropout, Flatten y Dense final con softmax).
10. Compilación con Adam y pérdida `categorical_crossentropy`.
11. Callbacks: EarlyStopping (paciencia 15) y ModelCheckpoint (salva mejores modelos por `val_accuracy`).
12. Entrenamiento (`model.fit`) y guardado de historial en un DataFrame para graficar.
13. Selección del mejor modelo guardado y evaluación en el conjunto de prueba.
14. Ejemplo de inferencia sobre una imagen de validación y visualización del resultado.
15. Guardado final del modelo `cnn_los_simpsons.keras`.

Requisitos (paquetes principales)
---------------------------------
- Python 3.7+
- numpy
- pandas
- matplotlib
- pillow (PIL)
- scikit-learn
- tqdm
- tensorflow (>=2.x)
- keras (si se usa separado) 
- cufflinks (opcional para plots interactivos)

Instalación de dependencias (ejemplo)
-------------------------------------
pip install numpy pandas matplotlib pillow scikit-learn tqdm tensorflow cufflinks

Uso
---
1. Colocar todas las imágenes .jpg originales en la carpeta `simpsons/`.
2. Abrir el notebook y ejecutar las celdas en orden (desde las importaciones hasta entrenamiento/evaluación).
3. Ajustar parámetros en el notebook si hace falta:
     - TARGET_SIZE, BATCH_SIZE, epochs, learning_rate.
     - Rutas (source_dir, base_dir).
4. Monitorizar la carpeta `models/` para los checkpoints; el notebook carga el mejor modelo por `val_accuracy`.

Consejos y notas
----------------
- Asegurar suficiente memoria y, preferiblemente, GPU para entrenamiento.
- El tamaño de entrada (200x200) y el batch size pueden ajustarse según la GPU/memoria.
- Cambiar la semilla si se desea realizar experimentos con distintas particiones.
- Si faltan fuentes para los títulos en mosaicos, se usa la fuente por defecto de PIL.
- Revisar la distribución de imágenes por clase: clases con pocas imágenes pueden dificultar el aprendizaje.

Resultados y evaluación
-----------------------
- El historial de entrenamiento se almacena en `history` y se grafica con Plotly/pandas.
- Se guarda el mejor checkpoint por `val_accuracy` y se evalúa con `test_generator`.
- Ejemplo de inferencia muestra la etiqueta predicha y la confianza (probabilidad).

Licencia
--------
Entrega/uso personal o educativo. Adaptar a la licencia del dataset original si aplica.

Contactos / Referencias
-----------------------
Este README acompaña al notebook y pretende documentar el flujo y cómo reproducir los resultados localmente.

Contactarse con el dueño del repositorio para proporcionar los datos para su replica