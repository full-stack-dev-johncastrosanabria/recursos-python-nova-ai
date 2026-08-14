"""Ejercicio: contar días hábiles.

Escribe `business_days_between`, que cuenta los días de lunes a viernes entre
dos fechas: **incluyendo** la de inicio y **excluyendo** la de fin.

    business_days_between(date(2026, 3, 2), date(2026, 3, 7))   -> 5
    (del lunes 2 al viernes 6, ambos contados; el sábado 7 no entra)

Reglas:

- Si `end` es anterior o igual a `start`, el resultado es 0. No es un error:
  un rango vacío tiene cero días.
- Sábados y domingos no cuentan.
- No te preocupes por los festivos: eso depende del país y sería otro
  ejercicio.

Mira sus tests antes de escribir nada: usan `parametrize` para cubrir una tabla
entera de casos con una sola función. Es la técnica que evita copiar el mismo
test ocho veces.
"""

from datetime import date


def business_days_between(start: date, end: date) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
