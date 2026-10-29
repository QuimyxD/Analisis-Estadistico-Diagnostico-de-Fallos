from collections import Counter
import math

"""
rango = rango
RSI = rango semi-intercuartilico
Interpolar = interpolacion
DesvMedia (Dm) = Desviacion media
Varianza (var) = varianza
DesvEstandar (De) = Desviacion Estandar
mediaAritmetica = mu
Chebyshev = teorema de Chebyshev
Zscore (Z) = Z-Score
CV = coeficiente de variacion
"""

# Rnago
def Rango(xj):
    xk = xj[-1] # ultima marca de clase
    x1 = xj[0] # primera marca de clase

    rango = xk - x1

    return rango 

# Rango Semi-Intercuartilico
def RSI(Q3, Q1):
    RSI = Q3 - Q1 / 2

    return RSI

# Interpolacion
def Interpolar(F_anterior, fj_cuantil, limInf, c): # Metodo de interpolacion
    posicion = (K * N) / 4
    return limInf + ((posicion - F_anterior) / fj_cuantil) * c

# Desviacion media
def DesvMedia(fj, xj, media):
    N = sum(fj)
    suma_desviaciones = sum(f * abs(x - media) for f, x in zip(fj, xj)) # Dm = (1/N) * sum( fj * |xj - mu| )
    Dm = suma_desviaciones / N

    return Dm


# Varianza
def Varianza(fj, xj, media):
    N = sum(fj)
    suma_cuadrados = sum(f * ((x - media) ** 2) for f, x in zip(fj, xj)) # var = sum( fj * (xj - mu)^2 ) / N

    return suma_cuadrados / N


# Desviacion estandar
def DesvEstandar(var):
    De = math.sqrt(var) # Raiz cuadraa de la varianza

    return De

# Teorema de Chebyshev
def Chebyshev(K):
    if K <= 1:
        raise ValueError("El valor de \"K\" debe ser mayor a 1.")
    
    return 1 - (1 / (K ** 2))

# Z-Score
def Zscore(X, De, media):
    Z = (X - media) / De

    return Z

# Coeficiente de variacion
def CV(De, media):
    CV = (De / media) * 100

    return CV



# Auditoria automatica
if __name__ == "__main__":

    print("\nAuditoria: Modulo Dispersión")
    # Datos de prueba
    xj_prueba = [15.0, 25.0, 35.0, 45.0, 55.0]
    fj_prueba = [5, 10, 20, 10, 5]
    media_prueba = 35.0
    
    rango_val = Rango(xj_prueba)
    dm_val = DesvMedia(fj_prueba, xj_prueba, media_prueba)
    var_val = Varianza(fj_prueba, xj_prueba, media_prueba)
    de_val = DesvEstandar(var_val)
    cv_val = CV(de_val, media_prueba)
    
    print(f"Rango: {rango_val:.4f}")
    print(f"Desviacion Media: {dm_val:.4f}")
    print(f"Varianza: {var_val:.4f}")
    print(f"Desviacion Estandar: {de_val:.4f}")
    print(f"Coeficiente Var(%): {cv_val:.4f}%")