import pytest


def test_summarize_devuelve_minimo_maximo_y_media(solution):
    assert solution.summarize([1, 2, 3, 4]) == {
        "min": 1,
        "max": 4,
        "mean": 2.5,
    }


def test_summarize_con_un_solo_numero(solution):
    assert solution.summarize([7]) == {"min": 7, "max": 7, "mean": 7}


def test_summarize_rechaza_una_lista_vacia(solution):
    with pytest.raises(ValueError):
        solution.summarize([])
