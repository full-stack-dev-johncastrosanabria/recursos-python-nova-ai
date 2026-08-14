"""Solución de referencia del ejercicio `carrito`.

`None` como valor por defecto es el patrón canónico: es inmutable, así que
compartirlo entre llamadas no tiene consecuencias, y la lista nueva se crea
dentro del cuerpo, una por invocación.
"""


def add_item(item: str, basket: list[str] | None = None) -> list[str]:
    if basket is None:
        basket = []
    basket.append(item)
    return basket
