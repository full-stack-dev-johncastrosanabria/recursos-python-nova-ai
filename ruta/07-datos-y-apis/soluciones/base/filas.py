"""Solución de referencia del ejercicio `filas`.

El `start=2` del `enumerate` es todo el detalle: las filas de datos empiezan
después de la cabecera, y un número de línea equivocado en un error hace perder
más tiempo que no darlo.
"""

from collections.abc import Iterable


class RowError(ValueError):
    """Una fila del archivo no se pudo interpretar."""


def parse_rows(rows: Iterable[dict]) -> list[dict]:
    registros = []

    for numero, fila in enumerate(rows, start=2):
        ref = (fila.get("ref") or "").strip()
        if not ref:
            raise RowError(f"línea {numero}: falta la referencia")

        crudo = (fila.get("monto") or "").strip()
        try:
            monto = int(crudo)
        except ValueError as error:
            raise RowError(
                f"línea {numero}: el monto {crudo!r} no es un entero"
            ) from error

        divisa = (fila.get("divisa") or "").strip().upper() or "CRC"

        registros.append({"ref": ref, "amount_cents": monto, "currency": divisa})

    return registros
