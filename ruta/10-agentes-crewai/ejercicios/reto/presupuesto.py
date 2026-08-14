"""Reto: un orquestador que sabe cuándo parar.

Cada agente que añades cuesta. Escribe `run_with_budget`, que ejecuta tareas
mientras alcance el presupuesto y dice con claridad qué quedó sin hacer.

    tasks = [
        {"name": "extraer",  "cost": 2, "run": lambda ctx: "datos"},
        {"name": "analizar", "cost": 5, "run": lambda ctx: "análisis"},
        {"name": "redactar", "cost": 4, "run": lambda ctx: "informe"},
    ]

    run_with_budget(tasks, budget=8)
    -> {
        "context": {"extraer": "datos", "analizar": "análisis"},
        "completed": ["extraer", "analizar"],
        "skipped": ["redactar"],
        "spent": 7,
    }

Reglas:

- Las tareas se intentan **en orden**.
- Una tarea se ejecuta solo si su `cost` cabe en lo que queda de presupuesto.
- Al no caber una, **se para**: no se sigue buscando una más barata más
  adelante. Un informe a medias con los pasos en orden es útil; uno con el paso
  1 y el 5 no.
- `spent` es la suma de lo que costaron las completadas.
- Igual que en `equipo`, cada tarea recibe el contexto acumulado.
- Presupuesto negativo es `ValueError`. Un presupuesto de 0 es válido: no se
  ejecuta nada y todo queda en `skipped`.
- Si una tarea falla, su coste **sí se ha gastado** —la llamada al modelo se
  pagó igual— y la excepción se propaga tal cual, sin envolver.
"""


def run_with_budget(
    tasks: list[dict], budget: int, initial_context: dict | None = None
) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
