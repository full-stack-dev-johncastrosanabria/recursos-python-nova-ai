"""Crea el esqueleto de un módulo nuevo.

Uso:
    uv run python scripts/nuevo_modulo.py 12 despliegue "Despliegue" \\
        --prerrequisitos "módulos 01-07" --minutos 120 \\
        --salto "salta al módulo 13" \\
        --objetivo "Publicar un agente en producción"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from novatools.skeleton import ModuleSpec, create_module  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea el esqueleto de un módulo")
    parser.add_argument("numero", type=int, help="número del módulo, p. ej. 12")
    parser.add_argument("slug", help="nombre de carpeta en kebab-case")
    parser.add_argument("titulo", help="título legible del módulo")
    parser.add_argument("--prerrequisitos", default="ninguno")
    parser.add_argument("--minutos", type=int, default=90)
    parser.add_argument("--salto", default="no hay módulo siguiente todavía")
    parser.add_argument(
        "--objetivo",
        action="append",
        default=[],
        help="repetible: un objetivo de aprendizaje por bandera",
    )
    parser.add_argument(
        "--forzar",
        action="store_true",
        help="sobrescribe la GUIA.md si ya existe",
    )
    args = parser.parse_args()

    spec = ModuleSpec(
        number=args.numero,
        slug=args.slug,
        title=args.titulo,
        prerequisites=args.prerrequisitos,
        minutes=args.minutos,
        skip_to=args.salto,
        objectives=tuple(args.objetivo),
    )

    try:
        target = create_module(ROOT, spec, force=args.forzar)
    except FileExistsError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    print(f"Módulo creado en {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
