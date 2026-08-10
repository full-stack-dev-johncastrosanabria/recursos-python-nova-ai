"""Los tipos básicos de Python, en un archivo que puedes ejecutar.

Córrelo con:
    uv run python ruta/01-fundamentos/ejemplos/variables_y_tipos.py
"""

# Python deduce el tipo, pero anotarlo hace el código más claro.
name: str = "Ana"
age: int = 30
height: float = 1.62
is_active: bool = True

# f-strings: la forma normal de construir texto con valores dentro.
print(f"{name} tiene {age} años y mide {height} m")

# type() te dice el tipo de cualquier valor. Útil cuando algo no cuadra.
for value in (name, age, height, is_active):
    print(f"{value!r:>10} -> {type(value).__name__}")

# Las listas guardan varios valores en orden.
languages: list[str] = ["Python", "SQL", "Bash"]
print(f"Primero: {languages[0]} · Último: {languages[-1]}")

# Los dicts asocian claves con valores.
person: dict[str, str] = {"nombre": "Ana", "rol": "backend"}
print(f"{person['nombre']} trabaja en {person['rol']}")
