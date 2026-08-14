def test_empieza_en_cero(solution):
    _, valor = solution.make_counter()

    assert valor() == 0


def test_puede_empezar_en_otro_numero(solution):
    _, valor = solution.make_counter(100)

    assert valor() == 100


def test_incrementar_devuelve_el_valor_nuevo(solution):
    incrementar, _ = solution.make_counter()

    assert incrementar() == 1
    assert incrementar() == 2
    assert incrementar() == 3


def test_valor_no_modifica_nada(solution):
    incrementar, valor = solution.make_counter()
    incrementar()

    assert valor() == 1
    assert valor() == 1
    assert valor() == 1


def test_las_dos_funciones_comparten_el_mismo_contador(solution):
    incrementar, valor = solution.make_counter(10)

    incrementar()
    incrementar()

    assert valor() == 12


def test_dos_contadores_son_independientes(solution):
    """Cada llamada a make_counter crea su propio ámbito."""
    inc_a, val_a = solution.make_counter()
    inc_b, val_b = solution.make_counter(100)

    inc_a()
    inc_a()

    assert val_a() == 2
    assert val_b() == 100


def test_devuelve_una_tupla_de_dos_funciones(solution):
    resultado = solution.make_counter()

    assert isinstance(resultado, tuple)
    assert len(resultado) == 2
    assert all(callable(f) for f in resultado)


def test_funciona_con_valores_negativos(solution):
    incrementar, valor = solution.make_counter(-3)

    incrementar()

    assert valor() == -2
