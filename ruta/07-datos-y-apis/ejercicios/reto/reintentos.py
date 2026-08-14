"""Reto: reintentos con espera creciente, y probables sin esperar.

Escribe `retry`, que ejecuta `operation()` y lo reintenta si falla, esperando
cada vez el doble:

    retry(traer_datos, attempts=3, base_delay=1.0)

- Si la operación funciona, devuelve su resultado sin esperar nada.
- Si falla, espera `base_delay` y reintenta. Si vuelve a fallar, espera
  `base_delay * 2`. Luego `base_delay * 4`, y así.
- Si se agotan los intentos, **relanza la última excepción**. Tragarse el error
  y devolver `None` convertiría un fallo en datos corruptos.

El detalle que casi todo el mundo falla la primera vez: **no se espera después
del último intento**. Con `attempts=3` se duerme dos veces, no tres. Esperar
después del último es tiempo tirado antes de rendirse igual.

Reglas:

- `attempts` menor que 1 es un error: `ValueError`.
- Solo se reintentan las excepciones, no los resultados: si la operación
  devuelve `None`, eso es un resultado válido.

## Por qué se inyecta el reloj

`retry` recibe `sleeper`, la función con la que espera, que por defecto es
`time.sleep`. Así, en los tests se le pasa una que solo apunta cuánto le
pidieron dormir, y la suite corre en milisegundos en vez de en siete segundos.

Es la lección del módulo 05: si algo es difícil de probar, casi siempre está
mal diseñado. Un `time.sleep` incrustado hace la función imposible de probar
bien; recibirlo como argumento la hace trivial.
"""

import time
from collections.abc import Callable


def retry(
    operation: Callable,
    *,
    attempts: int = 3,
    base_delay: float = 1.0,
    sleeper: Callable[[float], None] = time.sleep,
):
    raise NotImplementedError("Borra esta línea y escribe tu solución")
