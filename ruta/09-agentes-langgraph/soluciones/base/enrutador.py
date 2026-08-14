"""Solución de referencia del ejercicio `enrutador`.

Cuatro condiciones en orden, sin ninguna llamada a un modelo. Corre en
microsegundos, cuesta cero y tiene tests: tres cosas que un enrutador con LLM
no puede ofrecer.
"""

import re

URGENTES = ("urgente", "bloqueado", "caído", "no funciona")
COMERCIALES = ("presupuesto", "demo", "precio", "contratar")
REFERENCIA = re.compile(r"TR-\d+")


def route(event: dict) -> str:
    asunto = event.get("asunto") or ""
    cuerpo = event.get("cuerpo") or ""

    if any(palabra in asunto.lower() for palabra in URGENTES):
        return "incidencia"

    if REFERENCIA.search(asunto) or REFERENCIA.search(cuerpo):
        return "conciliacion"

    if any(palabra in asunto.lower() for palabra in COMERCIALES):
        return "ventas"

    return "revision_humana"
