"""Solución de referencia del reto `tabla`.

Los anchos viven en constantes y no repetidos en cada f-string: cambiar una
columna es cambiar un número, y la cabecera y la línea de guiones se ajustan
solas.
"""

ANCHO_PRODUCTO = 12
ANCHO_CANTIDAD = 5
ANCHO_IMPORTE = 14


def _formatear_importe(cents: int) -> str:
    signo = "-" if cents < 0 else ""
    unidades, centimos = divmod(abs(cents), 100)
    return f"{signo}{unidades:,}.{centimos:02d}"


def render_row(product: str, quantity: int, cents: int) -> str:
    importe = _formatear_importe(cents)
    return (
        f"{product:<{ANCHO_PRODUCTO}}"
        f"{quantity:>{ANCHO_CANTIDAD}}"
        f"{importe:>{ANCHO_IMPORTE}}"
    )


def render_table(rows: list[tuple[str, int, int]]) -> str:
    cabecera = (
        f"{'producto':<{ANCHO_PRODUCTO}}"
        f"{'cant':>{ANCHO_CANTIDAD}}"
        f"{'importe':>{ANCHO_IMPORTE}}"
    )
    separador = "-" * (ANCHO_PRODUCTO + ANCHO_CANTIDAD + ANCHO_IMPORTE)

    return "\n".join([cabecera, separador, *(render_row(*fila) for fila in rows)])
