"""Solución de referencia del ejercicio `registro`."""

NIVELES = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}


def format_log(
    level: str, message: str, min_level: str = "INFO", **fields
) -> str | None:
    for nombre in (level, min_level):
        if nombre not in NIVELES:
            raise ValueError(
                f"nivel desconocido {nombre!r}; los válidos son {', '.join(NIVELES)}"
            )

    if NIVELES[level] < NIVELES[min_level]:
        return None

    linea = f"{level:<8}{message}"

    if fields:
        extras = " ".join(f"{clave}={fields[clave]}" for clave in sorted(fields))
        linea = f"{linea} {extras}"

    return linea
