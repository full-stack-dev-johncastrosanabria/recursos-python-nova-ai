import pytest


def test_lee_pares_clave_valor(solution):
    assert solution.parse_env("HOST=db.internal\nPORT=5432") == {
        "HOST": "db.internal",
        "PORT": "5432",
    }


def test_ignora_lineas_vacias_y_comentarios(solution):
    texto = """
    # esto es un comentario
    HOST=db.internal

       # y este también
    PORT=5432
    """

    assert solution.parse_env(texto) == {"HOST": "db.internal", "PORT": "5432"}


def test_quita_espacios_alrededor(solution):
    assert solution.parse_env("  HOST  =  db.internal  ") == {"HOST": "db.internal"}


def test_quita_las_comillas_del_valor(solution):
    assert solution.parse_env('SALUDO="hola mundo"') == {"SALUDO": "hola mundo"}
    assert solution.parse_env("SALUDO='hola mundo'") == {"SALUDO": "hola mundo"}


def test_el_valor_puede_contener_igual(solution):
    """Se parte por el primer =, no por todos."""
    assert solution.parse_env("URL=postgres://user:pa=ss@host/db") == {
        "URL": "postgres://user:pa=ss@host/db"
    }


def test_la_ultima_clave_repetida_gana(solution):
    assert solution.parse_env("PORT=1\nPORT=2") == {"PORT": "2"}


def test_un_valor_vacio_es_valido(solution):
    assert solution.parse_env("ANTHROPIC_API_KEY=") == {"ANTHROPIC_API_KEY": ""}


def test_texto_vacio_da_diccionario_vacio(solution):
    assert solution.parse_env("") == {}


def test_una_linea_sin_igual_es_un_error(solution):
    with pytest.raises(ValueError):
        solution.parse_env("HOST=ok\nesto no tiene igual")


def test_el_error_dice_en_que_linea(solution):
    with pytest.raises(ValueError) as error:
        solution.parse_env("HOST=ok\n\nroto")

    assert "3" in str(error.value)
