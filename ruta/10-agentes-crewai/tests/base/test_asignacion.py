import pytest

AGENTES = [
    {"role": "analista", "tools": {"sql", "buscar", "graficar"}},
    {"role": "consultor", "tools": {"buscar"}},
    {"role": "becario", "tools": set()},
]


def test_elige_un_agente_que_cubre_la_tarea(solution):
    tarea = {"name": "consultar", "needs": {"sql"}}

    assert solution.assign(AGENTES, tarea)["role"] == "analista"


def test_prefiere_al_mas_especializado(solution):
    """Los dos pueden buscar; gana el que tiene menos herramientas."""
    tarea = {"name": "investigar", "needs": {"buscar"}}

    assert solution.assign(AGENTES, tarea)["role"] == "consultor"


def test_una_tarea_sin_requisitos_va_al_mas_especializado(solution):
    tarea = {"name": "saludar", "needs": set()}

    assert solution.assign(AGENTES, tarea)["role"] == "becario"


def test_necesita_varias_herramientas(solution):
    tarea = {"name": "informe", "needs": {"sql", "graficar"}}

    assert solution.assign(AGENTES, tarea)["role"] == "analista"


def test_en_caso_de_empate_gana_el_primero(solution):
    agentes = [
        {"role": "primero", "tools": {"buscar"}},
        {"role": "segundo", "tools": {"buscar"}},
    ]

    assert solution.assign(agentes, {"name": "t", "needs": {"buscar"}})["role"] == (
        "primero"
    )


def test_si_ninguno_sirve_es_un_error(solution):
    tarea = {"name": "desplegar", "needs": {"kubernetes"}}

    with pytest.raises(solution.NoSuitableAgent):
        solution.assign(AGENTES, tarea)


def test_el_error_dice_que_herramienta_falta(solution):
    tarea = {"name": "desplegar", "needs": {"kubernetes"}}

    with pytest.raises(solution.NoSuitableAgent) as error:
        solution.assign(AGENTES, tarea)

    assert "kubernetes" in str(error.value)


def test_sin_agentes_es_un_error(solution):
    with pytest.raises(solution.NoSuitableAgent):
        solution.assign([], {"name": "t", "needs": {"buscar"}})


def test_una_tarea_sin_clave_needs_la_puede_hacer_cualquiera(solution):
    assert solution.assign(AGENTES, {"name": "t"})["role"] == "becario"
