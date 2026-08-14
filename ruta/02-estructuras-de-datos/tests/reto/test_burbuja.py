import pytest


def test_ordena(solution):
    ordenada, _ = solution.bubble_sort([3, 1, 2])

    assert ordenada == [1, 2, 3]


def test_cuenta_los_intercambios(solution):
    _, intercambios = solution.bubble_sort([3, 1, 2])

    assert intercambios == 2


def test_una_lista_ya_ordenada_no_necesita_intercambios(solution):
    ordenada, intercambios = solution.bubble_sort([1, 2, 3, 4])

    assert ordenada == [1, 2, 3, 4]
    assert intercambios == 0


def test_una_lista_al_reves_da_el_maximo_de_intercambios(solution):
    """Con n elementos invertidos hay n*(n-1)/2 pares desordenados."""
    ordenada, intercambios = solution.bubble_sort([4, 3, 2, 1])

    assert ordenada == [1, 2, 3, 4]
    assert intercambios == 6


def test_dos_elementos(solution):
    assert solution.bubble_sort([2, 1]) == ([1, 2], 1)


@pytest.mark.parametrize("entrada", [[], [7]])
def test_listas_triviales(solution, entrada):
    ordenada, intercambios = solution.bubble_sort(entrada)

    assert ordenada == entrada
    assert intercambios == 0


def test_con_repetidos(solution):
    ordenada, _ = solution.bubble_sort([3, 1, 3, 1])

    assert ordenada == [1, 1, 3, 3]


def test_con_negativos_y_decimales(solution):
    ordenada, _ = solution.bubble_sort([2.5, -1, 0, -3.5])

    assert ordenada == [-3.5, -1, 0, 2.5]


def test_no_modifica_la_lista_recibida(solution):
    original = [3, 1, 2]

    solution.bubble_sort(original)

    assert original == [3, 1, 2]


def test_una_lista_larga(solution):
    entrada = list(range(20, 0, -1))

    ordenada, intercambios = solution.bubble_sort(entrada)

    assert ordenada == list(range(1, 21))
    assert intercambios == 190
