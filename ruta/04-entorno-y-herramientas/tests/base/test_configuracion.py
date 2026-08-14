def test_la_capa_mas_especifica_gana(solution):
    resultado = solution.merge_config(
        {"host": "localhost", "port": 8000},
        {"port": 5432},
        {"host": "prod.internal"},
    )

    assert resultado == {"host": "prod.internal", "port": 5432}


def test_sin_capas_devuelve_diccionario_vacio(solution):
    assert solution.merge_config() == {}


def test_una_sola_capa_se_devuelve_tal_cual(solution):
    assert solution.merge_config({"a": 1}) == {"a": 1}


def test_los_valores_none_no_pisan_nada(solution):
    """Un argumento que nadie pasó no debe borrar lo que venía del archivo."""
    assert solution.merge_config({"a": 1}, {"a": None}) == {"a": 1}


def test_las_claves_nuevas_se_anaden(solution):
    assert solution.merge_config({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_no_modifica_las_capas_recibidas(solution):
    defaults = {"host": "localhost"}
    entorno = {"host": "prod"}

    solution.merge_config(defaults, entorno)

    assert defaults == {"host": "localhost"}
    assert entorno == {"host": "prod"}


def test_un_false_o_un_cero_si_pisan(solution):
    """Solo None significa 'no especificado'. False y 0 son valores legítimos."""
    assert solution.merge_config({"debug": True}, {"debug": False}) == {"debug": False}
    assert solution.merge_config({"reintentos": 3}, {"reintentos": 0}) == {
        "reintentos": 0
    }
