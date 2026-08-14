"""Solución de referencia del ejercicio `informe`.

Se construye una lista de líneas y se une al final: sale más legible que ir
concatenando, y el `"\\n".join` deja el control del salto final en un solo
sitio.
"""


def render_report(result: dict) -> str:
    matched = result.get("matched", set())
    only_bank = result.get("only_bank", set())
    only_internal = result.get("only_internal", set())
    anomalies = result.get("anomalies", [])

    lines = [
        "# Informe de conciliación",
        "",
        f"- Cuadran: {len(matched)}",
        f"- Solo en el banco: {len(only_bank)}",
        f"- Solo en registros internos: {len(only_internal)}",
        f"- Anomalías: {len(anomalies)}",
    ]

    if only_bank:
        lines += ["", "## Solo en el banco", ""]
        lines += [f"- {ref}" for ref in sorted(only_bank)]

    if only_internal:
        lines += ["", "## Solo en registros internos", ""]
        lines += [f"- {ref}" for ref in sorted(only_internal)]

    if anomalies:
        lines += ["", "## Anomalías", ""]
        lines += [f"- {a['ref']} · {a['rule']} ({a['severity']})" for a in anomalies]

    return "\n".join(lines) + "\n"
