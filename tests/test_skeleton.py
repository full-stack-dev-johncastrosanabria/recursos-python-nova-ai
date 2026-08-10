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
