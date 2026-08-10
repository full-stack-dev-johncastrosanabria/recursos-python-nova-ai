"""Tests del generador de esqueletos de módulo."""

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
    assert "**Prerrequisitos:** módulos 01–04" in guide
    assert "**Tiempo estimado:** 90 min" in guide
    assert "**Si ya dominas esto:** salta al módulo 06" in guide


def test_render_guide_lista_los_objetivos():
    guide = render_guide(EXAMPLE)
    assert "- Escribir un test con pytest" in guide
    assert "- Usar fixtures" in guide


def test_create_module_crea_todas_las_subcarpetas(tmp_path):
    module_dir = create_module(tmp_path, EXAMPLE)

    assert module_dir == tmp_path / "ruta" / "05-testing"
    for sub in SUBFOLDERS:
        assert (module_dir / sub).is_dir(), f"falta {sub}"


def test_create_module_escribe_la_guia(tmp_path):
    module_dir = create_module(tmp_path, EXAMPLE)

    guide = (module_dir / "GUIA.md").read_text(encoding="utf-8")
    assert "# Módulo 05 · Testing" in guide


def test_create_module_es_idempotente(tmp_path):
    create_module(tmp_path, EXAMPLE)
    module_dir = create_module(tmp_path, EXAMPLE)

    assert (module_dir / "GUIA.md").exists()
