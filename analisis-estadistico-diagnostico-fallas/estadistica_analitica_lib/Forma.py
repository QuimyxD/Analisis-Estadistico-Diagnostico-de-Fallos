from collections import Counter
import math

# Momentos, sesgo y curtosis

"""
xj = lista de marcas de clase
fj = lista de frecuencias absolutas
N = total de observaciones (sum(fj))
media = media aritmetica (mu)
De = desviacion estandar (sigma)
r = orden del momento (1, 2, 3, 4)
A = origen arbitrario
"""


# Momentos

def MomentoCrudo(fj: list, xj: list, r: int) -> float:
    N = sum(fj)
    suma = sum(f * (x ** r) for f, x in zip(fj, xj)) # sumatoria de (fj * xj^r) / N

    return suma / N

def MomentoCentral(fj: list, xj: list, media: float, r: int) -> float:
    N = sum(fj)
    suma = sum(f * ((x - media) ** r) for f, x in zip(fj, xj)) # sumatoria de (fj * (xj - media)^r) / N

    return suma / N

def MomentoArbitrario(fj: list, xj: list, A: float, r: int) -> float:
    N = sum(fj)
    suma = sum(f * ((x - A) ** r) for f, x in zip(fj, xj))

    return suma / N

def MomentoAdimensional(fj: list, xj: list, media: float, De: float, r: int) -> float:
    mr = MomentoCentral(fj, xj, media, r)

    return mr / (De ** r)



# Sesgo

def SesgoFisherPearson(fj: list, xj: list, media: float, De: float) -> float:
    m3 = MomentoCentral(fj, xj, media, 3)

    return m3 / (De ** 3)

def SesgoPearson1(media: float, moda: float, De: float) -> float:
    return (media - moda) / De

def SesgoPearson2(media: float, mediana: float, De: float) -> float:
    return (3 * (media - mediana)) / De

def SesgoCuantiles(Q1: float, Q2: float, Q3: float) -> float:
    return (Q3 + Q1 - (2 * Q2)) / (Q3 - Q1)

def CriterioAsimetria(gamma1: float) -> str:
    abs_g1 = abs(gamma1)
    if abs_g1 < 0.5:
        return "Asimetria leve" 
    elif 0.5 <= abs_g1 < 1.0:
        return "Asimetria moderada"
    else:
        return "Asimetria severa"

    

# Curtosis

def ExcesoCurtosis(fj: list, xj: list, media: float, De: float) -> float:
    m4 = MomentoCentral(fj, xj, media, 4)
    return (m4 / (De ** 4)) - 3

def TipoCurtosis(kappa: float) -> str:
    if kappa == 0:
        return "Mesocúrtica"
    elif kappa > 0:
        return "Leptocúrtica"
    else:
        return "Platicúrtica"

def CurtosisPercentilica(P90: float, P10: float, P75: float, P25: float) -> float:
    return (P90 - P10) / (P75 - P25)



# Audioria automatica
if __name__ == "__main__":

    print("\nAuditoria: Modulo Forma")
    # Datos de prueba
    xj_prueba = [15.0, 25.0, 35.0, 45.0, 55.0]
    fj_prueba = [5, 10, 20, 10, 5]
    media_prueba = 35.0
    de_prueba = 10.0
    
    m1 = MomentoCrudo(fj_prueba, xj_prueba, 1)
    m2 = MomentoCentral(fj_prueba, xj_prueba, media_prueba, 2)
    sesgo = SesgoFisherPearson(fj_prueba, xj_prueba, media_prueba, de_prueba)
    curt = ExcesoCurtosis(fj_prueba, xj_prueba, media_prueba, de_prueba)
    
    print(f"Momento Crudo 1: {m1:.4f}")
    print(f"Momento Central 2: {m2:.4f}")
    print(f"Sesgo Fisher: {sesgo:.4f} ({CriterioAsimetria(sesgo)})")
    print(f"Exceso Curtosis: {curt:.4f} ({TipoCurtosis(curt)})")