"""Reto: un libro de asientos con estado.

Implementa `Ledger`, que va guardando movimientos y mantiene el saldo.

    libro = Ledger()
    libro.add("TR-001", 1_500)
    libro.add("TR-002", 2_500)
    libro.balance        -> 4000
    len(libro)           -> 2
    libro.entries()      -> (("TR-001", 1500), ("TR-002", 2500))

Reglas:

- `balance` es una **propiedad**, no un método: se lee como `libro.balance`.
- `entries()` devuelve una **tupla** de pares, en el orden en que se añadieron.
  Que sea una tupla no es un capricho: si devolvieras la lista interna, quien
  la recibiera podría modificarla y romper el saldo por la espalda.
- Añadir una referencia repetida lanza `DuplicateEntry`. Es el problema de
  idempotencia real: si un webhook llega dos veces, no puedes contarlo dos
  veces.
- Un importe de cero o negativo lanza `ValueError`.
- Un libro recién creado tiene saldo 0 y longitud 0.

Mira sus tests: usan una fixture para construir el libro. Fíjate en que cada
test recibe uno nuevo, así que ninguno puede ensuciar a otro.
"""


class DuplicateEntry(Exception):
    """Esa referencia ya estaba registrada."""


class Ledger:
    def __init__(self) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
