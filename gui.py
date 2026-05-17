import tkinter as tk
from tkinter import ttk
from app.motor import MotorExperto
from app.mapeador import mapear_respuestas


class SistemaExpertoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto")
        self.root.geometry("500x600")
        self.root.config(padx=20, pady=20)

        # Titulo
        tk.Label(root, text="Recomendación de Tecnologías",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Preguntas a realizar
        marco_preguntas = ttk.LabelFrame(
            root, text=" Parámetros del Proyecto ")
        marco_preguntas.pack(fill="x", pady=10, ipadx=10, ipady=10)

        # Diccionario de variables [interfaz]
        self.variables = {
            "tipo_app": tk.StringVar(value="web"),
            "escala": tk.StringVar(value="baja"),
            "equipo": tk.StringVar(value="pequeno"),
            "tiempo": tk.StringVar(value="normal"),
            "complejidad": tk.StringVar(value="baja")
        }

        # Menus desplegables
        self.crear_opcion(marco_preguntas, "Tipo de app:",
                          "tipo_app", ["web", "movil", "backend"])
        self.crear_opcion(marco_preguntas, "Escala:",
                          "escala", ["baja", "media", "alta"])
        self.crear_opcion(marco_preguntas, "Equipo:",
                          "equipo", ["pequeno", "grande"])
        self.crear_opcion(marco_preguntas, "Tiempo:",
                          "tiempo", ["rapido", "normal"])
        self.crear_opcion(marco_preguntas, "Complejidad:",
                          "complejidad", ["baja", "media", "alta"])

        # Boton de Consultas
        ttk.Button(root, text="Ejecutar Consulta",
                   command=self.ejecutar_consulta).pack(pady=15)

        # Resuldos
        tk.Label(root, text="Resultados de la Inferencia:",
                 font=("Arial", 12, "bold")).pack(anchor="w")

        # MARCO [texto / scrollbar]
        frame_resultados = tk.Frame(root)
        frame_resultados.pack(pady=5, fill="both", expand=True)

        # [Scrollbar] -> para resultados largos
        scrollbar = ttk.Scrollbar(frame_resultados)
        scrollbar.pack(side="right", fill="y")

       # Caja texto -> vincula al scrollbar
        self.caja_resultados = tk.Text(frame_resultados, height=12, width=55, font=(
            "Consolas", 10), yscrollcommand=scrollbar.set)
        self.caja_resultados.pack(side="left", fill="both", expand=True)

        # Configuracion del scrollbar
        scrollbar.config(command=self.caja_resultados.yview)

        self.caja_resultados.config(state=tk.DISABLED)  # Bloquear edición

    def crear_opcion(self, cabeza, texto, clave, opciones):
        # [Función auxiliar] -> etiquetas y comboboxes ordenados
        frame = tk.Frame(cabeza)
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=texto, width=15, anchor="w").pack(side="left")
        combo = ttk.Combobox(
            frame, textvariable=self.variables[clave], values=opciones, state="readonly")
        combo.pack(side="left", fill="x", expand=True)

    def ejecutar_consulta(self):
        # 1.- Limpiar los resultados anteriores
        self.caja_resultados.config(state=tk.NORMAL)
        self.caja_resultados.delete(1.0, tk.END)
        self.caja_resultados.insert(tk.END, "Procesando reglas lógicas...\n\n")
        self.root.update()

        # 2. Inicializar el motor [limpiar hechos anteriores]
        motor = MotorExperto()

        # 3. Respuestas de interfaz
        respuestas = {clave: var.get()
                      for clave, var in self.variables.items()}

        # 4. Mapeao e insercion de hechos en Prolog
        hechos = mapear_respuestas(respuestas)
        for hecho in hechos:
            motor.agregar_hecho(hecho)

        # 5. Consultar al motor
        self.mostrar_resultado(
            "Arquitectura", motor.consultar("arquitectura(X)"))
        self.mostrar_resultado("API", motor.consultar("api(X)"))
        self.mostrar_resultado("Tecnología", motor.consultar("tecnologia(X)"))
        self.mostrar_resultado("Diagnóstico", motor.consultar("problema(X)"))
        self.mostrar_resultado("Evaluación", motor.consultar("evaluacion(X)"))

        self.caja_resultados.config(state=tk.DISABLED)

    def mostrar_resultado(self, etiqueta, resultados):
        texto = f"📌 {etiqueta}:\n"
        if not resultados:
            texto += "   ❌ Sin resultados (Faltan reglas)\n"
        else:
            for r in resultados:
                texto += f"   ✅ {r['X']}\n"

        self.caja_resultados.insert(tk.END, texto + "\n")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = SistemaExpertoGUI(ventana)
    ventana.mainloop()
