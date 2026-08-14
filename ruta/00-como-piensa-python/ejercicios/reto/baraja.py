"""Reto: hacer que tu clase hable los protocolos del lenguaje.

Implementa `Deck`, una baraja de 52 cartas, definiendo **solo dos** métodos
especiales: `__len__` y `__getitem__`. Con eso basta para que funcionen
`len(deck)`, `deck[0]`, el slicing, el operador `in` y el bucle `for`.

Que la iteración funcione sin definir `__iter__` no es casualidad: Python
recurre al protocolo de secuencia antiguo, pidiendo `deck[0]`, `deck[1]`… hasta
que la clase levanta `IndexError`. Ese es el modelo mental 3 en acción.

Las cartas son textos con el formato `"{rango} de {palo}"`, generadas
recorriendo los palos por fuera y los rangos por dentro:

    RANKS = ("2","3","4","5","6","7","8","9","10","J","Q","K","A")
    SUITS = ("picas", "corazones", "diamantes", "tréboles")

    len(deck)   -> 52
    deck[0]     -> "2 de picas"
    deck[12]    -> "A de picas"
    deck[13]    -> "2 de corazones"
    deck[-1]    -> "A de tréboles"

Si usas una lista interna y delegas en ella, el slicing y los índices negativos
te salen gratis.
"""

RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
SUITS = ("picas", "corazones", "diamantes", "tréboles")


class Deck:
    def __init__(self) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
