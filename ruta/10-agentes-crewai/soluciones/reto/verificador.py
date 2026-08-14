"""Solución de referencia del reto `verificador`.

La normalización es lo que evita los falsos positivos: sin ella, un informe que
escribe `1,500` sobre un dato que vale `1500` daría una alerta cada vez, y una
alerta que siempre salta se acaba ignorando.
"""

import re

NUMERO = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _normalizar(valor: str) -> str:
    limpio = valor.replace(",", "")
    if "." in limpio:
        limpio = limpio.rstrip("0").rstrip(".")
    return limpio or "0"


def unsupported_numbers(text: str, data: dict) -> list[str]:
    respaldados = {
        _normalizar(str(valor))
        for valor in data.values()
        if isinstance(valor, (int, float)) and not isinstance(valor, bool)
    }

    sospechosos: list[str] = []
    for encontrado in NUMERO.findall(text):
        if _normalizar(encontrado) not in respaldados and encontrado not in sospechosos:
            sospechosos.append(encontrado)

    return sospechosos
