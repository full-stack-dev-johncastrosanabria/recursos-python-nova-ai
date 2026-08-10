# Cheatsheet · pytest

## Ejecutar

```bash
uv run pytest                                   # todo
uv run pytest ruta/01-fundamentos               # un módulo
uv run pytest ruta/01-fundamentos/tests/base    # solo los de nivel base
uv run pytest -k saludo                         # los que lleven "saludo"
uv run pytest -x                                # parar en el primer fallo
uv run pytest -v                                # nombre de cada test
uv run pytest --lf                              # solo los que fallaron
```

## Comprobaciones

```python
assert resultado == esperado
assert "texto" in respuesta
assert isinstance(valor, dict)
```

Números decimales, nunca con `==`:

```python
import pytest

assert resultado == pytest.approx(97.88)
```

Esperar un error:

```python
with pytest.raises(ValueError):
    summarize([])
```

## Varios casos, un test

```python
@pytest.mark.parametrize(
    ("celsius", "fahrenheit"),
    [(0, 32), (100, 212), (-40, -40)],
)
def test_conversion(solution, celsius, fahrenheit):
    assert solution.celsius_to_fahrenheit(celsius) == fahrenheit
```

## La fixture `solution`

En este repositorio los tests no importan el ejercicio: piden `solution`.

```python
def test_greet(solution):
    assert solution.greet("Ana") == "Hola, Ana"
```

Por defecto carga tu archivo de `ejercicios/`. Con `NOVA_SOLUCIONES=1` carga el
de `soluciones/`, que es como corre el CI.
