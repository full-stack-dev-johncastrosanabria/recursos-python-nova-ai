import pytest


def test_sin_descuento_explicito_aplica_el_por_defecto(solution):
    assert solution.apply_discount(10_000) == 8_800


def test_aplica_el_descuento_que_se_le_pasa(solution):
    assert solution.apply_discount(10_000, 25) == 7_500


def test_un_descuento_de_cero_no_aplica_nada(solution):
    """El test que delata el bug del cero legítimo.

    Con `if not discount_percent` esto devolvería 8800: le habría aplicado el
    12% por defecto a quien pidió explícitamente ninguno.
    """
    assert solution.apply_discount(10_000, 0) == 10_000


def test_descuento_del_cien_por_cien(solution):
    assert solution.apply_discount(10_000, 100) == 0


def test_precio_cero(solution):
    assert solution.apply_discount(0, 50) == 0


def test_el_resultado_es_un_entero(solution):
    """Nada de floats en el recorrido del dinero."""
    assert isinstance(solution.apply_discount(9_999, 33), int)


@pytest.mark.parametrize("porcentaje", [-1, 101, 500])
def test_un_porcentaje_fuera_de_rango_es_un_error(solution, porcentaje):
    with pytest.raises(ValueError):
        solution.apply_discount(10_000, porcentaje)


def test_un_precio_negativo_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.apply_discount(-100)
