from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from matriz_vectorial import construir_matriz, sparsidad
from motor_busqueda import buscar
from preprocesamiento import cargar_documentos, generar_vocabulario


RUTA_DOCUMENTOS = Path(__file__).resolve().parent / "Documentos"


def cargar_datos():
    # Carga los textos y crea su representación vectorial.
    documentos = cargar_documentos(str(RUTA_DOCUMENTOS))
    vocabulario = generar_vocabulario(documentos)
    nombres = list(documentos.keys())
    matriz = construir_matriz(documentos, vocabulario)

    return documentos, vocabulario, nombres, matriz


def iniciar_interfaz():
    if not RUTA_DOCUMENTOS.is_dir():
        messagebox.showerror("Error", "No se encontró la carpeta Documentos.")
        return

    documentos, vocabulario, nombres, matriz = cargar_datos()

    if not documentos:
        messagebox.showerror("Error", "No se encontraron documentos .txt.")
        return

    ventana = tk.Tk()
    ventana.title("Buscador semántico")
    ventana.geometry("760x520")
    ventana.minsize(680, 480)
    ventana.configure(bg="#F4F7FB")

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        rowheight=34,
        font=("Segoe UI", 10),
    )
    estilo.configure(
        "Treeview.Heading",
        background="#E8EEF8",
        foreground="#1E293B",
        font=("Segoe UI", 10, "bold"),
    )

    titulo = tk.Label(
        ventana,
        text="Buscador semántico",
        bg="#F4F7FB",
        fg="#173B70",
        font=("Segoe UI", 22, "bold"),
    )
    titulo.pack(pady=(28, 4))

    informacion = (
        f"{len(documentos)} documentos  •  {len(vocabulario)} términos  •  "
        f"{sparsidad(matriz) * 100:.2f}% de sparsidad"
    )
    tk.Label(
        ventana,
        text=informacion,
        bg="#F4F7FB",
        fg="#64748B",
        font=("Segoe UI", 10),
    ).pack()

    zona_busqueda = tk.Frame(ventana, bg="#F4F7FB")
    zona_busqueda.pack(fill="x", padx=45, pady=25)

    entrada = tk.Entry(
        zona_busqueda,
        font=("Segoe UI", 12),
        relief="solid",
        bd=1,
    )
    entrada.pack(side="left", fill="x", expand=True, ipady=9)

    boton = tk.Button(
        zona_busqueda,
        text="Buscar",
        bg="#2563EB",
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        padx=24,
        pady=9,
    )
    boton.pack(side="left", padx=(12, 0))

    tabla = ttk.Treeview(
        ventana,
        columns=("posicion", "documento", "similitud", "porcentaje"),
        show="headings",
        height=7,
    )
    tabla.heading("posicion", text="#")
    tabla.heading("documento", text="Documento")
    tabla.heading("similitud", text="Similitud coseno")
    tabla.heading("porcentaje", text="Porcentaje")
    tabla.column("posicion", width=55, anchor="center")
    tabla.column("documento", width=230, anchor="center")
    tabla.column("similitud", width=170, anchor="center")
    tabla.column("porcentaje", width=140, anchor="center")
    tabla.pack(fill="both", expand=True, padx=45)

    mensaje = tk.Label(
        ventana,
        text="Ingrese una consulta para encontrar los documentos más similares.",
        bg="#F4F7FB",
        fg="#64748B",
        font=("Segoe UI", 10),
    )
    mensaje.pack(pady=18)

    def realizar_busqueda(evento=None):
        consulta = entrada.get().strip()

        if not consulta:
            mensaje.config(text="Debe ingresar una consulta.", fg="#DC2626")
            return

        resultados = buscar(
            consulta,
            vocabulario,
            matriz,
            nombres,
            cantidad=3,
            umbral=0.0001,
        )

        for fila in tabla.get_children():
            tabla.delete(fila)

        if not resultados:
            mensaje.config(
                text="La consulta no contiene palabras del vocabulario.",
                fg="#DC2626",
            )
            return

        for posicion, (documento, similitud) in enumerate(resultados, start=1):
            tabla.insert(
                "",
                "end",
                values=(
                    posicion,
                    documento,
                    f"{similitud:.4f}",
                    f"{similitud * 100:.2f}%",
                ),
            )

        mensaje.config(
            text=f"Se encontraron {len(resultados)} resultados para: “{consulta}”",
            fg="#15803D",
        )

    boton.config(command=realizar_busqueda)
    entrada.bind("<Return>", realizar_busqueda)
    entrada.focus()
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()
