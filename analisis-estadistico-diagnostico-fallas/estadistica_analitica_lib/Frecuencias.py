from collections import Counter
import math

# Modulo de Distribucion de Frecuencias
"""
datos = lista de datos crudos
k = número de clases/intervalo
R = rango de los datos
c = amplitud del intervalo
limInf = lista de límites inferiores reales
limSup = lista de límites superiores reales
xj = lista de marcas de clase
fj = lista de frecuencias absolutas
Fj = lista de frecuencias acumuladas
hj = lista de frecuencias relativas
Hj = lista de frecuencias relativas acumuladas
FAB = frecuencia absoluta
FA = frecuencia acumulada
FR = frecuencia relativa
FRA = frecuencia relativa acumulada
"""


# Informacion necesaria 

def TotalClases(N: int):
    k_calculado = 1 + (3.322 * math.log10(N))
    k = int(k_calculado)
    if k_calculado > k:
        k += 1

    return k


# buscar rangos
def RangoDatos(datos: list):
    return max(datos) - min(datos)


# definir amplitud
def Amplitud(rango: float, k: int):
    return rango / k


# sacar limites
def LimitesReales(datos: list, k: int, c: float):
    val_min = min(datos)
    limInf = []
    limSup = []
    
    actual = val_min
    for i in range(k):
        limInf.append(actual)
        actual += c
        limSup.append(actual)
        
    return limInf, limSup


# marca de clase 
def MarcaClase(limInf: list, limSup: list) -> list:
    xj = [(sup + inf) / 2 for inf, sup in zip(limInf, limSup)]

    return xj


def FAB(datos: list, limInf: list, limSup: list) -> list: # frecuencia absoluta
    fj = []
    k = len(limInf)
    
    for i in range(k):
        cont = 0
        inf = limInf[i]
        sup = limSup[i]
        
        for j in datos:
            if i == k - 1:
                if inf <= j <= sup:
                    cont += 1
            else:
                if inf <= j < sup:
                    cont += 1
                    
        fj.append(cont)
        
    return fj


def FA(fj: list) -> list: # frecuencia acumulada
    Fj = []
    cont = 0
    for f in fj:
        cont += f
        Fj.append(cont)

    return Fj


def FR(fj: list, N: int) -> list: # frecuencia relativa
    hj = [f / N for f in fj]

    return hj


def FRA(hj: list) -> list: # frecuencia relativa acumulada
    Hj = []
    cont = 0.0
    for h in hj:
        cont += h
        Hj.append(cont)

    return Hj


# Generacion de tabla de frecuencias
def TablaFrecuencias(datos: list) -> dict:
    N = len(datos)
    k = TotalClases(N)
    R = RangoDatos(datos)
    c = Amplitud(R, k)
    
    limInf, limSup = LimitesReales(datos, k, c)
    xj = MarcaClase(limInf, limSup)
    fj = FAB(datos, limInf, limSup)
    Fj = FA(fj)
    hj = FR(fj, N)
    Hj = FRA(hj)
    
    return {"N": N, "k": k, "R": R, "c": c, "limInf": limInf, "limSup": limSup, "xj": xj, "fj": fj, "Fj": Fj, "hj": hj, "Hj": Hj}







# Auditoria automatica
if __name__ == "__main__":
    print("\nAuditoria: Modulo Frecuencias")

    # Datos de prueba
    datos_prueba = [12, 15, 22, 25, 28, 30, 33, 35, 40, 45, 50, 55]
    tabla = TablaFrecuencias(datos_prueba)
    
    print(f"Total Datos (N): {tabla['N']}")
    print(f"Num Clases (k): {tabla['k']}")
    print(f"Amplitud (c): {tabla['c']:.2f}")
    print(f"Frecuencias (fj): {tabla['fj']}")