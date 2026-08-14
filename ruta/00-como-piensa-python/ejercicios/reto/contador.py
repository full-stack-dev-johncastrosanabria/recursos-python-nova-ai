"""Reto: closures y `nonlocal`, o la regla LEGB en acción.

Escribe `make_counter`, que devuelve **dos funciones** que comparten un mismo
contador privado:

    incrementar, valor = make_counter()

    valor()          -> 0
    incrementar()    -> 1
    incrementar()    -> 2
    valor()          -> 2

Y dos contadores distintos son independientes:

    inc_a, val_a = make_counter()
    inc_b, val_b = make_counter(100)

    inc_a()          -> 1
    val_b()          -> 100     ← el de a no lo tocó

Aquí es donde el modelo mental 5 deja de ser teoría. `incrementar` necesita
**reasignar** una variable que vive en el ámbito de `make_counter`, y en Python
asignar dentro de una función crea una variable local nueva por defecto. Sin
declararlo, esto falla:

    def make_counter(start=0):
        count = start
        def incrementar():
            count = count + 1     # UnboundLocalError: lee una local sin asignar
            return count
        ...

La palabra que lo arregla es `nonlocal`, y dice exactamente "esta asignación se
refiere a la variable del ámbito de fuera, no crees una local".

Fíjate en que `valor` **no** la necesita: leer sí atraviesa los ámbitos hacia
fuera sin declarar nada. Solo asignar exige la declaración. Esa asimetría es
todo el ejercicio.

Reglas:

- `make_counter(start=0)` devuelve la tupla `(incrementar, valor)`.
- `incrementar()` suma uno y **devuelve el valor nuevo**.
- `valor()` devuelve el actual sin modificarlo.
- Los contadores son independientes entre sí.
"""

from collections.abc import Callable


def make_counter(start: int = 0) -> tuple[Callable[[], int], Callable[[], int]]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
