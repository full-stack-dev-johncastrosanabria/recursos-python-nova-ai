"""Ejercicio: poner plazo a una espera.

Una espera sin plazo no es una espera: es una fuga. Si una petición se queda
colgada, su tarea retiene memoria y —si estaba dentro de un semáforo— también
retiene la plaza, hasta que el proceso se degrada del todo.

Escribe `with_timeout`, que ejecuta una operación asíncrona con un tiempo
máximo:

    await with_timeout(operacion_rapida, seconds=1.0)
    -> el resultado de la operación

    await with_timeout(operacion_lenta, seconds=0.01, default="sin datos")
    -> "sin datos"     ← se agotó el plazo y degradó con gracia

Reglas:

- `operation` es una función sin argumentos que devuelve algo esperable, igual
  que en los ejercicios anteriores del módulo.
- Si termina a tiempo, se devuelve su resultado.
- Si se agota el plazo, se devuelve `default` (que por defecto es `None`). **No
  se propaga el `TimeoutError`**: el sentido de esta función es degradar con
  gracia, y quien la llama distingue por el valor devuelto.
- **Cualquier otra excepción sí se propaga.** Un fallo real no es lo mismo que
  una tardanza, y confundirlos convierte un bug en un "no había datos".
- Un plazo de cero o negativo es `ValueError`.

Pista: `asyncio.timeout` (context manager, desde 3.11) o `asyncio.wait_for`.
Recuerda que la excepción que lanzan es `TimeoutError` — desde 3.11 es la
integrada, la misma que `asyncio.TimeoutError`.
"""

from collections.abc import Callable


async def with_timeout(operation: Callable, seconds: float, default=None):
    raise NotImplementedError("Borra esta línea y escribe tu solución")
