"""Fixtures: preparar lo que el test necesita, y que cada test reciba lo suyo.

`libro_vacio` y `libro_con_movimientos` se construyen de cero para cada test
que las pide. Por eso ninguno de estos tests puede ensuciar a otro, y por eso
da igual el orden en que se ejecuten.
"""

import pytest


@pytest.fixture
def libro_vacio(solution):
    return solution.Ledger()


@pytest.fixture
def libro_con_movimientos(solution):
    libro = solution.Ledger()
    libro.add("TR-001", 1_500)
    libro.add("TR-002", 2_500)
    return libro


def test_un_libro_nuevo_esta_vacio(libro_vacio):
    assert libro_vacio.balance == 0
    assert len(libro_vacio) == 0
    assert libro_vacio.entries() == ()


def test_el_saldo_suma_las_entradas(libro_con_movimientos):
    assert libro_con_movimientos.balance == 4_000


def test_la_longitud_cuenta_los_movimientos(libro_con_movimientos):
    assert len(libro_con_movimientos) == 2


def test_las_entradas_conservan_el_orden(libro_con_movimientos):
    assert libro_con_movimientos.entries() == (("TR-001", 1_500), ("TR-002", 2_500))


def test_las_entradas_se_devuelven_como_tupla(libro_con_movimientos):
    """Si devolviera la lista interna, quien la reciba podría romper el saldo."""
    assert isinstance(libro_con_movimientos.entries(), tuple)


def test_cada_test_recibe_un_libro_nuevo(libro_vacio):
    """Este test pasa siempre, ejecútese antes o después de los otros."""
    libro_vacio.add("TR-999", 100)

    assert len(libro_vacio) == 1


def test_una_referencia_repetida_es_un_error(solution, libro_con_movimientos):
    """Si un webhook llega dos veces, no puede contarse dos veces."""
    with pytest.raises(solution.DuplicateEntry):
        libro_con_movimientos.add("TR-001", 999)


def test_el_saldo_no_cambia_tras_un_duplicado(solution, libro_con_movimientos):
    with pytest.raises(solution.DuplicateEntry):
        libro_con_movimientos.add("TR-001", 999)

    assert libro_con_movimientos.balance == 4_000


@pytest.mark.parametrize("importe", [0, -1, -5_000])
def test_los_importes_no_positivos_se_rechazan(libro_vacio, importe):
    with pytest.raises(ValueError):
        libro_vacio.add("TR-003", importe)


def test_el_error_de_duplicado_dice_que_referencia(solution, libro_con_movimientos):
    with pytest.raises(solution.DuplicateEntry) as error:
        libro_con_movimientos.add("TR-001", 999)

    assert "TR-001" in str(error.value)
