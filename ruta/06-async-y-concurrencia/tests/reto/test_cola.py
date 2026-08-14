import asyncio

import pytest


class Rastreador:
    def __init__(self) -> None:
        self.en_vuelo = 0
        self.maximo_simultaneo = 0
        self.procesados: list = []

    def worker(self, demora: float = 0.01):
        async def trabajar(elemento):
            self.en_vuelo += 1
            self.maximo_simultaneo = max(self.maximo_simultaneo, self.en_vuelo)
            await asyncio.sleep(demora)
            self.en_vuelo -= 1
            self.procesados.append(elemento)
            return elemento * 2

        return trabajar


def test_devuelve_los_resultados_en_orden_de_entrada(solution):
    rastreador = Rastreador()

    resultados = asyncio.run(
        solution.run_queue([1, 2, 3, 4], rastreador.worker(), workers=2, max_queue=2)
    )

    assert resultados == [2, 4, 6, 8]


def test_procesa_todos_los_elementos(solution):
    rastreador = Rastreador()

    asyncio.run(solution.run_queue(list(range(10)), rastreador.worker(), workers=3))

    assert sorted(rastreador.procesados) == list(range(10))


def test_cada_elemento_se_procesa_una_sola_vez(solution):
    rastreador = Rastreador()

    asyncio.run(solution.run_queue(list(range(10)), rastreador.worker(), workers=3))

    assert len(rastreador.procesados) == 10


def test_respeta_el_numero_de_trabajadores(solution):
    rastreador = Rastreador()

    asyncio.run(
        solution.run_queue(list(range(12)), rastreador.worker(), workers=3, max_queue=4)
    )

    assert rastreador.maximo_simultaneo <= 3


def test_aprovecha_todos_los_trabajadores(solution):
    rastreador = Rastreador()

    asyncio.run(
        solution.run_queue(list(range(12)), rastreador.worker(), workers=3, max_queue=4)
    )

    assert rastreador.maximo_simultaneo == 3


def test_con_un_solo_trabajador_es_secuencial(solution):
    rastreador = Rastreador()

    asyncio.run(solution.run_queue([1, 2, 3], rastreador.worker(), workers=1))

    assert rastreador.maximo_simultaneo == 1
    assert rastreador.procesados == [1, 2, 3]


def test_el_orden_no_depende_de_quien_termine_antes(solution):
    """El primero tarda más, pero su resultado sigue saliendo primero."""

    async def worker(elemento):
        await asyncio.sleep(0.05 if elemento == 1 else 0.001)
        return elemento * 10

    resultados = asyncio.run(solution.run_queue([1, 2, 3], worker, workers=3))

    assert resultados == [10, 20, 30]


def test_sin_elementos(solution):
    rastreador = Rastreador()

    assert asyncio.run(solution.run_queue([], rastreador.worker())) == []


def test_una_cola_pequena_sigue_procesando_todo(solution):
    """Con max_queue=1 el productor se frena, pero no se pierde nada."""
    rastreador = Rastreador()

    resultados = asyncio.run(
        solution.run_queue([1, 2, 3, 4, 5], rastreador.worker(), workers=2, max_queue=1)
    )

    assert resultados == [2, 4, 6, 8, 10]


@pytest.mark.parametrize("trabajadores", [0, -1])
def test_un_numero_de_trabajadores_invalido_es_un_error(solution, trabajadores):
    with pytest.raises(ValueError):
        asyncio.run(solution.run_queue([1], lambda x: x, workers=trabajadores))


@pytest.mark.parametrize("tope", [0, -1])
def test_un_tope_de_cola_invalido_es_un_error(solution, tope):
    with pytest.raises(ValueError):
        asyncio.run(solution.run_queue([1], lambda x: x, max_queue=tope))


def test_no_deja_tareas_vivas(solution):
    """Los consumidores son bucles infinitos: hay que cancelarlos."""

    async def comprobar():
        rastreador = Rastreador()
        await solution.run_queue([1, 2, 3], rastreador.worker(), workers=2)
        return [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    assert asyncio.run(comprobar()) == []
