"""Solución de referencia del ejercicio `similitud`.

La clave de `top_k` es la clave de ordenación: `(-similitud, nombre)` ordena de
mayor a menor y desempata alfabéticamente en una sola pasada.
"""

import math
from collections.abc import Sequence


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError(f"los vectores miden distinto: {len(a)} y {len(b)}")
    if not a:
        raise ValueError("los vectores no pueden estar vacíos")

    producto = sum(x * y for x, y in zip(a, b, strict=True))
    norma_a = math.sqrt(sum(x * x for x in a))
    norma_b = math.sqrt(sum(y * y for y in b))

    if norma_a == 0 or norma_b == 0:
        return 0.0

    return producto / (norma_a * norma_b)


def top_k(
    query: Sequence[float], vectors: dict[str, Sequence[float]], k: int = 3
) -> list[tuple[str, float]]:
    if k < 1:
        raise ValueError(f"k debe ser al menos 1, no {k}")

    puntuados = [
        (nombre, cosine_similarity(query, vector)) for nombre, vector in vectors.items()
    ]

    return sorted(puntuados, key=lambda par: (-par[1], par[0]))[:k]
