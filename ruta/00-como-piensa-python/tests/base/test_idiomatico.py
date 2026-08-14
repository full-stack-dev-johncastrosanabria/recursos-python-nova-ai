def test_active_names_devuelve_solo_los_activos(solution):
    users = [
        {"name": "Ana", "active": True},
        {"name": "Beto", "active": False},
        {"name": "Carla", "active": True},
    ]

    assert solution.active_names(users) == ["Ana", "Carla"]


def test_active_names_conserva_el_orden_de_entrada(solution):
    users = [
        {"name": "Zoe", "active": True},
        {"name": "Ana", "active": True},
    ]

    assert solution.active_names(users) == ["Zoe", "Ana"]


def test_active_names_con_lista_vacia(solution):
    assert solution.active_names([]) == []


def test_active_names_cuando_ninguno_esta_activo(solution):
    users = [{"name": "Ana", "active": False}]

    assert solution.active_names(users) == []
