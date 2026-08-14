"""Solución de referencia del ejercicio `limitado`.

Las tareas se crean todas, pero el semáforo solo deja pasar `limit` a la vez.
El resto esperan su turno en la puerta sin consumir nada.
"""

import asyncio
from collections.abc import Callable, Sequence


async def run_limited(operations: Sequence[Callable], limit: int) -> list:
    if limit < 1:
        raise ValueError(f"el límite debe ser al menos 1, no {limit}")

    semaphore = asyncio.Semaphore(limit)

    async def guarded(operation: Callable):
        async with semaphore:
            return await operation()

    return list(await asyncio.gather(*(guarded(op) for op in operations)))
