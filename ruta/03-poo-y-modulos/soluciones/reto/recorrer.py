"""Solución de referencia del reto `recorrer`.

Las tres funciones tienen la misma forma: un caso base para el archivo y una
llamada recursiva sobre los hijos. Cambia solo qué se combina — sumar, contar o
tomar el máximo.
"""


def total_size(node: dict) -> int:
    if "size" in node:
        return node["size"]
    return sum(total_size(child) for child in node["children"])


def count_files(node: dict) -> int:
    if "size" in node:
        return 1
    return sum(count_files(child) for child in node["children"])


def max_depth(node: dict) -> int:
    if "size" in node or not node["children"]:
        return 0
    return 1 + max(max_depth(child) for child in node["children"])
