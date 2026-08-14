DATOS = {"total": 1500, "operaciones": 3, "cliente": "ACME"}


def test_todo_respaldado(solution):
    texto = "El total fue 1500 en 3 operaciones"

    assert solution.unsupported_numbers(texto, DATOS) == []


def test_detecta_una_cifra_inventada(solution):
    texto = "El total fue 1500 en 4 operaciones"

    assert solution.unsupported_numbers(texto, DATOS) == ["4"]


def test_acepta_separadores_de_miles(solution):
    """El informe puede escribir el número como quiera."""
    texto = "El total fue 1,500"

    assert solution.unsupported_numbers(texto, DATOS) == []


def test_acepta_decimales_que_no_aportan(solution):
    texto = "El total fue 1500.00"

    assert solution.unsupported_numbers(texto, DATOS) == []


def test_detecta_varias_inventadas(solution):
    texto = "Fueron 99 casos y 1500 en total, con 7 incidencias"

    assert solution.unsupported_numbers(texto, DATOS) == ["99", "7"]


def test_las_devuelve_en_orden_de_aparicion(solution):
    texto = "primero 88 y luego 99"

    assert solution.unsupported_numbers(texto, DATOS) == ["88", "99"]


def test_no_repite_la_misma_cifra(solution):
    texto = "99 aquí y 99 allá"

    assert solution.unsupported_numbers(texto, DATOS) == ["99"]


def test_las_devuelve_tal_como_aparecen(solution):
    """Quien lea el aviso tiene que poder buscarlas en el informe."""
    texto = "el importe fue 12,345"

    assert solution.unsupported_numbers(texto, DATOS) == ["12,345"]


def test_un_texto_sin_numeros(solution):
    assert solution.unsupported_numbers("todo correcto", DATOS) == []


def test_un_texto_vacio(solution):
    assert solution.unsupported_numbers("", DATOS) == []


def test_los_valores_no_numericos_no_respaldan(solution):
    """Un nombre de cliente no respalda cifras."""
    assert solution.unsupported_numbers("son 1500", {"cliente": "1500"}) == ["1500"]


def test_sin_datos_todo_es_sospechoso(solution):
    assert solution.unsupported_numbers("son 1500", {}) == ["1500"]


def test_acepta_decimales_de_verdad(solution):
    datos = {"media": 12.5}

    assert solution.unsupported_numbers("la media fue 12.5", datos) == []


def test_el_caso_real_del_modulo(solution):
    datos = {"total_cents": 1_580_870, "operaciones": 42, "media": 37639}
    informe = (
        "Esta semana se procesaron 42 operaciones por un total de 1,580,870 "
        "céntimos, con una media de 37639. Se detectaron 5 incidencias."
    )

    assert solution.unsupported_numbers(informe, datos) == ["5"]
