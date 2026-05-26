% --- Microservicios ---
arquitectura(microservicios) :-
    escala(alta),
    equipo(grande).

arquitectura(microservicios) :-
    complejidad(alta),
    equipo(grande).

% --- Monolito modular (punto medio) ---
arquitectura(monolito_modular) :-
    complejidad(media),
    escala(media).

arquitectura(monolito_modular) :-
    complejidad(media),
    equipo(grande).

% --- Monolito simple ---
arquitectura(monolito) :-
    tiempo(rapido).

arquitectura(monolito) :-
    equipo(pequeno),
    escala(baja).

arquitectura(monolito) :-
    equipo(pequeno),
    escala(media).

% --- Serverless (backend liviano con alta escala y equipo chico) ---
arquitectura(serverless) :-
    tipo_app(backend),
    escala(alta),
    equipo(pequeno).
