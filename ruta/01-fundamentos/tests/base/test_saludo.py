def test_greet_saluda_por_nombre(solution):
    assert solution.greet("Ana") == "Hola, Ana"


def test_greet_funciona_con_cualquier_nombre(solution):
    assert solution.greet("Beto") == "Hola, Beto"


def test_greet_recorta_espacios_sobrantes(solution):
    assert solution.greet("  Ana  ") == "Hola, Ana"
