import asyncio

import pytest


def operacion(valor, demora=0.01):
    async def ejecutar():
        await asyncio.sleep(demora)
        return valor

    return ejecutar


def operacion_rota(error, demora=0.01):
    async def ejecutar():
        await asyncio.sleep(demora)
        raise error

    return ejecutar


def test_devuelve_el_resultado_si_llega_a_tiempo(solution):
    assert asyncio.run(solution.with_timeout(operacion("ok"), seconds=1.0)) == "ok"


def test_devuelve_el_default_si_se_agota_el_plazo(solution):
    resultado = asyncio.run(
        solution.with_timeout(operacion("tarde", demora=1.0), 0.01, default="sin datos")
    )

    assert resultado == "sin datos"


def test_el_default_por_omision_es_none(solution):
    resultado = asyncio.run(solution.with_timeout(operacion("x", demora=1.0), 0.01))

    assert resultado is None


def test_no_propaga_el_timeout(solution):
    """Degradar con gracia: quien llama distingue por el valor devuelto."""
    asyncio.run(solution.with_timeout(operacion("x", demora=1.0), 0.01))


def test_las_demas_excepciones_si_se_propagan(solution):
    """Un fallo real y una tardanza no son lo mismo."""
    with pytest.raises(ValueError, match="algo falló"):
        asyncio.run(
            solution.with_timeout(operacion_rota(ValueError("algo falló")), 1.0)
        )


def test_un_fallo_rapido_no_se_confunde_con_un_timeout(solution):
    with pytest.raises(KeyError):
        asyncio.run(
            solution.with_timeout(
                operacion_rota(KeyError("falta"), demora=0.001),
                seconds=1.0,
                default="sin datos",
            )
        )


@pytest.mark.parametrize("plazo", [0, -1, -0.5])
def test_un_plazo_invalido_es_un_error(solution, plazo):
    with pytest.raises(ValueError):
        asyncio.run(solution.with_timeout(operacion("x"), plazo))


def test_devuelve_valores_falsy_tal_cual(solution):
    """Un 0 o una lista vacía son resultados legítimos, no ausencia."""
    assert asyncio.run(solution.with_timeout(operacion(0), 1.0, default="X")) == 0
    assert asyncio.run(solution.with_timeout(operacion([]), 1.0, default="X")) == []


def test_no_espera_mas_de_la_cuenta(solution):
    """Si esperase a que la operación termine, esto tardaría un segundo."""
    from time import perf_counter

    inicio = perf_counter()
    asyncio.run(solution.with_timeout(operacion("x", demora=1.0), 0.05))

    assert perf_counter() - inicio < 0.5
