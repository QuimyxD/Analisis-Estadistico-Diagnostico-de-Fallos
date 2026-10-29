from collections import Counter
import math

# Promedios para medidas de tendencia central
""" 
xj = marca de clase
fj = frecuencias
mediaAr = media aritmetica
G = media geometrica
H = media armonica
mediana = mediana
moda = moda
RCM = raiz cuadrada media
cuantil = cuantil
posicion = Posicion del cuantil
"""


def marcaClase(limInf, limSup):
    if (limInf > limSup): # Si estan al reves hacemos un swap con una variable temporal
        temp = limInf
        limInf = limSup
        limSup = temp

    xj = (limSup + limInf) / 2    # Marca de clase

    return xj


def FrecuenciaClase(Frecuencias):
    fj = sum(Frecuencias)  # Frecuencia

    return fj


# Media aritmetica
def MediaAritmetica(fj, xj):
    fx = sum(f * x for f, x in zip(fj, xj)) # Sumatoria de frecuancias * marca de clase
    N = sum(fj) # Suma total de frecuencias
    
    mediaAr = fx / N

    return mediaAr
        

# Media geometrica para datos agrupados
def MediaGeometrica(fj, xj):
    N = sum(fj)
    suma_log = sum(f * math.log10(x) for f, x in zip(fj, xj))

    return 10 ** (suma_log / N)


# Media armonica para datos agrupados
def MediaArmonica(fj, xj):
    N = sum(fj)
    inversos = sum(f / x for f, x in zip(fj, xj))

    return N / inversos


# Mediana para datos agrupados
def Mediana(limInf, N, F_anterior, f_mediana, c):
    mediana = limInf + (((N / 2) - F_anterior) / f_mediana) * c   # Mediana = Li + [ ((N/2) - F_prev) / f_mediana ] * c

    return mediana
    


# Moda para datos agrupados
def Moda(limInf, delta1, delta2, c):
    moda = limInf + (delta1 / (delta1 + delta2)) * c # Moda = Li + [ delta1 / (delta1 + delta2) ] * c

    return moda
    


# Raiz cuadrada media (RCM) para datos agrupados
def RCM(fj, xj):
    N = sum(fj)
    suma_cuadrados = sum(f * (x ** 2) for f, x in zip(fj, xj))
    RCM = math.sqrt(suma_cuadrados / N) # RCM = sqrt( sum(fj * xj^2) / N )

    return RCM
    

# Posicion del cuantil
def PosCuantil(K, N, q):
    posicion = (K * N) / q

    return posicion

# Cuantiles para datos agrupados
def Cuantil(limInf, K, N, q, F_anterior, f_cuantil, c):
    posicion = PosCuantil(K, N, q) # Q_k = Li + [ ((K*N / q) - F_prev) / f ] * c
    cuantil = limInf + ((posicion - F_anterior) / f_cuantil) * c

    return cuantil

def Cuartil(K, limInf, N, F_anterior, f_cuantil, c):
    return Cuantil(limInf, K, N, 4, F_anterior, f_cuantil, c)

def Decil(K, limInf, N, F_anterior, f_cuantil, c):
    return Cuantil(limInf, K, N, 10, F_anterior, f_cuantil, c)

def Percentil(K, limInf, N, F_anterior, f_cuantil, c):
    return Cuantil(limInf, K, N, 100, F_anterior, f_cuantil, c)

def buscarCuantil(fj, posicion):
    for pos, acumulada in enumerate(fj):
        if acumulada >= posicion:
            return pos
        
    return len(fj) - 1


# xj = [marcaClase(inf, sup) for inf, sup in zip(limInf, limSup)] # Marca de clase



# Auditoria automatica
if __name__ == "__main__":
    print("\nAuditoria autonoma: Modulo de Tendencias")
    
    # Datos de prueba
    xj_prueba = [15.0, 25.0, 35.0, 45.0, 55.0]
    fj_prueba = [5, 10, 20, 10, 5]
    
    media = MediaAritmetica(fj_prueba, xj_prueba)
    geo = MediaGeometrica(fj_prueba, xj_prueba)
    arm = MediaArmonica(fj_prueba, xj_prueba)
    rcm_val = RCM(fj_prueba, xj_prueba)
    
    print(f"Media Aritmetica: {media:.4f}")
    print(f"Media Geometrica: {geo:.4f}")
    print(f"Media Armonica: {arm:.4f}")
    print(f"RCM: {rcm_val:.4f}")