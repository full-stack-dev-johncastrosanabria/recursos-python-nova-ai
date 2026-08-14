# Módulo 01 · Fundamentos

> **Prerrequisitos:** ninguno; el módulo 00 ayuda pero no hace falta<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 02

Fundamentos no significa superficial. Este módulo cubre lo que se usa todos los
días —imprimir, calcular, leer datos, decidir, repetir y agrupar en funciones—
pero contando lo que casi nunca se cuenta: **qué contrato tiene cada cosa y
dónde se rompe**.

La mitad de los bugs caros de un sistema nacen aquí: un importe en `float`, un
descuento de cero tratado como "no hay descuento", un `input()` que devuelve
texto cuando esperabas un número, una función que devuelve `0` cuando debería
fallar. Nada de eso es sintaxis avanzada. Es esto, mal entendido.

## Qué vas a poder hacer al terminar

- Imprimir con control sobre el formato y los separadores
- Escribir literales numéricos y de texto en todas sus formas
- Aplicar los operadores conociendo sus prioridades
- Leer datos del usuario y convertirlos con seguridad
- Elegir el tipo numérico correcto según el contrato de error de tu dominio
- Distinguir "está vacío" de "no se proporcionó"
- Manipular bits con máscaras
- Escribir condicionales, bucles y funciones idiomáticas
- Tratar los errores como parte del contrato de una función

## 1. Tu primer programa y `print()`

```python
print("Hola, mundo")
```

`print` es una **función**: un trozo de código con nombre que se invoca
escribiendo su nombre y unos paréntesis. Lo que va dentro son sus
**argumentos**.

Acepta varios, y los separa con un espacio:

```python
print("Ana", "Pérez", 30)      # Ana Pérez 30
```

Y tiene dos argumentos con nombre que cambian su comportamiento y que casi nadie
descubre a tiempo:

```python
print("a", "b", "c", sep="-")        # a-b-c
print("sin salto", end="")           # no baja de línea al terminar
print("uno", "dos", sep=", ", end="!\n")   # uno, dos!
```

`sep` es lo que va **entre** los argumentos; `end` es lo que va **después del
último**, y por defecto vale `"\n"`, el salto de línea. Cuando quieras construir
una línea en varios pasos, `end=""` es la herramienta.

### Argumentos posicionales y con nombre

Esa distinción aparece aquí por primera vez y recorre todo el lenguaje:

- **Posicional**: su significado lo da su posición. `print("a", "b")`.
- **Con nombre (keyword)**: su significado lo da su nombre. `sep="-"`.

Los posicionales van siempre antes que los de nombre. Volveremos a ello al
hablar de funciones.

### Caracteres de escape

Algunos caracteres no se pueden escribir directamente dentro de un texto, y se
representan con una barra invertida:

```python
print("primera\nsegunda")      # \n  salto de línea
print("col1\tcol2")            # \t  tabulador
print("Dijo \"hola\"")         # \"  comilla dentro de comillas
print("C:\\ruta\\archivo")     # \\  una barra invertida literal
```

Cuando el texto lleva muchas barras —rutas de Windows, expresiones regulares—
existe el prefijo `r` de *raw*, que desactiva los escapes:

```python
print(r"C:\ruta\archivo")      # C:\ruta\archivo
```

## 2. Literales: cómo se escriben los datos

Un **literal** es un dato escrito directamente en el código. Python tiene más
formas de las que parece, y varias ahorran errores:

```python
# Enteros
1_500_000        # los guiones bajos se ignoran: solo son para leerlo
0b1010           # binario  → 10
0o755            # octal    → 493
0xFF             # hexadecimal → 255

# Decimales
3.14
1.5e3            # notación científica: 1500.0
6.02e23
.5               # el 0 inicial es opcional (aunque conviene ponerlo)

# Texto
"comillas dobles"
'comillas simples'      # equivalentes: usa las que eviten escapar
"""texto
en varias líneas"""

# Booleanos y ausencia
True, False
None
```

Ese `1_500_000` es de lo más útil que hay para el dinero y los umbrales: el
intérprete ignora los guiones bajos y tú lees la cifra de un vistazo.

## 3. Variables y asignación

```python
name: str = "Ana"
age: int = 30
```

Python deduce el tipo, pero anotarlo hace el código más claro. Hazlo: dentro de
seis meses, quien lo lea serás tú.

Los nombres tienen reglas: empiezan por letra o guion bajo, siguen con letras,
dígitos o guiones bajos, distinguen mayúsculas de minúsculas (`total` y `Total`
son variables distintas) y no pueden ser palabras reservadas del lenguaje.
La convención es `snake_case` para variables y funciones.

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

## 4. Operadores y prioridades

```python
7 + 2      # 9     suma
7 - 2      # 5     resta
7 * 2      # 14    multiplicación
7 / 2      # 3.5   división: SIEMPRE devuelve float
7 // 2     # 3     división entera: trunca hacia abajo
7 % 2      # 1     resto
7 ** 2     # 49    potencia
```

Tres detalles que dan sorpresas:

**`/` siempre devuelve `float`**, aunque la división sea exacta: `4 / 2` es
`2.0`, no `2`. Si quieres un entero, `//`.

**`//` trunca hacia abajo, no hacia cero.** `-7 // 2` es `-4`, no `-3`. Y el
resto acompaña: `-7 % 2` es `1`. Es coherente (`a == (a // b) * b + a % b`) pero
sorprende si vienes de C.

**`**` asocia por la derecha**: `2 ** 3 ** 2` es `2 ** 9`, es decir 512, no 64.

### Prioridades

Cuando hay varios operadores sin paréntesis, se aplican en este orden (de más a
menos prioritario):

| Prioridad | Operadores |
|---|---|
| 1 | `**` |
| 2 | `+x`, `-x`, `~x` (unarios) |
| 3 | `*`, `/`, `//`, `%` |
| 4 | `+`, `-` |
| 5 | `<<`, `>>` |
| 6 | `&` |
| 7 | `^` |
| 8 | `\|` |
| 9 | comparaciones: `<`, `<=`, `>`, `>=`, `==`, `!=`, `is`, `in` |
| 10 | `not` |
| 11 | `and` |
| 12 | `or` |

No hace falta memorizarla. Hace falta saber que existe y **poner paréntesis
cuando la expresión no sea obvia de un vistazo**: el paréntesis que no
necesitabas cuesta dos caracteres, y el que faltaba cuesta una tarde.

### Operadores abreviados

```python
total = 0
total += 10     # equivale a total = total + 10
total -= 3
total *= 2
total //= 4
total **= 2
```

No son solo azúcar: dicen "modifica esto" en vez de "calcula esto otro y
reasígnalo", que es información para quien lee.

### Comparaciones encadenadas

Python permite algo que la mayoría de lenguajes no:

```python
if 0 <= edad <= 120:        # se lee como en matemáticas
    ...
```

Equivale a `0 <= edad and edad <= 120`, pero evalúa `edad` una sola vez.

## 5. Números: cuatro tipos y un contrato de error

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

## 6. Texto

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

### Los operadores sobre texto

```python
"CR" + "01"           # 'CR01'   concatenación
"-" * 20              # '--------------------'  repetición
"01" in "CR01-0002"   # True     subcadena
len("CR01")           # 4
```

Ojo: `+` entre texto y número **no** funciona. `"1" + 1` es un `TypeError`, no
un `"11"` sorpresa como en JavaScript. Es el *explicit is better than implicit*
del módulo 00 aplicado a la aritmética.

### f-strings: más de lo que parece

```python
nombre, saldo, ratio = "Ana", 1234.5678, 0.8734

f"{nombre}: {saldo:.2f}"          # 'Ana: 1234.57'      — dos decimales
f"{saldo:>12.2f}"                 # '     1234.57'      — alineado a la derecha
f"{saldo:<12.2f}"                 # '1234.57     '      — a la izquierda
f"{nombre:^11}"                   # '    Ana    '       — centrado
f"{saldo:,.2f}"                   # '1,234.57'          — separador de miles
f"{ratio:.1%}"                    # '87.3%'             — como porcentaje
f"{255:b}" , f"{255:x}"           # '11111111', 'ff'    — otras bases
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
"a,b,c".split(",")                # ['a', 'b', 'c']
"-".join(["CR01", "0002"])        # 'CR01-0002'
"CR01-0002".startswith("CR")      # True
"CR01-0002".replace("-", "")      # 'CR010002'
"CR01-0002".find("-")             # 4  (-1 si no está)
"1500".isdigit()                  # True
"ana@nova.ai".casefold()          # comparación insensible CORRECTA (mejor que lower)
```

Todos devuelven algo nuevo. Ninguno modifica el original.

## 7. Leer del usuario, y convertir con seguridad

```python
nombre = input("¿Cómo te llamas? ")
```

`input()` muestra el mensaje, espera a que el usuario escriba y devuelve lo
tecleado. Y aquí está la trampa que se lleva por delante a todo el mundo la
primera vez:

> **`input()` devuelve SIEMPRE un `str`.** Siempre. Aunque el usuario escriba
> `42`, lo que recibes es el texto `"42"`.

```python
edad = input("¿Edad? ")     # el usuario escribe 30
edad + 1                    # TypeError: no se puede sumar str e int
edad * 2                    # '3030'  ← esto sí "funciona", y es peor
```

Ese segundo caso es el peligroso: no falla, hace algo distinto de lo que
querías. Hay que **convertir explícitamente**:

```python
edad = int(input("¿Edad? "))
altura = float(input("¿Altura en metros? "))
```

### La conversión también falla

`int("hola")` lanza `ValueError`. Y ese error hay que tratarlo, porque el
usuario escribe cualquier cosa:

```python
try:
    edad = int(input("¿Edad? "))
except ValueError:
    print("Eso no es un número entero.")
```

Las conversiones que usarás:

```python
int("42")        # 42
int("42", 2)     # ← con base: '42' no es binario, ValueError
int("1010", 2)   # 10  — interpreta en base 2
int(3.99)        # 3   — trunca, no redondea
float("3.14")    # 3.14
str(42)          # '42'
bool("")         # False  (ver la sección siguiente)
```

Fíjate en `int(3.99) == 3`: trunca hacia cero, no redondea. Para redondear,
`round(3.99)` da `4`.

## 8. La verdad, y el bug del cero legítimo

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

## 9. Bits: cuando el dato son banderas

Además de los lógicos (`and`, `or`, `not`), que trabajan sobre valores de
verdad, hay operadores que trabajan **bit a bit** sobre enteros:

```python
0b1100 & 0b1010    # 0b1000  AND: 1 si ambos bits son 1
0b1100 | 0b1010    # 0b1110  OR:  1 si alguno lo es
0b1100 ^ 0b1010    # 0b0110  XOR: 1 si son distintos
~0b1100            # -13     NOT: invierte todos los bits
0b0001 << 3        # 0b1000  desplaza a la izquierda (×2 por posición)
0b1000 >> 2        # 0b0010  desplaza a la derecha (÷2 por posición)
```

No confundas `and` con `&`: el primero trabaja con la verdad del objeto entero,
el segundo con cada bit por separado.

¿Para qué sirve esto en 2026? Para **conjuntos compactos de banderas**: permisos
de archivo en Unix, flags de configuración, estados que se combinan. Un entero
guarda 64 booleanos y se comprueban en una operación.

```python
LEER, ESCRIBIR, EJECUTAR = 0b100, 0b010, 0b001

permisos = LEER | ESCRIBIR          # activar dos
permisos & ESCRIBIR                 # distinto de 0 → la tiene
permisos & ~ESCRIBIR                # quitarla
permisos ^ EJECUTAR                 # alternarla
```

Es tu ejercicio `banderas`.

## 10. Control de flujo

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
for n in range(5): ...                   # 0, 1, 2, 3, 4
for n in range(2, 10, 3): ...            # 2, 5, 8  (inicio, fin, paso)
```

`range(fin)` empieza en 0 y **no incluye el fin**. Es la misma convención
semiabierta del slicing, y por la misma razón: `len(range(a, b)) == b - a`.

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

### `while`, `break`, `continue`

`while` es para cuando **no sabes cuántas vueltas** habrá:

```python
while queue:
    procesar(queue.pop())
```

Dentro de cualquier bucle, `break` sale del todo y `continue` salta a la
siguiente vuelta:

```python
for linea in archivo:
    if not linea.strip():
        continue          # línea vacía: pasa a la siguiente
    if linea == "FIN":
        break             # termina el bucle
    procesar(linea)
```

### El `else` de los bucles

Los bucles admiten un `else` que se ejecuta **si no hubo `break`**:

```python
for movimiento in movimientos:
    if movimiento["ref"] == buscada:
        print("encontrado")
        break
else:
    print("no aparece en el archivo")     # solo si el for terminó sin break
```

Es exactamente "busca; si no lo encontraste, haz esto otro", sin variables
bandera. Se lee mal la primera vez y se agradece la décima.

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

## 11. Funciones: la unidad de diseño

```python
def average(numbers: list[float]) -> float:
    """Calcula la media. Lanza ValueError si la lista está vacía."""
    if not numbers:
        raise ValueError("no se puede promediar una lista vacía")
    return sum(numbers) / len(numbers)
```

Las anotaciones no las verifica Python al ejecutar, pero documentan la
intención y tu editor las usa para avisarte antes de que ejecutes nada.

### Por qué existen las funciones

No es solo para no repetirse. Una función **nombra** un trozo de razonamiento,
y ese nombre es lo que te permite pensar en el problema grande sin tener el
pequeño en la cabeza. Si no sabes cómo llamar a una función, normalmente es que
hace más de una cosa.

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

### `return`, y el `None` implícito

```python
def sin_return(x):
    x * 2            # calcula y tira el resultado

sin_return(5)        # None
```

Una función sin `return` devuelve `None`. Un `return` sin valor, también. No es
un error del lenguaje, pero sí una fuente de bugs cuando falta el `return` en
una rama:

```python
def clasificar(t):
    if t < 0:
        return "helada"
    elif t < 15:
        return "fría"
    # ← si t es 20, devuelve None en silencio
```

### Los errores son parte del contrato

Cuando una función recibe algo con lo que no puede trabajar, **lanza una
excepción**. No devuelvas `None`, ni `0`, ni `-1`.

## 12. Excepciones: cuando algo sale mal

```python
try:
    edad = int(input("¿Edad? "))
except ValueError:
    print("Eso no es un número.")
```

El bloque `try` contiene lo que puede fallar; el `except` dice qué hacer si
falla. Si no hay excepción, el `except` se salta entero.

### Varios `except`, del más concreto al más general

```python
try:
    with open(ruta) as archivo:
        datos = int(archivo.read())
except FileNotFoundError:
    print(f"No existe {ruta}")
except PermissionError:
    print(f"Sin permiso para leer {ruta}")
except ValueError:
    print("El archivo no contiene un número")
```

Se evalúan **en orden**, y gana el primero que encaje. Por eso el más general va
al final: si pones `except Exception` primero, los de abajo no se alcanzan
nunca.

### `else` y `finally`

```python
try:
    conexion = abrir_conexion()
except ConnectionError:
    logger.warning("no se pudo conectar")
else:
    procesar(conexion)        # solo si NO hubo excepción
finally:
    limpiar()                 # SIEMPRE, haya fallado o no
```

`else` es para lo que solo tiene sentido si todo fue bien, y sirve para
mantener el `try` lo más pequeño posible — cuanto menos código haya dentro,
menos probable es capturar una excepción que venía de otro sitio.

`finally` se ejecuta pase lo que pase, incluso si hay `return` o si la excepción
se propaga. Es donde se cierra lo que hay que cerrar.

### Las excepciones que más vas a ver

| Excepción | Cuándo |
|---|---|
| `ValueError` | el tipo es correcto pero el valor no: `int("hola")` |
| `TypeError` | el tipo es incorrecto: `"1" + 1` |
| `KeyError` | esa clave no está en el diccionario |
| `IndexError` | ese índice está fuera de la lista |
| `FileNotFoundError` | no existe el archivo |
| `ZeroDivisionError` | dividir entre cero |
| `AttributeError` | el objeto no tiene ese atributo |

### Lanzar las tuyas

```python
def withdraw(saldo_cents: int, monto_cents: int) -> int:
    if monto_cents <= 0:
        raise ValueError(f"el monto debe ser positivo, no {monto_cents}")
    if monto_cents > saldo_cents:
        raise ValueError(f"saldo insuficiente: hay {saldo_cents}")
    return saldo_cents - monto_cents
```

Fíjate en los mensajes: incluyen **el valor concreto**. Un error que dice
"monto inválido" obliga a reproducir el problema; uno que dice "el monto debe
ser positivo, no -500" se arregla leyendo el log.

Y la regla del módulo 00, ahora con sintaxis: captura la excepción **más
específica** que puedas, tan cerca como puedas de donde sabes qué hacer con
ella. `except Exception: pass` oculta desde un error de tipos hasta una caída de
red, y convierte un fallo en datos silenciosamente malos.

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
- **`ejercicios/base/entrada.py`** — convertir lo que escribe un usuario en un
  importe, con todos los errores tratados.
- **`ejercicios/base/banderas.py`** — permisos con operadores bit a bit.
- **`ejercicios/reto/estadisticas.py`** — resumir una lista de números,
  incluida la mediana.
- **`ejercicios/reto/clasificar.py`** — ramificar por la forma de un dato con
  `match`.
- **`ejercicios/reto/tabla.py`** — alinear una tabla de texto con
  especificadores de formato.

Para correr uno solo:

```bash
uv run pytest ruta/01-fundamentos/tests/base/test_saludo.py -v
```

Si te atascas, en `soluciones/` está la versión de referencia. Míralas después
de intentarlo, no antes: leer una solución da la sensación de haber aprendido
sin haber aprendido.

## Resumen

- `print` acepta varios argumentos y tiene `sep` y `end`, que casi nadie
  descubre a tiempo.
- Los literales numéricos admiten guiones bajos (`1_500_000`) y otras bases
  (`0b`, `0o`, `0x`).
- Asignar ata un nombre a un objeto. `is` compara identidad, `==` compara
  valor, y `is` solo se usa contra `None`, `True` y `False`.
- Los inmutables no se modifican: los métodos de `str` devuelven uno nuevo.
- `/` devuelve `float` siempre; `//` trunca hacia abajo; `**` asocia por la
  derecha. Pon paréntesis cuando la expresión no sea obvia.
- `int` tiene precisión arbitraria. `float` cumple IEEE 754, así que
  `0.1 + 0.2 != 0.3` y los floats se comparan con `math.isclose`.
- El dinero va en `Decimal` o en enteros de céntimos. Nunca en `float`.
- **`input()` devuelve siempre texto.** Convertir es tu trabajo, y esa
  conversión puede fallar.
- `if x:` pregunta si tiene contenido; `if x is None:` pregunta si se
  proporcionó. Confundirlas es el bug del cero legítimo.
- `and` y `or` devuelven operandos, no booleanos, y evalúan con pereza.
- Los operadores bit a bit (`&`, `|`, `^`, `~`, `<<`, `>>`) sirven para
  conjuntos compactos de banderas. No los confundas con los lógicos.
- El `for` consume un protocolo. Para la posición, `enumerate`; para dos
  secuencias, `zip`. Nunca un contador manual.
- El `else` de un bucle se ejecuta si no hubo `break`.
- `match` compara por forma y extrae valores a la vez. Pon siempre el `case _`.
- Un `*` en la firma obliga a pasar por nombre lo que venga después.
- Una función sin `return` devuelve `None`, y una rama sin `return` también.
- Los `except` se evalúan en orden: del más concreto al más general. `else` es
  para el camino feliz; `finally` se ejecuta pase lo que pase.
- Cuando una función no puede cumplir su contrato, lanza — y el mensaje incluye
  el valor concreto que llegó.

## Preguntas de repaso

1. ¿Qué imprime `print("a", "b", sep="", end="!")` y por qué?
2. ¿Cuánto vale `2 ** 3 ** 2`? ¿Y `-7 // 2`?
3. `a = [1, 2]; b = a; c = a[:]`. Tras `b.append(3)`, ¿qué valen `a`, `b` y
   `c`? ¿Y qué devuelven `a is b` y `a == c`?
4. ¿Por qué `0.1 + 0.2 == 0.3` es `False`, y cómo se compara bien?
5. Te piden guardar importes en una base de datos. ¿Qué tipo usas y por qué no
   `float`?
6. Un usuario escribe `30` cuando le pides la edad. ¿Qué devuelve `input()`, y
   qué pasa si haces `edad * 2` sin convertir?
7. Una función recibe `descuento=0`. ¿Qué hace mal `if not descuento:` y cómo
   se arregla?
8. ¿Qué devuelve `[] or "vacío"`? ¿Y `0 or 5`? ¿Y `"a" and "b"`?
9. ¿Qué diferencia hay entre `and` y `&`?
10. Recorres una lista buscando un elemento y quieres hacer algo si no aparece.
    ¿Cómo lo escribes sin una variable bandera?
11. Tienes tres `except`: `Exception`, `ValueError` y `KeyError`. ¿En qué orden
    los pones y qué pasa si te equivocas?
12. ¿Cuándo usarías `finally` en lugar de poner el código después del `try`?
13. `average([])`: ¿devolver `0` o lanzar `ValueError`? Justifícalo con el caso
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
- [Excepciones integradas](https://docs.python.org/es/3/library/exceptions.html)
  — `doc-oficial` · `es` · `intermedio`. La jerarquía completa: útil para saber
  qué capturar y qué lanzar.
- [`decimal` — documentación](https://docs.python.org/es/3/library/decimal.html)
  — `doc-oficial` · `es` · `intermedio`. Para cuando el dinero sea tuyo.
- [What Every Computer Scientist Should Know About Floating-Point](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)
  — `artículo` · `en` · `avanzado`. El clásico sobre por qué los floats son
  así. Denso, pero se lee una vez en la vida y se entiende para siempre.

Más enlaces por tema en [`recursos/enlaces/`](../../recursos/enlaces/README.md).

## Siguiente

Módulo 02 · Estructuras de datos.
