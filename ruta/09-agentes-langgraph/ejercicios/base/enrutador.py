"""Ejercicio: enrutar por reglas antes de gastar una llamada al modelo.

El patrón de enrutamiento decide una vez a dónde va cada entrada. Esa decisión
la puede tomar un modelo… o unas reglas. Y **la mitad de los enrutamientos que
se implementan con un LLM son cuatro condiciones**: más rápidos, gratis,
deterministas y con tests.

Escribe `route`, que clasifica un evento entrante:

    route({"asunto": "URGENTE: pago rechazado", "cuerpo": "..."})
    -> "incidencia"

Las reglas, **en este orden de prioridad**:

1. Si el asunto contiene alguna palabra de `URGENTES` (sin distinguir
   mayúsculas), va a `"incidencia"`.
2. Si el asunto o el cuerpo contienen una referencia con el formato `TR-` más
   dígitos, va a `"conciliacion"`.
3. Si el asunto contiene alguna palabra de `COMERCIALES`, va a `"ventas"`.
4. Si no encaja en nada, va a `"revision_humana"`.

Que haya un destino explícito para "no lo sé" es la misma lección del prompt de
clasificación del módulo 08: sin una salida para lo desconocido, el sistema
inventa una.

Reglas de implementación:

- Un evento sin `asunto` o sin `cuerpo` se trata como si esos campos fueran
  cadenas vacías. Un correo sin asunto es raro, no es un error.
- El orden importa: un asunto que diga "URGENTE: TR-0042" va a `"incidencia"`,
  no a `"conciliacion"`, porque la regla 1 va antes.
- Devuelve siempre uno de los cuatro destinos. Nunca `None`.

Para la referencia, una expresión regular sencilla: `TR-` seguido de uno o más
dígitos.
"""

import re

URGENTES = ("urgente", "bloqueado", "caído", "no funciona")
COMERCIALES = ("presupuesto", "demo", "precio", "contratar")
REFERENCIA = re.compile(r"TR-\d+")


def route(event: dict) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
