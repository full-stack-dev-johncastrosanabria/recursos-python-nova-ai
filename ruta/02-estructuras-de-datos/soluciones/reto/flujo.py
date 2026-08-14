"""Solución de referencia del reto `flujo`.

La clave está en `iter()`: convierte el iterable en un iterador del que se va
sacando, de modo que cada `islice` continúa donde lo dejó el anterior. Nada se
materializa salvo el trozo que se está construyendo.
"""

from collections.abc import Iterable, Iterator
from itertools import islice


def chunked(iterable: Iterable, size: int) -> Iterator[list]:
    if size < 1:
        raise ValueError(f"el tamaño del trozo debe ser al menos 1, no {size}")

    source = iter(iterable)
    while chunk := list(islice(source, size)):
        yield chunk
