import pytest

COMPLETO = {
    "id": "TR-1",
    "amount": {"cents": 150_000, "currency": "CRC"},
    "parties": {
        "from": {"account": "CR01-0001"},
        "to": {"account": "CR01-0002"},
    },
    "reference": "factura 42",
}


def sin(payload: dict, *ruta: str) -> dict:
    """Copia el payload quitando la clave del final de la ruta."""
    import copy

    copia = copy.deepcopy(payload)
    actual = copia
    for clave in ruta[:-1]:
        actual = actual[clave]
    del actual[ruta[-1]]
    return copia


def test_aplana_el_payload_completo(solution):
    assert solution.normalize_transfer(COMPLETO) == {
        "id": "TR-1",
        "amount_cents": 150_000,
        "currency": "CRC",
        "origin": "CR01-0001",
        "destination": "CR01-0002",
        "reference": "factura 42",
    }


def test_la_divisa_tiene_valor_por_defecto(solution):
    resultado = solution.normalize_transfer(sin(COMPLETO, "amount", "currency"))

    assert resultado["currency"] == "CRC"


def test_la_referencia_ausente_es_none(solution):
    resultado = solution.normalize_transfer(sin(COMPLETO, "reference"))

    assert resultado["reference"] is None


@pytest.mark.parametrize(
    ("ruta", "esperado_en_mensaje"),
    [
        (("id",), "id"),
        (("amount", "cents"), "amount.cents"),
        (("parties", "from", "account"), "parties.from.account"),
        (("parties", "to", "account"), "parties.to.account"),
    ],
)
def test_un_obligatorio_que_falta_es_un_error(solution, ruta, esperado_en_mensaje):
    with pytest.raises(ValueError) as error:
        solution.normalize_transfer(sin(COMPLETO, *ruta))

    assert esperado_en_mensaje in str(error.value)


def test_falta_una_rama_entera(solution):
    with pytest.raises(ValueError):
        solution.normalize_transfer(sin(COMPLETO, "parties"))


def test_un_payload_vacio_falla_con_mensaje_util(solution):
    with pytest.raises(ValueError) as error:
        solution.normalize_transfer({})

    assert "id" in str(error.value)


def test_una_referencia_vacia_no_es_lo_mismo_que_ausente(solution):
    """La cadena vacía es un valor; se conserva tal cual."""
    payload = dict(COMPLETO, reference="")

    assert solution.normalize_transfer(payload)["reference"] == ""
