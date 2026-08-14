'''Ejercicio: el informe, determinista.

Escribe `render_report`, que convierte el resultado de la conciliación en un
documento markdown.

Entrada:

    {
        "matched": {"TR-2"},
        "only_bank": {"TR-1"},
        "only_internal": {"TR-3"},
        "anomalies": [{"ref": "TR-1", "rule": "monto_alto", "severity": "alta"}],
    }

Salida, exactamente con esta forma:

    """# Informe de conciliación

    - Cuadran: 1
    - Solo en el banco: 1
    - Solo en registros internos: 1
    - Anomalías: 1

    ## Solo en el banco

    - TR-1

    ## Solo en registros internos

    - TR-3

    ## Anomalías

    - TR-1 · monto_alto (alta)
    """

Reglas:

- Las referencias van **ordenadas alfabéticamente**. Es lo que hace el informe
  determinista, y sin eso no puedes comparar el de hoy con el de ayer.
- Las anomalías conservan el orden en que llegaron: ya venían ordenadas del
  motor de reglas.
- **Una sección vacía no se imprime.** Si no hay nada solo en el banco, esa
  sección desaparece entera. Un informe lleno de "(ninguna)" entrena a la gente
  a no leerlo.
- El resumen de arriba siempre sale, con los cuatro contadores, aunque valgan
  cero.
- El documento termina en un único salto de línea.
'''


def render_report(result: dict) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
