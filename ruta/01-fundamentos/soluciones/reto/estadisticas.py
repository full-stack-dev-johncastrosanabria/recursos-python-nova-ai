"""Solución de referencia del reto `estadisticas`.

`sorted` devuelve una lista nueva, así que la del que llama queda intacta. El
`divmod` sobre la longitud separa de una vez el índice central y si el número
de elementos era par o impar.
"""


def summarize(numbers: list[float]) -> dict[str, float]:
    if not numbers:
        raise ValueError("no se puede resumir una lista vacía")

    ordenados = sorted(numbers)
    mitad, resto = divmod(len(ordenados), 2)

    if resto:
        mediana = ordenados[mitad]
    else:
        mediana = (ordenados[mitad - 1] + ordenados[mitad]) / 2

    return {
        "min": ordenados[0],
        "max": ordenados[-1],
        "mean": sum(ordenados) / len(ordenados),
        "median": mediana,
    }
