"""Solución de referencia del ejercicio `temporizado`.

Solo se captura `TimeoutError`. Cualquier otra excepción sube tal cual: un
fallo real y una tardanza son cosas distintas, y tratarlas igual convierte un
bug en un "no había datos".
"""

import asyncio
from collections.abc import Callable


async def with_timeout(operation: Callable, seconds: float, default=None):
    if seconds <= 0:
        raise ValueError(f"el plazo debe ser positivo, no {seconds}")

    try:
        async with asyncio.timeout(seconds):
            return await operation()
    except TimeoutError:
        return default
