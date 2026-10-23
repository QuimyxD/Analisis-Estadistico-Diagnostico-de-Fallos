# Analisis-Estadistico-Diagnostico-de-Fallos
Este repositorio contiene un módulo de Análisis Exploratorio de Datos (EDA) y procesamiento estadístico desarrollado en Python para un conjunto de datos de mantenimiento de dispositivos. El proyecto permite calcular medidas de tendencia central y dispersión (tanto para datos agrupados como no agrupados) y generar automatizadamente visualizaciones estadísticas anotadas.

Estructura del Proyecto (Anatomía de Carpetas)
A continuación se muestra la evolución de la estructura del repositorio antes y después de la ejecución del script principal de generación de gráficos e informes.

---

## 1. Estado Inicial (Antes de generar gráficos y TXT)
Antes de ejecutar los scripts de análisis, el proyecto cuenta únicamente con el código fuente y los archivos CSV de datos en la raíz:


```text
analisis-estadistico-diagnostico-fallas/
├── 0_c2264c30c100.csv
├── 1_c0000c30c100.csv
├── 2_c0759c30c100.csv
├── 3_c1513c30c100.csv
├── graficos.py
├── main.py
└── README.md
```

---

## 2. Estado Final (Después de generar gráficos y TXT)
Tras la ejecución del pipeline de análisis, el programa crea dinámicamente carpetas de salida (output/ o graficos/), exportando las visualizaciones en formato imagen y el resumen estadístico descriptivo en un archivo de texto (.txt):

```text
analisis-estadistico-diagnostico-fallas/
├── 0_c2264c30c100.csv
├── 1_c0000c30c100.csv
├── 2_c0759c30c100.csv
├── 3_c1513c30c100.csv
├── graficos.py
├── main.py
├── README.md
├── resultados_analisis.txt
└── output_graficos/
    ├── distribucion_fallas.png
    ├── histograma_tendencia_central.png
    ├── boxplot_multimetrico.png
    └── dispersion_fallas.png
```


---

## Funcionalidades Principales

## Cálculo de Estadísticos: Computo exacto y estimado de media, mediana, moda y varianza muestral para distribuciones de datos agrupados y no agrupados.

## Visualización de Datos:

Histogramas anotados comparando medidas exactas vs. estimadas de tendencia central.

Diagramas de caja (Boxplots) multimétricos para la detección de valores atípicos (outliers).

Gráficos de dispersión (Scatter plots) para evaluar correlaciones entre variables de falla.

Gráficos de barras para frecuencias categóricas de tipos de falla.

Exportación Dinámica: Gestión de rutas mediante pathlib para guardar automáticamente los reportes e imágenes generados.

---

## Requisitos e Instalación

Para ejecutar este proyecto, asegúrate de tener instalado Python 3.8+ y las siguientes librerías:
pip install pandas numpy matplotlib seaborn

---

## Uso

Ejecuta el script principal para procesar los archivos CSV y generar los entregables:
python main.py

Las imágenes generadas se guardarán automáticamente en la carpeta de salida y las métricas se escribirán en el archivo .txt correspondiente.


---

## Autor y Créditos

**Cecil Quimey Azuara Yáñez**

- **Carrera:** Licenciatura en Ingeniería de Datos e Inteligencia Artificial (LIDIA).
- **Institución:** Universidad de Guanajuato – División de Ingenierías (Campus Irapuato - Salamanca).
- **Asignatura:** Estadística Inferencial.
