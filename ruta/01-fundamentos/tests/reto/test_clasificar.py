import pytest


def test_un_pago_normal(solution):
    assert solution.describe({"tipo": "pago", "monto": 5_000}) == "pago de 5000"


def test_un_pago_grande(solution):
    assert (
        solution.describe({"tipo": "pago", "monto": 500_000}) == "pago grande de 500000"
    )


def test_el_limite_de_grande_no_se_incluye(solution):
    """Supera los 100.000, no los alcanza."""
    assert solution.describe({"tipo": "pago", "monto": 100_000}) == "pago de 100000"
    assert (
        solution.describe({"tipo": "pago", "monto": 100_001}) == "pago grande de 100001"
    )


def test_un_reverso(solution):
    assert solution.describe({"tipo": "reverso", "ref": "TR-1"}) == "reverso de TR-1"


def test_un_cierre(solution):
    assert solution.describe({"tipo": "cierre"}) == "cierre de día"


@pytest.mark.parametrize(
    "evento",
    [
        {},
        {"tipo": "loquesea"},
        {"monto": 500},
        {"tipo": "pago"},
        {"tipo": "reverso"},
    ],
)
def test_lo_que_no_encaja_es_desconocido(solution, evento):
    """Un pago sin monto o un reverso sin ref no revientan: son desconocidos."""
    assert solution.describe(evento) == "evento desconocido"


def test_las_claves_de_mas_no_estorban(solution):
    """Un patrón de diccionario comprueba lo que nombra, no exige exactitud."""
    evento = {"tipo": "pago", "monto": 5_000, "canal": "app", "hora": "10:32"}

    assert solution.describe(evento) == "pago de 5000"


def test_nunca_devuelve_none(solution):
    """Sin el `case _` final, esto saldría None en silencio."""
    assert solution.describe({"tipo": "algo_nuevo"}) is not None
