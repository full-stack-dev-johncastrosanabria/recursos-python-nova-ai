def get_balance(account: str, include_pending: bool = False) -> int:
    """Devuelve el saldo en céntimos de una cuenta.

    Este párrafo no debe aparecer en la descripción.
    """
    return 0


def sin_docstring(x: int) -> int:
    return x


def variados(texto: str, numero: int, decimal: float, bandera: bool) -> None:
    """Una de cada tipo."""


def raro(cosa) -> None:
    """Sin anotación."""


def test_toma_el_nombre_de_la_funcion(solution):
    assert solution.tool_schema(get_balance)["name"] == "get_balance"


def test_la_descripcion_es_la_primera_linea_del_docstring(solution):
    esquema = solution.tool_schema(get_balance)

    assert esquema["description"] == "Devuelve el saldo en céntimos de una cuenta."


def test_sin_docstring_la_descripcion_queda_vacia(solution):
    assert solution.tool_schema(sin_docstring)["description"] == ""


def test_el_esquema_es_un_objeto(solution):
    assert solution.tool_schema(get_balance)["input_schema"]["type"] == "object"


def test_traduce_los_tipos(solution):
    propiedades = solution.tool_schema(variados)["input_schema"]["properties"]

    assert propiedades == {
        "texto": {"type": "string"},
        "numero": {"type": "integer"},
        "decimal": {"type": "number"},
        "bandera": {"type": "boolean"},
    }


def test_un_tipo_desconocido_cae_en_string(solution):
    propiedades = solution.tool_schema(raro)["input_schema"]["properties"]

    assert propiedades["cosa"] == {"type": "string"}


def test_solo_son_obligatorios_los_que_no_tienen_defecto(solution):
    esquema = solution.tool_schema(get_balance)

    assert esquema["input_schema"]["required"] == ["account"]


def test_todos_obligatorios_cuando_ninguno_tiene_defecto(solution):
    esquema = solution.tool_schema(variados)

    assert esquema["input_schema"]["required"] == [
        "texto",
        "numero",
        "decimal",
        "bandera",
    ]


def test_el_retorno_no_aparece_en_el_esquema(solution):
    esquema = solution.tool_schema(get_balance)

    assert "return" not in esquema["input_schema"]["properties"]
