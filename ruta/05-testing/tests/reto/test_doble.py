import pytest


def test_el_spy_es_invocable(solution):
    espia = solution.Spy()

    espia()

    assert espia.call_count == 1


def test_el_spy_cuenta_las_llamadas(solution):
    espia = solution.Spy()

    espia()
    espia()
    espia()

    assert espia.call_count == 3


def test_el_spy_empieza_sin_llamadas(solution):
    espia = solution.Spy()

    assert espia.call_count == 0
    assert espia.calls == ()


def test_el_spy_registra_argumentos(solution):
    espia = solution.Spy()

    espia("TR-1", monto=1500)

    assert espia.calls == ((("TR-1",), {"monto": 1500}),)


def test_el_spy_conserva_el_orden(solution):
    espia = solution.Spy()

    espia("primera")
    espia("segunda")

    assert [args[0] for args, _ in espia.calls] == ["primera", "segunda"]


def test_calls_es_una_tupla(solution):
    """Quien lo consulta puede leer el registro, no falsearlo."""
    espia = solution.Spy()
    espia()

    assert isinstance(espia.calls, tuple)


def test_called_with_encuentra_la_llamada(solution):
    espia = solution.Spy()

    espia("TR-1", monto=1500)

    assert espia.called_with("TR-1", monto=1500) is True


def test_called_with_es_falso_si_no_coincide(solution):
    espia = solution.Spy()

    espia("TR-1", monto=1500)

    assert espia.called_with("TR-9") is False
    assert espia.called_with("TR-1") is False
    assert espia.called_with("TR-1", monto=999) is False


def test_called_with_busca_en_todas_las_llamadas(solution):
    espia = solution.Spy()

    espia("primera")
    espia("segunda")

    assert espia.called_with("primera") is True
    assert espia.called_with("segunda") is True


def test_el_spy_devuelve_none_por_defecto(solution):
    assert solution.Spy()() is None


def test_el_spy_puede_devolver_un_valor_fijo(solution):
    espia = solution.Spy(return_value="ok")

    assert espia() == "ok"
    assert espia("con", "argumentos") == "ok"


def test_el_reloj_empieza_donde_le_digas(solution):
    assert solution.FakeClock(start=100.0).now() == 100.0


def test_el_reloj_empieza_en_cero_por_defecto(solution):
    assert solution.FakeClock().now() == 0.0


def test_dormir_adelanta_el_reloj(solution):
    reloj = solution.FakeClock(start=100.0)

    reloj.sleep(2.5)

    assert reloj.now() == 102.5


def test_el_reloj_registra_lo_que_durmio(solution):
    reloj = solution.FakeClock()

    reloj.sleep(1.0)
    reloj.sleep(2.0)

    assert reloj.slept == (1.0, 2.0)


def test_slept_empieza_vacio(solution):
    assert solution.FakeClock().slept == ()


def test_slept_es_una_tupla(solution):
    reloj = solution.FakeClock()
    reloj.sleep(1)

    assert isinstance(reloj.slept, tuple)


def test_dormir_un_tiempo_negativo_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.FakeClock().sleep(-1)


def test_los_dos_dobles_juntos(solution):
    """Así se prueba una espera creciente sin esperar de verdad."""
    reloj = solution.FakeClock()
    operacion = solution.Spy(return_value="listo")

    for espera in (1.0, 2.0, 4.0):
        operacion()
        reloj.sleep(espera)

    assert operacion.call_count == 3
    assert reloj.slept == (1.0, 2.0, 4.0)
    assert reloj.now() == 7.0
