VACIO = {
    "matched": set(),
    "only_bank": set(),
    "only_internal": set(),
    "anomalies": [],
}


def test_el_titulo(solution):
    assert solution.render_report(VACIO).startswith("# Informe de conciliación\n")


def test_el_resumen_sale_siempre_aunque_todo_este_a_cero(solution):
    informe = solution.render_report(VACIO)

    assert "- Cuadran: 0" in informe
    assert "- Solo en el banco: 0" in informe
    assert "- Solo en registros internos: 0" in informe
    assert "- Anomalías: 0" in informe


def test_cuenta_bien(solution):
    resultado = {
        "matched": {"A", "B"},
        "only_bank": {"C"},
        "only_internal": {"D", "E", "F"},
        "anomalies": [{"ref": "C", "rule": "r", "severity": "alta"}],
    }

    informe = solution.render_report(resultado)

    assert "- Cuadran: 2" in informe
    assert "- Solo en el banco: 1" in informe
    assert "- Solo en registros internos: 3" in informe
    assert "- Anomalías: 1" in informe


def test_las_secciones_vacias_no_se_imprimen(solution):
    informe = solution.render_report(VACIO)

    assert "## Solo en el banco" not in informe
    assert "## Solo en registros internos" not in informe
    assert "## Anomalías" not in informe


def test_lista_las_referencias_ordenadas(solution):
    resultado = {**VACIO, "only_bank": {"TR-3", "TR-1", "TR-2"}}

    informe = solution.render_report(resultado)

    assert "- TR-1\n- TR-2\n- TR-3" in informe


def test_el_formato_de_las_anomalias(solution):
    resultado = {
        **VACIO,
        "anomalies": [{"ref": "TR-1", "rule": "monto_alto", "severity": "alta"}],
    }

    assert "- TR-1 · monto_alto (alta)" in solution.render_report(resultado)


def test_las_anomalias_conservan_su_orden(solution):
    resultado = {
        **VACIO,
        "anomalies": [
            {"ref": "TR-9", "rule": "b", "severity": "alta"},
            {"ref": "TR-1", "rule": "a", "severity": "baja"},
        ],
    }

    informe = solution.render_report(resultado)

    assert informe.index("TR-9") < informe.index("TR-1")


def test_termina_en_un_unico_salto_de_linea(solution):
    informe = solution.render_report(VACIO)

    assert informe.endswith("\n")
    assert not informe.endswith("\n\n")


def test_es_determinista(solution):
    """Dos ejecuciones sobre lo mismo dan el mismo texto: si no, no compara."""
    resultado = {
        "matched": {"B", "A"},
        "only_bank": {"Z", "Y", "X"},
        "only_internal": {"M"},
        "anomalies": [{"ref": "X", "rule": "r", "severity": "alta"}],
    }

    assert solution.render_report(resultado) == solution.render_report(resultado)


def test_informe_completo(solution):
    resultado = {
        "matched": {"TR-2"},
        "only_bank": {"TR-1"},
        "only_internal": {"TR-3"},
        "anomalies": [{"ref": "TR-1", "rule": "monto_alto", "severity": "alta"}],
    }

    assert solution.render_report(resultado) == (
        "# Informe de conciliación\n"
        "\n"
        "- Cuadran: 1\n"
        "- Solo en el banco: 1\n"
        "- Solo en registros internos: 1\n"
        "- Anomalías: 1\n"
        "\n"
        "## Solo en el banco\n"
        "\n"
        "- TR-1\n"
        "\n"
        "## Solo en registros internos\n"
        "\n"
        "- TR-3\n"
        "\n"
        "## Anomalías\n"
        "\n"
        "- TR-1 · monto_alto (alta)\n"
    )
