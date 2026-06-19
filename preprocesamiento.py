import os
def limpiador(texto: str) -> list[str]:
    if not texto:
        return []
    
    text_lower = texto.lower()
    signos = '!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~¡¿""'
    texto_sin_signo = ""

    for caracter in text_lower:
        if caracter not in signos:
            texto_sin_signo += caracter

    token = texto_sin_signo.split()
    return token


def generar_vocabulario(documentos: dict[str, str]) -> list[str]:
    palabras_unicas = set()
    for texto in documentos.values():
        tokens = limpiador(texto)
        for palabra in tokens:
            palabras_unicas.add(palabra)
    vocabulario = sorted(palabras_unicas)
    return vocabulario

def frecuencia_palabras(tokens: list[str], vocabulario: list[str]) -> list[int]:
    vector = []
    for palabra in vocabulario:
        conteo = 0
        for token in tokens:
            if token == palabra:
                conteo += 1
        vector.append(conteo)
    return vector


def cargar_documentos(ruta_carpeta: str) -> dict[str, str]:
    documentos = {}
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            with open(ruta_completa, "r", encoding="utf-8") as f:
                documentos[archivo] = f.read()
    return documentos