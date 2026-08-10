# Diseño: recursos-python-nova-ai

**Fecha:** 2026-08-10
**Estado:** aprobado
**Repositorio:** `full-stack-dev-johncastrosanabria/recursos-python-nova-ai` (público)

## Propósito

Repositorio de capacitación en Python para el equipo de Nova AI. Lleva a personas
de nivel cero hasta construir agentes con LangGraph y CrewAI, y sirve además como
biblioteca de consulta permanente.

El equipo tiene niveles heterogéneos: desde quien nunca ha instalado Python hasta
perfiles intermedios. El repositorio debe ser útil para todos sin duplicar
contenido por nivel.

### Criterios de éxito

1. Alguien sin Python instalado escribe y ejecuta código en menos de 10 minutos.
2. Alguien de nivel intermedio identifica su punto de entrada sin leer los
   módulos previos.
3. Un miembro del equipo aporta un enlace, un ejercicio o una guía siguiendo una
   receta escrita, sin preguntar dónde va.
4. Todo ejercicio publicado es resoluble: su solución pasa sus propios tests en
   CI.

### Fuera de alcance

- Material interno o confidencial de Nova AI. El repositorio es público.
- Claves de API reales. Solo `.env.example` y documentación.
- Traducir identificadores de código al español (ver Convenciones).

## Arquitectura

Monorepo con un único entorno de Python gestionado por `uv`, con grupos de
dependencias opcionales para aislar lo pesado.

```
recursos-python-nova-ai/
├── README.md                  # portada, mapa de la ruta, arranque rápido
├── EMPIEZA-AQUI.md            # autodiagnóstico de nivel → módulo de entrada
├── CONTRIBUTING.md            # tres recetas de contribución
├── LICENSE                    # MIT (código)
├── LICENSE-CONTENIDO          # CC BY 4.0 (guías y contenido)
├── pyproject.toml             # uv: base + grupos ia, docs, dev
├── uv.lock
├── .python-version
├── mkdocs.yml
├── conftest.py                # resolución ejercicios/soluciones (ver CI)
├── .env.example
├── .devcontainer/
│   └── devcontainer.json      # Codespaces para nivel cero
├── docs/
│   └── superpowers/specs/     # diseño del proyecto (fuera del sitio)
├── ruta/                      # capacitación: se recorre en orden
│   └── NN-nombre/
│       ├── GUIA.md
│       ├── ejemplos/
│       ├── ejercicios/
│       │   ├── base/
│       │   └── reto/
│       ├── soluciones/
│       │   ├── base/
│       │   └── reto/
│       └── tests/
├── recursos/                  # consulta: se accede salteado
│   ├── enlaces/
│   ├── cheatsheets/
│   └── plantillas/
├── scripts/
└── .github/
    ├── workflows/{ci,enlaces,docs}.yml
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE/{recurso,error-guia}.yml
```

`ruta/` y `recursos/` son hermanas y con propósitos disjuntos: una se recorre en
orden, la otra se consulta. La separación elimina la pregunta "¿dónde pongo
esto?" en cada contribución.

### Por qué un solo entorno

Un `pyproject.toml` en la raíz significa un solo setup para el aprendiz. El
inconveniente —instalar el stack de IA para aprender listas— se resuelve con
grupos de dependencias de `uv`:

| Grupo | Contenido | Cuándo |
|-------|-----------|--------|
| base | stdlib, `pytest` | siempre |
| `ia` | SDK de Claude, `langgraph`, `crewai` | módulos 08–11 |
| `docs` | `mkdocs-material`, `mkdocs-same-dir` | solo quien edita el sitio |
| `dev` | `ruff`, herramientas de CI | contribuidores |

`uv sync` deja lo básico; `uv sync --group ia` añade lo pesado cuando toca.

## La ruta de aprendizaje

| # | Módulo | Contenido |
|---|--------|-----------|
| 01 | fundamentos | sintaxis, tipos, control de flujo, funciones |
| 02 | estructuras-de-datos | listas, dicts, sets, comprehensions, generadores |
| 03 | poo-y-modulos | clases, dataclasses, paquetes e imports |
| 04 | entorno-y-herramientas | uv, ruff, type hints, anatomía de un proyecto |
| 05 | testing | pytest, fixtures, parametrize, TDD básico |
| 06 | async-y-concurrencia | async/await, asyncio, cuándo no usarlo |
| 07 | datos-y-apis | pydantic, httpx, FastAPI mínimo, pandas básico |
| 08 | llms-fundamentos | SDK de Claude, prompts, tool use, salida estructurada, RAG básico |
| 09 | agentes-langgraph | grafos de estado, nodos, checkpoints, human-in-the-loop |
| 10 | agentes-crewai | agentes por roles, tareas, delegación |
| 11 | proyecto-final | agente completo que integra la ruta |

09 y 10 se mantienen separados a propósito: LangGraph modela grafos de estado y
CrewAI modela equipos con roles. Presentarlos como alternativas con filosofías
distintas enseña más que fundirlos en un módulo genérico de "agentes".

### Anatomía de un módulo

Todos los módulos comparten la misma estructura. `GUIA.md` abre con una cabecera
fija:

```markdown
> **Prerrequisitos:** módulos 01–03
> **Tiempo estimado:** 90 min
> **Si ya dominas esto:** salta al módulo 05
```

- `ejemplos/` — código completo, comentado, que se lee y se ejecuta.
- `ejercicios/base/` — stubs para consolidar lo del módulo.
- `ejercicios/reto/` — stubs para quien ya llegaba sabiendo el tema.
- `soluciones/` — espejo de `ejercicios/`, misma estructura de archivos.
- `tests/` — pytest, uno por ejercicio.

### Contenido del commit inicial

Los 11 módulos se crean como esqueleto: cada `GUIA.md` con su cabecera,
objetivos de aprendizaje e índice de temas. **Solo el módulo 01 va completo**,
funcionando de punta a punta con ejemplos, ejercicios base y reto, soluciones y
tests.

El 01 actúa como plantilla viva: quien escriba el módulo 05 copia una estructura
real en lugar de interpretar un documento sobre cómo debería ser. Publicar once
módulos vacíos sería peor que publicar uno real.

## Multi-nivel

Una sola ruta con varias puertas de entrada. No hay pistas paralelas por nivel:
duplicarían el mantenimiento y divergirían con el tiempo.

1. **`EMPIEZA-AQUI.md`** — checklist de autodiagnóstico, una pregunta por
   concepto clave ("¿puedes explicar qué hace `{k: v for k, v in …}` sin
   buscarlo?"). El resultado indica el módulo de entrada. Sin puntuaciones ni
   evaluación.
2. **Cabecera de cada guía** — prerrequisitos, tiempo estimado y salto sugerido
   para quien ya domina el tema.
3. **Ejercicios en dos niveles** — `base/` y `reto/` dentro del mismo módulo, con
   la misma guía. El intermedio no se aburre; el principiante no se ahoga.

### Nivel cero

`.devcontainer/devcontainer.json` permite abrir el repositorio en GitHub
Codespaces con Python y dependencias listas, sin instalar nada localmente. Quien
nunca configuró un entorno empieza a escribir código de inmediato y aprende a
instalarlo en el módulo 04, cuando ya entiende por qué.

En local, `uv` instala el propio intérprete de Python, así que el arranque es un
solo comando.

### Claves de API (módulos 08–11)

Requieren claves de pago. El repositorio es público, por lo que se incluye
`.env.example` y una guía para aportar la propia clave. Nunca una clave real en
el repositorio. Se documenta también la alternativa con modelos locales vía
Ollama para que el coste no bloquee a nadie.

## Documentación y enlaces

### Sitio

MkDocs Material con el plugin `same-dir`, configurado para leer los `GUIA.md`
donde ya viven en `ruta/`. No hay carpeta `docs/` espejo ni copia de archivos en
el build: cada guía tiene un único origen de verdad.

El workflow `docs.yml` publica en GitHub Pages al mergear a `main`. Queda
incluido pero inerte hasta que se active Pages en la configuración del
repositorio.

> Nota: `docs/superpowers/specs/` (donde vive este documento) queda excluido de
> la navegación del sitio; es documentación de proyecto, no material didáctico.

### Enlaces curados

`recursos/enlaces/` con un archivo por tema, espejo de los módulos
(`03-poo.md`, `08-ia.md`) más `general.md`. Formato fijo por entrada:

```markdown
### [Real Python: Comprehensions](https://…)
`artículo` · `en` · `intermedio` — La mejor explicación de cuándo una
comprehension deja de ser legible.
```

Tres etiquetas —tipo, idioma, nivel— y una línea justificando por qué vale la
pena. Ese último campo es lo que mantiene útil la lista: sin él, en seis meses
hay cien URLs y ninguna razón para abrir ninguna. El formato fijo hace que en
revisión de PR se vea de un vistazo si falta algo.

Se editan a mano en markdown. Sin YAML ni paso de generación.

## Tooling y CI

**Base:** `uv` (gestiona también el intérprete), `ruff` (lint y formato),
`pytest`.

### Resolución ejercicios/soluciones

Los tests de los ejercicios fallan por diseño: son stubs. El CI no puede correr
`pytest` a secas y quedarse verde.

Un `conftest.py` en la raíz expone una fixture `solucion` que carga el módulo del
ejercicio bajo prueba. Los tests nunca hacen `import` directo del ejercicio; piden
la fixture y trabajan con lo que devuelve:

```python
def test_saluda(solucion):
    assert solucion.greet("Ana") == "Hola, Ana"
```

La fixture resuelve la ruta del archivo a partir del nombre del test
(`tests/test_ej_01_saludo.py` → `ej_01_saludo.py`) y elige la carpeta origen:

- Sin variable de entorno → carga desde `ejercicios/`. El aprendiz ve rojo hasta
  resolver.
- Con `NOVA_SOLUCIONES=1` → carga desde `soluciones/`. Es como corre el CI.

La carga se hace con `importlib.util.spec_from_file_location`, de modo que
`ejercicios/` y `soluciones/` no necesitan ser paquetes importables ni compartir
nombres de módulo en `sys.modules`.

Así el CI verifica que cada ejercicio publicado es resoluble, atrapando en el PR
el fallo típico del material didáctico: un enunciado que no cuadra con su test.

### Workflows

| Workflow | Dispara | Hace |
|----------|---------|------|
| `ci.yml` | push y PR | `ruff check`, `ruff format --check`, `pytest` con `NOVA_SOLUCIONES=1` |
| `enlaces.yml` | PR que toca `recursos/`, y semanal | `lychee` sobre enlaces rotos |
| `docs.yml` | push a `main` | build y deploy de MkDocs a Pages |

`main` no lleva protección de rama, por decisión explícita.

## Contribución

`CONTRIBUTING.md` se organiza en tres recetas concretas en vez de principios
abstractos:

1. Añadir un enlace a `recursos/enlaces/`.
2. Añadir un ejercicio (stub + solución + test).
3. Escribir o corregir una guía.

Plantilla de PR con checklist breve. Dos plantillas de issue: *proponer recurso*
y *error en una guía*. La segunda importa especialmente: quien está aprendiendo
es quien detecta que una guía está equivocada, y hay que hacerle fácil decirlo.

## Convenciones

- **Prosa en español, identificadores en inglés.** Guías, comentarios y nombres
  de carpeta en español; variables, funciones y clases en inglés desde el módulo
  01. Es lo que el equipo encontrará en código real, y leerlo desde el principio
  es parte de la capacitación.
- **Carpetas en kebab-case**, módulos con prefijo numérico de dos dígitos.
- **Términos técnicos sin traducir**: `list comprehension`, no "comprensión de
  listas".

## Licencia

Dual, estándar en repositorios educativos:

- **MIT** para el código (`LICENSE`).
- **CC BY 4.0** para el contenido: guías, cheatsheets, listas de enlaces
  (`LICENSE-CONTENIDO`).

El `README.md` explica qué licencia cubre qué.

## Decisiones descartadas

| Alternativa | Por qué no |
|-------------|-----------|
| Un `pyproject.toml` por módulo | Aísla dependencias, pero obliga al aprendiz a hacer setup N veces y complica el CI con matriz de jobs. Los grupos de `uv` dan el aislamiento sin la fricción. |
| MkDocs como estructura principal | Relegaría los ejercicios con tests a un anexo, y añade mantenimiento de build antes de existir contenido. El sitio se monta sobre la estructura, no al revés. |
| Enlaces en YAML con markdown generado | Permitiría filtrar por etiqueta, pero añade un paso de build a algo que se edita a mano tres veces por semana. |
| Pistas duplicadas por nivel | Triplica el mantenimiento y las copias divergen. Se resuelve con puertas de entrada sobre una ruta única. |
| Protección de `main` | Descartada explícitamente por el propietario del repositorio. |
