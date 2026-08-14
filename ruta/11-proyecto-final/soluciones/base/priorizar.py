"""Solución de referencia del ejercicio `priorizar`.

La clave de ordenación devuelve una tupla `(rango de severidad, referencia)`,
así que una sola pasada de `sorted` ordena por lo principal y desempata por lo
secundario. Y como `sorted` no muta, la lista de quien llama queda intacta.
"""

SEVERIDADES = ("error", "alta", "media", "baja")


def prioritize(anomalies: list[dict], budget: int) -> list[dict]:
    if budget < 0:
        raise ValueError(f"el presupuesto no puede ser negativo, llegó {budget}")

    def orden(anomalia: dict) -> tuple[int, str]:
        severidad = anomalia.get("severity")
        rango = (
            SEVERIDADES.index(severidad)
            if severidad in SEVERIDADES
            else len(SEVERIDADES)
        )
        return rango, anomalia.get("ref", "")

    return sorted(anomalies, key=orden)[:budget]
