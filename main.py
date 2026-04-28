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

    print("Arquitectura:")
    print(motor.consultar("arquitectura(X)"))

    print("API:")
    print(motor.consultar("api(X)"))

    print("Tecnologia:")
    print(motor.consultar("tecnologia(X)"))

    print("Diagnostico:")
    print(motor.consultar("problema(X)"))

    print("Evaluacion:")
    print(motor.consultar("evaluacion(X)"))

if __name__ == "__main__":
    main()

