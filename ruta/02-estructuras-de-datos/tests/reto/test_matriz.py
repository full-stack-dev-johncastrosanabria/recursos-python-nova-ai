import pytest


def test_make_matrix_tiene_la_forma_pedida(solution):
    matriz = solution.make_matrix(2, 3)

    assert matriz == [[0, 0, 0], [0, 0, 0]]
    assert len(matriz) == 2
    assert len(matriz[0]) == 3


def test_make_matrix_admite_otro_valor(solution):
    assert solution.make_matrix(2, 2, value=7) == [[7, 7], [7, 7]]


def test_las_filas_son_independientes(solution):
    """La trampa de [[0] * 3] * 2: las dos filas serían el mismo objeto."""
    matriz = solution.make_matrix(2, 3)

    matriz[0][0] = 9

    assert matriz[1][0] == 0, "modificar una fila no debe afectar a la otra"
    assert matriz[0] is not matriz[1]


def test_una_matriz_de_una_celda(solution):
    assert solution.make_matrix(1, 1) == [[0]]


@pytest.mark.parametrize(("filas", "columnas"), [(0, 3), (3, 0), (-1, 2)])
def test_dimensiones_invalidas_son_un_error(solution, filas, columnas):
    with pytest.raises(ValueError):
        solution.make_matrix(filas, columnas)


def test_transpose(solution):
    assert solution.transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]


def test_transpose_de_una_matriz_cuadrada(solution):
    assert solution.transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]


def test_transpose_dos_veces_devuelve_el_original(solution):
    matriz = [[1, 2, 3], [4, 5, 6]]

    assert solution.transpose(solution.transpose(matriz)) == matriz


def test_transpose_no_modifica_la_matriz(solution):
    matriz = [[1, 2], [3, 4]]

    solution.transpose(matriz)

    assert matriz == [[1, 2], [3, 4]]


def test_transpose_devuelve_listas_no_tuplas(solution):
    resultado = solution.transpose([[1, 2], [3, 4]])

    assert all(isinstance(fila, list) for fila in resultado)


def test_transpose_de_una_matriz_vacia(solution):
    assert solution.transpose([]) == []


def test_row_sums(solution):
    assert solution.row_sums([[1, 2, 3], [4, 5, 6]]) == [6, 15]


def test_row_sums_con_negativos(solution):
    assert solution.row_sums([[1, -1], [-5, 5]]) == [0, 0]


def test_row_sums_de_una_matriz_vacia(solution):
    assert solution.row_sums([]) == []
