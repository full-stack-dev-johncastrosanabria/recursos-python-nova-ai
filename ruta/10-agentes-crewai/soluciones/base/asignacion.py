"""Solución de referencia del ejercicio `asignacion`.

`>=` entre conjuntos es "contiene a todos los de", así que la regla 1 cabe en
una condición. Y `min` con `key` elige al más especializado conservando el
orden en caso de empate, porque `min` devuelve el primero de los mínimos.
"""


class NoSuitableAgent(Exception):
    """Ningún agente tiene las herramientas que la tarea necesita."""


def assign(agents: list[dict], task: dict) -> dict:
    needs = set(task.get("needs", ()))
    candidates = [agent for agent in agents if set(agent["tools"]) >= needs]

    if not candidates:
        disponibles = (
            set().union(*(set(a["tools"]) for a in agents)) if agents else set()
        )
        faltan = sorted(needs - disponibles) or sorted(needs)
        raise NoSuitableAgent(
            f"ningún agente cubre la tarea {task.get('name', '?')!r}: "
            f"faltan herramientas {', '.join(faltan)}"
        )

    return min(candidates, key=lambda agent: len(agent["tools"]))
