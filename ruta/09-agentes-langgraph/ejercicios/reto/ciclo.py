"""Reto: el bucle de agente completo.

Escribe `run_agent`, que hace el ida y vuelta con el modelo hasta obtener una
respuesta en texto.

El `model` que recibes es una función que toma la lista de mensajes y devuelve
un diccionario, de una de estas dos formas:

    {"type": "text", "text": "La respuesta es 42"}
    {"type": "tool_use", "name": "get_balance", "input": {"account": "CR01-0001"}}

Tu trabajo en cada vuelta:

- Si es `text`, terminaste. Devuelve el resultado (ver más abajo).
- Si es `tool_use`, busca la herramienta en `tools`, ejecútala con `**input`,
  y añade a los mensajes primero lo que dijo el modelo y después el resultado:

      {"role": "assistant", "content": respuesta}
      {"role": "user", "content": {"type": "tool_result", "content": str(resultado)}}

Devuelve un diccionario:

    {"answer": "La respuesta es 42", "steps": 3, "messages": [...]}

donde `steps` es cuántas veces llamaste al modelo.

Reglas que separan un ejercicio de un agente que se puede desplegar:

- **Tope de pasos.** Si se agotan sin respuesta en texto, lanza `RuntimeError`.
- **Una herramienta desconocida no revienta el agente.** Si el modelo pide algo
  que no está en `tools`, el resultado que le devuelves es un texto de error
  (`"error: no existe la herramienta X"`) y el bucle continúa. El modelo puede
  corregirse; una excepción no le da esa oportunidad.
- **Si la herramienta falla, tampoco revienta.** Captura la excepción y
  devuélvela como resultado (`"error: ..."`). Es lo mismo: información para que
  el modelo reaccione.
- Los mensajes empiezan con `{"role": "user", "content": user_message}`.
"""

from collections.abc import Callable, Mapping


def run_agent(
    model: Callable,
    tools: Mapping[str, Callable],
    user_message: str,
    max_steps: int = 5,
) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
