MONTO_ALTO = {
    "name": "monto_alto",
    "severity": "alta",
    "check": lambda t: t["cents"] > 1_000_000,
}
SIN_REFERENCIA = {
    "name": "sin_referencia",
    "severity": "media",
    "check": lambda t: not t.get("reference"),
}
ROTA = {
    "name": "rota",
    "severity": "baja",
    "check": lambda t: t["campo_que_no_existe"] > 0,
}


def test_marca_la_transferencia_que_dispara_la_regla(solution):
    transferencias = [{"ref": "TR-1", "cents": 5_000_000}]

    assert solution.detect_anomalies(transferencias, [MONTO_ALTO]) == [
        {"ref": "TR-1", "rule": "monto_alto", "severity": "alta"}
    ]


def test_no_marca_la_que_no_dispara(solution):
    transferencias = [{"ref": "TR-2", "cents": 100}]

    assert solution.detect_anomalies(transferencias, [MONTO_ALTO]) == []


def test_recorre_todas_las_transferencias(solution):
    transferencias = [
        {"ref": "TR-1", "cents": 5_000_000},
        {"ref": "TR-2", "cents": 100},
        {"ref": "TR-3", "cents": 9_000_000},
    ]

    hallazgos = solution.detect_anomalies(transferencias, [MONTO_ALTO])

    assert [h["ref"] for h in hallazgos] == ["TR-1", "TR-3"]


def test_aplica_todas_las_reglas_a_cada_transferencia(solution):
    transferencias = [{"ref": "TR-1", "cents": 5_000_000}]

    hallazgos = solution.detect_anomalies(transferencias, [MONTO_ALTO, SIN_REFERENCIA])

    assert [h["rule"] for h in hallazgos] == ["monto_alto", "sin_referencia"]


def test_el_orden_es_determinista(solution):
    transferencias = [
        {"ref": "TR-1", "cents": 5_000_000},
        {"ref": "TR-2", "cents": 8_000_000},
    ]

    hallazgos = solution.detect_anomalies(transferencias, [MONTO_ALTO, SIN_REFERENCIA])

    assert [(h["ref"], h["rule"]) for h in hallazgos] == [
        ("TR-1", "monto_alto"),
        ("TR-1", "sin_referencia"),
        ("TR-2", "monto_alto"),
        ("TR-2", "sin_referencia"),
    ]


def test_una_regla_rota_se_marca_como_error(solution):
    """Un informe con la regla rota señalada vale más que ningún informe."""
    transferencias = [{"ref": "TR-1", "cents": 100}]

    hallazgos = solution.detect_anomalies(transferencias, [ROTA])

    assert hallazgos == [{"ref": "TR-1", "rule": "rota", "severity": "error"}]


def test_una_regla_rota_no_impide_las_demas(solution):
    transferencias = [{"ref": "TR-1", "cents": 5_000_000}]

    hallazgos = solution.detect_anomalies(transferencias, [ROTA, MONTO_ALTO])

    assert [h["rule"] for h in hallazgos] == ["rota", "monto_alto"]


def test_una_regla_rota_no_detiene_las_siguientes_transferencias(solution):
    transferencias = [{"ref": "TR-1", "cents": 100}, {"ref": "TR-2", "cents": 100}]

    hallazgos = solution.detect_anomalies(transferencias, [ROTA])

    assert [h["ref"] for h in hallazgos] == ["TR-1", "TR-2"]


def test_sin_reglas_no_hay_hallazgos(solution):
    assert solution.detect_anomalies([{"ref": "TR-1", "cents": 1}], []) == []


def test_sin_transferencias_no_hay_hallazgos(solution):
    assert solution.detect_anomalies([], [MONTO_ALTO]) == []


def test_no_modifica_las_transferencias(solution):
    transferencia = {"ref": "TR-1", "cents": 5_000_000}

    solution.detect_anomalies([transferencia], [MONTO_ALTO])

    assert transferencia == {"ref": "TR-1", "cents": 5_000_000}
