# Módulo 02 · Estructuras de datos

> **Prerrequisitos:** módulo 01<br>
> **Tiempo estimado:** 120 min<br>
> **Si ya dominas esto:** salta al módulo 03

Cuatro estructuras integradas —`list`, `tuple`, `dict`, `set`— cubren el 95% de
lo que necesita un sistema real. La cláusula que decide todo es *bien usadas*.

Este módulo no es un catálogo de métodos. Es sobre cómo están implementadas por
dentro, porque de ahí se deduce qué operación cuesta O(1) y cuál O(n) — y esa
diferencia es la que separa un servicio que escala de uno que se degrada
misteriosamente a las diez mil iteraciones.

## Qué vas a poder hacer al terminar

- Elegir entre list, dict, set y tuple según el caso
- Escribir list comprehensions legibles
- Usar generadores para no cargar todo en memoria

## 1. La lista por dentro: un array, no una lista enlazada

El nombre engaña a quien viene de estructuras de datos clásicas. La `list` de
Python **no** es una lista enlazada: es un array dinámico, un bloque contiguo de
memoria que guarda referencias, con capacidad de sobra reservada para absorber
el crecimiento.

```text
list "orders"  (longitud 5, capacidad 8)
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ ref  │ ref  │ ref  │ ref  │ ref  │  ——  │  ——  │  ——  │
└──┬───┴──┬───┴──┬───┴──┬───┴──┬───┴──────┴──────┴──────┘
   ▼      ▼      ▼      ▼      ▼      (huecos reservados:
  obj    obj    obj    obj    obj      append no realoja todavía)
```

De ese dibujo se deduce la tabla de costes entera, sin memorizarla:

| Operación | Coste | Por qué |
|---|---|---|
| `lst[i]` | O(1) | aritmética de punteros: base + i × tamaño |
| `lst.append(x)` | O(1) amortizado | escribe en el hueco; realoja solo al agotarse |
| `lst.pop()` | O(1) | quita la última referencia |
| `lst.pop(0)`, `lst.insert(0, x)` | **O(n)** | desplaza *todas* las referencias |
| `x in lst` | O(n) | búsqueda lineal: no hay índice por valor |
| `lst[a:b]` | O(b−a) | copia ese rango de referencias |
| `lst.sort()` | O(n log n) | Timsort |
| `len(lst)` | O(1) | la longitud se guarda, no se cuenta |

*Amortizado* merece precisión porque es concepto de diseño, no de examen: cuando
`append` agota la capacidad, Python reserva un bloque mayor y copia todo — esa
llamada concreta es O(n). Pero como el crecimiento es geométrico, las
realocaciones se espacian exponencialmente y el coste medio por operación queda
en O(1). Traducción práctica: construir una lista con `append` en un bucle es
eficiente e idiomático. No necesitas predimensionar nada.

### El antipatrón O(n²) que nadie ve venir

```python
queue = ["job1", "job2", ...]
while queue:
    job = queue.pop(0)   # O(n) CADA VEZ: desplaza toda la lista
    process(job)         # el bucle completo: O(n²)
```

Con mil trabajos es invisible. Con un millón son ~10¹² desplazamientos de
punteros y el servicio "se degrada misteriosamente". La estructura correcta ya
viene de serie:

```python
from collections import deque

queue = deque(jobs)
while queue:
    job = queue.popleft()   # O(1): barata por AMBOS extremos
    process(job)
```

**La regla:** `list` para pila (append/pop del final) y acceso por índice;
`deque` para cola o ventana deslizante. Nunca `pop(0)` ni `insert(0, …)` en
código caliente.

Detrás hay un principio que gobierna todo el módulo: **elegir estructura es
elegir qué patrón de acceso va a ser O(1)**.

## 2. Slicing: el álgebra de las secuencias

```python
data = [10, 20, 30, 40, 50, 60]

data[1:4]    # [20, 30, 40] — el final es EXCLUSIVO: [start, stop)
data[:3]     # [10, 20, 30] — omitir = desde el principio / hasta el final
data[-2:]    # [50, 60]     — índices negativos: desde el final
data[::2]    # [10, 30, 50] — con paso
data[::-1]   # invertida     — el idioma de inversión
data[10:20]  # []            — fuera de rango NO revienta: recorta
```

Que el final sea exclusivo no es un capricho: hace que `len(data[a:b]) == b - a`,
que `data[:k] + data[k:]` reconstruya el original exacto y que la rebanada vacía
se represente sin casos especiales.

Y ojo con estos dos, que se parecen y no son lo mismo:

```python
copia = data[:]        # copia superficial: objeto NUEVO
data[:] = new_values   # muta el objeto EN EL SITIO: todos los alias lo ven
data = new_values      # solo re-vincula ESTE nombre
```

Es el modelo de etiquetas del módulo 00 otra vez, ahora con sintaxis.

## 3. Tuplas: registros, no listas de solo lectura

Presentar la tupla como "una lista que no cambia" pierde su significado. La
distinción que practica la comunidad:

- La **lista** es una secuencia homogénea de longitud variable: *n* cosas del
  mismo tipo. Lo que importa de un elemento es que pertenece, no dónde está.
- La **tupla** es un registro heterogéneo de longitud fija: cada posición
  significa algo. `(lat, lon)`, `(host, port)`. Es un struct anónimo.

De ser inmutable hereda sus superpoderes: es hashable, así que sirve de clave de
diccionario (`precios[("USD", "CRC")]`), se comparte sin copiar y es más barata
que una lista.

El lenguaje está tejido de tuplas implícitas:

```python
point = 9.93, 4.05             # la coma crea la tupla, no los paréntesis
x, y = point                   # unpacking
a, b = b, a                    # el swap canónico
first, *rest = [1, 2, 3, 4]    # unpacking extendido: first=1, rest=[2,3,4]

for i, order in enumerate(orders, start=1): ...

def min_max(xs) -> tuple[float, float]:
    return min(xs), max(xs)    # "retorno múltiple" = devolver UNA tupla

low, high = min_max(data)
```

La esquina clásica: `(1)` es el entero 1 entre paréntesis. La tupla de un
elemento es `(1,)` — el operador es la coma.

Cuando el registro pasa de dos o tres campos, las posiciones desnudas se
vuelven ilegibles (`row[3]`, ¿era el monto o la fecha?). Ahí empieza una escalera
de formalización que recorrerás entera a lo largo de la ruta:

```python
from typing import NamedTuple

class Transfer(NamedTuple):
    origin: str
    destination: str
    amount_cents: int      # dinero como entero de la unidad mínima, nunca float
    currency: str = "CRC"

t = Transfer("CR01-0001", "CR01-0002", 1_500_000)
t.amount_cents                    # acceso por nombre: se documenta solo
t[2]                              # sigue siendo tupla
origin, dest, cents, cur = t      # sigue desempaquetando
```

**tupla → NamedTuple → dataclass (módulo 03) → modelo validado (módulo 07)**.
Elegir el peldaño según cuánta estructura pide el dato es una micro-decisión de
diseño que un revisor con experiencia nota enseguida.

## 4. Ordenar: Timsort, `key` y la estabilidad

Python ordena con Timsort, que tiene tres propiedades de contrato: O(n log n) en
el peor caso, **O(n) sobre datos ya casi ordenados** (el caso más frecuente de
la vida real: logs por fecha, exports de base de datos) y **estabilidad** — los
elementos iguales conservan su orden relativo.

```python
orders.sort()     # muta la lista y devuelve None
sorted(orders)    # devuelve una lista nueva y acepta cualquier iterable
```

La pieza profesional es `key`: una función que extrae de cada elemento el valor
por el que ordenar. Se llama una sola vez por elemento.

```python
from operator import attrgetter, itemgetter

transfers.sort(key=lambda t: t.amount_cents)
transfers.sort(key=attrgetter("currency", "amount_cents"))  # multiclave sin lambda
rows.sort(key=itemgetter(2))                                # por columna
names.sort(key=str.casefold)                                # orden correcto sin mayúsculas
```

Y un idioma que solo funciona *porque* Timsort es estable: para ordenar por
varios criterios con direcciones distintas, se ordena en pasadas sucesivas, de
la clave menos importante a la más importante.

```python
transfers.sort(key=attrgetter("amount_cents"), reverse=True)  # criterio secundario
transfers.sort(key=attrgetter("currency"))                    # criterio principal
# resultado: por divisa ascendente y, dentro de cada divisa, por monto descendente
```

## 5. Diccionarios con criterio

La diferencia entre usar dicts y dominarlos está en un puñado de métodos que
codifican patrones enteros.

```python
config = {"host": "db.internal", "port": 5432}

config["timeout"]                  # KeyError — correcto si faltar es un BUG
config.get("timeout")              # None    — correcto si faltar es NORMAL
config.get("timeout", 30)          # default, sin tocar el dict
config.setdefault("timeout", 30)   # default Y lo inserta

defaults | file_cfg | cli_args     # dict nuevo; a igual clave gana la derecha
{r["ref"]: r for r in records}     # dict comprehension
dict(zip(headers, row))            # dos secuencias paralelas → dict
```

Elegir dentro de esa tríada de lectura es **semántico, no estilístico**.
`d[k]` afirma "esta clave tiene que estar; si no, quiero el error ahora mismo".
`.get` afirma "que falte es un caso normal del dominio". Usar `.get` por reflejo
convierte bugs de datos en `None` que viajan tres capas y estallan como un
`AttributeError` incomprensible.

Las vistas (`keys()`, `values()`, `items()`) no son listas: son ventanas vivas
sobre el dict. Y las de claves se comportan como conjuntos:

```python
current.keys() - previous.keys()   # claves añadidas, sin un solo bucle

for k in list(d):        # iterar sobre una COPIA de las claves...
    if expired(d[k]):
        del d[k]         # ...porque borrar mientras iteras la vista viva revienta
```

Tres subclases de `collections` eliminan otros tantos rituales:

```python
from collections import defaultdict, Counter

by_currency = defaultdict(list)
for t in transfers:
    by_currency[t.currency].append(t)     # sin el "si no está, créala"

levels = Counter(entry.level for entry in logs)
levels.most_common(3)                     # [('INFO', 8412), ('WARN', 312), ...]
```

## 6. Conjuntos: la matemática que borra bucles

Un `set` es la misma tabla hash del dict sin la columna de valores: pertenencia,
inserción y borrado O(1) de media, elementos únicos, sin orden garantizado.

Su valor no es "quitar duplicados". Es que **sustituye categorías enteras de
bucles por álgebra**:

```python
bank_refs = {m["ref"] for m in bank_moves}
internal_refs = {r["ref"] for r in internal}

matched       = bank_refs & internal_refs   # en ambos lados
only_bank     = bank_refs - internal_refs   # sin contraparte interna
only_internal = internal_refs - bank_refs
discrepancies = bank_refs ^ internal_refs   # en exactamente uno de los dos

required_fields <= set(payload)             # ¿están todos los campos? ⊆
user_perms >= required_perms                # un sistema de autorización en una línea
```

Compara `only_bank` con el doble bucle que haría lo mismo: un carácter frente a
seis líneas O(n·m). Cuando un problema se deja formular como teoría de
conjuntos, la implementación desaparece.

Los reflejos que deberías tener: deduplicar (`set(xs)`; si el orden importa,
`list(dict.fromkeys(xs))`), pertenencia en código caliente (`x in conjunto` es
O(1), `x in lista` es O(n)) y relaciones entre colecciones.

El trade-off honesto: los contenedores hash compran tiempo con memoria, y no dan
orden ni rangos. Acceso por identidad exacta → hash. Acceso por rango u orden →
secuencia ordenada. Las dos cosas a escala → eso ya es un índice de base de
datos.

## 7. Comprehensions y generadores

Una comprehension comunica *qué* quieres; un bucle comunica *cómo* lo obtienes.

```python
squares = [n * n for n in range(10) if n % 2 == 0]     # list
by_ref = {r["ref"]: r for r in records}                # dict
refs = {r["ref"] for r in records}                     # set
```

El límite es la legibilidad: si necesitas dos `for` anidados y dos condiciones,
un bucle normal se lee mejor. La comprehension no es un deporte.

Cambia los corchetes por paréntesis y tienes otra cosa completamente distinta:

```python
total = sum(t.amount_cents for t in transfers)   # generator expression
```

Eso no construye ninguna lista intermedia. Produce los valores de uno en uno, a
demanda. Con un millón de transferencias, la versión con corchetes reserva
memoria para el millón; esta usa memoria constante.

Y con `yield` escribes tus propios flujos perezosos:

```python
from pathlib import Path

def error_lines(logs_dir: str | Path):
    """Va soltando las líneas con ERROR de todos los .log del directorio."""
    for path in Path(logs_dir).glob("*.log"):
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if "ERROR" in line:
                    yield line.rstrip()

worst = max(error_lines("/var/log/app"), key=len)
```

Ocho líneas que procesan gigabytes con memoria constante, cierran cada archivo
de forma determinista y componen con `max` sin materializar nada. Es el modelo
mental 4 del módulo 00 convertido en herramienta.

## Caso real

Un equipo financiero concilia cada noche los movimientos del banco contra los
registros internos: hay que decir qué cuadra, qué está solo en el banco y qué
está solo dentro. La primera versión que escribió alguien, con prisa:

```python
matched = []
only_bank = []
for movement in bank_moves:               # n
    found = False
    for record in internal:               # × m  → O(n·m)
        if movement["ref"] == record["ref"]:
            found = True
            break
    if found:
        matched.append(movement["ref"])
    else:
        only_bank.append(movement["ref"])
```

Con 3.000 movimientos por lado corría en un segundo y nadie lo miró. Al crecer
el negocio a 300.000, el proceso pasó de un segundo a más de dos horas: el
trabajo no creció 100 veces, creció 10.000. Es la curva de O(n·m).

La versión con la maquinaria correcta no es más rápida por ser más lista, sino
porque cambia la pregunta a una que la tabla hash responde en O(1):

```python
bank_refs = {m["ref"] for m in bank_moves}
internal_refs = {r["ref"] for r in internal}

reporte = {
    "matched": bank_refs & internal_refs,
    "only_bank": bank_refs - internal_refs,
    "only_internal": internal_refs - bank_refs,
}
```

Tres líneas, O(n + m), y además las tres claves del diccionario son exactamente
las tres secciones del informe que recibe el equipo. Ese es el ejercicio
`conciliacion` que vas a escribir.

## Ejercicios

```bash
uv run pytest ruta/02-estructuras-de-datos
```

- **`ejercicios/base/conciliacion.py`** — el caso real de arriba, con álgebra de
  conjuntos.
- **`ejercicios/base/agrupar.py`** — agrupar registros por una clave sin el
  ritual de "si no está, créala".
- **`ejercicios/reto/flujo.py`** — un generador que trocea cualquier iterable
  sin materializarlo. Aquí se comprueba si entendiste la pereza.

## Resumen

- La `list` es un array dinámico: índice y `append` son O(1); `pop(0)` es O(n).
  Para cola, `deque`.
- Elegir estructura es elegir qué acceso será O(1).
- El slicing tiene el final exclusivo por razones de álgebra, no de gusto.
  `data[:] = x` muta; `data = x` re-vincula.
- La tupla es un registro de longitud fija, no una lista congelada. Sube por la
  escalera tupla → NamedTuple → dataclass → modelo validado según haga falta.
- Timsort es estable, y esa garantía habilita el idioma de ordenar en pasadas.
- `d[k]` frente a `.get(k)` es una decisión semántica: ¿faltar es un bug o es
  parte del dominio?
- Los conjuntos convierten bucles en álgebra. Si el problema se deja escribir
  como intersección y diferencia, ya está resuelto.
- Corchetes construyen en memoria; paréntesis producen a demanda.

## Preguntas de repaso

1. Tienes una lista de un millón de elementos y necesitas ir sacando del
   principio. ¿Qué pasa y qué usarías?
2. `data[:] = otra` y `data = otra`. ¿En qué se diferencian para alguien que
   tenga otro nombre apuntando a `data`?
3. ¿Por qué `(1)` no es una tupla y `(1,)` sí?
4. Necesitas ordenar por divisa ascendente y, dentro de cada divisa, por monto
   descendente. ¿Cómo lo consigues y qué propiedad de Timsort lo permite?
5. ¿Cuándo es un error usar `.get()` en lugar de `d[clave]`?
6. Escribe en una línea "las referencias que están en el banco pero no en los
   registros internos".
7. `sum([x * 2 for x in datos])` y `sum(x * 2 for x in datos)` dan el mismo
   número. ¿En qué se diferencian con diez millones de datos?

## Recursos

- [Estructuras de datos — tutorial oficial](https://docs.python.org/es/3/tutorial/datastructures.html)
  — `doc-oficial` · `es` · `principiante`. En español y con los idiomas
  canónicos.
- [TimeComplexity — wiki de Python](https://wiki.python.org/moin/TimeComplexity)
  — `doc-oficial` · `en` · `intermedio`. La tabla de costes de cada operación
  de cada estructura. Consulta obligada cuando algo va lento.
- [`collections` — la documentación del módulo](https://docs.python.org/es/3/library/collections.html)
  — `doc-oficial` · `es` · `intermedio`. `deque`, `defaultdict`, `Counter`.

## Siguiente

Módulo 03 · POO y módulos, donde estos datos empiezan a tener comportamiento.
