_VALORES_VALIDOS: dict[str, set] = {
    "tipo_app":    {"web", "movil", "backend"},
    "escala":      {"baja", "media", "alta"},
    "equipo":      {"pequeno", "grande"},
    "tiempo":      {"rapido", "normal"},
    "complejidad": {"baja", "media", "alta"},
}


def mapear_respuestas(respuestas: dict) -> list[str]:
    for clave, valor in respuestas.items():
        permitidos = _VALORES_VALIDOS.get(clave)
        if permitidos and valor not in permitidos:
            raise ValueError(
                f"Valor inválido para '{clave}': '{valor}'. "
                f"Opciones permitidas: {sorted(permitidos)}"
            )
    return [f"{clave}({valor})" for clave, valor in respuestas.items()]
