import math

import pytest


def test_el_clasico_de_los_floats(solution):
    assert solution.approx_equal(0.1 + 0.2, 0.3) is True


def test_dos_numeros_distintos_no_son_iguales(solution):
    assert solution.approx_equal(1.0, 1.1) is False


def test_la_igualdad_exacta_siempre_pasa(solution):
    assert solution.approx_equal(5, 5) is True
    assert solution.approx_equal(0, 0) is True


def test_la_tolerancia_relativa_escala_con_la_magnitud(solution):
    """Un céntimo sobre un millón es despreciable; sobre dos euros, no."""
    assert solution.approx_equal(1_000_000.5, 1_000_000, rel=1e-3) is True
    assert solution.approx_equal(2.5, 2.0, rel=1e-3) is False


def test_con_esperado_cero_manda_la_absoluta(solution):
    """Un porcentaje de cero es cero: la relativa no sirve aquí."""
    assert solution.approx_equal(1e-15, 0.0) is True
    assert solution.approx_equal(0.5, 0.0) is False


def test_se_puede_ajustar_la_tolerancia_absoluta(solution):
    assert solution.approx_equal(0.001, 0.0, abs_tol=0.01) is True
    assert solution.approx_equal(0.001, 0.0, abs_tol=1e-9) is False


def test_nan_nunca_es_igual_a_nada(solution):
    nan = float("nan")

    assert solution.approx_equal(nan, 1.0) is False
    assert solution.approx_equal(1.0, nan) is False
    assert solution.approx_equal(nan, nan) is False


def test_infinito_es_igual_a_si_mismo(solution):
    """Sin el atajo de la igualdad exacta, inf - inf daría nan."""
    assert solution.approx_equal(float("inf"), float("inf")) is True


def test_infinito_no_es_igual_a_un_numero(solution):
    assert solution.approx_equal(float("inf"), 1e308) is False


def test_funciona_con_negativos(solution):
    assert solution.approx_equal(-0.1 - 0.2, -0.3) is True


@pytest.mark.parametrize(("rel", "abs_tol"), [(-1e-6, 1e-12), (1e-6, -1e-12), (-1, -1)])
def test_una_tolerancia_negativa_es_un_error(solution, rel, abs_tol):
    with pytest.raises(ValueError):
        solution.approx_equal(1.0, 1.0, rel=rel, abs_tol=abs_tol)


def test_coincide_con_pytest_approx(solution):
    """La referencia: debería comportarse igual que la herramienta real."""
    for actual, esperado in [(0.1 + 0.2, 0.3), (1 / 3, 0.3333333333), (2.0, 2.0)]:
        assert solution.approx_equal(actual, esperado, rel=1e-6) == (
            actual == pytest.approx(esperado, rel=1e-6)
        )


def test_la_suma_acumulada_de_floats(solution):
    assert solution.approx_equal(sum([0.1] * 10), 1.0) is True
    assert math.isclose(sum([0.1] * 10), 1.0)
