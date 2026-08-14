"""Solución de referencia del reto `herencia`.

Cada `describe` llama al de arriba y le añade lo suyo. El formato del titular y
el saldo se escribe **una sola vez**, en la base: si mañana cambia, cambia en
un sitio.
"""

FEE_CENTS = 500


class Account:
    FEE_CENTS = FEE_CENTS

    def __init__(self, holder: str, balance_cents: int = 0) -> None:
        self.holder = holder
        self.balance_cents = balance_cents

    def describe(self) -> str:
        return f"{self.holder}: {self.balance_cents}"

    def fee_cents(self) -> int:
        return self.FEE_CENTS


class SavingsAccount(Account):
    def __init__(self, holder: str, balance_cents: int = 0, rate: float = 0.02) -> None:
        super().__init__(holder, balance_cents)
        self.rate = rate

    def describe(self) -> str:
        return f"{super().describe()} (ahorro al {self.rate:.1%})"


class PremiumAccount(SavingsAccount):
    FEE_CENTS = 0

    def describe(self) -> str:
        return f"{super().describe()} [premium]"
