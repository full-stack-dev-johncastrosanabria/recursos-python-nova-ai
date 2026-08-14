import pytest

ANOMALIAS = [
    {"ref": "TR-3", "rule": "monto_alto", "severity": "media"},
    {"ref": "TR-1", "rule": "sin_ref", "severity": "alta"},
    {"ref": "TR-2", "rule": "duplicada", "severity": "alta"},
]


def test_ordena_por_severidad(solution):
    resultado = solution.prioritize(ANOMALIAS, budget=3)

    assert [a["severity"] for a in resultado] == ["alta", "alta", "media"]


def test_desempata_por_referencia(solution):
    """Sin esta regla no podrías comparar el informe de hoy con el de ayer."""
    resultado = solution.prioritize(ANOMALIAS, budget=2)

    assert [a["ref"] for a in resultado] == ["TR-1", "TR-2"]


def test_respeta_el_presupuesto(solution):
    assert len(solution.prioritize(ANOMALIAS, budget=2)) == 2


def test_un_presupuesto_mayor_que_las_anomalias(solution):
    assert len(solution.prioritize(ANOMALIAS, budget=100)) == 3


def test_presupuesto_cero(solution):
    """Hoy no hay dinero para investigar: es legítimo, no un error."""
    assert solution.prioritize(ANOMALIAS, budget=0) == []


def test_presupuesto_negativo_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.prioritize(ANOMALIAS, budget=-1)


def test_el_orden_completo_de_severidades(solution):
    anomalias = [
        {"ref": "a", "severity": "baja"},
        {"ref": "b", "severity": "error"},
        {"ref": "c", "severity": "media"},
        {"ref": "d", "severity": "alta"},
    ]

    resultado = solution.prioritize(anomalias, budget=4)

    assert [a["severity"] for a in resultado] == ["error", "alta", "media", "baja"]


def test_una_severidad_desconocida_va_al_final(solution):
    anomalias = [
        {"ref": "a", "severity": "inventada"},
        {"ref": "b", "severity": "baja"},
    ]

    resultado = solution.prioritize(anomalias, budget=2)

    assert [a["ref"] for a in resultado] == ["b", "a"]


def test_sin_anomalias(solution):
    assert solution.prioritize([], budget=5) == []


def test_no_modifica_la_lista_recibida(solution):
    original = list(ANOMALIAS)

    solution.prioritize(ANOMALIAS, budget=1)

    assert ANOMALIAS == original


def test_devuelve_los_mismos_objetos(solution):
    """No hace falta copiar los diccionarios: solo se eligen."""
    resultado = solution.prioritize(ANOMALIAS, budget=1)

    assert any(resultado[0] is a for a in ANOMALIAS)


def test_es_determinista(solution):
    assert solution.prioritize(ANOMALIAS, 2) == solution.prioritize(ANOMALIAS, 2)
