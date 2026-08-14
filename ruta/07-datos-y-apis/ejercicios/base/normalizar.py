"""Ejercicio: aplanar un payload de API y distinguir lo que falta.

Escribe `normalize_transfer`, que convierte el payload anidado que devuelve un
proveedor en el registro plano que usa tu sistema.

Entrada:

    {
        "id": "TR-1",
        "amount": {"cents": 150000, "currency": "CRC"},
        "parties": {
            "from": {"account": "CR01-0001"},
            "to": {"account": "CR01-0002"},
        },
        "reference": "factura 42",
    }

Salida:

    {
        "id": "TR-1",
        "amount_cents": 150000,
        "currency": "CRC",
        "origin": "CR01-0001",
        "destination": "CR01-0002",
        "reference": "factura 42",
    }

Reglas, y aquí está lo importante del ejercicio:

- **Lo obligatorio que falta es un error**, no un `None`. Si no está `id`,
  `amount.cents`, `parties.from.account` o `parties.to.account`, lanza
  `ValueError` diciendo qué ruta faltó, por ejemplo `parties.from.account`.
  Tratar la ausencia de un campo obligatorio como un caso normal es cómo se
  pierden transferencias en silencio.
- **`currency` es opcional** y su valor por defecto es `"CRC"`.
- **`reference` es opcional** y su valor por defecto es `None`. Aquí sí, porque
  de verdad puede no haber referencia.

La diferencia entre las dos últimas reglas y la primera es todo el ejercicio.
"""


def normalize_transfer(payload: dict) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
