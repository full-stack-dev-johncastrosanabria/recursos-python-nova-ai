import pytest

TAREAS = [
    {"name": "extraer", "run": lambda ctx: [1, 2, 3]},
    {"name": "sumar", "run": lambda ctx: sum(ctx["extraer"])},
    {"name": "redactar", "run": lambda ctx: f"El total es {ctx['sumar']}"},
]


def test_encadena_las_tareas(solution):
    assert solution.run_crew(TAREAS) == {
        "extraer": [1, 2, 3],
        "sumar": 6,
        "redactar": "El total es 6",
    }


def test_cada_tarea_ve_lo_que_produjeron_las_anteriores(solution):
    vistos = []
    tareas = [
        {"name": "primera", "run": lambda ctx: "a"},
        {"name": "segunda", "run": lambda ctx: vistos.append(dict(ctx)) or "b"},
    ]

    solution.run_crew(tareas)

    assert vistos == [{"primera": "a"}]


def test_parte_de_un_contexto_inicial(solution):
    tareas = [{"name": "usar", "run": lambda ctx: ctx["ref"].lower()}]

    resultado = solution.run_crew(tareas, {"ref": "TR-1"})

    assert resultado == {"ref": "TR-1", "usar": "tr-1"}


def test_sin_tareas_devuelve_el_contexto_inicial(solution):
    assert solution.run_crew([], {"ref": "TR-1"}) == {"ref": "TR-1"}


def test_sin_tareas_ni_contexto(solution):
    assert solution.run_crew([]) == {}


def test_no_modifica_el_contexto_inicial(solution):
    inicial = {"ref": "TR-1"}

    solution.run_crew([{"name": "x", "run": lambda ctx: 1}], inicial)

    assert inicial == {"ref": "TR-1"}


def test_dos_tareas_con_el_mismo_nombre_es_un_error(solution):
    tareas = [
        {"name": "repetida", "run": lambda ctx: 1},
        {"name": "repetida", "run": lambda ctx: 2},
    ]

    with pytest.raises(ValueError):
        solution.run_crew(tareas)


def test_una_tarea_que_falla_se_envuelve_en_crew_failure(solution):
    def explota(ctx):
        raise RuntimeError("el modelo no respondió")

    tareas = [
        {"name": "primera", "run": lambda ctx: "ok"},
        {"name": "segunda", "run": explota},
    ]

    with pytest.raises(solution.CrewFailure):
        solution.run_crew(tareas)


def test_el_fallo_dice_que_tarea_fue(solution):
    def explota(ctx):
        raise RuntimeError("boom")

    with pytest.raises(solution.CrewFailure) as error:
        solution.run_crew([{"name": "analizar", "run": explota}])

    assert "analizar" in str(error.value)


def test_el_fallo_conserva_el_trabajo_ya_hecho(solution):
    """Perder lo que ya se pagó porque falló la última tarea es tirar dinero."""

    def explota(ctx):
        raise RuntimeError("boom")

    tareas = [
        {"name": "primera", "run": lambda ctx: "cara de calcular"},
        {"name": "segunda", "run": explota},
    ]

    with pytest.raises(solution.CrewFailure) as error:
        solution.run_crew(tareas)

    assert error.value.context["primera"] == "cara de calcular"
