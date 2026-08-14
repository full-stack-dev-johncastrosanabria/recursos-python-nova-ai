"""Solución de referencia del ejercicio `cuenta`."""


class InsufficientFunds(Exception):
    """No hay saldo suficiente para completar la operación."""


class Account:
    def __init__(self, holder: str, balance_cents: int = 0) -> None:
        self.holder = holder
        self.balance_cents = balance_cents

    def deposit(self, cents: int) -> None:
        if cents <= 0:
            raise ValueError(f"el depósito debe ser positivo, no {cents}")
        self.balance_cents += cents

    def withdraw(self, cents: int) -> None:
        if cents <= 0:
            raise ValueError(f"el retiro debe ser positivo, no {cents}")
        if cents > self.balance_cents:
            raise InsufficientFunds(
                f"no se pueden retirar {cents} céntimos: "
                f"el saldo disponible es {self.balance_cents}"
            )
        self.balance_cents -= cents

    def __repr__(self) -> str:
        return f"Account({self.holder!r}, {self.balance_cents})"
