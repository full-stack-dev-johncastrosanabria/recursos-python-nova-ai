"""Solución de referencia del reto `reintentos`.

La condición `if attempt < attempts - 1` es la que evita dormir después del
último intento. Sin ella la función tarda lo mismo pero se rinde igual: tiempo
regalado.
"""

import time
from collections.abc import Callable


def retry(
    operation: Callable,
    *,
    attempts: int = 3,
    base_delay: float = 1.0,
    sleeper: Callable[[float], None] = time.sleep,
):
    if attempts < 1:
        raise ValueError(f"attempts debe ser al menos 1, no {attempts}")

    for attempt in range(attempts):
        try:
            return operation()
        except Exception:
            if attempt == attempts - 1:
                raise
            sleeper(base_delay * 2**attempt)

    raise AssertionError("inalcanzable")  # pragma: no cover
