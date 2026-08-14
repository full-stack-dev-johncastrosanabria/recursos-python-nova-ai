# Módulo 01 · Fundamentos

> **Prerrequisitos:** ninguno; el módulo 00 ayuda pero no hace falta<br>
> **Tiempo estimado:** 120 min<br>
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

## Caso real

Un script leía temperaturas de unos sensores y calculaba la media diaria. Un
día, uno de los sensores dejó de reportar y el archivo llegó vacío.

La primera versión hacía esto:

```python
def average(numbers):
    if not numbers:
        return 0        # ← parece prudente
    return sum(numbers) / len(numbers)
```

Devolver `0` para una lista vacía parece defensivo, y es justo lo contrario. El
panel mostró **0 °C** para ese sensor, que es una temperatura perfectamente
creíble en invierno. Nadie se dio cuenta en tres semanas, y durante tres
semanas la media general estuvo mal.

La versión correcta es la que ya has visto:

```python
def average(numbers):
    if not numbers:
        raise ValueError("no se puede promediar una lista vacía")
    return sum(numbers) / len(numbers)
```

Con esa, el fallo aparece el primer día, en el sensor concreto, con un mensaje
que dice qué pasó. La diferencia entre las dos versiones son dos líneas; la
diferencia en consecuencias fue de tres semanas de datos.

Esa es la idea que vas a ver repetida en toda la ruta: **un valor por defecto
que oculta un fallo es peor que un error**. Tu ejercicio `estadisticas` te pide
exactamente esto.

## Ejercicios

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

## Resumen

- Python deduce el tipo, pero anotarlo hace el código más claro para quien lo
  lea después — y ese alguien sueles ser tú.
- Los bloques se marcan con indentación: cuatro espacios, siempre.
- Para recorrer una colección, `for`. Si además necesitas la posición,
  `enumerate`, nunca un contador a mano.
- Una función agrupa código que hace una cosa y le pone nombre.
- Las anotaciones (`list[float]`, `-> float`) no las comprueba el intérprete,
  pero documentan la intención y tu editor las aprovecha.
- Cuando una función recibe algo con lo que no puede trabajar, lanza una
  excepción. Un `0` o un `None` de consolación convierten un fallo en datos
  malos que viajan lejos.

## Preguntas de repaso

1. ¿Qué diferencia hay entre `"3"` y `3`, y qué pasa si intentas sumarlos?
2. Necesitas el índice y el valor de cada elemento de una lista. ¿Cómo lo
   escribes?
3. ¿Por qué `average([])` es mejor que lance un error a que devuelva `0`?
4. Si el intérprete no comprueba las anotaciones de tipo, ¿para qué las
   escribes?
5. ¿Qué hace `f"{valor:.2f}"` y cuándo lo usarías?

## Recursos

- [El tutorial oficial de Python](https://docs.python.org/es/3/tutorial/) —
  `doc-oficial` · `es` · `principiante`. En español y escrito por quienes hacen
  el lenguaje. Los capítulos 3 al 5 cubren casi todo este módulo.
- [PEP 8 — Guía de estilo](https://peps.python.org/pep-0008/) —
  `doc-oficial` · `en` · `principiante`. Ruff la aplica por ti, pero conviene
  saber de dónde salen las reglas.
- [f-strings en profundidad](https://realpython.com/python-f-strings/) —
  `artículo` · `en` · `principiante`. Alineación, decimales y `!r`.

Más enlaces por tema en [`recursos/enlaces/`](../../recursos/enlaces/README.md).

## Siguiente

Módulo 02 · Estructuras de datos.
