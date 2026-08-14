"""Reto: agrupar y resumir sin pandas.

Con doscientas filas, montar pandas añade una dependencia enorme para algo que
un `defaultdict` resuelve mejor. Escribe `summarize_by`, que agrupa registros
por un campo y resume otro:

    summarize_by(
        [
            {"divisa": "CRC", "monto": 100},
            {"divisa": "USD", "monto": 50},
            {"divisa": "CRC", "monto": 300},
        ],
        key="divisa",
        value="monto",
    )
    -> {
        "CRC": {"count": 2, "total": 400, "min": 100, "max": 300, "mean": 200.0},
        "USD": {"count": 1, "total": 50, "min": 50, "max": 50, "mean": 50.0},
    }

Reglas:

- Los grupos salen **ordenados alfabéticamente por su clave**. Un informe que
  cambia de orden entre ejecuciones no se puede comparar con el de ayer — es la
  misma razón que en el módulo 11.
- `mean` es un `float`; `total`, `min` y `max` conservan el tipo de los datos.
- Un registro al que le falte el campo `key` o el campo `value` lanza
  `KeyError`. Aquí faltar **es** un bug: si tus datos no tienen la columna por
  la que agrupas, el resumen no significa nada, y devolver un grupo `None` sería
  esconderlo.
- Sin registros, diccionario vacío.
- No modifiques los registros que recibes.

Pista: `defaultdict(list)` para juntar los valores de cada grupo y luego una
comprehension sobre los grupos ordenados. Dos pasadas se leen mejor que una
sola haciendo malabares con acumuladores.
"""

from collections.abc import Iterable


def summarize_by(records: Iterable[dict], key: str, value: str) -> dict[str, dict]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
