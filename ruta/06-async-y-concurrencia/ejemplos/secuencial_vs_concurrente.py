"""La misma espera, tres formas de organizarla.

Córrelo con:
    uv run python ruta/06-async-y-concurrencia/ejemplos/secuencial_vs_concurrente.py
"""

import asyncio
from time import perf_counter

DEMORA = 0.2
CUANTAS = 6


async def consultar(numero: int) -> int:
    """Simula una llamada de red: espera sin usar CPU."""
    await asyncio.sleep(DEMORA)
    return numero * 10


async def secuencial() -> list[int]:
    resultados = []
    for numero in range(CUANTAS):
        resultados.append(await consultar(numero))  # una detrás de otra
    return resultados


async def concurrente() -> list[int]:
    return list(await asyncio.gather(*(consultar(n) for n in range(CUANTAS))))


async def concurrente_con_limite(limite: int) -> list[int]:
    semaforo = asyncio.Semaphore(limite)

    async def una(numero: int) -> int:
        async with semaforo:
            return await consultar(numero)

    return list(await asyncio.gather(*(una(n) for n in range(CUANTAS))))


async def main() -> None:
    print(f"{CUANTAS} consultas de {DEMORA}s cada una\n")

    for nombre, corrutina in (
        ("secuencial", secuencial()),
        ("concurrente", concurrente()),
        ("concurrente, límite 2", concurrente_con_limite(2)),
    ):
        inicio = perf_counter()
        resultados = await corrutina
        transcurrido = perf_counter() - inicio
        print(f"{nombre:<24} {transcurrido:>5.2f}s   {resultados}")

    print(
        "\nLa secuencial suma las esperas. La concurrente las solapa.\n"
        "La limitada elige el punto medio: rápida, pero sin lanzar seis\n"
        "peticiones a la vez contra una API que solo tolera dos."
    )


asyncio.run(main())
