"""Ejercicio: el estado del grafo y sus reducers.

En un grafo de estado, cada nodo devuelve una **actualización**, no el estado
entero. Cómo se combina esa actualización con lo que ya había lo decide un
*reducer* por clave:

- Una clave **con** reducer acumula: `nuevo = reducer(anterior, actualizacion)`.
- Una clave **sin** reducer se reemplaza.

Escribe `apply_update`:

    apply_update(
        state={"messages": ["hola"], "steps": 2, "answer": "viejo"},
        update={"messages": ["¿qué tal?"], "steps": 1, "answer": "nuevo"},
        reducers={"messages": operator.add, "steps": operator.add},
    )
    -> {"messages": ["hola", "¿qué tal?"], "steps": 3, "answer": "nuevo"}

Reglas:

- Las claves que estaban en el estado y no vienen en la actualización se
  conservan sin tocar.
- Si una clave con reducer aparece por primera vez (no estaba en el estado), el
  reducer no se aplica: se toma el valor de la actualización tal cual. No hay
  nada con lo que combinar.
- **No modifiques el estado que recibes.** Devuelve un diccionario nuevo. Un
  nodo que muta el estado compartido es la forma más rápida de tener un grafo
  imposible de depurar.

Esto es todo el modelo de estado de LangGraph. El framework le añade
persistencia y dibujos; el fondo es este pliegue.
"""

from collections.abc import Callable, Mapping


def apply_update(
    state: Mapping, update: Mapping, reducers: Mapping[str, Callable]
) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
