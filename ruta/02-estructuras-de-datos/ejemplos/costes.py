"""La diferencia entre O(1) y O(n), medida en tu propia máquina.

Córrelo con:
    uv run python ruta/02-estructuras-de-datos/ejemplos/costes.py
"""

from collections import deque
from time import perf_counter


def vaciar_lista_por_el_principio(cantidad: int) -> float:
    cola = list(range(cantidad))
    inicio = perf_counter()
    while cola:
        cola.pop(0)  # O(n): desplaza todo el array una posición
    return perf_counter() - inicio


def vaciar_deque_por_el_principio(cantidad: int) -> float:
    cola = deque(range(cantidad))
    inicio = perf_counter()
    while cola:
        cola.popleft()  # O(1): barata por ambos extremos
    return perf_counter() - inicio


print(f"{'elementos':>10} {'list.pop(0)':>14} {'deque.popleft()':>17} {'ratio':>8}")
print("-" * 52)

for cantidad in (10_000, 20_000, 40_000, 80_000):
    con_lista = vaciar_lista_por_el_principio(cantidad)
    con_deque = vaciar_deque_por_el_principio(cantidad)
    ratio = con_lista / con_deque if con_deque else 0
    print(f"{cantidad:>10,} {con_lista:>13.4f}s {con_deque:>16.4f}s {ratio:>7.0f}×")

print(
    "\nAl doblar los elementos, la lista cuadruplica su tiempo: eso es O(n²).\n"
    "El deque lo dobla: eso es O(n). La curva es la que te tumba el servicio,\n"
    "no la constante."
)

# Lo mismo con la pertenencia: buscar en una lista recorre; en un set, no.
elementos = list(range(200_000))
como_lista = elementos
como_conjunto = set(elementos)
objetivo = 199_999

inicio = perf_counter()
encontrado_en_lista = objetivo in como_lista
en_lista = perf_counter() - inicio

inicio = perf_counter()
encontrado_en_conjunto = objetivo in como_conjunto
en_conjunto = perf_counter() - inicio

assert encontrado_en_lista == encontrado_en_conjunto

print("\nBuscar un elemento al final de 200.000:")
print(f"  x in lista  -> {en_lista * 1_000:.3f} ms   (recorre hasta encontrarlo)")
print(f"  x in set    -> {en_conjunto * 1_000:.3f} ms   (calcula el hash y salta)")
