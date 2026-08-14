import pytest


@pytest.mark.parametrize(
    "asunto",
    ["URGENTE: pago rechazado", "servicio caído", "El portal no funciona", "bloqueado"],
)
def test_las_urgencias_van_a_incidencia(solution, asunto):
    assert solution.route({"asunto": asunto, "cuerpo": ""}) == "incidencia"


def test_no_distingue_mayusculas(solution):
    assert solution.route({"asunto": "urgente", "cuerpo": ""}) == "incidencia"
    assert solution.route({"asunto": "URGENTE", "cuerpo": ""}) == "incidencia"


def test_una_referencia_en_el_asunto_va_a_conciliacion(solution):
    assert solution.route({"asunto": "consulta TR-0042", "cuerpo": ""}) == (
        "conciliacion"
    )


def test_una_referencia_en_el_cuerpo_tambien(solution):
    evento = {"asunto": "consulta", "cuerpo": "sobre la TR-99 de ayer"}

    assert solution.route(evento) == "conciliacion"


@pytest.mark.parametrize(
    "asunto", ["solicito presupuesto", "queremos una demo", "consulta de precio"]
)
def test_los_comerciales_van_a_ventas(solution, asunto):
    assert solution.route({"asunto": asunto, "cuerpo": ""}) == "ventas"


def test_lo_que_no_encaja_va_a_revision_humana(solution):
    """Sin una salida para lo desconocido, el sistema inventa una."""
    assert solution.route({"asunto": "hola", "cuerpo": "qué tal"}) == "revision_humana"


def test_la_prioridad_manda(solution):
    """URGENTE gana aunque también haya una referencia."""
    evento = {"asunto": "URGENTE: TR-0042 rechazada", "cuerpo": ""}

    assert solution.route(evento) == "incidencia"


def test_la_referencia_gana_a_lo_comercial(solution):
    evento = {"asunto": "precio de la TR-1", "cuerpo": ""}

    assert solution.route(evento) == "conciliacion"


def test_un_evento_sin_asunto(solution):
    assert solution.route({"cuerpo": "hola"}) == "revision_humana"


def test_un_evento_sin_cuerpo(solution):
    assert solution.route({"asunto": "urgente"}) == "incidencia"


def test_un_evento_vacio(solution):
    assert solution.route({}) == "revision_humana"


def test_siempre_devuelve_uno_de_los_cuatro(solution):
    destinos = {"incidencia", "conciliacion", "ventas", "revision_humana"}

    for evento in [{}, {"asunto": "x"}, {"cuerpo": "TR-1"}, {"asunto": "demo"}]:
        assert solution.route(evento) in destinos


def test_una_referencia_mal_formada_no_cuenta(solution):
    assert solution.route({"asunto": "sobre TR-", "cuerpo": ""}) == "revision_humana"
