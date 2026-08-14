"""Ejercicio: en qué gastar la llamada cara.

Tienes ocho anomalías y presupuesto para investigar tres. Cuáles eliges no es
un detalle: es la tesis del proyecto convertida en función.

Escribe `prioritize`:

    prioritize(
        [
            {"ref": "TR-3", "rule": "monto_alto", "severity": "media"},
            {"ref": "TR-1", "rule": "sin_ref", "severity": "alta"},
            {"ref": "TR-2", "rule": "duplicada", "severity": "alta"},
        ],
        budget=2,
    )
    -> [{"ref": "TR-1", ...}, {"ref": "TR-2", ...}]

Reglas:

- Se ordenan por **severidad**, de más grave a menos, según el orden de
  `SEVERIDADES`. Una severidad que no esté en esa lista se trata como la menos
  grave de todas.
- A igual severidad, por **referencia alfabética**. Sin esa regla, dos
  ejecuciones sobre los mismos datos podrían investigar cosas distintas, y
  entonces no puedes comparar el informe de hoy con el de ayer.
- Se devuelven como mucho `budget` elementos.
- Un presupuesto de 0 devuelve lista vacía: es una situación legítima —hoy no
  hay dinero para investigar— y no un error.
- Un presupuesto negativo sí es `ValueError`.
- No modifiques la lista que recibes ni sus elementos.

Fíjate en lo que **no** hace: no llama a ningún modelo ni decide si una anomalía
es "interesante". Decide dónde gastar, que es una cuestión de política, no de
juicio. Por eso es código y no un prompt.
"""

SEVERIDADES = ("error", "alta", "media", "baja")


def prioritize(anomalies: list[dict], budget: int) -> list[dict]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
