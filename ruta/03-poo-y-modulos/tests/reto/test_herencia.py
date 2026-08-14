def test_la_cuenta_base(solution):
    cuenta = solution.Account("Ana", 100_000)

    assert cuenta.describe() == "Ana: 100000"
    assert cuenta.fee_cents() == 500


def test_la_cuenta_base_arranca_sin_saldo(solution):
    assert solution.Account("Ana").balance_cents == 0


def test_la_cuenta_de_ahorro_extiende_la_descripcion(solution):
    cuenta = solution.SavingsAccount("Beto", 200_000, rate=0.03)

    assert cuenta.describe() == "Beto: 200000 (ahorro al 3.0%)"


def test_la_cuenta_de_ahorro_tiene_un_tipo_por_defecto(solution):
    assert solution.SavingsAccount("Beto").rate == 0.02


def test_la_cuenta_de_ahorro_hereda_la_comision(solution):
    assert solution.SavingsAccount("Beto", 1_000).fee_cents() == 500


def test_la_premium_encadena_las_tres_descripciones(solution):
    cuenta = solution.PremiumAccount("Caro", 500_000, rate=0.05)

    assert cuenta.describe() == "Caro: 500000 (ahorro al 5.0%) [premium]"


def test_la_premium_no_paga_comision(solution):
    assert solution.PremiumAccount("Caro", 500_000).fee_cents() == 0


def test_la_premium_sigue_siendo_una_cuenta(solution):
    cuenta = solution.PremiumAccount("Caro", 1_000)

    assert isinstance(cuenta, solution.Account)
    assert isinstance(cuenta, solution.SavingsAccount)


def test_el_mro_es_el_esperado(solution):
    nombres = [clase.__name__ for clase in solution.PremiumAccount.__mro__]

    assert nombres == ["PremiumAccount", "SavingsAccount", "Account", "object"]


def test_cambiar_la_base_cambia_a_todas(solution):
    """Si describe() se copiara en vez de extenderse, esto no se propagaría."""
    original = solution.Account.describe
    try:
        solution.Account.describe = lambda self: f"<{self.holder}>"
        cuenta = solution.PremiumAccount("Caro", 1_000, rate=0.05)

        assert cuenta.describe() == "<Caro> (ahorro al 5.0%) [premium]"
    finally:
        solution.Account.describe = original
