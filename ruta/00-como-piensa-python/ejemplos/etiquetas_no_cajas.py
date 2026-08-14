"""El modelo de etiquetas, comprobado con `id()`.

Córrelo con:
    uv run python ruta/00-como-piensa-python/ejemplos/etiquetas_no_cajas.py
"""

# `id()` devuelve la identidad del objeto. Si dos nombres dan el mismo id,
# no hay dos objetos: hay uno con dos etiquetas.
a = [1, 2, 3]
b = a
c = a[:]  # esto sí crea un objeto nuevo

print(f"a -> id {id(a)}")
print(f"b -> id {id(b)}   ¿mismo objeto que a? {a is b}")
print(f"c -> id {id(c)}   ¿mismo objeto que a? {a is c}")

b.append(4)
print(f"\ntras b.append(4):  a={a}  b={b}  c={c}")
print("a cambió porque b nunca fue una copia, era otra etiqueta.")

# `==` compara valor, `is` compara identidad. No son lo mismo.
print(f"\na == c -> {a == c}   (mismo contenido, no)")
print(f"a is c -> {a is c}   (mismo objeto)")


# La distinción se vuelve crítica con los argumentos por defecto.
# El `noqa` de abajo silencia a ruff a propósito: el bug está aquí para verlo.
# En código de verdad, ruff te avisa de esto antes de que llegue a producción.
def add_broken(item, basket=[]):  # noqa: B006
    """No hagas esto: la lista por defecto se crea una vez, al definir."""
    basket.append(item)
    return basket


print(f"\nadd_broken('pan')   -> {add_broken('pan')}")
print(f"add_broken('leche') -> {add_broken('leche')}  ← arrastra la anterior")

# El objeto por defecto vive en la propia función, y se puede inspeccionar:
print(f"\nvalor por defecto guardado: {add_broken.__defaults__}")
print("Todo es un objeto, incluso los valores por defecto de una función.")
