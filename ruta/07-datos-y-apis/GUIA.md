# Módulo 07 · Datos y APIs

> **Prerrequisitos:** módulos 01-06
> **Tiempo estimado:** 150 min
> **Si ya dominas esto:** salta al módulo 08

Este es el módulo de las fronteras: donde tu programa habla con el mundo. Datos
que llegan de fuera y no te puedes fiar, servicios que responden tarde o mal,
tablas que hay que explorar antes de decidir nada.

Casi todos los bugs caros de un sistema viven aquí, no en la lógica de negocio.

## Qué vas a poder hacer al terminar

- Validar datos con pydantic
- Consumir APIs con httpx
- Exponer un endpoint con FastAPI
- Explorar datos tabulares con pandas

## 1. La frontera: validar en la puerta

Dentro de tu sistema puedes confiar en el duck typing. En la puerta, no. Un
payload que llega con la forma equivocada debe rechazarse **ahí**, con un
mensaje claro, en vez de propagarse tres capas y estallar como un
`AttributeError` incomprensible.

En el módulo 04 escribiste esa validación a mano. Pydantic la declara:

```python
from pydantic import BaseModel, Field, field_validator

class Transfer(BaseModel):
    origin: str = Field(min_length=5)
    destination: str
    amount_cents: int = Field(gt=0)
    currency: str = "CRC"

    @field_validator("destination")
    @classmethod
    def distinta_del_origen(cls, value: str, info):
        if value == info.data.get("origin"):
            raise ValueError("origen y destino coinciden")
        return value

t = Transfer.model_validate({"origin": "CR01-0001", "destination": "CR01-0002",
                             "amount_cents": "150000"})
t.amount_cents   # 150000, ya como int: convirtió el string
```

Tres cosas que lo hacen distinto de escribirlo a mano:

- **Convierte además de validar.** El `"150000"` que llegó como texto sale
  como `int`. Es el salto del módulo 04, hecho por ti.
- **Informa de todos los errores a la vez**, no del primero. Quien manda el
  payload lo arregla de una vez.
- **Usa las anotaciones de tipo** que ya sabes escribir. Es una de las dos
  excepciones a "el intérprete no lee las anotaciones": Pydantic sí las lee, en
  tiempo de ejecución.

La regla: **valida en la frontera, confía dentro**. Un modelo Pydantic en el
borde y dataclasses normales en el núcleo es una arquitectura, no una
preferencia.

## 2. Hablar con APIs: httpx

```python
import httpx

with httpx.Client(timeout=10.0) as client:
    respuesta = client.get("https://api.ejemplo.com/transfers")
    respuesta.raise_for_status()
    datos = respuesta.json()
```

Tres decisiones que no son opcionales en producción:

**Timeout siempre.** Sin él, una petición puede colgarse indefinidamente y
llevarse por delante el worker. `httpx` obliga a pensarlo; muchas librerías no.

**`raise_for_status()`.** Un 500 no lanza excepción por sí solo: te devuelve un
objeto respuesta con `status_code=500`. Si no lo compruebas, `respuesta.json()`
te dará basura o reventará lejos del origen.

**Reutiliza el cliente.** Crear un `Client` por petición tira a la basura el
pool de conexiones. Uno por proceso, o inyectado.

Y en async, lo del módulo 06 aplica igual:

```python
async with httpx.AsyncClient(timeout=10.0) as client:
    respuestas = await asyncio.gather(*(client.get(u) for u in urls))
```

### Paginación y reintentos

Dos patrones que vas a escribir en cada integración:

```python
def all_pages(client, url):
    """Va soltando los elementos de todas las páginas, sin cargarlas todas."""
    page = 1
    while True:
        datos = client.get(url, params={"page": page}).json()
        yield from datos["items"]
        if not datos["has_more"]:
            return
        page += 1
```

Fíjate en que es un generador: quien lo consume puede parar a la mitad y no se
habrán pedido las páginas restantes. Es el modelo mental 4 otra vez.

Y los reintentos con espera creciente, porque un 503 casi siempre es temporal:

```python
delays = [base * 2**n for n in range(attempts)]   # 1, 2, 4, 8…
```

Los dos son tus ejercicios.

## 3. Exponer una API: FastAPI

FastAPI no es un framework nuevo que aprender: es la composición de lo que ya
sabes. Anotaciones de tipo para declarar la entrada, Pydantic para validarla,
`async` para atender concurrentemente.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/transfers", status_code=201)
async def create_transfer(transfer: Transfer) -> dict:
    if not account_exists(transfer.origin):
        raise HTTPException(status_code=404, detail="la cuenta de origen no existe")
    return {"id": save(transfer)}
```

Esa anotación `transfer: Transfer` hace cuatro cosas a la vez: parsea el JSON,
lo valida, devuelve un 422 con el detalle si no cuadra, y documenta el endpoint
en el OpenAPI que FastAPI genera solo. Cuatro cosas que en otros frameworks son
cuatro trozos de código que se desincronizan.

```bash
uv run uvicorn app:app --reload    # y la documentación viva en /docs
```

## 4. Datos tabulares: pandas y el criterio

```python
import pandas as pd

df = pd.read_csv("movimientos.csv", parse_dates=["fecha"])
df.head()
df.info()                                     # tipos y nulos: mira esto SIEMPRE primero
df.groupby("divisa")["monto"].sum()
df[df["monto"] > 100_000].sort_values("fecha")
```

Dos avisos que ahorran disgustos:

**Mira los tipos antes de calcular.** Una columna de montos que se leyó como
texto porque una fila traía `"N/A"` produce sumas silenciosamente absurdas.
`df.info()` lo enseña en un segundo.

**El dinero, otra vez, no en float.** Si vas a sumar importes, trabaja en
enteros de la unidad mínima o usa `Decimal`.

Y el criterio de cuándo usar qué: pandas para explorar y para volúmenes que
caben en memoria; Polars o DuckDB cuando no caben o cuando el rendimiento
importa; SQL cuando los datos ya están en una base de datos — traerse un millón
de filas a Python para filtrarlas es casi siempre un error de diseño.

## 5. Por qué los ejercicios no importan nada de esto

Los tests de este módulo usan solo la biblioteca estándar. No es pereza, es la
lección del módulo 05 aplicada: **un test que necesita red no es un test
unitario, es una fuente de fallos intermitentes**.

Las tres piezas que vas a escribir —paginación, normalización y reintentos— son
exactamente la lógica que rodea a `httpx`, extraída de forma que se pueda probar
sin tocar la red. Que se puedan probar así no es casualidad: es lo que pasa
cuando separas el cálculo del efecto.

Si quieres ver el módulo con las librerías de verdad instaladas:

```bash
uv sync --group ia
```

## Caso real

Una integración con un proveedor de pagos funcionó seis meses y un lunes empezó
a perder transferencias. No fallaba: perdía. El informe diario cuadraba menos de
lo que debía y nadie veía errores en los logs.

Tres causas, las tres en la frontera:

1. **La paginación asumía dos páginas.** El código pedía `page=1` y `page=2` y
   paraba. Funcionó hasta que el volumen creció y hubo una tercera. No hubo
   error: simplemente dejaron de existir las transferencias de la tercera
   página.
2. **`raise_for_status()` no estaba.** Cuando el proveedor devolvía 503, el
   código hacía `.json()` sobre una página de error HTML, capturaba la
   excepción de parseo y seguía con una lista vacía.
3. **Un campo opcional cambió de nombre.** El código usaba `.get("reference")`,
   que empezó a devolver `None`, y esos `None` se filtraban más adelante sin
   avisar.

Las tres son el mismo error de fondo: **tratar la ausencia como si fuera un
caso normal cuando era un fallo**. Es la tríada de lectura del módulo 02 y el
`errors should never pass silently` del módulo 00, cobrados con intereses.

## Ejercicios

```bash
uv run pytest ruta/07-datos-y-apis
```

- **`ejercicios/base/paginacion.py`** — recorrer todas las páginas de una API,
  perezosamente y sin asumir cuántas hay.
- **`ejercicios/base/normalizar.py`** — convertir un payload anidado en un
  registro plano, distinguiendo lo que falta de lo que está vacío.
- **`ejercicios/reto/reintentos.py`** — reintentos con espera creciente, con el
  reloj inyectado para poder probarlos sin esperar de verdad.

## Resumen

- Valida en la frontera, confía dentro. Pydantic en el borde, dataclasses en el
  núcleo.
- Pydantic convierte además de validar, e informa de todos los errores a la vez.
- Con httpx: timeout siempre, `raise_for_status()` siempre, y reutiliza el
  cliente.
- Pagina con un generador: quien consume decide cuándo parar.
- Reintenta con espera creciente, y no duermas después del último intento.
- FastAPI es composición de lo que ya sabes: anotaciones + Pydantic + async.
- En pandas, mira `df.info()` antes de calcular nada. El dinero, en enteros.
- Filtrar en la base de datos, no en Python, cuando los datos ya están allí.
- Un test que necesita red no es un test unitario.

## Preguntas de repaso

1. ¿Por qué un modelo de validación en la frontera no sustituye al duck typing
   de dentro, ni al revés?
2. Tu petición devuelve 500 y tu código hace `.json()` sin más. ¿Qué pasa y
   dónde te vas a enterar?
3. ¿Qué ventaja tiene que el recorrido de páginas sea un generador?
4. Escribes reintentos con `for intento in range(3)`. ¿Cuál es el error más
   común en ese bucle?
5. ¿Cómo pruebas una función que espera entre reintentos sin que el test tarde
   siete segundos?
6. Sumas una columna de importes en pandas y el total es absurdo. ¿Qué miras
   primero?

## Recursos

- [Pydantic](https://docs.pydantic.dev/) — `doc-oficial` · `en` · `intermedio`.
  Empieza por *Models* y por *Validators*.
- [httpx](https://www.python-httpx.org/) — `doc-oficial` · `en` · `intermedio`.
  La guía avanzada explica bien los timeouts y el pool de conexiones.
- [FastAPI](https://fastapi.tiangolo.com/es/) — `doc-oficial` · `es` ·
  `intermedio`. El tutorial está en español y es de los mejores que existen.
- [pandas — 10 minutos](https://pandas.pydata.org/docs/user_guide/10min.html)
  — `doc-oficial` · `en` · `principiante`. Para orientarse rápido.

## Siguiente

Módulo 08 · Fundamentos de LLMs. A partir de aquí, la ruta cambia de tema.
