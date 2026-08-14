"""Solución de referencia del ejercicio `configuracion`.

Se construye un diccionario nuevo y se van escribiendo encima las capas, de
menos a más específica. Como nunca se toca ninguna capa de entrada, quien llama
conserva sus diccionarios intactos.
"""

from collections.abc import Mapping


def merge_config(*layers: Mapping) -> dict:
    merged: dict = {}

    for layer in layers:
        merged.update({key: value for key, value in layer.items() if value is not None})

    return merged
