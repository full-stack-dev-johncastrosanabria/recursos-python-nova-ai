import pytest


def test_una_cuenta_nueva_empieza_sin_saldo(solution):
    assert solution.Account("Ana").balance_cents == 0


def test_una_cuenta_puede_nacer_con_saldo(solution):
    assert solution.Account("Ana", 5_000).balance_cents == 5_000


def test_deposit_suma_al_saldo(solution):
    cuenta = solution.Account("Ana")

    cuenta.deposit(1_500)

    assert cuenta.balance_cents == 1_500


def test_withdraw_resta_del_saldo(solution):
    cuenta = solution.Account("Ana", 1_500)

    cuenta.withdraw(500)

    assert cuenta.balance_cents == 1_000


@pytest.mark.parametrize("importe", [0, -1, -500])
def test_deposit_rechaza_importes_no_positivos(solution, importe):
    with pytest.raises(ValueError):
        solution.Account("Ana").deposit(importe)


@pytest.mark.parametrize("importe", [0, -1, -500])
def test_withdraw_rechaza_importes_no_positivos(solution, importe):
    with pytest.raises(ValueError):
        solution.Account("Ana", 1_000).withdraw(importe)


def test_no_se_puede_retirar_mas_de_lo_que_hay(solution):
    cuenta = solution.Account("Ana", 1_000)

    with pytest.raises(solution.InsufficientFunds):
        cuenta.withdraw(1_001)


def test_el_saldo_no_cambia_tras_un_retiro_fallido(solution):
    cuenta = solution.Account("Ana", 1_000)

    with pytest.raises(solution.InsufficientFunds):
        cuenta.withdraw(5_000)

    assert cuenta.balance_cents == 1_000


def test_el_error_de_saldo_dice_cuanto_habia(solution):
    """Quien lea esto en un log a las tres de la mañana lo va a agradecer."""
    cuenta = solution.Account("Ana", 1_000)

    with pytest.raises(solution.InsufficientFunds) as error:
        cuenta.withdraw(5_000)

    assert "1000" in str(error.value)


def test_insufficient_funds_no_es_un_value_error(solution):
    """Es un error de dominio: quien capture ValueError no debe atraparlo."""
    assert not issubclass(solution.InsufficientFunds, ValueError)


def test_repr_de_la_cuenta(solution):
    assert repr(solution.Account("Ana", 1_000)) == "Account('Ana', 1000)"
