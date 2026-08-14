"""Las piezas se inyectan, así que el pipeline se prueba solo.

`detect` y `render` de mentira dejan comprobar el orden y el cableado sin
montar el motor de reglas ni el renderizador de verdad.
"""

import pytest

BANCO = [{"ref": "TR-1", "cents": 500}, {"ref": "TR-2", "cents": 800}]
INTERNO = [{"ref": "TR-2", "cents": 800}, {"ref": "TR-3", "cents": 100}]


def sin_anomalias(transfers):
    return []


def informe_falso(result):
    return "informe"


def test_concilia_por_referencia(solution):
    resultado = solution.run_pipeline(
        BANCO, INTERNO, detect=sin_anomalias, render=informe_falso
    )

    assert resultado["matched"] == {"TR-2"}
    assert resultado["only_bank"] == {"TR-1"}
    assert resultado["only_internal"] == {"TR-3"}


def test_incluye_el_informe(solution):
    resultado = solution.run_pipeline(
        BANCO, INTERNO, detect=sin_anomalias, render=informe_falso
    )

    assert resultado["report"] == "informe"


def test_detect_recibe_los_movimientos_del_banco(solution):
    vistos = []

    def detect(transfers):
        vistos.append(list(transfers))
        return []

    solution.run_pipeline(BANCO, INTERNO, detect=detect, render=informe_falso)

    assert vistos == [BANCO]


def test_las_anomalias_llegan_al_resultado(solution):
    hallazgos = [{"ref": "TR-1", "rule": "r", "severity": "alta"}]

    resultado = solution.run_pipeline(
        BANCO, INTERNO, detect=lambda t: hallazgos, render=informe_falso
    )

    assert resultado["anomalies"] == hallazgos


def test_render_recibe_la_conciliacion_y_las_anomalias(solution):
    vistos = []

    def render(result):
        vistos.append(result)
        return "x"

    solution.run_pipeline(BANCO, INTERNO, detect=sin_anomalias, render=render)

    recibido = vistos[0]
    assert recibido["matched"] == {"TR-2"}
    assert recibido["only_bank"] == {"TR-1"}
    assert recibido["only_internal"] == {"TR-3"}
    assert recibido["anomalies"] == []


def test_las_referencias_repetidas_cuentan_una_vez(solution):
    banco = [{"ref": "TR-1"}, {"ref": "TR-1"}]

    resultado = solution.run_pipeline(
        banco, [], detect=sin_anomalias, render=informe_falso
    )

    assert resultado["only_bank"] == {"TR-1"}


def test_sin_datos(solution):
    resultado = solution.run_pipeline(
        [], [], detect=sin_anomalias, render=informe_falso
    )

    assert resultado["matched"] == set()
    assert resultado["only_bank"] == set()
    assert resultado["only_internal"] == set()


def test_no_modifica_las_entradas(solution):
    banco = [{"ref": "TR-1", "cents": 500}]
    interno = [{"ref": "TR-2", "cents": 100}]

    solution.run_pipeline(banco, interno, detect=sin_anomalias, render=informe_falso)

    assert banco == [{"ref": "TR-1", "cents": 500}]
    assert interno == [{"ref": "TR-2", "cents": 100}]


def test_un_fallo_de_detect_se_propaga(solution):
    def detect_roto(transfers):
        raise RuntimeError("bug en el motor de reglas")

    with pytest.raises(RuntimeError, match="motor de reglas"):
        solution.run_pipeline(BANCO, INTERNO, detect=detect_roto, render=informe_falso)


def test_funciona_con_las_piezas_de_verdad(solution):
    """El pipeline compuesto con un detector y un renderizador reales."""

    def detect(transfers):
        return [
            {"ref": t["ref"], "rule": "monto_alto", "severity": "alta"}
            for t in transfers
            if t["cents"] > 600
        ]

    def render(result):
        return f"anomalías: {len(result['anomalies'])}"

    resultado = solution.run_pipeline(BANCO, INTERNO, detect=detect, render=render)

    assert resultado["anomalies"] == [
        {"ref": "TR-2", "rule": "monto_alto", "severity": "alta"}
    ]
    assert resultado["report"] == "anomalías: 1"
