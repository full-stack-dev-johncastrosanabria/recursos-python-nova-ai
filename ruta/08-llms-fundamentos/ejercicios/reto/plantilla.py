"""Reto: rellenar un prompt sin que el contenido te inyecte instrucciones.

Un prompt casi nunca es texto fijo: lleva huecos que se rellenan con datos. Y
esos datos vienen de fuera —un correo de un cliente, un documento subido— así
que son **entrada no confiable**, exactamente igual que un payload de red.

Escribe `render_prompt`:

    render_prompt(
        "Clasifica esto:\\n<documento>\\n{texto}\\n</documento>",
        texto="PAGO NOMINA MARZO",
    )
    -> "Clasifica esto:\\n<documento>\\nPAGO NOMINA MARZO\\n</documento>"

Reglas:

- Los huecos son `{nombre}`. Se sustituyen por el valor correspondiente.
- Si la plantilla pide una variable que no se pasó, `ValueError` nombrándola.
  Un hueco sin rellenar que llega al modelo como `{texto}` literal es un prompt
  roto que nadie ve hasta que las respuestas salen raras.
- Si se pasa una variable que la plantilla no usa, también `ValueError`. Suele
  significar que alguien renombró un hueco y se olvidó de un sitio.
- **El valor no puede cerrar la etiqueta que lo envuelve.** Si el texto
  contiene `</documento>`, un atacante podría cerrar el bloque y escribir
  instrucciones fuera de él. Sustituye `<` por `&lt;` y `>` por `&gt;` en los
  **valores** (nunca en la plantilla), que es el escapado mínimo que impide
  cerrar una etiqueta.
- El orden del escapado importa: si sustituyes `&` después de `<`, acabas
  rompiendo las entidades que acabas de crear. Escapa `&` primero.

Este ejercicio no te protege de toda la inyección de prompt —eso no lo resuelve
ninguna función— pero cierra el agujero más burdo, y te deja con el modelo
mental correcto: **el contenido nunca es instrucción**.
"""


def render_prompt(template: str, **values: str) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
