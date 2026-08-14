"""Solución de referencia del ejercicio `normalizar`.

`_required` recorre la ruta paso a paso para poder decir exactamente dónde se
cortó. Un error que dice `parties.from.account` se arregla sin abrir el
depurador; uno que dice `KeyError: 'account'` no.
"""


def _required(payload: dict, *path: str):
    current = payload
    for index, key in enumerate(path):
        if not isinstance(current, dict) or key not in current:
            raise ValueError(
                f"falta el campo obligatorio {'.'.join(path[: index + 1])}"
            )
        current = current[key]
    return current


def normalize_transfer(payload: dict) -> dict:
    amount = payload.get("amount") or {}

    return {
        "id": _required(payload, "id"),
        "amount_cents": _required(payload, "amount", "cents"),
        "currency": amount.get("currency", "CRC"),
        "origin": _required(payload, "parties", "from", "account"),
        "destination": _required(payload, "parties", "to", "account"),
        "reference": payload.get("reference"),
    }
