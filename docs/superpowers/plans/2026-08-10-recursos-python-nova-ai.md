# recursos-python-nova-ai — Plan de Implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar un repositorio público de capacitación en Python que lleve al equipo de Nova AI de nivel cero a construir agentes con LangGraph y CrewAI, con infraestructura que verifique que cada ejercicio publicado es resoluble.

**Architecture:** Monorepo con un único entorno gestionado por `uv` y grupos de dependencias opcionales (`ia`, `docs`, `dev`). La carpeta `ruta/` contiene 11 módulos numerados que se recorren en orden; `recursos/` contiene material de consulta. Un paquete `novatools/` implementa la infraestructura: una fixture de pytest que decide si un test carga el stub del aprendiz o la solución de referencia, y un generador de esqueletos de módulo.

**Tech Stack:** Python 3.12, uv, pytest, ruff, MkDocs Material, GitHub Actions, lychee.

**Spec:** `docs/superpowers/specs/2026-08-10-recursos-python-nova-ai-design.md`

## Global Constraints

Estas reglas aplican a **todas** las tareas:

- **Python 3.12** exacto. `.python-version` contiene `3.12`; `requires-python = ">=3.12"`.
- **`uv` es el único gestor.** Nunca `pip install`, `python -m venv` ni activación manual de entornos. Todo comando de Python se ejecuta con `uv run`.
- **Prosa en español, identificadores en inglés.** Guías, comentarios, docstrings y nombres de carpeta en español. Variables, funciones, clases y parámetros en inglés — incluida la infraestructura de `novatools/`.
- **Términos técnicos sin traducir:** `list comprehension`, `type hints`, `fixture`. No "comprensión de listas".
- **Carpetas en kebab-case.** Módulos con prefijo numérico de dos dígitos: `01-fundamentos`.
- **Nunca una clave de API real** en ningún archivo. Solo `.env.example` con valores vacíos.
- **`main` sin protección de rama.** No configurar reglas de protección.
- **Licencia dual:** MIT para código (`LICENSE`), CC BY 4.0 para contenido (`LICENSE-CONTENIDO`).
- **El repositorio ya existe localmente** en `~/Developer/recursos-python-nova-ai` con git inicializado, rama `main` y un commit con el spec. No hacer `git init`.

---

## File Structure

| Archivo | Responsabilidad |
|---------|-----------------|
| `pyproject.toml` | Metadatos, grupos de dependencias, configuración de pytest y ruff |
| `novatools/resolution.py` | Traducir ruta de test → ruta de ejercicio; cargar un `.py` suelto como módulo |
| `novatools/skeleton.py` | Generar la estructura de carpetas y `GUIA.md` de un módulo nuevo |
| `conftest.py` | Exponer la fixture `solution` a todos los tests de la ruta |
| `scripts/nuevo_modulo.py` | CLI sobre `novatools.skeleton` para contribuidores |
| `tests/` | Tests de `novatools` (infraestructura, no contenido didáctico) |
| `ruta/NN-*/` | Los 11 módulos de la capacitación |
| `recursos/` | Enlaces curados, cheatsheets, plantillas |
| `mkdocs.yml` | Configuración del sitio, leyendo el markdown donde ya vive |
| `.github/workflows/` | `ci.yml`, `enlaces.yml`, `docs.yml` |

`novatools/resolution.py` y `novatools/skeleton.py` se separan porque no comparten nada: uno se ejecuta en cada test, el otro solo cuando alguien crea un módulo.

---

### Task 1: Base del proyecto y entorno reproducible

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `.gitignore`

**Interfaces:**
- Consumes: nada.
- Produces: `uv run` funcionando; configuración de pytest con `pythonpath = ["."]` e `--import-mode=importlib` de la que dependen todas las tareas siguientes.

- [ ] **Step 1: Crear `.python-version`**

```
3.12
```

- [ ] **Step 2: Crear `pyproject.toml`**

Los grupos `ia` van sin límite inferior de versión a propósito: `uv.lock` fijará las versiones resueltas hoy, y poner floors inventados solo causaría conflictos de resolución.

```toml
[project]
name = "recursos-python-nova-ai"
version = "0.1.0"
description = "Ruta de capacitación en Python para el equipo de Nova AI"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8",
    "ruff>=0.6",
]
ia = [
    "anthropic",
    "langgraph",
    "crewai",
    "python-dotenv",
]
docs = [
    "mkdocs-material>=9.5",
    "mkdocs-same-dir>=0.1.3",
]

[tool.pytest.ini_options]
addopts = "--import-mode=importlib"
pythonpath = ["."]
testpaths = ["tests", "ruta"]

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

`--import-mode=importlib` no es opcional: sin él, dos archivos `test_saludo.py` en módulos distintos colisionan al importarse y pytest falla con "import file mismatch".

- [ ] **Step 3: Crear `.gitignore`**

```
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.env
site/
.DS_Store
```

- [ ] **Step 4: Sincronizar el entorno y verificar**

Run: `uv sync --group dev`
Expected: crea `.venv/` y `uv.lock` sin errores.

Run: `uv run python --version`
Expected: `Python 3.12.x`

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml uv.lock .python-version .gitignore
git commit -m "chore: base del proyecto con uv y Python 3.12"
```

---

### Task 2: Resolución ejercicios/soluciones

Esta es la única pieza del repositorio con lógica real. Se construye con TDD.

**Files:**
- Create: `novatools/__init__.py`
- Create: `novatools/resolution.py`
- Create: `tests/test_resolution.py`
- Create: `conftest.py`

**Interfaces:**
- Consumes: configuración de pytest de la Task 1.
- Produces:
  - `novatools.resolution.solutions_enabled(env: Mapping[str, str] | None = None) -> bool`
  - `novatools.resolution.target_path(test_path: Path, use_solutions: bool) -> Path`
  - `novatools.resolution.load_module(path: Path) -> ModuleType`
  - `novatools.resolution.SOLUTIONS_ENV_VAR: str` (valor `"NOVA_SOLUCIONES"`)
  - Fixture de pytest `solution`, que todos los tests de `ruta/` consumen.

- [ ] **Step 1: Escribir los tests que fallan**

Crear `novatools/__init__.py` vacío y `tests/test_resolution.py`:

```python
"""Tests de la infraestructura que resuelve qué archivo prueba cada test."""

from pathlib import Path

import pytest

from novatools.resolution import load_module, solutions_enabled, target_path


def test_target_path_apunta_a_ejercicios_por_defecto():
    test_path = Path("ruta/01-fundamentos/tests/base/test_saludo.py")
    assert target_path(test_path, use_solutions=False) == Path(
        "ruta/01-fundamentos/ejercicios/base/saludo.py"
    )


def test_target_path_apunta_a_soluciones_cuando_se_pide():
    test_path = Path("ruta/01-fundamentos/tests/reto/test_estadisticas.py")
    assert target_path(test_path, use_solutions=True) == Path(
        "ruta/01-fundamentos/soluciones/reto/estadisticas.py"
    )


def test_target_path_rechaza_test_fuera_de_carpeta_tests():
    with pytest.raises(ValueError, match="tests/"):
        target_path(
            Path("ruta/01-fundamentos/base/test_saludo.py"), use_solutions=False
        )


def test_target_path_rechaza_archivo_sin_prefijo_test():
    with pytest.raises(ValueError, match="test_"):
        target_path(
            Path("ruta/01-fundamentos/tests/base/saludo.py"), use_solutions=False
        )


def test_solutions_enabled_lee_la_variable():
    assert solutions_enabled({"NOVA_SOLUCIONES": "1"}) is True
    assert solutions_enabled({"NOVA_SOLUCIONES": "0"}) is False
    assert solutions_enabled({}) is False


def test_load_module_carga_un_archivo_suelto(tmp_path):
    archivo = tmp_path / "saludo.py"
    archivo.write_text(
        'def greet(name):\n    return f"Hola, {name}"\n', encoding="utf-8"
    )

    modulo = load_module(archivo)

    assert modulo.greet("Ana") == "Hola, Ana"


def test_load_module_no_colisiona_entre_modulos(tmp_path):
    uno = tmp_path / "01-fundamentos" / "ejercicios" / "base"
    dos = tmp_path / "02-estructuras-de-datos" / "ejercicios" / "base"
    uno.mkdir(parents=True)
    dos.mkdir(parents=True)
    (uno / "saludo.py").write_text("VALUE = 1\n", encoding="utf-8")
    (dos / "saludo.py").write_text("VALUE = 2\n", encoding="utf-8")

    assert load_module(uno / "saludo.py").VALUE == 1
    assert load_module(dos / "saludo.py").VALUE == 2
```

El último test es el que justifica la estrategia de nombres en `load_module`: dos ejercicios con el mismo nombre de archivo en módulos distintos son inevitables, y no pueden pisarse en `sys.modules`.

- [ ] **Step 2: Ejecutar los tests para verificar que fallan**

Run: `uv run pytest tests/test_resolution.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'novatools.resolution'`

- [ ] **Step 3: Implementar `novatools/resolution.py`**

```python
"""Decide qué archivo carga el test de un ejercicio.

Los tests de la ruta nunca importan el ejercicio directamente: piden la fixture
`solution`, que usa estas funciones para cargar el stub del aprendiz o la
solución de referencia, según la variable de entorno NOVA_SOLUCIONES.
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from types import ModuleType

SOLUTIONS_ENV_VAR = "NOVA_SOLUCIONES"


def solutions_enabled(env: Mapping[str, str] | None = None) -> bool:
    """True si los tests deben correr contra soluciones/ en vez de ejercicios/."""
    source = os.environ if env is None else env
    return source.get(SOLUTIONS_ENV_VAR, "") == "1"


def target_path(test_path: Path, use_solutions: bool) -> Path:
    """Traduce la ruta de un test a la del archivo que pone a prueba.

    ruta/01-fundamentos/tests/base/test_saludo.py
        -> ruta/01-fundamentos/ejercicios/base/saludo.py
    """
    parts = list(test_path.parts)
    if "tests" not in parts:
        raise ValueError(f"El test debe vivir bajo una carpeta 'tests/': {test_path}")

    index = len(parts) - 1 - parts[::-1].index("tests")
    parts[index] = "soluciones" if use_solutions else "ejercicios"

    filename = test_path.name
    if not filename.startswith("test_"):
        raise ValueError(f"El archivo de test debe empezar por 'test_': {filename}")
    parts[-1] = filename.removeprefix("test_")

    return Path(*parts)


def load_module(path: Path) -> ModuleType:
    """Carga un archivo .py suelto como módulo, sin que su carpeta sea paquete."""
    resolved = path.resolve()
    tail = "_".join(resolved.with_suffix("").parts[-4:])
    module_name = "nova_" + re.sub(r"\W+", "_", tail)

    spec = importlib.util.spec_from_file_location(module_name, resolved)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar {resolved}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
```

- [ ] **Step 4: Ejecutar los tests para verificar que pasan**

Run: `uv run pytest tests/test_resolution.py -v`
Expected: PASS, 7 tests.

- [ ] **Step 5: Crear `conftest.py` en la raíz**

```python
"""Configuración global de pytest para la ruta de aprendizaje."""

from pathlib import Path

import pytest

from novatools.resolution import load_module, solutions_enabled, target_path


@pytest.fixture
def solution(request):
    """Carga el ejercicio bajo prueba.

    Por defecto carga tu archivo de `ejercicios/`, así que los tests estarán en
    rojo hasta que lo resuelvas. Con NOVA_SOLUCIONES=1 carga la solución de
    referencia: así verifica el CI que cada ejercicio publicado es resoluble.
    """
    test_path = Path(request.path)
    use_solutions = solutions_enabled()
    path = target_path(test_path, use_solutions)

    if not path.exists():
        carpeta = "soluciones" if use_solutions else "ejercicios"
        pytest.fail(
            f"Falta el archivo en {carpeta}/: {path}\n"
            f"Cada test necesita su pareja: {test_path.name} -> {path.name}"
        )

    return load_module(path)
```

- [ ] **Step 6: Verificar que la suite completa sigue verde**

Run: `uv run pytest -v`
Expected: PASS, 7 tests (aún no hay módulos en `ruta/`).

- [ ] **Step 7: Commit**

```bash
git add novatools/ tests/ conftest.py
git commit -m "feat: fixture solution que resuelve ejercicios o soluciones"
```

---

### Task 3: Generador de esqueletos de módulo

**Files:**
- Create: `novatools/skeleton.py`
- Create: `tests/test_skeleton.py`
- Create: `scripts/nuevo_modulo.py`

**Interfaces:**
- Consumes: nada de tareas anteriores.
- Produces:
  - `novatools.skeleton.ModuleSpec` — dataclass congelada con campos `number: int`, `slug: str`, `title: str`, `prerequisites: str`, `minutes: int`, `skip_to: str`, `objectives: tuple[str, ...]`
  - `novatools.skeleton.folder_name(spec: ModuleSpec) -> str`
  - `novatools.skeleton.render_guide(spec: ModuleSpec) -> str`
  - `novatools.skeleton.create_module(root: Path, spec: ModuleSpec) -> Path`
  - `novatools.skeleton.SUBFOLDERS: tuple[str, ...]`

- [ ] **Step 1: Escribir los tests que fallan**

Crear `tests/test_skeleton.py`:

```python
"""Tests del generador de esqueletos de módulo."""

from novatools.skeleton import (
    SUBFOLDERS,
    ModuleSpec,
    create_module,
    folder_name,
    render_guide,
)

EJEMPLO = ModuleSpec(
    number=5,
    slug="testing",
    title="Testing",
    prerequisites="módulos 01–04",
    minutes=90,
    skip_to="salta al módulo 06",
    objectives=("Escribir un test con pytest", "Usar fixtures"),
)


def test_folder_name_rellena_con_cero():
    assert folder_name(EJEMPLO) == "05-testing"


def test_render_guide_incluye_la_cabecera_fija():
    guia = render_guide(EJEMPLO)
    assert "# Módulo 05 · Testing" in guia
    assert "**Prerrequisitos:** módulos 01–04" in guia
    assert "**Tiempo estimado:** 90 min" in guia
    assert "**Si ya dominas esto:** salta al módulo 06" in guia


def test_render_guide_lista_los_objetivos():
    guia = render_guide(EJEMPLO)
    assert "- Escribir un test con pytest" in guia
    assert "- Usar fixtures" in guia


def test_create_module_crea_todas_las_subcarpetas(tmp_path):
    module_dir = create_module(tmp_path, EJEMPLO)

    assert module_dir == tmp_path / "ruta" / "05-testing"
    for sub in SUBFOLDERS:
        assert (module_dir / sub).is_dir(), f"falta {sub}"


def test_create_module_escribe_la_guia(tmp_path):
    module_dir = create_module(tmp_path, EJEMPLO)

    guia = (module_dir / "GUIA.md").read_text(encoding="utf-8")
    assert "# Módulo 05 · Testing" in guia


def test_create_module_es_idempotente(tmp_path):
    create_module(tmp_path, EJEMPLO)
    module_dir = create_module(tmp_path, EJEMPLO)

    assert (module_dir / "GUIA.md").exists()
```

- [ ] **Step 2: Ejecutar los tests para verificar que fallan**

Run: `uv run pytest tests/test_skeleton.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'novatools.skeleton'`

- [ ] **Step 3: Implementar `novatools/skeleton.py`**

````python
"""Genera la estructura de un módulo de la ruta.

Un módulo siempre tiene la misma anatomía. Generarla evita que cada
contribución invente su propia variante.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUBFOLDERS = (
    "ejemplos",
    "ejercicios/base",
    "ejercicios/reto",
    "soluciones/base",
    "soluciones/reto",
    "tests/base",
    "tests/reto",
)


@dataclass(frozen=True)
class ModuleSpec:
    """Los datos que definen un módulo antes de tener contenido."""

    number: int
    slug: str
    title: str
    prerequisites: str
    minutes: int
    skip_to: str
    objectives: tuple[str, ...]


def folder_name(spec: ModuleSpec) -> str:
    return f"{spec.number:02d}-{spec.slug}"


def render_guide(spec: ModuleSpec) -> str:
    objectives = "\n".join(f"- {item}" for item in spec.objectives)
    return f"""# Módulo {spec.number:02d} · {spec.title}

> **Prerrequisitos:** {spec.prerequisites}
> **Tiempo estimado:** {spec.minutes} min
> **Si ya dominas esto:** {spec.skip_to}

## Qué vas a poder hacer al terminar

{objectives}

## Contenido

Este módulo todavía no está escrito. El módulo 01 es la plantilla viva: copia
su estructura. Si quieres escribir este, lee `CONTRIBUTING.md`.

## Ejercicios

- `ejercicios/base/` — para consolidar lo del módulo.
- `ejercicios/reto/` — si ya llegabas sabiendo el tema.

Para ver tu progreso:

```bash
uv run pytest ruta/{folder_name(spec)}
```
"""


def create_module(root: Path, spec: ModuleSpec) -> Path:
    """Crea las carpetas y la GUIA.md del módulo. Idempotente."""
    module_dir = root / "ruta" / folder_name(spec)

    for sub in SUBFOLDERS:
        target = module_dir / sub
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitkeep").touch()

    (module_dir / "GUIA.md").write_text(render_guide(spec), encoding="utf-8")
    return module_dir
````

- [ ] **Step 4: Ejecutar los tests para verificar que pasan**

Run: `uv run pytest tests/test_skeleton.py -v`
Expected: PASS, 6 tests.

- [ ] **Step 5: Crear el CLI `scripts/nuevo_modulo.py`**

```python
"""Crea el esqueleto de un módulo nuevo.

Uso:
    uv run python scripts/nuevo_modulo.py 12 despliegue "Despliegue" \\
        --prerrequisitos "módulos 01-07" --minutos 120 \\
        --salto "salta al módulo 13" \\
        --objetivo "Publicar un agente en producción"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from novatools.skeleton import ModuleSpec, create_module

RAIZ = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea el esqueleto de un módulo")
    parser.add_argument("numero", type=int, help="número del módulo, p. ej. 12")
    parser.add_argument("slug", help="nombre de carpeta en kebab-case")
    parser.add_argument("titulo", help="título legible del módulo")
    parser.add_argument("--prerrequisitos", default="ninguno")
    parser.add_argument("--minutos", type=int, default=90)
    parser.add_argument("--salto", default="no hay módulo siguiente todavía")
    parser.add_argument(
        "--objetivo",
        action="append",
        default=[],
        help="repetible: un objetivo de aprendizaje por bandera",
    )
    args = parser.parse_args()

    spec = ModuleSpec(
        number=args.numero,
        slug=args.slug,
        title=args.titulo,
        prerequisites=args.prerrequisitos,
        minutes=args.minutos,
        skip_to=args.salto,
        objectives=tuple(args.objetivo),
    )

    destino = create_module(RAIZ, spec)
    print(f"Módulo creado en {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Verificar el CLI a mano y limpiar**

Run: `uv run python scripts/nuevo_modulo.py 99 prueba "Prueba" --objetivo "Comprobar el generador"`
Expected: imprime `Módulo creado en ruta/99-prueba`

Run: `ls ruta/99-prueba && rm -rf ruta/99-prueba`
Expected: lista `GUIA.md`, `ejemplos`, `ejercicios`, `soluciones`, `tests`; luego se borra.

- [ ] **Step 7: Commit**

```bash
git add novatools/skeleton.py tests/test_skeleton.py scripts/nuevo_modulo.py
git commit -m "feat: generador de esqueletos de módulo"
```

---

### Task 4: Módulo 01 completo (la plantilla viva)

Este es el único módulo con contenido real en el arranque. Todo lo demás se copia de aquí, así que la calidad importa más que la velocidad.

**Files:**
- Create: `ruta/01-fundamentos/GUIA.md`
- Create: `ruta/01-fundamentos/ejemplos/variables_y_tipos.py`
- Create: `ruta/01-fundamentos/ejemplos/control_de_flujo.py`
- Create: `ruta/01-fundamentos/ejercicios/base/saludo.py`
- Create: `ruta/01-fundamentos/ejercicios/base/temperatura.py`
- Create: `ruta/01-fundamentos/ejercicios/reto/estadisticas.py`
- Create: `ruta/01-fundamentos/soluciones/base/saludo.py`
- Create: `ruta/01-fundamentos/soluciones/base/temperatura.py`
- Create: `ruta/01-fundamentos/soluciones/reto/estadisticas.py`
- Test: `ruta/01-fundamentos/tests/base/test_saludo.py`
- Test: `ruta/01-fundamentos/tests/base/test_temperatura.py`
- Test: `ruta/01-fundamentos/tests/reto/test_estadisticas.py`

**Interfaces:**
- Consumes: fixture `solution` de la Task 2.
- Produces: las funciones que los tests esperan —`greet(name: str) -> str`, `celsius_to_fahrenheit(celsius: float) -> float`, `summarize(numbers: list[float]) -> dict[str, float]`— y el patrón de módulo que copian las Tasks 5 y siguientes.

- [ ] **Step 1: Crear el esqueleto del módulo con el generador**

Run:
```bash
uv run python scripts/nuevo_modulo.py 1 fundamentos "Fundamentos" \
  --prerrequisitos "ninguno" --minutos 120 \
  --salto "salta al módulo 02" \
  --objetivo "Declarar variables y reconocer los tipos básicos de Python" \
  --objetivo "Escribir condicionales y bucles" \
  --objetivo "Definir funciones con parámetros y valor de retorno" \
  --objetivo "Ejecutar tests y leer por qué fallan"
```
Expected: `Módulo creado en ruta/01-fundamentos`

- [ ] **Step 2: Escribir los tests de los tres ejercicios**

`ruta/01-fundamentos/tests/base/test_saludo.py`:

```python
def test_greet_saluda_por_nombre(solution):
    assert solution.greet("Ana") == "Hola, Ana"


def test_greet_funciona_con_cualquier_nombre(solution):
    assert solution.greet("Beto") == "Hola, Beto"


def test_greet_recorta_espacios_sobrantes(solution):
    assert solution.greet("  Ana  ") == "Hola, Ana"
```

`ruta/01-fundamentos/tests/base/test_temperatura.py`:

```python
import pytest


def test_celsius_to_fahrenheit_en_el_punto_de_congelacion(solution):
    assert solution.celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_en_el_punto_de_ebullicion(solution):
    assert solution.celsius_to_fahrenheit(100) == 212


def test_celsius_to_fahrenheit_admite_negativos(solution):
    assert solution.celsius_to_fahrenheit(-40) == -40


def test_celsius_to_fahrenheit_admite_decimales(solution):
    assert solution.celsius_to_fahrenheit(36.6) == pytest.approx(97.88)
```

`ruta/01-fundamentos/tests/reto/test_estadisticas.py`:

```python
import pytest


def test_summarize_devuelve_minimo_maximo_y_media(solution):
    assert solution.summarize([1, 2, 3, 4]) == {
        "min": 1,
        "max": 4,
        "mean": 2.5,
    }


def test_summarize_con_un_solo_numero(solution):
    assert solution.summarize([7]) == {"min": 7, "max": 7, "mean": 7}


def test_summarize_rechaza_una_lista_vacia(solution):
    with pytest.raises(ValueError):
        solution.summarize([])
```

- [ ] **Step 3: Escribir los stubs de los ejercicios**

`ruta/01-fundamentos/ejercicios/base/saludo.py`:

```python
"""Ejercicio: saludar por nombre.

Completa `greet` para que devuelva un saludo. Los espacios sobrantes alrededor
del nombre no deben aparecer en el resultado.

    greet("Ana")     -> "Hola, Ana"
    greet("  Ana  ") -> "Hola, Ana"
"""


def greet(name: str) -> str:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
```

`ruta/01-fundamentos/ejercicios/base/temperatura.py`:

```python
"""Ejercicio: convertir grados Celsius a Fahrenheit.

La fórmula es: F = C * 9/5 + 32

    celsius_to_fahrenheit(0)   -> 32
    celsius_to_fahrenheit(100) -> 212
"""


def celsius_to_fahrenheit(celsius: float) -> float:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
```

`ruta/01-fundamentos/ejercicios/reto/estadisticas.py`:

```python
"""Reto: resumir una lista de números.

Devuelve un dict con el mínimo, el máximo y la media:

    summarize([1, 2, 3, 4]) -> {"min": 1, "max": 4, "mean": 2.5}

Una lista vacía no tiene mínimo ni media, así que debe lanzar ValueError.
"""


def summarize(numbers: list[float]) -> dict[str, float]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
```

- [ ] **Step 4: Ejecutar los tests sin la variable — deben fallar**

Run: `uv run pytest ruta/01-fundamentos -v`
Expected: FAIL, 10 tests, todos con `NotImplementedError`. Es el estado correcto: así lo ve el aprendiz.

- [ ] **Step 5: Escribir las soluciones de referencia**

`ruta/01-fundamentos/soluciones/base/saludo.py`:

```python
"""Solución de referencia del ejercicio `saludo`."""


def greet(name: str) -> str:
    return f"Hola, {name.strip()}"
```

`ruta/01-fundamentos/soluciones/base/temperatura.py`:

```python
"""Solución de referencia del ejercicio `temperatura`."""


def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32
```

`ruta/01-fundamentos/soluciones/reto/estadisticas.py`:

```python
"""Solución de referencia del reto `estadisticas`."""


def summarize(numbers: list[float]) -> dict[str, float]:
    if not numbers:
        raise ValueError("summarize necesita al menos un número")

    return {
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }
```

- [ ] **Step 6: Ejecutar los tests con la variable — deben pasar**

Run: `NOVA_SOLUCIONES=1 uv run pytest ruta/01-fundamentos -v`
Expected: PASS, 10 tests. Esto demuestra que los tres ejercicios son resolubles.

- [ ] **Step 7: Escribir los ejemplos**

`ruta/01-fundamentos/ejemplos/variables_y_tipos.py`:

```python
"""Los tipos básicos de Python, en un archivo que puedes ejecutar.

Córrelo con:
    uv run python ruta/01-fundamentos/ejemplos/variables_y_tipos.py
"""

# Python deduce el tipo, pero anotarlo hace el código más claro.
name: str = "Ana"
age: int = 30
height: float = 1.62
is_active: bool = True

# f-strings: la forma normal de construir texto con valores dentro.
print(f"{name} tiene {age} años y mide {height} m")

# type() te dice el tipo de cualquier valor. Útil cuando algo no cuadra.
for value in (name, age, height, is_active):
    print(f"{value!r:>10} -> {type(value).__name__}")

# Las listas guardan varios valores en orden.
languages: list[str] = ["Python", "SQL", "Bash"]
print(f"Primero: {languages[0]} · Último: {languages[-1]}")

# Los dicts asocian claves con valores.
person: dict[str, str] = {"nombre": "Ana", "rol": "backend"}
print(f"{person['nombre']} trabaja en {person['rol']}")
```

`ruta/01-fundamentos/ejemplos/control_de_flujo.py`:

```python
"""Condicionales, bucles y funciones.

Córrelo con:
    uv run python ruta/01-fundamentos/ejemplos/control_de_flujo.py
"""


def classify(temperature: float) -> str:
    """Clasifica una temperatura en Celsius."""
    if temperature < 0:
        return "helada"
    if temperature < 15:
        return "fría"
    if temperature < 28:
        return "templada"
    return "calurosa"


def average(numbers: list[float]) -> float:
    """Calcula la media. Lanza ValueError si la lista está vacía."""
    if not numbers:
        raise ValueError("no se puede promediar una lista vacía")
    return sum(numbers) / len(numbers)


readings = [-5.0, 12.0, 22.5, 31.0]

for reading in readings:
    print(f"{reading:>6.1f} °C -> {classify(reading)}")

print(f"Media: {average(readings):.2f} °C")

# Un bucle con índice, cuando de verdad necesitas el número de posición.
for position, reading in enumerate(readings, start=1):
    print(f"Lectura {position}: {reading} °C")
```

- [ ] **Step 8: Verificar que los ejemplos se ejecutan**

Run: `uv run python ruta/01-fundamentos/ejemplos/variables_y_tipos.py`
Expected: imprime las líneas sin error.

Run: `uv run python ruta/01-fundamentos/ejemplos/control_de_flujo.py`
Expected: imprime las clasificaciones y la media, sin error.

- [ ] **Step 9: Escribir la `GUIA.md` completa**

Sustituir el contenido generado por:

````markdown
# Módulo 01 · Fundamentos

> **Prerrequisitos:** ninguno
> **Tiempo estimado:** 120 min
> **Si ya dominas esto:** salta al módulo 02

## Qué vas a poder hacer al terminar

- Declarar variables y reconocer los tipos básicos de Python
- Escribir condicionales y bucles
- Definir funciones con parámetros y valor de retorno
- Ejecutar tests y leer por qué fallan

## 1. Variables y tipos

Python no necesita que declares el tipo de una variable, pero puedes anotarlo.
Hazlo: dentro de seis meses, el que lea el código serás tú.

```python
name: str = "Ana"
age: int = 30
```

Los cuatro tipos básicos son `str` (texto), `int` (entero), `float` (decimal) y
`bool` (verdadero o falso). Para agrupar valores tienes `list` (en orden) y
`dict` (por clave).

Abre y ejecuta `ejemplos/variables_y_tipos.py`:

```bash
uv run python ruta/01-fundamentos/ejemplos/variables_y_tipos.py
```

## 2. Condicionales y bucles

Python usa la indentación para marcar bloques: no hay llaves. Cuatro espacios,
siempre.

```python
if temperature < 0:
    print("helada")
elif temperature < 15:
    print("fría")
else:
    print("templada")
```

Para recorrer una colección, `for`:

```python
for reading in readings:
    print(reading)
```

Si necesitas la posición además del valor, `enumerate` — no un contador manual.

## 3. Funciones

Una función agrupa código que hace una cosa y le pone nombre:

```python
def average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("no se puede promediar una lista vacía")
    return sum(numbers) / len(numbers)
```

Las anotaciones (`list[float]`, `-> float`) no las verifica Python al ejecutar,
pero documentan la intención y tu editor las usa para avisarte de errores.

Cuando una función recibe algo con lo que no puede trabajar, lanza una
excepción en vez de devolver un valor raro como `None` o `0`. Quien la llame
se enterará del problema en el momento, no tres funciones más abajo.

Ejecuta `ejemplos/control_de_flujo.py` y léelo entero.

## 4. Ejercicios

Los ejercicios están en `ejercicios/`. Cada archivo tiene una función sin
terminar. Tu trabajo es completarla.

Corre los tests:

```bash
uv run pytest ruta/01-fundamentos
```

Los verás en rojo: es lo esperado. Los stubs lanzan `NotImplementedError` a
propósito. Ve resolviendo y vuelve a correrlos hasta que estén verdes.

- **`ejercicios/base/saludo.py`** — devolver un saludo, sin espacios sobrantes.
- **`ejercicios/base/temperatura.py`** — convertir Celsius a Fahrenheit.
- **`ejercicios/reto/estadisticas.py`** — resumir una lista de números. Este
  requiere manejar el caso de la lista vacía.

Para correr un solo ejercicio:

```bash
uv run pytest ruta/01-fundamentos/tests/base/test_saludo.py -v
```

Si te atascas, en `soluciones/` está la versión de referencia. Míralas después
de intentarlo, no antes: leer una solución da la sensación de haber aprendido
sin haber aprendido.

## Siguiente

Módulo 02 · Estructuras de datos.
````

- [ ] **Step 10: Verificar lint y la suite completa**

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: sin errores. Si `ruff format` se queja, ejecuta `uv run ruff format .` y repite.

Run: `NOVA_SOLUCIONES=1 uv run pytest -v`
Expected: PASS, 23 tests (13 de infraestructura + 10 del módulo 01).

- [ ] **Step 11: Commit**

```bash
git add ruta/01-fundamentos
git commit -m "feat: módulo 01 completo como plantilla viva"
```

---

### Task 5: Esqueletos de los módulos 02–11

**Files:**
- Create: `ruta/02-estructuras-de-datos/` … `ruta/11-proyecto-final/` (10 módulos)

**Interfaces:**
- Consumes: `scripts/nuevo_modulo.py` de la Task 3.
- Produces: las carpetas que la Task 8 referencia en la navegación de MkDocs.

- [ ] **Step 1: Generar los diez módulos**

Ejecutar cada comando. Los objetivos vienen del spec; no inventar otros.

```bash
uv run python scripts/nuevo_modulo.py 2 estructuras-de-datos "Estructuras de datos" \
  --prerrequisitos "módulo 01" --minutos 120 --salto "salta al módulo 03" \
  --objetivo "Elegir entre list, dict, set y tuple según el caso" \
  --objetivo "Escribir list comprehensions legibles" \
  --objetivo "Usar generadores para no cargar todo en memoria"

uv run python scripts/nuevo_modulo.py 3 poo-y-modulos "POO y módulos" \
  --prerrequisitos "módulos 01-02" --minutos 120 --salto "salta al módulo 04" \
  --objetivo "Definir clases con estado y comportamiento" \
  --objetivo "Usar dataclasses para estructuras de datos" \
  --objetivo "Organizar código en módulos y paquetes"

uv run python scripts/nuevo_modulo.py 4 entorno-y-herramientas "Entorno y herramientas" \
  --prerrequisitos "módulos 01-03" --minutos 90 --salto "salta al módulo 05" \
  --objetivo "Crear y gestionar un proyecto con uv" \
  --objetivo "Configurar ruff para lint y formato" \
  --objetivo "Anotar tipos y entender qué verifican" \
  --objetivo "Reconocer la anatomía de un proyecto Python"

uv run python scripts/nuevo_modulo.py 5 testing "Testing" \
  --prerrequisitos "módulos 01-04" --minutos 120 --salto "salta al módulo 06" \
  --objetivo "Escribir tests con pytest" \
  --objetivo "Usar fixtures y parametrize" \
  --objetivo "Escribir el test antes que el código"

uv run python scripts/nuevo_modulo.py 6 async-y-concurrencia "Async y concurrencia" \
  --prerrequisitos "módulos 01-05" --minutos 120 --salto "salta al módulo 07" \
  --objetivo "Escribir funciones async y esperarlas con await" \
  --objetivo "Lanzar tareas concurrentes con asyncio" \
  --objetivo "Distinguir cuándo async ayuda y cuándo estorba"

uv run python scripts/nuevo_modulo.py 7 datos-y-apis "Datos y APIs" \
  --prerrequisitos "módulos 01-06" --minutos 150 --salto "salta al módulo 08" \
  --objetivo "Validar datos con pydantic" \
  --objetivo "Consumir APIs con httpx" \
  --objetivo "Exponer un endpoint con FastAPI" \
  --objetivo "Explorar datos tabulares con pandas"

uv run python scripts/nuevo_modulo.py 8 llms-fundamentos "Fundamentos de LLMs" \
  --prerrequisitos "módulos 01-07" --minutos 150 --salto "salta al módulo 09" \
  --objetivo "Llamar a un modelo con el SDK de Claude" \
  --objetivo "Escribir prompts que den resultados repetibles" \
  --objetivo "Definir herramientas y manejar tool use" \
  --objetivo "Obtener salida estructurada y validarla" \
  --objetivo "Montar un RAG básico"

uv run python scripts/nuevo_modulo.py 9 agentes-langgraph "Agentes con LangGraph" \
  --prerrequisitos "módulos 01-08" --minutos 180 --salto "salta al módulo 10" \
  --objetivo "Modelar un flujo como grafo de estado" \
  --objetivo "Definir nodos y transiciones condicionales" \
  --objetivo "Persistir estado con checkpoints" \
  --objetivo "Insertar un paso de human-in-the-loop"

uv run python scripts/nuevo_modulo.py 10 agentes-crewai "Agentes con CrewAI" \
  --prerrequisitos "módulos 01-08" --minutos 180 --salto "salta al módulo 11" \
  --objetivo "Definir agentes con rol, objetivo y contexto" \
  --objetivo "Componer tareas y encadenarlas" \
  --objetivo "Delegar trabajo entre agentes" \
  --objetivo "Contrastar el modelo de CrewAI con el de LangGraph"

uv run python scripts/nuevo_modulo.py 11 proyecto-final "Proyecto final" \
  --prerrequisitos "toda la ruta" --minutos 300 --salto "no hay siguiente: este es el final" \
  --objetivo "Construir un agente que resuelva un problema real de Nova AI" \
  --objetivo "Cubrirlo con tests" \
  --objetivo "Documentar cómo se ejecuta y se despliega"
```

- [ ] **Step 2: Verificar que están los once módulos**

Run: `ls ruta/`
Expected: `01-fundamentos` … `11-proyecto-final`, once carpetas.

Run: `NOVA_SOLUCIONES=1 uv run pytest -v`
Expected: PASS, 23 tests. Los módulos vacíos no aportan tests ni rompen nada.

- [ ] **Step 3: Commit**

```bash
git add ruta/
git commit -m "feat: esqueleto de los módulos 02-11"
```

---

### Task 6: Portada y autodiagnóstico de nivel

**Files:**
- Create: `README.md`
- Create: `EMPIEZA-AQUI.md`

**Interfaces:**
- Consumes: los once módulos de las Tasks 4 y 5.
- Produces: `README.md`, que MkDocs usa como página de inicio en la Task 8.

- [ ] **Step 1: Escribir `README.md`**

````markdown
# Recursos Python · Nova AI

Ruta de capacitación en Python para el equipo, de nivel cero a construir
agentes con LangGraph y CrewAI. Incluye guías, código ejecutable, ejercicios
con tests y una biblioteca de enlaces curados.

**¿No sabes por dónde empezar?** Lee [EMPIEZA-AQUI.md](EMPIEZA-AQUI.md): son
diez preguntas y te dice tu módulo de entrada.

## Arranque rápido

### Sin instalar nada

Abre el repositorio en GitHub Codespaces (botón **Code › Codespaces**). Tienes
Python y las dependencias listas en un par de minutos.

### En tu máquina

Necesitas [uv](https://docs.astral.sh/uv/). Instala el resto —incluido el
propio Python— por ti:

```bash
git clone https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai.git
cd recursos-python-nova-ai
uv sync
uv run pytest ruta/01-fundamentos
```

Los tests te saldrán en rojo. Es correcto: son los ejercicios sin resolver.

Cuando llegues al módulo 08 necesitarás las dependencias de IA:

```bash
uv sync --group ia
```

## La ruta

| # | Módulo | Qué cubre |
|---|--------|-----------|
| [01](ruta/01-fundamentos/GUIA.md) | Fundamentos | sintaxis, tipos, control de flujo, funciones |
| [02](ruta/02-estructuras-de-datos/GUIA.md) | Estructuras de datos | listas, dicts, sets, comprehensions, generadores |
| [03](ruta/03-poo-y-modulos/GUIA.md) | POO y módulos | clases, dataclasses, paquetes e imports |
| [04](ruta/04-entorno-y-herramientas/GUIA.md) | Entorno y herramientas | uv, ruff, type hints, anatomía de un proyecto |
| [05](ruta/05-testing/GUIA.md) | Testing | pytest, fixtures, parametrize, TDD básico |
| [06](ruta/06-async-y-concurrencia/GUIA.md) | Async y concurrencia | async/await, asyncio, cuándo no usarlo |
| [07](ruta/07-datos-y-apis/GUIA.md) | Datos y APIs | pydantic, httpx, FastAPI, pandas |
| [08](ruta/08-llms-fundamentos/GUIA.md) | Fundamentos de LLMs | SDK de Claude, prompts, tool use, RAG |
| [09](ruta/09-agentes-langgraph/GUIA.md) | Agentes con LangGraph | grafos de estado, checkpoints, human-in-the-loop |
| [10](ruta/10-agentes-crewai/GUIA.md) | Agentes con CrewAI | agentes por roles, tareas, delegación |
| [11](ruta/11-proyecto-final/GUIA.md) | Proyecto final | un agente completo, de punta a punta |

Ahora mismo **solo el módulo 01 tiene contenido**. El resto son esqueletos con
sus objetivos definidos, a la espera de que alguien los escriba. Empieza por
[CONTRIBUTING.md](CONTRIBUTING.md) si quieres ser esa persona.

## Recursos de consulta

- [Enlaces curados](recursos/enlaces/) — artículos, vídeos y cursos por tema
- [Cheatsheets](recursos/cheatsheets/) — referencias rápidas
- [Plantillas](recursos/plantillas/) — scaffolds de proyecto reutilizables

## Claves de API

Los módulos 08 al 11 llaman a modelos de pago. Copia `.env.example` a `.env` y
pon tus propias claves; `.env` está en `.gitignore` y nunca debe subirse.

Si no quieres gastar, el módulo 08 documenta cómo usar modelos locales con
Ollama.

## Licencia

Doble licencia: el **código** bajo [MIT](LICENSE), el **contenido** (guías,
cheatsheets, listas de enlaces) bajo
[CC BY 4.0](LICENSE-CONTENIDO).
````

- [ ] **Step 2: Escribir `EMPIEZA-AQUI.md`**

```markdown
# Empieza aquí

Este repositorio sirve a gente con niveles muy distintos. En vez de hacerte
recorrer módulos que ya dominas, respóndete estas preguntas con honestidad.

No hay nota ni te evalúa nadie. Mentirte aquí solo te hace perder tiempo
después.

## Cómo funciona

Ve bajando. En cuanto respondas **"no"** a una pregunta, ese es tu módulo de
entrada. Empieza ahí.

## Las preguntas

**1. ¿Has escrito alguna vez código en cualquier lenguaje?**
Si no → empieza en el [módulo 01](ruta/01-fundamentos/GUIA.md). Está escrito
para alguien que nunca ha programado.

**2. ¿Puedes escribir de memoria una función en Python que reciba una lista y
devuelva su media, lanzando un error si está vacía?**
Si no → [módulo 01 · Fundamentos](ruta/01-fundamentos/GUIA.md)

**3. ¿Sabes explicar qué hace `{k: v for k, v in pares if v > 0}` sin
buscarlo?**
Si no → [módulo 02 · Estructuras de datos](ruta/02-estructuras-de-datos/GUIA.md)

**4. ¿Sabes cuándo usar un `set` en vez de una `list`, y por qué?**
Si no → [módulo 02 · Estructuras de datos](ruta/02-estructuras-de-datos/GUIA.md)

**5. ¿Has escrito una clase con `__init__` y sabes qué aporta `@dataclass`?**
Si no → [módulo 03 · POO y módulos](ruta/03-poo-y-modulos/GUIA.md)

**6. ¿Has creado un entorno virtual y gestionado dependencias de un proyecto?**
Si no → [módulo 04 · Entorno y herramientas](ruta/04-entorno-y-herramientas/GUIA.md)

**7. ¿Has escrito tests con pytest, incluyendo alguna fixture?**
Si no → [módulo 05 · Testing](ruta/05-testing/GUIA.md)

**8. ¿Sabes qué hace `await` y por qué `async` no acelera un cálculo pesado?**
Si no → [módulo 06 · Async y concurrencia](ruta/06-async-y-concurrencia/GUIA.md)

**9. ¿Has consumido una API REST desde Python y validado la respuesta?**
Si no → [módulo 07 · Datos y APIs](ruta/07-datos-y-apis/GUIA.md)

**10. ¿Has llamado a un LLM desde código y manejado tool use?**
Si no → [módulo 08 · Fundamentos de LLMs](ruta/08-llms-fundamentos/GUIA.md)

**¿Respondiste que sí a todas?**
Vete directo a [LangGraph](ruta/09-agentes-langgraph/GUIA.md) y
[CrewAI](ruta/10-agentes-crewai/GUIA.md), que es a donde va esta ruta.

## Si vas sobrado en tu módulo

Cada guía abre diciendo sus prerrequisitos y a dónde saltar si ya dominas el
tema. Y cada módulo tiene ejercicios en `ejercicios/reto/` además de los de
`ejercicios/base/`: si los de base te resultan triviales, haz solo los retos.
```

- [ ] **Step 3: Verificar que no hay enlaces rotos a módulos**

Run:
```bash
uv run python -c "
import re, pathlib
raiz = pathlib.Path('.')
rotos = []
for doc in ('README.md', 'EMPIEZA-AQUI.md'):
    for destino in re.findall(r']\((?!https?:)([^)#]+)\)', pathlib.Path(doc).read_text(encoding='utf-8')):
        if not (raiz / destino).exists():
            rotos.append(f'{doc} -> {destino}')
print('\n'.join(rotos) if rotos else 'todos los enlaces locales existen')
"
```
Expected: `todos los enlaces locales existen`

Si aparece algún roto de `CONTRIBUTING.md`, `LICENSE`, `LICENSE-CONTENIDO`,
`.env.example` o `recursos/`, es esperado: se crean en las Tasks 7, 9 y 10.
Repite esta verificación al final de la Task 10.

- [ ] **Step 4: Commit**

```bash
git add README.md EMPIEZA-AQUI.md
git commit -m "docs: portada y autodiagnóstico de nivel"
```

---

### Task 7: Biblioteca de consulta

**Files:**
- Create: `recursos/enlaces/README.md`
- Create: `recursos/enlaces/general.md`
- Create: `recursos/enlaces/01-fundamentos.md`
- Create: `recursos/enlaces/09-agentes.md`
- Create: `recursos/cheatsheets/pytest.md`
- Create: `recursos/plantillas/README.md`

**Interfaces:**
- Consumes: nada.
- Produces: el formato de entrada de enlace que `CONTRIBUTING.md` documenta en la Task 10, y las rutas que la Task 8 pone en la navegación.

Se crean cuatro archivos de enlaces, no once: los demás los añade quien
escriba cada módulo. Un archivo vacío por módulo sería ruido.

- [ ] **Step 1: Crear `recursos/enlaces/README.md`**

````markdown
# Enlaces curados

Un archivo por tema. Cada entrada lleva tres etiquetas y una línea explicando
por qué vale la pena — sin esa línea, en seis meses esto son cien URLs y
ninguna razón para abrir ninguna.

## Formato

```markdown
### [Título del recurso](https://ejemplo.com)
`tipo` · `idioma` · `nivel` — Por qué vale la pena, en una línea.
```

- **tipo**: `artículo`, `vídeo`, `curso`, `libro`, `repo`, `doc-oficial`
- **idioma**: `es`, `en`
- **nivel**: `principiante`, `intermedio`, `avanzado`

## Índice

- [General](general.md) — Python en general, sin tema concreto
- [01 · Fundamentos](01-fundamentos.md)
- [09 · Agentes](09-agentes.md) — LangGraph y CrewAI

¿Falta el tema que buscas? Créalo siguiendo el nombre del módulo, o abre un
issue de tipo *proponer recurso*.
````

- [ ] **Step 2: Crear `recursos/enlaces/general.md`**

```markdown
# Enlaces · General

### [Documentación oficial de Python](https://docs.python.org/es/3/)
`doc-oficial` · `es` · `principiante` — Traducida al español y con un tutorial
completo. La referencia a la que volver siempre.

### [Real Python](https://realpython.com/)
`artículo` · `en` · `intermedio` — Artículos largos y bien editados. Cuando
buscas entender un tema a fondo, no resolver una duda de dos minutos.

### [Documentación de uv](https://docs.astral.sh/uv/)
`doc-oficial` · `en` · `principiante` — El gestor que usa este repositorio.
Vale la pena leer la sección de proyectos entera.

### [Ruff](https://docs.astral.sh/ruff/)
`doc-oficial` · `en` · `intermedio` — El linter y formateador del repositorio.
Consulta aquí qué significa cada código de error.
```

- [ ] **Step 3: Crear `recursos/enlaces/01-fundamentos.md`**

```markdown
# Enlaces · 01 Fundamentos

### [El tutorial oficial de Python](https://docs.python.org/es/3/tutorial/)
`doc-oficial` · `es` · `principiante` — En español y escrito por quienes hacen
el lenguaje. Los capítulos 3 al 5 cubren casi todo el módulo 01.

### [PEP 8 — Guía de estilo](https://peps.python.org/pep-0008/)
`doc-oficial` · `en` · `principiante` — Las convenciones que sigue todo el
mundo. Ruff las aplica por ti, pero conviene saber de dónde salen.

### [f-strings en profundidad](https://realpython.com/python-f-strings/)
`artículo` · `en` · `principiante` — Formateo de texto más allá de lo básico:
alineación, decimales, `!r`.
```

- [ ] **Step 4: Crear `recursos/enlaces/09-agentes.md`**

```markdown
# Enlaces · 09 Agentes

### [Documentación de LangGraph](https://langchain-ai.github.io/langgraph/)
`doc-oficial` · `en` · `intermedio` — Empieza por los tutoriales; los conceptos
de estado y checkpoints se entienden mejor con el código delante.

### [Documentación de CrewAI](https://docs.crewai.com/)
`doc-oficial` · `en` · `intermedio` — El modelo de agentes por roles explicado
desde cero, con ejemplos ejecutables.

### [Building effective agents (Anthropic)](https://www.anthropic.com/research/building-effective-agents)
`artículo` · `en` · `intermedio` — Cuándo un agente es la herramienta correcta
y cuándo basta con una cadena de prompts. Léelo antes de elegir framework.
```

- [ ] **Step 5: Crear `recursos/cheatsheets/pytest.md`**

````markdown
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
````

- [ ] **Step 6: Crear `recursos/plantillas/README.md`**

```markdown
# Plantillas

Scaffolds reutilizables para arrancar un proyecto sin partir de cero.

Todavía no hay ninguna. Las primeras previstas, según vayan haciendo falta:

- Proyecto FastAPI mínimo con tests
- Agente LangGraph con checkpoints
- Crew de CrewAI con dos agentes

¿Necesitas una? Ábrela como issue o léete `CONTRIBUTING.md` y súbela.
```

- [ ] **Step 7: Commit**

```bash
git add recursos/
git commit -m "docs: biblioteca de enlaces, cheatsheets y plantillas"
```

---

### Task 8: Sitio de documentación

**Files:**
- Create: `mkdocs.yml`

**Interfaces:**
- Consumes: `README.md`, `EMPIEZA-AQUI.md`, las `GUIA.md` de los once módulos, `recursos/`.
- Produces: `site/` al construir; lo consume `docs.yml` en la Task 11.

- [ ] **Step 1: Crear `mkdocs.yml`**

El plugin `same-dir` es lo que permite que la raíz del repositorio sea el
`docs_dir`. Sin él, MkDocs exigiría una carpeta `docs/` con copias del
markdown.

```yaml
site_name: Recursos Python · Nova AI
site_description: Ruta de capacitación en Python, de cero a agentes
repo_url: https://github.com/full-stack-dev-johncastrosanabria/recursos-python-nova-ai
edit_uri: edit/main/

theme:
  name: material
  language: es
  features:
    - navigation.sections
    - navigation.top
    - content.code.copy
    - search.highlight
  palette:
    - scheme: default
      primary: indigo
      toggle:
        icon: material/weather-night
        name: Modo oscuro
    - scheme: slate
      primary: indigo
      toggle:
        icon: material/weather-sunny
        name: Modo claro

plugins:
  - search:
      lang: es
  - same-dir

exclude_docs: |
  .venv/
  docs/superpowers/
  scripts/
  novatools/
  tests/

markdown_extensions:
  - admonition
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences

nav:
  - Inicio: README.md
  - Empieza aquí: EMPIEZA-AQUI.md
  - Ruta:
      - 01 · Fundamentos: ruta/01-fundamentos/GUIA.md
      - 02 · Estructuras de datos: ruta/02-estructuras-de-datos/GUIA.md
      - 03 · POO y módulos: ruta/03-poo-y-modulos/GUIA.md
      - 04 · Entorno y herramientas: ruta/04-entorno-y-herramientas/GUIA.md
      - 05 · Testing: ruta/05-testing/GUIA.md
      - 06 · Async y concurrencia: ruta/06-async-y-concurrencia/GUIA.md
      - 07 · Datos y APIs: ruta/07-datos-y-apis/GUIA.md
      - 08 · Fundamentos de LLMs: ruta/08-llms-fundamentos/GUIA.md
      - 09 · Agentes con LangGraph: ruta/09-agentes-langgraph/GUIA.md
      - 10 · Agentes con CrewAI: ruta/10-agentes-crewai/GUIA.md
      - 11 · Proyecto final: ruta/11-proyecto-final/GUIA.md
  - Recursos:
      - Enlaces: recursos/enlaces/README.md
      - General: recursos/enlaces/general.md
      - 01 · Fundamentos: recursos/enlaces/01-fundamentos.md
      - 09 · Agentes: recursos/enlaces/09-agentes.md
      - Cheatsheet de pytest: recursos/cheatsheets/pytest.md
      - Plantillas: recursos/plantillas/README.md
  - Contribuir: CONTRIBUTING.md
```

- [ ] **Step 2: Construir el sitio**

`CONTRIBUTING.md` aún no existe (Task 10), así que `--strict` fallará por esa
referencia. Construye sin `--strict` para verificar el resto:

Run: `uv sync --group docs && uv run mkdocs build`
Expected: genera `site/`. Advertencia sobre `CONTRIBUTING.md`; cualquier otro
error hay que corregirlo ahora.

- [ ] **Step 3: Revisar el sitio en local**

Run: `uv run mkdocs serve`
Expected: sirve en `http://127.0.0.1:8000`. Comprobar que la portada carga, que
la ruta lista los once módulos y que el módulo 01 muestra su guía completa.
Cortar con `Ctrl+C`.

- [ ] **Step 4: Commit**

```bash
git add mkdocs.yml pyproject.toml uv.lock
git commit -m "feat: sitio de documentación con MkDocs Material"
```

---

### Task 9: Entorno de nivel cero

**Files:**
- Create: `.devcontainer/devcontainer.json`
- Create: `.env.example`

**Interfaces:**
- Consumes: `pyproject.toml` de la Task 1.
- Produces: nada que otras tareas consuman.

- [ ] **Step 1: Crear `.devcontainer/devcontainer.json`**

Se instala `uv` con su script oficial en vez de un devcontainer feature de
terceros: una dependencia menos que pueda romperse.

```json
{
  "name": "recursos-python-nova-ai",
  "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bookworm",
  "postCreateCommand": "curl -LsSf https://astral.sh/uv/install.sh | sh && $HOME/.local/bin/uv sync --group dev",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "charliermarsh.ruff"
      ],
      "settings": {
        "python.defaultInterpreterPath": ".venv/bin/python",
        "python.testing.pytestEnabled": true
      }
    }
  }
}
```

- [ ] **Step 2: Crear `.env.example`**

```
# Copia este archivo a .env y pon tus propias claves.
# .env está en .gitignore: nunca subas claves reales al repositorio.

# Necesaria a partir del módulo 08.
ANTHROPIC_API_KEY=

# Solo si algún ejercicio la pide explícitamente.
OPENAI_API_KEY=

# Alternativa local sin coste. Ver ruta/08-llms-fundamentos/GUIA.md
OLLAMA_BASE_URL=http://localhost:11434
```

- [ ] **Step 3: Verificar que el JSON es válido**

Run: `uv run python -c "import json,pathlib; json.loads(pathlib.Path('.devcontainer/devcontainer.json').read_text()); print('devcontainer.json válido')"`
Expected: `devcontainer.json válido`

- [ ] **Step 4: Verificar que `.env` está ignorado**

Run: `git check-ignore -v .env`
Expected: muestra la línea de `.gitignore` que lo cubre. Si no imprime nada, la
entrada falta y hay que añadirla.

- [ ] **Step 5: Commit**

```bash
git add .devcontainer/ .env.example
git commit -m "feat: devcontainer para Codespaces y ejemplo de variables"
```

---

### Task 10: Contribución y licencias

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `LICENSE`
- Create: `LICENSE-CONTENIDO`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/ISSUE_TEMPLATE/recurso.yml`
- Create: `.github/ISSUE_TEMPLATE/error-guia.yml`

**Interfaces:**
- Consumes: el formato de enlace de la Task 7, la anatomía de módulo de la Task 4.
- Produces: `CONTRIBUTING.md`, que la navegación de MkDocs (Task 8) ya referencia.

- [ ] **Step 1: Escribir `CONTRIBUTING.md`**

````markdown
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
````

- [ ] **Step 2: Crear `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2026 John Benjamin Castro Sanabria

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Crear `LICENSE-CONTENIDO` (CC BY 4.0)**

```
Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) 2026 John Benjamin Castro Sanabria

Esta licencia cubre el CONTENIDO de este repositorio: las guías (GUIA.md), los
cheatsheets, las listas de enlaces y el resto de material didáctico en
markdown. El código fuente se distribuye bajo la licencia MIT del archivo
LICENSE.

Eres libre de:

  Compartir — copiar y redistribuir el material en cualquier medio o formato.
  Adaptar — remezclar, transformar y construir a partir del material para
  cualquier finalidad, incluso comercial.

Bajo la siguiente condición:

  Atribución — Debes reconocer la autoría de manera adecuada, proporcionar un
  enlace a la licencia e indicar si se han realizado cambios. Puedes hacerlo
  de cualquier manera razonable, pero no de una manera que sugiera que tienes
  el apoyo del licenciador o lo recibes por el uso que haces.

No hay restricciones adicionales: no puedes aplicar términos legales ni
medidas tecnológicas que restrinjan legalmente a otros hacer cualquier uso
permitido por la licencia.

Texto legal completo:
https://creativecommons.org/licenses/by/4.0/legalcode.es
```

- [ ] **Step 4: Crear `.github/PULL_REQUEST_TEMPLATE.md`**

```markdown
## Qué aporta este PR

<!-- Una o dos frases. -->

## Tipo

- [ ] Enlace nuevo en `recursos/enlaces/`
- [ ] Ejercicio nuevo (stub + solución + test)
- [ ] Guía nueva o ampliada
- [ ] Corrección de un error
- [ ] Infraestructura

## Comprobado

- [ ] `uv run ruff check .` sin errores
- [ ] `NOVA_SOLUCIONES=1 uv run pytest` en verde
- [ ] Si añadí un ejercicio: sin la variable **falla**, con la variable **pasa**
- [ ] Si añadí enlaces: llevan las tres etiquetas y la línea de por qué
- [ ] No hay ninguna clave de API real
```

- [ ] **Step 5: Crear `.github/ISSUE_TEMPLATE/recurso.yml`**

```yaml
name: Proponer un recurso
description: Un enlace, curso o libro que merece estar en la biblioteca
title: "[Recurso] "
labels: ["recurso"]
body:
  - type: input
    id: url
    attributes:
      label: Enlace
      placeholder: https://
    validations:
      required: true
  - type: dropdown
    id: tipo
    attributes:
      label: Tipo
      options: [artículo, vídeo, curso, libro, repo, doc-oficial]
    validations:
      required: true
  - type: dropdown
    id: nivel
    attributes:
      label: Nivel
      options: [principiante, intermedio, avanzado]
    validations:
      required: true
  - type: input
    id: modulo
    attributes:
      label: Módulo relacionado
      placeholder: "05-testing, o 'general' si no encaja en ninguno"
    validations:
      required: true
  - type: textarea
    id: porque
    attributes:
      label: Por qué vale la pena
      description: Una línea. Es lo que acabará en la lista.
    validations:
      required: true
```

- [ ] **Step 6: Crear `.github/ISSUE_TEMPLATE/error-guia.yml`**

```yaml
name: Error en una guía
description: Algo está mal, poco claro o no funciona
title: "[Error] "
labels: ["error-guia"]
body:
  - type: markdown
    attributes:
      value: |
        Si estás aprendiendo y algo no te cuadra, este issue es para ti.
        No hace falta que sepas cuál es la solución.
  - type: input
    id: donde
    attributes:
      label: Dónde
      placeholder: "ruta/01-fundamentos/GUIA.md, sección 3"
    validations:
      required: true
  - type: textarea
    id: problema
    attributes:
      label: Qué pasa
      description: Qué esperabas y qué te encontraste.
    validations:
      required: true
  - type: textarea
    id: entorno
    attributes:
      label: Cómo lo estás ejecutando
      placeholder: "Codespaces, o macOS con uv 0.11"
```

- [ ] **Step 7: Verificar los YAML y la construcción estricta del sitio**

Run:
```bash
uv run python -c "
import pathlib, yaml
for p in sorted(pathlib.Path('.github/ISSUE_TEMPLATE').glob('*.yml')):
    yaml.safe_load(p.read_text(encoding='utf-8'))
    print(f'{p} válido')
" 2>/dev/null || uv run --with pyyaml python -c "
import pathlib, yaml
for p in sorted(pathlib.Path('.github/ISSUE_TEMPLATE').glob('*.yml')):
    yaml.safe_load(p.read_text(encoding='utf-8'))
    print(f'{p} válido')
"
```
Expected: las dos plantillas marcadas como válidas.

Run: `uv run mkdocs build --strict`
Expected: construye sin advertencias. Ahora `CONTRIBUTING.md` ya existe.

- [ ] **Step 8: Repetir la verificación de enlaces locales de la Task 6**

Run:
```bash
uv run python -c "
import re, pathlib
raiz = pathlib.Path('.')
rotos = []
for doc in ('README.md', 'EMPIEZA-AQUI.md', 'CONTRIBUTING.md'):
    for destino in re.findall(r']\((?!https?:)([^)#]+)\)', pathlib.Path(doc).read_text(encoding='utf-8')):
        if not (raiz / destino).exists():
            rotos.append(f'{doc} -> {destino}')
print('\n'.join(rotos) if rotos else 'todos los enlaces locales existen')
"
```
Expected: `todos los enlaces locales existen`

- [ ] **Step 9: Commit**

```bash
git add CONTRIBUTING.md LICENSE LICENSE-CONTENIDO .github/
git commit -m "docs: guía de contribución, licencias y plantillas"
```

---

### Task 11: Integración continua

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/enlaces.yml`
- Create: `.github/workflows/docs.yml`

**Interfaces:**
- Consumes: `pyproject.toml`, `mkdocs.yml`, y la variable `NOVA_SOLUCIONES` de la Task 2.
- Produces: nada que otras tareas consuman en local; se verifica de verdad en la Task 12.

- [ ] **Step 1: Crear `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  calidad:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Instalar uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true

      - name: Sincronizar dependencias
        run: uv sync --group dev

      - name: Lint
        run: uv run ruff check .

      - name: Formato
        run: uv run ruff format --check .

      - name: Tests contra las soluciones de referencia
        # Verifica que cada ejercicio publicado es realmente resoluble.
        env:
          NOVA_SOLUCIONES: "1"
        run: uv run pytest -v
```

- [ ] **Step 2: Crear `.github/workflows/enlaces.yml`**

```yaml
name: Enlaces

on:
  pull_request:
    paths:
      - "recursos/**"
      - "**/*.md"
  schedule:
    # Lunes a las 06:00 UTC.
    - cron: "0 6 * * 1"
  workflow_dispatch:

jobs:
  lychee:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Buscar enlaces rotos
        uses: lycheeverse/lychee-action@v2
        with:
          # 429 es rate limiting, no un enlace roto.
          args: >-
            --no-progress
            --accept 200,206,429
            --exclude-path .venv
            --exclude-path site
            './**/*.md'
          fail: true
```

- [ ] **Step 3: Crear `.github/workflows/docs.yml`**

```yaml
name: Docs

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Instalar uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true

      - name: Construir el sitio
        run: |
          uv sync --group docs
          uv run mkdocs build --strict

      - uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 4: Reproducir el CI en local antes de subirlo**

Run:
```bash
uv sync --group dev && \
uv run ruff check . && \
uv run ruff format --check . && \
NOVA_SOLUCIONES=1 uv run pytest -v
```
Expected: PASS, 23 tests, sin errores de lint ni de formato.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/
git commit -m "ci: lint, tests contra soluciones, enlaces y despliegue de docs"
```

---

### Task 12: Publicar en GitHub

**Files:**
- Modifica: configuración remota del repositorio (no archivos).

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: el repositorio público y el sitio publicado.

> **Confirmar con el usuario antes del Step 2.** Ese paso publica el
> repositorio y su contenido queda accesible públicamente e indexable.

- [ ] **Step 1: Verificar la cuenta activa de gh**

Run: `gh api user --jq .login`
Expected: `full-stack-dev-johncastrosanabria`

Si devuelve otra cuenta: `gh auth switch --user full-stack-dev-johncastrosanabria`

- [ ] **Step 2: Crear el repositorio público y subir**

Run:
```bash
gh repo create recursos-python-nova-ai \
  --public \
  --source=. \
  --remote=origin \
  --description "Ruta de capacitación en Python para el equipo de Nova AI: de fundamentos a agentes con LangGraph y CrewAI" \
  --push
```
Expected: imprime la URL del repositorio creado y sube `main`.

- [ ] **Step 3: Añadir los topics**

Run:
```bash
gh repo edit --add-topic python,aprendizaje,langgraph,crewai,agentes,capacitacion
```
Expected: sin errores.

- [ ] **Step 4: Activar GitHub Pages**

Run: `gh api -X POST repos/:owner/recursos-python-nova-ai/pages -f build_type=workflow`
Expected: responde con la configuración de Pages. Si devuelve `409 Conflict`,
Pages ya estaba activado: continúa.

- [ ] **Step 5: Verificar que los workflows pasan**

Run: `gh run list --limit 5`
Expected: aparecen `CI` y `Docs`. Esperar a que terminen:

Run: `gh run watch`
Expected: ambos en `success`.

Si `CI` falla por la versión de una action (`astral-sh/setup-uv@v6` o
`actions/checkout@v5`), consultar la versión vigente con
`gh api repos/astral-sh/setup-uv/releases/latest --jq .tag_name`, actualizar el
workflow, commitear y volver a verificar.

- [ ] **Step 6: Verificar el sitio publicado**

Run: `gh api repos/:owner/recursos-python-nova-ai/pages --jq .html_url`
Expected: imprime la URL. Abrirla y comprobar que la portada carga y que el
módulo 01 se ve completo.

- [ ] **Step 7: Verificar que no se subió ninguna clave**

Run: `git log --all -p | grep -iE "(sk-ant|sk-proj|ghp_|gho_)" | head`
Expected: sin resultados.

---

## Verificación final

Con las doce tareas completas, esto debe cumplirse:

- [ ] `uv sync && uv run pytest ruta/01-fundamentos` falla con `NotImplementedError` (estado correcto para el aprendiz)
- [ ] `NOVA_SOLUCIONES=1 uv run pytest` pasa los 23 tests
- [ ] `uv run ruff check . && uv run ruff format --check .` sin errores
- [ ] `uv run mkdocs build --strict` construye sin advertencias
- [ ] `ruta/` tiene once módulos; solo el 01 con contenido
- [ ] El repositorio es público en `full-stack-dev-johncastrosanabria`
- [ ] CI y Docs en verde en GitHub
- [ ] El sitio de Pages carga
- [ ] `main` sin reglas de protección
- [ ] Ninguna clave de API en el historial de git
