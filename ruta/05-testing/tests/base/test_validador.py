"""Los errores son parte del contrato, así que se prueban igual que el resto.

Fíjate en que aquí no basta con comprobar que "falla": se comprueba QUÉ error
concreto sale, que la jerarquía permite capturarlos en bloque, y que el mensaje
dice lo suficiente para arreglar el problema sin reproducirlo.
"""

import pytest


@pytest.mark.parametrize(
    "valor",
    ["CR01-0002", "CR99-9999", "CR00-0000"],
)
def test_acepta_cuentas_bien_formadas(solution, valor):
    assert solution.validate_account(valor) == valor


def test_normaliza_espacios_y_mayusculas(solution):
    assert solution.validate_account("  cr01-0002  ") == "CR01-0002"


@pytest.mark.parametrize("valor", ["", "   ", "\n", "\t "])
def test_una_cuenta_vacia_tiene_su_propio_error(solution, valor):
    with pytest.raises(solution.EmptyAccount):
        solution.validate_account(valor)


@pytest.mark.parametrize(
    "valor",
    [
        "CR1-0002",  # un dígito de menos en el banco
        "CR001-0002",  # uno de más
        "CR01-002",  # faltan dígitos en la cuenta
        "CR01-00021",  # sobran
        "US01-0002",  # otro país
        "CR010002",  # sin guion
        "CR01_0002",  # guion bajo en vez de guion
        "cuenta",  # nada que ver
        "CR01-000X",  # una letra donde va un dígito
    ],
)
def test_los_formatos_invalidos_tienen_su_propio_error(solution, valor):
    with pytest.raises(solution.InvalidFormat):
        solution.validate_account(valor)


def test_ambos_errores_comparten_familia(solution):
    """Quien solo quiera saber 'no vale' captura AccountError y ya."""
    assert issubclass(solution.EmptyAccount, solution.AccountError)
    assert issubclass(solution.InvalidFormat, solution.AccountError)


def test_se_pueden_capturar_en_bloque(solution):
    with pytest.raises(solution.AccountError):
        solution.validate_account("")

    with pytest.raises(solution.AccountError):
        solution.validate_account("basura")


def test_el_mensaje_incluye_el_valor_recibido(solution):
    """Un error que no dice qué llegó obliga a reproducir el problema."""
    with pytest.raises(solution.InvalidFormat) as error:
        solution.validate_account("CR1-0002")

    assert "CR1-0002" in str(error.value)
