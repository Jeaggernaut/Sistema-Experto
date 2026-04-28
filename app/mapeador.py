def mapear_respuestas(respuestas: dict):
    hechos = []

    hechos.append(f"tipo_app({respuestas['tipo_app']})")
    hechos.append(f"escala({respuestas['escala']})")
    hechos.append(f"equipo({respuestas['equipo']})")
    hechos.append(f"tiempo({respuestas['tiempo']})")
    hechos.append(f"tiempo_real({respuestas['tiempo_real']})")
    hechos.append(f"complejidad({respuestas['complejidad']})")

    return hechos