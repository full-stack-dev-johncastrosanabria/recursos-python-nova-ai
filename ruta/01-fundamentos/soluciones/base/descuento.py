"""Solución de referencia del ejercicio `descuento`.

`is None` en vez de `not`: la pregunta era si el descuento se proporcionó, no
si es distinto de cero. Con `not`, un descuento legítimo de 0 se convierte en
el 12% por defecto y el cliente paga de menos sin que nadie lo vea.
"""

DEFAULT_DISCOUNT_PERCENT = 12


def apply_discount(price_cents: int, discount_percent: int | None = None) -> int:
    if price_cents < 0:
        raise ValueError(f"el precio no puede ser negativo, llegó {price_cents}")

    if discount_percent is None:
        discount_percent = DEFAULT_DISCOUNT_PERCENT

    if not 0 <= discount_percent <= 100:
        raise ValueError(
            f"el descuento debe estar entre 0 y 100, llegó {discount_percent}"
        )

    return price_cents - price_cents * discount_percent // 100
