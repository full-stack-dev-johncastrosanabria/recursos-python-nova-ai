"""Qué hacen y qué no hacen las anotaciones de tipos.

Córrelo con:
    uv run python ruta/04-entorno-y-herramientas/ejemplos/tipos.py
"""

from collections.abc import Iterable


def total(amounts: list[int]) -> int:
    return sum(amounts)


# 1. El intérprete NO comprueba las anotaciones. Esto se ejecuta tan tranquilo.
print("total([1, 2, 3])      ->", total([1, 2, 3]))
print("total((1, 2, 3))      ->", total((1, 2, 3)), " ← era una tupla, no una lista")
print("Nadie se quejó: las anotaciones son metadatos, no validación.\n")

# 2. Pero ahí están, y las herramientas las leen.
print("Anotaciones de total:", total.__annotations__)


# 3. Anotar con el tipo más general que de verdad necesitas abre puertas.
def total_general(amounts: Iterable[int]) -> int:
    """Solo recorro una vez, así que Iterable basta."""
    return sum(amounts)


print("\nCon Iterable, esto también vale:")
print("  desde un generador ->", total_general(n for n in range(1, 4)))
print("  desde un set       ->", total_general({1, 2, 3}))
print("  desde un dict      ->", total_general({1: "a", 2: "b"}))
print("Pedir `list` habría cerrado esas tres puertas sin ganar nada.")


# 4. El caso dominante: la unión con None y el narrowing.
def find_price(catalog: dict[str, int], sku: str) -> int | None:
    return catalog.get(sku)


catalog = {"CAFE-01": 3_500}

for sku in ("CAFE-01", "NO-EXISTE"):
    price = find_price(catalog, sku)

    # Un verificador estático rechazaría usar `price` aquí sin comprobar:
    # podría ser None. Dentro del if, sabe que ya no lo es. Eso es narrowing.
    if price is not None:
        print(f"\n{sku}: {price / 100:.2f}")
    else:
        print(f"\n{sku}: no está en el catálogo")

print(
    "\nSin tipos, ese None viaja y estalla tres capas más adentro.\n"
    "Con tipos, el error aparece mientras escribes."
)
