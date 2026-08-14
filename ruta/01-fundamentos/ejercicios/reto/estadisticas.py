"""Reto: resumir una lista de números.

Devuelve un diccionario con el mínimo, el máximo, la media y la mediana:

    summarize([1, 2, 3, 4])   -> {"min": 1, "max": 4, "mean": 2.5, "median": 2.5}
    summarize([7])            -> {"min": 7, "max": 7, "mean": 7, "median": 7}
    summarize([5, 1, 3])      -> {"min": 1, "max": 5, "mean": 3, "median": 3}

La **mediana** es el valor central de los datos ordenados. Con un número par de
elementos no hay uno central, así que es la media de los dos del medio: la
mediana de `[1, 2, 3, 4]` es `(2 + 3) / 2 = 2.5`.

Ojo con dos cosas:

- Hay que **ordenar** para la mediana, pero no debes modificar la lista que te
  pasan. `sorted()` devuelve una nueva; `.sort()` muta la original.
- Una lista vacía no tiene mínimo, ni media, ni mediana. Lanza `ValueError`.
  Devolver `0` sería un valor perfectamente creíble que oculta un fallo — es el
  bug 1 del caso real de la guía.
"""


def summarize(numbers: list[float]) -> dict[str, float]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
