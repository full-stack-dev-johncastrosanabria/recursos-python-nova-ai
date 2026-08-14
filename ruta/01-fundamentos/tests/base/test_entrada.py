import pytest


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("1500", 150_000),
        ("1500.50", 150_050),
        ("0.99", 99),
        ("0", 0),
        ("0.00", 0),
        ("1500.5", 150_050),
        ("1500.05", 150_005),
    ],
)
def test_convierte_a_centimos(solution, texto, esperado):
    assert solution.parse_amount(texto) == esperado


def test_ignora_los_espacios(solution):
    assert solution.parse_amount("   1500.50   ") == 150_050


def test_ignora_los_separadores_de_miles(solution):
    assert solution.parse_amount("1,500.50") == 150_050
    assert solution.parse_amount("1,234,567") == 123_456_700


def test_devuelve_un_entero(solution):
    assert isinstance(solution.parse_amount("1500.50"), int)


@pytest.mark.parametrize("texto", ["", "   ", "\t", "\n"])
def test_un_texto_vacio_es_un_error(solution, texto):
    with pytest.raises(ValueError):
        solution.parse_amount(texto)


@pytest.mark.parametrize("texto", ["hola", "12ab", "1.2.3", "€1500", "1 500"])
def test_lo_que_no_es_un_numero_es_un_error(solution, texto):
    with pytest.raises(ValueError):
        solution.parse_amount(texto)


def test_un_importe_negativo_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.parse_amount("-100")


def test_mas_de_dos_decimales_es_un_error(solution):
    """Redondear en silencio sería peor que rechazarlo."""
    with pytest.raises(ValueError):
        solution.parse_amount("10.999")


def test_el_mensaje_incluye_el_valor_recibido(solution):
    """Quien lea el log no tiene el dato delante."""
    with pytest.raises(ValueError) as error:
        solution.parse_amount("12ab")

    assert "12ab" in str(error.value)
