"""Solución de referencia del reto `resiliente`.

`return_exceptions=True` hace que `gather` devuelva la excepción como un
resultado más en vez de propagarla y cancelar el resto. Lo único que queda es
darle una forma que se lea bien donde se use.
"""

import asyncio
from collections.abc import Callable, Sequence


async def gather_settled(operations: Sequence[Callable]) -> list[tuple[bool, object]]:
    results = await asyncio.gather(
        *(operation() for operation in operations), return_exceptions=True
    )

    return [
        (False, result) if isinstance(result, BaseException) else (True, result)
        for result in results
    ]
