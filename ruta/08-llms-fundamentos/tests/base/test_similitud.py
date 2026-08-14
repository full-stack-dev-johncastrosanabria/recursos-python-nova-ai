import pytest


def test_vectores_identicos(solution):
    assert solution.cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)


def test_vectores_perpendiculares(solution):
    assert solution.cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


def test_vectores_opuestos(solution):
    assert solution.cosine_similarity([1, 0], [-1, 0]) == pytest.approx(-1.0)


def test_no_depende_de_la_magnitud(solution):
    """Mide dirección: un texto largo y uno corto del mismo tema se alinean."""
    assert solution.cosine_similarity([1, 1], [10, 10]) == pytest.approx(1.0)


def test_con_mas_dimensiones(solution):
    a = [1, 2, 3]
    b = [2, 4, 6]

    assert solution.cosine_similarity(a, b) == pytest.approx(1.0)


def test_un_vector_de_ceros_da_cero(solution):
    """El coseno no está definido, pero dividir entre cero es peor."""
    assert solution.cosine_similarity([0, 0], [1, 1]) == 0.0


def test_vectores_de_distinta_longitud(solution):
    with pytest.raises(ValueError):
        solution.cosine_similarity([1, 2], [1, 2, 3])


def test_vectores_vacios(solution):
    with pytest.raises(ValueError):
        solution.cosine_similarity([], [])


def test_top_k_ordena_de_mayor_a_menor(solution):
    resultado = solution.top_k([1, 0], {"a": [0.9, 0.1], "b": [0, 1], "c": [1, 0]}, k=3)

    assert [nombre for nombre, _ in resultado] == ["c", "a", "b"]


def test_top_k_recorta(solution):
    resultado = solution.top_k([1, 0], {"a": [0.9, 0.1], "b": [0, 1], "c": [1, 0]}, k=2)

    assert len(resultado) == 2


def test_top_k_devuelve_las_similitudes(solution):
    resultado = solution.top_k([1, 0], {"c": [1, 0]}, k=1)

    assert resultado[0][1] == pytest.approx(1.0)


def test_top_k_desempata_alfabeticamente(solution):
    """Sin esta regla el resultado no sería reproducible."""
    resultado = solution.top_k([1, 0], {"zeta": [1, 0], "alfa": [1, 0]}, k=1)

    assert resultado[0][0] == "alfa"


def test_top_k_con_menos_vectores_que_k(solution):
    resultado = solution.top_k([1, 0], {"a": [1, 0]}, k=10)

    assert len(resultado) == 1


def test_top_k_sin_vectores(solution):
    assert solution.top_k([1, 0], {}, k=3) == []


@pytest.mark.parametrize("k", [0, -1])
def test_un_k_invalido_es_un_error(solution, k):
    with pytest.raises(ValueError):
        solution.top_k([1, 0], {"a": [1, 0]}, k=k)


def test_una_busqueda_semantica_de_juguete(solution):
    documentos = {
        "rechazo": [0.9, 0.1, 0.0],
        "receta": [0.0, 0.1, 0.9],
        "pago_fallido": [0.85, 0.15, 0.05],
    }

    resultado = solution.top_k([1.0, 0.0, 0.0], documentos, k=2)

    assert {nombre for nombre, _ in resultado} == {"rechazo", "pago_fallido"}
