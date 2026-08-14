import pytest


def test_las_constantes_son_bits_distintos(solution):
    assert solution.LEER == 4
    assert solution.ESCRIBIR == 2
    assert solution.EJECUTAR == 1


def test_grant_activa_una_bandera(solution):
    assert solution.grant(0, solution.LEER) == 4


def test_grant_no_toca_las_demas(solution):
    assert solution.grant(solution.LEER, solution.ESCRIBIR) == 6


def test_grant_es_idempotente(solution):
    """Activar lo que ya está activo no cambia nada."""
    assert solution.grant(6, solution.LEER) == 6


def test_revoke_desactiva_una_bandera(solution):
    assert solution.revoke(6, solution.ESCRIBIR) == 4


def test_revoke_de_algo_inactivo_no_cambia_nada(solution):
    assert solution.revoke(4, solution.ESCRIBIR) == 4


def test_revoke_no_toca_las_demas(solution):
    assert solution.revoke(7, solution.ESCRIBIR) == 5


def test_has_detecta_las_activas(solution):
    assert solution.has(6, solution.LEER) is True
    assert solution.has(6, solution.ESCRIBIR) is True


def test_has_detecta_las_inactivas(solution):
    assert solution.has(6, solution.EJECUTAR) is False


def test_has_devuelve_un_booleano_no_un_entero(solution):
    """`permisos & LEER` da 4, que es verdadero pero no es True."""
    assert solution.has(4, solution.LEER) is True


@pytest.mark.parametrize(
    ("permisos", "esperado"),
    [
        (7, "rwx"),
        (6, "rw-"),
        (5, "r-x"),
        (4, "r--"),
        (3, "-wx"),
        (2, "-w-"),
        (1, "--x"),
        (0, "---"),
    ],
)
def test_describe(solution, permisos, esperado):
    assert solution.describe(permisos) == esperado


def test_un_ciclo_completo(solution):
    permisos = 0
    permisos = solution.grant(permisos, solution.LEER)
    permisos = solution.grant(permisos, solution.EJECUTAR)

    assert solution.describe(permisos) == "r-x"

    permisos = solution.revoke(permisos, solution.EJECUTAR)

    assert solution.describe(permisos) == "r--"
