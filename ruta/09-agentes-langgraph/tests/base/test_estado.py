import operator


def test_una_clave_con_reducer_acumula(solution):
    resultado = solution.apply_update(
        {"messages": ["hola"]},
        {"messages": ["¿qué tal?"]},
        {"messages": operator.add},
    )

    assert resultado["messages"] == ["hola", "¿qué tal?"]


def test_una_clave_sin_reducer_se_reemplaza(solution):
    resultado = solution.apply_update({"answer": "viejo"}, {"answer": "nuevo"}, {})

    assert resultado["answer"] == "nuevo"


def test_mezcla_acumulacion_y_reemplazo(solution):
    resultado = solution.apply_update(
        {"messages": ["hola"], "steps": 2, "answer": "viejo"},
        {"messages": ["adiós"], "steps": 1, "answer": "nuevo"},
        {"messages": operator.add, "steps": operator.add},
    )

    assert resultado == {
        "messages": ["hola", "adiós"],
        "steps": 3,
        "answer": "nuevo",
    }


def test_las_claves_no_actualizadas_se_conservan(solution):
    resultado = solution.apply_update({"a": 1, "b": 2}, {"a": 9}, {})

    assert resultado == {"a": 9, "b": 2}


def test_una_clave_nueva_no_aplica_el_reducer(solution):
    """No había nada con lo que combinar: se toma el valor tal cual."""
    resultado = solution.apply_update(
        {}, {"messages": ["hola"]}, {"messages": operator.add}
    )

    assert resultado["messages"] == ["hola"]


def test_no_modifica_el_estado_recibido(solution):
    """Un nodo que muta el estado compartido hace el grafo indepurable."""
    estado = {"messages": ["hola"], "steps": 1}

    solution.apply_update(estado, {"messages": ["otro"]}, {"messages": operator.add})

    assert estado == {"messages": ["hola"], "steps": 1}


def test_una_actualizacion_vacia_devuelve_el_mismo_contenido(solution):
    assert solution.apply_update({"a": 1}, {}, {}) == {"a": 1}


def test_funciona_con_reducers_propios(solution):
    def quedarse_con_el_mayor(anterior, nuevo):
        return max(anterior, nuevo)

    resultado = solution.apply_update(
        {"maximo": 10}, {"maximo": 3}, {"maximo": quedarse_con_el_mayor}
    )

    assert resultado["maximo"] == 10
