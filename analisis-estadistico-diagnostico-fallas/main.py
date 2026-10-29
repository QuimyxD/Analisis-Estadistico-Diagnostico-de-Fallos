import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Carpeta donde se encuentra este codigo de python
script_dir = Path(__file__).resolve().parent

# Buscar la carpeta de la librería dentro del proyecto
rutas_busqueda = [script_dir] + [
    p for p in script_dir.iterdir() if p.is_dir()
]

for ruta in rutas_busqueda:
    if (ruta / "estadistica_analitica_lib").is_dir():
        sys.path.insert(0, str(ruta))
        break

# Importar las funciones estadísticas
from estadistica_analitica_lib import Tendencias as tend
from estadistica_analitica_lib import Dispersion as disp
from estadistica_analitica_lib import Forma as forma


# Definir la ruta base del proyecto usando pathlib
base_dir = Path(__file__).resolve().parent

# Crear subcarpeta de resultados
resultados_dir = base_dir / "Resultados" / "Subcarpeta_Resultados"
resultados_dir.mkdir(parents = True, exist_ok = True)

# Lista de archivos en orden Estado Sano, Falla A, Falla B, Falla C
archivos_csv = [
    "1_c0000c30c100.csv",  # Estado Sano
    "0_c2264c30c100.csv",  # Condicion de Falla A
    "2_c0759c30c100.csv",  # Condicion de Falla B
    "3_c1513c30c100.csv",  # Condicion de Falla C
    ]

nombres_estados = ["Sano", "Falla A", "Falla B", "Falla C"]
nombres_canales = ["CH2", "CH3", "CH4"]

lista_estados = []

for archivo in archivos_csv:
    ruta_archivo = base_dir / archivo
    # Cargar datos saltando las primeras 20 líneas de metadatos
    # Usamos las columnas 1, 2 y 3 (CH2, CH3, CH4), sin la columna del tiempo (columna 0)
    datos_matriz = np.loadtxt(ruta_archivo, delimiter = ",", skiprows = 21, usecols = (1, 2, 3))
    lista_estados.append(datos_matriz)

# Construir el tensor tridimensional (N_estados, N_muestras, N_fases) -> (4, 100000, 3)
tensor_datos = np.stack(lista_estados, axis = 0)
 
n_estados, n_muestras, n_fases = tensor_datos.shape
print(
    f"Dimensiones del tensor final: {tensor_datos.shape} (Estados, Muestras, Canales)"
)


# Calculos estadisticos y guardado de estos mismos datos
# Seleccion de 10 metricas estaisticas con las librerias propias

nombres_metricas = [
    "Media",
    "Mediana",
    "Moda",
    "Varianza",
    "Desv_Esta+",
    "Rango",
    "RMS",
    "Fact_Cresta",
    "Sesgo",
    "Curtosis",
]

n_metricas = len(nombres_metricas)

# Matriz 3D para almacenarlos (N_estados, N_canales, N_metricas)
matriz_estadisticos = np.zeros((n_estados, n_fases, n_metricas))

def calcular_rms(x):
    return np.sqrt(np.mean(np.square(x)))


def calcular_factor_cresta(x):
    rms_val = calcular_rms(x)
    return np.max(np.abs(x)) / rms_val if rms_val != 0 else 0


for e in range(n_estados):
    for c in range(n_fases):
        col = tensor_datos[e, :, c]

        # Funciones de libreria propia
        m_media = tend.media(col) if hasattr(tend, "media") else np.mean(col)
        m_mediana = (tend.mediana(col) if hasattr(tend, "mediana") else np.median(col))
        m_moda = tend.moda(col) if hasattr(tend, "moda") else col[0]

        m_var = (disp.varianza(col) if hasattr(disp, "varianza") else np.var(col))
        m_std = (
            disp.desviacion_estandar(col)
            if hasattr(disp, "desviacion_estandar")
            else np.std(col)
        )
        m_rango = (
            disp.rango(col)
            if hasattr(disp, "rango")
            else (np.max(col) - np.min(col))
        )

        m_rms = calcular_rms(col)
        m_fc = calcular_factor_cresta(col)

        m_sesgo = (
            forma.sesgo(col)
            if hasattr(forma, "sesgo")
            else float(
                np.mean((col - np.mean(col)) ** 3) / (np.std(col) ** 3 + 1e-12)
            )
        )
        m_curt = (
            forma.curtosis(col)
            if hasattr(forma, "curtosis")
            else float(
                np.mean((col - np.mean(col)) ** 4) / (np.std(col) ** 4 + 1e-12)
            )
        )

        matriz_estadisticos[e, c, :] = [
            m_media,
            m_mediana,
            m_moda,
            m_var,
            m_std,
            m_rango,
            m_rms,
            m_fc,
            m_sesgo,
            m_curt,
        ]

# Guardar los resultados en .txt y .csv
ruta_txt = resultados_dir / "resumen_estadistico.txt"
ruta_csv = resultados_dir / "resumen_estadistico.csv"

with open(ruta_txt, "w") as f:
    f.write("Metricas estadisticas y su canal\n")
    f.write("\n")
    for e_idx, est in enumerate(nombres_estados):
        f.write(f"\nESTADO: {est}\n")
        header = (
            f"{'Metrica':<18} "
            + " ".join([f"{ch:>12}" for ch in nombres_canales])
            + "\n"
        )
        f.write(header)
        for m_idx, met in enumerate(nombres_metricas):
            val_ch2 = matriz_estadisticos[e_idx, 0, m_idx]
            val_ch3 = matriz_estadisticos[e_idx, 1, m_idx]
            val_ch4 = matriz_estadisticos[e_idx, 2, m_idx]
            f.write(
                f"{met:<18} {val_ch2:12.5f} {val_ch3:12.5f} {val_ch4:12.5f}\n"
            )



# Impresion de 3 tablas en la consola
print("\n")
print("Resumen de metricas por cada canal")
print("\n")

for c_idx, canal in enumerate(nombres_canales):
    print(f"\nTABLA DEL CANAL {canal}")
    
    # Encabezado con los nombres de las 10 metricas
    header_str = f"{'Estado':<10}" + "".join([f"{m:>13}" for m in nombres_metricas])
    print(header_str)
    print("-" * len(header_str))
    
    # Filas con los datos de cada estado para el canal actual
    for e_idx, est in enumerate(nombres_estados):
        row_str = f"{est:<10}" + "".join(
            [f"{matriz_estadisticos[e_idx, c_idx, m_idx]:13.4f}" for m_idx in range(n_metricas)]
        )
        print(row_str)
print("\n")

# Visualizar diagnostico
colores = ["red", "yellow", "purple", "blue"]  # colores: rojo, amarillo, morado, azul



# Diagramas de caja (Boxplots) comparativos para CH2
plt.figure(figsize = (10, 6))
datos_ch2 = [tensor_datos[e, :, 0] for e in range(n_estados)]
bplot = plt.boxplot(
    datos_ch2,
    patch_artist = True,
    labels = nombres_estados,
    flierprops = dict(marker = ".", markersize = 1, alpha = 0.1),
) 

for patch, color in zip(bplot["boxes"], colores):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

plt.title(
    "Comparación de la distribución de señal (CH2) entre el estado Sano y estado de fallas",
    fontsize = 12,
    fontweight = "bold",
)
plt.xlabel("Condicion del motor de induccion", fontsize = 10)
plt.ylabel("Amplitud de la senal", fontsize = 10)
plt.grid(True, linestyle = "--", alpha = 0.5)
plt.tight_layout()

ruta_boxplot = resultados_dir / "boxplot_comparativo_CH2.png"
plt.savefig(ruta_boxplot, dpi = 300)
plt.close()




# Grafico de barras agrupadas para hacer la comparacion de media aritmetica
fig, ax = plt.subplots(figsize = (10, 5))
# Ancho de las barras y posiciones x para cada estado
bar_width = 0.25
x = np.arange(n_estados)
colores_fases = ["purple","yellow", "skyblue"]
etiquetas_fases = ["Fase 1 (CH2)", "Fase 2 (CH3)", "Fase 3 (CH4)"]

# 3 barras para cada uno de los 4 estados
for c_idx in range(n_fases):
    # Valor de la media (índice 0 en nombres_metricas) para todos los estados
    medias_fase = matriz_estadisticos[:, c_idx, 0]
    posiciones = x + (c_idx - 1) * bar_width

    rects = ax.bar(
        posiciones,
        medias_fase,
        bar_width,
        label = etiquetas_fases[c_idx],
        color = colores_fases[c_idx],
        edgecolor = "black",
        linewidth = 0.5,
    )

    # Agregar las etiquetas con los valores exactos encima de cada barra
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f"{height:.4f}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext = (0, 3),  # Desplazamiento en vertical de 3 puntos
            textcoords = "offset points",
            ha = "center",
            va = "bottom",
            fontsize = 8,
        )

ax.set_title(
    "Comparación de Media Aritmética por Condición y Fase", fontsize = 12
)
ax.set_xlabel("Condición Operativa", fontsize = 10)
ax.set_ylabel("Media de la Amplitud", fontsize = 10)
ax.set_xticks(x)
ax.set_xticklabels(nombres_estados)

# Ajuste fino del eje Y y cuadricula horizontal
ax.set_ylim(1.64, 1.71)
ax.grid(axis = "y", linestyle = "-", alpha = 0.3)
ax.set_axisbelow(True)

# Leyenda en la esquina superior izquierda
ax.legend(loc = "upper left", frameon = True)

plt.tight_layout()

# Guardar la imagen en la carpeta de resultados
ruta_histograma = resultados_dir / "comparacion_media_aritmetica.png"
plt.savefig(ruta_histograma, dpi = 300)
plt.close()



# Histogramas superpuestos para el canal CH2
plt.figure(figsize = (10, 6))
for e in range(n_estados):
    plt.hist(
        tensor_datos[e, :, 0],
        bins = 100,
        density = True,
        alpha = 0.4,
        color = colores[e],
        label = nombres_estados[e],
    )

plt.title(
    "Histogramas superpuestos de densidad de probabilidad (CH2)",
    fontsize = 12,
    fontweight = "bold",
)
plt.xlabel("Amplitud de la Senal", fontsize = 10)
plt.ylabel("Densidad de Probabilidad", fontsize = 10)
plt.legend(loc = "upper right", frameon = True)
plt.grid(True, linestyle = "--", alpha = 0.5)
plt.tight_layout()

ruta_histograma = resultados_dir / "histograma_superpuesto_CH2.png"
plt.savefig(ruta_histograma, dpi = 300)
plt.close()


print(f"Graficos guardados en la siguiente carpeta: {resultados_dir}")







# Analisis y discusion (preguntas)
print("\n")
print("Analisis y discusion de resultados")
print("\n")

print("Nombre: Cecil Quimey Azuara Yáñez","\n","Fecha: 23 octubre de 2026\n")

print("""
1. ¿Qué métrica o canal muestra la mayor sensibilidad o la mayor desviación respecto al estado sano?
Respuesta: En cuanto a las métricas, la media aritmética y las métricas de energía/dispersión (como RMS y Varianza) muestran la mayor sensibilidad respecto al estado sano. 
Específicamente, la media registra un incremento notable al pasar del estado Sano (alrededor de 1.6579 - 1.6699) a las condiciones con falla (alcanzando valores entre 1.6755 y 1.6958). 
La moda también presenta variaciones drásticas debido al comportamiento bimodal de la señal.

Respecto a los canales, el canal CH2 (Fase 1) destaca por registrar los valores medios más altos en todas las condiciones operativas (Sano y Fallas) 
en comparación con CH3 y CH4, siendo el canal que mejor refleja el incremento en el nivel medio de la señal ante la presencia de anomalías.


2. ¿Es posible separar o clasificar claramente los diferentes niveles de falla basándose únicamente en este análisis estadístico descriptivo?
Respuesta: No, no es posible clasificar o separar claramente los diferentes estados basándose únicamente en la estadística descriptiva en el dominio del tiempo.

Al examinar tanto el diagrama de cajas (Boxplot) como el histograma superpuesto de densidad de probabilidad para CH2, se aprecia que las distribuciones 
de amplitud de los cuatro estados (Sano, Falla A, Falla B y Falla C) coinciden de forma casi exacta en rango, cuartiles y forma bimodal. Debido a esto, 
los estadísticos globales no ofrecen la resolución necesaria para diagnosticar de forma discriminatoria el tipo o severidad de la falla.\n

"""
)
