def test_la_baraja_tiene_52_cartas(solution):
    assert len(solution.Deck()) == 52


def test_indexacion_desde_el_principio(solution):
    deck = solution.Deck()

    assert deck[0] == "2 de picas"
    assert deck[12] == "A de picas"
    assert deck[13] == "2 de corazones"


def test_indices_negativos(solution):
    assert solution.Deck()[-1] == "A de tréboles"


def test_slicing(solution):
    assert solution.Deck()[:3] == ["2 de picas", "3 de picas", "4 de picas"]


def test_la_iteracion_funciona_sin_definir_iter(solution):
    """Python cae al protocolo de secuencia antiguo: pide [0], [1]… hasta IndexError."""
    cartas = list(solution.Deck())

    assert len(cartas) == 52
    assert cartas[0] == "2 de picas"
    assert cartas[-1] == "A de tréboles"


def test_el_operador_in_funciona_gracias_a_la_iteracion(solution):
    deck = solution.Deck()

    assert "A de corazones" in deck
    assert "Z de nada" not in deck


def test_no_hay_cartas_repetidas(solution):
    cartas = list(solution.Deck())

    assert len(set(cartas)) == 52
