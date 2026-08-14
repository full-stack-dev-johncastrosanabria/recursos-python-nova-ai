"""Tres tests que pasan sobre código roto.

Córrelo con:
    uv run python ruta/05-testing/ejemplos/tests_que_no_prueban.py

No usa pytest a propósito: son asserts a pelo para que veas que el problema no
es la herramienta, es qué se comprueba.
"""


# ── Una implementación claramente rota ────────────────────────────
def reconcile_roto(bank_refs, internal_refs):
    """Debería devolver las tres secciones. Devuelve cualquier cosa."""
    return {"matched": set(), "only_bank": set(), "only_internal": set()}


# ── Test 1: el que no afirma nada ─────────────────────────────────
def test_inutil():
    resultado = reconcile_roto(["A", "B"], ["B", "C"])
    assert resultado is not None  # casi nada del universo es None


# ── Test 2: el que prueba el doble, no el código ──────────────────
class RepositorioFalso:
    def __init__(self):
        self.llamadas = 0

    def save(self, item):
        self.llamadas += 1


def guardar_roto(repo, item):
    repo.save(item)  # guarda… ¿y si el item va vacío? nadie lo mira


def test_prueba_el_mock():
    repo = RepositorioFalso()
    guardar_roto(repo, None)  # ← guardando un None
    assert repo.llamadas == 1  # "pasa": comprobó que llamaste, no que sirviera


# ── Test 3: el gigante, cuyo fallo no dice qué se rompió ──────────
def test_flujo_completo():
    resultado = reconcile_roto(["A"], ["A"])
    assert isinstance(resultado, dict)
    assert "matched" in resultado
    assert "only_bank" in resultado
    assert "only_internal" in resultado
    # ...y ni uno solo comprueba los VALORES


for test in (test_inutil, test_prueba_el_mock, test_flujo_completo):
    test()
    print(f"✓ {test.__name__} pasa")

print("\nTres tests en verde, cobertura alta, y reconcile está roto:")
print("  reconcile_roto(['A'], ['A']) ->", reconcile_roto(["A"], ["A"]))
print("  debería haber devuelto matched={'A'}")

print("\n── El test que sí sirve ──")


def test_util():
    resultado = reconcile_roto(["A", "B"], ["B", "C"])
    assert resultado["matched"] == {"B"}


try:
    test_util()
except AssertionError:
    print("✗ test_util FALLA, que es justo lo que queríamos:")
    print("  comprueba el valor concreto, no la forma.")

print(
    "\nLa cobertura mide qué líneas se ejecutaron, no si comprobaste algo\n"
    "útil sobre ellas. Es un mapa de dónde NO has mirado."
)
