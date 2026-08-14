import pytest


@pytest.mark.parametrize(
    ("cents", "esperado"),
    [
        (0, "0.00"),
        (1, "0.01"),
        (99, "0.99"),
        (100, "1.00"),
        (150_000, "1,500.00"),
        (1_234_567, "12,345.67"),
        (-50_000, "-500.00"),
        (-1, "-0.01"),
    ],
)
def test_format_cents(solution, cents, esperado):
    assert solution.format_cents(cents) == esperado


def test_siempre_dos_decimales(solution):
    assert solution.format_cents(105) == "1.05"
    assert solution.format_cents(150) == "1.50"


def test_el_signo_va_delante_de_todo(solution):
    assert solution.format_cents(-1_234_567) == "-12,345.67"


def test_importes_grandes_son_exactos(solution):
    """Con float, un importe así ya habría perdido precisión."""
    assert solution.format_cents(99_999_999_999_999) == "999,999,999,999.99"


def test_no_hay_separador_por_debajo_de_mil(solution):
    assert solution.format_cents(99_999) == "999.99"
