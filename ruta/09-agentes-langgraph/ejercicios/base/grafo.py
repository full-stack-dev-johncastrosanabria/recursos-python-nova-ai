"""Ejercicio: el ejecutor del grafo.

Escribe `run_graph`, que recorre un grafo de estado hasta llegar al final.

    nodes = {
        "pensar":     lambda state: {"steps": state["steps"] + 1},
        "herramienta": lambda state: {"datos": "listo"},
    }
    edges = {
        "pensar": lambda state: "herramienta" if state["steps"] < 2 else END,
        "herramienta": lambda state: "pensar",
    }

    run_graph(nodes, edges, start="pensar", initial_state={"steps": 0})

Cómo funciona cada vuelta:

1. Se ejecuta el nodo actual con el estado: devuelve una actualización.
2. La actualización se mezcla sobre el estado (reemplazando claves; los
   reducers son el otro ejercicio).
3. Se pregunta a la arista de ese nodo cuál es el siguiente.
4. Si el siguiente es `END`, se devuelve el estado final.

Reglas:

- Devuelve el estado final, no el historial.
- **`max_steps` es obligatorio de respetar**: si se superan, lanza
  `RuntimeError`. Un grafo con ciclos y sin tope es una factura abierta.
- Si el nodo a ejecutar no existe en `nodes`, lanza `ValueError` con su nombre.
  Lo mismo si un nodo no tiene arista definida.
- El estado inicial no se modifica.
- Si `start` es `END`, se devuelve el estado inicial sin ejecutar nada.
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
    raise NotImplementedError("Borra esta línea y escribe tu solución")
