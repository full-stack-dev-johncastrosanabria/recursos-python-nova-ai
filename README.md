# Recursos Python · Nova AI

Ruta de capacitación en Python para el equipo, de nivel cero a construir
agentes con LangGraph y CrewAI. Incluye guías, código ejecutable, ejercicios
con tests y una biblioteca de enlaces curados.

**¿No sabes por dónde empezar?** Lee [EMPIEZA-AQUI.md](EMPIEZA-AQUI.md): son
diez preguntas y te dice tu módulo de entrada.

## Arranque rápido

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

Cuando llegues al módulo 08 necesitarás las dependencias de IA:

```bash
uv sync --group ia
```

## La ruta

| # | Módulo | Qué cubre |
|---|--------|-----------|
| [01](ruta/01-fundamentos/GUIA.md) | Fundamentos | sintaxis, tipos, control de flujo, funciones |
| [02](ruta/02-estructuras-de-datos/GUIA.md) | Estructuras de datos | listas, dicts, sets, comprehensions, generadores |
| [03](ruta/03-poo-y-modulos/GUIA.md) | POO y módulos | clases, dataclasses, paquetes e imports |
| [04](ruta/04-entorno-y-herramientas/GUIA.md) | Entorno y herramientas | uv, ruff, type hints, anatomía de un proyecto |
| [05](ruta/05-testing/GUIA.md) | Testing | pytest, fixtures, parametrize, TDD básico |
| [06](ruta/06-async-y-concurrencia/GUIA.md) | Async y concurrencia | async/await, asyncio, cuándo no usarlo |
| [07](ruta/07-datos-y-apis/GUIA.md) | Datos y APIs | pydantic, httpx, FastAPI, pandas |
| [08](ruta/08-llms-fundamentos/GUIA.md) | Fundamentos de LLMs | SDK de Claude, prompts, tool use, RAG |
| [09](ruta/09-agentes-langgraph/GUIA.md) | Agentes con LangGraph | grafos de estado, checkpoints, human-in-the-loop |
| [10](ruta/10-agentes-crewai/GUIA.md) | Agentes con CrewAI | agentes por roles, tareas, delegación |
| [11](ruta/11-proyecto-final/GUIA.md) | Proyecto final | un agente completo, de punta a punta |

Ahora mismo **solo el módulo 01 tiene contenido**. El resto son esqueletos con
sus objetivos definidos, a la espera de que alguien los escriba. Empieza por
[CONTRIBUTING.md](CONTRIBUTING.md) si quieres ser esa persona.

## Recursos de consulta

- [Enlaces curados](recursos/enlaces/README.md) — artículos, vídeos y cursos por tema
- [Cheatsheets](recursos/cheatsheets/README.md) — referencias rápidas
- [Plantillas](recursos/plantillas/README.md) — scaffolds de proyecto reutilizables (todavía por escribir)

## Claves de API

Los módulos 08 al 11 llaman a modelos de pago. Copia `.env.example` a `.env` y
pon tus propias claves; `.env` está en `.gitignore` y nunca debe subirse.

Si no quieres gastar, el módulo 08 documenta cómo usar modelos locales con
Ollama.

## Licencia

Doble licencia: el **código** bajo
[MIT](https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai/blob/main/LICENSE),
el **contenido** (guías, cheatsheets, listas de enlaces) bajo
[CC BY 4.0](https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai/blob/main/LICENSE-CONTENIDO).
