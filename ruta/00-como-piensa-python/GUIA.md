# Módulo 00 · Cómo piensa Python

> **Prerrequisitos:** ninguno<br>
> **Tiempo estimado:** 180 min<br>
> **Si ya dominas esto:** salta al módulo 01

Este módulo no enseña sintaxis. Enseña dos cosas: **qué es un programa** y con
qué **modelos mentales** razona un pythonista sobre cualquier código. Eso es lo
que separa a quien traduce sintaxis de otro lenguaje de quien piensa en este.

Puedes saltártelo y empezar por el 01. Mucha gente lo hace y aprende a
programar igual. Pero cuando en el módulo 09 te encuentres un grafo de estado
de LangGraph, la diferencia entre "esto es magia que memorizo" y "esto es el
protocolo de iteración otra vez" se decide aquí.

## Qué vas a poder hacer al terminar

- Explicar qué hace un ordenador cuando ejecuta tu programa
- Distinguir compilación de interpretación y saber qué implica cada una
- Explicar por qué una variable es una etiqueta y no una caja
- Reconocer código idiomático y el acento de otros lenguajes
- Usar los protocolos para integrar tus tipos con el lenguaje
- Elegir entre EAFP y LBYL con criterio
- Diagnosticar errores de nombres con la regla LEGB

## 1. Qué es un programa, en realidad

Un ordenador sin programa es un objeto, igual que un piano sin pianista es una
caja de madera. Y lo que hace un ordenador es mucho más simple de lo que
parece: **solo sabe ejecutar operaciones elementales** —sumar, dividir, comparar,
mover un dato de un sitio a otro— pero las hace muy rápido y las repite
cuantas veces haga falta.

Supón que quieres la velocidad media de un viaje. Sabes la distancia y el
tiempo. El ordenador no tiene ni idea de qué es la velocidad, así que hay que
decírselo paso a paso:

1. toma un número que representa la distancia
2. toma un número que representa el tiempo
3. divide el primero entre el segundo y guarda el resultado
4. muestra ese resultado

Esas cuatro acciones son un **programa**. Y el punto que conviene retener:
programar no es explicarle un concepto al ordenador, es descomponer ese
concepto en operaciones que ya sabe hacer.

### El lenguaje de la máquina

El conjunto completo de operaciones que un procesador reconoce se llama su
**lista de instrucciones**, y es su alfabeto. Es rudimentario: "coge ese
número, divídelo por aquel, guarda el resultado".

Todo lenguaje —humano o de máquina— se compone de cuatro cosas:

| Elemento | Qué es | Ejemplo de error |
|---|---|---|
| **Alfabeto** | los símbolos disponibles | escribir en un alfabeto que el lenguaje no reconoce |
| **Léxico** | las palabras que existen | `pritn(...)` — esa palabra no está en el diccionario |
| **Sintaxis** | cómo se combinan | `if x = 3:` — el orden no forma una frase válida |
| **Semántica** | si la frase tiene sentido | `edad = "hola" / 2` — es válido de escribir y no significa nada |

Los cuatro tipos de error existen en programación, y cada uno se descubre en un
momento distinto. Los tres primeros los caza el intérprete antes o al arrancar.
**El cuarto lo descubres tú, en producción, cuando el resultado no cuadra.** Por
eso este repositorio insiste tanto en los tests: son la única red para la cuarta
categoría.

Un programa escrito en un lenguaje que un humano puede leer se llama **código
fuente**. Lo que ejecuta la máquina es otra cosa, y algo tiene que traducir.

## 2. Compilar o interpretar

Hay dos formas de pasar del código fuente al lenguaje de la máquina:

**Compilar.** Se traduce el programa entero, una vez, y sale un archivo
ejecutable. Se distribuye ese archivo y se ejecuta directamente.

**Interpretar.** No hay traducción previa: un programa —el intérprete— lee tu
código y lo va ejecutando línea a línea, cada vez que corres el programa.

Ninguna de las dos es mejor; tienen contratos distintos:

| | Compilado | Interpretado |
|---|---|---|
| Velocidad de ejecución | alta: ya está traducido | menor: se traduce sobre la marcha |
| Ver el resultado de un cambio | hay que recompilar | ejecutas y ya |
| Errores de sintaxis | todos, antes de ejecutar | cuando la línea se alcanza |
| Distribuir | un ejecutable por plataforma | el código, y el intérprete en destino |
| Ocultar el código | sí | no |

Python es **interpretado**, y de ahí salen tres consecuencias que vas a notar
todos los días:

- **El ciclo es corto.** Escribes, ejecutas, ves el resultado. Sin paso de
  compilación. Es la razón principal de que Python domine el prototipado y la
  ciencia de datos.
- **Un error de sintaxis en la línea 200 no impide que se ejecuten las 199
  primeras.** El programa arranca y revienta al llegar. En un lenguaje
  compilado no habrías podido ni ejecutarlo.
- **Es más lento.** Bastante. Y esto explica la anomalía que más desconcierta a
  quien llega: **el stack de IA está escrito en Python siendo Python lento.**

La resolución de esa paradoja: NumPy, PyTorch y compañía no ejecutan Python en
el bucle caliente. Ejecutan C, CUDA y Rust. Python es la capa donde un humano
describe *qué* quiere. Es el lenguaje de coordinación, no el de cálculo.

Tenlo presente durante toda la ruta: casi nunca vas a escribir Python rápido.
Vas a escribir Python **claro** que orquesta cosas rápidas.

### Hay más de un Python

Cuando alguien dice "Python" puede referirse a dos cosas distintas: al
**lenguaje** (las reglas) o a una **implementación** (un programa concreto que
las ejecuta).

- **CPython** es la implementación de referencia, escrita en C. Es la que
  instalas por defecto y la que usa este repositorio.
- **PyPy** ejecuta el mismo lenguaje con compilación al vuelo: mucho más rápido
  en código Python puro, y peor integrado con extensiones en C.
- Existen otras (Jython, IronPython, MicroPython) para entornos concretos.

Esta distinción no es trivia: cuando en el módulo 06 hablemos del **GIL**, verás
que es una característica de *CPython*, no del lenguaje. Confundir el lenguaje
con su implementación lleva a conclusiones equivocadas sobre qué se puede
cambiar y qué no.

## 3. Un lenguaje que nadie planeó

Python no nació de un comité ni de una empresa. Guido van Rossum lo empezó en
las navidades de 1989 como proyecto personal, arrastrando la lección de un
lenguaje anterior llamado ABC: ABC era elegante y pedagógicamente brillante,
pero **cerrado** — no podías extenderlo ni conectarlo con el sistema operativo,
así que nadie lo usó para trabajar de verdad.

Python heredó la legibilidad de ABC y corrigió su error: se diseñó para ser
extensible y para hablar con el resto del mundo. Esa decisión —poder envolver
bibliotecas escritas en C— es exactamente la que treinta años después lo
convirtió en el lenguaje de la IA.

## 4. El Zen como criterio de decisión

Escribe esto en un intérprete:

```python
import this
```

Salen diecinueve aforismos (PEP 20). Leídos como póster de oficina son
perogrulladas. Leídos como **criterios de decisión** son una herramienta de
ingeniería: deciden qué código pasa una revisión y qué API se considera bien
diseñada. Los cinco que más consecuencias tienen:

### Explicit is better than implicit

No prohíbe abstraer; prohíbe la magia que no puedes rastrear.

```python
# Opaco: ¿de dónde sale `settings`?
from app.config import *

# Rastreable: puedes seguir el hilo hasta la definición
from app.config import settings
```

El criterio no es "poca abstracción", es **rastreabilidad**. Un decorador
visible encima de la función es explícito. Un parche aplicado en otro módulo al
importarse, no.

El mismo principio explica decisiones profundas del lenguaje: el `self`
explícito en los métodos, que no haya conversiones automáticas entre tipos
(`"1" + 1` es un error, no un `"11"` sorpresa como en JavaScript), y que haga
falta declarar `global` para reasignar una variable de fuera.

### Simple is better than complex. Complex is better than complicated.

Tres niveles que conviene distinguir, porque el uso coloquial los confunde:

| Nivel | Qué es | Veredicto |
|---|---|---|
| **Simple** | las mínimas partes móviles para el problema real | ideal |
| **Complejo** | muchas partes, cada una justificada por el dominio | aceptable |
| **Complicado** | partes que existen por historia, moda o descuido | deuda técnica |

La complejidad **esencial** (un motor de conciliación bancaria lo es) se
gestiona. La **accidental** (tres capas de indirección porque "así lo hace
Netflix") se elimina. Distinguirlas es probablemente el criterio de diseño más
importante de toda la ingeniería de software.

### Errors should never pass silently. Unless explicitly silenced.

```python
# Condenado: esto oculta desde un error de tipo hasta una caída de red
try:
    process_payment(order)
except Exception:
    pass

# Aprobado: excepción concreta, tratada, y con rastro
try:
    process_payment(order)
except PaymentDeclinedError as exc:
    logger.info("Pago rechazado para la orden %s: %s", order.id, exc)
    order.mark_declined(reason=str(exc))
```

La regla que se deriva: captura la excepción **más específica posible**, tan
cerca como puedas de donde sabes qué hacer con ella, y nunca sin dejar rastro.

### There should be one obvious way to do it

Es una declaración de guerra contra el "cada uno a su manera" (y contra el lema
opuesto de Perl). Para cada tarea común hay una forma canónica, y apartarse de
ella tiene coste social y técnico.

```python
# Acento extranjero: correcto, pero delata que vienes de C o Java
squares = []
i = 0
while i < 10:
    if i % 2 == 0:
        squares.append(i * i)
    i += 1

# Idiomático
squares = [n * n for n in range(10) if n % 2 == 0]
```

Los dos funcionan. Solo uno pasa una revisión sin comentarios. Y no es estética:
el segundo elimina dos fuentes de bugs —el contador manual y la condición de
parada— y comunica la intención (transformar filtrando) en vez del mecanismo
(iterar mutando).

### Namespaces are one honking great idea

El último aforismo es una pista sobre la arquitectura interna: en Python
**casi todo mecanismo de organización es un espacio de nombres** —módulos,
paquetes, clases, instancias, ámbitos de función— es decir, un mapeo de nombres
a objetos. Volveremos a ello en el modelo mental 5.

## 5. Modelo mental 1: todo es un objeto

En Python no hay ciudadanos de segunda. Los enteros son objetos. Las funciones
son objetos. Las clases son objetos. Los módulos son objetos.

```python
def greet(name: str) -> str:
    return f"Hola, {name}"

print(greet.__name__)         # 'greet' — tiene atributos
print(greet.__annotations__)  # {'name': <class 'str'>, 'return': <class 'str'>}

handlers = {"greeting": greet}   # cabe en una estructura de datos

def twice(func, value):          # se pasa como argumento
    return func(func(value))
```

Que las funciones sean objetos de primera clase es lo que hace posibles los
decoradores, los callbacks y media programación funcional. Que las clases sean
objetos es lo que hace posibles las factorías y los registros de plugins.

**Cuando algo en Python te parezca magia, la primera pregunta correcta es: ¿qué
objeto es esto y qué atributos tiene?** Casi siempre la magia se disuelve ahí.
Las herramientas para preguntarlo son `type()`, `dir()` y `vars()`.

## 6. Modelo mental 2: nombres, no cajas

La metáfora escolar —una variable es una caja que guarda un valor— produce
predicciones equivocadas en Python de forma sistemática. La metáfora correcta
es la **etiqueta**: un nombre atado a un objeto, y varios nombres pueden estar
atados al mismo objeto.

```python
a = [1, 2, 3]
b = a          # b NO es una copia: es otra etiqueta sobre el MISMO objeto
b.append(4)
print(a)       # [1, 2, 3, 4]  ← solo sorprende si piensas en cajas
```

```text
  Modelo "caja" (incorrecto)          Modelo "etiqueta" (correcto)

  a ┌─────────┐   b ┌─────────┐        a ──┐
    │ [1,2,3] │     │ [1,2,3] │             ├──▶ [1, 2, 3, 4]
    └─────────┘     └─────────┘        b ──┘
     (dos objetos)                      (un objeto, dos nombres)
```

De este modelo se deducen, sin memorizar nada, media docena de preguntas que
llenan foros: por qué copiar una lista exige `list(otra)` o `otra[:]`, qué
diferencia hay entre `==` (mismo valor) e `is` (mismo objeto), y por qué "Python
pasa por referencia" y "Python pasa por valor" son **las dos** descripciones
incorrectas. El término preciso es *paso por asignación*.

La trampa más cara que se deriva de no tener este modelo:

```python
# El valor por defecto se crea UNA vez, al definir la función.
def add_item(item, basket=[]):     # ← bug
    basket.append(item)
    return basket

add_item("pan")     # ['pan']
add_item("leche")   # ['pan', 'leche']  ← el mismo objeto de la llamada anterior
```

Lo arreglarás tú mismo en el ejercicio `carrito`.

## 7. Modelo mental 3: protocolos, no jerarquías

Quien viene de Java pregunta: ¿qué interfaz implementa este objeto? Un
pythonista pregunta: **¿qué métodos especiales define?** El lenguaje entero
está construido sobre protocolos: contratos de métodos `__dunder__` que
cualquier clase puede adoptar sin pedirle permiso a ninguna jerarquía.

| Si tu objeto define… | …habla el protocolo | …y funciona con |
|---|---|---|
| `__len__` | tamaño | `len(x)` |
| `__bool__` | verdad | `if x:` |
| `__iter__` / `__next__` | iteración | `for`, comprehensions, `sum`, `max` |
| `__getitem__` | indexación | `x[i]`, slicing |
| `__contains__` | pertenencia | `x in y` |
| `__enter__` / `__exit__` | contexto | `with` |
| `__call__` | invocación | `x(...)` |
| `__eq__`, `__lt__` | comparación | `==`, `sorted`, `min` |
| `__add__`, `__mul__` | aritmética | `+`, `*` |

Los protocolos además **encadenan**: el valor de verdad de un objeto se resuelve
preguntando primero por `__bool__`; si no está, por `__len__`; y si tampoco,
es verdadero. Eso explica por qué una lista vacía es falsa sin que nadie haya
escrito una regla especial para las listas.

La consecuencia estratégica: tus tipos se integran con la sintaxis del lenguaje
y con toda la biblioteca estándar simplemente **hablando el protocolo
adecuado**. NumPy, Pandas y PyTorch son, vistos así, colecciones enormes de
objetos que hablan los protocolos de aritmética, indexación e iteración — por
eso `matriz_a + matriz_b` y `tensor[mask]` se sienten parte del lenguaje.

## 8. Modelo mental 4: la iteración es la abstracción central

Si hubiera que elegir una sola abstracción como corazón de Python, sería el
iterable. El `for` de Python no es el `for` de C (un contador con condición de
parada): es una petición de protocolo — *dame tus elementos, uno a uno, hasta
que te agotes*.

```python
for char in "python": ...            # caracteres de un texto
for line in open("data.log"): ...    # líneas de un archivo, sin cargarlo entero
for row in db_cursor: ...            # filas de una consulta SQL
for chunk in llm_stream: ...         # tokens de un LLM en streaming
```

El mismo patrón sobre cuatro cosas radicalmente distintas. De aquí nacen las
comprehensions, los generadores (procesar gigabytes con memoria constante),
`itertools`, y por extensión directa el `async for` y los streams asíncronos que
dominan el backend moderno y los sistemas de agentes.

En Python, pensar un problema es muy a menudo **pensar qué fluye y cómo se
transforma ese flujo**.

## 9. Modelo mental 5: todo nombre vive en un espacio de nombres

Cuando Python encuentra el nombre `x`, lo busca en una cadena ordenada de
diccionarios: **L**ocal, **E**nclosing (funciones que la envuelven), **G**lobal
del módulo y **B**uiltin del lenguaje. Es la regla LEGB.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)   # local → si no existiera: enclosing → global → builtin
    inner()
```

Para atributos vale lo mismo con otra cadena: `obj.attr` se busca en el
`__dict__` de la instancia, luego en el de su clase, luego en las clases base.
**No hay excepciones ocultas: toda resolución de nombres es un recorrido
predecible sobre diccionarios que puedes inspeccionar.**

El valor de este modelo es diagnóstico: convierte los errores más confusos para
quien empieza —`UnboundLocalError`, haber llamado `list` a una variable y romper
la función `list`, atributos "que desaparecen"— en recorridos mecánicos que se
razonan en segundos con `vars()`, `dir()` y `__dict__`.

Y explica una regla que si no parece arbitraria: para **reasignar** una variable
de fuera desde dentro de una función hay que declararlo (`global` o `nonlocal`).
Sin esa declaración, asignar crea una variable local nueva. Lo vas a usar en el
ejercicio `contador`.

## 10. Duck typing, EAFP y batteries included

### Duck typing

Si camina como un pato y grazna como un pato, es un pato. La pregunta relevante
sobre un objeto no es *de qué clase es* sino *qué sabe hacer*. Una función que
necesita algo iterable no debe exigir una `list`:

```python
from collections.abc import Iterable

def total_amount(payments: Iterable[float]) -> float:
    return sum(payments)
```

Funciona igual con una lista en memoria, con un generador que lee un CSV de
10 GB línea a línea o con un cursor que pagina PostgreSQL.

Dónde **no** confiar en duck typing: en las fronteras del sistema —entrada de
usuario, payload de red, datos de terceros— donde un objeto con la forma
equivocada debe rechazarse pronto y con un mensaje claro, en vez de propagarse
hasta reventar tres capas más adentro. Ahí entra la validación explícita, que
verás con Pydantic en el módulo 07.

### EAFP frente a LBYL

Dos formas de tratar lo incierto: mirar antes de saltar (*Look Before You Leap*)
o actuar y pedir perdón (*Easier to Ask Forgiveness than Permission*).

```python
# LBYL
if "user_id" in payload:
    user_id = payload["user_id"]
else:
    user_id = None

# EAFP — idiomático
try:
    user_id = payload["user_id"]
except KeyError:
    user_id = None

# ...que en este caso concreto se condensa
user_id = payload.get("user_id")
```

Python prefiere EAFP por dos razones técnicas, no estéticas:

1. **Elimina condiciones de carrera.** Entre comprobar que un archivo existe y
   abrirlo puede pasar tiempo en el que otro proceso lo borra. `try: open(...)`
   no tiene esa ventana; `if os.path.exists(...)` sí. En sistemas concurrentes
   esto es una clase entera de bugs.
2. **Optimiza el camino feliz.** Si la clave casi siempre está, evitas una
   comprobación en cada llamada.

Cuándo preferir LBYL: cuando el fallo es **frecuente y esperado** (lanzar
excepciones sí cuesta), cuando la comprobación se lee mejor para el caso de
negocio, o al validar argumentos al principio de una función pública.

### Batteries included

Python trae más de doscientos módulos de serie. El orden correcto de búsqueda
ante una necesidad nueva es: **(1) biblioteca estándar, (2) paquete maduro y
mantenido, (3) código propio.** Invertirlo produce árboles de dependencias
frágiles, superficie de ataque en la cadena de suministro y proyectos que
envejecen mal. Cada dependencia es un contrato de mantenimiento que firmas con
un desconocido.

## Caso real

Estás diseñando el SDK de un servicio de pagos. Dos borradores para crear un
cargo:

```python
# Borrador A — configuración implícita, estado global
import paysdk
paysdk.init("sk_live_...")
charge = paysdk.charge(1000, "USD")

# Borrador B — dependencias explícitas
from paysdk import Client
client = Client(api_key="sk_live_...", timeout=10.0, max_retries=3)
charge = client.charges.create(amount=1000, currency="USD")
```

El Zen decide sin ambigüedad, y no por gusto:

- **Explícito**: en B, las credenciales y la configuración tienen un origen
  rastreable. En A, `charge` usa un estado global que se puso en otro sitio.
- **Namespaces**: `client.charges.create` organiza la superficie de la API en
  espacios navegables; con autocompletado descubres qué existe.
- **Testabilidad**: un `Client` se inyecta y se sustituye en un test. Un módulo
  con estado global se parchea con dolor.

Esto es lo que quiere decir que la filosofía es *operativa*: no fue decoración,
fue el árbol de decisión.

## Ejercicios

```bash
uv run pytest ruta/00-como-piensa-python
```

Los verás en rojo: los ejercicios están sin resolver, y ese es el estado
correcto de partida.

- **`ejercicios/base/idiomatico.py`** — reescribir un bucle con acento
  extranjero en la forma idiomática.
- **`ejercicios/base/carrito.py`** — arreglar la trampa del argumento mutable
  por defecto. Aquí compruebas si de verdad tienes el modelo de etiquetas.
- **`ejercicios/base/protocolo.py`** — la cascada del valor de verdad:
  `__bool__`, `__len__` y qué pasa cuando no hay ninguno.
- **`ejercicios/reto/baraja.py`** — hacer que una clase tuya hable los
  protocolos del lenguaje. Sale más corto de lo que esperas.
- **`ejercicios/reto/contador.py`** — closures y `nonlocal`: la regla LEGB en
  acción, y por qué asignar no es lo mismo que leer.

## Resumen

- Un ordenador solo hace operaciones elementales, muy rápido. Programar es
  descomponer un concepto en operaciones que ya sabe hacer.
- Todo lenguaje tiene alfabeto, léxico, sintaxis y semántica. Los tres primeros
  errores los caza el intérprete; **el semántico lo descubres tú**.
- Python es interpretado: ciclo corto, errores que aparecen al alcanzarlos, y
  más lento. Por eso es la capa de coordinación, no la de cálculo.
- "Python" es un lenguaje; CPython es una implementación. El GIL es de CPython.
- El Zen no es decoración: es el árbol de decisión de una revisión de código.
- Distingue complejidad esencial (se gestiona) de accidental (se elimina).
- **Todo es un objeto.** Ante algo que parece magia: ¿qué objeto es y qué
  atributos tiene?
- **Nombres, no cajas.** Varias etiquetas pueden apuntar al mismo objeto; de
  ahí salen los bugs de aliasing y el del argumento mutable por defecto.
- **Protocolos, no jerarquías.** Tus tipos se integran con el lenguaje hablando
  los `__dunder__` adecuados, y los protocolos encadenan.
- **La iteración es el corazón.** El mismo `for` recorre un texto, un archivo,
  un cursor de base de datos y un stream de LLM.
- **Todo nombre se resuelve en un espacio de nombres**, siguiendo LEGB. Es una
  herramienta de diagnóstico, no un dato de examen.
- EAFP por defecto; LBYL cuando el fallo es frecuente y esperado.
- Biblioteca estándar primero. Cada dependencia es un contrato con un
  desconocido.

## Preguntas de repaso

1. ¿Cuál de los cuatro tipos de error de un lenguaje no puede detectar el
   intérprete, y qué haces al respecto?
2. Tu programa tiene un error de sintaxis en la línea 200. ¿Qué pasa al
   ejecutarlo en Python, y qué habría pasado en un lenguaje compilado?
3. Si Python es lento, ¿por qué el stack de IA está escrito en Python?
4. ¿Qué diferencia hay entre "el lenguaje Python" y "CPython", y por qué
   importa esa distinción?
5. `a = [1, 2]; b = a; c = a[:]` — después de `b.append(3)`, ¿qué valen `a`,
   `b` y `c`? Explícalo con el modelo de etiquetas, sin ejecutarlo.
6. ¿Por qué una lista vacía es falsa sin que exista una regla especial para las
   listas?
7. ¿Por qué `except Exception: pass` es peor que no capturar nada?
8. Una función necesita "algo con lo que iterar". ¿Por qué anotarla como `list`
   es una mala decisión, y qué anotarías en su lugar?
9. Da un caso donde LBYL sea preferible a EAFP y explica por qué.
10. ¿Qué tienen en común un archivo abierto, un cursor de base de datos y la
    respuesta en streaming de un LLM?

## Recursos

- [El Zen de Python (PEP 20)](https://peps.python.org/pep-0020/) —
  `doc-oficial` · `en` · `principiante`. Diecinueve líneas; se lee en un minuto
  y se entiende en toda una carrera.
- [PEP 8 — Guía de estilo](https://peps.python.org/pep-0008/) —
  `doc-oficial` · `en` · `principiante`. Ruff la aplica por ti, pero conviene
  saber de dónde salen las reglas.
- [Modelo de datos de Python](https://docs.python.org/es/3/reference/datamodel.html)
  — `doc-oficial` · `es` · `avanzado`. La referencia de todos los protocolos.
  No se lee de corrido: se consulta.
- [Ejecución de programas](https://docs.python.org/es/3/reference/executionmodel.html)
  — `doc-oficial` · `es` · `avanzado`. Cómo se resuelven los nombres, con la
  precisión de una especificación.

Más enlaces por tema en [`recursos/enlaces/`](../../recursos/enlaces/README.md).

## Siguiente

Módulo 01 · Fundamentos, donde estos modelos se convierten en sintaxis.
