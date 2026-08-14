"""Ejercicio: el motor de reglas.

Escribe `detect_anomalies`, que aplica un conjunto de reglas a cada
transferencia y devuelve los hallazgos.

Cada regla es un diccionario:

    {
        "name": "monto_alto",
        "severity": "alta",
        "check": lambda t: t["cents"] > 1_000_000,
    }

Y cada hallazgo:

    {"ref": "TR-1", "rule": "monto_alto", "severity": "alta"}

Ejemplo:

    detect_anomalies(
        [{"ref": "TR-1", "cents": 5_000_000}, {"ref": "TR-2", "cents": 100}],
        [regla_monto_alto],
    )
    -> [{"ref": "TR-1", "rule": "monto_alto", "severity": "alta"}]

Reglas del motor:

- Se recorren las transferencias en orden y, dentro de cada una, las reglas en
  orden. El resultado es determinista.
- Solo se registra el hallazgo cuando `check` devuelve algo verdadero.
- **Una regla con un bug no puede tumbar el proceso.** Si `check` lanza una
  excepción, se registra un hallazgo con `severity="error"` y se sigue con las
  demás reglas y transferencias. A las tres de la mañana, un informe con una
  regla rota marcada es infinitamente más útil que ningún informe.
- La transferencia debe seguir intacta: no le añadas nada.
"""

from collections.abc import Callable, Iterable, Mapping  # noqa: F401


def detect_anomalies(
    transfers: Iterable[Mapping], rules: Iterable[Mapping]
) -> list[dict]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
