import pytest


def test_una_linea_sin_campos(solution):
    assert solution.format_log("INFO", "todo bien") == "INFO    todo bien"


def test_el_nivel_va_alineado_en_ocho(solution):
    linea = solution.format_log("ERROR", "falló")

    assert linea.startswith("ERROR   ")
    assert linea[:8] == "ERROR   "


def test_los_campos_van_detras(solution):
    linea = solution.format_log("INFO", "procesada", ref="TR-1", monto=1500)

    assert linea == "INFO    procesada monto=1500 ref=TR-1"


def test_los_campos_salen_ordenados(solution):
    """Ordenarlos hace que dos líneas del mismo evento se puedan comparar."""
    linea = solution.format_log("INFO", "x", zeta=1, alfa=2, media=3)

    assert linea == "INFO    x alfa=2 media=3 zeta=1"


def test_sin_campos_no_queda_un_espacio_colgando(solution):
    assert not solution.format_log("INFO", "x").endswith(" ")


def test_un_nivel_por_debajo_del_minimo_se_filtra(solution):
    assert solution.format_log("DEBUG", "detalle", min_level="INFO") is None


def test_el_nivel_igual_al_minimo_pasa(solution):
    assert solution.format_log("INFO", "x", min_level="INFO") is not None


def test_un_nivel_por_encima_pasa(solution):
    assert solution.format_log("ERROR", "x", min_level="INFO") is not None


def test_con_minimo_debug_pasa_todo(solution):
    assert solution.format_log("DEBUG", "x", min_level="DEBUG") is not None


def test_con_minimo_error_solo_pasan_los_errores(solution):
    assert solution.format_log("WARNING", "x", min_level="ERROR") is None
    assert solution.format_log("ERROR", "x", min_level="ERROR") is not None


@pytest.mark.parametrize("nivel", ["TRACE", "info", "", "CRITICAL"])
def test_un_nivel_desconocido_es_un_error(solution, nivel):
    with pytest.raises(ValueError):
        solution.format_log(nivel, "x")


def test_un_minimo_desconocido_tambien_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.format_log("INFO", "x", min_level="TRACE")


def test_el_error_menciona_el_nivel_recibido(solution):
    with pytest.raises(ValueError) as error:
        solution.format_log("TRACE", "x")

    assert "TRACE" in str(error.value)
