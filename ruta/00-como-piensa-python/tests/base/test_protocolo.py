CON_STOCK = {"café": 3, "azúcar": 0}
AGOTADO = {"café": 0, "azúcar": 0}


def test_len_cuenta_los_productos_distintos(solution):
    assert len(solution.Inventory(CON_STOCK)) == 2


def test_len_cuenta_tambien_los_agotados(solution):
    assert len(solution.Inventory(AGOTADO)) == 2


def test_es_verdadero_si_queda_existencia_de_algo(solution):
    assert bool(solution.Inventory(CON_STOCK)) is True


def test_es_falso_si_todo_esta_a_cero(solution):
    """__bool__ gana sobre __len__: hay productos, pero no hay nada que vender."""
    assert bool(solution.Inventory(AGOTADO)) is False


def test_los_dos_protocolos_pueden_discrepar(solution):
    agotado = solution.Inventory(AGOTADO)

    assert len(agotado) == 2
    assert not agotado


def test_un_inventario_vacio_es_falso(solution):
    assert not solution.Inventory({})
    assert len(solution.Inventory({})) == 0


def test_el_if_usa_el_valor_de_verdad(solution):
    if solution.Inventory(AGOTADO):
        raise AssertionError("un inventario agotado no debería entrar en el if")

    if not solution.Inventory(CON_STOCK):
        raise AssertionError("un inventario con stock sí debería entrar")


def test_in_encuentra_los_productos(solution):
    inventario = solution.Inventory(CON_STOCK)

    assert "café" in inventario
    assert "té" not in inventario


def test_in_encuentra_tambien_los_agotados(solution):
    """Estar en el catálogo y tener existencias son preguntas distintas."""
    assert "azúcar" in solution.Inventory(CON_STOCK)


def test_no_comparte_el_diccionario_recibido(solution):
    stock = {"café": 3}
    inventario = solution.Inventory(stock)

    stock["café"] = 0

    assert bool(inventario) is True, "el inventario no debe verse afectado desde fuera"
