## Contexto del proyecto

Este notebook construye un Índice de Marginación Municipal para México a partir del Censo 2020 (INEGI). El objetivo es sintetizar múltiples privaciones sociales en un único índice por municipio, facilitar comparaciones entre municipios y entidades, y generar salidas tabulares y cartográficas reproducibles.

### Origen de los datos
- Fuente: Censo 2020 (INEGI).  
- Archivo principal utilizado: `./conjunto_de_datos/conjunto_de_datos_iter_00CSV20.csv`.  
- Shapefile de municipios: `./conjunto_de_datos/00mun.shp`.

### Descripción y preprocesamiento
- Se filtran las filas correspondientes al total por municipio (`NOM_LOC == "Total del Municipio"`).
- Se detectan y limpian valores no numéricos típicos del INEGI (ej. `"*"`, `"N/D"`), transformando columnas relevantes a tipo numérico.
- Se preservan columnas de identificación (ENTIDAD, NOM_ENT, MUN, NOM_MUN, etc.) como texto/categoría.

### Indicadores construidos
Se generan porcentajes que representan privaciones por municipio:
- p_analfabetismo = P15YM_AN / P_15YMAS * 100
- p_sin_escolaridad = P15YM_SE / P_15YMAS * 100
- p_sin_TV = VPH_SINRTV / VIVPAR_HAB * 100
- p_sin_TC = VPH_SINLTC / VIVPAR_HAB * 100
- p_sin_INT = VPH_SINCINT / VIVPAR_HAB * 100
- p_sin_bienes = VPH_SNBIEN / VIVPAR_HAB * 100
- p_sin_tic = VPH_SINTIC / VIVPAR_HAB * 100

### Análisis exploratorio y reducción de dimensionalidad
- Se examinan distribuciones (histogramas) y correlaciones entre variables.
- Se aplica un pipeline: StandardScaler + PCA para reducir dimensionalidad.
- Se evalúa la varianza explicada y se visualiza un biplot de las primeras componentes.

### Construcción del índice de marginación
- Se usa la primera componente principal (PC1) como índice sintético de marginación.
- Se normaliza el índice con MinMaxScaler para obtener `indice_marginacion_norm`.

### Salidas y productos generados
- Excel con índice municipal: `indice_marginacion_municipal.xlsx`.
- Mapa coroplético por entidad (promedio del índice) y figura guardada: `mapa_marginacion_estatico.png`.
- Gráficos interactivos (Plotly) y estáticos (Matplotlib/Seaborn) durante el notebook.

### Reproducibilidad y dependencias
- Ejecutar las celdas en orden (las importaciones y configuraciones principales están en la celda ya provista).
- Librerías principales usadas: pandas, numpy, geopandas, scikit-learn, matplotlib, seaborn, plotly, openpyxl.
- Archivos de entrada deben estar en `./conjunto_de_datos/`.

### Interpretación y siguientes pasos sugeridos
- El índice sintetiza privaciones; valores mayores indican mayor marginación relativa en la muestra.
- Validar con indicadores socioeconómicos externos y ajustar la selección/ponderación de variables.
- Explorar agrupaciones espaciales, análisis por cuantiles y generación de mapas interactivos para difusión.

Para su uso, contactar con el dueño del repositorio para los datos correspondientes.