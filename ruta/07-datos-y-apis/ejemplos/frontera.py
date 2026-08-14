"""Qué pasa cuando la frontera no valida.

Córrelo con:
    uv run python ruta/07-datos-y-apis/ejemplos/frontera.py
"""

# El proveedor cambió un campo y ahora manda `ref` en vez de `reference`.
PAYLOAD = {
    "id": "TR-1",
    "amount": {"cents": 150_000},
    "parties": {"from": {"account": "CR01-0001"}, "to": {"account": "CR01-0002"}},
    "ref": "factura 42",
}


# ── Sin validar: todo .get() y a seguir ───────────────────────────
def normalizar_permisivo(payload: dict) -> dict:
    return {
        "id": payload.get("id"),
        "amount_cents": payload.get("amount", {}).get("cents"),
        "origin": payload.get("parties", {}).get("from", {}).get("account"),
        "reference": payload.get("reference"),  # ← el campo ya no se llama así
    }


registro = normalizar_permisivo(PAYLOAD)
print("Permisivo :", registro)
print("           el sistema sigue funcionando y la referencia se perdió.")
print("           Nadie verá un error hasta que alguien cuadre el informe.\n")


# ── Validando: lo obligatorio que falta revienta aquí ─────────────
def requerido(payload: dict, *ruta: str):
    actual = payload
    for indice, clave in enumerate(ruta):
        if not isinstance(actual, dict) or clave not in actual:
            raise ValueError(
                f"falta el campo obligatorio {'.'.join(ruta[: indice + 1])}"
            )
        actual = actual[clave]
    return actual


def normalizar_estricto(payload: dict) -> dict:
    return {
        "id": requerido(payload, "id"),
        "amount_cents": requerido(payload, "amount", "cents"),
        "origin": requerido(payload, "parties", "from", "account"),
        "reference": requerido(payload, "reference"),
    }


try:
    normalizar_estricto(PAYLOAD)
except ValueError as error:
    print("Estricto  : ValueError ->", error)
    print("           El fallo aparece en la puerta, con el nombre del campo,")
    print("           el día del despliegue y no tres meses después.\n")

# Lo opcional de verdad sí puede faltar, y eso no es un fallo.
print("La regla no es 'validar todo': es distinguir lo que puede faltar")
print("de lo que no. `reference` opcional -> None. `id` ausente -> error.")
