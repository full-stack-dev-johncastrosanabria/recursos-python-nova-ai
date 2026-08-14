"""Ejercicio: formatear dinero sin tocar un solo float.

El importe llega en céntimos, como entero, que es la forma correcta de mover
dinero por un sistema. Tu trabajo es presentarlo:

    format_cents(150_000)   -> "1,500.00"
    format_cents(99)        -> "0.99"
    format_cents(0)         -> "0.00"
    format_cents(-50_000)   -> "-500.00"
    format_cents(1_234_567) -> "12,345.67"

Reglas:

- Siempre dos decimales.
- Separador de miles con coma, solo en la parte entera.
- El signo menos va delante de todo: `-500.00`, no `500.00-` ni `-,500.00`.
- **Aritmética de enteros únicamente.** Si en algún momento escribes
  `cents / 100`, ya introdujiste un float y con él su error de representación.
  La operación que buscas es `divmod`, que te da cociente y resto de una vez.

Pista para el separador: las f-strings saben ponerlo. `f"{12345:,}"` da
`'12,345'`.
"""


def format_cents(cents: int) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
