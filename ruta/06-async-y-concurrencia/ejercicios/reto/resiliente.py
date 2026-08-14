"""Reto: recoger todos los resultados, incluidos los fallos.

Cuando un orquestador lanza tres herramientas en paralelo y una devuelve error,
lo razonable casi nunca es tirar las otras dos. Escribe `gather_settled`, que
ejecuta las operaciones concurrentemente y devuelve, en orden, un par por cada
una:

    (True, resultado)    si terminó bien
    (False, excepcion)   si lanzó una excepción

Ejemplo:

    await gather_settled([ok, falla, ok2])
    -> [(True, "a"), (False, ValueError("vaya")), (True, "c")]

Reglas:

- Que una operación falle **no** debe impedir que las demás terminen. Sus tests
  lo comprueban contando cuántas llegaron al final.
- El segundo elemento del par es la excepción en sí, no su mensaje.
- Sin operaciones, lista vacía.

Este es el modo `return_exceptions=True` de `asyncio.gather`, envuelto en algo
que se lee mejor en el sitio donde se usa: `if ok:` dice más que comprobar si
un elemento resultó ser una instancia de `Exception`.
"""

from collections.abc import Callable, Sequence


async def gather_settled(operations: Sequence[Callable]) -> list[tuple[bool, object]]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
