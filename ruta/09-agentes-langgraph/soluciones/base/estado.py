"""Solución de referencia del ejercicio `estado`."""

from collections.abc import Callable, Mapping


def apply_update(
    state: Mapping, update: Mapping, reducers: Mapping[str, Callable]
) -> dict:
    merged = dict(state)

    for key, value in update.items():
        reducer = reducers.get(key)
        if reducer is not None and key in state:
            merged[key] = reducer(state[key], value)
        else:
            merged[key] = value

    return merged
