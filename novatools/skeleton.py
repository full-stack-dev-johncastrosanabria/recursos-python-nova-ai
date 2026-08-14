"""Genera la estructura de un módulo de la ruta.

Un módulo siempre tiene la misma anatomía. Generarla evita que cada
contribución invente su propia variante.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUBFOLDERS = (
    "ejemplos",
    "ejercicios/base",
    "ejercicios/reto",
    "soluciones/base",
    "soluciones/reto",
    "tests/base",
    "tests/reto",
)


@dataclass(frozen=True)
class ModuleSpec:
    """Los datos que definen un módulo antes de tener contenido."""

    number: int
    slug: str
    title: str
    prerequisites: str
    minutes: int
    skip_to: str
    objectives: tuple[str, ...]


def folder_name(spec: ModuleSpec) -> str:
    return f"{spec.number:02d}-{spec.slug}"


def render_guide(spec: ModuleSpec) -> str:
    objectives = "\n".join(f"- {item}" for item in spec.objectives)
    return f"""# Módulo {spec.number:02d} · {spec.title}

> **Prerrequisitos:** {spec.prerequisites}
> **Tiempo estimado:** {spec.minutes} min
> **Si ya dominas esto:** {spec.skip_to}

## Qué vas a poder hacer al terminar

{objectives}

## Contenido

Este módulo todavía no está escrito. El módulo 01 es la plantilla viva: copia
su estructura. Si quieres escribir este, lee `CONTRIBUTING.md`.

## Caso real

Pendiente: un problema concreto donde lo del módulo se usa de verdad, con el
error que se comete cuando no se entiende.

## Ejercicios

- `ejercicios/base/` — para consolidar lo del módulo.
- `ejercicios/reto/` — si ya llegabas sabiendo el tema.

Para ver tu progreso:

```bash
uv run pytest ruta/{folder_name(spec)}
```

## Resumen

Pendiente: las ideas del módulo en una lista que se pueda releer en un minuto.

## Preguntas de repaso

Pendiente: preguntas que se responden con criterio, no de memoria.

## Recursos

Pendiente: enlaces para profundizar. Los curados por tema viven en
`recursos/enlaces/`.

## Siguiente

{spec.skip_to.capitalize()}.
"""


def create_module(root: Path, spec: ModuleSpec, force: bool = False) -> Path:
    """Crea las carpetas del módulo y escribe su GUIA.md.

    Las subcarpetas son idempotentes: se pueden recrear sin riesgo. La
    GUIA.md no lo es: si ya existe, no se sobrescribe salvo que `force` sea
    `True`, para no destruir contenido ya escrito por error.
    """
    module_dir = root / "ruta" / folder_name(spec)

    for sub in SUBFOLDERS:
        target = module_dir / sub
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitkeep").touch()

    guide_path = module_dir / "GUIA.md"
    if guide_path.exists() and not force:
        raise FileExistsError(
            f"Ya existe {guide_path} y no se va a sobrescribir. "
            "Si de verdad quieres reemplazarla, usa force=True "
            "(o --forzar desde la línea de comandos)."
        )

    guide_path.write_text(render_guide(spec), encoding="utf-8")
    return module_dir
