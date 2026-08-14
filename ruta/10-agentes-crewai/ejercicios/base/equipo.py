"""Ejercicio: encadenar tareas pasando el contexto.

El corazón del modelo de CrewAI: cada tarea recibe lo que produjeron las
anteriores y añade lo suyo.

Escribe `run_crew`:

    tasks = [
        {"name": "extraer",   "run": lambda ctx: [1, 2, 3]},
        {"name": "sumar",     "run": lambda ctx: sum(ctx["extraer"])},
        {"name": "redactar",  "run": lambda ctx: f"El total es {ctx['sumar']}"},
    ]

    run_crew(tasks)
    -> {"extraer": [1, 2, 3], "sumar": 6, "redactar": "El total es 6"}

Reglas:

- Cada tarea se ejecuta en orden, recibiendo el contexto acumulado hasta ese
  momento. Su resultado se guarda bajo su `name`.
- Se puede partir de un contexto inicial: `run_crew(tasks, {"ref": "TR-1"})`.
- Dos tareas con el mismo nombre es un error (`ValueError`): la segunda
  pisaría a la primera en silencio.
- Si una tarea lanza una excepción, se envuelve en `CrewFailure`, que debe
  llevar el nombre de la tarea que falló en su mensaje y el contexto acumulado
  hasta entonces en su atributo `context`. Perder el trabajo de las tareas
  anteriores porque falló la cuarta es tirar tokens ya pagados.
- El contexto inicial que te pasan no se modifica.
"""


class CrewFailure(Exception):
    """Una tarea del equipo falló."""

    def __init__(self, message: str, context: dict) -> None:
        super().__init__(message)
        self.context = context


def run_crew(tasks: list[dict], initial_context: dict | None = None) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
