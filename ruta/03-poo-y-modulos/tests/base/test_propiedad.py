import pytest


def test_guarda_la_temperatura(solution):
    assert solution.Thermostat(21).celsius == 21


def test_fahrenheit_es_derivada(solution):
    assert solution.Thermostat(21).fahrenheit == pytest.approx(69.8)


def test_cero_celsius_son_32_fahrenheit(solution):
    assert solution.Thermostat(0).fahrenheit == 32


def test_el_setter_de_celsius_actualiza(solution):
    termo = solution.Thermostat(21)

    termo.celsius = 25

    assert termo.celsius == 25
    assert termo.fahrenheit == 77


def test_escribir_en_fahrenheit_cambia_el_celsius(solution):
    termo = solution.Thermostat(21)

    termo.fahrenheit = 104

    assert termo.celsius == pytest.approx(40)


@pytest.mark.parametrize("valor", [-91, 61, 1000, -273])
def test_una_temperatura_fuera_de_rango_es_un_error(solution, valor):
    with pytest.raises(ValueError):
        solution.Thermostat(valor)


def test_el_setter_tambien_valida(solution):
    termo = solution.Thermostat(21)

    with pytest.raises(ValueError):
        termo.celsius = 500


def test_el_setter_de_fahrenheit_tambien_valida(solution):
    """500 °F son 260 °C: la validación tiene que aplicarse por las dos vías."""
    termo = solution.Thermostat(21)

    with pytest.raises(ValueError):
        termo.fahrenheit = 500


def test_el_error_menciona_el_valor(solution):
    with pytest.raises(ValueError) as error:
        solution.Thermostat(500)

    assert "500" in str(error.value)


def test_los_extremos_del_rango_son_validos(solution):
    assert solution.Thermostat(-90).celsius == -90
    assert solution.Thermostat(60).celsius == 60


def test_una_temperatura_fallida_no_deja_el_objeto_a_medias(solution):
    termo = solution.Thermostat(21)

    with pytest.raises(ValueError):
        termo.celsius = 500

    assert termo.celsius == 21
