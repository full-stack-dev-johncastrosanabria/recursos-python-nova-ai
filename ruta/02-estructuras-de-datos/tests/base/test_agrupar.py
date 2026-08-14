import pytest

TRANSFERENCIAS = [
    {"ref": "A", "currency": "CRC"},
    {"ref": "B", "currency": "USD"},
    {"ref": "C", "currency": "CRC"},
]


def test_group_by_currency_agrupa_por_divisa(solution):
    grupos = solution.group_by_currency(TRANSFERENCIAS)

    assert set(grupos) == {"CRC", "USD"}
    assert len(grupos["CRC"]) == 2
    assert len(grupos["USD"]) == 1


def test_group_by_currency_conserva_el_orden_dentro_del_grupo(solution):
    grupos = solution.group_by_currency(TRANSFERENCIAS)

    assert [t["ref"] for t in grupos["CRC"]] == ["A", "C"]


def test_group_by_currency_con_entrada_vacia(solution):
    assert solution.group_by_currency([]) == {}


def test_group_by_currency_devuelve_un_dict_normal(solution):
    """Un defaultdict que se escapa crea grupos con solo leerlos: eso es un bug."""
    grupos = solution.group_by_currency(TRANSFERENCIAS)

    with pytest.raises(KeyError):
        grupos["EUR"]

    assert set(grupos) == {"CRC", "USD"}, "consultar no debe crear grupos nuevos"


def test_group_by_currency_acepta_un_generador(solution):
    grupos = solution.group_by_currency(t for t in TRANSFERENCIAS)

    assert set(grupos) == {"CRC", "USD"}
