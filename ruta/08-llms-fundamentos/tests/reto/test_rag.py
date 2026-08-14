import pytest


def test_trocea_con_solapamiento(solution):
    assert solution.chunk_text("abcdefghij", size=4, overlap=1) == [
        "abcd",
        "defg",
        "ghij",
        "j",
    ]


def test_sin_solapamiento_es_un_corte_limpio(solution):
    assert solution.chunk_text("abcdefgh", size=4, overlap=0) == ["abcd", "efgh"]


def test_el_solapamiento_repite_el_final_del_anterior(solution):
    trozos = solution.chunk_text("abcdefgh", size=4, overlap=2)

    assert trozos[0][-2:] == trozos[1][:2]


def test_el_ultimo_trozo_puede_ser_mas_corto(solution):
    trozos = solution.chunk_text("abcde", size=4, overlap=0)

    assert trozos == ["abcd", "e"]


def test_texto_vacio(solution):
    assert solution.chunk_text("", size=4, overlap=1) == []


def test_texto_mas_corto_que_el_trozo(solution):
    assert solution.chunk_text("ab", size=10, overlap=2) == ["ab"]


def test_todo_el_texto_aparece_en_algun_trozo(solution):
    texto = "la conciliación cuadra cuando ambas partes coinciden"

    trozos = solution.chunk_text(texto, size=10, overlap=3)

    assert texto.startswith(trozos[0])
    assert texto.endswith(trozos[-1])


@pytest.mark.parametrize("size", [0, -1])
def test_un_tamano_invalido_es_un_error(solution, size):
    with pytest.raises(ValueError):
        solution.chunk_text("abc", size=size)


def test_un_solapamiento_negativo_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.chunk_text("abc", size=4, overlap=-1)


@pytest.mark.parametrize("overlap", [4, 5, 10])
def test_un_solapamiento_que_no_avanza_es_un_error(solution, overlap):
    """Sin esta validación, la función se quedaría troceando para siempre."""
    with pytest.raises(ValueError):
        solution.chunk_text("abcdefgh", size=4, overlap=overlap)
