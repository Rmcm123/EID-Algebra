import preprocesamiento as pp
import matriz_vectorial as mv

def vectorizar_consulta(consulta, vocabulario) -> list[int]:
    # Convierte la consulta en un vector de frecuencias de palabras, 
    # usando el mismo vocabulario que se usó para construir la matriz documento-termino.
    consulta_limpia = pp.limpiador(consulta)
    consulta_vectorizada = pp.frecuencia_palabras(consulta_limpia, vocabulario)

    return consulta_vectorizada

def calcular_similitudes(vector_consulta, matriz, nombres_documentos) -> list[tuple[str, float]]:
    # Calcula la similitud entre el vector de la consulta y cada vector de documento en la matriz, 
    # devolviendo una lista de tuplas con el nombre del documento y su similitud.
    similitudes = []
    
    if len(nombres_documentos) != len(matriz):
        raise ValueError("El número de nombres de documentos no coincide con el número de vectores en la matriz.")
    
    for nombre, vector_documento in zip(nombres_documentos, matriz):
        similitud = mv.similitud_coseno(vector_consulta, vector_documento)
        similitudes.append((nombre, similitud))
    
    return similitudes

def ordenar_resultados(resultados, cantidad=3, umbral=0.0) -> list[tuple[str, float]]:
    # Ordena los resultados por similitud y devuelve solo los mejores, filtrando por un umbral mínimo de similitud.
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero")

    resultados_filtrados = [
        resultado for resultado in resultados 
        if resultado[1] > umbral # Filtra los resultados que tienen una similitud mayor que el umbral
        ]
    
    resultados_ordenados = sorted(
        resultados_filtrados, 
        key=lambda resultado: resultado[1],  # Ordena por la similitud (segundo elemento de la tupla)
        reverse=True) # Orden descendente para que los más similares estén primero
    
    return resultados_ordenados[:cantidad]

def buscar(consulta, vocabulario, matriz, nombres_documentos, cantidad=3, umbral=0.0) -> list[tuple[str, float]]:
    # Busca los documentos más relevantes para la consulta dada, usando el vocabulario y la matriz documento-termino ya construidos. 
    
    if not consulta or not consulta.strip(): 
        # Si la consulta es vacía o solo tiene espacios, no tiene sentido buscar, así que devolvemos una lista vacía
        return []
    
    if umbral < 0 or umbral > 1:
        raise ValueError("El umbral debe estar entre 0 y 1")

    vector_consulta = vectorizar_consulta(consulta, vocabulario)

    
    if not any(vector_consulta): 
        # Si el vector de la consulta es todo ceros, no tiene sentido buscar, así que devolvemos una lista vacía
        return []

    similitudes = calcular_similitudes(vector_consulta, matriz, nombres_documentos)
    resultados_ordenados = ordenar_resultados(similitudes, cantidad, umbral)

    return resultados_ordenados