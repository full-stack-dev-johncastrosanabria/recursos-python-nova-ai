import pytest

REGISTROS = [
    {"divisa": "CRC", "monto": 100},
    {"divisa": "USD", "monto": 50},
    {"divisa": "CRC", "monto": 300},
]


def test_agrupa_y_resume(solution):
    assert solution.summarize_by(REGISTROS, key="divisa", value="monto") == {
        "CRC": {"count": 2, "total": 400, "min": 100, "max": 300, "mean": 200.0},
        "USD": {"count": 1, "total": 50, "min": 50, "max": 50, "mean": 50.0},
    }


def test_los_grupos_salen_ordenados(solution):
    registros = [
        {"g": "zeta", "v": 1},
        {"g": "alfa", "v": 2},
        {"g": "media", "v": 3},
    ]

    assert list(solution.summarize_by(registros, key="g", value="v")) == [
        "alfa",
        "media",
        "zeta",
    ]


def test_es_determinista(solution):
    """Un informe que cambia de orden no se puede comparar con el de ayer."""
    primero = solution.summarize_by(REGISTROS, key="divisa", value="monto")
    segundo = solution.summarize_by(REGISTROS, key="divisa", value="monto")

    assert list(primero) == list(segundo)


def test_un_solo_grupo(solution):
    registros = [{"g": "a", "v": 10}, {"g": "a", "v": 20}]

    resumen = solution.summarize_by(registros, key="g", value="v")

    assert resumen == {
        "a": {"count": 2, "total": 30, "min": 10, "max": 20, "mean": 15.0}
    }


def test_la_media_es_float(solution):
    resumen = solution.summarize_by([{"g": "a", "v": 3}], key="g", value="v")

    assert isinstance(resumen["a"]["mean"], float)


def test_funciona_con_negativos(solution):
    registros = [{"g": "a", "v": -10}, {"g": "a", "v": 30}]

    resumen = solution.summarize_by(registros, key="g", value="v")

    assert resumen["a"] == {
        "count": 2,
        "total": 20,
        "min": -10,
        "max": 30,
        "mean": 10.0,
    }


def test_sin_registros(solution):
    assert solution.summarize_by([], key="g", value="v") == {}


def test_falta_el_campo_de_agrupacion(solution):
    """Si no está la columna por la que agrupas, el resumen no significa nada."""
    with pytest.raises(KeyError):
        solution.summarize_by([{"v": 1}], key="g", value="v")


def test_falta_el_campo_de_valor(solution):
    with pytest.raises(KeyError):
        solution.summarize_by([{"g": "a"}], key="g", value="v")


def test_no_modifica_los_registros(solution):
    registros = [{"g": "a", "v": 1}]

    solution.summarize_by(registros, key="g", value="v")

    assert registros == [{"g": "a", "v": 1}]


def test_acepta_un_generador(solution):
    resumen = solution.summarize_by((r for r in REGISTROS), key="divisa", value="monto")

    assert resumen["CRC"]["count"] == 2
