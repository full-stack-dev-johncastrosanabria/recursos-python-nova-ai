"""Solución de referencia del reto `presupuesto`.

Se para en la primera que no cabe en vez de buscar una más barata más
adelante: las tareas están en orden porque unas dependen de otras.
"""


def run_with_budget(
    tasks: list[dict], budget: int, initial_context: dict | None = None
) -> dict:
    if budget < 0:
        raise ValueError(f"el presupuesto no puede ser negativo, llegó {budget}")

    context = dict(initial_context or {})
    completed: list[str] = []
    spent = 0

    for index, task in enumerate(tasks):
        if spent + task["cost"] > budget:
            return {
                "context": context,
                "completed": completed,
                "skipped": [t["name"] for t in tasks[index:]],
                "spent": spent,
            }

        spent += task["cost"]
        context[task["name"]] = task["run"](context)
        completed.append(task["name"])

    return {
        "context": context,
        "completed": completed,
        "skipped": [],
        "spent": spent,
    }
