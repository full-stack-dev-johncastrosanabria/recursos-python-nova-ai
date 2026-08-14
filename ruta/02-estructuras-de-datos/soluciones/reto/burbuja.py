"""Solución de referencia del reto `burbuja`.

El `while` con la bandera `hubo_cambios` es lo que hace que una lista ya
ordenada cueste una sola pasada: sin ella, el algoritmo daría siempre n
pasadas aunque no hubiera nada que mover.
"""


def bubble_sort(numbers: list[float]) -> tuple[list[float], int]:
    valores = list(numbers)
    intercambios = 0
    hubo_cambios = True

    while hubo_cambios:
        hubo_cambios = False
        for i in range(len(valores) - 1):
            if valores[i] > valores[i + 1]:
                valores[i], valores[i + 1] = valores[i + 1], valores[i]
                intercambios += 1
                hubo_cambios = True

    return valores, intercambios
