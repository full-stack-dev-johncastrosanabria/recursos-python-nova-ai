"""Reto: listas de listas, y la trampa de la fila compartida.

Tres funciones sobre matrices representadas como listas de listas:

    make_matrix(2, 3)            -> [[0, 0, 0], [0, 0, 0]]
    make_matrix(2, 2, value=7)   -> [[7, 7], [7, 7]]

    transpose([[1, 2, 3], [4, 5, 6]])   -> [[1, 4], [2, 5], [3, 6]]

    row_sums([[1, 2, 3], [4, 5, 6]])    -> [6, 15]

Lo importante está en la primera. Esto **parece** construir una matriz y no lo
hace:

    mal = [[0] * 3] * 2
    mal[0][0] = 9
    mal                 # [[9, 0, 0], [9, 0, 0]]  ← las dos filas

El `* 2` no copia la lista interior: repite la **misma referencia** dos veces,
así que las dos "filas" son el mismo objeto. Es el modelo de etiquetas del
módulo 00 en su versión más dolorosa, y sus tests lo comprueban: modificar una
celda no puede afectar a otra fila.

Reglas:

- `make_matrix(rows, cols, value=0)` devuelve `rows` filas de `cols` elementos,
  **independientes entre sí**.
- Un número de filas o columnas menor que 1 es `ValueError`.
- `transpose` intercambia filas por columnas y **no modifica** la matriz
  recibida. Una matriz vacía se transpone a una lista vacía.
- `row_sums` devuelve la suma de cada fila, en orden.

Pista para `transpose`: `zip(*matriz)` hace casi todo el trabajo, aunque
devuelve tuplas. Si no quieres usarlo, dos bucles anidados también valen.
"""


def make_matrix(rows: int, cols: int, value: int = 0) -> list[list[int]]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def row_sums(matrix: list[list[int]]) -> list[int]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
