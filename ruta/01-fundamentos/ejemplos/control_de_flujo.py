"""Condicionales, bucles y funciones.

Córrelo con:
    uv run python ruta/01-fundamentos/ejemplos/control_de_flujo.py
"""


def classify(temperature: float) -> str:
    """Clasifica una temperatura en Celsius."""
    if temperature < 0:
        return "helada"
    if temperature < 15:
        return "fría"
    if temperature < 28:
        return "templada"
    return "calurosa"


def average(numbers: list[float]) -> float:
    """Calcula la media. Lanza ValueError si la lista está vacía."""
    if not numbers:
        raise ValueError("no se puede promediar una lista vacía")
    return sum(numbers) / len(numbers)


readings = [-5.0, 12.0, 22.5, 31.0]

for reading in readings:
    print(f"{reading:>6.1f} °C -> {classify(reading)}")

print(f"Media: {average(readings):.2f} °C")

# Un bucle con índice, cuando de verdad necesitas el número de posición.
for position, reading in enumerate(readings, start=1):
    print(f"Lectura {position}: {reading} °C")
