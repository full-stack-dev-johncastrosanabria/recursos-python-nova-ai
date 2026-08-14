'''Ejercicio: generar el esquema de una herramienta desde la función.

Para que un modelo pueda usar tu función como herramienta, hay que describirle
su nombre, para qué sirve y qué argumentos recibe. Escribir ese diccionario a
mano por cada función es tedioso y se desincroniza en cuanto cambias la firma.

Escribe `tool_schema`, que lo genera leyendo la propia función:

    def get_balance(account: str, include_pending: bool = False) -> int:
        """Devuelve el saldo en céntimos de una cuenta.

        Detalles que no van en la descripción.
        """

    tool_schema(get_balance)
    -> {
        "name": "get_balance",
        "description": "Devuelve el saldo en céntimos de una cuenta.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account": {"type": "string"},
                "include_pending": {"type": "boolean"},
            },
            "required": ["account"],
        },
    }

Reglas:

- El nombre sale de `__name__`.
- La descripción es la **primera línea** del docstring, sin espacios sobrantes.
  Si no hay docstring, cadena vacía.
- Cada parámetro entra en `properties` con su tipo traducido según `JSON_TYPES`.
  Un tipo que no esté en el mapa se anota como `"string"`.
- Solo son `required` los parámetros **sin valor por defecto**, en el orden de
  la firma.
- El valor de retorno no aparece: al modelo no le hace falta.

Esto es el módulo 00 (todo es un objeto y se puede inspeccionar) y el 04 (las
anotaciones son datos legibles) cobrados a la vez. Mira `inspect.signature`.
'''

JSON_TYPES = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def tool_schema(func) -> dict:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
