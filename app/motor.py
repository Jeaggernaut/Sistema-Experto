import os
from pyswip import Prolog

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROLOG_DIR = os.path.join(_BASE_DIR, "prolog")

_ARCHIVOS_PROLOG = [
    "arquitectura.pl",
    "tecnologias.pl",
    "diagnostico.pl",
    "evaluacion.pl",
]


class MotorExperto:
    def __init__(self):
        self.prolog = Prolog()
        self._cargar_conocimiento()

    def _cargar_conocimiento(self):
        for archivo in _ARCHIVOS_PROLOG:
            ruta = os.path.join(_PROLOG_DIR, archivo)
            if not os.path.isfile(ruta):
                raise FileNotFoundError(
                    f"Archivo de conocimiento no encontrado: {ruta}"
                )
            # SWI-Prolog requiere barras forward en Windows
            self.prolog.consult(ruta.replace("\\", "/"))

    def agregar_hecho(self, hecho: str):
        try:
            pred = hecho.split("(")[0]
            list(self.prolog.query(f"retractall({pred}(_))"))
            self.prolog.assertz(hecho)
        except Exception as e:
            raise RuntimeError(f"Error al agregar hecho '{hecho}': {e}") from e

    def consultar(self, consulta: str) -> list:
        try:
            return list(self.prolog.query(consulta))
        except Exception as e:
            raise RuntimeError(f"Error en consulta '{consulta}': {e}") from e
