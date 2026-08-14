"""Solución de referencia del reto `dependencias`.

Algoritmo de Kahn. La lista de candidatos se mantiene ordenada en cada vuelta,
que es lo que hace el resultado reproducible: sin eso, el orden dependería de
cómo iteró el diccionario.
"""


class CircularDependency(Exception):
    """Hay un ciclo: no existe ningún orden de instalación válido."""


def install_order(dependencies: dict[str, list[str]]) -> list[str]:
    # Todo lo que aparece, sea como clave o como dependencia de alguien.
    paquetes = set(dependencies)
    for requeridos in dependencies.values():
        paquetes.update(requeridos)

    pendientes = {p: set(dependencies.get(p, ())) & paquetes for p in paquetes}
    orden: list[str] = []

    while pendientes:
        listos = sorted(p for p, faltan in pendientes.items() if not faltan)

        if not listos:
            raise CircularDependency(
                "ciclo de dependencias entre: " + ", ".join(sorted(pendientes))
            )

        elegido = listos[0]
        orden.append(elegido)
        del pendientes[elegido]

        for faltan in pendientes.values():
            faltan.discard(elegido)

    return orden
