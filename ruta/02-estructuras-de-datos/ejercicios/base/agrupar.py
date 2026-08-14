"""Ejercicio: agrupar sin el ritual de "si no está, créala".

Recibes transferencias (diccionarios con una clave `currency`) y las agrupas
por divisa:

    group_by_currency([
        {"ref": "A", "currency": "CRC"},
        {"ref": "B", "currency": "USD"},
        {"ref": "C", "currency": "CRC"},
    ])
    -> {"CRC": [{"ref": "A", ...}, {"ref": "C", ...}],
        "USD": [{"ref": "B", ...}]}

Requisitos:

- Dentro de cada grupo se conserva el orden de entrada.
- Devuelve un `dict` normal. Si usas `defaultdict` para construirlo —es lo
  idiomático— conviértelo antes de devolverlo: un defaultdict que se escapa a
  quien te llama crea entradas nuevas con solo leerlas, y eso es un bug muy
  difícil de encontrar.

    resultado["EUR"]   -> debe lanzar KeyError, no devolver []
"""

from collections.abc import Iterable


def group_by_currency(transfers: Iterable[dict]) -> dict[str, list[dict]]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
