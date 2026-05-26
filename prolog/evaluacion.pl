evaluacion("Alta escalabilidad horizontal") :-
    arquitectura(microservicios).

evaluacion("Escalabilidad gestionada por el proveedor") :-
    arquitectura(serverless).

evaluacion("Despliegue rapido, menor overhead inicial") :-
    arquitectura(monolito).

evaluacion("Balance entre modularidad y simplicidad") :-
    arquitectura(monolito_modular).

evaluacion("Desarrollo acelerado") :-
    tiempo(rapido).

evaluacion("Mayor complejidad tecnica y operacional") :-
    arquitectura(microservicios).

evaluacion("Curva de aprendizaje elevada") :-
    complejidad(alta).

evaluacion("Facil de mantener y onboardear") :-
    complejidad(baja),
    equipo(pequeno).
