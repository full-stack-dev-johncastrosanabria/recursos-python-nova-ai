"""Reto: escribir dobles de prueba a mano.

La forma más limpia de sustituir una dependencia en un test casi nunca es una
librería de mocking: es **inyectarla**. Y cuando la dependencia entra por
parámetro, el doble es una clase de veinte líneas que escribes tú.

Implementa dos.

## `Spy` — registra cómo lo llamaron

    guardar = Spy()
    guardar("TR-1", monto=1500)
    guardar("TR-2", monto=900)

    guardar.call_count               -> 2
    guardar.calls                    -> ((("TR-1",), {"monto": 1500}),
                                         (("TR-2",), {"monto": 900}))
    guardar.called_with("TR-1", monto=1500)   -> True
    guardar.called_with("TR-9")               -> False

    respuesta = Spy(return_value="ok")
    respuesta()                      -> "ok"

Requisitos:

- Es **invocable**: se llama como una función. Eso significa `__call__`.
- `calls` devuelve una **tupla** de pares `(args, kwargs)`, en orden. Que sea
  tupla y no lista es a propósito: quien la reciba no debería poder falsear el
  registro.
- `call_count` es una propiedad, no un método.
- `called_with` es `True` si **alguna** de las llamadas coincide exactamente en
  posicionales y con nombre.
- Sin `return_value`, devuelve `None`.

## `FakeClock` — el tiempo bajo control

    reloj = FakeClock(start=100.0)

    reloj.now()          -> 100.0
    reloj.sleep(2.5)
    reloj.now()          -> 102.5     ← dormir adelanta el reloj, sin esperar
    reloj.slept          -> (2.5,)

Requisitos:

- `now()` devuelve el instante actual.
- `sleep(seconds)` **no espera**: registra la duración y adelanta el reloj.
- `slept` es una tupla con lo que se durmió, en orden.
- Dormir un tiempo negativo es `ValueError`.

Con estos dos, un test de la función `retry` del módulo 07 se escribe sin
esperar siete segundos y sin parchear nada:

    reloj = FakeClock()
    retry(operacion, sleeper=reloj.sleep)
    assert reloj.slept == (1.0, 2.0)
"""


class Spy:
    def __init__(self, return_value=None) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
