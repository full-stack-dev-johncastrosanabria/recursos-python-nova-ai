"""Solución de referencia del reto `estadisticas`."""


def summarize(numbers: list[float]) -> dict[str, float]:
    if not numbers:
        raise ValueError("summarize necesita al menos un número")

    return {
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }
