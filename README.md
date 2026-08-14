# Recursos Python · Nova AI

Ruta de capacitación en Python para el equipo, de nivel cero a construir
agentes con LangGraph y CrewAI. **Doce módulos de 3 a 5 horas cada uno —unas 48
en total—** con guías, código que se ejecuta, **717 tests** que verifican tus
ejercicios, y una biblioteca de enlaces curados.

No es un catálogo de sintaxis. Cada módulo empieza por el criterio —cuándo usar
algo y cuándo no— y termina en ejercicios que fallan hasta que los resuelves.

<div class="nova-tarjetas" markdown>

<div class="nova-tarjeta" markdown>
**[¿Por dónde empiezo?](EMPIEZA-AQUI.md)**
{ .nova-titulo }

Diez preguntas y te dice tu módulo de entrada. No hace falta empezar por el
principio.
</div>

<div class="nova-tarjeta" markdown>
**[Arranque rápido](#arranque-rapido)**
{ .nova-titulo }

Un `git clone` y un comando. `uv` instala hasta el propio Python.
</div>

<div class="nova-tarjeta" markdown>
**[Contribuir](CONTRIBUTING.md)**
{ .nova-titulo }

Tres recetas concretas: añadir un enlace, un ejercicio o una guía.
</div>

</div>

## Arranque rápido { #arranque-rapido }

### Sin instalar nada

Abre el repositorio en GitHub Codespaces (botón **Code › Codespaces**). Tienes
Python y las dependencias listas en un par de minutos.

### En tu máquina

Necesitas [uv](https://docs.astral.sh/uv/). Instala el resto —incluido el
propio Python— por ti:

```bash
git clone https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai.git
cd recursos-python-nova-ai
uv sync
uv run pytest ruta/01-fundamentos
```

Los tests te saldrán en rojo. Es correcto: son los ejercicios sin resolver.

Cuando llegues al módulo 08 y quieras hablar con un modelo de verdad:

```bash
uv sync --group ia
cp .env.example .env      # y pon tu clave dentro
```

## La ruta

### Fundamentos

| # | Módulo | Qué cubre |
|---|--------|-----------|
| [00](ruta/00-como-piensa-python/GUIA.md) | Cómo piensa Python | qué es un programa, el Zen, los cinco modelos mentales |
| [01](ruta/01-fundamentos/GUIA.md) | Fundamentos | asignación, números y dinero, la verdad, control de flujo, funciones |
| [02](ruta/02-estructuras-de-datos/GUIA.md) | Estructuras de datos | costes por dentro, matrices, álgebra de conjuntos, generadores |
| [03](ruta/03-poo-y-modulos/GUIA.md) | POO y módulos | clases, propiedades, herencia y MRO, recursión, imports |

### El oficio

| # | Módulo | Qué cubre |
|---|--------|-----------|
| [04](ruta/04-entorno-y-herramientas/GUIA.md) | Entorno y herramientas | uv, ruff, tipos, pre-commit, logging, empaquetado |
| [05](ruta/05-testing/GUIA.md) | Testing | pytest a fondo, dobles, cobertura, property-based |
| [06](ruta/06-async-y-concurrencia/GUIA.md) | Async y concurrencia | el GIL, hilos y procesos, TaskGroup, colas |
| [07](ruta/07-datos-y-apis/GUIA.md) | Datos y APIs | archivos, pydantic, httpx, FastAPI, pandas |

### Inteligencia artificial

| # | Módulo | Qué cubre |
|---|--------|-----------|
| [08](ruta/08-llms-fundamentos/GUIA.md) | Fundamentos de LLMs | tokens, embeddings, prompts, tool use, RAG |
| [09](ruta/09-agentes-langgraph/GUIA.md) | Agentes con LangGraph | los cinco patrones, grafos de estado, memoria |
| [10](ruta/10-agentes-crewai/GUIA.md) | Agentes con CrewAI | roles, diseño de herramientas, barreras, verificación |
| [11](ruta/11-proyecto-final/GUIA.md) | Proyecto final | un sistema completo, de punta a punta |

## Cómo funcionan los ejercicios

Cada módulo tiene la misma anatomía:

```text
ruta/NN-modulo/
├── GUIA.md          la lección
├── ejemplos/        código que se lee y se ejecuta
├── ejercicios/      lo que completas tú (base/ y reto/)
├── soluciones/      la versión de referencia
└── tests/           lo que dice si acertaste
```

Los ejercicios son funciones sin terminar. Sus tests **fallan a propósito**
hasta que los resuelves:

```bash
uv run pytest ruta/02-estructuras-de-datos          # rojo: aún no lo has hecho
uv run pytest ruta/02-estructuras-de-datos -k conciliacion   # solo uno
```

Los tests no importan tu archivo directamente: piden una fixture llamada
`solution`, que carga tu ejercicio o —cuando corre el CI— la solución de
referencia. Así el repositorio verifica que **todo ejercicio publicado es
resoluble**, que es el fallo típico del material didáctico: un enunciado que no
cuadra con su test.

Hay ejercicios de dos niveles en cada módulo: `base/` para consolidar y `reto/`
si ya llegabas sabiendo el tema.

## Recursos de consulta

- [Enlaces curados](recursos/enlaces/README.md) — artículos, vídeos y cursos
  por tema, cada uno con una línea explicando por qué vale la pena
- [Cheatsheets](recursos/cheatsheets/README.md) — referencias rápidas
- [Plantillas](recursos/plantillas/README.md) — scaffolds reutilizables
  (todavía por escribir)

## Claves de API

Los módulos 08 al 11 pueden llamar a modelos de pago, pero **sus ejercicios no
necesitan clave ni conexión**: prueban el código que rodea al modelo, que es lo
que se puede probar. Si quieres además hablar con un modelo de verdad, copia
`.env.example` a `.env` y pon la tuya. `.env` está en `.gitignore`.

## Licencia y créditos

Doble licencia: el **código** bajo
[MIT](https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai/blob/main/LICENSE),
el **contenido** (guías, cheatsheets, listas de enlaces) bajo
[CC BY 4.0](https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai/blob/main/LICENSE-CONTENIDO).

La estructura de la ruta y varios de los casos reales se apoyan en dos libros:
*Python: El Lenguaje del Pensamiento* (edición 2026) para el criterio de
ingeniería y la parte de IA, y *Python Essentials 1* del OpenEDG Python
Institute para la cobertura de fundamentos.
