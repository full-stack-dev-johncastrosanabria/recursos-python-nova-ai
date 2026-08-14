"""Solución de referencia del reto `clasificar`.

El orden de los `case` es el contrato: el pago grande va antes que el pago a
secas porque, si no, el patrón general lo capturaría primero y la guarda nunca
llegaría a evaluarse.
"""


def describe(event: dict) -> str:
    match event:
        case {"tipo": "pago", "monto": monto} if monto > 100_000:
            return f"pago grande de {monto}"
        case {"tipo": "pago", "monto": monto}:
            return f"pago de {monto}"
        case {"tipo": "reverso", "ref": ref}:
            return f"reverso de {ref}"
        case {"tipo": "cierre"}:
            return "cierre de día"
        case _:
            return "evento desconocido"
