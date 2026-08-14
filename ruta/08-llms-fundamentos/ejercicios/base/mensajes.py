"""Ejercicio: construir la petición recortando el historial.

El modelo no recuerda nada: en cada llamada le mandas la conversación entera.
Como la ventana de contexto tiene un tope y cada token se paga, hay que
recortar el historial cuando crece.

Escribe `build_request`, que devuelve la petición lista para enviar:

    build_request(
        system="Eres un asistente.",
        history=[{"role": "user", "content": "hola"},
                 {"role": "assistant", "content": "¡hola!"}],
        user_message="¿qué tal?",
        max_history_tokens=100,
    )
    -> {
        "system": "Eres un asistente.",
        "messages": [
            {"role": "user", "content": "hola"},
            {"role": "assistant", "content": "¡hola!"},
            {"role": "user", "content": "¿qué tal?"},
        ],
    }

Reglas:

- El mensaje nuevo del usuario se añade **al final** y **nunca se recorta**,
  aunque él solo pase del presupuesto: es la pregunta que hay que responder.
- El presupuesto `max_history_tokens` se aplica solo al historial previo. Si
  se pasa, se van quitando mensajes **por el principio** (los más viejos) hasta
  que quepa.
- El `system` se devuelve tal cual y no cuenta para el presupuesto. Nunca se
  recorta: son las reglas, y sin ellas el modelo deja de comportarse.
- No modifiques la lista `history` que te pasan.

Usa `estimate_tokens` para contar. Es una aproximación de servilleta, que es
justo lo que se usa en la práctica para presupuestar.
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
    raise NotImplementedError("Borra esta línea y escribe tu solución")
