"""Solución de referencia del ejercicio `entrada`.

Se valida antes de convertir (LBYL) porque aquí los fallos son frecuentes —es
entrada de usuario— y porque así el mensaje de error puede decir exactamente
qué estaba mal en vez de repetir el de `int()`.
"""


def parse_amount(raw: str) -> int:
    limpio = raw.strip().replace(",", "")

    if not limpio:
        raise ValueError("no se recibió ningún importe")

    if limpio.startswith("-"):
        raise ValueError(f"el importe no puede ser negativo: {raw!r}")

    unidades, punto, decimales = limpio.partition(".")

    if not unidades.isdigit() or (punto and not decimales.isdigit()):
        raise ValueError(f"{raw!r} no es un importe válido")

    if len(decimales) > 2:
        raise ValueError(
            f"{raw!r} tiene más de dos decimales: un importe no puede partirse "
            "en fracciones de céntimo"
        )

    return int(unidades) * 100 + int(decimales.ljust(2, "0") or 0)
