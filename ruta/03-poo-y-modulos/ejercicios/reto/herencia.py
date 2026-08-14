"""Reto: una jerarquía pequeña, `super()` y el MRO.

Tres clases de cuenta, cada una añadiendo algo a la anterior:

    Account          — la base: titular, saldo y una comisión fija
    SavingsAccount   — añade un tipo de interés
    PremiumAccount   — no paga comisión

Comportamiento esperado:

    a = Account("Ana", 100_000)
    a.describe()          -> "Ana: 100000"
    a.fee_cents()         -> 500

    s = SavingsAccount("Beto", 200_000, rate=0.03)
    s.describe()          -> "Beto: 200000 (ahorro al 3.0%)"
    s.fee_cents()         -> 500          ← heredada sin tocar

    p = PremiumAccount("Caro", 500_000, rate=0.05)
    p.describe()          -> "Caro: 500000 (ahorro al 5.0%) [premium]"
    p.fee_cents()         -> 0            ← sobrescrita

Reglas:

- `Account.__init__(holder, balance_cents=0)`.
- `Account.describe()` devuelve `"{holder}: {balance_cents}"`.
- `Account.fee_cents()` devuelve la constante de clase `FEE_CENTS`, que vale
  500. Léela desde `self` para que una subclase pueda cambiarla.
- `SavingsAccount.__init__` añade `rate=0.02` y **llama a `super().__init__`**
  en vez de repetir las asignaciones.
- `SavingsAccount.describe()` **reutiliza** el de la base con `super()` y le
  añade `" (ahorro al X%)"`, con el porcentaje a un decimal (`f"{rate:.1%}"`).
- `PremiumAccount` hereda de `SavingsAccount`, añade `" [premium]"` a la
  descripción —otra vez con `super()`— y devuelve 0 de comisión.

El punto del ejercicio no es la jerarquía, que es de juguete: es que `super()`
te deja **extender** en vez de **copiar**. Si en `SavingsAccount.describe()`
repites el formato de la base, el día que cambie la base tendrás dos verdades.

Sus tests además comprueban el MRO de `PremiumAccount`. Míralo tú también:

    PremiumAccount.__mro__
"""

FEE_CENTS = 500


class Account:
    FEE_CENTS = FEE_CENTS

    def __init__(self, holder: str, balance_cents: int = 0) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
