"""Reto: ordenar a mano, una vez en la vida.

Implementa el **ordenamiento de burbuja**: recorre la lista comparando cada
pareja de vecinos e intercambiándolos si están desordenados; repite hasta que
una pasada completa no haga ningún intercambio.

    bubble_sort([3, 1, 2])
    -> ([1, 2, 3], 3)

Devuelves una tupla: la **lista ordenada** y **cuántos intercambios** hiciste.

Ese segundo número no es decorativo. Es lo que demuestra que implementaste el
algoritmo en vez de llamar a `sorted()`, y además tiene significado: coincide
con el número de *inversiones* de la lista, es decir, cuántos pares están en el
orden equivocado. Una lista ya ordenada da 0. Una lista al revés da el máximo
posible, `n * (n - 1) / 2`.

Reglas:

- **No uses `sorted()` ni `.sort()`.** El ejercicio es hacerlo tú.
- No modifiques la lista que recibes: trabaja sobre una copia.
- Una lista vacía o de un solo elemento ya está ordenada: cero intercambios.
- El orden es ascendente.

Por qué merece la pena escribirlo aunque nunca lo uses: entiendes qué significa
"ordenar" en términos de comparaciones e intercambios, y entiendes por qué
Python trae Timsort. La burbuja es O(n²); Timsort es O(n log n) y encima
aprovecha los tramos que ya venían ordenados. Después de este ejercicio,
`sorted()` deja de ser una caja negra y pasa a ser un regalo.
"""


def bubble_sort(numbers: list[float]) -> tuple[list[float], int]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
