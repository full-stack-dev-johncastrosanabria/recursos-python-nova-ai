from itertools import count

import pytest


def test_chunked_trocea_en_partes_iguales(solution):
    assert list(solution.chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]


def test_el_ultimo_trozo_puede_ser_mas_corto(solution):
    assert list(solution.chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_chunked_con_iterable_vacio_no_produce_nada(solution):
    assert list(solution.chunked([], 3)) == []


def test_chunked_con_trozo_mayor_que_la_entrada(solution):
    assert list(solution.chunked([1, 2], 10)) == [[1, 2]]


def test_chunked_rechaza_tamanos_invalidos(solution):
    with pytest.raises(ValueError):
        list(solution.chunked([1, 2, 3], 0))

    with pytest.raises(ValueError):
        list(solution.chunked([1, 2, 3], -1))


def test_chunked_es_perezoso_sobre_un_iterable_infinito(solution):
    """Si materializas la entrada antes de trocear, esto se cuelga para siempre."""
    trozos = solution.chunked(count(), 3)

    assert next(trozos) == [0, 1, 2]
    assert next(trozos) == [3, 4, 5]


def test_chunked_solo_consume_lo_que_le_piden(solution):
    consumidos = []

    def fuente():
        for numero in range(100):
            consumidos.append(numero)
            yield numero

    trozos = solution.chunked(fuente(), 4)
    next(trozos)

    assert consumidos == [0, 1, 2, 3], "no debe leer más allá del trozo pedido"
