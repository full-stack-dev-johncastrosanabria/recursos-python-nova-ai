"""Solución de referencia del reto `contador`.

`count` vive en el ámbito de `make_counter`. Las dos funciones internas lo ven
porque la búsqueda de nombres sube hacia fuera (la E de LEGB), pero solo la que
**asigna** necesita declarar `nonlocal`. Cada llamada a `make_counter` crea un
ámbito nuevo, y de ahí que los contadores sean independientes.
"""

from collections.abc import Callable


def make_counter(start: int = 0) -> tuple[Callable[[], int], Callable[[], int]]:
    count = start

    def incrementar() -> int:
        nonlocal count
        count += 1
        return count

    def valor() -> int:
        return count

    return incrementar, valor
