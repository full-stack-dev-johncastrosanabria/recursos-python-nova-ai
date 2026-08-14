"""Solución de referencia del ejercicio `validador`."""

import re

PATTERN = re.compile(r"^CR\d{2}-\d{4}$")


class AccountError(Exception):
    """La cuenta no es válida."""


class EmptyAccount(AccountError):
    """No se recibió ninguna cuenta."""


class InvalidFormat(AccountError):
    """La cuenta no tiene el formato esperado."""


def validate_account(value: str) -> str:
    normalized = value.strip().upper()

    if not normalized:
        raise EmptyAccount(f"no se recibió ninguna cuenta (llegó {value!r})")

    if not PATTERN.match(normalized):
        raise InvalidFormat(
            f"{value!r} no tiene el formato CRnn-nnnn (por ejemplo, CR01-0002)"
        )

    return normalized
