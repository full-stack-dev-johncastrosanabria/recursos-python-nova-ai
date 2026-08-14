"""Solución de referencia del reto `dinero`.

Comparar tuplas hace el trabajo de `__eq__` sin escribir condiciones: las
tuplas ya comparan campo a campo. Y devolver `NotImplemented` en vez de `False`
es lo que hace que `==` responda `False` mientras `<` y `+` levantan
`TypeError`, que es justo la semántica correcta.
"""


class Money:
    def __init__(self, cents: int, currency: str = "CRC") -> None:
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({self.cents}, {self.currency!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.cents, self.currency) == (other.cents, other.currency)

    def __hash__(self) -> int:
        # Al definir __eq__ se pierde el __hash__ heredado. Si el objeto es
        # inmutable de hecho, conviene devolvérselo.
        return hash((self.cents, self.currency))

    def __lt__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return self.cents < other.cents

    def __add__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(self.cents + other.cents, self.currency)
