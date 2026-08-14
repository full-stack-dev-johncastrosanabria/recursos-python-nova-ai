"""Solución de referencia del reto `cola`.

Cada elemento viaja con su posición, así que los trabajadores pueden terminar
en cualquier orden y el resultado sale ordenado igualmente. El `finally` con
`task_done` garantiza que `join()` no se quede esperando para siempre aunque
un trabajo falle.
"""

import asyncio
from collections.abc import Callable, Sequence


async def run_queue(
    items: Sequence, worker: Callable, workers: int = 3, max_queue: int = 10
) -> list:
    if workers < 1:
        raise ValueError(f"hacen falta al menos 1 trabajador, no {workers}")
    if max_queue < 1:
        raise ValueError(f"la cola debe admitir al menos 1 elemento, no {max_queue}")

    if not items:
        return []

    cola: asyncio.Queue = asyncio.Queue(maxsize=max_queue)
    resultados: list = [None] * len(items)

    async def consumir() -> None:
        while True:
            posicion, elemento = await cola.get()
            try:
                resultados[posicion] = await worker(elemento)
            finally:
                cola.task_done()

    consumidores = [asyncio.create_task(consumir()) for _ in range(workers)]

    try:
        for posicion, elemento in enumerate(items):
            await cola.put((posicion, elemento))
        await cola.join()
    finally:
        for tarea in consumidores:
            tarea.cancel()
        await asyncio.gather(*consumidores, return_exceptions=True)

    return resultados
