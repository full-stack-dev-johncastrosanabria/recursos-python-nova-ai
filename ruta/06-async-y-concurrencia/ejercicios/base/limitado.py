"""Ejercicio: concurrencia con límite.

Como el ejercicio anterior, pero sin pasarse: `run_limited` ejecuta las
operaciones concurrentemente permitiendo **como mucho `limit` a la vez**.

    await run_limited([op1, ..., op10], limit=3)
    -> los diez resultados, en orden, sin que nunca haya más de tres en vuelo

Es el patrón de cada API con límite de tasa, las de LLMs incluidas: puedes
lanzar mil peticiones, pero si lo haces te van a bloquear.

Reglas:

- Los resultados salen en el orden de entrada, no en el de finalización.
- `limit` menor que 1 es un error: `ValueError`.
- Si `limit` es mayor que el número de operaciones, no pasa nada raro: se
  ejecutan todas a la vez.

Sus tests cuentan cuántas operaciones llegan a estar dentro simultáneamente, así
que no basta con que el resultado sea correcto: el límite tiene que respetarse
de verdad.

Pista: `asyncio.Semaphore` y un `async with`.
"""

from collections.abc import Callable, Sequence


async def run_limited(operations: Sequence[Callable], limit: int) -> list:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
