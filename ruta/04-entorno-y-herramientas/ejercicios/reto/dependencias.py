"""Reto: en qué orden se instalan las dependencias.

Antes de instalar nada, un gestor de paquetes tiene que decidir el orden: no
puedes instalar algo antes que aquello de lo que depende. Eso es un
**ordenamiento topológico**, y lo vas a escribir.

    install_order({
        "app": ["httpx", "pydantic"],
        "httpx": ["certifi"],
        "pydantic": [],
        "certifi": [],
    })
    -> ["certifi", "httpx", "pydantic", "app"]

Ese orden sale de aplicar la regla de desempate paso a paso: al principio solo
`certifi` y `pydantic` están listos, y gana `certifi` por orden alfabético; en
cuanto sale, `httpx` queda listo y vuelve a haber empate, que ahora gana `httpx`.

Reglas:

- Cada paquete aparece **después** de todas sus dependencias.
- Cuando varios paquetes están listos a la vez, se eligen en **orden
  alfabético**. Sin esa regla habría muchas respuestas válidas y el resultado no
  sería reproducible — y un instalador que da órdenes distintas en cada
  ejecución es un instalador que no se puede depurar.
- Un paquete que aparece como dependencia pero no como clave se trata como si
  no tuviera dependencias propias.
- Un **ciclo** es un error: lanza `CircularDependency` con los nombres de los
  paquetes implicados, ordenados alfabéticamente y separados por comas. Un ciclo
  de dependencias no se puede instalar en ningún orden, igual que el ciclo de
  imports del módulo 03 no se puede resolver sin romperlo.
- Un grafo vacío devuelve una lista vacía.

El algoritmo clásico es el de Kahn: cuentas cuántas dependencias pendientes
tiene cada paquete, vas sacando los que tienen cero, y cada vez que sacas uno
descuentas a los que dependían de él. Si al final queda alguno sin salir, es
que había un ciclo.
"""


class CircularDependency(Exception):
    """Hay un ciclo: no existe ningún orden de instalación válido."""


def install_order(dependencies: dict[str, list[str]]) -> list[str]:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
