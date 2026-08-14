"""Ejercicio: elegir qué agente hace cada tarea.

Cada agente tiene un rol y un conjunto de herramientas. Cada tarea declara qué
herramientas necesita. Escribe `assign`, que elige el agente adecuado.

    agents = [
        {"role": "analista", "tools": {"sql", "buscar", "graficar"}},
        {"role": "consultor", "tools": {"buscar"}},
    ]
    task = {"name": "investigar", "needs": {"buscar"}}

    assign(agents, task)   -> el consultor

Reglas, y la segunda es la interesante:

1. Sirve cualquier agente cuyas herramientas **contengan** todas las que la
   tarea necesita.
2. Entre los que sirven, gana el que **menos herramientas** tenga. No es un
   capricho: un agente con demasiadas herramientas elige peor. Prefiere siempre
   al más especializado que cumpla.
3. Si empatan en número de herramientas, gana el que aparezca antes en la lista.
4. Si ninguno sirve, lanza `NoSuitableAgent` diciendo qué herramientas faltan.
5. Una tarea que no necesita nada (`needs` vacío) la puede hacer cualquiera:
   gana el más especializado, por la regla 2.

La regla 1 es una comparación de conjuntos del módulo 02. Si te sale un bucle
comprobando herramienta por herramienta, hay un operador que hace eso.
"""


class NoSuitableAgent(Exception):
    """Ningún agente tiene las herramientas que la tarea necesita."""


def assign(agents: list[dict], task: dict) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
