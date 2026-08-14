"""Solución de referencia del ejercicio `entorno`."""


def parse_env(text: str) -> dict[str, str]:
    values: dict[str, str] = {}

    for number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ValueError(f"línea {number}: se esperaba CLAVE=valor, hay {line!r}")

        key, _, value = line.partition("=")
        value = value.strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]

        values[key.strip()] = value

    return values
