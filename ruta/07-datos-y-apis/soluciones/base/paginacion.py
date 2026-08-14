"""Solución de referencia del ejercicio `paginacion`.

`yield from` suelta los elementos de la página uno a uno. Al ser un generador,
la siguiente página no se pide hasta que alguien consume el último elemento de
la actual.
"""

from collections.abc import Callable, Iterator


def all_items(fetch_page: Callable[[int], dict]) -> Iterator:
    page = 1
    while True:
        data = fetch_page(page)
        yield from data["items"]

        if not data["has_more"]:
            return

        page += 1
