# Módulo 04 · Entorno y herramientas

> **Prerrequisitos:** módulos 01-03<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 05

Hasta aquí has escrito Python. Este módulo va de lo que rodea al código y
decide si tu proyecto sobrevive: cómo se instala, cómo se mantiene consistente
entre máquinas, cómo se lee el estilo sin discutirlo, cómo se documentan los
contratos con tipos, cómo se sabe qué pasó cuando algo falla, y cómo se
distribuye.

Es el módulo menos vistoso de la ruta y el que más incidentes evita.

## Qué vas a poder hacer al terminar

- Crear y gestionar un proyecto con uv
- Configurar ruff para lint y formato
- Anotar tipos, incluidos genéricos y Protocol, y entender qué verifican
- Automatizar las comprobaciones con pre-commit
- Registrar eventos con `logging` en vez de con `print`
- Depurar con criterio, y saber cuándo basta un `print`
- Reconocer la anatomía de un proyecto Python y publicarlo

## 1. El problema real: "en mi máquina funciona"

Durante años, el flanco débil de Python fue el entorno. Instalabas paquetes en
el Python del sistema, dos proyectos pedían versiones distintas de la misma
librería y algo se rompía sin que nadie supiera qué había cambiado.

La respuesta tiene dos piezas: **un entorno aislado por proyecto** y **un
registro exacto de lo instalado**. Hoy las dos las resuelve `uv`, que es lo que
usa este repositorio.

```bash
uv sync                 # crea .venv e instala exactamente lo del lock
uv sync --group ia      # añade el grupo de dependencias de IA
uv add httpx            # añade una dependencia y actualiza el lock
uv add --dev pytest     # añade al grupo de desarrollo
uv remove httpx         # la quita
uv lock --upgrade       # actualiza versiones dentro de lo que permite pyproject
uv tree                 # el árbol de dependencias, para ver quién trae qué
uv run pytest           # ejecuta dentro del entorno, sin "activarlo"
uv python pin 3.12      # fija la versión del intérprete
```

Dos detalles que valen más de lo que parecen:

**`uv` instala el propio Python.** El `.python-version` de este repositorio dice
`3.12`, y `uv` se encarga de tener ese intérprete. No necesitas instalarlo
aparte ni pelearte con la versión del sistema.

**`uv run` en vez de activar el entorno.** Activar
(`source .venv/bin/activate`) es un estado invisible: tres terminales abiertas y
en una de ellas no está activado. `uv run` no tiene estado — el comando dice a
qué entorno pertenece.

## 2. `pyproject.toml`: una sola fuente de verdad

Lo que antes eran cinco archivos (`setup.py`, `requirements.txt`, `setup.cfg`,
`.flake8`, `pytest.ini`) hoy es uno solo y declarativo:

```toml
[project]
name = "recursos-python-nova-ai"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = ["pytest>=8", "ruff>=0.6"]
ia = ["anthropic", "langgraph", "crewai"]
docs = ["mkdocs-material"]

[tool.pytest.ini_options]
addopts = "--import-mode=importlib"

[tool.ruff]
target-version = "py312"
```

Los **grupos de dependencias** son la pieza que más se agradece en un proyecto
como este: quien viene a aprender listas no instala PyTorch. `uv sync` trae lo
básico; `uv sync --group ia` trae lo pesado cuando toca.

Y el **lockfile** (`uv.lock`) es lo que hace que "en mi máquina funciona" deje
de ser una frase. Fija las versiones exactas de todo el árbol, transitivas
incluidas. Se commitea. No se edita a mano.

### Rangos de versión, y el criterio

```toml
dependencies = [
    "httpx>=0.27",          # mínimo: quiero al menos esta
    "pydantic>=2,<3",       # rango: la 3 podría romper la API
    "requests==2.31.0",     # exacta: casi nunca es lo correcto en una librería
]
```

La regla: en una **aplicación**, sé permisivo en `pyproject.toml` y deja que el
lockfile fije lo exacto. En una **librería** que otros van a instalar, sé
permisivo de verdad — un rango estrecho en una librería popular provoca
conflictos irresolubles a quien la use.

## 3. Ruff: el estilo deja de ser una conversación

PEP 8 es la guía de estilo oficial: cuatro espacios, `snake_case` para
funciones y variables, `PascalCase` para clases. Pero su justificación importa
más que sus reglas concretas, y está en el propio documento: **el código se lee
muchas más veces de las que se escribe**, así que optimizar la escritura a costa
de la lectura es un mal negocio con certeza matemática.

En 2026 aplicar PEP 8 no es disciplina, es tooling:

```bash
uv run ruff check .           # detecta problemas
uv run ruff check --fix .     # arregla los que puede
uv run ruff format .          # formatea
uv run ruff format --check .  # falla si algo no está formateado (esto corre el CI)
```

### Elegir reglas

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

Cada letra es una familia: `E` errores de estilo, `F` errores lógicos
(variables sin usar, imports que faltan), `I` orden de imports, `UP` moderniza
sintaxis antigua, `B` errores comunes reales (`bugbear`) como el argumento
mutable por defecto que viste en el módulo 00.

Cuando una regla estorba **en un sitio concreto**, se silencia ahí y se explica:

```python
def add_broken(item, basket=[]):  # noqa: B006
    """El bug está aquí a propósito: es material didáctico."""
```

Un `noqa` sin explicación es deuda. Uno explicado es una decisión.

La conversación profesional ya no es "¿cumples PEP 8?" sino "¿tu pipeline lo
garantiza solo?". Cuando el formato lo decide una herramienta, deja de haber
discusiones de estilo en las revisiones y quedan las de fondo.

## 4. Type hints: contratos que las herramientas leen

Python incorporó anotaciones de tipos sin cambiar una premisa: **el intérprete
no las verifica**.

```python
def total(amounts: list[int]) -> int:
    return sum(amounts)

total("hola")   # no lanza TypeError por la anotación: se ejecuta y falla luego
```

Eso parece inútil hasta que se entiende qué problema resuelven, que no es el que
resuelven los tipos de Java. Los type hints son **contratos legibles por
herramientas**: un verificador estático los comprueba antes de ejecutar, el
editor los usa para autocompletar y refactorizar con seguridad, y quien lee el
código los usa como la documentación que no puede mentir mucho tiempo.

El resultado es un sistema **gradual**: se adopta por zonas, convive con código
sin tipar, y su retorno se concentra donde llevas tres módulos viendo que viven
los bugs — las fronteras.

### La unión con `None` y el narrowing

El caso dominante en la práctica es la ausencia:

```python
def find_transfer(ref: str) -> Transfer | None: ...

t = find_transfer(ref)
t.amount_cents          # el verificador lo RECHAZA: t puede ser None

if t is not None:
    t.amount_cents      # OK: dentro del if, el verificador estrechó el tipo
```

A eso se le llama *narrowing* y es la experiencia central de trabajar con
tipos: el verificador sigue el flujo de control y ajusta el tipo por rama. Toda
la familia de bugs donde "un `None` viajó tres capas y estalló lejos de su
origen" pasa de tiempo de ejecución a tiempo de edición.

### Anotar con el tipo más general que de verdad necesitas

```python
from collections.abc import Iterable, Sequence, Mapping, Callable

def total(amounts: Iterable[int]) -> int:       # solo lo recorro una vez
    return sum(amounts)

def median(values: Sequence[float]) -> float:   # necesito índice y len
    ...

def apply(f: Callable[[int], str], n: int) -> str:   # una función como argumento
    return f(n)
```

Pedir `list` cuando te bastaba `Iterable` cierra la puerta a los generadores sin
ganar nada. Es la versión tipada de la postura liberal en la entrada del duck
typing del módulo 00.

### Genéricos

```python
def first[T](items: Sequence[T], default: T | None = None) -> T | None:
    return items[0] if items else default

x = first([1, 2, 3])          # el verificador infiere int | None
s = first(["a"], default="")  # str | None

class Repository[T]:
    def get(self, ref: str) -> T | None: ...
    def save(self, item: T) -> None: ...
```

Sin el genérico tendrías que anotar `Any` y el verificador olvidaría qué entró.
El criterio de uso es la contención: los genéricos pagan en contenedores,
repositorios y funciones de transformación. En el resto, estorban.

### `Protocol` y `TypedDict`

```python
from typing import Protocol, TypedDict

class Repository(Protocol):           # duck typing verificable
    def get(self, ref: str) -> dict | None: ...
    def save(self, item: dict) -> None: ...

class TransferPayload(TypedDict):     # la forma de un dict concreto
    ref: str
    amount_cents: int
    currency: str
```

`Protocol` describe **qué sabe hacer** un objeto sin exigir herencia — es lo que
querrás para las fronteras de tu sistema. `TypedDict` describe **qué claves
tiene** un diccionario, que es lo que llega de un JSON antes de validarlo.

### El verificador, en la práctica

```bash
uv run mypy src/          # o pyright
```

Empieza por lo laxo y aprieta luego. La configuración inicial razonable:

```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_ignores = true
```

Y el modo estricto (`strict = true`) cuando el proyecto ya esté tipado. Activar
`strict` el primer día en un código existente produce mil errores y el abandono
de la idea.

## 5. pre-commit: que no llegue roto al CI

El CI te dice que algo está mal **después** de subirlo. `pre-commit` lo dice
antes de que llegue a commitearse:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

```bash
uv run pre-commit install     # una vez, engancha el hook de git
uv run pre-commit run --all-files
```

El criterio de qué meter ahí: **lo rápido y determinista**. Lint y formato, sí.
La suite completa de tests, no — un hook que tarda treinta segundos se acaba
saltando con `--no-verify`, y entonces no sirve para nada.

## 6. Logging: `print` no es observabilidad

`print` va a la salida estándar, no tiene niveles, no tiene marca de tiempo y no
se puede apagar sin editar el código. Sirve para depurar mientras escribes, y
para nada más.

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("payload recibido: %s", payload)      # detalle de desarrollo
logger.info("transferencia %s procesada", ref)     # curso normal de los eventos
logger.warning("reintento %d de %d", intento, total)   # algo raro, pero seguimos
logger.error("no se pudo procesar %s: %s", ref, error) # falló esta operación
logger.exception("fallo inesperado")               # como error, + traza completa
```

Cinco cosas que separan un log útil de ruido:

**`getLogger(__name__)`**, nunca el logger raíz. Así cada módulo tiene su canal
y se puede subir o bajar el nivel de una parte del sistema sin tocar el resto.

**Los parámetros van con `%s`, no con f-string.** `logger.debug("x: %s", caro())`
no evalúa `caro()` si el nivel `DEBUG` está apagado; con una f-string se evalúa
siempre. En un bucle caliente esa diferencia se nota.

**`logger.exception` solo dentro de un `except`**: añade la traza completa
automáticamente. Es lo que quieres casi siempre en el bloque de captura.

**El nivel se configura fuera**, en el arranque de la aplicación, no en la
librería:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
```

**Nunca registres secretos.** Ni claves, ni tokens, ni el payload entero de una
tarjeta. Un log es un archivo que acaba en sitios que no controlas.

## 7. Depurar con criterio

Hay tres herramientas y cada una tiene su momento:

**El `print` bien puesto.** No es vergonzoso: es la herramienta más rápida para
"¿llega aquí y con qué?". Con f-strings y `{variable=}` es todavía mejor:

```python
print(f"{ref=} {monto=} {estado=}")     # ref='TR-1' monto=1500 estado='pendiente'
```

Lo que sí es un problema es dejarlo. Por eso ruff tiene una regla (`T20`) para
detectar `print` olvidados en código de producción.

**El depurador.** Cuando el problema es "no entiendo qué está pasando", parar y
mirar vale más que veinte `print`:

```python
breakpoint()      # detiene la ejecución y abre el depurador aquí
```

Dentro: `n` siguiente línea, `s` entra en la función, `c` continúa, `p expr`
imprime, `l` muestra el código alrededor, `q` sale. Tu editor probablemente
tenga esto con botones, y funciona igual de bien.

**Los tests.** Cuando encuentres el bug, escribe el test **antes** de
arreglarlo. Ese test es lo que garantiza que no vuelva, y es el tema del módulo
siguiente.

## 8. Secretos y configuración

Nunca en el código. Nunca en el repositorio.

```python
import os

api_key = os.environ["ANTHROPIC_API_KEY"]    # falta → KeyError inmediato y claro
debug = os.environ.get("DEBUG", "0") == "1"  # ausencia con valor por defecto
```

Fíjate en la elección: para la clave de API, `os.environ[...]`, porque si falta
quiero enterarme al arrancar y no tres capas más adentro. Es la tríada de
lectura del módulo 02 aplicada a la configuración.

El patrón estándar es un `.env` que **no se commitea** y un `.env.example` que
sí, con las claves y los valores vacíos — como el que tiene este repositorio.

La precedencia habitual, de menor a mayor: valores por defecto del código <
archivo de configuración < variables de entorno < argumentos de línea de
comandos. En Python eso se escribe casi solo:

```python
config = defaults | file_config | env_config | cli_args   # gana la derecha
```

## 9. Empaquetar y distribuir

Cuando tu proyecto deja de ser tuyo y pasa a instalarse en otros sitios:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "billing"
version = "0.1.0"
description = "Conciliación bancaria"
readme = "README.md"
requires-python = ">=3.12"

[project.scripts]
billing = "billing.cli:main"     # crea un comando `billing` al instalar
```

```bash
uv build                  # genera el .whl y el .tar.gz en dist/
uv publish                # lo sube al índice de paquetes
```

El `[project.scripts]` es lo que convierte tu paquete en un comando del
sistema: quien lo instale escribirá `billing` y no `python -m billing.cli`.

Y la versión: **el número no es decorativo**. `MAYOR.MENOR.PARCHE`, donde subir
el mayor significa "he roto la compatibilidad". Quien dependa de ti toma
decisiones con ese número.

## Caso real

Un servicio funcionaba en la máquina de quien lo escribió y fallaba en
producción con un error que no decía nada. El diagnóstico llevó dos días y
resultaron ser cuatro cosas superpuestas:

1. **No había lockfile.** El `requirements.txt` decía `httpx>=0.20`. En el
   portátil se había instalado la 0.24 seis meses antes; el servidor instaló la
   última, que había cambiado el comportamiento por defecto de los timeouts.
2. **La configuración se leía con `.get()` y valores por defecto.** Faltaba una
   variable de entorno en producción, pero en vez de fallar al arrancar, el
   servicio tomó el valor por defecto —un endpoint de pruebas— y funcionó
   "bien" durante cuatro horas escribiendo en el sitio equivocado.
3. **No había verificación de tipos.** La función devolvía `Response | None` y
   quien la llamaba asumía que siempre había respuesta. En desarrollo nunca era
   `None`; en producción, con timeout, sí.
4. **No había logs, solo `print`.** Y como los `print` iban a una salida que
   nadie capturaba, el diagnóstico se hizo a ciegas. Con un `logger.error` y su
   traza, el primer día habría bastado.

Las cuatro se previenen con lo de este módulo, y ninguna con más tests de la
lógica de negocio: el bug no estaba en el dominio, estaba alrededor.

## Ejercicios

```bash
uv run pytest ruta/04-entorno-y-herramientas
```

- **`ejercicios/base/entorno.py`** — leer un archivo `.env` de verdad, con sus
  comentarios, comillas y casos raros.
- **`ejercicios/base/configuracion.py`** — capas de configuración con
  precedencia.
- **`ejercicios/base/registro.py`** — formatear líneas de log con nivel,
  filtrado y campos estructurados.
- **`ejercicios/reto/ajustes.py`** — convertir un diccionario de strings en un
  objeto de configuración validado. Es lo que hace Pydantic, a mano, para que
  cuando lo veas en el módulo 07 sepas qué te está ahorrando.
- **`ejercicios/reto/dependencias.py`** — ordenar un grafo de dependencias y
  detectar ciclos. Es lo que hace `uv` antes de instalar nada.

## Resumen

- Un entorno por proyecto y un lockfile: eso es lo que hace reproducible un
  despliegue. `uv` resuelve las dos cosas, e instala hasta el intérprete.
- `uv run` en lugar de activar el entorno: sin estado invisible.
- `pyproject.toml` es la fuente única de verdad. En aplicaciones, rangos
  permisivos y que el lock fije lo exacto.
- El estilo lo garantiza el pipeline, no la disciplina. Un `noqa` sin explicar
  es deuda.
- Los type hints no los verifica el intérprete: los verifican herramientas,
  antes de ejecutar. Su retorno está en las fronteras.
- `X | None` más narrowing convierte la familia de bugs del `None` viajero en
  errores de edición.
- Anota parámetros con el tipo más general que de verdad uses. Genéricos solo
  donde la relación entrada→salida importe.
- `Protocol` para contratos sin herencia; `TypedDict` para la forma de un JSON.
- Empieza el verificador en modo laxo y aprieta después.
- `pre-commit` para lo rápido y determinista. Un hook lento se acaba saltando.
- `logging` con `getLogger(__name__)`, parámetros con `%s` y el nivel
  configurado fuera. Nunca secretos en el log.
- El `print` para depurar está bien; dejarlo, no. Para entender, el depurador.
  Para que no vuelva, un test.
- Los secretos van en el entorno. Si falta uno crítico, mejor reventar al
  arrancar.
- El número de versión es un contrato con quien depende de ti.

## Preguntas de repaso

1. ¿Qué problema resuelve el lockfile que no resuelve un `requirements.txt` con
   rangos de versión?
2. ¿Por qué `uv run pytest` es preferible a activar el entorno y llamar a
   `pytest`?
3. Estás publicando una librería. ¿Pones `pydantic==2.5.1` o `pydantic>=2,<3`?
   ¿Por qué?
4. Si el intérprete no comprueba las anotaciones, ¿para qué sirven?
5. Una función acepta `list[int]` pero solo la recorre una vez. ¿Qué anotación
   sería mejor y qué ganas con el cambio?
6. ¿Cuándo eliges `Protocol` y cuándo `TypedDict`?
7. ¿Por qué `logger.debug("x: %s", caro())` es mejor que
   `logger.debug(f"x: {caro()}")`?
8. ¿Qué diferencia hay entre `logger.error` y `logger.exception`?
9. Lees una variable de entorno crítica. ¿`os.environ[...]` o
   `os.environ.get(...)`? ¿Por qué?
10. ¿Qué meterías en un hook de pre-commit y qué dejarías para el CI?

## Recursos

- [Documentación de uv](https://docs.astral.sh/uv/) — `doc-oficial` · `en` ·
  `principiante`. La sección de proyectos merece leerse entera una vez.
- [Ruff](https://docs.astral.sh/ruff/rules/) — `doc-oficial` · `en` ·
  `intermedio`. El catálogo de reglas: busca aquí qué significa cada código.
- [`typing` — documentación](https://docs.python.org/es/3/library/typing.html)
  — `doc-oficial` · `es` · `intermedio`. La referencia de anotaciones.
- [mypy — documentación](https://mypy.readthedocs.io/) — `doc-oficial` · `en` ·
  `intermedio`. Su guía de introducción explica el modelo gradual mejor que
  ningún tutorial.
- [Logging HOWTO](https://docs.python.org/es/3/howto/logging.html) —
  `doc-oficial` · `es` · `intermedio`. En español, y con la configuración
  explicada de menos a más.
- [Python Packaging User Guide](https://packaging.python.org/en/latest/) —
  `doc-oficial` · `en` · `intermedio`. Para cuando toque publicar.

## Siguiente

Módulo 05 · Testing, donde todo esto se convierte en la red que te deja cambiar
el código sin miedo.
