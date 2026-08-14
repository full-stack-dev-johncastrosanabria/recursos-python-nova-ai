"""Cuando el problema se deja escribir como conjuntos, desaparece el código.

Córrelo con:
    uv run python ruta/02-estructuras-de-datos/ejemplos/conjuntos.py
"""

movimientos_banco = [
    {"ref": "TR-001", "monto": 15_000},
    {"ref": "TR-002", "monto": 4_500},
    {"ref": "TR-003", "monto": 92_300},
    {"ref": "TR-005", "monto": 1_200},
]

registros_internos = [
    {"ref": "TR-002", "monto": 4_500},
    {"ref": "TR-003", "monto": 92_300},
    {"ref": "TR-004", "monto": 8_000},
]

refs_banco = {m["ref"] for m in movimientos_banco}
refs_internas = {r["ref"] for r in registros_internos}

print("Referencias del banco :", sorted(refs_banco))
print("Referencias internas  :", sorted(refs_internas))

print("\n── El informe completo, en tres operaciones ──")
print("Cuadran            :", sorted(refs_banco & refs_internas))
print("Solo en el banco   :", sorted(refs_banco - refs_internas))
print("Solo en lo interno :", sorted(refs_internas - refs_banco))
print("En un lado u otro  :", sorted(refs_banco ^ refs_internas))

# Más álgebra que sustituye bucles enteros.
campos_requeridos = {"ref", "monto", "fecha"}
payload = {"ref": "TR-010", "monto": 500}

print("\n── Validación sin bucles ──")
print("¿Están todos los campos?", campos_requeridos <= set(payload))
print("Faltan:", sorted(campos_requeridos - set(payload)))

permisos_usuario = {"leer", "escribir"}
permisos_necesarios = {"leer"}
print("\n¿Autorizado?", permisos_usuario >= permisos_necesarios)

# Deduplicar conservando el orden de aparición: dict recuerda inserción.
con_repetidos = ["b", "a", "c", "a", "b", "d"]
print("\nSin duplicados, sin orden :", set(con_repetidos))
print("Sin duplicados, con orden :", list(dict.fromkeys(con_repetidos)))
