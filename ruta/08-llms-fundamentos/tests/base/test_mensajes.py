def mensaje(rol: str, caracteres: int, marca: str) -> dict:
    """Un mensaje de tamaño conocido: `caracteres` // 4 tokens estimados."""
    return {"role": rol, "content": marca * caracteres}


def test_el_mensaje_nuevo_va_al_final(solution):
    peticion = solution.build_request("sistema", [], "¿qué tal?")

    assert peticion["messages"] == [{"role": "user", "content": "¿qué tal?"}]


def test_conserva_el_system_tal_cual(solution):
    peticion = solution.build_request("Eres un asistente.", [], "hola")

    assert peticion["system"] == "Eres un asistente."


def test_mantiene_el_historial_que_cabe(solution):
    historial = [
        {"role": "user", "content": "hola"},
        {"role": "assistant", "content": "¡hola!"},
    ]

    peticion = solution.build_request("s", historial, "¿qué tal?", 100)

    assert peticion["messages"] == [
        {"role": "user", "content": "hola"},
        {"role": "assistant", "content": "¡hola!"},
        {"role": "user", "content": "¿qué tal?"},
    ]


def test_recorta_los_mensajes_mas_viejos(solution):
    # Cuatro mensajes de 40 caracteres: 10 tokens estimados cada uno.
    historial = [mensaje("user", 40, str(n)) for n in range(4)]

    peticion = solution.build_request("s", historial, "nueva", 25)

    contenidos = [m["content"][0] for m in peticion["messages"][:-1]]
    assert contenidos == ["2", "3"], "debía quedarse con los dos más recientes"


def test_el_mensaje_nuevo_nunca_se_recorta(solution):
    """Aunque él solo se pase del presupuesto: es la pregunta a responder."""
    peticion = solution.build_request("s", [], "x" * 4_000, max_history_tokens=1)

    assert peticion["messages"][-1]["content"] == "x" * 4_000


def test_puede_vaciar_el_historial_entero(solution):
    historial = [mensaje("user", 400, "a")]

    peticion = solution.build_request("s", historial, "nueva", max_history_tokens=1)

    assert peticion["messages"] == [{"role": "user", "content": "nueva"}]


def test_el_system_no_cuenta_para_el_presupuesto(solution):
    """Son las reglas: recortarlas es peor que gastar tokens."""
    historial = [{"role": "user", "content": "hola"}]

    peticion = solution.build_request("x" * 10_000, historial, "nueva", 100)

    assert peticion["system"] == "x" * 10_000
    assert len(peticion["messages"]) == 2


def test_no_modifica_el_historial_recibido(solution):
    historial = [mensaje("user", 400, "a"), mensaje("user", 400, "b")]
    copia = list(historial)

    solution.build_request("s", historial, "nueva", max_history_tokens=1)

    assert historial == copia
