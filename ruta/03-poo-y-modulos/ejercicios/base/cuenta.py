"""Ejercicio: una clase con estado, comportamiento y errores de dominio.

Implementa `Account`. El saldo se guarda en céntimos y como entero: nunca en
`float`.

    cuenta = Account("Ana")
    cuenta.balance_cents        -> 0
    cuenta.deposit(1_500)
    cuenta.balance_cents        -> 1500
    cuenta.withdraw(500)
    cuenta.balance_cents        -> 1000

Reglas:

- `Account(holder)` empieza con saldo 0. `Account(holder, 5_000)` empieza con
  ese saldo.
- `deposit` y `withdraw` rechazan importes de cero o negativos con
  `ValueError`.
- Sacar más de lo que hay lanza `InsufficientFunds`, que ya está definida abajo.
  El mensaje del error debe incluir el saldo disponible: quien lo lea en un log
  a las tres de la mañana lo agradecerá.
- Una cuenta se representa como `Account('Ana', 1000)` al imprimirla en el
  intérprete. Eso es `__repr__`.

`InsufficientFunds` hereda de `Exception`, no de `ValueError`: es un error del
dominio del negocio, no un argumento mal formado. Quien capture uno no quiere
capturar el otro por accidente.
"""


class InsufficientFunds(Exception):
    """No hay saldo suficiente para completar la operación."""


class Account:
    def __init__(self, holder: str, balance_cents: int = 0) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
