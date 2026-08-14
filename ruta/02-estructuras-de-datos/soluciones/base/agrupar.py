"""Solución de referencia del ejercicio `agrupar`.

`defaultdict(list)` evita el "si no está, créala" mientras se construye, y el
`dict(...)` final devuelve un diccionario normal: quien reciba el resultado ya
no puede crear grupos sin darse cuenta con solo consultarlo.
"""

from collections import defaultdict
from collections.abc import Iterable


def group_by_currency(transfers: Iterable[dict]) -> dict[str, list[dict]]:
    groups: defaultdict[str, list[dict]] = defaultdict(list)

    for transfer in transfers:
        groups[transfer["currency"]].append(transfer)

    return dict(groups)
