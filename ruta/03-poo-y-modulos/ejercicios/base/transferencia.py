"""Ejercicio: una dataclass inmutable que se valida al nacer.

Convierte `Transfer` en una dataclass congelada con estos campos:

    origin: str
    destination: str
    amount_cents: int
    currency: str = "CRC"

Y añádele:

- Validación en `__post_init__`: `amount_cents` tiene que ser positivo
  (`ValueError` si no lo es) y `origin` no puede ser igual a `destination`
  (`ValueError` también: transferirse a uno mismo es un error, no una
  transferencia de cero).
- Una propiedad `amount` que devuelva el importe en unidades, como `float`:
  150_000 céntimos son 1500.0.

Al ser `frozen=True` obtienes tres cosas gratis: comparación por valor,
hashabilidad (entra en un `set` y sirve de clave de dict) y la garantía de que
nadie la modifica después de crearla.

    t = Transfer("CR-01", "CR-02", 150_000)
    t.amount                              -> 1500.0
    t == Transfer("CR-01", "CR-02", 150_000)   -> True
    {t}                                   -> funciona: es hashable
    t.amount_cents = 5                    -> FrozenInstanceError
"""

from dataclasses import dataclass


@dataclass
class Transfer:
    origin: str
    destination: str
    amount_cents: int
    currency: str = "CRC"

    def __post_init__(self) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
