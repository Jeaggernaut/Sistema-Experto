% --- Tecnologia movil ---
tecnologia(flutter) :-
    tipo_app(movil).

% --- Tecnologia web ---
tecnologia('next.js') :-
    tipo_app(web),
    complejidad(alta).

tecnologia(react) :-
    tipo_app(web),
    complejidad(media).

tecnologia(react) :-
    tipo_app(web),
    complejidad(baja).

% --- Tecnologia backend ---
tecnologia('node.js') :-
    tipo_app(backend),
    tiempo(rapido).

tecnologia('django / fastapi') :-
    tipo_app(backend),
    tiempo(normal).

% --- API ---
api(graphql) :-
    complejidad(alta).

api(rest) :-
    complejidad(media).

api(rest) :-
    complejidad(baja).
