import dataclasses

import pytest


def test_convierte_los_tipos_desde_texto(solution):
    ajustes = solution.Settings.from_mapping({"HOST": "db.internal", "PORT": "5432"})

    assert ajustes.host == "db.internal"
    assert ajustes.port == 5432
    assert isinstance(ajustes.port, int)


def test_aplica_los_valores_por_defecto(solution):
    ajustes = solution.Settings.from_mapping({"HOST": "h", "PORT": "1"})

    assert ajustes.debug is False
    assert ajustes.timeout == 30.0


def test_lee_los_opcionales_cuando_estan(solution):
    ajustes = solution.Settings.from_mapping(
        {"HOST": "h", "PORT": "1", "DEBUG": "true", "TIMEOUT": "2.5"}
    )

    assert ajustes.debug is True
    assert ajustes.timeout == 2.5


@pytest.mark.parametrize("valor", ["1", "true", "TRUE", "Yes", "on", "  ON  "])
def test_valores_verdaderos_de_debug(solution, valor):
    ajustes = solution.Settings.from_mapping({"HOST": "h", "PORT": "1", "DEBUG": valor})

    assert ajustes.debug is True


@pytest.mark.parametrize("valor", ["0", "false", "no", "", "cualquier cosa"])
def test_valores_falsos_de_debug(solution, valor):
    ajustes = solution.Settings.from_mapping({"HOST": "h", "PORT": "1", "DEBUG": valor})

    assert ajustes.debug is False


def test_falta_una_obligatoria(solution):
    with pytest.raises(ValueError):
        solution.Settings.from_mapping({"HOST": "h"})


def test_el_error_menciona_todas_las_que_faltan(solution):
    """Quien despliega quiere arreglarlo de una vez, no una por ejecución."""
    with pytest.raises(ValueError) as error:
        solution.Settings.from_mapping({})

    mensaje = str(error.value)
    assert "HOST" in mensaje
    assert "PORT" in mensaje


def test_un_puerto_que_no_es_numero(solution):
    with pytest.raises(ValueError) as error:
        solution.Settings.from_mapping({"HOST": "h", "PORT": "ocho mil"})

    mensaje = str(error.value)
    assert "PORT" in mensaje
    assert "ocho mil" in mensaje


def test_un_timeout_que_no_es_numero(solution):
    with pytest.raises(ValueError) as error:
        solution.Settings.from_mapping(
            {"HOST": "h", "PORT": "1", "TIMEOUT": "despacito"}
        )

    assert "TIMEOUT" in str(error.value)


def test_los_ajustes_son_inmutables(solution):
    ajustes = solution.Settings.from_mapping({"HOST": "h", "PORT": "1"})

    with pytest.raises(dataclasses.FrozenInstanceError):
        ajustes.port = 9999
