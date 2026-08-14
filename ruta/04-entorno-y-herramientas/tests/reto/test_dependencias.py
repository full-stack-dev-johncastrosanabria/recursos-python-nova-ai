import pytest

ARBOL = {
    "app": ["httpx", "pydantic"],
    "httpx": ["certifi"],
    "pydantic": [],
    "certifi": [],
}


def test_el_orden_del_ejemplo(solution):
    assert solution.install_order(ARBOL) == ["certifi", "httpx", "pydantic", "app"]


def test_cada_paquete_va_despues_de_sus_dependencias(solution):
    orden = solution.install_order(ARBOL)

    for paquete, requeridos in ARBOL.items():
        for requerido in requeridos:
            assert orden.index(requerido) < orden.index(paquete)


def test_una_cadena_simple(solution):
    grafo = {"c": ["b"], "b": ["a"], "a": []}

    assert solution.install_order(grafo) == ["a", "b", "c"]


def test_sin_dependencias_sale_todo_en_orden_alfabetico(solution):
    grafo = {"zeta": [], "alfa": [], "media": []}

    assert solution.install_order(grafo) == ["alfa", "media", "zeta"]


def test_un_grafo_vacio(solution):
    assert solution.install_order({}) == []


def test_un_solo_paquete(solution):
    assert solution.install_order({"solo": []}) == ["solo"]


def test_una_dependencia_que_no_es_clave_tambien_se_instala(solution):
    """`certifi` no aparece como clave, pero hay que instalarlo igual."""
    orden = solution.install_order({"httpx": ["certifi"]})

    assert orden == ["certifi", "httpx"]


def test_el_resultado_es_reproducible(solution):
    """Sin la regla alfabética, cada ejecución podría dar un orden distinto."""
    assert solution.install_order(ARBOL) == solution.install_order(ARBOL)


def test_un_ciclo_es_un_error(solution):
    with pytest.raises(solution.CircularDependency):
        solution.install_order({"a": ["b"], "b": ["a"]})


def test_un_ciclo_de_tres(solution):
    with pytest.raises(solution.CircularDependency):
        solution.install_order({"a": ["b"], "b": ["c"], "c": ["a"]})


def test_el_error_del_ciclo_nombra_los_paquetes(solution):
    with pytest.raises(solution.CircularDependency) as error:
        solution.install_order({"a": ["b"], "b": ["a"]})

    mensaje = str(error.value)
    assert "a" in mensaje
    assert "b" in mensaje


def test_un_ciclo_no_impide_detectar_lo_demas(solution):
    """Aunque parte del grafo sea instalable, el ciclo lo invalida."""
    with pytest.raises(solution.CircularDependency):
        solution.install_order({"ok": [], "a": ["b"], "b": ["a"]})


def test_un_paquete_que_depende_de_varios(solution):
    grafo = {"app": ["c", "b", "a"], "a": [], "b": [], "c": []}

    assert solution.install_order(grafo) == ["a", "b", "c", "app"]
