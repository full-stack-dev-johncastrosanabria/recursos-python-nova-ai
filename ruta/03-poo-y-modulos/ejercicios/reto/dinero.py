"""Reto: que tu tipo hable los protocolos del lenguaje.

Implementa `Money` con cuatro métodos especiales, de forma que estas cosas
funcionen sin escribir ni un helper:

    Money(1000) == Money(1000)                 -> True
    Money(500) < Money(1000)                   -> True
    sorted([Money(300), Money(100)])           -> [Money(100), Money(300)]
    Money(500) + Money(300)                    -> Money(800)
    repr(Money(1000))                          -> "Money(1000, 'CRC')"

Reglas de las divisas: comparar o sumar importes de divisas distintas no es
"False", es una operación sin sentido. En esos casos, tus dunder deben devolver
`NotImplemented` (la constante, **no** lanzar `NotImplementedError`), que es la
forma que tiene Python de decir "yo no sé con eso". El lenguaje se encarga
entonces de preguntarle al otro operando y, si tampoco sabe, de lanzar un
`TypeError` con un mensaje claro.

Consecuencias que los tests comprueban:

    Money(100, "CRC") == Money(100, "USD")     -> False
    Money(100, "CRC") == "hola"                -> False
    Money(100, "CRC") < Money(100, "USD")      -> TypeError
    Money(100, "CRC") + Money(100, "USD")      -> TypeError

Fíjate en la asimetría: `==` con algo incomparable da `False` (Python
convierte el NotImplemented en eso), pero `<` y `+` levantan `TypeError`. No
tienes que programar esa diferencia: sale sola de devolver `NotImplemented`.
"""


class Money:
    def __init__(self, cents: int, currency: str = "CRC") -> None:
        raise NotImplementedError("Borra esta línea y escribe tu solución")
