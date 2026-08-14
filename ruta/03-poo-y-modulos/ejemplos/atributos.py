"""Dónde viven los atributos, y la trampa del mutable compartido.

Córrelo con:
    uv run python ruta/03-poo-y-modulos/ejemplos/atributos.py
"""

from dataclasses import dataclass, field


class Account:
    banco = "Nova Bank"  # atributo de CLASE: uno solo para todas

    def __init__(self, holder: str, balance_cents: int = 0) -> None:
        self.holder = holder  # atributos de INSTANCIA: uno por objeto
        self.balance_cents = balance_cents


ana = Account("Ana", 1_000)
beto = Account("Beto", 500)

print("Atributos de la instancia ana :", ana.__dict__)
print("Atributos de la instancia beto:", beto.__dict__)
print("El banco no está en la instancia, se hereda de la clase:", ana.banco)
print("Métodos y atributos de clase :", [k for k in vars(Account) if k != "__dict__"])

# La búsqueda es un recorrido: instancia -> clase -> bases. Sin magia.
ana.banco = "Otro Banco"  # esto CREA un atributo en la instancia
print("\nTras ana.banco = 'Otro Banco':")
print(f"  ana.banco  -> {ana.banco}   (ahora está en su __dict__)")
print(f"  beto.banco -> {beto.banco}  (sigue leyendo el de la clase)")


# ── La trampa: un mutable como atributo de clase ──────────────────
class BasketRoto:
    items = []  # UNA lista para todas las instancias

    def add(self, item):
        self.items.append(item)


a, b = BasketRoto(), BasketRoto()
a.add("pan")
print(f"\nBasketRoto: a añade 'pan' y el carrito de b es {b.items}")
print("Es el mismo bug del argumento mutable por defecto, con otro disfraz.")


class BasketBien:
    def __init__(self) -> None:
        self.items = []  # una lista NUEVA por instancia

    def add(self, item):
        self.items.append(item)


c, d = BasketBien(), BasketBien()
c.add("pan")
print(f"BasketBien: c añade 'pan' y el carrito de d es {d.items}")


# Con dataclasses, el mismo problema tiene una solución declarada.
@dataclass
class BasketDataclass:
    items: list[str] = field(default_factory=list)  # una lista por instancia


e, f = BasketDataclass(), BasketDataclass()
e.items.append("pan")
print(f"Dataclass con default_factory: el carrito de f es {f.items}")
