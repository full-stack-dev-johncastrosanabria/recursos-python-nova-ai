# Módulo 03 · POO y módulos

> **Prerrequisitos:** módulos 01-02<br>
> **Tiempo estimado:** 120 min<br>
> **Si ya dominas esto:** salta al módulo 04

Hasta aquí has movido datos. Este módulo va de darles comportamiento y de
organizar el resultado en archivos que no se conviertan, con el tiempo, en ese
`utils.py` de mil ochocientas líneas que todo el mundo importa y nadie entiende.

Son dos temas en uno porque en la práctica van juntos: las clases definen las
piezas, y los módulos deciden quién puede ver a quién.

## Qué vas a poder hacer al terminar

- Definir clases con estado y comportamiento
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

### Dinero: nunca en `float`

Fíjate en `balance_cents`. `0.1 + 0.2` no vale `0.3` en ningún lenguaje que use
IEEE 754, Python incluido:

```python
>>> 0.1 + 0.2
0.30000000000000004
```

Para dinero: enteros de la unidad mínima (céntimos) o `decimal.Decimal`. Nunca
`float`. Es de los errores que más caro salen y de los más fáciles de evitar.

## 2. Los atributos viven en diccionarios

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

## 3. Dataclasses: declarar en vez de ceremoniar

Muchas clases existen solo para agrupar datos. Escribir a mano su `__init__`,
su `__repr__` y su `__eq__` es ceremonia repetitiva y una fuente de bugs.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Transfer:
    origin: str
    destination: str
    amount_cents: int
    currency: str = "CRC"

    def __post_init__(self) -> None:
        if self.amount_cents <= 0:
            raise ValueError("el monto debe ser positivo")

t = Transfer("CR01-0001", "CR01-0002", 1_500_000)
t                       # Transfer(origin='CR01-0001', ..., currency='CRC')
t == Transfer("CR01-0001", "CR01-0002", 1_500_000)   # True: compara por valor
```

Tres parámetros que conviene entender, no copiar:

- **`frozen=True`** hace la instancia inmutable. Ganas hashabilidad (sirve de
  clave de dict, entra en un `set`) y la tranquilidad de que nadie la modifica
  a tus espaldas. Es el valor por defecto que deberías querer para datos que
  viajan.
- **`slots=True`** cambia el `__dict__` por ranuras fijas: menos memoria y
  acceso más rápido, a cambio de no poder añadir atributos nuevos al vuelo.
- **`__post_init__`** es donde valida un dataclass. Sin él, `frozen` te protege
  de cambios pero no de nacer mal.

Esto continúa la escalera del módulo 02: **tupla → NamedTuple → dataclass →
modelo validado**. La dataclass es el peldaño donde el dato empieza a tener
comportamiento propio. El siguiente, Pydantic, lo verás en el módulo 07: es lo
que se usa en la *frontera* del sistema, donde los datos llegan de fuera y no
te puedes fiar.

## 4. Los protocolos, ahora en tus clases

El módulo 00 decía que tus tipos se integran con el lenguaje hablando
`__dunder__`. Aquí lo aplicas:

```python
class Money:
    def __init__(self, cents: int, currency: str = "CRC") -> None:
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({self.cents}, {self.currency!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.cents, self.currency) == (other.cents, other.currency)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return self.cents < other.cents

    def __add__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(self.cents + other.cents, self.currency)
```

Con esos cuatro métodos, `Money` ya funciona con `==`, `sorted()`, `min()`,
`max()` y `+`. No heredó de nada: habla los protocolos.

Devolver `NotImplemented` (que no es `NotImplementedError`) es la forma
correcta de decir "yo no sé comparar con eso": Python entonces le pregunta al
otro operando, y si tampoco sabe, lanza `TypeError` con un mensaje claro.

## 5. Herencia y composición

La herencia sirve para *es un*: `AdminUser` es un `User`. La composición sirve
para *tiene un*, y en la práctica se necesita mucho más.

```python
# Herencia: frágil si se usa para reutilizar código
class ReportWithCache(Report, CacheMixin, LoggerMixin): ...

# Composición: cada pieza se sustituye y se prueba por separado
class Report:
    def __init__(self, cache: Cache, logger: Logger) -> None:
        self._cache = cache
        self._logger = logger
```

La regla práctica: hereda cuando el subtipo pueda sustituir al padre en
cualquier sitio sin sorpresas. Si heredas solo para no repetir código, casi
siempre querías composición.

Cuando hay herencia múltiple, el orden en que Python busca los métodos se llama
**MRO** y se consulta, no se adivina: `Clase.__mro__`. Si necesitas dibujarlo
en una pizarra para entender tu propia jerarquía, la jerarquía está mal.

## 6. Qué pasa exactamente en un `import`

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
- **`ejercicios/reto/dinero.py`** — hacer que tu tipo hable los protocolos de
  comparación y aritmética.

## Resumen

- `self` explícito y sin `private`: Python prefiere convenciones a barandillas.
- El dinero va en enteros de la unidad mínima o en `Decimal`. Nunca en `float`.
- Los atributos se resuelven recorriendo diccionarios: instancia, clase, bases.
  Un mutable como atributo de clase se comparte entre todas las instancias.
- `@dataclass(frozen=True, slots=True)` te da `__init__`, `__repr__` y `__eq__`
  gratis; `__post_init__` es donde valida.
- Devuelve `NotImplemented` (no `NotImplementedError`) cuando tu dunder no sabe
  operar con el otro tipo.
- Hereda para *es un*; compón para *tiene un*. Heredar para reutilizar código
  suele ser composición mal hecha.
- Importar es: caché → localizar → registrar → ejecutar una vez → vincular. De
  ahí salen los módulos como singleton y el "define, no actúes" del nivel
  superior.
- Un ciclo de imports es un diagnóstico de diseño. Cura correcta: extraer el
  concepto común.
- Un módulo se nombra por su dominio. `utils` no es un dominio.

## Preguntas de repaso

1. ¿Por qué `items = []` dentro del cuerpo de una clase casi nunca es lo que
   querías?
2. ¿Qué te da `frozen=True` además de impedir asignaciones?
3. ¿Cuál es la diferencia entre devolver `NotImplemented` y lanzar
   `NotImplementedError` desde un `__eq__`?
4. Un compañero hereda de `Report` para reutilizar tres métodos, pero
   `CachedReport` no puede sustituir a `Report` en todos los sitios. ¿Qué le
   propondrías?
5. Importas el mismo módulo desde tres archivos distintos. ¿Cuántas veces se
   ejecuta su código de nivel superior?
6. Tienes un ciclo de imports que existe solo porque una anotación de tipo
   menciona la otra clase. ¿Cuál de las tres curas aplicas?
7. ¿Por qué el `src/` layout hace que tus tests sean más fiables?

## Recursos

- [Clases — tutorial oficial](https://docs.python.org/es/3/tutorial/classes.html)
  — `doc-oficial` · `es` · `principiante`. El modelo de objetos explicado por
  quienes lo diseñaron.
- [`dataclasses` — documentación](https://docs.python.org/es/3/library/dataclasses.html)
  — `doc-oficial` · `es` · `intermedio`. Todos los parámetros del decorador,
  con lo que hace cada uno.
- [El sistema de imports](https://docs.python.org/es/3/reference/import.html)
  — `doc-oficial` · `es` · `avanzado`. Denso, pero es la referencia cuando un
  import hace algo que no esperabas.

## Siguiente

Módulo 04 · Entorno y herramientas, donde este proyecto pasa a tener forma
profesional.
