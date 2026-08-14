"""Ejercicio: permisos con operadores bit a bit.

Un entero guarda muchos booleanos a la vez. Es como funcionan los permisos de
archivo en Unix desde hace cincuenta años, y como funcionan la mitad de los
sistemas de flags que te vas a encontrar.

Tres banderas, cada una en su bit:

    LEER     = 0b100  (4)
    ESCRIBIR = 0b010  (2)
    EJECUTAR = 0b001  (1)

Implementa cuatro funciones:

    grant(0, LEER)              -> 4        activa una bandera
    grant(4, ESCRIBIR)          -> 6        activa otra sin tocar la primera
    grant(6, LEER)              -> 6        activar lo ya activo no cambia nada

    revoke(6, ESCRIBIR)         -> 4        desactiva una
    revoke(4, ESCRIBIR)         -> 4        desactivar lo que no está tampoco cambia

    has(6, LEER)                -> True
    has(6, EJECUTAR)            -> False

    describe(7)                 -> "rwx"
    describe(6)                 -> "rw-"
    describe(4)                 -> "r--"
    describe(0)                 -> "---"

Los operadores que necesitas:

- `|` activa bits (OR)
- `&` comprueba bits (AND)
- `&` junto con `~` desactiva bits (AND con el complemento)

Ojo con `has`: `permisos & LEER` no devuelve `True`, devuelve `4`. Tu función
tiene que devolver un booleano de verdad, no un entero que resulta ser
verdadero — los tests lo comprueban con `is True`.
"""

LEER = 0b100
ESCRIBIR = 0b010
EJECUTAR = 0b001


def grant(permissions: int, flag: int) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def revoke(permissions: int, flag: int) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def has(permissions: int, flag: int) -> bool:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def describe(permissions: int) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
