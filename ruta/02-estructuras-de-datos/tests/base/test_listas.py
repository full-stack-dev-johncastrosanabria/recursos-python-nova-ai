def test_anade_y_quita(solution):
    assert solution.organizar(["TR-003", "TR-001"], "TR-002", "TR-003") == [
        "TR-001",
        "TR-002",
    ]


def test_el_resultado_sale_ordenado(solution):
    assert solution.organizar(["TR-009", "TR-001", "TR-005"], "TR-003", "") == [
        "TR-001",
        "TR-003",
        "TR-005",
        "TR-009",
    ]


def test_no_anade_un_duplicado(solution):
    assert solution.organizar(["TR-001"], "TR-001", "") == ["TR-001"]


def test_quitar_algo_que_no_esta_no_es_un_error(solution):
    assert solution.organizar(["TR-001"], "TR-002", "TR-999") == ["TR-001", "TR-002"]


def test_no_modifica_la_lista_recibida(solution):
    original = ["TR-003", "TR-001"]

    solution.organizar(original, "TR-002", "TR-003")

    assert original == ["TR-003", "TR-001"]


def test_devuelve_una_lista_no_none(solution):
    """La trampa de `refs = refs.sort()`, que deja refs valiendo None."""
    resultado = solution.organizar(["TR-002", "TR-001"], "TR-003", "")

    assert resultado is not None
    assert isinstance(resultado, list)


def test_sobre_una_lista_vacia(solution):
    assert solution.organizar([], "TR-001", "TR-999") == ["TR-001"]


def test_quitar_deja_la_lista_vacia(solution):
    assert solution.organizar(["TR-001"], "TR-001", "TR-001") == []
