"""Solución de referencia del ejercicio `dinero`.

`divmod` da cociente y resto de una vez, así que las unidades y los céntimos
salen sin dividir nunca en coma flotante. El signo se trata aparte para que la
coma de los miles caiga donde debe.
"""


def format_cents(cents: int) -> str:
    signo = "-" if cents < 0 else ""
    unidades, centimos = divmod(abs(cents), 100)

    return f"{signo}{unidades:,}.{centimos:02d}"
