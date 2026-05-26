% Microservicios con equipo chico es sobreingenieria
problema("Posible sobreingenieria") :-
    arquitectura(microservicios),
    equipo(pequeno).

% Monolito con alta escala acumula deuda de escalabilidad
problema("Falta de escalabilidad") :-
    arquitectura(monolito),
    escala(alta).

% Velocidad forzada con alta complejidad genera deuda tecnica
problema("Riesgo de deuda tecnica") :-
    tiempo(rapido),
    complejidad(alta).

% Equipo grande ociosos en proyecto simple
problema("Equipo sobredimensionado para el proyecto") :-
    equipo(grande),
    escala(baja),
    complejidad(baja).

% Monolito con equipo grande genera conflictos de merge
problema("Alto riesgo de conflictos de integracion") :-
    arquitectura(monolito),
    equipo(grande).
