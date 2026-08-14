def test_reconcile_separa_las_tres_secciones(solution):
    resultado = solution.reconcile(["A", "B", "C"], ["B", "C", "D"])

    assert resultado["matched"] == {"B", "C"}
    assert resultado["only_bank"] == {"A"}
    assert resultado["only_internal"] == {"D"}


def test_reconcile_devuelve_conjuntos(solution):
    resultado = solution.reconcile(["A"], ["A"])

    for seccion in ("matched", "only_bank", "only_internal"):
        assert isinstance(resultado[seccion], set), f"{seccion} debería ser un set"


def test_reconcile_deduplica_las_referencias_repetidas(solution):
    resultado = solution.reconcile(["A", "A", "A"], ["A", "A"])

    assert resultado["matched"] == {"A"}
    assert resultado["only_bank"] == set()


def test_reconcile_cuando_no_cuadra_nada(solution):
    resultado = solution.reconcile(["A"], ["B"])

    assert resultado["matched"] == set()
    assert resultado["only_bank"] == {"A"}
    assert resultado["only_internal"] == {"B"}


def test_reconcile_con_un_lado_vacio(solution):
    resultado = solution.reconcile([], ["B", "C"])

    assert resultado["matched"] == set()
    assert resultado["only_bank"] == set()
    assert resultado["only_internal"] == {"B", "C"}


def test_reconcile_acepta_cualquier_iterable_no_solo_listas(solution):
    """Un generador que lea un CSV enorme tiene que servir igual que una lista."""
    banco = (ref for ref in ["A", "B"])
    interno = (ref for ref in ["B", "C"])

    resultado = solution.reconcile(banco, interno)

    assert resultado["matched"] == {"B"}
