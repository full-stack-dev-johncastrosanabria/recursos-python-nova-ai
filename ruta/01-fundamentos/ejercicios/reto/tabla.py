'''Reto: alinear una tabla con especificadores de formato.

Todo esto se hace con f-strings, sin una sola línea de rellenar con espacios a
mano.

Dos funciones:

    render_row("café", 3, 150_000)
    -> "café            3      1,500.00"

    render_table([("café", 3, 150_000), ("azúcar", 12, 99)])
    ->
    """producto     cant       importe
    -------------------------------
    café            3      1,500.00
    azúcar         12          0.99"""

Anchos de columna, que ya están definidos abajo como constantes:

- **producto**: 12 caracteres, alineado a la **izquierda**
- **cantidad**: 5 caracteres, alineado a la **derecha**
- **importe**: 14 caracteres, alineado a la **derecha**, formateado como dinero
  (separador de miles y dos decimales) a partir de los céntimos

La tabla lleva encima una fila de títulos —`producto`, `cant`, `importe`, con
los mismos anchos y alineaciones— y debajo una línea de guiones tan larga como
la suma de los anchos. Las filas se unen con saltos de línea y **no hay salto
final**.

Un producto más largo que su columna no se recorta: se sale, y la fila queda
desalineada. Eso es lo que hace `:<12`, y es la decisión correcta — mutilar un
nombre para que quepa es peor que una fila torcida.

Recuerda del módulo: `f"{texto:<12}"` alinea a la izquierda, `f"{n:>5}"` a la
derecha, `f"{n:,}"` pone el separador de miles. Y el importe se construye con
`divmod`, sin dividir en coma flotante.
'''

ANCHO_PRODUCTO = 12
ANCHO_CANTIDAD = 5
ANCHO_IMPORTE = 14


def render_row(product: str, quantity: int, cents: int) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def render_table(rows: list[tuple[str, int, int]]) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
