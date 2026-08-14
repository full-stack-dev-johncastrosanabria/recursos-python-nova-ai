"""Ejercicio: comparar números que no son exactos.

Implementa `approx_equal`, que es lo que hace `pytest.approx` por dentro.
Escribirlo una vez es la mejor forma de no volver a usarlo mal.

    approx_equal(0.1 + 0.2, 0.3)      -> True
    approx_equal(1.0, 1.1)            -> False
    approx_equal(0.0, 1e-15)          -> True    ← aquí manda la tolerancia absoluta

La regla: dos números son "iguales" si la diferencia entre ellos no supera la
mayor de las dos tolerancias:

    abs(actual - expected) <= max(rel * abs(expected), abs_tol)

Por qué hacen falta las dos:

- La **relativa** (`rel`) es la correcta casi siempre: un error de un céntimo
  sobre un millón es despreciable; sobre dos euros, no. La tolerancia tiene que
  escalar con la magnitud.
- La **absoluta** (`abs_tol`) existe para cuando el valor esperado es **cero**.
  Un porcentaje de cero es cero, así que la relativa se vuelve inútil justo ahí,
  que es un caso frecuentísimo.

Casos que hay que tratar:

- Si los dos valores son **exactamente** iguales, `True` sin más cuentas. Eso
  hace que funcione también con infinitos: `inf == inf`.
- **`nan` nunca es igual a nada**, ni a sí mismo. Si alguno de los dos es `nan`,
  la respuesta es `False`. Se detecta con `math.isnan`.
- Una tolerancia negativa no tiene sentido: `ValueError`.

Los valores por defecto (`rel=1e-6`, `abs_tol=1e-12`) son los mismos que usa
`pytest.approx`.
"""

import math  # noqa: F401  (lo vas a necesitar para isnan)


def approx_equal(
    actual: float, expected: float, rel: float = 1e-6, abs_tol: float = 1e-12
) -> bool:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
