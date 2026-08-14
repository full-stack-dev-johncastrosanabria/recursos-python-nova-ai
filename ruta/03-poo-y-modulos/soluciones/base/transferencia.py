"""Solución de referencia del ejercicio `transferencia`.

`frozen=True` da comparación por valor, hashabilidad e inmutabilidad; `slots`
cambia el diccionario de instancia por ranuras fijas, que ocupa menos y accede
más rápido.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Transfer:
    origin: str
    destination: str
    amount_cents: int
    currency: str = "CRC"

    def __post_init__(self) -> None:
        if self.amount_cents <= 0:
            raise ValueError(f"el monto debe ser positivo, no {self.amount_cents}")
        if self.origin == self.destination:
            raise ValueError(f"origen y destino coinciden: {self.origin}")

    @property
    def amount(self) -> float:
        return self.amount_cents / 100
