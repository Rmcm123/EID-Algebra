import os

STOPWORDS_ES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "al", "a", "en", "con", "por", "para",
    "y", "o", "e", "u", "ni", "que", "es", "son", "se",
    "su", "sus", "lo", "le", "les", "me", "te", "nos",
    "mi", "tu", "yo", "él", "ella", "ello", "nosotros",
    "ellos", "ellas", "este", "esta", "estos", "estas",
    "ese", "esa", "esos", "esas", "aquel", "aquella",
    "como", "pero", "más", "mas", "si", "no", "ya",
    "muy", "tan", "entre", "sobre", "sin", "hasta",
    "desde", "donde", "cuando", "también", "fue", "ha",
    "hay", "ser", "estar", "tiene", "tienen", "puede",
    "era", "sido", "otro", "otra", "otros", "otras",
    "todo", "toda", "todos", "todas", "cada", "mismo",
    "misma", "porque", "aunque", "hacia", "después",
    "antes", "durante", "según", "contra", "mediante",
}
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
    token_filtrado = [t for t in token if t not in STOPWORDS_ES]
    return token_filtrado


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