# Módulo 00 · Cómo piensa Python

> **Prerrequisitos:** ninguno
> **Tiempo estimado:** 90 min
> **Si ya dominas esto:** salta al módulo 01

Este módulo no enseña sintaxis. Enseña los cinco modelos mentales con los que
un pythonista razona sobre cualquier programa, y que separan a quien traduce
sintaxis de otro lenguaje de quien piensa en este.

Puedes saltártelo y empezar por el 01. Mucha gente lo hace y aprende a
programar igual. Pero cuando en el módulo 09 te encuentres un grafo de estado
de LangGraph, o en el 06 un `async for`, la diferencia entre "esto es magia que
memorizo" y "esto es el protocolo de iteración otra vez" se decide aquí.

## Qué vas a poder hacer al terminar

- Explicar por qué una variable es una etiqueta y no una caja
- Reconocer código idiomático y el acento de otros lenguajes
- Usar los protocolos para integrar tus tipos con el lenguaje
- Elegir entre EAFP y LBYL con criterio
- Diagnosticar errores de nombres con la regla LEGB

## 1. Un lenguaje que nadie planeó

Python no nació de un comité ni de una empresa. Guido van Rossum lo empezó en
las navidades de 1989 como proyecto personal, arrastrando la lección de un
lenguaje anterior llamado ABC: ABC era elegante y pedagógicamente brillante,
pero cerrado — no podías extenderlo ni conectarlo con el sistema operativo, así
que nadie lo usó para trabajar.

Python heredó la legibilidad de ABC y corrigió su error: se diseñó para ser
extensible y para hablar con el resto del mundo. Ese rasgo explica la anomalía
que hoy te afecta directamente: **el stack de IA está escrito en Python siendo
Python un lenguaje lento**. NumPy, PyTorch y compañía no ejecutan Python en el
bucle caliente; ejecutan C, CUDA y Rust. Python es la capa donde un humano
describe *qué* quiere. Es el lenguaje de coordinación, no el de cálculo.

Ten esa idea presente durante toda la ruta: casi nunca vas a escribir Python
rápido. Vas a escribir Python **claro** que orquesta cosas rápidas.

## 2. El Zen como criterio de decisión

Escribe esto en un intérprete:

```python
import this
```

Salen diecinueve aforismos (PEP 20). Leídos como póster de oficina son
perogrulladas. Leídos como criterios de decisión son una herramienta de
ingeniería: deciden qué código pasa una revisión y qué API se considera bien
diseñada. Tres que tienen consecuencias todos los días:

**Explicit is better than implicit.** No prohíbe abstraer; prohíbe la magia
que no puedes rastrear.

```python
# Opaco: ¿de dónde sale `settings`?
from app.config import *

# Rastreable: puedes seguir el hilo hasta la definición
from app.config import settings
```

El criterio no es "poca abstracción", es **rastreabilidad**. Un decorador
visible encima de la función es explícito. Un parche aplicado en otro módulo al
importarse, no.

**Errors should never pass silently. Unless explicitly silenced.**

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

**There should be one obvious way to do it.** Es una declaración de guerra
contra el "cada uno a su manera". Para cada tarea común hay una forma canónica,
y apartarse de ella tiene coste social y técnico.

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

Los dos funcionan. Solo uno pasa una revisión sin comentarios. Y no es
estética: el segundo elimina dos fuentes de bugs — el contador manual y la
condición de parada — y comunica la intención (transformar filtrando) en vez
del mecanismo (iterar mutando).

## 3. Modelo mental 1: todo es un objeto

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
decoradores, los callbacks y media programación funcional. Cuando algo en
Python te parezca magia, la primera pregunta correcta es: **¿qué objeto es esto
y qué atributos tiene?** Casi siempre la magia se disuelve ahí.

## 4. Modelo mental 2: nombres, no cajas

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

## 5. Modelo mental 3: protocolos, no jerarquías

Quien viene de Java pregunta: ¿qué interfaz implementa este objeto? Un
pythonista pregunta: **¿qué métodos especiales define?** El lenguaje entero
está construido sobre protocolos: contratos de métodos `__dunder__` que
cualquier clase puede adoptar sin pedirle permiso a ninguna jerarquía.

| Si tu objeto define… | …habla el protocolo | …y funciona con |
|---|---|---|
| `__len__` | tamaño | `len(x)` |
| `__iter__` / `__next__` | iteración | `for`, comprehensions, `sum`, `max` |
| `__getitem__` | indexación | `x[i]`, slicing |
| `__enter__` / `__exit__` | contexto | `with` |
| `__call__` | invocación | `x(...)` |
| `__eq__`, `__lt__` | comparación | `==`, `sorted`, `min` |

La consecuencia estratégica: tus tipos se integran con la sintaxis del lenguaje
y con toda la biblioteca estándar simplemente **hablando el protocolo
adecuado**. NumPy, Pandas y PyTorch son, vistos así, colecciones enormes de
objetos que hablan los protocolos de aritmética, indexación e iteración — por
eso `matriz_a + matriz_b` y `tensor[mask]` se sienten parte del lenguaje.

## 6. Modelo mental 4: la iteración es la abstracción central

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

## 7. Modelo mental 5: todo nombre vive en un espacio de nombres

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

El valor de este modelo es diagnóstico: convierte los errores más confusos para
quien empieza —`UnboundLocalError`, haber llamado `list` a una variable y romper
la función `list`, atributos "que desaparecen"— en recorridos mecánicos que se
razonan en segundos con `vars()`, `dir()` y `__dict__`.

## 8. Duck typing, EAFP y batteries included

**Duck typing.** Si camina como un pato y grazna como un pato, es un pato. La
pregunta relevante sobre un objeto no es *de qué clase es* sino *qué sabe
hacer*. Una función que necesita algo iterable no debe exigir una `list`:

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

**EAFP frente a LBYL.** Dos formas de tratar lo incierto: mirar antes de saltar
(*Look Before You Leap*) o actuar y pedir perdón (*Easier to Ask Forgiveness
than Permission*).

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

Python prefiere EAFP por dos razones técnicas, no estéticas. La primera es que
elimina condiciones de carrera: entre comprobar que un archivo existe y abrirlo
puede pasar tiempo en el que otro proceso lo borra. `try: open(...)` no tiene
esa ventana; `if os.path.exists(...)` sí. La segunda es que optimiza el camino
feliz: si la clave casi siempre está, evitas una comprobación en cada llamada.

**Batteries included.** Python trae más de doscientos módulos de serie. El
orden correcto de búsqueda ante una necesidad nueva es: (1) biblioteca
estándar, (2) paquete maduro y mantenido, (3) código propio. Invertirlo produce
árboles de dependencias frágiles y proyectos que envejecen mal. Cada
dependencia es un contrato de mantenimiento que firmas con un desconocido.

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
- **`ejercicios/reto/baraja.py`** — hacer que una clase tuya hable los
  protocolos del lenguaje. Sale más corto de lo que esperas.

## Resumen

- Python es la capa donde describes *qué* quieres; lo rápido casi siempre pasa
  por debajo, en C o CUDA.
- El Zen no es decoración: es el árbol de decisión de una revisión de código.
- **Todo es un objeto.** Ante algo que parece magia: ¿qué objeto es y qué
  atributos tiene?
- **Nombres, no cajas.** Varias etiquetas pueden apuntar al mismo objeto; de
  ahí salen los bugs de aliasing y el del argumento mutable por defecto.
- **Protocolos, no jerarquías.** Tus tipos se integran con el lenguaje hablando
  los `__dunder__` adecuados.
- **La iteración es el corazón.** El mismo `for` recorre un texto, un archivo,
  un cursor de base de datos y un stream de LLM.
- **Todo nombre se resuelve en un espacio de nombres**, siguiendo LEGB. Es una
  herramienta de diagnóstico, no un dato de examen.
- EAFP por defecto; LBYL cuando el fallo es frecuente y esperado.

## Preguntas de repaso

1. `a = [1, 2]; b = a; c = a[:]` — después de `b.append(3)`, ¿qué valen `a`,
   `b` y `c`? Explícalo con el modelo de etiquetas, sin ejecutarlo.
2. ¿Por qué `except Exception: pass` es peor que no capturar nada?
3. Una función necesita "algo con lo que iterar". ¿Por qué anotarla como
   `list` es una mala decisión, y qué anotarías en su lugar?
4. Da un caso donde LBYL sea preferible a EAFP y explica por qué.
5. ¿Qué tienen en común un archivo abierto, un cursor de base de datos y la
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

Más enlaces por tema en [`recursos/enlaces/`](../../recursos/enlaces/README.md).

## Siguiente

Módulo 01 · Fundamentos, donde estos modelos se convierten en sintaxis.
