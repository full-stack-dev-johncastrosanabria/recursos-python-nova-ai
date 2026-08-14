"""Solución de referencia del reto `doble`.

Las dos clases guardan su registro en una lista privada y lo exponen como
tupla: quien lo consulta puede leerlo, no reescribirlo.
"""


class Spy:
    def __init__(self, return_value=None) -> None:
        self._calls: list[tuple[tuple, dict]] = []
        self._return_value = return_value

    def __call__(self, *args, **kwargs):
        self._calls.append((args, kwargs))
        return self._return_value

    @property
    def calls(self) -> tuple[tuple[tuple, dict], ...]:
        return tuple(self._calls)

    @property
    def call_count(self) -> int:
        return len(self._calls)

    def called_with(self, *args, **kwargs) -> bool:
        return (args, kwargs) in self._calls


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self._now = start
        self._slept: list[float] = []

    def now(self) -> float:
        return self._now

    def sleep(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError(f"no se puede dormir un tiempo negativo: {seconds}")
        self._slept.append(seconds)
        self._now += seconds

    @property
    def slept(self) -> tuple[float, ...]:
        return tuple(self._slept)
