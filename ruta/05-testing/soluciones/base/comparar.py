"""Solución de referencia del ejercicio `comparar`.

El atajo de la igualdad exacta al principio no es una optimización: es lo que
hace que `inf` funcione, porque `inf - inf` es `nan` y la comparación posterior
daría `False`.
"""

import math


def approx_equal(
    actual: float, expected: float, rel: float = 1e-6, abs_tol: float = 1e-12
) -> bool:
    if rel < 0 or abs_tol < 0:
        raise ValueError(
            f"las tolerancias no pueden ser negativas: rel={rel}, abs_tol={abs_tol}"
        )

    if math.isnan(actual) or math.isnan(expected):
        return False

    if actual == expected:
        return True

    return abs(actual - expected) <= max(rel * abs(expected), abs_tol)
