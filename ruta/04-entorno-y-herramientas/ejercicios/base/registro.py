"""Ejercicio: formatear una línea de log con nivel y campos.

Escribe `format_log`, que produce la línea que acabaría en el archivo de log —o
devuelve `None` si el nivel no llega al mínimo configurado.

    format_log("INFO", "transferencia procesada", ref="TR-1", monto=1500)
    -> "INFO     transferencia procesada monto=1500 ref=TR-1"

    format_log("DEBUG", "payload recibido", min_level="INFO")
    -> None      ← filtrado: DEBUG está por debajo de INFO

Reglas:

- Los niveles y su severidad están en `NIVELES`. Un nivel que no esté ahí —ni
  el que se registra ni el mínimo— es `ValueError`.
- El nombre del nivel va **alineado a la izquierda en 8 caracteres**, seguido
  del mensaje. Eso hace que los mensajes queden en columna al leer el archivo.
- Los campos extra van detrás, como `clave=valor`, separados por espacios y
  **ordenados alfabéticamente**. Ordenarlos no es capricho: hace que dos líneas
  del mismo evento se puedan comparar, y que un `grep` encuentre lo mismo
  siempre.
- Sin campos extra, la línea termina en el mensaje: nada de un espacio colgando.
- El mínimo por defecto es `"INFO"`, que es lo habitual en producción.

Fíjate en lo que **no** hace esta función: no imprime, no abre archivos y no
mira el reloj. Devuelve un texto. Por eso se puede probar en microsegundos y sin
tocar nada — la lección del módulo 05, adelantada.
"""

NIVELES = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}


def format_log(
    level: str, message: str, min_level: str = "INFO", **fields
) -> str | None:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
