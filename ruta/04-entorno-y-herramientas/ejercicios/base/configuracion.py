"""Ejercicio: capas de configuración con precedencia.

Escribe `merge_config`, que combina varias capas de configuración. Las capas
llegan de menos a más específica y **gana la última**:

    merge_config(
        {"host": "localhost", "port": 8000},   # valores por defecto
        {"port": 5432},                        # archivo de configuración
        {"host": "prod.internal"},             # variables de entorno
    )
    -> {"host": "prod.internal", "port": 5432}

Dos reglas más:

- Las claves cuyo valor sea `None` se ignoran. Representan "no especificado":
  un argumento de línea de comandos que nadie pasó no debe borrar lo que venía
  del archivo de configuración.
- No modifiques las capas que recibes. Quien te llama no espera que le cambies
  su diccionario de valores por defecto.

    merge_config({"a": 1}, {"a": None})   -> {"a": 1}
    merge_config()                        -> {}
"""

from collections.abc import Mapping


def merge_config(*layers: Mapping) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
