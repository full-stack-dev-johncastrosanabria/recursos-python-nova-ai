"""Solución de referencia del reto `rag`.

La validación de `overlap` no es cosmética: si el avance (`size - overlap`)
fuera cero o negativo, el bucle no terminaría nunca.
"""


def chunk_text(text: str, size: int, overlap: int = 0) -> list[str]:
    if size < 1:
        raise ValueError(f"size debe ser al menos 1, no {size}")
    if overlap < 0:
        raise ValueError(f"overlap no puede ser negativo, llegó {overlap}")
    if overlap >= size:
        raise ValueError(
            f"overlap ({overlap}) debe ser menor que size ({size}): "
            "si no, el troceo nunca avanzaría"
        )

    step = size - overlap

    return [text[start : start + size] for start in range(0, len(text), step)]
