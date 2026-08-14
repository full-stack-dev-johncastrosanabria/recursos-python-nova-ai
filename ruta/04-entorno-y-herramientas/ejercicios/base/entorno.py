"""Ejercicio: leer un archivo .env de verdad.

Escribe `parse_env`, que recibe el contenido de un archivo `.env` como texto y
devuelve un diccionario.

    parse_env("HOST=db.internal\\nPORT=5432")
    -> {"HOST": "db.internal", "PORT": "5432"}

Reglas, que salen de cómo son los .env reales:

- Las líneas vacías y las que empiezan por `#` (después de quitar espacios) se
  ignoran.
- Se quitan los espacios alrededor de la clave y del valor.
- El valor puede ir entre comillas simples o dobles; en ese caso se quitan.
  `SALUDO="hola mundo"` da `hola mundo`.
- El valor puede contener `=`. Se parte por el **primer** `=` solamente:
  `URL=postgres://a=b` da `postgres://a=b`.
- Si una clave aparece dos veces, gana la última.
- Una línea que no esté vacía, no sea comentario y no tenga `=` es un error:
  lanza `ValueError` mencionando el número de línea (empezando en 1). Un .env
  mal escrito debe fallar al arrancar, no dejar la variable sin cargar y que te
  enteres tres horas después.

Todos los valores son strings. Convertirlos a int o bool es trabajo del reto.
"""


def parse_env(text: str) -> dict[str, str]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
