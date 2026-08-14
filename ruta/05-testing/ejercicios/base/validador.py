"""Ejercicio: validar con errores que se puedan distinguir.

Escribe `validate_account`, que comprueba y normaliza un número de cuenta.

El formato válido es: `CR`, dos dígitos, un guion y cuatro dígitos.

    validate_account("CR01-0002")     -> "CR01-0002"
    validate_account("  cr01-0002 ")  -> "CR01-0002"   (limpia y pone en mayúsculas)

Los errores ya están definidos abajo y forman una jerarquía:

    AccountError            <- lo que captura quien solo quiere saber "no vale"
    ├── EmptyAccount        <- vino vacío o solo espacios
    └── InvalidFormat       <- vino algo, pero no con la forma correcta

Esa jerarquía no es decoración: permite que quien te llame elija cuánta
precisión quiere. Un formulario querrá distinguir "no rellenaste el campo" de
"lo rellenaste mal"; un log agregado querrá capturar `AccountError` y ya.

Los mensajes de error deben incluir el valor que se recibió. Un error que dice
"formato inválido" y no dice de qué obliga a reproducir el problema para
entenderlo.

Mira sus tests: comprueban la jerarquía además del comportamiento.
"""

import re

PATTERN = re.compile(r"^CR\d{2}-\d{4}$")


class AccountError(Exception):
    """La cuenta no es válida."""


class EmptyAccount(AccountError):
    """No se recibió ninguna cuenta."""


class InvalidFormat(AccountError):
    """La cuenta no tiene el formato esperado."""


def validate_account(value: str) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
