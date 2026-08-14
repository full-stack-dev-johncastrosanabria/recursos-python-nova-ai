"""Reto: componer el sistema.

Escribe `run_pipeline`, que junta las etapas: concilia, detecta y redacta.

    run_pipeline(
        bank_moves=[{"ref": "TR-1", "cents": 500}],
        internal_records=[{"ref": "TR-2", "cents": 500}],
        detect=mi_detector,
        render=mi_renderizador,
    )

Devuelve:

    {
        "matched": set(...),
        "only_bank": set(...),
        "only_internal": set(...),
        "anomalies": [...],
        "report": "# Informe de conciliación\\n...",
    }

Qué hace, en orden:

1. **Concilia** por la clave `ref`: los tres conjuntos del módulo 02.
2. **Detecta** anomalías llamando a `detect(bank_moves)`. Las anomalías se
   buscan sobre los movimientos del banco, que es lo que llega de fuera.
3. **Redacta** llamando a `render(...)` con un diccionario que tenga las cuatro
   claves de conciliación y anomalías.

Por qué `detect` y `render` llegan como argumentos y no se importan: así el
pipeline se prueba sin montar el sistema entero, y cambiar el motor de reglas
no obliga a tocarlo. Es la misma inyección del reloj del módulo 07.

Reglas:

- Las referencias repetidas cuentan una vez.
- Ni `bank_moves` ni `internal_records` se modifican.
- Si `detect` o `render` fallan, la excepción se propaga tal cual: son piezas
  tuyas, y un fallo ahí es un bug, no una condición del negocio.
"""

from collections.abc import Callable, Iterable, Mapping


def run_pipeline(
    bank_moves: Iterable[Mapping],
    internal_records: Iterable[Mapping],
    *,
    detect: Callable,
    render: Callable,
) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
