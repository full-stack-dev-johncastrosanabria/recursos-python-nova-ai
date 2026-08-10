"""Verifica que cada test de la ruta tenga su pareja en ejercicios/ y soluciones/.

Uso:
    uv run python scripts/verificar_parejas.py

Sale con código distinto de cero si falta algún archivo, para que el CI lo
detecte.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from novatools.resolution import missing_pairs  # noqa: E402


def main() -> None:
    missing = missing_pairs(ROOT)

    if not missing:
        print("Todos los tests tienen su pareja en ejercicios/ y soluciones/.")
        return

    print("Faltan estos archivos:")
    for path in missing:
        print(f"  - {path.relative_to(ROOT)}")
    sys.exit(1)


if __name__ == "__main__":
    main()
