import pytest

TAREAS = [
    {"name": "extraer", "cost": 2, "run": lambda ctx: "datos"},
    {"name": "analizar", "cost": 5, "run": lambda ctx: "análisis"},
    {"name": "redactar", "cost": 4, "run": lambda ctx: "informe"},
]


def test_ejecuta_todo_si_el_presupuesto_alcanza(solution):
    resultado = solution.run_with_budget(TAREAS, budget=100)

    assert resultado["completed"] == ["extraer", "analizar", "redactar"]
    assert resultado["skipped"] == []
    assert resultado["spent"] == 11


def test_se_detiene_cuando_no_alcanza(solution):
    resultado = solution.run_with_budget(TAREAS, budget=8)

    assert resultado["completed"] == ["extraer", "analizar"]
    assert resultado["skipped"] == ["redactar"]
    assert resultado["spent"] == 7


def test_el_contexto_solo_trae_lo_ejecutado(solution):
    resultado = solution.run_with_budget(TAREAS, budget=8)

    assert resultado["context"] == {"extraer": "datos", "analizar": "análisis"}


def test_no_busca_una_tarea_mas_barata_despues(solution):
    """Las tareas están en orden porque unas dependen de otras."""
    tareas = [
        {"name": "cara", "cost": 10, "run": lambda ctx: "a"},
        {"name": "barata", "cost": 1, "run": lambda ctx: "b"},
    ]

    resultado = solution.run_with_budget(tareas, budget=5)

    assert resultado["completed"] == []
    assert resultado["skipped"] == ["cara", "barata"]


def test_presupuesto_exacto(solution):
    resultado = solution.run_with_budget(TAREAS, budget=11)

    assert resultado["completed"] == ["extraer", "analizar", "redactar"]
    assert resultado["spent"] == 11


def test_presupuesto_cero_no_ejecuta_nada(solution):
    resultado = solution.run_with_budget(TAREAS, budget=0)

    assert resultado["completed"] == []
    assert resultado["skipped"] == ["extraer", "analizar", "redactar"]
    assert resultado["spent"] == 0


def test_presupuesto_negativo_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.run_with_budget(TAREAS, budget=-1)


def test_las_tareas_reciben_el_contexto_acumulado(solution):
    tareas = [
        {"name": "primera", "cost": 1, "run": lambda ctx: 41},
        {"name": "segunda", "cost": 1, "run": lambda ctx: ctx["primera"] + 1},
    ]

    resultado = solution.run_with_budget(tareas, budget=10)

    assert resultado["context"]["segunda"] == 42


def test_parte_de_un_contexto_inicial(solution):
    tareas = [{"name": "usar", "cost": 1, "run": lambda ctx: ctx["ref"]}]

    resultado = solution.run_with_budget(tareas, budget=5, initial_context={"ref": "R"})

    assert resultado["context"]["usar"] == "R"


def test_si_una_tarea_falla_la_excepcion_se_propaga(solution):
    def explota(ctx):
        raise RuntimeError("boom")

    tareas = [{"name": "rota", "cost": 1, "run": explota}]

    with pytest.raises(RuntimeError, match="boom"):
        solution.run_with_budget(tareas, budget=10)


def test_sin_tareas(solution):
    resultado = solution.run_with_budget([], budget=10)

    assert resultado == {"context": {}, "completed": [], "skipped": [], "spent": 0}
