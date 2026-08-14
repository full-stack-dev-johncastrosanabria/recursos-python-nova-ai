"""Solución de referencia del reto `matriz`.

La comprehension exterior evalúa `[value] * cols` una vez por fila, así que
cada fila es una lista distinta. Ese es todo el arreglo frente a `[[0]*3]*2`.
"""


def make_matrix(rows: int, cols: int, value: int = 0) -> list[list[int]]:
    if rows < 1 or cols < 1:
        raise ValueError(f"la matriz debe tener al menos 1x1, pidieron {rows}x{cols}")

    return [[value] * cols for _ in range(rows)]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    # `strict=True` hace que una matriz con filas de distinta longitud falle en
    # vez de recortarse en silencio, que es lo que hacía zip por defecto.
    return [list(columna) for columna in zip(*matrix, strict=True)]


def row_sums(matrix: list[list[int]]) -> list[int]:
    return [sum(fila) for fila in matrix]
