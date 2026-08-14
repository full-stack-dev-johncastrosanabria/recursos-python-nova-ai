"""Reto: comprobar con código que un modelo no inventó cifras.

Es la pieza que arregló el caso real de la guía. Un agente redactor recibe unas
métricas ya calculadas y escribe el informe; el problema es que a veces se
inventa un número. Poner otro modelo a revisarlo no funciona: hereda el mismo
defecto. Lo que sí funciona es comprobarlo.

Escribe `unsupported_numbers`, que devuelve los números del texto que **no**
aparecen entre los datos de origen:

    unsupported_numbers(
        "El total fue 1500 en 3 operaciones",
        {"total": 1500, "operaciones": 3},
    )
    -> []          ← todo respaldado

    unsupported_numbers(
        "El total fue 1500 en 4 operaciones",
        {"total": 1500, "operaciones": 3},
    )
    -> ["4"]       ← ese 4 no está en los datos

Reglas:

- Se extraen del texto todas las secuencias de dígitos, admitiendo separadores
  de miles y decimales: `1500`, `1,500`, `1500.50`.
- Un número está respaldado si **su forma normalizada** coincide con la de
  algún valor de los datos. Normalizar significa quitar las comas y los ceros
  decimales que no aportan: `"1,500"`, `"1500"` y `"1500.00"` son el mismo
  número, y el informe debe poder escribirlo como quiera.
- Se devuelven **tal y como aparecen en el texto**, en orden de aparición y sin
  repetir. Quien lea el aviso tiene que poder buscarlos en el informe.
- Los valores de los datos que no son números se ignoran: un nombre de cliente
  no respalda cifras.
- Un texto sin números devuelve lista vacía.

Lo que hace valiosa a esta función es lo que **no** hace: no juzga si el
informe está bien redactado ni si la conclusión es razonable. Convierte una
pregunta de juicio —"¿se lo inventó?"— en una comprobación mecánica. Eso es
todo el módulo en cinco líneas.
"""

import re  # noqa: F401

NUMERO = re.compile(r"\d[\d,]*(?:\.\d+)?")


def unsupported_numbers(text: str, data: dict) -> list[str]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
