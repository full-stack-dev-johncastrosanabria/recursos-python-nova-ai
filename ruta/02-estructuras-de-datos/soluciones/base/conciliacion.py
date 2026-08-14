"""Solución de referencia del ejercicio `conciliacion`.

Construir los dos conjuntos cuesta O(n + m) y deduplica de paso. Las tres
operaciones que siguen son las tres secciones del informe, literalmente.
"""

from collections.abc import Iterable


def reconcile(
    bank_refs: Iterable[str], internal_refs: Iterable[str]
) -> dict[str, set[str]]:
    bank = set(bank_refs)
    internal = set(internal_refs)

    return {
        "matched": bank & internal,
        "only_bank": bank - internal,
        "only_internal": internal - bank,
    }
