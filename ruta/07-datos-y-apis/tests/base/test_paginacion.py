import types


def hacer_fetch(paginas, registro=None):
    """Devuelve un fetch_page falso sobre una lista de páginas."""

    def fetch_page(numero):
        if registro is not None:
            registro.append(numero)
        return paginas[numero - 1]

    return fetch_page


def test_recorre_varias_paginas(solution):
    paginas = [
        {"items": ["a", "b"], "has_more": True},
        {"items": ["c"], "has_more": True},
        {"items": ["d", "e"], "has_more": False},
    ]

    assert list(solution.all_items(hacer_fetch(paginas))) == ["a", "b", "c", "d", "e"]


def test_una_sola_pagina(solution):
    paginas = [{"items": ["a"], "has_more": False}]

    assert list(solution.all_items(hacer_fetch(paginas))) == ["a"]


def test_sin_elementos(solution):
    paginas = [{"items": [], "has_more": False}]

    assert list(solution.all_items(hacer_fetch(paginas))) == []


def test_las_paginas_empiezan_en_uno(solution):
    registro = []
    paginas = [{"items": ["a"], "has_more": False}]

    list(solution.all_items(hacer_fetch(paginas, registro)))

    assert registro == [1]


def test_pide_las_paginas_en_orden(solution):
    registro = []
    paginas = [
        {"items": ["a"], "has_more": True},
        {"items": ["b"], "has_more": True},
        {"items": ["c"], "has_more": False},
    ]

    list(solution.all_items(hacer_fetch(paginas, registro)))

    assert registro == [1, 2, 3]


def test_devuelve_un_generador(solution):
    paginas = [{"items": ["a"], "has_more": False}]

    resultado = solution.all_items(hacer_fetch(paginas))

    assert isinstance(resultado, types.GeneratorType)


def test_es_perezoso_no_pide_paginas_de_mas(solution):
    """Quien consume dos elementos no debe provocar que se pidan cinco páginas."""
    registro = []
    paginas = [
        {"items": ["a", "b"], "has_more": True},
        {"items": ["c"], "has_more": True},
        {"items": ["d"], "has_more": False},
    ]

    flujo = solution.all_items(hacer_fetch(paginas, registro))
    next(flujo)
    next(flujo)

    assert registro == [1], "solo hacía falta la primera página"


def test_no_asume_cuantas_paginas_hay(solution):
    """El bug clásico: funcionar con dos páginas y perder la tercera."""
    paginas = [{"items": [n], "has_more": True} for n in range(9)]
    paginas.append({"items": [9], "has_more": False})

    assert list(solution.all_items(hacer_fetch(paginas))) == list(range(10))
