"""Decide qué archivo carga el test de un ejercicio.

Los tests de la ruta nunca importan el ejercicio directamente: piden la fixture
`solution`, que usa estas funciones para cargar el stub del aprendiz o la
solución de referencia, según la variable de entorno NOVA_SOLUCIONES.
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from types import ModuleType

SOLUTIONS_ENV_VAR = "NOVA_SOLUCIONES"


def solutions_enabled(env: Mapping[str, str] | None = None) -> bool:
    """True si los tests deben correr contra soluciones/ en vez de ejercicios/."""
    source = os.environ if env is None else env
    return source.get(SOLUTIONS_ENV_VAR, "") == "1"


def target_path(test_path: Path, use_solutions: bool) -> Path:
    """Traduce la ruta de un test a la del archivo que pone a prueba.

    ruta/01-fundamentos/tests/base/test_saludo.py
        -> ruta/01-fundamentos/ejercicios/base/saludo.py
    """
    parts = list(test_path.parts)
    if "tests" not in parts:
        raise ValueError(f"El test debe vivir bajo una carpeta 'tests/': {test_path}")

    index = len(parts) - 1 - parts[::-1].index("tests")
    parts[index] = "soluciones" if use_solutions else "ejercicios"

    filename = test_path.name
    if not filename.startswith("test_"):
        raise ValueError(f"El archivo de test debe empezar por 'test_': {filename}")
    parts[-1] = filename.removeprefix("test_")

    return Path(*parts)


def load_module(path: Path) -> ModuleType:
    """Carga un archivo .py suelto como módulo, sin que su carpeta sea paquete."""
    resolved = path.resolve()
    tail = "_".join(resolved.with_suffix("").parts[-4:])
    module_name = "nova_" + re.sub(r"\W+", "_", tail)

    spec = importlib.util.spec_from_file_location(module_name, resolved)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar {resolved}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
