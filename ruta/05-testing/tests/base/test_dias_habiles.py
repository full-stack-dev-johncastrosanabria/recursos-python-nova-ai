"""Una tabla de casos, un solo test.

Marzo de 2026 empieza en domingo: el 2 es lunes, el 6 viernes, el 7 sábado.
Tener eso presente hace legible toda la tabla de abajo.
"""

from datetime import date

import pytest


@pytest.mark.parametrize(
    ("start", "end", "esperado"),
    [
        # una semana laboral completa: de lunes a sábado excluido
        (date(2026, 3, 2), date(2026, 3, 7), 5),
        # hasta el lunes siguiente: el fin de semana no suma
        (date(2026, 3, 2), date(2026, 3, 9), 5),
        # un solo día hábil
        (date(2026, 3, 2), date(2026, 3, 3), 1),
        # rango vacío: mismo día
        (date(2026, 3, 2), date(2026, 3, 2), 0),
        # solo fin de semana
        (date(2026, 3, 7), date(2026, 3, 9), 0),
        # empieza un domingo
        (date(2026, 3, 1), date(2026, 3, 2), 0),
        # cruza el fin de semana: viernes y lunes
        (date(2026, 3, 6), date(2026, 3, 10), 2),
        # dos semanas completas
        (date(2026, 3, 2), date(2026, 3, 16), 10),
    ],
)
def test_business_days_between(solution, start, end, esperado):
    assert solution.business_days_between(start, end) == esperado


def test_un_rango_invertido_no_es_un_error_sino_cero(solution):
    """Un rango vacío tiene cero días hábiles. No hay nada que reportar."""
    assert solution.business_days_between(date(2026, 3, 9), date(2026, 3, 2)) == 0


def test_un_mes_entero(solution):
    """Marzo de 2026 tiene 22 días hábiles."""
    assert solution.business_days_between(date(2026, 3, 1), date(2026, 4, 1)) == 22
