"""Solución de referencia del ejercicio `protocolo`.

`__bool__` gana sobre `__len__` en la cascada, y por eso un inventario con
productos pero sin existencias es falso: la pregunta que hace `if inventario:`
es "¿tengo algo que vender?", no "¿tengo filas en la tabla?".
"""


class Inventory:
    def __init__(self, stock: dict[str, int]) -> None:
        self._stock = dict(stock)

    def __len__(self) -> int:
        return len(self._stock)

    def __bool__(self) -> bool:
        return sum(self._stock.values()) > 0

    def __contains__(self, product: str) -> bool:
        return product in self._stock

    def __repr__(self) -> str:
        return f"Inventory({self._stock!r})"
