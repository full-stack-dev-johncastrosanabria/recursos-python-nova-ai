"""Cómo un objeto propio se integra con la sintaxis del lenguaje.

`Temperatures` no hereda de nada. Solo habla protocolos, y con eso ya funciona
con `len`, indexación, `for`, `in`, `sum`, `max` y `sorted`.

Córrelo con:
    uv run python ruta/00-como-piensa-python/ejemplos/protocolos.py
"""


class Temperatures:
    """Una serie de temperaturas que habla el protocolo de secuencia."""

    def __init__(self, readings: list[float]) -> None:
        self._readings = readings

    def __len__(self) -> int:
        return len(self._readings)

    def __getitem__(self, position):
        return self._readings[position]

    def __repr__(self) -> str:
        return f"Temperatures({self._readings!r})"


series = Temperatures([12.5, 18.0, 7.3, 22.1, 15.8])

# Ninguna de estas líneas necesitó un método propio: son protocolos.
print(f"repr:      {series}")
print(f"len:       {len(series)}")
print(f"primera:   {series[0]}")
print(f"última:    {series[-1]}")
print(f"slice:     {series[:2]}")
print(f"in:        {22.1 in series}")
print(f"suma:      {sum(series)}")
print(f"máxima:    {max(series)}")
print(f"ordenadas: {sorted(series)}")

print("\nY el for funciona sin haber definido __iter__:")
for reading in series:
    marca = "█" * int(reading)
    print(f"  {reading:>5.1f} °C {marca}")

# La pregunta útil ante cualquier objeto: ¿qué protocolos habla?
protocolos = [name for name in dir(series) if name.startswith("__")]
print(f"\nMétodos especiales definidos o heredados: {len(protocolos)}")
print("Los propios:", [n for n in vars(Temperatures) if n.startswith("__")])
