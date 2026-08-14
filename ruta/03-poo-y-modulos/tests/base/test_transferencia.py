import dataclasses

import pytest


def test_se_construye_con_los_campos_esperados(solution):
    t = solution.Transfer("CR-01", "CR-02", 150_000)

    assert t.origin == "CR-01"
    assert t.destination == "CR-02"
    assert t.amount_cents == 150_000
    assert t.currency == "CRC"


def test_la_divisa_tiene_un_valor_por_defecto(solution):
    assert solution.Transfer("CR-01", "CR-02", 100, "USD").currency == "USD"


def test_amount_convierte_centimos_a_unidades(solution):
    assert solution.Transfer("CR-01", "CR-02", 150_000).amount == 1_500.0


def test_rechaza_montos_no_positivos(solution):
    with pytest.raises(ValueError):
        solution.Transfer("CR-01", "CR-02", 0)

    with pytest.raises(ValueError):
        solution.Transfer("CR-01", "CR-02", -100)


def test_rechaza_transferirse_a_uno_mismo(solution):
    with pytest.raises(ValueError):
        solution.Transfer("CR-01", "CR-01", 100)


def test_compara_por_valor(solution):
    assert solution.Transfer("CR-01", "CR-02", 100) == solution.Transfer(
        "CR-01", "CR-02", 100
    )
    assert solution.Transfer("CR-01", "CR-02", 100) != solution.Transfer(
        "CR-01", "CR-02", 200
    )


def test_es_hashable_asi_que_entra_en_un_conjunto(solution):
    una = solution.Transfer("CR-01", "CR-02", 100)
    otra = solution.Transfer("CR-01", "CR-02", 100)

    assert len({una, otra}) == 1


def test_es_inmutable(solution):
    t = solution.Transfer("CR-01", "CR-02", 100)

    with pytest.raises(dataclasses.FrozenInstanceError):
        t.amount_cents = 5
