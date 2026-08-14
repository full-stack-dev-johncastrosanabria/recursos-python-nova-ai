"""Reto: trocear un flujo sin materializarlo.

Escribe un generador que vaya soltando listas de `size` elementos:

    list(chunked([1, 2, 3, 4, 5], 2))   -> [[1, 2], [3, 4], [5]]

El último trozo puede ser más corto. Con `size` menor que 1, lanza
`ValueError`.

Lo que de verdad se evalúa aquí es la **pereza**. Tu función tiene que
funcionar sobre un iterable infinito y consumir solo lo que le pidan:

    numeros = itertools.count()        # 0, 1, 2, 3, ... para siempre
    trozos = chunked(numeros, 3)
    next(trozos)                       # [0, 1, 2] y ni un elemento más

Si construyes una lista con todo antes de trocear, funcionará con las listas
del test pero se colgará con lo de arriba. Piensa en términos de "pedir de uno
en uno hasta llenar el trozo", no de "tener todo y luego partirlo".

Pista: `iter()` sobre el iterable te da algo de lo que puedes ir sacando con
`next()`, y `itertools.islice` sabe tomar los n siguientes.
"""

from collections.abc import Iterable, Iterator


def chunked(iterable: Iterable, size: int) -> Iterator[list]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
