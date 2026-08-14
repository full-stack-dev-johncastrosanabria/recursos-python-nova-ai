import pytest


def test_resume_una_lista_par(solution):
    assert solution.summarize([1, 2, 3, 4]) == {
        "min": 1,
        "max": 4,
        "mean": 2.5,
        "median": 2.5,
    }


def test_resume_una_lista_impar(solution):
    assert solution.summarize([5, 1, 3]) == {
        "min": 1,
        "max": 5,
        "mean": 3,
        "median": 3,
    }


def test_con_un_solo_numero(solution):
    assert solution.summarize([7]) == {"min": 7, "max": 7, "mean": 7, "median": 7}


def test_la_mediana_no_depende_del_orden_de_entrada(solution):
    """Hay que ordenar para la mediana: la entrada puede venir como sea."""
    assert solution.summarize([9, 1, 5, 3])["median"] == 4


def test_la_mediana_de_un_par_es_la_media_de_los_dos_centrales(solution):
    assert solution.summarize([10, 20, 30, 40])["median"] == 25


def test_la_mediana_no_es_lo_mismo_que_la_media(solution):
    """Un valor extremo mueve la media y casi no mueve la mediana."""
    resultado = solution.summarize([1, 2, 3, 1000])

    assert resultado["median"] == 2.5
    assert resultado["mean"] == 251.5


def test_funciona_con_negativos(solution):
    resultado = solution.summarize([-5, -1, -3])

    assert resultado["min"] == -5
    assert resultado["max"] == -1
    assert resultado["median"] == -3


def test_no_modifica_la_lista_recibida(solution):
    numeros = [3, 1, 2]

    solution.summarize(numeros)

    assert numeros == [3, 1, 2], "usa sorted(), no .sort()"


def test_rechaza_una_lista_vacia(solution):
    """Devolver 0 sería un valor creíble que oculta un fallo."""
    with pytest.raises(ValueError):
        solution.summarize([])
