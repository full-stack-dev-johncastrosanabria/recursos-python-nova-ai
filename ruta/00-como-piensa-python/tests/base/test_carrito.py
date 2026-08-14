def test_add_item_devuelve_un_carrito_con_el_articulo(solution):
    assert solution.add_item("pan") == ["pan"]


def test_dos_llamadas_sin_carrito_no_comparten_lista(solution):
    """El test que delata el bug del argumento mutable por defecto."""
    primera = solution.add_item("pan")
    segunda = solution.add_item("leche")

    assert primera == ["pan"]
    assert segunda == ["leche"]
    assert primera is not segunda


def test_add_item_anade_sobre_el_carrito_recibido(solution):
    basket = ["pan", "leche"]

    resultado = solution.add_item("sal", basket)

    assert resultado == ["pan", "leche", "sal"]


def test_add_item_devuelve_el_mismo_carrito_que_recibe(solution):
    basket = ["pan"]

    assert solution.add_item("sal", basket) is basket
