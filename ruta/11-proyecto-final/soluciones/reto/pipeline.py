"""Solución de referencia del reto `pipeline`.

Las tres etapas encadenadas y nada más: el pipeline no sabe cómo se detecta ni
cómo se redacta, solo en qué orden va cada cosa. Por eso se puede probar con
piezas de mentira y por eso cambiar el motor de reglas no lo toca.
"""

from collections.abc import Callable, Iterable, Mapping


def run_pipeline(
    bank_moves: Iterable[Mapping],
    internal_records: Iterable[Mapping],
    *,
    detect: Callable,
    render: Callable,
) -> dict:
    bank_moves = list(bank_moves)
    internal_records = list(internal_records)

    bank_refs = {move["ref"] for move in bank_moves}
    internal_refs = {record["ref"] for record in internal_records}

    result = {
        "matched": bank_refs & internal_refs,
        "only_bank": bank_refs - internal_refs,
        "only_internal": internal_refs - bank_refs,
        "anomalies": detect(bank_moves),
    }

    return {**result, "report": render(result)}
