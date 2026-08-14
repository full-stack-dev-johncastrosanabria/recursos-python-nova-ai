# Módulo 01 · Fundamentos

> **Prerrequisitos:** ninguno; el módulo 00 ayuda pero no hace falta<br>
> **Tiempo estimado:** 180 min<br>
> **Si ya dominas esto:** salta al módulo 02

Fundamentos no significa superficial. Este módulo cubre lo que se usa todos los
días —variables, números, texto, condiciones, bucles y funciones— pero contando
lo que casi nunca se cuenta: **qué contrato tiene cada cosa y dónde se rompe**.

La mitad de los bugs caros de un sistema nacen aquí: un importe en `float`, un
descuento de cero tratado como "no hay descuento", una función que devuelve `0`
cuando debería fallar. Nada de eso es sintaxis avanzada. Es esto, mal entendido.

## Qué vas a poder hacer al terminar

- Declarar variables y reconocer los tipos básicos de Python
- Escribir condicionales y bucles
- Definir funciones con parámetros y valor de retorno
- Elegir el tipo numérico correcto según el contrato de error de tu dominio
- Distinguir "está vacío" de "no se proporcionó"
- Ejecutar tests y leer por qué fallan

## 1. Asignar: qué ocurre exactamente

```python
name: str = "Ana"
age: int = 30
```

Python deduce el tipo, pero anotarlo hace el código más claro. Hazlo: dentro de
seis meses, quien lo lea serás tú.

Lo que sucede al asignar es más simple de lo que parece y explica muchas cosas
después: Python crea el objeto y **ata un nombre a él**. La variable no es una
caja que contiene el valor; es una etiqueta pegada al objeto.

```python
a = [1, 2, 3]
b = a          # otra etiqueta sobre EL MISMO objeto
b.append(4)
print(a)       # [1, 2, 3, 4]
```

Puedes comprobarlo tú mismo, sin creerte nada:

```python
a = [1, 2, 3]
b = a
c = a[:]       # esto sí construye un objeto nuevo

a is b         # True  — mismo objeto
a is c         # False — objetos distintos…
a == c         # True  — …con el mismo contenido
```

**`is` compara identidad; `==` compara valor.** Confundirlos es una fuente
constante de bugs raros. La regla práctica: `is` solo se usa contra `None`,
`True` y `False`. Para todo lo demás, `==`.

De aquí sale la distinción que organiza el lenguaje entero: hay objetos
**mutables** (lista, dict, set) y objetos **inmutables** (int, float, str,
tuple, frozenset). Con un inmutable, "modificar" es en realidad crear otro:

```python
texto = "hola"
texto.upper()    # 'HOLA' — devuelve uno nuevo
texto            # 'hola' — el original no cambió
```

Por eso los métodos de `str` **devuelven** en vez de modificar, y por eso
olvidar el `texto = texto.strip()` es un clásico.

## 2. Números: cuatro tipos y un contrato de error

### `int`: precisión arbitraria

```python
2 ** 1000        # funciona: 302 dígitos, sin desbordamiento
```

En la mayoría de los lenguajes un entero tiene 64 bits y desborda en silencio.
En Python crece hasta donde llegue la memoria. Es una decisión de diseño:
prefiere la respuesta correcta y lenta a la rápida y equivocada.

### `float`: rápido, y con letra pequeña

```python
0.1 + 0.2        # 0.30000000000000004
0.1 + 0.2 == 0.3 # False
```

Esto no es un bug de Python: es el estándar IEEE 754, el mismo en C, Java y
JavaScript. Un `float` es binario, y 0.1 en binario es periódico igual que 1/3
en decimal. Nunca cabe exacto.

Tres reglas que hay que interiorizar:

```python
import math

math.isclose(0.1 + 0.2, 0.3)     # True — así se comparan floats

n = float("nan")
n == n                            # False — NaN no es igual ni a sí mismo
math.isnan(n)                     # True — la única comprobación correcta

sum([0.1] * 1_000_000)            # 100000.00000133288 — error acumulado
math.fsum([0.1] * 1_000_000)      # 100000.0 — suma compensada
```

### El dinero no va en `float`

```python
from decimal import Decimal, ROUND_HALF_UP

Decimal("0.1") + Decimal("0.2")   # Decimal('0.3') — exacto
Decimal(0.1)                      # ← MAL: importa el error del float

precio = Decimal("13990.00")
iva = (precio * Decimal("0.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
total = precio + iva              # auditable al céntimo
```

Hay **dos formas válidas** de manejar dinero y una prohibida:

- **Válida A:** `Decimal` en todo el dominio, serializado como texto en JSON y
  como `NUMERIC` en SQL.
- **Válida B:** enteros de la unidad mínima —céntimos— y la conversión a
  unidades solo en la capa de presentación. Es lo que hace Stripe: `1099`
  significa 10,99.
- **Prohibida:** `float` en cualquier punto del recorrido del dinero, incluida
  la columna de la base de datos.

Este repositorio usa la B en todos sus ejercicios. Verás `amount_cents` una y
otra vez, y ahora sabes por qué.

### La tabla de decisión

| Tipo | Exactitud | Velocidad | Cuándo |
|---|---|---|---|
| `int` | total | alta | conteos, identificadores, dinero en céntimos |
| `float` | aproximada (2⁻⁵³) | máxima | medición, ciencia, gráficos, ML |
| `Decimal` | exacta en base 10 | baja | dinero, contabilidad, impuestos |
| `Fraction` | total | muy baja | probabilidad exacta, reparto proporcional |

La pregunta de diseño no es "¿qué tipo es mejor?" sino **"¿cuál es el contrato
de error de mi dominio?"**. Un sensor con ±0,5 % de precisión no se degrada por
un error relativo de 2⁻⁵³: ahí `float` es correcto. Una factura, no.

## 3. Texto

Un `str` es una secuencia **inmutable de code points Unicode**. Un `bytes` es
una secuencia de enteros de 0 a 255. La codificación es la función que convierte
entre los dos mundos, y en 2026 es UTF-8, sin excepciones que no vengan
impuestas por un sistema heredado.

```python
texto = "año 2026 — ñandú"
datos = texto.encode("utf-8")     # str → bytes
datos.decode("utf-8")             # bytes → str, reversible
datos.decode("latin-1")           # 'aÃ±o…' ← mojibake: decodificar mal no falla,
                                  #   produce basura convincente
```

### f-strings: más de lo que parece

```python
nombre, saldo, ratio = "Ana", 1234.5678, 0.8734

f"{nombre}: {saldo:.2f}"          # 'Ana: 1234.57'      — dos decimales
f"{saldo:>12.2f}"                 # '     1234.57'      — alineado a la derecha
f"{saldo:,.2f}"                   # '1,234.57'          — separador de miles
f"{ratio:.1%}"                    # '87.3%'             — como porcentaje
f"{nombre!r}"                     # "'Ana'"             — repr, con comillas
f"{saldo=}"                       # 'saldo=1234.5678'   — depuración
```

Ese `{variable=}` es de lo más útil que tiene el lenguaje para depurar: imprime
el nombre y el valor sin repetirte.

### Los métodos que de verdad usarás

```python
"  CR01-0002  ".strip()           # 'CR01-0002'  — quita espacios de los extremos
"cr01".upper()                    # 'CR01'
"Ana Pérez".split()               # ['Ana', 'Pérez']
"-".join(["CR01", "0002"])        # 'CR01-0002'
"CR01-0002".startswith("CR")      # True
"CR01-0002".replace("-", "")      # 'CR010002'
"ana@nova.ai".casefold()          # comparación insensible CORRECTA (mejor que lower)
```

Todos devuelven algo nuevo. Ninguno modifica el original.

## 4. La verdad, y el bug del cero legítimo

Todo objeto de Python tiene un valor de verdad. Son falsos exactamente estos:
`False`, `None`, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `range(0)`. Todo
lo demás es verdadero — incluidos `"False"` (texto no vacío) y `[0]` (lista no
vacía).

Eso habilita el estilo idiomático `if items:` para preguntar "¿hay elementos?".
Y habilita también el bug más caro de este módulo:

```python
# INCORRECTO: un descuento de 0 es un valor legítimo del negocio
# ("hoy no hay descuento"), pero es falsy y se confunde con "no me lo pasaron"
def apply_discount(price, discount=None):
    if not discount:
        discount = DESCUENTO_POR_DEFECTO
    return price * (1 - discount)

# CORRECTO: la pregunta real no era "¿es verdadero?" sino "¿me lo pasaron?"
def apply_discount(price, discount=None):
    if discount is None:
        discount = DESCUENTO_POR_DEFECTO
    return price * (1 - discount)
```

**La regla:** `if x:` pregunta *¿tiene contenido?*; `if x is None:` pregunta
*¿fue proporcionado?*. Son preguntas distintas y el dominio decide cuál toca.
Lo vas a implementar en el ejercicio `descuento`.

### `and` y `or` no devuelven booleanos

Devuelven **uno de sus operandos**, y evalúan con pereza:

```python
nombre = entrada or "anónimo"     # si entrada es falsy, usa el default
usuario and usuario.notificar()   # solo llama si usuario es verdadero
```

El cortocircuito no es solo estilo: el operando de la derecha puede ser una
llamada cara, y no se evalúa si no hace falta.

## 5. Control de flujo

```python
if temperature < 0:
    print("helada")
elif temperature < 15:
    print("fría")
else:
    print("templada")
```

Los bloques se marcan con **indentación**, no con llaves. Cuatro espacios,
siempre.

### El `for` es un consumidor de protocolo

No es un contador con condición de parada como en C: es una petición — *dame
tus elementos hasta que te agotes*.

```python
for reading in readings: ...             # una lista
for char in "python": ...                # un texto
for line in open("data.log"): ...        # un archivo, sin cargarlo entero
```

Cuando necesitas más que el elemento, hay una herramienta para cada caso, y
ninguna es un contador manual:

```python
for i, reading in enumerate(readings, start=1):    # posición y valor
    print(f"Lectura {i}: {reading}")

for nombre, saldo in zip(nombres, saldos):         # dos secuencias a la vez
    print(f"{nombre}: {saldo}")

for ref in sorted(refs):                           # ordenado, sin tocar refs
    print(ref)

for ref in reversed(refs):                         # al revés
    print(ref)
```

### `while`, y el `else` que casi nadie conoce

`while` es para cuando **no sabes cuántas vueltas** habrá:

```python
while queue:
    procesar(queue.pop())
```

Y los bucles admiten un `else` que se ejecuta **si no hubo `break`**:

```python
for movimiento in movimientos:
    if movimiento["ref"] == buscada:
        print("encontrado")
        break
else:
    print("no aparece en el archivo")     # solo si el for terminó sin break
```

Es exactamente "busca; si no lo encontraste, haz esto otro", sin variables
bandera.

### `match`: comparar por forma

Desde Python 3.10 puedes ramificar según la **estructura** de un dato, no solo
según su valor:

```python
def describir(evento: dict) -> str:
    match evento:
        case {"tipo": "pago", "monto": monto} if monto > 100_000:
            return f"pago grande de {monto}"
        case {"tipo": "pago", "monto": monto}:
            return f"pago de {monto}"
        case {"tipo": "reverso", "ref": ref}:
            return f"reverso de {ref}"
        case _:
            return "evento desconocido"
```

Fíjate en lo que hace: comprueba la forma **y** extrae los valores en la misma
línea. Con `if` encadenados serían cuatro comprobaciones de clave más cuatro
accesos. Ese `case _` final es el comodín, y conviene ponerlo siempre: sin él,
un evento que no encaje pasa de largo en silencio.

## 6. Funciones: la unidad de diseño

```python
def average(numbers: list[float]) -> float:
    """Calcula la media. Lanza ValueError si la lista está vacía."""
    if not numbers:
        raise ValueError("no se puede promediar una lista vacía")
    return sum(numbers) / len(numbers)
```

Las anotaciones no las verifica Python al ejecutar, pero documentan la
intención y tu editor las usa para avisarte antes de que ejecutes nada.

### El repertorio de parámetros

```python
def transferir(origen, destino, *, monto_cents, concepto="", **extra):
    ...
```

- **Posicionales**: `origen`, `destino`. Se pasan por orden.
- **Con valor por defecto**: `concepto=""`. Opcionales.
- **`*` a secas**: todo lo que va después es **obligatoriamente por nombre**.
  `transferir("a", "b", 5000)` falla; hay que escribir `monto_cents=5000`. Para
  un argumento que se puede confundir con otro, esto no es formalismo: es
  impedir un bug.
- **`**extra`**: recoge los sobrantes en un dict.

Y el detalle que ya viste en el módulo 00: **nunca uses un mutable como valor
por defecto**. Se crea una sola vez, al definir la función, y se comparte entre
todas las llamadas. `None` y crear dentro del cuerpo es el patrón correcto.

### Los errores son parte del contrato

Cuando una función recibe algo con lo que no puede trabajar, **lanza una
excepción**. No devuelvas `None`, ni `0`, ni `-1`:

```python
try:
    media = average(lecturas)
except ValueError as error:
    logger.warning("sensor sin lecturas: %s", error)
    media = None
```

Captura la excepción **más específica** que puedas, y tan cerca como puedas de
donde sabes qué hacer con ella. `except Exception: pass` oculta desde un error
de tipos hasta una caída de red, y convierte un fallo en datos silenciosamente
malos.

## Caso real

Un panel mostraba el consumo medio diario por sucursal. Durante tres semanas
estuvo mal y nadie lo notó, porque el número que enseñaba era perfectamente
creíble. Cuando por fin se miró, había **tres bugs de este módulo apilados**:

```python
def resumen(lecturas, descuento=None):
    if not lecturas:
        return 0                                   # bug 1
    if not descuento:
        descuento = DESCUENTO_ESTANDAR             # bug 2
    total = sum(l["importe"] for l in lecturas)    # bug 3: importe era float
    return total * (1 - descuento) / len(lecturas)
```

**Bug 1.** Un sensor sin lecturas devolvía `0`, que es un consumo medio
perfectamente posible en invierno. El fallo se disfrazó de dato. Devolver un
valor de consolación en vez de lanzar `ValueError` convirtió un error visible
en una mentira invisible.

**Bug 2.** Una sucursal tenía descuento `0.0` ese mes — un valor legítimo del
negocio. Como `0.0` es falsy, `not descuento` se cumplió y le aplicó el
descuento estándar del 12 %. Cobró de menos durante tres semanas. La pregunta
correcta era `if descuento is None`.

**Bug 3.** Los importes venían en `float`. Al sumar decenas de miles, el error
de redondeo acumulado ya era de céntimos por sucursal; al cruzarlo con
contabilidad, nada cuadraba y nadie sabía por qué. Con `int` de céntimos, el
total habría sido exacto.

Los tres arreglos son de una línea cada uno. Los tres son de este módulo. Y
ninguno se habría detectado con más tests de la lógica de negocio, porque la
lógica de negocio era correcta — lo que estaba mal eran los cimientos.

## Ejercicios

Los ejercicios están en `ejercicios/`. Cada archivo tiene una función sin
terminar. Tu trabajo es completarla.

```bash
uv run pytest ruta/01-fundamentos
```

Los verás en rojo: es lo esperado. Los stubs lanzan `NotImplementedError` a
propósito. Ve resolviendo y vuelve a correrlos hasta que estén verdes.

- **`ejercicios/base/saludo.py`** — devolver un saludo, sin espacios sobrantes.
  El más sencillo de la ruta, para empezar.
- **`ejercicios/base/temperatura.py`** — convertir Celsius a Fahrenheit.
- **`ejercicios/base/dinero.py`** — formatear un importe en céntimos, con su
  signo y sus separadores. Aritmética de enteros, ni un `float`.
- **`ejercicios/base/descuento.py`** — el bug del cero legítimo, para que lo
  cometas una vez aquí y no en producción.
- **`ejercicios/reto/estadisticas.py`** — resumir una lista de números,
  incluida la mediana. Requiere manejar la lista vacía y el número par de
  elementos.
- **`ejercicios/reto/clasificar.py`** — ramificar por la forma de un dato con
  `match`.

Para correr uno solo:

```bash
uv run pytest ruta/01-fundamentos/tests/base/test_saludo.py -v
```

Si te atascas, en `soluciones/` está la versión de referencia. Míralas después
de intentarlo, no antes: leer una solución da la sensación de haber aprendido
sin haber aprendido.

## Resumen

- Asignar ata un nombre a un objeto. `is` compara identidad, `==` compara
  valor, y `is` solo se usa contra `None`, `True` y `False`.
- Los inmutables no se modifican: los métodos de `str` devuelven uno nuevo.
- `int` tiene precisión arbitraria. `float` cumple IEEE 754, así que
  `0.1 + 0.2 != 0.3` y los floats se comparan con `math.isclose`.
- `nan` no es igual ni a sí mismo; se detecta con `math.isnan`.
- El dinero va en `Decimal` o en enteros de céntimos. Nunca en `float`, ni
  siquiera en la columna de la base de datos.
- Elige el tipo numérico por el contrato de error de tu dominio.
- El texto son code points; los bytes son bytes; UTF-8 es la codificación por
  defecto. Decodificar mal no falla: produce basura convincente.
- `if x:` pregunta si tiene contenido; `if x is None:` pregunta si se
  proporcionó. Confundirlas es el bug del cero legítimo.
- `and` y `or` devuelven operandos, no booleanos, y evalúan con pereza.
- El `for` consume un protocolo. Para la posición, `enumerate`; para dos
  secuencias, `zip`. Nunca un contador manual.
- El `else` de un bucle se ejecuta si no hubo `break`.
- `match` compara por forma y extrae valores a la vez. Pon siempre el `case _`.
- Un `*` en la firma obliga a pasar por nombre lo que venga después. Úsalo
  cuando confundir dos argumentos sea posible.
- Cuando una función no puede cumplir su contrato, lanza. Un valor de
  consolación convierte un fallo en datos malos.

## Preguntas de repaso

1. `a = [1, 2]; b = a; c = a[:]`. Tras `b.append(3)`, ¿qué valen `a`, `b` y
   `c`? ¿Y qué devuelven `a is b` y `a == c`?
2. ¿Por qué `0.1 + 0.2 == 0.3` es `False`, y cómo se compara bien?
3. Te piden guardar importes en una base de datos. ¿Qué tipo usas y por qué no
   `float`?
4. Una función recibe `descuento=0`. ¿Qué hace mal `if not descuento:` y cómo
   se arregla?
5. ¿Qué devuelve `[] or "vacío"`? ¿Y `0 or 5`? ¿Y `"a" and "b"`?
6. Recorres una lista buscando un elemento y quieres hacer algo si no aparece.
   ¿Cómo lo escribes sin una variable bandera?
7. ¿Qué ventaja tiene `match` sobre cuatro `if` encadenados al procesar un
   diccionario con forma variable?
8. ¿Para qué sirve el `*` suelto en `def f(a, b, *, c)`?
9. `average([])`: ¿devolver `0` o lanzar `ValueError`? Justifícalo con el caso
   real del módulo.

## Recursos

- [El tutorial oficial de Python](https://docs.python.org/es/3/tutorial/) —
  `doc-oficial` · `es` · `principiante`. En español y escrito por quienes hacen
  el lenguaje. Los capítulos 3 al 5 cubren casi todo este módulo.
- [PEP 8 — Guía de estilo](https://peps.python.org/pep-0008/) —
  `doc-oficial` · `en` · `principiante`. Ruff la aplica por ti, pero conviene
  saber de dónde salen las reglas.
- [Mini-especificación de formato](https://docs.python.org/es/3/library/string.html#format-specification-mini-language)
  — `doc-oficial` · `es` · `intermedio`. Todo lo que cabe después de los dos
  puntos en una f-string.
- [`decimal` — documentación](https://docs.python.org/es/3/library/decimal.html)
  — `doc-oficial` · `es` · `intermedio`. Para cuando el dinero sea tuyo.
- [What Every Computer Scientist Should Know About Floating-Point](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)
  — `artículo` · `en` · `avanzado`. El clásico sobre por qué los floats son
  así. Denso, pero se lee una vez en la vida y se entiende para siempre.

Más enlaces por tema en [`recursos/enlaces/`](../../recursos/enlaces/README.md).

## Siguiente

Módulo 02 · Estructuras de datos.
