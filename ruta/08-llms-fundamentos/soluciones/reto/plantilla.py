"""Solución de referencia del reto `plantilla`.

El escapado sustituye `&` primero: al revés, las entidades recién creadas
volverían a escaparse y el texto acabaría con `&amp;lt;`.
"""

import re

HUECO = re.compile(r"\{(\w+)\}")


def _escapar(valor: str) -> str:
    return valor.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_prompt(template: str, **values: str) -> str:
    pedidos = set(HUECO.findall(template))
    dados = set(values)

    if faltan := pedidos - dados:
        raise ValueError(f"faltan variables: {', '.join(sorted(faltan))}")

    if sobran := dados - pedidos:
        raise ValueError(f"la plantilla no usa: {', '.join(sorted(sobran))}")

    return HUECO.sub(lambda m: _escapar(str(values[m.group(1)])), template)
