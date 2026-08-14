"""Reto: trocear texto con solapamiento.

Es el primer paso de cualquier RAG y el que más determina la calidad del
resultado. Trozos grandes traen ruido; trozos pequeños parten las ideas por la
mitad. El solapamiento existe para que una frase cortada siga entera en alguno
de los dos trozos vecinos.

Escribe `chunk_text`:

    chunk_text("abcdefghij", size=4, overlap=1)
    -> ["abcd", "defg", "ghij", "j"]

Cada trozo empieza `size - overlap` caracteres después del anterior, así que el
solapamiento repite el final del trozo previo.

Reglas:

- El último trozo puede ser más corto.
- Texto vacío devuelve lista vacía.
- `size` menor que 1 es `ValueError`.
- `overlap` negativo es `ValueError`.
- **`overlap` mayor o igual que `size` es `ValueError`.** Esta es la regla que
  importa: sin ella, el avance sería cero o negativo y la función se quedaría
  produciendo trozos para siempre. Es un bucle infinito esperando a que alguien
  configure mal el troceador.
"""


def chunk_text(text: str, size: int, overlap: int = 0) -> list[str]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
