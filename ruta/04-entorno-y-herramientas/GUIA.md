# Módulo 04 · Entorno y herramientas

> **Prerrequisitos:** módulos 01-03<br>
> **Tiempo estimado:** 90 min<br>
> **Si ya dominas esto:** salta al módulo 05

Hasta aquí has escrito Python. Este módulo va de lo que rodea al código y
decide si tu proyecto sobrevive: cómo se instala, cómo se mantiene consistente
entre máquinas, cómo se lee el estilo sin discutirlo y cómo se documentan los
contratos con tipos.

Es el módulo menos vistoso de la ruta y el que más incidentes evita.

## Qué vas a poder hacer al terminar

- Crear y gestionar un proyecto con uv
- Configurar ruff para lint y formato
- Anotar tipos y entender qué verifican
- Reconocer la anatomía de un proyecto Python

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
uv run pytest           # ejecuta dentro del entorno, sin "activarlo"
uv run python script.py
```

Dos detalles que valen más de lo que parecen:

**`uv` instala el propio Python.** El `.python-version` de este repositorio dice
`3.12`, y `uv` se encarga de tener ese intérprete. No necesitas instalarlo
aparte ni pelearte con la versión del sistema.

**`uv run` en vez de activar el entorno.** Activar (`source .venv/bin/activate`)
es un estado invisible: tres terminales abiertas y en una de ellas no está
activado. `uv run` no tiene estado — el comando dice a qué entorno pertenece.

## 2. `pyproject.toml`: una sola fuente de verdad

Lo que antes eran cinco archivos (`setup.py`, `requirements.txt`,
`setup.cfg`, `.flake8`, `pytest.ini`) hoy es uno solo y declarativo:

```toml
[project]
name = "recursos-python-nova-ai"
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

La conversación profesional ya no es "¿cumples PEP 8?" sino "¿tu pipeline lo
garantiza solo?". Cuando el formato lo decide una herramienta, deja de haber
discusiones de estilo en las revisiones y quedan las de fondo, que son las que
importan.

Un detalle de este repositorio: `pyproject.toml` excluye los `*.md` del alcance
de ruff. Es deliberado — el markdown de aquí es material didáctico y sus
ejemplos están escritos para enseñar, no para pasar un formateador.

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
herramientas**: un verificador estático (mypy, pyright) los comprueba antes de
ejecutar, el editor los usa para autocompletar y para refactorizar con
seguridad, y quien lee el código los usa como la documentación que no puede
mentir mucho tiempo sin que alguien lo note.

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
from collections.abc import Iterable, Sequence

def total(amounts: Iterable[int]) -> int:   # solo lo recorro una vez
    return sum(amounts)

def median(values: Sequence[float]) -> float:   # necesito índice y len
    ...
```

`Iterable[T]` promete "puedo darte los elementos". `Sequence[T]` añade índice y
`len`. Pedir `list` cuando te bastaba `Iterable` cierra la puerta a los
generadores sin ganar nada. Es la versión tipada de la postura liberal en la
entrada del duck typing del módulo 00.

### Genéricos, cuando la relación entrada→salida importa

```python
def first[T](items: Sequence[T], default: T | None = None) -> T | None:
    return items[0] if items else default

x = first([1, 2, 3])          # el verificador infiere int | None
s = first(["a"], default="")  # str | None
```

Sin el genérico tendrías que anotar `Any` y el verificador olvidaría qué entró.
El criterio de uso es la contención: los genéricos pagan en contenedores,
repositorios y funciones de transformación. En el resto, estorban.

## 5. Secretos y configuración

Nunca en el código. Nunca en el repositorio.

```python
import os

api_key = os.environ["ANTHROPIC_API_KEY"]   # falta → KeyError inmediato y claro
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

## Caso real

Un servicio funcionaba en la máquina de quien lo escribió y fallaba en
producción con un error que no decía nada. El diagnóstico llevó dos días y
resultaron ser tres cosas superpuestas:

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

Las tres se previenen con lo de este módulo, y ninguna con más tests de la
lógica de negocio: el bug no estaba en el dominio, estaba alrededor.

## Ejercicios

```bash
uv run pytest ruta/04-entorno-y-herramientas
```

- **`ejercicios/base/entorno.py`** — leer un archivo `.env` de verdad, con sus
  comentarios, comillas y casos raros.
- **`ejercicios/base/configuracion.py`** — capas de configuración con
  precedencia.
- **`ejercicios/reto/ajustes.py`** — convertir un diccionario de strings en un
  objeto de configuración validado. Es lo que hace Pydantic, a mano, para que
  cuando lo veas en el módulo 07 sepas qué te está ahorrando.

## Resumen

- Un entorno por proyecto y un lockfile: eso es lo que hace reproducible un
  despliegue. `uv` resuelve las dos cosas, e instala hasta el intérprete.
- `uv run` en lugar de activar el entorno: sin estado invisible.
- `pyproject.toml` es la fuente única de verdad: dependencias, grupos y
  configuración de herramientas.
- Los grupos de dependencias evitan que quien aprende listas instale PyTorch.
- El estilo lo garantiza el pipeline, no la disciplina. Ruff hace lint y
  formato.
- Los type hints no los verifica el intérprete: los verifican herramientas,
  antes de ejecutar. Su retorno está en las fronteras.
- `X | None` más narrowing convierte la familia de bugs del `None` viajero en
  errores de edición.
- Anota parámetros con el tipo más general que de verdad uses.
- Los secretos van en el entorno, nunca en el repositorio. Si falta uno
  crítico, mejor reventar al arrancar.

## Preguntas de repaso

1. ¿Qué problema resuelve el lockfile que no resuelve un `requirements.txt` con
   rangos de versión?
2. ¿Por qué `uv run pytest` es preferible a activar el entorno y llamar a
   `pytest`?
3. Si el intérprete no comprueba las anotaciones, ¿para qué sirven?
4. Una función acepta `list[int]` pero solo la recorre una vez. ¿Qué anotación
   sería mejor y qué ganas con el cambio?
5. Lees una variable de entorno crítica. ¿`os.environ[...]` o
   `os.environ.get(...)`? ¿Por qué?
6. Tienes valores por defecto, un archivo de config y variables de entorno.
   ¿Cómo los combinas para que gane el más específico?

## Recursos

- [Documentación de uv](https://docs.astral.sh/uv/) — `doc-oficial` · `en` ·
  `principiante`. La sección de proyectos merece leerse entera una vez.
- [Ruff](https://docs.astral.sh/ruff/) — `doc-oficial` · `en` · `intermedio`.
  Busca aquí qué significa cada código de error que te salga.
- [`typing` — documentación](https://docs.python.org/es/3/library/typing.html)
  — `doc-oficial` · `es` · `intermedio`. La referencia de anotaciones.
- [mypy — documentación](https://mypy.readthedocs.io/) — `doc-oficial` · `en` ·
  `intermedio`. El verificador más extendido; su guía de introducción explica
  el modelo gradual mejor que ningún tutorial.

## Siguiente

Módulo 05 · Testing, donde todo esto se convierte en la red que te deja cambiar
el código sin miedo.
