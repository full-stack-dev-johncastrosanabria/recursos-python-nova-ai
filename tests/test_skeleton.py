"""Tests del generador de esqueletos de módulo."""

import pytest

from novatools.skeleton import (
    SUBFOLDERS,
    ModuleSpec,
    create_module,
    folder_name,
    render_guide,
)

EXAMPLE = ModuleSpec(
    number=5,
    slug="testing",
    title="Testing",
    prerequisites="módulos 01–04",
    minutes=90,
    skip_to="salta al módulo 06",
    objectives=("Escribir un test con pytest", "Usar fixtures"),
)


def test_folder_name_rellena_con_cero():
    assert folder_name(EXAMPLE) == "05-testing"


def test_render_guide_incluye_la_cabecera_fija():
    guide = render_guide(EXAMPLE)
    assert "# Módulo 05 · Testing" in guide
    assert "**Prerrequisitos:** módulos 01–04<br>" in guide
    assert "**Tiempo estimado:** 90 min<br>" in guide
    assert "**Si ya dominas esto:** salta al módulo 06" in guide


def test_render_guide_lista_los_objetivos():
    guide = render_guide(EXAMPLE)
    assert "- Escribir un test con pytest" in guide
    assert "- Usar fixtures" in guide


def test_render_guide_trae_todas_las_secciones_de_la_anatomia():
    """Toda guía comparte la misma anatomía, la escriba quien la escriba."""
    guide = render_guide(EXAMPLE)
    for section in (
        "## Qué vas a poder hacer al terminar",
        "## Contenido",
        "## Caso real",
        "## Ejercicios",
        "## Resumen",
        "## Preguntas de repaso",
        "## Recursos",
        "## Siguiente",
    ):
        assert section in guide, f"falta la sección {section}"


def test_create_module_crea_todas_las_subcarpetas(tmp_path):
    module_dir = create_module(tmp_path, EXAMPLE)

    assert module_dir == tmp_path / "ruta" / "05-testing"
    for sub in SUBFOLDERS:
        assert (module_dir / sub).is_dir(), f"falta {sub}"


def test_create_module_escribe_la_guia(tmp_path):
    module_dir = create_module(tmp_path, EXAMPLE)

    guide = (module_dir / "GUIA.md").read_text(encoding="utf-8")
    assert "# Módulo 05 · Testing" in guide


def test_create_module_no_sobrescribe_una_guia_existente(tmp_path):
    create_module(tmp_path, EXAMPLE)
    guide_path = tmp_path / "ruta" / "05-testing" / "GUIA.md"
    original_content = guide_path.read_text(encoding="utf-8")

    otro_spec = ModuleSpec(
        number=5,
        slug="testing",
        title="Otro título completamente distinto",
        prerequisites="nada",
        minutes=1,
        skip_to="nunca",
        objectives=("otro objetivo",),
    )

    with pytest.raises(FileExistsError):
        create_module(tmp_path, otro_spec)

    assert guide_path.read_text(encoding="utf-8") == original_content


def test_create_module_lanza_excepcion_con_ruta_y_como_forzar(tmp_path):
    create_module(tmp_path, EXAMPLE)

    with pytest.raises(FileExistsError) as exc_info:
        create_module(tmp_path, EXAMPLE)

    message = str(exc_info.value)
    assert "GUIA.md" in message
    assert "force" in message


def test_create_module_con_force_si_sobrescribe(tmp_path):
    create_module(tmp_path, EXAMPLE)

    otro_spec = ModuleSpec(
        number=5,
        slug="testing",
        title="Otro título completamente distinto",
        prerequisites="nada",
        minutes=1,
        skip_to="nunca",
        objectives=("otro objetivo",),
    )

    module_dir = create_module(tmp_path, otro_spec, force=True)

    guide = (module_dir / "GUIA.md").read_text(encoding="utf-8")
    assert "Otro título completamente distinto" in guide
