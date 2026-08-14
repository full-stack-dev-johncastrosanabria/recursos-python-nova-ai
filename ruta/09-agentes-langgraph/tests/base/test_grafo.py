import pytest

END = "__end__"


def test_un_grafo_de_un_solo_nodo(solution):
    nodes = {"unico": lambda state: {"visitado": True}}
    edges = {"unico": lambda state: END}

    final = solution.run_graph(nodes, edges, "unico", {})

    assert final == {"visitado": True}


def test_recorre_varios_nodos_en_cadena(solution):
    nodes = {
        "a": lambda state: {"paso": "a"},
        "b": lambda state: {"paso": "b"},
    }
    edges = {"a": lambda state: "b", "b": lambda state: END}

    assert solution.run_graph(nodes, edges, "a", {})["paso"] == "b"


def test_la_actualizacion_se_mezcla_sobre_el_estado(solution):
    nodes = {"a": lambda state: {"nuevo": 1}}
    edges = {"a": lambda state: END}

    final = solution.run_graph(nodes, edges, "a", {"previo": 0})

    assert final == {"previo": 0, "nuevo": 1}


def test_el_nodo_recibe_el_estado_actual(solution):
    nodes = {"sumar": lambda state: {"n": state["n"] + 1}}
    edges = {"sumar": lambda state: END}

    assert solution.run_graph(nodes, edges, "sumar", {"n": 41})["n"] == 42


def test_transicion_condicional(solution):
    nodes = {
        "contar": lambda state: {"n": state["n"] + 1},
        "final": lambda state: {"terminado": True},
    }
    edges = {
        "contar": lambda state: "contar" if state["n"] < 3 else "final",
        "final": lambda state: END,
    }

    final = solution.run_graph(nodes, edges, "contar", {"n": 0})

    assert final["n"] == 3
    assert final["terminado"] is True


def test_un_ciclo_con_salida_termina(solution):
    nodes = {
        "pensar": lambda state: {"pasos": state["pasos"] + 1},
        "herramienta": lambda state: {"datos": "listo"},
    }
    edges = {
        "pensar": lambda state: "herramienta" if state["pasos"] < 2 else END,
        "herramienta": lambda state: "pensar",
    }

    final = solution.run_graph(nodes, edges, "pensar", {"pasos": 0})

    assert final["pasos"] == 2
    assert final["datos"] == "listo"


def test_un_ciclo_sin_salida_revienta_con_el_tope(solution):
    """Un grafo con ciclos y sin tope es una factura abierta."""
    nodes = {"siempre": lambda state: {}}
    edges = {"siempre": lambda state: "siempre"}

    with pytest.raises(RuntimeError, match="pasos"):
        solution.run_graph(nodes, edges, "siempre", {}, max_steps=10)


def test_el_error_del_tope_menciona_el_limite(solution):
    nodes = {"siempre": lambda state: {}}
    edges = {"siempre": lambda state: "siempre"}

    with pytest.raises(RuntimeError) as error:
        solution.run_graph(nodes, edges, "siempre", {}, max_steps=7)

    assert "7" in str(error.value)


def test_un_nodo_inexistente_es_un_error(solution):
    nodes = {"a": lambda state: {}}
    edges = {"a": lambda state: "fantasma"}

    with pytest.raises(ValueError) as error:
        solution.run_graph(nodes, edges, "a", {})

    assert "fantasma" in str(error.value)


def test_un_nodo_sin_arista_es_un_error(solution):
    nodes = {"a": lambda state: {}, "b": lambda state: {}}
    edges = {"a": lambda state: "b"}

    with pytest.raises(ValueError):
        solution.run_graph(nodes, edges, "a", {})


def test_empezar_en_end_no_ejecuta_nada(solution):
    assert solution.run_graph({}, {}, END, {"intacto": True}) == {"intacto": True}


def test_no_modifica_el_estado_inicial(solution):
    nodes = {"a": lambda state: {"nuevo": 1}}
    edges = {"a": lambda state: END}
    inicial = {"previo": 0}

    solution.run_graph(nodes, edges, "a", inicial)

    assert inicial == {"previo": 0}
