"""Ejercicio: reescribir un bucle con acento extranjero.

Esta versión funciona, pero delata que vienes de C o de Java: recorre por
índice, compara contra True y construye la lista a mano.

    def active_names(users):
        result = []
        for i in range(len(users)):
            if users[i]["active"] == True:
                result.append(users[i]["name"])
        return result

Reescríbela en la forma idiomática. Debe caber en una línea.

    active_names([{"name": "Ana", "active": True},
                  {"name": "Beto", "active": False}])   -> ["Ana"]

El orden de entrada se conserva.
"""


def active_names(users: list[dict]) -> list[str]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
