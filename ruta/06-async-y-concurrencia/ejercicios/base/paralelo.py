"""Ejercicio: que las esperas ocurran a la vez.

Escribe `gather_all`, que recibe varias operaciones asíncronas y las ejecuta
**concurrentemente**, devolviendo sus resultados en el mismo orden en que
llegaron.

Cada operación es una función sin argumentos que devuelve algo esperable:

    async def traer_uno():
        await asyncio.sleep(0.1)
        return 1

    await gather_all([traer_uno, traer_dos, traer_tres])
    -> [1, 2, 3]        en ~0.1 s, no en ~0.3 s

Se reciben funciones y no corrutinas ya creadas por una razón práctica: una
corrutina solo se puede esperar una vez, así que pasarlas hechas convierte la
función en algo de un solo uso y difícil de probar.

Si no llega ninguna operación, el resultado es una lista vacía.

Ojo: hacer `for op in operations: resultados.append(await op())` **no** es
concurrente. Eso es exactamente lo que sus tests detectan.
"""

from collections.abc import Callable, Sequence


async def gather_all(operations: Sequence[Callable]) -> list:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
