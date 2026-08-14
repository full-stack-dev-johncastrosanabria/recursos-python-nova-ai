"""Reto: ramificar por la forma del dato, con `match`.

Llegan eventos como diccionarios y hay que describirlos. Podrías hacerlo con
`if` encadenados comprobando claves, pero `match` compara la forma **y** extrae
los valores en la misma línea.

    describe({"tipo": "pago", "monto": 500_000})   -> "pago grande de 500000"
    describe({"tipo": "pago", "monto": 5_000})     -> "pago de 5000"
    describe({"tipo": "reverso", "ref": "TR-1"})   -> "reverso de TR-1"
    describe({"tipo": "cierre"})                   -> "cierre de día"
    describe({"tipo": "loquesea"})                 -> "evento desconocido"
    describe({})                                   -> "evento desconocido"

Reglas:

- Un pago es **grande** si su monto supera los 100.000. Un `case` puede llevar
  una condición extra con `if`, y el orden importa: el caso más específico va
  primero.
- Un evento al que le falte la clave que su tipo necesita —un pago sin `monto`,
  un reverso sin `ref`— cae en `"evento desconocido"`. No revientes.
- Pon siempre el comodín `case _` al final. Sin él, un evento que no encaje con
  ningún patrón sale de la función sin pasar por ningún `return`, y devuelve
  `None` en silencio.

La forma de un case sobre diccionario es esta:

    match evento:
        case {"tipo": "pago", "monto": monto} if monto > 100_000:
            return f"pago grande de {monto}"

Fíjate en que `monto` queda **ligado** al valor extraído: no hace falta
`evento["monto"]` después.
"""


def describe(event: dict) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
