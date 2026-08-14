"""Por qué el dinero no va en float, comprobado en tu propia máquina.

Córrelo con:
    uv run python ruta/01-fundamentos/ejemplos/dinero_y_floats.py
"""

import math
from decimal import ROUND_HALF_UP, Decimal

print("── El clásico ──")
print(f"0.1 + 0.2          = {0.1 + 0.2!r}")
print(f"0.1 + 0.2 == 0.3   -> {0.1 + 0.2 == 0.3}")
print("No es un bug de Python: es IEEE 754, igual en C, Java y JavaScript.")
cerca = math.isclose(0.1 + 0.2, 0.3)
print(f"Así se comparan bien: math.isclose(0.1 + 0.2, 0.3) -> {cerca}")

print("\n── El error se acumula ──")
muchos = [0.1] * 1_000_000
print(f"sum([0.1] * 1_000_000)       = {sum(muchos)!r}")
print(f"math.fsum([0.1] * 1_000_000) = {math.fsum(muchos)!r}   ← suma compensada")

print("\n── Una factura con float ──")
precio_float = 13990.00
iva_float = precio_float * 0.13
print(f"precio {precio_float}  iva {iva_float!r}")
print(f"total  {precio_float + iva_float!r}   ← ¿cuánto se cobra exactamente?")

print("\n── La misma factura con Decimal ──")
precio = Decimal("13990.00")
iva = (precio * Decimal("0.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(f"precio {precio}  iva {iva}")
print(f"total  {precio + iva}   ← auditable al céntimo")

print("\n── La trampa al construir un Decimal ──")
print(f'Decimal("0.1") = {Decimal("0.1")}')
print(f"Decimal(0.1)   = {Decimal(0.1)}")
print("Construir desde float importa el error binario. Siempre desde texto.")

print("\n── La otra forma válida: enteros de céntimos ──")
precio_cents = 1_399_000
iva_cents = precio_cents * 13 // 100
total_cents = precio_cents + iva_cents


def formatear(cents: int) -> str:
    signo = "-" if cents < 0 else ""
    unidades, centimos = divmod(abs(cents), 100)
    return f"{signo}{unidades:,}.{centimos:02d}"


print(f"precio {formatear(precio_cents)}  iva {formatear(iva_cents)}")
print(f"total  {formatear(total_cents)}   ← aritmética de enteros, exacta")

print("\n── Y el cero legítimo, de regalo ──")
DESCUENTO_ESTANDAR = 12


def mal(precio_cents, descuento=None):
    if not descuento:  # ← 0 es falsy
        descuento = DESCUENTO_ESTANDAR
    return precio_cents - precio_cents * descuento // 100


def bien(precio_cents, descuento=None):
    if descuento is None:  # ← la pregunta correcta
        descuento = DESCUENTO_ESTANDAR
    return precio_cents - precio_cents * descuento // 100


print("Sucursal con descuento 0 (legítimo: este mes no tiene)")
print(f"  versión con `not`      -> {formatear(mal(10_000, 0))}   ← le aplicó el 12%")
print(f"  versión con `is None`  -> {formatear(bien(10_000, 0))}  ← correcto")
