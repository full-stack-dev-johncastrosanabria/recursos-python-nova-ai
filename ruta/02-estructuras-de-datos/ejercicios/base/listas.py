"""Ejercicio: los métodos de lista, con sus dos trampas.

Escribe `organizar`, que toma una lista de referencias, añade una, quita otra y
devuelve el resultado **ordenado**:

    organizar(["TR-003", "TR-001"], añadir="TR-002", quitar="TR-003")
    -> ["TR-001", "TR-002"]

Reglas:

- `añadir` se incorpora **solo si no estaba ya**. Añadir un duplicado no tiene
  sentido en un listado de referencias.
- `quitar` se elimina si está. Si no está, no pasa nada: no es un error.
- El resultado sale **ordenado alfabéticamente**.
- **No modifiques la lista que recibes.** Quien te llama no espera que le
  cambies su lista.

Las dos trampas que este ejercicio existe para que cometas aquí y no en
producción:

1. `lista.sort()` ordena en el sitio y devuelve `None`. Si escribes
   `resultado = lista.sort()`, `resultado` vale `None` y el bug aparece más
   adelante. La función que devuelve una lista nueva es `sorted()`.
2. `remove` borra **por valor** y lanza `ValueError` si el valor no está. O
   compruebas antes con `in`, o capturas la excepción. Las dos vías valen.
"""


def organizar(refs: list[str], añadir: str, quitar: str) -> list[str]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
