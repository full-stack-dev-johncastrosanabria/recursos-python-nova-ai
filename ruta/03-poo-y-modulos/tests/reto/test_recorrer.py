ARBOL = {
    "name": "raiz",
    "children": [
        {"name": "notas.txt", "size": 100},
        {
            "name": "fotos",
            "children": [
                {"name": "a.jpg", "size": 400},
                {"name": "b.jpg", "size": 250},
            ],
        },
    ],
}

SOLO_ARCHIVO = {"name": "solo.txt", "size": 42}
CARPETA_VACIA = {"name": "vacia", "children": []}

PROFUNDO = {
    "name": "n0",
    "children": [
        {
            "name": "n1",
            "children": [{"name": "n2", "children": [{"name": "hoja.txt", "size": 1}]}],
        }
    ],
}


def test_total_size(solution):
    assert solution.total_size(ARBOL) == 750


def test_total_size_de_un_solo_archivo(solution):
    assert solution.total_size(SOLO_ARCHIVO) == 42


def test_total_size_de_una_carpeta_vacia(solution):
    assert solution.total_size(CARPETA_VACIA) == 0


def test_total_size_baja_todos_los_niveles(solution):
    assert solution.total_size(PROFUNDO) == 1


def test_count_files(solution):
    assert solution.count_files(ARBOL) == 3


def test_count_files_no_cuenta_las_carpetas(solution):
    assert solution.count_files(CARPETA_VACIA) == 0


def test_count_files_de_un_solo_archivo(solution):
    assert solution.count_files(SOLO_ARCHIVO) == 1


def test_max_depth(solution):
    assert solution.max_depth(ARBOL) == 2


def test_max_depth_de_un_archivo_suelto_es_cero(solution):
    assert solution.max_depth(SOLO_ARCHIVO) == 0


def test_max_depth_de_una_carpeta_vacia_es_cero(solution):
    assert solution.max_depth(CARPETA_VACIA) == 0


def test_max_depth_en_un_arbol_profundo(solution):
    assert solution.max_depth(PROFUNDO) == 3


def test_no_modifica_el_arbol(solution):
    import copy

    copia = copy.deepcopy(ARBOL)

    solution.total_size(ARBOL)
    solution.count_files(ARBOL)
    solution.max_depth(ARBOL)

    assert ARBOL == copia
