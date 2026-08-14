"""Estos tests no miden el reloj: cuentan cuántas operaciones coinciden dentro.

Medir tiempos hace los tests frágiles (una máquina lenta y fallan sin motivo).
Contar concurrencia es determinista: si las operaciones se ejecutan una detrás
de otra, nunca habrá dos a la vez, y eso se ve sin cronómetro.
"""

import asyncio


class Rastreador:
    """Fabrica operaciones asíncronas que registran cuántas coinciden."""

    def __init__(self) -> None:
        self.en_vuelo = 0
        self.maximo_simultaneo = 0
        self.terminadas: list[str] = []

    def operacion(self, nombre: str, demora: float = 0.01):
        async def ejecutar():
            self.en_vuelo += 1
            self.maximo_simultaneo = max(self.maximo_simultaneo, self.en_vuelo)
            await asyncio.sleep(demora)
            self.en_vuelo -= 1
            self.terminadas.append(nombre)
            return nombre

        return ejecutar


def test_devuelve_los_resultados_en_orden(solution):
    rastreador = Rastreador()
    operaciones = [rastreador.operacion(n) for n in ("a", "b", "c")]

    resultados = asyncio.run(solution.gather_all(operaciones))

    assert resultados == ["a", "b", "c"]


def test_las_operaciones_ocurren_a_la_vez(solution):
    """Si esto da 1, las estás esperando una detrás de otra."""
    rastreador = Rastreador()
    operaciones = [rastreador.operacion(n) for n in ("a", "b", "c")]

    asyncio.run(solution.gather_all(operaciones))

    assert rastreador.maximo_simultaneo == 3


def test_el_orden_de_salida_no_depende_del_de_finalizacion(solution):
    """La primera tarda más, pero sigue saliendo primera."""
    rastreador = Rastreador()
    operaciones = [
        rastreador.operacion("lenta", demora=0.05),
        rastreador.operacion("rapida", demora=0.01),
    ]

    resultados = asyncio.run(solution.gather_all(operaciones))

    assert resultados == ["lenta", "rapida"]
    assert rastreador.terminadas == ["rapida", "lenta"]


def test_sin_operaciones_devuelve_lista_vacia(solution):
    assert asyncio.run(solution.gather_all([])) == []


def test_devuelve_una_lista(solution):
    rastreador = Rastreador()

    resultados = asyncio.run(solution.gather_all([rastreador.operacion("a")]))

    assert isinstance(resultados, list)
