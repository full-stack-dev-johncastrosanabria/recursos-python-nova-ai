"""Configuración global de pytest para la ruta de aprendizaje."""

from pathlib import Path

import pytest

from novatools.resolution import load_module, solutions_enabled, target_path


@pytest.fixture
def solution(request):
    """Carga el ejercicio bajo prueba.

    Por defecto carga tu archivo de `ejercicios/`, así que los tests estarán en
    rojo hasta que lo resuelvas. Con NOVA_SOLUCIONES=1 carga la solución de
    referencia: así verifica el CI que cada ejercicio publicado es resoluble.
    """
    test_path = Path(request.path)
    use_solutions = solutions_enabled()
    path = target_path(test_path, use_solutions)

    if not path.exists():
        carpeta = "soluciones" if use_solutions else "ejercicios"
        pytest.fail(
            f"Falta el archivo en {carpeta}/: {path}\n"
            f"Cada test necesita su pareja: {test_path.name} -> {path.name}"
        )

    return load_module(path)
