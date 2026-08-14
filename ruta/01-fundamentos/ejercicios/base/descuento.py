"""Ejercicio: el bug del cero legítimo.

Aplica un descuento a un precio en céntimos:

    apply_discount(10_000)        -> 8_800    (sin especificar: 12% por defecto)
    apply_discount(10_000, 25)    -> 7_500
    apply_discount(10_000, 0)     -> 10_000   ← el caso que importa

Esa última línea es todo el ejercicio. Un descuento de **cero es un valor
legítimo del negocio**: significa "este mes esta sucursal no tiene descuento".
Pero `0` es falsy, así que la versión ingenua…

    if not discount_percent:
        discount_percent = DEFAULT_DISCOUNT_PERCENT

…le aplica el 12% a quien pidió explícitamente ninguno. Es un bug real que
estuvo tres semanas cobrando de menos en el caso real de la guía.

La pregunta correcta no es "¿es verdadero?" sino "¿me lo pasaron?".

Reglas:

- Sin `discount_percent`, se aplica `DEFAULT_DISCOUNT_PERCENT`.
- El porcentaje es un entero de 0 a 100. Fuera de ese rango, `ValueError`.
- Un precio negativo es `ValueError`.
- Devuelve céntimos, entero. Usa división entera: `precio * pct // 100`. Sin
  floats, por lo mismo del ejercicio anterior.
"""

DEFAULT_DISCOUNT_PERCENT = 12


def apply_discount(price_cents: int, discount_percent: int | None = None) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
