"""Solución de referencia del reto `ciclo`.

Los errores se le devuelven al modelo como resultado en vez de propagarse: un
agente que revienta ante una herramienta que falla no puede corregirse, y
corregirse es justamente lo que sabe hacer.
"""

from collections.abc import Callable, Mapping


def run_agent(
    model: Callable,
    tools: Mapping[str, Callable],
    user_message: str,
    max_steps: int = 5,
) -> dict:
    messages = [{"role": "user", "content": user_message}]

    for step in range(1, max_steps + 1):
        response = model(messages)

        if response["type"] == "text":
            return {"answer": response["text"], "steps": step, "messages": messages}

        tool = tools.get(response["name"])
        if tool is None:
            result = f"error: no existe la herramienta {response['name']}"
        else:
            try:
                result = str(tool(**response["input"]))
            except Exception as error:
                result = f"error: {error}"

        messages.append({"role": "assistant", "content": response})
        messages.append(
            {"role": "user", "content": {"type": "tool_result", "content": result}}
        )

    raise RuntimeError(
        f"el agente no terminó en {max_steps} pasos; "
        "revisa el prompt o sube el presupuesto a conciencia"
    )
