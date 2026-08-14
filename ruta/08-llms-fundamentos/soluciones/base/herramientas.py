"""Solución de referencia del ejercicio `herramientas`.

`inspect.signature` da los parámetros con sus anotaciones y sus valores por
defecto. Como el esquema se deriva de la firma, no puede quedarse desfasado
cuando alguien cambie la función.
"""

import inspect

JSON_TYPES = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def tool_schema(func) -> dict:
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func) or ""

    properties = {}
    required = []

    for name, parameter in signature.parameters.items():
        properties[name] = {"type": JSON_TYPES.get(parameter.annotation, "string")}
        if parameter.default is inspect.Parameter.empty:
            required.append(name)

    return {
        "name": func.__name__,
        "description": docstring.splitlines()[0].strip() if docstring else "",
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }
