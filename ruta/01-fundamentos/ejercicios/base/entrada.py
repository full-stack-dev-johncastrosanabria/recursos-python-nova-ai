"""Ejercicio: convertir lo que escribe un usuario.

`input()` devuelve siempre texto. Convertirlo a lo que tu programa necesita —y
tratar los casos en los que no se puede— es trabajo tuyo.

Escribe `parse_amount`, que toma lo que escribió el usuario y devuelve el
importe **en céntimos, como entero**:

    parse_amount("1500")        -> 150000
    parse_amount("1500.50")     -> 150050
    parse_amount(" 1,500.50 ")  -> 150050
    parse_amount("0.99")        -> 99
    parse_amount("0")           -> 0

Reglas de aceptación:

- Se ignoran los espacios de los extremos.
- Se ignoran las comas: son separadores de miles.
- La parte decimal es opcional y admite **como mucho dos cifras**. `"1500.5"`
  son 150050 céntimos, no 15005.

Y los errores, que son la mitad del ejercicio. Todos son `ValueError`, y el
mensaje debe **incluir el valor recibido**, porque quien lea el log no lo tiene
delante:

- Texto vacío o solo espacios.
- Algo que no es un número: `"hola"`, `"12ab"`.
- Un importe negativo: aquí no tienen sentido.
- Más de dos decimales: `"10.999"` no es una cantidad de dinero válida, y
  redondearla en silencio sería peor que rechazarla.

Pista: `str.strip`, `str.replace`, y separar por el punto con `str.partition`.
Y recuerda que `int("hola")` lanza `ValueError` por su cuenta: puedes dejar que
lo haga y capturarlo, o comprobarlo antes. Las dos vías son válidas; el módulo
00 llamaba a eso EAFP y LBYL.
"""


def parse_amount(raw: str) -> int:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
