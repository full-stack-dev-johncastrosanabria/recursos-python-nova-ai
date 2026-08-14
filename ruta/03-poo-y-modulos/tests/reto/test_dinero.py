import pytest


def test_repr(solution):
    assert repr(solution.Money(1_000)) == "Money(1000, 'CRC')"


def test_igualdad_por_valor(solution):
    assert solution.Money(1_000) == solution.Money(1_000)
    assert solution.Money(1_000) != solution.Money(500)


def test_distinta_divisa_no_es_igual(solution):
    assert solution.Money(100, "CRC") != solution.Money(100, "USD")


def test_comparar_con_otro_tipo_da_falso_no_error(solution):
    """Devolver NotImplemented hace que Python convierta esto en False."""
    assert solution.Money(100) != "hola"
    assert not (solution.Money(100) == 100)


def test_orden_dentro_de_la_misma_divisa(solution):
    assert solution.Money(500) < solution.Money(1_000)
    assert not (solution.Money(1_000) < solution.Money(500))


def test_sorted_funciona_sin_key(solution):
    montos = [solution.Money(300), solution.Money(100), solution.Money(200)]

    assert sorted(montos) == [
        solution.Money(100),
        solution.Money(200),
        solution.Money(300),
    ]


def test_min_y_max_tambien(solution):
    montos = [solution.Money(300), solution.Money(100)]

    assert min(montos) == solution.Money(100)
    assert max(montos) == solution.Money(300)


def test_suma_dentro_de_la_misma_divisa(solution):
    assert solution.Money(500) + solution.Money(300) == solution.Money(800)


def test_ordenar_divisas_distintas_es_un_error(solution):
    """Aquí NotImplemented sí se convierte en TypeError, y debe hacerlo."""
    with pytest.raises(TypeError):
        _ = solution.Money(100, "CRC") < solution.Money(100, "USD")


def test_sumar_divisas_distintas_es_un_error(solution):
    with pytest.raises(TypeError):
        solution.Money(100, "CRC") + solution.Money(100, "USD")


def test_sumar_algo_que_no_es_dinero_es_un_error(solution):
    with pytest.raises(TypeError):
        solution.Money(100) + 100
