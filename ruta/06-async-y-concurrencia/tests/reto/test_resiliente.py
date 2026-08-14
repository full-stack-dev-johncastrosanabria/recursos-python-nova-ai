import asyncio


def operacion_ok(valor, demora=0.01):
    async def ejecutar():
        await asyncio.sleep(demora)
        return valor

    return ejecutar


def operacion_rota(error, demora=0.01):
    async def ejecutar():
        await asyncio.sleep(demora)
        raise error

    return ejecutar


def test_todo_bien(solution):
    resultados = asyncio.run(
        solution.gather_settled([operacion_ok("a"), operacion_ok("b")])
    )

    assert resultados == [(True, "a"), (True, "b")]


def test_marca_los_fallos_sin_propagarlos(solution):
    fallo = ValueError("vaya")

    resultados = asyncio.run(
        solution.gather_settled([operacion_ok("a"), operacion_rota(fallo)])
    )

    assert resultados[0] == (True, "a")
    assert resultados[1][0] is False
    assert resultados[1][1] is fallo


def test_un_fallo_no_impide_que_las_demas_terminen(solution):
    """Lo importante del reto: la segunda revienta y las otras dos siguen."""
    terminadas = []

    def registrar(nombre, demora):
        async def ejecutar():
            await asyncio.sleep(demora)
            terminadas.append(nombre)
            return nombre

        return ejecutar

    operaciones = [
        registrar("primera", 0.01),
        operacion_rota(RuntimeError("boom"), demora=0.001),
        registrar("tercera", 0.02),
    ]

    resultados = asyncio.run(solution.gather_settled(operaciones))

    assert sorted(terminadas) == ["primera", "tercera"]
    assert [ok for ok, _ in resultados] == [True, False, True]


def test_conserva_el_orden_de_entrada(solution):
    operaciones = [
        operacion_ok("lenta", demora=0.05),
        operacion_ok("rapida", demora=0.001),
    ]

    resultados = asyncio.run(solution.gather_settled(operaciones))

    assert [valor for _, valor in resultados] == ["lenta", "rapida"]


def test_devuelve_la_excepcion_no_su_mensaje(solution):
    fallo = KeyError("falta")

    resultados = asyncio.run(solution.gather_settled([operacion_rota(fallo)]))

    assert isinstance(resultados[0][1], KeyError)


def test_sin_operaciones(solution):
    assert asyncio.run(solution.gather_settled([])) == []


def test_todas_fallan(solution):
    resultados = asyncio.run(
        solution.gather_settled(
            [operacion_rota(ValueError("a")), operacion_rota(ValueError("b"))]
        )
    )

    assert [ok for ok, _ in resultados] == [False, False]
