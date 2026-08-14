"""Ejercicio: recorrer todas las páginas de una API.

Escribe `all_items`, un generador que va soltando los elementos de todas las
páginas, una tras otra, sin saber de antemano cuántas hay.

Recibes una función `fetch_page(numero)` que devuelve un diccionario así:

    {"items": ["a", "b"], "has_more": True}

Las páginas empiezan en **1**. Se pide la siguiente mientras `has_more` sea
verdadero.

    all_items(fetch)   ->  "a", "b", "c", "d", ...

Requisitos:

- Devuelve un generador, no una lista. Quien lo consuma debe poder parar a la
  mitad y que no se pidan las páginas restantes. Sus tests cuentan las
  llamadas, así que construir la lista entera se detecta.
- Si la primera página viene sin elementos y sin más páginas, no sueltas nada.
- No asumas un número máximo de páginas. El bug más común de este patrón es
  exactamente ese: funciona hasta que aparece una página más y las
  transferencias de esa página desaparecen sin que nadie vea un error.
"""

from collections.abc import Callable, Iterator


def all_items(fetch_page: Callable[[int], dict]) -> Iterator:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
