from preprocesamiento import cargar_documentos, generar_vocabulario
from matriz_vectorial import construir_matriz, sparsidad, producto_punto, norma, similitud_coseno

# cargamos los documentos y generamos el vocabulario (esto lo hizo el integrante 1)
documentos = cargar_documentos("documentos")
vocabulario = generar_vocabulario(documentos)
nombres = list(documentos.keys())

print("Documentos:", nombres)
print("Vocabulario (", len(vocabulario), "palabras ):", vocabulario)

# ahora construimos la matriz documento-termino
matriz = construir_matriz(documentos, vocabulario)

print("\nMatriz documento-termino:")
for nombre, fila in zip(nombres, matriz):
    print(nombre, "->", fila)

print("\nDimensiones:", len(matriz), "documentos x", len(vocabulario), "palabras")
print("Sparsidad:", round(sparsidad(matriz) * 100, 2), "% de ceros")

# probamos las funciones matematicas comparando los dos primeros documentos
v1 = matriz[0]
v2 = matriz[1]

print("\nComparando", nombres[0], "con", nombres[1])
print("Producto punto:", producto_punto(v1, v2))
print("Norma", nombres[0], ":", round(norma(v1), 3))
print("Norma", nombres[1], ":", round(norma(v2), 3))
print("Similitud coseno:", round(similitud_coseno(v1, v2), 3))
