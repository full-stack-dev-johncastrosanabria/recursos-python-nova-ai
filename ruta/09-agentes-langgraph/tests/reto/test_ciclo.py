"""Un modelo de mentira que responde según un guion.

Así se prueba un agente: el no determinismo se sustituye por una secuencia
fija, y lo que se verifica es el bucle, no el modelo.
"""

import pytest


def modelo_con_guion(*respuestas):
    """Devuelve las respuestas en orden, una por llamada."""
    estado = {"llamadas": 0, "vistos": []}

    def modelo(messages):
        estado["vistos"].append(list(messages))
        respuesta = respuestas[min(estado["llamadas"], len(respuestas) - 1)]
        estado["llamadas"] += 1
        return respuesta

    modelo.estado = estado
    return modelo


TEXTO = {"type": "text", "text": "El saldo es 1500"}
USA_HERRAMIENTA = {
    "type": "tool_use",
    "name": "get_balance",
    "input": {"account": "CR01-0001"},
}

HERRAMIENTAS = {"get_balance": lambda account: 1_500}


def test_si_el_modelo_responde_texto_termina_enseguida(solution):
    resultado = solution.run_agent(modelo_con_guion(TEXTO), HERRAMIENTAS, "¿saldo?")

    assert resultado["answer"] == "El saldo es 1500"
    assert resultado["steps"] == 1


def test_ejecuta_la_herramienta_y_vuelve_a_preguntar(solution):
    modelo = modelo_con_guion(USA_HERRAMIENTA, TEXTO)

    resultado = solution.run_agent(modelo, HERRAMIENTAS, "¿saldo?")

    assert resultado["answer"] == "El saldo es 1500"
    assert resultado["steps"] == 2


def test_el_resultado_de_la_herramienta_llega_al_modelo(solution):
    modelo = modelo_con_guion(USA_HERRAMIENTA, TEXTO)

    solution.run_agent(modelo, HERRAMIENTAS, "¿saldo?")

    segunda_llamada = modelo.estado["vistos"][1]
    assert "1500" in str(segunda_llamada[-1]["content"])


def test_los_mensajes_empiezan_con_el_del_usuario(solution):
    resultado = solution.run_agent(modelo_con_guion(TEXTO), HERRAMIENTAS, "¿saldo?")

    assert resultado["messages"][0] == {"role": "user", "content": "¿saldo?"}


def test_varias_vueltas_de_herramienta(solution):
    modelo = modelo_con_guion(USA_HERRAMIENTA, USA_HERRAMIENTA, TEXTO)

    resultado = solution.run_agent(modelo, HERRAMIENTAS, "¿saldo?")

    assert resultado["steps"] == 3


def test_una_herramienta_desconocida_no_revienta_el_agente(solution):
    """El modelo puede corregirse si le dices qué pasó; una excepción no."""
    inexistente = {"type": "tool_use", "name": "no_existe", "input": {}}
    modelo = modelo_con_guion(inexistente, TEXTO)

    resultado = solution.run_agent(modelo, HERRAMIENTAS, "¿saldo?")

    assert resultado["answer"] == "El saldo es 1500"
    assert "error" in str(modelo.estado["vistos"][1][-1]["content"]).lower()


def test_una_herramienta_que_falla_tampoco_revienta(solution):
    def explota(**kwargs):
        raise RuntimeError("la base de datos no responde")

    modelo = modelo_con_guion(USA_HERRAMIENTA, TEXTO)

    resultado = solution.run_agent(modelo, {"get_balance": explota}, "¿saldo?")

    assert resultado["answer"] == "El saldo es 1500"
    assert "error" in str(modelo.estado["vistos"][1][-1]["content"]).lower()


def test_agotar_el_presupuesto_de_pasos_es_un_error(solution):
    modelo = modelo_con_guion(USA_HERRAMIENTA)  # nunca responde texto

    with pytest.raises(RuntimeError, match="pasos"):
        solution.run_agent(modelo, HERRAMIENTAS, "¿saldo?", max_steps=3)


def test_no_llama_al_modelo_mas_veces_que_el_tope(solution):
    modelo = modelo_con_guion(USA_HERRAMIENTA)

    with pytest.raises(RuntimeError, match="pasos"):
        solution.run_agent(modelo, HERRAMIENTAS, "¿saldo?", max_steps=3)

    assert modelo.estado["llamadas"] == 3
