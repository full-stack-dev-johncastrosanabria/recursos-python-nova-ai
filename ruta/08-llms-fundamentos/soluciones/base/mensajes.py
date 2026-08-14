"""Solución de referencia del ejercicio `mensajes`.

Se recorta por el principio porque lo viejo es lo que menos falta hace, y se
copia la lista para no dejarle al que llama un historial mutilado.
"""


def estimate_tokens(text: str) -> int:
    """Aproximación habitual: unos cuatro caracteres por token."""
    return max(1, len(text) // 4)


def build_request(
    system: str,
    history: list[dict],
    user_message: str,
    max_history_tokens: int = 100,
) -> dict:
    kept = list(history)
    used = sum(estimate_tokens(message["content"]) for message in kept)

    while kept and used > max_history_tokens:
        removed = kept.pop(0)
        used -= estimate_tokens(removed["content"])

    return {
        "system": system,
        "messages": [*kept, {"role": "user", "content": user_message}],
    }
