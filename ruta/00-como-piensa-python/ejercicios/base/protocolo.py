"""Ejercicio: la cascada del valor de verdad.

Todo objeto de Python tiene un valor de verdad, y se resuelve preguntando en
este orden:

1. ¿Define `__bool__`? Se usa su resultado.
2. ¿No, pero define `__len__`? Es verdadero si su longitud no es cero.
3. ¿Ninguno de los dos? Es verdadero siempre.

Implementa `Inventory`, un inventario de productos con existencias, para ver la
cascada con los dos protocolos **en desacuerdo a propósito**.

    inv = Inventory({"café": 3, "azúcar": 0})

    len(inv)          -> 2       ← dos productos distintos
    bool(inv)         -> True    ← hay existencias de algo
    "café" in inv     -> True
    "té" in inv       -> False

    agotado = Inventory({"café": 0, "azúcar": 0})
    len(agotado)      -> 2       ← sigue habiendo dos productos…
    bool(agotado)     -> False   ← …pero no queda nada: `__bool__` manda
    if agotado: ...              ← no entra

Lo que hay que implementar:

- `__len__`: cuántos productos distintos hay, tengan o no existencias.
- `__bool__`: verdadero solo si **la suma de existencias es mayor que cero**.
- `__contains__`: si un producto está en el inventario, tenga las existencias
  que tenga.

Ese desacuerdo entre `len` y `bool` es el ejercicio: si solo definieras
`__len__`, un inventario con todo a cero sería verdadero, y `if inventario:`
diría que hay stock cuando no lo hay.
"""


class Inventory:
    def __init__(self, stock: dict[str, int]) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
