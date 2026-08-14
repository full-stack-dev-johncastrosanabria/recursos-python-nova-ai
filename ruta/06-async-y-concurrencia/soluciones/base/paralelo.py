"""Solución de referencia del ejercicio `paralelo`.

`gather` recibe corrutinas ya creadas, así que se llaman todas primero —eso no
las ejecuta, solo las crea— y luego se esperan juntas.
"""

import asyncio
from collections.abc import Callable, Sequence


async def gather_all(operations: Sequence[Callable]) -> list:
    return list(await asyncio.gather(*(operation() for operation in operations)))
