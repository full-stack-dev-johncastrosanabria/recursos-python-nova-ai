"""Solución de referencia del reto `agregar`.

Dos pasadas: primero se juntan los valores por grupo, después se resume cada
uno. Sale más legible que llevar cinco acumuladores a la vez, y el coste es el
mismo orden de magnitud.
"""

from collections import defaultdict
from collections.abc import Iterable


def summarize_by(records: Iterable[dict], key: str, value: str) -> dict[str, dict]:
    grupos: defaultdict[str, list] = defaultdict(list)

    for registro in records:
        grupos[registro[key]].append(registro[value])

    return {
        nombre: {
            "count": len(valores),
            "total": sum(valores),
            "min": min(valores),
            "max": max(valores),
            "mean": sum(valores) / len(valores),
        }
        for nombre, valores in sorted(grupos.items())
    }
