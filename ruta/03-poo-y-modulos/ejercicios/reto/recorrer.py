"""Reto: recursión sobre una estructura anidada.

Un árbol de carpetas y archivos, representado con diccionarios:

    arbol = {
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

Un nodo es un **archivo** si tiene la clave `"size"`, y una **carpeta** si tiene
`"children"`. Escribe tres funciones:

    total_size(arbol)     -> 750    suma el tamaño de todos los archivos
    count_files(arbol)    -> 3      cuántos archivos hay (las carpetas no cuentan)
    max_depth(arbol)      -> 2      cuántos niveles de anidamiento hay

Sobre `max_depth`: la raíz está en el nivel 0, sus hijos directos en el 1, y así.
Un árbol que es un único archivo tiene profundidad 0. Una carpeta vacía también,
porque no hay nada dentro que baje un nivel.

Reglas:

- Una carpeta puede estar vacía (`"children": []`).
- Las carpetas pueden anidarse sin límite práctico.
- No modifiques el árbol.

Por qué recursión y no un bucle: **la forma del problema es recursiva**. Una
carpeta contiene cosas que pueden ser carpetas que contienen cosas. Con un bucle
tendrías que llevar tú una pila de nodos pendientes; con recursión, esa pila la
gestiona el lenguaje. Ese es el criterio para elegirla — no es que sea más
elegante, es que el dato ya tiene esa estructura.
"""


def total_size(node: dict) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def count_files(node: dict) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")


def max_depth(node: dict) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
