import pytest


def test_celsius_to_fahrenheit_en_el_punto_de_congelacion(solution):
    assert solution.celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_en_el_punto_de_ebullicion(solution):
    assert solution.celsius_to_fahrenheit(100) == 212


def test_celsius_to_fahrenheit_admite_negativos(solution):
    assert solution.celsius_to_fahrenheit(-40) == -40


def test_celsius_to_fahrenheit_admite_decimales(solution):
    assert solution.celsius_to_fahrenheit(36.6) == pytest.approx(97.88)
