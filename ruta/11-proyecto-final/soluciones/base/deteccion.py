"""Solución de referencia del ejercicio `deteccion`.

Capturar la excepción de una regla y seguir es lo que convierte un proceso
nocturno frágil en uno que siempre entrega algo, con el problema señalado.
"""

from collections.abc import Iterable, Mapping


def detect_anomalies(
    transfers: Iterable[Mapping], rules: Iterable[Mapping]
) -> list[dict]:
    rules = list(rules)
    findings: list[dict] = []

    for transfer in transfers:
        for rule in rules:
            try:
                triggered = rule["check"](transfer)
            except Exception:
                findings.append(
                    {"ref": transfer["ref"], "rule": rule["name"], "severity": "error"}
                )
                continue

            if triggered:
                findings.append(
                    {
                        "ref": transfer["ref"],
                        "rule": rule["name"],
                        "severity": rule["severity"],
                    }
                )

    return findings
