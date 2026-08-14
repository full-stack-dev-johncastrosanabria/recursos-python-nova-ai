"""Ejercicio: encapsular con `@property`.

Implementa `Thermostat`, un termostato que guarda su temperatura objetivo.

    termo = Thermostat(21)
    termo.celsius        -> 21
    termo.fahrenheit     -> 69.8

    termo.celsius = 25   -> pasa por el setter y valida
    termo.fahrenheit = 104
    termo.celsius        -> 40.0    ← escribir en Fahrenheit cambia el Celsius

Dos propiedades, cada una con su lección:

**`celsius`** es la de verdad: guarda el valor en `self._celsius` y **valida en
el setter**. El rango admitido es de -90 a 60 (los extremos registrados en la
Tierra, con margen). Fuera de ahí, `ValueError` mencionando el valor recibido.

**`fahrenheit`** es **derivada**: no guarda nada. Su getter convierte desde
Celsius y su setter convierte hacia Celsius **reutilizando el setter de
`celsius`**, de forma que la validación se aplique también por esta vía. Un
`termo.fahrenheit = 500` tiene que fallar, porque son 260 °C.

    F = C * 9/5 + 32
    C = (F - 32) * 5/9

Lo que este ejercicio enseña: quien usa la clase escribe `termo.celsius = 25`
igual que si fuera un atributo normal. La propiedad convierte un atributo en un
par de métodos **sin cambiar la sintaxis de uso**, y por eso en Python se
empieza con atributos públicos y se convierten en propiedades el día que hace
falta.
"""


class Thermostat:
    def __init__(self, celsius: float) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
