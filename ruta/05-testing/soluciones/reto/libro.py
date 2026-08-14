"""Solución de referencia del reto `libro`.

El saldo se recalcula al leerlo en vez de mantenerse en un atributo aparte: así
no puede quedar desincronizado con las entradas, que es la clase de bug que
aparece cuando hay dos fuentes de verdad para el mismo dato.
"""


class DuplicateEntry(Exception):
    """Esa referencia ya estaba registrada."""


class Ledger:
    def __init__(self) -> None:
        self._entries: dict[str, int] = {}

    def add(self, ref: str, cents: int) -> None:
        if cents <= 0:
            raise ValueError(f"el importe debe ser positivo, no {cents}")
        if ref in self._entries:
            raise DuplicateEntry(f"la referencia {ref!r} ya estaba registrada")

        self._entries[ref] = cents

    @property
    def balance(self) -> int:
        return sum(self._entries.values())

    def entries(self) -> tuple[tuple[str, int], ...]:
        return tuple(self._entries.items())

    def __len__(self) -> int:
        return len(self._entries)
