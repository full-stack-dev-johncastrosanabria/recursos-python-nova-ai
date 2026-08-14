"""Ejercicio: el corazón de la búsqueda semántica.

Toda búsqueda por significado se reduce a esto: convertir textos en vectores y
buscar los más cercanos. La parte de convertir la hace el modelo de embeddings;
la de buscar es aritmética, y es la que vas a escribir.

Dos funciones:

    cosine_similarity([1, 0], [1, 0])    -> 1.0     misma dirección
    cosine_similarity([1, 0], [0, 1])    -> 0.0     perpendiculares
    cosine_similarity([1, 0], [-1, 0])   -> -1.0    opuestos

    top_k(
        query=[1, 0],
        vectors={"a": [0.9, 0.1], "b": [0, 1], "c": [1, 0]},
        k=2,
    )
    -> [("c", 1.0), ("a", 0.994...)]

La **similitud coseno** es el coseno del ángulo entre dos vectores:

    similitud = (a · b) / (|a| * |b|)

donde `a · b` es el producto punto (sumar los productos elemento a elemento) y
`|a|` es la longitud del vector (la raíz de la suma de sus cuadrados).

Se usa el coseno y no la distancia normal porque **mide dirección, no
magnitud**: dos textos sobre el mismo tema quedan alineados aunque uno sea
mucho más largo que el otro.

Reglas de `cosine_similarity`:

- Vectores de distinta longitud: `ValueError`.
- Vectores vacíos: `ValueError`.
- Un vector de solo ceros no tiene dirección, así que el coseno no está
  definido: devuelve `0.0` en vez de dividir entre cero.

Reglas de `top_k`:

- Devuelve una lista de pares `(nombre, similitud)`, **de mayor a menor**.
- Si hay empate en la similitud, gana el nombre alfabéticamente menor. Sin esa
  regla el resultado no sería reproducible.
- `k` mayor que el número de vectores devuelve todos los que haya.
- `k` menor que 1 es `ValueError`.
- Sin vectores, lista vacía.
"""

from collections.abc import Sequence


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def top_k(
    query: Sequence[float], vectors: dict[str, Sequence[float]], k: int = 3
) -> list[tuple[str, float]]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
