from pyswip import Prolog

class MotorExperto:
    def __init__(self):
        self.prolog = Prolog()
        self._cargar_conocimiento()

    def _cargar_conocimiento(self):
        # self.prolog.consult("conocimiento/base.pl")
        self.prolog.consult("prolog/arquitectura.pl")
        self.prolog.consult("prolog/tecnologias.pl")
        self.prolog.consult("prolog/diagnostico.pl")
        self.prolog.consult("prolog/evaluacion.pl")

    def agregar_hecho(self, hecho: str):
        self.prolog.assertz(hecho)

    def consultar(self, consulta: str):
        return list(self.prolog.query(consulta))