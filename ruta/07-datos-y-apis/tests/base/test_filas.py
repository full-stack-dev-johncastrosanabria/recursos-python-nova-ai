import pytest


def test_convierte_una_fila_completa(solution):
    assert solution.parse_rows([{"ref": "TR-1", "monto": "1500", "divisa": "USD"}]) == [
        {"ref": "TR-1", "amount_cents": 1500, "currency": "USD"}
    ]


def test_la_divisa_tiene_valor_por_defecto(solution):
    resultado = solution.parse_rows([{"ref": "TR-1", "monto": "990"}])

    assert resultado[0]["currency"] == "CRC"


def test_una_divisa_vacia_tambien_toma_el_defecto(solution):
    resultado = solution.parse_rows([{"ref": "TR-1", "monto": "990", "divisa": "  "}])

    assert resultado[0]["currency"] == "CRC"


def test_la_divisa_se_pasa_a_mayusculas(solution):
    resultado = solution.parse_rows([{"ref": "TR-1", "monto": "1", "divisa": "usd"}])

    assert resultado[0]["currency"] == "USD"


def test_la_referencia_se_limpia(solution):
    resultado = solution.parse_rows([{"ref": "  TR-1  ", "monto": "1"}])

    assert resultado[0]["ref"] == "TR-1"


def test_el_monto_sale_como_entero(solution):
    resultado = solution.parse_rows([{"ref": "TR-1", "monto": "1500"}])

    assert resultado[0]["amount_cents"] == 1500
    assert isinstance(resultado[0]["amount_cents"], int)


def test_varias_filas(solution):
    resultado = solution.parse_rows(
        [{"ref": "TR-1", "monto": "1"}, {"ref": "TR-2", "monto": "2"}]
    )

    assert [r["ref"] for r in resultado] == ["TR-1", "TR-2"]


def test_sin_filas(solution):
    assert solution.parse_rows([]) == []


@pytest.mark.parametrize("ref", ["", "   ", None])
def test_una_referencia_vacia_es_un_error(solution, ref):
    with pytest.raises(solution.RowError):
        solution.parse_rows([{"ref": ref, "monto": "1"}])


def test_falta_la_referencia(solution):
    with pytest.raises(solution.RowError):
        solution.parse_rows([{"monto": "1"}])


@pytest.mark.parametrize("monto", ["", "hola", "15.50", None])
def test_un_monto_invalido_es_un_error(solution, monto):
    with pytest.raises(solution.RowError):
        solution.parse_rows([{"ref": "TR-1", "monto": monto}])


def test_la_primera_fila_de_datos_es_la_linea_dos(solution):
    """La línea 1 es la cabecera del CSV."""
    with pytest.raises(solution.RowError) as error:
        solution.parse_rows([{"ref": "", "monto": "1"}])

    assert "2" in str(error.value)


def test_el_numero_de_linea_avanza(solution):
    filas = [
        {"ref": "TR-1", "monto": "1"},
        {"ref": "TR-2", "monto": "2"},
        {"ref": "TR-3", "monto": "roto"},
    ]

    with pytest.raises(solution.RowError) as error:
        solution.parse_rows(filas)

    assert "4" in str(error.value)


def test_row_error_es_un_value_error(solution):
    assert issubclass(solution.RowError, ValueError)
