# Módulo 01 · Fundamentos

> **Prerrequisitos:** ninguno
> **Tiempo estimado:** 120 min
> **Si ya dominas esto:** salta al módulo 02

## Qué vas a poder hacer al terminar

- Declarar variables y reconocer los tipos básicos de Python
- Escribir condicionales y bucles
- Definir funciones con parámetros y valor de retorno
- Ejecutar tests y leer por qué fallan

## 1. Variables y tipos

Python no necesita que declares el tipo de una variable, pero puedes anotarlo.
Hazlo: dentro de seis meses, el que lea el código serás tú.

```python
name: str = "Ana"
age: int = 30
```

Los cuatro tipos básicos son `str` (texto), `int` (entero), `float` (decimal) y
`bool` (verdadero o falso). Para agrupar valores tienes `list` (en orden) y
`dict` (por clave).

Abre y ejecuta `ejemplos/variables_y_tipos.py`:

```bash
uv run python ruta/01-fundamentos/ejemplos/variables_y_tipos.py
```

## 2. Condicionales y bucles

Python usa la indentación para marcar bloques: no hay llaves. Cuatro espacios,
siempre.

```python
if temperature < 0:
    print("helada")
elif temperature < 15:
    print("fría")
else:
    print("templada")
```

Para recorrer una colección, `for`:

```python
for reading in readings:
    print(reading)
```

Si necesitas la posición además del valor, `enumerate` — no un contador manual.

## 3. Funciones

Una función agrupa código que hace una cosa y le pone nombre:

```python
def average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("no se puede promediar una lista vacía")
    return sum(numbers) / len(numbers)
```

Las anotaciones (`list[float]`, `-> float`) no las verifica Python al ejecutar,
pero documentan la intención y tu editor las usa para avisarte de errores.

Cuando una función recibe algo con lo que no puede trabajar, lanza una
excepción en vez de devolver un valor raro como `None` o `0`. Quien la llame
se enterará del problema en el momento, no tres funciones más abajo.

Ejecuta `ejemplos/control_de_flujo.py` y léelo entero.

## 4. Ejercicios

Los ejercicios están en `ejercicios/`. Cada archivo tiene una función sin
terminar. Tu trabajo es completarla.

Corre los tests:

```bash
uv run pytest ruta/01-fundamentos
```

Los verás en rojo: es lo esperado. Los stubs lanzan `NotImplementedError` a
propósito. Ve resolviendo y vuelve a correrlos hasta que estén verdes.

- **`ejercicios/base/saludo.py`** — devolver un saludo, sin espacios sobrantes.
- **`ejercicios/base/temperatura.py`** — convertir Celsius a Fahrenheit.
- **`ejercicios/reto/estadisticas.py`** — resumir una lista de números. Este
  requiere manejar el caso de la lista vacía.

Para correr un solo ejercicio:

```bash
uv run pytest ruta/01-fundamentos/tests/base/test_saludo.py -v
```

Si te atascas, en `soluciones/` está la versión de referencia. Míralas después
de intentarlo, no antes: leer una solución da la sensación de haber aprendido
sin haber aprendido.

## Siguiente

Módulo 02 · Estructuras de datos.
