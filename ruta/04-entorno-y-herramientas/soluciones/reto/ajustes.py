"""Solución de referencia del reto `ajustes`.

Reunir todas las claves que faltan antes de fallar convierte tres despliegues
fallidos en uno. Es el mismo criterio que aplica Pydantic cuando informa de
todos los errores de un payload a la vez.
"""

from collections.abc import Mapping
from dataclasses import dataclass

REQUIRED = ("HOST", "PORT")
TRUTHY = frozenset({"1", "true", "yes", "on"})


def _convert(key: str, value: str, converter):
    try:
        return converter(value)
    except ValueError as error:
        raise ValueError(
            f"{key} debería ser {converter.__name__}, pero trae {value!r}"
        ) from error


@dataclass(frozen=True, slots=True)
class Settings:
    host: str
    port: int
    debug: bool = False
    timeout: float = 30.0

    @classmethod
    def from_mapping(cls, raw: Mapping[str, str]) -> "Settings":
        missing = [key for key in REQUIRED if key not in raw]
        if missing:
            raise ValueError(f"faltan variables obligatorias: {', '.join(missing)}")

        return cls(
            host=raw["HOST"],
            port=_convert("PORT", raw["PORT"], int),
            debug=raw.get("DEBUG", "").strip().lower() in TRUTHY,
            timeout=_convert("TIMEOUT", raw.get("TIMEOUT", "30.0"), float),
        )
