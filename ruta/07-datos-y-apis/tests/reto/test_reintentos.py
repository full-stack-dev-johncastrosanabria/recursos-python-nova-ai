"""El reloj se inyecta, así que estos tests corren en milisegundos.

Si `retry` llamara directamente a `time.sleep`, esta suite tardaría más de
siete segundos y nadie la ejecutaría al guardar.
"""

import pytest


class RelojFalso:
    """Apunta cuánto le pidieron dormir, sin dormir."""

    def __init__(self) -> None:
        self.esperas: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.esperas.append(seconds)


def operacion_que_falla(veces: int, resultado="ok"):
    """Falla las primeras `veces` llamadas y luego funciona."""
    estado = {"llamadas": 0}

    def operacion():
        estado["llamadas"] += 1
        if estado["llamadas"] <= veces:
            raise ConnectionError(f"fallo {estado['llamadas']}")
        return resultado

    operacion.estado = estado
    return operacion


def test_si_funciona_a_la_primera_no_espera(solution):
    reloj = RelojFalso()

    resultado = solution.retry(lambda: "ok", sleeper=reloj)

    assert resultado == "ok"
    assert reloj.esperas == []


def test_reintenta_hasta_que_funciona(solution):
    reloj = RelojFalso()
    operacion = operacion_que_falla(2)

    resultado = solution.retry(operacion, attempts=3, sleeper=reloj)

    assert resultado == "ok"
    assert operacion.estado["llamadas"] == 3


def test_la_espera_se_duplica_cada_vez(solution):
    reloj = RelojFalso()

    solution.retry(operacion_que_falla(2), attempts=3, base_delay=1.0, sleeper=reloj)

    assert reloj.esperas == [1.0, 2.0]


def test_respeta_el_base_delay(solution):
    reloj = RelojFalso()

    solution.retry(operacion_que_falla(3), attempts=4, base_delay=0.5, sleeper=reloj)

    assert reloj.esperas == [0.5, 1.0, 2.0]


def test_no_espera_despues_del_ultimo_intento(solution):
    """Con 3 intentos se duerme 2 veces. Dormir la tercera es tiempo tirado."""
    reloj = RelojFalso()

    with pytest.raises(ConnectionError):
        solution.retry(operacion_que_falla(99), attempts=3, sleeper=reloj)

    assert len(reloj.esperas) == 2


def test_relanza_la_ultima_excepcion(solution):
    reloj = RelojFalso()

    with pytest.raises(ConnectionError) as error:
        solution.retry(operacion_que_falla(99), attempts=2, sleeper=reloj)

    assert "fallo 2" in str(error.value)


def test_con_un_solo_intento_no_reintenta(solution):
    reloj = RelojFalso()
    operacion = operacion_que_falla(99)

    with pytest.raises(ConnectionError):
        solution.retry(operacion, attempts=1, sleeper=reloj)

    assert operacion.estado["llamadas"] == 1
    assert reloj.esperas == []


@pytest.mark.parametrize("intentos", [0, -1])
def test_un_numero_de_intentos_invalido_es_un_error(solution, intentos):
    with pytest.raises(ValueError):
        solution.retry(lambda: "ok", attempts=intentos)


def test_un_none_devuelto_es_un_resultado_valido(solution):
    """Solo se reintentan las excepciones, no los resultados que no gustan."""
    reloj = RelojFalso()
    llamadas = {"n": 0}

    def operacion():
        llamadas["n"] += 1
        return None

    assert solution.retry(operacion, sleeper=reloj) is None
    assert llamadas["n"] == 1
