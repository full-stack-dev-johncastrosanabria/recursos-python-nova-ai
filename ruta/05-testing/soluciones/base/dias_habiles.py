"""Solución de referencia del ejercicio `dias_habiles`.

`weekday()` devuelve 0 para el lunes y 6 para el domingo, así que "es día
hábil" es simplemente "menor que 5".
"""

from datetime import date, timedelta


def business_days_between(start: date, end: date) -> int:
    if end <= start:
        return 0

    total = 0
    current = start
    while current < end:
        if current.weekday() < 5:
            total += 1
        current += timedelta(days=1)

    return total
