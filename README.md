# Análisis Temporal y Espacial de la Temperatura del Aire en la Ciudad de México

Este repositorio contiene el conjunto de programas, scripts de automatización y herramientas de procesamiento estadístico desarrollados para mi proyecto de titulación en **Ingeniería Geofísica (ESIA Ticomán - IPN)**. 

El objetivo principal de la investigación es evaluar las tendencias, variabilidad estacional y anomalías térmicas en la CDMX mediante el análisis de series históricas de estaciones meteorológicas y mallas de reanálisis global.

**Asesores Institucionales:**
* **M. en C. Enrique Azpra Romero** — Instituto de Ciencias de la Atmósfera y Cambio Climático, UNAM.
* **M. en C. Leodegario Sansón Reyes** — ESIA Ticomán, IPN.

---

## Metodología y Flujo de Trabajo en Python

El análisis se ejecuta de manera directa y estructurada, aprovechando la alta calidad de los datos de reanálisis y aplicando métodos numéricos y estadísticos para su validación frente a observaciones en superficie:

1. **Gestión y Descarga de Datos Históricos:** Descarga y ordenamiento de registros meteorológicos de estaciones en superficie. Se implementaron scripts con manejo de excepciones para optimizar la reestructuración y simplificación de las bases de datos.
2. **Segmentación y Agregación Temporal:** Procesamiento y organización cronológica de variables atmosféricas a escala anual para facilitar la identificación de tendencias climáticas de largo plazo.
3. **Lectura y Proyección Directa de Reanálisis:** Apertura y extracción de variables desde mallas globales en formato **NetCDF (.nc)** procedentes de **ERA5-Land (ECMWF)**. Al tratarse de datos de reanálisis previamente depurados, se procede directamente a su mapeo y proyección.
4. **Interpolación Numérica Espacial:** Implementación nativa de un algoritmo de **interpolación lineal** en Python sobre la malla de datos para generar los campos continuos, mapas de isolíneas y la cartografía meteorológica terminada.
5. **Validación Cruzada por Eventos (Ventana de 3 Días):** Extracción directa de variables y análisis comparativo frente a las observaciones reales en superficie de reportes aeronáuticos **METAR MMOX** (Aeropuerto de Oaxaca). El análisis estadístico se enfoca en ventanas críticas de 3 días (el día del evento de interés, un día antes y un día después) para evaluar con precisión la evolución sinóptica y el sesgo (*bias*) del modelo.

---

## Tecnologías y Librerías Utilizadas

Para el desarrollo e integración de este conjunto de programas se utilizó un entorno **Ubuntu/Linux** y programación en **Python**, implementando las siguientes librerías científicas:

* **Manejo de Datos Geofísicos y Climáticos:**
  * `xarray`: Apertura, manipulación y extracción eficiente de variables en rejillas y mallas multidimensionales de reanálisis (**NetCDF**).
  * `pandas` & `numpy`: Estructuración de series temporales, arreglos matriciales, alineación anual y cálculo de estadísticas descriptivas.

* **Sistemas de Información Geográfica (SIG) y Visualización:**
  * `geopandas`: Procesamiento de datos vectoriales y delimitación espacial/geográfica.
  * `basemap` (`mpl_toolkits.basemap`): Proyección de mapas cartográficos, mallas geográficas y manejo de coordenadas terrestres.
  * `matplotlib` (`pyplot`, `gridspec`, `colors`, `mpimg`): Arquitectura de gráficos avanzada. Se implementó el backend **`matplotlib.use("Agg")`** para optimizar la generación automatizada de imágenes directamente en servidor (sin interfaz gráfica), mapas de isolíneas y paletas de colores personalizadas (`LinearSegmentedColormap`).

* **Automatización y Control de Errores:**
  * `urllib.request` & `urllib.error`: Automatización de peticiones HTTP para la adquisición de datos históricos con manejo robusto de excepciones (control de errores 404 en servidores meteorológicos).
  * `pathlib`, `os` & `re`: Gestión de rutas de archivos en el sistema operativo y expresiones regulares para el filtrado cronológico de bases de datos.

---

## Resultados y Visualizaciones Climáticas

A continuación se presentan los productos generados de forma automatizada mediante los scripts de este repositorio, procesando variables atmosféricas horarias para el periodo histórico:

* **Dinámica Térmica y Pluviométrica:** Mapas espaciales de Temperatura a 2m y Precipitación horaria con escalas normalizadas.
* **Campos de Viento y Radiación:** Representación vectorial de la dirección y velocidad del viento a 10 metros mediante líneas de corriente (streamlines), junto con el análisis de Radiación incidente horaria.
* **Series Temporales:** Gráficas analíticas de tendencias y variabilidad temporal para cada variable meteorológica.

![Resultados Técnicos ERA5-Land](TODO_anio_mes_dia_horaUTC_pruebas01.png)
*Nota: Nomenclatura del prototipo de salida automatizada: `TODO_{anio}_{mes:02d}_{dia:02d}_{hora:02d}UTC_pruebas01.png`. El código está estructurado de forma modular para permitir la escalabilidad y optimización continua de los productos visuales.*
g)

---

## Estructura de los Scripts

Los códigos fuente están organizados en el directorio principal bajo la siguiente arquitectura funcional:

* `01_data_management.py`: Script para el ordenamiento simplificado, gestión de peticiones HTTP con control de errores y estructuración de registros meteorológicos crudos.
* `02_temporal_alignment.py`: Algoritmo para la organización de variables atmosféricas en escalas anuales.
* `03_era5_processor_and_interpolation.py`: Código principal encargado de la lectura del archivo `.nc`, proyección directa de la malla, ejecución de la interpolación lineal y generación de mapas con líneas de corriente operando bajo el backend *Agg*.
* `04_metar_validation_3days.py`: Script de análisis estadístico enfocado en la extracción, comparación directa y evaluación de discrepancias en ventanas de 3 días entre ERA5-Land y reportes METAR (MMOX).

---
 **Contacto:**  
Abisai Jiménez Pérez – [abisaijimenezperez_est@esiaticipnct.com]  
Estudiante de Ingeniería Geofísica - Instituto Politécnico Nacional
