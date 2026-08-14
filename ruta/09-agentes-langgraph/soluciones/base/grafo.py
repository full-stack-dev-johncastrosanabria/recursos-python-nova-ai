"""Solución de referencia del ejercicio `grafo`.

El contador de pasos no es una precaución teórica: es lo único que separa un
grafo con ciclos de una factura sin límite.
"""

from collections.abc import Callable, Mapping

END = "__end__"


def run_graph(
    nodes: Mapping[str, Callable],
    edges: Mapping[str, Callable],
    start: str,
    initial_state: Mapping,
    max_steps: int = 25,
) -> dict:
    state = dict(initial_state)
    current = start
    steps = 0

    while current != END:
        if current not in nodes:
            raise ValueError(f"no existe el nodo {current!r}")
        if current not in edges:
            raise ValueError(f"el nodo {current!r} no tiene arista de salida")

        steps += 1
        if steps > max_steps:
            raise RuntimeError(
                f"el grafo superó los {max_steps} pasos sin llegar al final; "
                "probablemente hay un ciclo sin condición de salida"
            )

        state.update(nodes[current](state))
        current = edges[current](state)

    return state
