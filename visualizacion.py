import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from preprocesamiento import cargar_documentos, generar_vocabulario
from matriz_vectorial import construir_matriz, similitud_coseno
from motor_busqueda import buscar, vectorizar_consulta

#configuraciones iniciales para matplotlib
plt.rcParams.update({
    "font.family" : "DejaVu Sans",
    "axes.spines.top" : False,
    "axes.spines.right" : False,
    "figure.facecolor" : "#F7F9FC",
    "axes.facecolor" : "#F7F9FC",
    "axes.titleweight" : "bold",
    "axes.titlesize" : 13,
    "axes.labelsize" : 11,
})

COLOR_DOCS = "#2563EB"
COLOR_QUERIES = "#DC2626"
COLOR_MEJOR = "#16A34A"

#construye una matriz cuadrada que contiene las similitudes coseno mutuas entre todos los documentos
def _matriz_sim_docs(matriz: list[list[int]]) -> np.ndarray:
    n = len(matriz)
    sim = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            sim[i, j] = similitud_coseno(matriz[i], matriz[j])
    return sim

#construye una matriz de similitud para evaluar el comportamiento de las búsquedas
def _matriz_sim_consultas(vectores_q: list[list[int]], matriz: list[list[int]]) -> np.ndarray:
    sim = np.zeros((len(vectores_q), len(matriz)))
    for i, vq in enumerate(vectores_q):
        for j, vd in enumerate(matriz):
            sim[i, j] = similitud_coseno(vq, vd)
    return sim

#reduce la dimensionalidad de los vectores a solo 2 dimensiones, permitiendo su representación en un plano cartesiano
def _pca_2d(vectores: list[list[float]]) -> np.ndarray:
    X = np.array(vectores, dtype=float)
    ns = np.linalg.norm(X, axis=1, keepdims = True)
    ns[ns == 0] = 1
    X = X / ns
    X -= X.mean(axis=0)
    d, d, Vt = np.linalg.svd(X, full_matrices = False)
    n_comp = min(2, Vt.shape[0])
    coords = X @ Vt[:n_comp].T
    if coords.shape[1] < 2:
        coords = np.hstack([coords, np.zeros((coords.shape[0], 2 - coords.shape[1]))])
    return coords 

#genera un mapa de calor que ilustra la afinidad entre los documentos del proyecto
def graficar_similitudes_docs(sim: np.ndarray, nombres: list[str], archivo: str = "fig1_similitud_documentos.png") -> None:
    n = len(nombres)
    fig, ax = plt.subplots(figsize=(max(6, n), max(5, n * 0.85)))
    im = ax.imshow(sim, cmap="YlOrRd", vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label="Similitud coseno")
    etiq = [name.replace(".txt", "") for name in nombres]
    ax.set_xticks(range(n))
    ax.set_xticklabels(etiq, rotation=0)
    ax.set_yticks(range(n))
    ax.set_yticklabels(etiq)
    for i in range(n):
        for j in range(n):
            val = sim[i, j]
            color_txt = "white" if val > 0.6 else "#1E293B"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=10, color=color_txt, fontweight="bold")

    ax.set_title("Similitud coseno entre documentos", pad=14)
    ax.set_xlabel("Documento"); ax.set_ylabel("Documento")
    plt.tight_layout()
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    print(f"[1/4] Guardado: {archivo}")
    plt.show()

#genera otro mapa de calor enfocado en los resultados del motor de búsqueda
def graficar_similitudes_consultas(sim: np.ndarray, consultas: list[str], nombres_docs: list[str], archivo: str = "fig2_similitud_consultas.png") -> None:
    q, n = sim.shape
    fig, ax = plt.subplots(figsize=(max(7, n * 1.1), max(4, q * 0.9)))
    im = ax.imshow(sim, cmap="Blues", vmin=0, vmax=1, aspect="auto")
    fig.colorbar(im, ax=ax, label="Similitud coseno")
    etiq_docs = [name.replace(".txt", "") for name in nombres_docs]
    etiq_q    = [f'"{c}"' for c in consultas]
    ax.set_xticks(range(n))
    ax.set_xticklabels(etiq_docs, rotation=0)
    ax.set_yticks(range(q))
    ax.set_yticklabels(etiq_q, fontsize=9)
    for i in range(q):
        for j in range(n):
            val = sim[i, j]
            color_txt = "white" if val > 0.5 else "#1E293B"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=10, color=color_txt, fontweight="bold")

    ax.set_title("Similitud coseno: consultas vs documentos", pad=14)
    ax.set_xlabel("Documento")
    ax.set_ylabel("Consulta")
    plt.tight_layout()
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    print(f"[2/4] Guardado: {archivo}")
    plt.show()

#crea un gráfico de barras horizontales para mostrar cuáles son los términos más populares en el sistema
def graficar_frecuencia_terminos(matriz: list[list[int]], vocabulario: list[str], top_n: int = 15, archivo: str = "fig3_frecuencia_terminos.png") -> None:
    frecuencias = np.array(matriz).sum(axis=0)
    indices = np.argsort(frecuencias)[::-1][:top_n]
    terminos = [vocabulario[i] for i in indices]
    freqs = frecuencias[indices]
    colores = plt.cm.Blues(0.4 + 0.6 * freqs / freqs.max())
    d, ax = plt.subplots(figsize=(9, max(4, top_n * 0.45)))
    barras = ax.barh(terminos[::-1], freqs[::-1], color=colores[::-1], edgecolor="white", height=0.7)
    for barra, val in zip(barras, freqs[::-1]):
        ax.text(barra.get_width() + 0.05, barra.get_y() + barra.get_height() / 2, str(int(val)), va="center", fontsize=9)

    ax.set_xlabel("Frecuencia total en el corpus")
    ax.set_title(f"Top {top_n} términos más frecuentes", pad=12)
    ax.set_xlim(0, freqs.max() * 1.18)
    plt.tight_layout()
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    print(f"[3/4] Guardado: {archivo}")
    plt.show()

#muestra un gráfico de dispersión bidimensional que muestra la distancia semántica entre documentos y consultas 
def graficar_pca(matriz: list[list[int]], nombres_docs: list[str], vectores_q: list[list[int]], consultas: list[str], archivo: str = "fig4_pca.png") -> None:
    todos = list(matriz) + list(vectores_q)
    coords = _pca_2d(todos)
    coords_docs = coords[:len(matriz)]
    coords_q = coords[len(matriz):]
    d, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(coords_docs[:, 0], coords_docs[:, 1], c=COLOR_DOCS, s=140, zorder=3, edgecolors="white", linewidths=1.2)
    for i, nombre in enumerate(nombres_docs):
        etiq = nombre.replace(".txt", "")
        ax.annotate(etiq, (coords_docs[i, 0], coords_docs[i, 1]), textcoords="offset points", xytext=(8, 6), fontsize=9, color="#1e3a6e", fontweight="bold")

    ax.scatter(coords_q[:, 0], coords_q[:, 1], c=COLOR_QUERIES, marker="*", s=280, zorder=4, edgecolors="white", linewidths=0.8)
    for i, consulta in enumerate(consultas):
        ax.annotate(f'"{consulta}"', (coords_q[i, 0], coords_q[i, 1]), textcoords="offset points", xytext=(8, -12), fontsize=8, color="#7f1d1d")

    ax.axhline(0, color="#CBD5E1", linewidth=0.7, linestyle="--")
    ax.axvline(0, color="#CBD5E1", linewidth=0.7, linestyle="--")
    ax.set_xlabel("Componente principal 1")
    ax.set_ylabel("Componente principal 2")
    ax.set_title("Documentos y consultas en el espacio vectorial (PCA 2D)", pad=14)
    ax.legend(handles=[mpatches.Patch(color=COLOR_DOCS, label="Documentos"), mpatches.Patch(color=COLOR_QUERIES, label="Consultas")], fontsize=9)
    plt.tight_layout()
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    print(f"[4/4] Guardado: {archivo}")
    plt.show()

if __name__ == "__main__":
    print("Buscador Semántico Simple")
    documentos = cargar_documentos("Documentos")
    vocabulario = generar_vocabulario(documentos)
    nombres = list(documentos.keys())
    print(f"\nDocumentos : {nombres}")
    print(f"Vocabulario : {len(vocabulario)} palabras \n")
    matriz = construir_matriz(documentos, vocabulario)
    CONSULTAS = ["gato animal domestico", "vectores algebra lineal", "perro parque pelota"]
    vectores_q = []
    for consulta in CONSULTAS:
        vec = vectorizar_consulta(consulta, vocabulario)
        res = buscar(consulta, vocabulario, matriz, nombres, cantidad=3, umbral=0.0)
        vectores_q.append(vec)
        print(f"Consulta: '{consulta}'")
        for doc, sim in res:
            print(f"  {doc}  ->  {sim:.4f}")

    print("\n Generando visualizaciones")
    graficar_similitudes_docs(_matriz_sim_docs(matriz), nombres)
    graficar_similitudes_consultas(_matriz_sim_consultas(vectores_q, matriz), CONSULTAS, nombres)
    graficar_frecuencia_terminos(matriz, vocabulario, top_n=15)
    graficar_pca(matriz, nombres, vectores_q, CONSULTAS)
    print("\n  Todas las visualizaciones fueron generadas")