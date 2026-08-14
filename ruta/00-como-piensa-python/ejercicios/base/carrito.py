"""Ejercicio: la trampa del argumento mutable por defecto.

Esta función tiene un bug clásico. El valor por defecto se crea UNA sola vez,
cuando Python define la función, así que todas las llamadas que no pasen
`basket` comparten la misma lista:

    def add_item(item, basket=[]):
        basket.append(item)
        return basket

    add_item("pan")     -> ["pan"]
    add_item("leche")   -> ["pan", "leche"]   ← el carrito de la llamada anterior

Arréglalo. Cada llamada sin `basket` debe empezar con un carrito vacío, y una
llamada que sí lo reciba debe añadir sobre ese mismo carrito y devolverlo.

    add_item("pan")                    -> ["pan"]
    add_item("leche")                  -> ["leche"]
    add_item("sal", ["pan", "leche"])  -> ["pan", "leche", "sal"]
"""


def add_item(item: str, basket: list[str] | None = None) -> list[str]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
