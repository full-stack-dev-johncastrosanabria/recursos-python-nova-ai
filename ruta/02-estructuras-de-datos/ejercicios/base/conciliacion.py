"""Ejercicio: conciliar movimientos con álgebra de conjuntos.

Es el caso real de la guía. Recibes las referencias que reporta el banco y las
que tienes en tus registros internos, y devuelves las tres secciones del
informe:

    reconcile(["A", "B", "C"], ["B", "C", "D"])
    -> {"matched": {"B", "C"}, "only_bank": {"A"}, "only_internal": {"D"}}

Requisitos:

- Los tres valores son conjuntos (`set`), no listas.
- Las referencias repetidas en la entrada cuentan una sola vez.
- Debe funcionar con cualquier iterable, no solo con listas: un generador que
  lea un CSV enorme tiene que servir igual.

Si te sale un bucle dentro de otro, párate y vuelve a la sección 6 de la guía:
esto son tres operaciones de conjuntos.
"""

from collections.abc import Iterable


def reconcile(
    bank_refs: Iterable[str], internal_refs: Iterable[str]
) -> dict[str, set[str]]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
