"""Solución de referencia del ejercicio `propiedad`.

El setter de `fahrenheit` no valida por su cuenta: convierte y asigna a
`self.celsius`, que es quien tiene la regla. Una sola fuente de verdad para la
validación, aunque haya dos puertas de entrada.
"""

MIN_CELSIUS = -90
MAX_CELSIUS = 60


class Thermostat:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius  # pasa por el setter: valida también al construir

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if not MIN_CELSIUS <= value <= MAX_CELSIUS:
            raise ValueError(
                f"la temperatura debe estar entre {MIN_CELSIUS} y {MAX_CELSIUS} "
                f"grados, llegó {value}"
            )
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9

    def __repr__(self) -> str:
        return f"Thermostat({self._celsius})"
