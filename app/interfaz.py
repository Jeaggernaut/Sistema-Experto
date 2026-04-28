def preguntar_usuario():
    print("=== Sistema Experto de Software ===")

    tipo_app = input("Tipo de app (web/movil/backend): ")
    escala = input("Escala (baja/media/alta): ")
    equipo = input("Equipo (pequeno/grande): ")
    tiempo = input("Tiempo (rapido/normal): ")
    tiempo_real = input("¿Tiempo real? (si/no): ")
    complejidad = input("Complejidad (baja/media/alta): ")

    return {
        "tipo_app": tipo_app,
        "escala": escala,
        "equipo": equipo,
        "tiempo": tiempo,
        "tiempo_real": tiempo_real,
        "complejidad": complejidad
    }