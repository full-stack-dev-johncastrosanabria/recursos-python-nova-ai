"""Solución de referencia del ejercicio `listas`.

Se copia primero y se trabaja sobre la copia: así la lista de quien llama queda
intacta. Y el resultado sale de `sorted()`, no de `.sort()`, que devolvería
`None`.
"""


def organizar(refs: list[str], añadir: str, quitar: str) -> list[str]:
    trabajo = list(refs)

    if añadir not in trabajo:
        trabajo.append(añadir)

    if quitar in trabajo:
        trabajo.remove(quitar)

    return sorted(trabajo)
