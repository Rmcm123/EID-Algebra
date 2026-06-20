import math
from preprocesamiento import limpiador, frecuencia_palabras

# Parte 2: matriz documento-termino y matematicas vectoriales
# Usa el vocabulario que genera el integrante 1 con generar_vocabulario()


def construir_matriz(documentos: dict[str, str], vocabulario: list[str]) -> list[list[int]]:
    # cada fila es un documento, cada columna es una palabra del vocabulario
    matriz = []
    for texto in documentos.values():
        tokens = limpiador(texto)
        fila = frecuencia_palabras(tokens, vocabulario)
        matriz.append(fila)
    return matriz


def sparsidad(matriz: list[list[int]]) -> float:
    # cuenta cuantos ceros hay en total, para ver que tan "vacia" es la matriz
    ceros = 0
    total = 0
    for fila in matriz:
        for valor in fila:
            total += 1
            if valor == 0:
                ceros += 1
    return ceros / total


def producto_punto(u: list[float], v: list[float]) -> float:
    # u . v = suma de cada par de componentes multiplicados
    suma = 0
    for i in range(len(u)):
        suma += u[i] * v[i]
    return suma


def norma(v: list[float]) -> float:
    # largo del vector: raiz de la suma de los cuadrados
    suma = 0
    for valor in v:
        suma += valor ** 2
    return math.sqrt(suma)


def similitud_coseno(u: list[float], v: list[float]) -> float:
    # cos(theta) = (u . v) / (norma(u) * norma(v))
    # si algun vector es todo ceros no se puede dividir, así que devolvemos 0
    norma_u = norma(u)
    norma_v = norma(v)

    if norma_u == 0 or norma_v == 0:
        return 0

    return producto_punto(u, v) / (norma_u * norma_v)
