"""Tests de la infraestructura que resuelve qué archivo prueba cada test."""

from pathlib import Path

import pytest

from novatools.resolution import load_module, solutions_enabled, target_path


def test_target_path_apunta_a_ejercicios_por_defecto():
    test_path = Path("ruta/01-fundamentos/tests/base/test_saludo.py")
    assert target_path(test_path, use_solutions=False) == Path(
        "ruta/01-fundamentos/ejercicios/base/saludo.py"
    )


def test_target_path_apunta_a_soluciones_cuando_se_pide():
    test_path = Path("ruta/01-fundamentos/tests/reto/test_estadisticas.py")
    assert target_path(test_path, use_solutions=True) == Path(
        "ruta/01-fundamentos/soluciones/reto/estadisticas.py"
    )


def test_target_path_rechaza_test_fuera_de_carpeta_tests():
    with pytest.raises(ValueError, match="tests/"):
        target_path(
            Path("ruta/01-fundamentos/base/test_saludo.py"), use_solutions=False
        )


def test_target_path_rechaza_archivo_sin_prefijo_test():
    with pytest.raises(ValueError, match="test_"):
        target_path(
            Path("ruta/01-fundamentos/tests/base/saludo.py"), use_solutions=False
        )


def test_solutions_enabled_lee_la_variable():
    assert solutions_enabled({"NOVA_SOLUCIONES": "1"}) is True
    assert solutions_enabled({"NOVA_SOLUCIONES": "0"}) is False
    assert solutions_enabled({}) is False


def test_load_module_carga_un_archivo_suelto(tmp_path):
    file = tmp_path / "saludo.py"
    file.write_text(
        'def greet(name):\n    return f"Hola, {name}"\n', encoding="utf-8"
    )

    module = load_module(file)

    assert module.greet("Ana") == "Hola, Ana"


def test_load_module_no_colisiona_entre_modulos(tmp_path):
    first = tmp_path / "01-fundamentos" / "ejercicios" / "base"
    second = tmp_path / "02-estructuras-de-datos" / "ejercicios" / "base"
    first.mkdir(parents=True)
    second.mkdir(parents=True)
    (first / "saludo.py").write_text("VALUE = 1\n", encoding="utf-8")
    (second / "saludo.py").write_text("VALUE = 2\n", encoding="utf-8")

    assert load_module(first / "saludo.py").VALUE == 1
    assert load_module(second / "saludo.py").VALUE == 2
