"""Solución de referencia del ejercicio `idiomatico`."""


def active_names(users: list[dict]) -> list[str]:
    return [user["name"] for user in users if user["active"]]
