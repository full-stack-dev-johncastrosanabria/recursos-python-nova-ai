"""Solución de referencia del reto `baraja`.

Delegar en una lista interna es lo que hace que el slicing y los índices
negativos funcionen sin escribir una línea para ellos: `list` ya habla ese
protocolo, y `__getitem__` se limita a pasarle la pregunta.
"""

RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
SUITS = ("picas", "corazones", "diamantes", "tréboles")


class Deck:
    def __init__(self) -> None:
        self._cards = [f"{rank} de {suit}" for suit in SUITS for rank in RANKS]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
