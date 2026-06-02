import os
import tkinter as tk
from tkinter import ttk, messagebox
from app.motor import MotorExperto
from app.mapeador import mapear_respuestas

try:
    from PIL import Image, ImageTk
    _PIL = True
except ImportError:
    _PIL = False

_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "assets")

# ── Paleta ────────────────────────────────────────────────────────────────────
BG         = "#F0F4F8"
CARD_BG    = "#FFFFFF"
HDR_BG     = "#1B2A4A"
HDR_FG     = "#FFFFFF"
HDR_SUB    = "#93C5FD"
ACCENT     = "#2563EB"
ACCENT_HOV = "#1D4ED8"
BTN2_BG    = "#E2E8F0"
BTN2_FG    = "#374151"
TEXT       = "#1F2937"
MUTED      = "#6B7280"
RESULT_BG  = "#F8FAFC"
BORDER     = "#E5E7EB"
ERROR_FG   = "#DC2626"


class SistemaExpertoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto — Recomendación de Tecnologías")
        self.root.geometry("640x740")
        self.root.minsize(840, 600)
        self.root.resizable(True, True)
        self.root.configure(bg=BG)

        self._aplicar_estilos()
        self._construir_header()
        self._construir_cuerpo()

    # ── Estilos ttk ───────────────────────────────────────────────────────────
    def _aplicar_estilos(self):
        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 10))

        s.configure("TCombobox",
                    fieldbackground=CARD_BG, background=CARD_BG,
                    foreground=TEXT, padding=(6, 5))
        s.map("TCombobox",
              fieldbackground=[("readonly", CARD_BG)],
              selectbackground=[("readonly", ACCENT)],
              selectforeground=[("readonly", "#FFFFFF")])

        s.configure("Primary.TButton",
                    background=ACCENT, foreground="#FFFFFF",
                    font=("Segoe UI", 10, "bold"),
                    padding=(20, 9), relief="flat", borderwidth=0)
        s.map("Primary.TButton",
              background=[("active", ACCENT_HOV), ("pressed", ACCENT_HOV)])

        s.configure("Secondary.TButton",
                    background=BTN2_BG, foreground=BTN2_FG,
                    font=("Segoe UI", 10),
                    padding=(20, 9), relief="flat", borderwidth=0)
        s.map("Secondary.TButton",
              background=[("active", "#CBD5E1"), ("pressed", "#CBD5E1")])

        s.configure("Vertical.TScrollbar",
                    background=BORDER, troughcolor=RESULT_BG,
                    borderwidth=0, arrowsize=12, relief="flat")

    # ── Carga de imágenes ─────────────────────────────────────────────────────
    def _cargar_imagen(self, nombre: str, altura: int):
        if not _PIL:
            return None
        ruta = os.path.join(_ASSETS, nombre)
        if not os.path.isfile(ruta):
            return None
        try:
            from PIL import ImageChops
            img = Image.open(ruta).convert("RGBA")
            r, g, b, a = img.split()

            # Tablas de búsqueda → Pillow las aplica en C, sin loop Python
            lut_blanco   = [255 if i > 220 else 0 for i in range(256)]
            lut_oscuro   = [255 if i <  80 else 0 for i in range(256)]
            lut_oscuro_b = [255 if i < 100 else 0 for i in range(256)]

            # Máscara píxeles blancos (r>220 AND g>220 AND b>220)
            mask_blanco = ImageChops.multiply(
                ImageChops.multiply(r.point(lut_blanco), g.point(lut_blanco)),
                b.point(lut_blanco),
            )
            # Máscara píxeles oscuros (r<80 AND g<80 AND b<100)
            mask_oscuro = ImageChops.multiply(
                ImageChops.multiply(r.point(lut_oscuro), g.point(lut_oscuro)),
                b.point(lut_oscuro_b),
            )

            # Aplicar: blanco → transparente
            nuevo_a = ImageChops.multiply(a, ImageChops.invert(mask_blanco))
            # Aplicar: oscuro → blanco (visible sobre fondo azul)
            blanco = Image.new("L", img.size, 255)
            nuevo_r = Image.composite(blanco, r, mask_oscuro)
            nuevo_g = Image.composite(blanco, g, mask_oscuro)
            nuevo_b_ch = Image.composite(blanco, b, mask_oscuro)

            img = Image.merge("RGBA", (nuevo_r, nuevo_g, nuevo_b_ch, nuevo_a))

            # Redimensionar después del procesamiento (anti-aliasing limpio)
            w, h = img.size
            nuevo_w = max(1, round(w * altura / h))
            img = img.resize((nuevo_w, altura), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    # ── Header ────────────────────────────────────────────────────────────────
    def _construir_header(self):
        hdr = tk.Frame(self.root, bg=HDR_BG)
        hdr.pack(fill="x")
        hdr.columnconfigure(1, weight=1)

        self._img4 = self._cargar_imagen("image4.png", 120)
        self._img5 = self._cargar_imagen("image5.png", 90)

        # Columna 0 — escudo ITSP directo sobre el header azul
        if self._img4:
            tk.Label(hdr, image=self._img4, bg=HDR_BG).grid(
                row=0, column=0, padx=(20, 0), pady=16, sticky="w")

        # Columna 1 — título + subtítulo (elemento principal)
        titulo_frame = tk.Frame(hdr, bg=HDR_BG)
        titulo_frame.grid(row=0, column=1, sticky="ew", padx=18, pady=(22, 22))
        tk.Label(titulo_frame, text="Sistema Experto",
                 bg=HDR_BG, fg=HDR_FG,
                 font=("Segoe UI", 18, "bold"), anchor="w"
                 ).pack(anchor="w")
        tk.Label(titulo_frame, text="Recomendación de tecnologías para tu proyecto",
                 bg=HDR_BG, fg=HDR_SUB,
                 font=("Segoe UI", 10), anchor="w"
                 ).pack(anchor="w")

        # Columna 2 — logo TecNM directo sobre el header azul
        if self._img5:
            tk.Label(hdr, image=self._img5, bg=HDR_BG).grid(
                row=0, column=2, padx=(0, 20), pady=16, sticky="e")

    # ── Cuerpo ────────────────────────────────────────────────────────────────
    def _construir_cuerpo(self):
        cuerpo = tk.Frame(self.root, bg=BG)
        cuerpo.pack(fill="both", expand=True, padx=24, pady=20)
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.rowconfigure(2, weight=1)

        self._card_parametros(cuerpo)   # row 0
        self._fila_botones(cuerpo)      # row 1
        self._card_resultados(cuerpo)   # row 2

    # ── Fábrica de cards ──────────────────────────────────────────────────────
    def _nueva_card(self, parent, row, titulo, sticky="ew", pady=0):
        wrapper = tk.Frame(parent, bg=CARD_BG,
                           highlightthickness=1,
                           highlightbackground=BORDER)
        wrapper.grid(row=row, column=0, sticky=sticky, pady=pady)
        tk.Label(wrapper, text=titulo,
                 bg=CARD_BG, fg=ACCENT,
                 font=("Segoe UI", 10, "bold"), anchor="w"
                 ).pack(fill="x", padx=16, pady=(14, 0))
        tk.Frame(wrapper, bg=BORDER, height=1).pack(fill="x",
                                                     padx=16, pady=(8, 0))
        content = tk.Frame(wrapper, bg=CARD_BG)
        content.pack(fill="both", expand=True)
        return content

    # ── Card: Parámetros ──────────────────────────────────────────────────────
    def _card_parametros(self, parent):
        content = self._nueva_card(parent, row=0,
                                   titulo="Parámetros del Proyecto",
                                   sticky="ew", pady=(0, 14))
        content.columnconfigure(1, weight=1)

        self.variables = {
            "tipo_app":    tk.StringVar(value="web"),
            "escala":      tk.StringVar(value="baja"),
            "equipo":      tk.StringVar(value="pequeno"),
            "tiempo":      tk.StringVar(value="normal"),
            "complejidad": tk.StringVar(value="baja"),
        }
        campos = [
            ("Tipo de app",  "tipo_app",    ["web", "movil", "backend"]),
            ("Escala",       "escala",      ["baja", "media", "alta"]),
            ("Equipo",       "equipo",      ["pequeno", "grande"]),
            ("Tiempo",       "tiempo",      ["rapido", "normal"]),
            ("Complejidad",  "complejidad", ["baja", "media", "alta"]),
        ]
        for i, (label, key, opts) in enumerate(campos):
            tk.Label(content, text=label,
                     bg=CARD_BG, fg=TEXT,
                     font=("Segoe UI", 10), anchor="w", width=14
                     ).grid(row=i, column=0, sticky="w",
                            padx=(16, 8), pady=9)
            ttk.Combobox(content, textvariable=self.variables[key],
                         values=opts, state="readonly",
                         font=("Segoe UI", 10)
                         ).grid(row=i, column=1, sticky="ew",
                                padx=(0, 16), pady=9)

    # ── Fila de botones ───────────────────────────────────────────────────────
    def _fila_botones(self, parent):
        frame = tk.Frame(parent, bg=BG)
        frame.grid(row=1, column=0, sticky="w", pady=(0, 14))
        ttk.Button(frame, text="Ejecutar Consulta",
                   style="Primary.TButton",
                   command=self.ejecutar_consulta
                   ).pack(side="left", padx=(0, 10))
        ttk.Button(frame, text="Limpiar",
                   style="Secondary.TButton",
                   command=self.limpiar_resultados
                   ).pack(side="left")

    # ── Card: Resultados ──────────────────────────────────────────────────────
    def _card_resultados(self, parent):
        content = self._nueva_card(parent, row=2,
                                   titulo="Resultados de la Inferencia",
                                   sticky="nsew", pady=0)
        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(content, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns", pady=(0, 14))

        self.caja_resultados = tk.Text(
            content,
            font=("Consolas", 10),
            bg=RESULT_BG, fg=TEXT,
            relief="flat", borderwidth=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            yscrollcommand=scrollbar.set,
            wrap="word",
            padx=14, pady=10,
            spacing1=2, spacing3=3,
            state=tk.DISABLED,
        )
        self.caja_resultados.grid(row=0, column=0, sticky="nsew",
                                   padx=(12, 4), pady=(0, 14))
        scrollbar.config(command=self.caja_resultados.yview)

        self.caja_resultados.tag_configure(
            "header", font=("Segoe UI", 10, "bold"),
            foreground=ACCENT, spacing1=6, spacing3=2)
        self.caja_resultados.tag_configure(
            "item", foreground=TEXT, lmargin1=12, lmargin2=20)
        self.caja_resultados.tag_configure(
            "muted", font=("Segoe UI", 9, "italic"),
            foreground=MUTED, lmargin1=12)
        self.caja_resultados.tag_configure(
            "processing", font=("Segoe UI", 10, "italic"),
            foreground=MUTED)
        self.caja_resultados.tag_configure(
            "error", font=("Segoe UI", 10, "bold"),
            foreground=ERROR_FG)

    # ── Lógica (sin cambios respecto al original) ─────────────────────────────
    def limpiar_resultados(self):
        self.caja_resultados.config(state=tk.NORMAL)
        self.caja_resultados.delete(1.0, tk.END)
        self.caja_resultados.config(state=tk.DISABLED)

    def ejecutar_consulta(self):
        self.caja_resultados.config(state=tk.NORMAL)
        self.caja_resultados.delete(1.0, tk.END)
        self.caja_resultados.insert(tk.END, "Procesando reglas lógicas…\n", "processing")
        self.root.update()

        try:
            motor = MotorExperto()
            respuestas = {clave: var.get() for clave, var in self.variables.items()}
            hechos = mapear_respuestas(respuestas)
            for hecho in hechos:
                motor.agregar_hecho(hecho)

            self.caja_resultados.delete(1.0, tk.END)
            self.mostrar_resultado("Arquitectura", motor.consultar("arquitectura(X)"))
            self.mostrar_resultado("API",          motor.consultar("api(X)"))
            self.mostrar_resultado("Tecnología",   motor.consultar("tecnologia(X)"))
            self.mostrar_resultado("Diagnóstico",  motor.consultar("problema(X)"))
            self.mostrar_resultado("Evaluación",   motor.consultar("evaluacion(X)"))

        except FileNotFoundError as e:
            self._mostrar_error(f"Archivo de conocimiento no encontrado:\n{e}")
        except RuntimeError as e:
            self._mostrar_error(f"Error en el motor de inferencia:\n{e}")
        except Exception as e:
            self._mostrar_error(f"Error inesperado:\n{e}")
        finally:
            self.caja_resultados.config(state=tk.DISABLED)

    def mostrar_resultado(self, etiqueta, resultados):
        self.caja_resultados.insert(tk.END, f"{etiqueta}\n", "header")
        vistos = set()
        unicos = []
        for r in resultados:
            val = r['X']
            if val not in vistos:
                vistos.add(val)
                unicos.append(r)
        if not unicos:
            self.caja_resultados.insert(tk.END,
                "Sin resultados para esta combinación\n\n", "muted")
        else:
            for r in unicos:
                self.caja_resultados.insert(tk.END, f"▸  {r['X']}\n", "item")
            self.caja_resultados.insert(tk.END, "\n")

    def _mostrar_error(self, mensaje: str):
        self.caja_resultados.config(state=tk.NORMAL)
        self.caja_resultados.delete(1.0, tk.END)
        self.caja_resultados.insert(tk.END, "Error del sistema\n\n", "error")
        self.caja_resultados.insert(tk.END, mensaje + "\n")
        messagebox.showerror("Error del Sistema Experto", mensaje)


if __name__ == "__main__":
    try:
        ventana = tk.Tk()
        app = SistemaExpertoGUI(ventana)
        ventana.mainloop()
    except KeyboardInterrupt:
        pass
