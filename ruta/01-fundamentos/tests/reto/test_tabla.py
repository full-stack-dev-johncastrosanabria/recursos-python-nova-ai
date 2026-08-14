FILAS = [("café", 3, 150_000), ("azúcar", 12, 99)]


def test_una_fila_tiene_el_ancho_total(solution):
    fila = solution.render_row("café", 3, 150_000)

    assert len(fila) == 31


def test_el_producto_va_a_la_izquierda(solution):
    fila = solution.render_row("café", 3, 150_000)

    assert fila.startswith("café        ")


def test_la_cantidad_va_a_la_derecha(solution):
    fila = solution.render_row("café", 3, 150_000)

    assert fila[12:17] == "    3"


def test_el_importe_va_a_la_derecha_y_con_formato(solution):
    fila = solution.render_row("café", 3, 150_000)

    assert fila[17:] == "      1,500.00"


def test_una_fila_completa(solution):
    assert solution.render_row("café", 3, 150_000) == (
        "café            3      1,500.00"
    )


def test_importes_pequenos_llevan_los_dos_decimales(solution):
    assert solution.render_row("azúcar", 12, 99).endswith("0.99")


def test_un_producto_largo_no_se_recorta(solution):
    """Mutilar un nombre para que quepa es peor que una fila torcida."""
    fila = solution.render_row("café de especialidad", 1, 100)

    assert "café de especialidad" in fila


def test_la_tabla_lleva_cabecera(solution):
    tabla = solution.render_table(FILAS)

    assert tabla.splitlines()[0] == "producto     cant       importe"


def test_la_tabla_lleva_separador(solution):
    tabla = solution.render_table(FILAS)

    assert tabla.splitlines()[1] == "-" * 31


def test_la_tabla_trae_todas_las_filas(solution):
    tabla = solution.render_table(FILAS)

    assert len(tabla.splitlines()) == 4


def test_la_tabla_no_termina_en_salto_de_linea(solution):
    assert not solution.render_table(FILAS).endswith("\n")


def test_una_tabla_sin_filas_conserva_cabecera_y_separador(solution):
    tabla = solution.render_table([])

    assert len(tabla.splitlines()) == 2


def test_la_tabla_completa(solution):
    assert solution.render_table(FILAS) == (
        "producto     cant       importe\n"
        "-------------------------------\n"
        "café            3      1,500.00\n"
        "azúcar         12          0.99"
    )
