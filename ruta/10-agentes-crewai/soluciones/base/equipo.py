"""Solución de referencia del ejercicio `equipo`."""


class CrewFailure(Exception):
    """Una tarea del equipo falló."""

    def __init__(self, message: str, context: dict) -> None:
        super().__init__(message)
        self.context = context


def run_crew(tasks: list[dict], initial_context: dict | None = None) -> dict:
    context = dict(initial_context or {})
    seen: set[str] = set()

    for task in tasks:
        name = task["name"]
        if name in seen:
            raise ValueError(f"hay dos tareas llamadas {name!r}")
        seen.add(name)

        try:
            context[name] = task["run"](context)
        except Exception as error:
            raise CrewFailure(
                f"la tarea {name!r} falló: {error}", context=context
            ) from error

    return context
