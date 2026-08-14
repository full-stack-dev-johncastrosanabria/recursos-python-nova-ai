"""Solución de referencia del ejercicio `banderas`.

`bool(...)` alrededor del `&` no es decorativo: sin él, `has` devolvería el
entero resultante de la máscara, que es verdadero pero no es `True`.
"""

LEER = 0b100
ESCRIBIR = 0b010
EJECUTAR = 0b001


def grant(permissions: int, flag: int) -> int:
    return permissions | flag


def revoke(permissions: int, flag: int) -> int:
    return permissions & ~flag


def has(permissions: int, flag: int) -> bool:
    return bool(permissions & flag)


def describe(permissions: int) -> str:
    return "".join(
        letra if has(permissions, bandera) else "-"
        for letra, bandera in (("r", LEER), ("w", ESCRIBIR), ("x", EJECUTAR))
    )
