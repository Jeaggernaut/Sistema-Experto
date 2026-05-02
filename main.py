from app.motor import MotorExperto
from app.interfaz import preguntar_usuario
from app.mapeador import mapear_respuestas

def main():
    motor = MotorExperto()

    respuestas = preguntar_usuario()
    hechos = mapear_respuestas(respuestas)

    for hecho in hechos:
        motor.agregar_hecho(hecho)

    print("\n--- RESULTADOS ---")
    mostrar_resultado("Arquitectura", motor.consultar("arquitectura(X)"))
    mostrar_resultado("API",          motor.consultar("api(X)"))
    mostrar_resultado("Tecnologia",   motor.consultar("tecnologia(X)"))
    mostrar_resultado("Diagnostico",  motor.consultar("problema(X)"))
    mostrar_resultado("Evaluacion",   motor.consultar("evaluacion(X)"))

def mostrar_resultado(etiqueta, resultados):
    print(f"{etiqueta}:", end=" ")
    if not resultados:
        print(" Sin resultados")
    else:
        for r in resultados:
            print(f"{r['X']}")

if __name__ == "__main__":
    main()

