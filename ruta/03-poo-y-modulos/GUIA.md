# Módulo 03 · POO y módulos

> **Prerrequisitos:** módulos 01-02<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 04

Hasta aquí has movido datos. Este módulo va de darles comportamiento y de
organizar el resultado en archivos que no se conviertan, con el tiempo, en ese
`utils.py` de mil ochocientas líneas que todo el mundo importa y nadie entiende.

Son dos temas en uno porque en la práctica van juntos: las clases definen las
piezas, y los módulos deciden quién puede ver a quién.

## Qué vas a poder hacer al terminar

- Definir clases con estado y comportamiento
- Elegir entre método de instancia, de clase y estático
- Encapsular con propiedades en vez de getters y setters
- Usar herencia cuando toca, y composición cuando toca más
- Leer un MRO y saber por qué existe
- Definir contratos con ABCs y con Protocol
- Escribir funciones recursivas sobre estructuras anidadas
- Usar dataclasses para estructuras de datos
- Organizar código en módulos y paquetes

## 1. Una clase es estado con comportamiento

```python
class Account:
    """Una cuenta con saldo. El dinero, en céntimos y como entero."""

    def __init__(self, holder: str, balance_cents: int = 0) -> None:
        self.holder = holder
        self.balance_cents = balance_cents

    def deposit(self, cents: int) -> None:
        if cents <= 0:
            raise ValueError("el depósito debe ser positivo")
        self.balance_cents += cents
```

Dos cosas que llaman la atención a quien viene de Java o C#:

**`self` es explícito.** No es una carencia del lenguaje: es el aforismo
*explicit is better than implicit* aplicado. En Python, `metodo(self, x)` deja
ver que la instancia es un argumento como cualquier otro — y de hecho puedes
llamarlo así: `Account.deposit(mi_cuenta, 500)`.

**No hay `private`.** La convención es un guion bajo delante: `_saldo` significa
"esto es interno, si lo tocas asumes el riesgo". Python confía en el
programador en vez de poner barandillas. Suena ingenuo hasta que llevas un
tiempo: los lenguajes con `private` estricto acaban llenos de getters y setters
que no protegen nada.

Existe además el **doble** guion bajo (`__saldo`), que activa el *name
mangling*: el atributo pasa a llamarse `_Account__saldo` por dentro. No es
privacidad, es evitar colisiones accidentales en jerarquías de herencia. Se usa
poco y con criterio.

### Dinero: nunca en `float`

Fíjate en `balance_cents`. `0.1 + 0.2` no vale `0.3` en ningún lenguaje que use
IEEE 754, Python incluido. Para dinero: enteros de la unidad mínima o
`decimal.Decimal`. Nunca `float`. Es de los errores que más caro salen y de los
más fáciles de evitar.

## 2. Tres clases de método

```python
class Transfer:
    MONTO_MAXIMO = 10_000_000          # atributo de clase: uno para todas

    def __init__(self, origin: str, amount_cents: int) -> None:
        self.origin = origin
        self.amount_cents = amount_cents

    def describe(self) -> str:                    # de INSTANCIA
        return f"{self.origin}: {self.amount_cents}"

    @classmethod
    def from_dict(cls, payload: dict) -> "Transfer":   # de CLASE
        return cls(payload["origin"], payload["amount_cents"])

    @staticmethod
    def is_valid_amount(cents: int) -> bool:      # ESTÁTICO
        return 0 < cents <= Transfer.MONTO_MAXIMO
```

- **De instancia**: recibe `self`. Necesita los datos de *este* objeto. Es el
  caso normal.
- **De clase**: recibe `cls`, la clase misma. El uso canónico es el
  **constructor alternativo**: `Transfer.from_dict(payload)`. Y como recibe
  `cls` y no `Transfer` a pelo, funciona bien con herencia — una subclase
  obtiene instancias de la subclase, no de la base.
- **Estático**: no recibe nada especial. Es una función normal que vive dentro
  de la clase porque conceptualmente pertenece ahí.

Si un método estático no usa nada de la clase, plantéate si no debería ser una
función del módulo. A veces sí (agrupa bien); a veces es una función disfrazada.

## 3. Los atributos viven en diccionarios

Cuando escribes `cuenta.holder`, Python busca en `cuenta.__dict__`, luego en
`Account.__dict__`, luego en sus clases base. Es el modelo mental 5 del módulo
00 aplicado a atributos: no hay magia, hay un recorrido.

```python
cuenta = Account("Ana", 1000)
cuenta.__dict__          # {'holder': 'Ana', 'balance_cents': 1000}
Account.__dict__.keys()  # los métodos viven aquí, no en la instancia
```

De ese modelo se deduce una trampa clásica:

```python
class Basket:
    items = []          # ← atributo de CLASE: uno solo, compartido por todas

    def add(self, item):
        self.items.append(item)

a, b = Basket(), Basket()
a.add("pan")
b.items                 # ['pan']  ← el carrito de a
```

Es el mismo bug del argumento mutable por defecto del módulo 00, con otro
disfraz. La cura es la misma: crear el objeto por instancia, en `__init__`.

## 4. Propiedades: encapsular sin ceremonia

En muchos lenguajes, exponer un atributo público es un compromiso irreversible:
si mañana necesitas validar, tienes que cambiar la API a `getSaldo()` y romper a
todo el mundo. En Python no:

```python
class Account:
    def __init__(self, balance_cents: int = 0) -> None:
        self._balance_cents = balance_cents

    @property
    def balance_cents(self) -> int:
        return self._balance_cents

    @balance_cents.setter
    def balance_cents(self, value: int) -> None:
        if value < 0:
            raise ValueError(f"el saldo no puede ser negativo: {value}")
        self._balance_cents = value

cuenta = Account()
cuenta.balance_cents = 500      # pasa por el setter y valida
cuenta.balance_cents            # pasa por el getter
cuenta.balance_cents = -1       # ValueError
```

Quien usa la clase escribe `cuenta.balance_cents` exactamente igual que antes.
La propiedad convierte un atributo en un par de métodos **sin cambiar la
sintaxis de uso**.

De ahí la regla cultural: **empieza con un atributo público normal**. Si algún
día necesitas validar o calcular, lo conviertes en propiedad y nadie se entera.
Escribir getters y setters "por si acaso", como en Java, es ceremonia que en
Python no compra nada.

Las propiedades también sirven para **valores derivados**:

```python
@property
def amount(self) -> float:
    return self.amount_cents / 100      # se lee como dato, se calcula al vuelo
```

## 5. Dataclasses: declarar en vez de ceremoniar

Muchas clases existen solo para agrupar datos. Escribir a mano su `__init__`,
su `__repr__` y su `__eq__` es ceremonia repetitiva y una fuente de bugs.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Transfer:
    origin: str
    destination: str
    amount_cents: int
    currency: str = "CRC"
    tags: list[str] = field(default_factory=list)   # mutable: SIEMPRE así

    def __post_init__(self) -> None:
        if self.amount_cents <= 0:
            raise ValueError("el monto debe ser positivo")

t = Transfer("CR01-0001", "CR01-0002", 1_500_000)
t                       # Transfer(origin='CR01-0001', ..., currency='CRC')
t == Transfer("CR01-0001", "CR01-0002", 1_500_000)   # True: compara por valor
```

Cuatro piezas que conviene entender, no copiar:

- **`frozen=True`** hace la instancia inmutable. Ganas hashabilidad (sirve de
  clave de dict, entra en un `set`) y la tranquilidad de que nadie la modifica
  a tus espaldas. Es el valor por defecto que deberías querer para datos que
  viajan.
- **`slots=True`** cambia el `__dict__` por ranuras fijas: menos memoria y
  acceso más rápido, a cambio de no poder añadir atributos nuevos al vuelo.
- **`field(default_factory=list)`** es la forma correcta de dar un valor por
  defecto mutable. Poner `tags: list = []` directamente da error, precisamente
  porque el lenguaje aprendió del bug del argumento mutable.
- **`__post_init__`** es donde valida un dataclass. Sin él, `frozen` te protege
  de cambios pero no de nacer mal.

Esto continúa la escalera del módulo 02: **tupla → NamedTuple → dataclass →
modelo validado**. La dataclass es el peldaño donde el dato empieza a tener
comportamiento propio. El siguiente, Pydantic, lo verás en el módulo 07: es lo
que se usa en la *frontera* del sistema, donde los datos llegan de fuera y no
te puedes fiar.

## 6. Los protocolos, ahora en tus clases

El módulo 00 decía que tus tipos se integran con el lenguaje hablando
`__dunder__`. Aquí lo aplicas:

```python
class Money:
    def __init__(self, cents: int, currency: str = "CRC") -> None:
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({self.cents}, {self.currency!r})"

    def __str__(self) -> str:
        return f"{self.cents / 100:,.2f} {self.currency}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.cents, self.currency) == (other.cents, other.currency)

    def __hash__(self) -> int:
        return hash((self.cents, self.currency))

    def __lt__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return self.cents < other.cents

    def __add__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(self.cents + other.cents, self.currency)
```

Con esos métodos, `Money` ya funciona con `==`, `sorted()`, `min()`, `max()` y
`+`. No heredó de nada: habla los protocolos.

Tres detalles que separan una implementación correcta de una aproximada:

**`__repr__` frente a `__str__`.** El primero es para quien programa —debería
poder pegarse en un intérprete y reconstruir el objeto— y el segundo para quien
lee la salida. Si solo defines uno, que sea `__repr__`: `str()` cae en él
cuando no hay `__str__`.

**Devolver `NotImplemented`** (que no es `NotImplementedError`) es la forma
correcta de decir "yo no sé comparar con eso": Python entonces le pregunta al
otro operando, y si tampoco sabe, lanza `TypeError` con un mensaje claro. Es lo
que hace que `==` con algo raro dé `False` mientras `<` levanta `TypeError`.

**Definir `__eq__` borra el `__hash__` heredado.** Si tu objeto es inmutable de
hecho, defínelo tú; si no, quedará como no hashable y no entrará en un `set`.

## 7. Herencia, `super()` y el MRO

La herencia sirve para *es un*: `AdminUser` es un `User`.

```python
class Account:
    def __init__(self, holder: str, balance_cents: int = 0) -> None:
        self.holder = holder
        self.balance_cents = balance_cents

    def describe(self) -> str:
        return f"{self.holder}: {self.balance_cents}"


class SavingsAccount(Account):
    def __init__(self, holder: str, balance_cents: int = 0, rate: float = 0.02):
        super().__init__(holder, balance_cents)     # ← inicializa la parte de arriba
        self.rate = rate

    def describe(self) -> str:
        return f"{super().describe()} (ahorro al {self.rate:.1%})"
```

`super()` no significa "la clase padre": significa "el siguiente en el orden de
resolución". Con herencia simple coinciden; con múltiple, no, y la diferencia
importa.

### El MRO

Cuando hay varias clases base, el orden en que Python busca un método se llama
**MRO** (*Method Resolution Order*) y **se consulta, no se adivina**:

```python
SavingsAccount.__mro__
# (SavingsAccount, Account, object)
```

La regla que aplica Python (linearización C3) garantiza que una clase siempre
aparece antes que sus bases y que se respeta el orden en que las declaraste. La
consecuencia práctica: si necesitas dibujar tu jerarquía en una pizarra para
entender de dónde sale un método, **la jerarquía está mal**.

### Herencia frente a composición

```python
# Herencia: frágil si se usa para reutilizar código
class ReportWithCache(Report, CacheMixin, LoggerMixin): ...

# Composición: cada pieza se sustituye y se prueba por separado
class Report:
    def __init__(self, cache: Cache, logger: Logger) -> None:
        self._cache = cache
        self._logger = logger
```

La regla práctica: hereda cuando el subtipo pueda **sustituir** al padre en
cualquier sitio sin sorpresas (es el principio de sustitución de Liskov). Si
heredas solo para no repetir código, casi siempre querías composición.

Y la pregunta que lo resuelve casi siempre: ¿mi clase **es un** X, o **tiene un**
X? Un `ReportWithCache` no es un tipo distinto de informe: es un informe que
tiene una caché.

## 8. Contratos explícitos: ABC y Protocol

Duck typing dice "si sabe hacerlo, sirve". A veces quieres declarar el contrato:

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, ref: str) -> dict | None: ...

    @abstractmethod
    def save(self, item: dict) -> None: ...

class InMemoryRepository(Repository):
    ...    # si olvidas implementar un abstractmethod, falla al instanciar
```

Una **ABC** es herencia nominal: hay que heredar de ella explícitamente. Da
garantías fuertes (no puedes instanciar una implementación incompleta) al precio
de acoplar tus clases a la jerarquía.

La alternativa moderna es **`Protocol`**, que es duck typing verificable:

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, ref: str) -> dict | None: ...
    def save(self, item: dict) -> None: ...
```

Cualquier clase con esos dos métodos **encaja**, sin heredar de nada y sin
saber que el protocolo existe. El verificador de tipos lo comprueba en
desarrollo. Es lo que querrás casi siempre para definir las fronteras de tu
sistema: das el contrato sin imponer la herencia.

## 9. Recursión: funciones que se llaman a sí mismas

Una función recursiva se define en términos de sí misma, y necesita dos cosas
para no ser un bucle infinito: un **caso base** que no recurre y una llamada que
se acerca a él.

```python
def factorial(n: int) -> int:
    if n <= 1:            # caso base
        return 1
    return n * factorial(n - 1)
```

Dónde se paga de verdad no es en los factoriales —ahí un bucle se lee mejor—
sino en las **estructuras anidadas**, donde la forma del problema es recursiva:

```python
def total_size(node: dict) -> int:
    """Suma el tamaño de un árbol de carpetas anidadas."""
    if "size" in node:                        # es un archivo
        return node["size"]
    return sum(total_size(hijo) for hijo in node["children"])
```

Un bucle tendría que gestionar una pila a mano; la recursión deja que la use el
lenguaje. Ese es el criterio: **si el dato es recursivo, el código quiere serlo**.

Dos avisos: Python tiene un límite de profundidad (unas mil llamadas por
defecto), y no optimiza la recursión de cola. Para árboles de datos normales
sobra; para recorrer un millón de niveles, no.

## 10. Qué pasa exactamente en un `import`

`import billing` hace cuatro cosas, en este orden:

1. **Mira la caché** `sys.modules`. Si ya está, se acabó: devuelve ese objeto.
2. **Localiza** el archivo recorriendo `sys.path`.
3. **Registra** el módulo en la caché.
4. **Ejecuta el archivo entero, una sola vez**, y vincula el nombre.

De ahí se deducen tres consecuencias que explican casi todas las dudas sobre
imports:

- Un módulo es un **singleton**: se ejecuta una vez por proceso, por muchas
  veces que lo importes.
- En el nivel superior de un módulo se **define**, no se actúa. Si abres una
  conexión ahí, se abrirá al importar, aunque quien importe solo quisiera una
  constante.
- Editar un archivo no cambia nada en un proceso ya arrancado. Recargar es
  reiniciar.

### Los dos roles de un archivo

```python
def main() -> None:
    ...

if __name__ == "__main__":
    main()
```

`__name__` vale `"__main__"` cuando el archivo se ejecuta directamente y el
nombre del módulo cuando se importa. Ese `if` permite que un archivo sea
biblioteca y programa a la vez sin que importarlo dispare nada.

Ejecuta con `python -m paquete.modulo` en vez de `python ruta/al/archivo.py`:
el primero resuelve los imports desde la raíz del proyecto y evita la clase de
bugs donde editas un archivo y "no cambia nada" porque se estaba importando
otro con el mismo nombre.

### Paquetes y fachada

Un paquete es una carpeta con `__init__.py`. Ese archivo es la **fachada**: lo
que expone es la API pública, y `__all__` la declara explícitamente.

```python
# billing/__init__.py
from billing.money import format_crc
from billing.accounts import validate_iban

__all__ = ["format_crc", "validate_iban"]
```

Con eso, quien te consume escribe `from billing import format_crc` y tú puedes
reorganizar los archivos internos sin romperle nada. Mantén el `__init__.py`
barato: si importa medio mundo, todo el que toque el paquete paga ese coste.

### Imports circulares: tres curas, en orden

`a` importa `b` y `b` importa `a`. Un ciclo no es un problema de sintaxis: es
un **diagnóstico de diseño**.

1. **Extraer el concepto común** a un tercer módulo. Es la cura correcta: el
   ciclo aparecía porque había una idea sin nombre repartida entre los dos.
2. **`TYPE_CHECKING`** si el ciclo existe solo por las anotaciones de tipo. Es
   idiomático y no tiene coste en ejecución:
   ```python
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from billing.accounts import Account
   ```
3. **Import diferido** dentro de la función. Funciona, y huele: esconde el
   grafo de dependencias dentro de cuerpos de funciones. Vale como táctica para
   hoy, nunca como estado final.

### La estructura de un proyecto

```text
mi-servicio/
├── pyproject.toml      ← metadatos, dependencias y config de herramientas
├── src/
│   └── billing/        ← el paquete real
│       └── __init__.py
├── tests/
└── README.md
```

El `src/` no es decoración. Sin él, `import billing` desde la raíz encuentra la
carpeta local aunque el paquete no esté bien instalado: tus tests pasan contra
algo que no es lo que se distribuye. Con `src/`, el import solo puede resolver
contra el paquete instalado, así que los tests ejercitan exactamente lo que
recibirá quien lo use.

## Caso real

Dos años después de arrancar, `utils.py` tiene 1.800 líneas: formateo de
montos, validación de cuentas, reintentos HTTP, cálculo de días hábiles y tres
funciones que ya no llama nadie. Todo el mundo importa `utils`; `utils` importa
de medio proyecto; los ciclos se parchean con imports dentro de funciones.

El coste es medible: cada test arrastra 1.800 líneas y sus dependencias, cada
merge colisiona en el mismo archivo, y nadie distingue qué es API pública de
qué es interno.

El desmontaje, en cuatro pasos:

1. **Cartografiar.** `grep -r "from utils import"` da la lista real de
   consumidores. Los nombres se agrupan **por dominio, no por tipo técnico**:
   `money.py`, `accounts.py`, `http_retry.py`, `bizdays.py`.
2. **Extraer con fachada.** Nacen los módulos nuevos y `utils.py` se queda una
   temporada reexportando lo que movimos, con un `DeprecationWarning`. Así
   nadie rompe el día uno y la migración es incremental.
3. **Romper los ciclos por diseño.** Con los dominios separados, las
   dependencias se vuelven direccionales. Los ciclos que sobreviven señalan un
   concepto todavía sin extraer.
4. **Sellar la dirección.** Un test de arquitectura declara qué capa puede
   importar a cuál y falla el CI si alguien reintroduce un ciclo. La
   arquitectura pasa de acuerdo oral a contrato ejecutable.

La moraleja se generaliza: `utils`, `helpers`, `common` y `misc` son nombres
que no significan nada, **y por eso lo atraen todo**. Un módulo se nombra por
su dominio. Si no puedes nombrar qué agrupa, todavía no sabes qué es — y el
archivo te lo va a confesar creciendo sin límite.

## Ejercicios

```bash
uv run pytest ruta/03-poo-y-modulos
```

- **`ejercicios/base/cuenta.py`** — una clase con estado, comportamiento y
  errores de dominio.
- **`ejercicios/base/transferencia.py`** — una dataclass inmutable que se
  valida al nacer.
- **`ejercicios/base/propiedad.py`** — encapsular con `@property`, incluida la
  validación en el setter y un valor derivado.
- **`ejercicios/reto/dinero.py`** — hacer que tu tipo hable los protocolos de
  comparación y aritmética.
- **`ejercicios/reto/herencia.py`** — una jerarquía pequeña con `super()`, y
  leer su MRO.
- **`ejercicios/reto/recorrer.py`** — recursión sobre una estructura anidada.

## Resumen

- `self` explícito y sin `private`: Python prefiere convenciones a barandillas.
  El doble guion bajo no es privacidad, es evitar colisiones.
- El dinero va en enteros de la unidad mínima o en `Decimal`. Nunca en `float`.
- Métodos de instancia para el objeto, de clase para constructores
  alternativos, estáticos para lo que pertenece conceptualmente.
- Los atributos se resuelven recorriendo diccionarios: instancia, clase, bases.
  Un mutable como atributo de clase se comparte entre todas las instancias.
- Empieza con atributos públicos; conviértelos en `@property` el día que
  necesites validar. Nadie que use tu clase se entera.
- `@dataclass(frozen=True, slots=True)` te da `__init__`, `__repr__` y `__eq__`
  gratis; `field(default_factory=...)` para los mutables; `__post_init__` valida.
- `__repr__` es para quien programa; `__str__` para quien lee la salida.
- Devuelve `NotImplemented` (no `NotImplementedError`) cuando tu dunder no sabe
  operar con el otro tipo. Y define `__hash__` si defines `__eq__`.
- `super()` significa "el siguiente del MRO", no "mi padre". El MRO se consulta
  con `__mro__`.
- Hereda para *es un*; compón para *tiene un*. Heredar para reutilizar código
  suele ser composición mal hecha.
- ABC impone herencia y da garantías fuertes; `Protocol` da el contrato sin
  imponer nada. Para fronteras, `Protocol`.
- Si el dato es recursivo, el código quiere serlo. Caso base primero.
- Importar es: caché → localizar → registrar → ejecutar una vez → vincular.
- Un ciclo de imports es un diagnóstico de diseño. Cura correcta: extraer el
  concepto común.
- Un módulo se nombra por su dominio. `utils` no es un dominio.

## Preguntas de repaso

1. ¿Por qué `items = []` dentro del cuerpo de una clase casi nunca es lo que
   querías?
2. ¿Cuándo usarías un `@classmethod` en vez de un `@staticmethod`?
3. Empiezas con `self.saldo` público y meses después necesitas validar. ¿Qué
   tienes que cambiar en el código de quien usa tu clase?
4. ¿Qué te da `frozen=True` además de impedir asignaciones?
5. ¿Por qué `tags: list = []` en una dataclass da error?
6. ¿Cuál es la diferencia entre devolver `NotImplemented` y lanzar
   `NotImplementedError` desde un `__eq__`?
7. Defines `__eq__` y tu objeto deja de entrar en un `set`. ¿Qué pasó?
8. ¿Qué diferencia hay entre `__repr__` y `__str__`, y cuál definirías si solo
   pudieras elegir uno?
9. `super()` en una jerarquía con dos bases: ¿a cuál llama?
10. Un compañero hereda de `Report` para reutilizar tres métodos, pero
    `CachedReport` no puede sustituir a `Report` en todos los sitios. ¿Qué le
    propondrías?
11. ¿Cuándo eliges `Protocol` en vez de una ABC?
12. Importas el mismo módulo desde tres archivos distintos. ¿Cuántas veces se
    ejecuta su código de nivel superior?
13. Tienes un ciclo de imports que existe solo porque una anotación de tipo
    menciona la otra clase. ¿Cuál de las tres curas aplicas?

## Recursos

- [Clases — tutorial oficial](https://docs.python.org/es/3/tutorial/classes.html)
  — `doc-oficial` · `es` · `principiante`. El modelo de objetos explicado por
  quienes lo diseñaron.
- [`dataclasses` — documentación](https://docs.python.org/es/3/library/dataclasses.html)
  — `doc-oficial` · `es` · `intermedio`. Todos los parámetros del decorador,
  con lo que hace cada uno.
- [Descriptor HowTo](https://docs.python.org/es/3/howto/descriptor.html) —
  `doc-oficial` · `es` · `avanzado`. Explica qué hay debajo de `@property` y de
  los métodos. Denso y revelador.
- [`typing.Protocol`](https://docs.python.org/es/3/library/typing.html#typing.Protocol)
  — `doc-oficial` · `es` · `intermedio`. Duck typing verificable.
- [El sistema de imports](https://docs.python.org/es/3/reference/import.html)
  — `doc-oficial` · `es` · `avanzado`. Denso, pero es la referencia cuando un
  import hace algo que no esperabas.

## Siguiente

Módulo 04 · Entorno y herramientas, donde este proyecto pasa a tener forma
profesional.
