"""Ejercicio: convertir filas de CSV en registros tipados.

`csv.DictReader` devuelve **siempre texto**, y una fila mal formada en medio de
un archivo de cincuenta mil no puede pasar desapercibida. Escribe `parse_rows`:

    parse_rows([
        {"ref": "TR-1", "monto": "1500", "divisa": "USD"},
        {"ref": "TR-2", "monto": "990"},
    ])
    -> [
        {"ref": "TR-1", "amount_cents": 1500, "currency": "USD"},
        {"ref": "TR-2", "amount_cents": 990, "currency": "CRC"},
    ]

Reglas:

- `ref` es obligatoria y no puede estar vacía ni ser solo espacios. Se le
  quitan los espacios de los extremos.
- `monto` es obligatorio y tiene que convertirse a entero. Ya viene en
  céntimos, así que no hay que multiplicar por nada: solo convertir.
- `divisa` es opcional; si falta o viene vacía, `"CRC"`. Se pasa a mayúsculas.
- Cualquier problema lanza `RowError` **mencionando el número de línea**. Y
  aquí está el detalle que importa: las filas de datos empiezan en la **línea
  2**, porque la 1 es la cabecera del CSV. Un error que dice "línea 1" cuando el
  problema está en la 2 hace perder más tiempo que no decir nada.

`RowError` hereda de `ValueError` para que quien no quiera distinguir pueda
capturar el general, como en el módulo 05.

Fíjate en que esta función **no abre ningún archivo**: recibe filas ya leídas.
Por eso se puede probar sin tocar el disco, y por eso separar el cálculo del
efecto no es una manía sino lo que hace testeable un sistema.
"""

from collections.abc import Iterable


class RowError(ValueError):
    """Una fila del archivo no se pudo interpretar."""


def parse_rows(rows: Iterable[dict]) -> list[dict]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
