import asyncio

import pytest


class Rastreador:
    def __init__(self) -> None:
        self.en_vuelo = 0
        self.maximo_simultaneo = 0
        self.terminadas: list[int] = []

    def operacion(self, numero: int, demora: float = 0.01):
        async def ejecutar():
            self.en_vuelo += 1
            self.maximo_simultaneo = max(self.maximo_simultaneo, self.en_vuelo)
            await asyncio.sleep(demora)
            self.en_vuelo -= 1
            self.terminadas.append(numero)
            return numero

        return ejecutar


def test_respeta_el_limite(solution):
    rastreador = Rastreador()
    operaciones = [rastreador.operacion(n) for n in range(9)]

    asyncio.run(solution.run_limited(operaciones, limit=3))

    assert rastreador.maximo_simultaneo <= 3


def test_aprovecha_todo_el_limite(solution):
    """No basta con no pasarse: si solo va de una en una, no hay concurrencia."""
    rastreador = Rastreador()
    operaciones = [rastreador.operacion(n) for n in range(9)]

    asyncio.run(solution.run_limited(operaciones, limit=3))

    assert rastreador.maximo_simultaneo == 3


def test_devuelve_todos_los_resultados_en_orden(solution):
    rastreador = Rastreador()
    operaciones = [rastreador.operacion(n) for n in range(9)]

    resultados = asyncio.run(solution.run_limited(operaciones, limit=3))

    assert resultados == list(range(9))


def test_un_limite_mayor_que_las_operaciones_no_estorba(solution):
    rastreador = Rastreador()
    operaciones = [rastreador.operacion(n) for n in range(3)]

    resultados = asyncio.run(solution.run_limited(operaciones, limit=100))

    assert resultados == [0, 1, 2]
    assert rastreador.maximo_simultaneo == 3


def test_limite_de_uno_es_secuencial(solution):
    rastreador = Rastreador()
    operaciones = [rastreador.operacion(n) for n in range(4)]

    asyncio.run(solution.run_limited(operaciones, limit=1))

    assert rastreador.maximo_simultaneo == 1


def test_sin_operaciones(solution):
    assert asyncio.run(solution.run_limited([], limit=3)) == []


@pytest.mark.parametrize("limite", [0, -1, -10])
def test_un_limite_invalido_es_un_error(solution, limite):
    with pytest.raises(ValueError):
        asyncio.run(solution.run_limited([], limit=limite))
