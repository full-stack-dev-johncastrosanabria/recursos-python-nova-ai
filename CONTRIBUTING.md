# Cómo contribuir

Tres cosas se pueden aportar aquí: un enlace, un ejercicio o una guía. Cada una
tiene su receta. Sigue la que toque y no hace falta que preguntes nada.

Todo entra por pull request. No hay revisión obligatoria configurada, pero
espera a que el CI esté verde antes de mergear.

## Antes de empezar

```bash
git clone https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai.git
cd recursos-python-nova-ai
uv sync --group dev
git checkout -b mi-aportacion
```

## Receta 1 · Añadir un enlace

1. Abre el archivo de `recursos/enlaces/` del tema que corresponda. Si no
   existe, créalo con el nombre del módulo (`05-testing.md`) y añádelo al
   índice de `recursos/enlaces/README.md`.
2. Añade la entrada con este formato exacto:

```markdown
### [Título del recurso](https://ejemplo.com)
`artículo` · `en` · `intermedio` — Por qué vale la pena, en una línea.
```

3. La línea del final es obligatoria. Un enlace sin explicación no ayuda a
   nadie a decidir si abrirlo.
4. Commit y PR.

El CI comprueba que el enlace no esté roto.

## Receta 2 · Añadir un ejercicio

Un ejercicio son **tres archivos** con el mismo nombre en tres carpetas. Para
un ejercicio `cadenas` de nivel base en el módulo 02:

| Archivo | Qué lleva |
|---------|-----------|
| `ruta/02-estructuras-de-datos/ejercicios/base/cadenas.py` | El stub: docstring con el enunciado y la función lanzando `NotImplementedError` |
| `ruta/02-estructuras-de-datos/soluciones/base/cadenas.py` | La solución de referencia |
| `ruta/02-estructuras-de-datos/tests/base/test_cadenas.py` | Los tests |

Los nombres deben cuadrar: `test_cadenas.py` busca `cadenas.py`. La fixture lo
resuelve quitando el prefijo `test_`.

**El stub** lleva el enunciado en el docstring, con ejemplos:

```python
"""Ejercicio: contar palabras únicas.

    count_unique("hola hola mundo") -> 2
"""


def count_unique(text: str) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
```

**El test** pide la fixture `solution`, nunca importa el ejercicio:

```python
def test_count_unique_ignora_repetidas(solution):
    assert solution.count_unique("hola hola mundo") == 2
```

**Verifica las dos direcciones** antes de abrir el PR:

```bash
uv run pytest ruta/02-estructuras-de-datos                    # debe FALLAR
NOVA_SOLUCIONES=1 uv run pytest ruta/02-estructuras-de-datos  # debe PASAR
```

Si la segunda no pasa, tu solución no resuelve tu propio ejercicio. El CI corre
exactamente esa comprobación.

## Receta 3 · Escribir una guía

Los módulos 02 al 11 son esqueletos esperando contenido. Para escribir uno:

1. Abre su `GUIA.md`. Ya tiene la cabecera y los objetivos definidos.
2. **Respeta los objetivos.** Están pensados como una progresión; si crees que
   alguno sobra o falta, discútelo en un issue antes.
3. Copia la estructura del [módulo 01](ruta/01-fundamentos/GUIA.md): secciones
   numeradas, ejemplos ejecutables, y una sección final de ejercicios.
4. Cada concepto que expliques debería tener un archivo en `ejemplos/` que se
   pueda ejecutar:

```bash
uv run python ruta/NN-modulo/ejemplos/mi_ejemplo.py
```

5. Añade al menos dos ejercicios base y uno de reto (Receta 2).
6. Actualiza el enlace del módulo en `README.md` si hace falta.

### Crear un módulo nuevo

```bash
uv run python scripts/nuevo_modulo.py 12 despliegue "Despliegue" \
  --prerrequisitos "módulos 01-07" --minutos 120 \
  --salto "no hay siguiente" \
  --objetivo "Publicar un agente en producción"
```

Acuérdate de añadirlo a `nav:` en `mkdocs.yml` y a la tabla del `README.md`.

## Estilo

- **Prosa en español, identificadores en inglés.** `def count_unique(text)`,
  con el docstring en español. Es lo que el equipo verá en código real.
- **Términos técnicos sin traducir:** `list comprehension`, no "comprensión de
  listas".
- **Tutea al lector.** "Abre el archivo", no "el estudiante deberá abrir".
- **Carpetas en kebab-case**, módulos con prefijo de dos dígitos.

## Antes de abrir el PR

```bash
uv run ruff format .
uv run ruff check .
NOVA_SOLUCIONES=1 uv run pytest
```

## Nunca

- Subir una clave de API real. El repositorio es público. Usa `.env.example`.
- Subir material interno o confidencial de Nova AI.
