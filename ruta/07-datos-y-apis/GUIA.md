# Módulo 07 · Datos y APIs

> **Prerrequisitos:** módulos 01-06<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 08

Este es el módulo de las fronteras: donde tu programa habla con el mundo. Datos
que llegan de fuera y no te puedes fiar, servicios que responden tarde o mal,
archivos que hay que leer sin cargarlos enteros, tablas que hay que explorar
antes de decidir nada.

Casi todos los bugs caros de un sistema viven aquí, no en la lógica de negocio.

## Qué vas a poder hacer al terminar

- Leer y escribir archivos con `pathlib` y sin fugas
- Procesar CSV y JSON con la biblioteca estándar
- Validar datos en la frontera con pydantic
- Consumir APIs con httpx: timeouts, errores, paginación y reintentos
- Exponer un endpoint con FastAPI
- Explorar datos tabulares y saber cuándo pandas no es la respuesta

## 1. Archivos: `pathlib` y el `with`

```python
from pathlib import Path

ruta = Path("datos") / "movimientos.csv"     # el / compone rutas, sin barras a mano

ruta.exists()
ruta.suffix              # '.csv'
ruta.stem                # 'movimientos'
ruta.parent              # Path('datos')
ruta.stat().st_size      # bytes

for archivo in Path("logs").glob("*.log"): ...
for archivo in Path("logs").rglob("*.log"): ...   # recursivo
```

`pathlib` sustituye a la mezcla de `os.path.join`, `os.listdir` y cadenas con
barras. Funciona igual en Windows y en Unix, y las rutas se componen con `/`.

Para leer y escribir, siempre con `with`:

```python
with ruta.open(encoding="utf-8") as archivo:
    for linea in archivo:               # perezoso: no carga el archivo entero
        procesar(linea)

# y para casos cortos, los atajos:
texto = ruta.read_text(encoding="utf-8")
ruta.write_text(contenido, encoding="utf-8")
```

Tres cosas que no son opcionales:

**El `with`** garantiza que el archivo se cierra aunque salte una excepción. Sin
él, en un servidor de larga vida acabas con miles de descriptores abiertos y un
`OSError: too many open files` que no dice de dónde viene.

**El `encoding="utf-8"` explícito.** Sin él, Python usa la codificación por
defecto del sistema, que no es la misma en tu portátil que en el contenedor de
producción. Ese es el origen del clásico "funciona en local y en el servidor
salen caracteres raros".

**Iterar el archivo, no leerlo entero.** `for linea in archivo` va línea a
línea; `archivo.read()` carga los dos gigabytes en memoria.

### CSV y JSON, sin dependencias

```python
import csv, json

with ruta.open(encoding="utf-8", newline="") as archivo:
    for fila in csv.DictReader(archivo):       # cada fila es un dict
        print(fila["ref"], fila["monto"])      # ← todo llega como TEXTO

datos = json.loads(texto)                      # texto  → objetos
texto = json.dumps(datos, ensure_ascii=False, indent=2)   # objetos → texto
```

Dos avisos: `csv` devuelve **siempre cadenas**, así que convertir es tu trabajo
—y el módulo 01 ya te dijo cómo hacerlo con seguridad—; y el `newline=""` del
`open` no es opcional, es lo que evita líneas en blanco intercaladas en Windows.

## 2. La frontera: validar en la puerta

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
  payload lo arregla de una vez:
  ```python
  from pydantic import ValidationError
  try:
      Transfer.model_validate(payload)
  except ValidationError as error:
      print(error.errors())    # lista de dicts: campo, tipo de error, mensaje
  ```
- **Usa las anotaciones de tipo** que ya sabes escribir. Es una de las dos
  excepciones a "el intérprete no lee las anotaciones": Pydantic sí las lee, en
  tiempo de ejecución.

La regla: **valida en la frontera, confía dentro**. Un modelo Pydantic en el
borde y dataclasses normales en el núcleo es una arquitectura, no una
preferencia.

Y para la configuración, `pydantic-settings` hace lo del ejercicio `ajustes`
del módulo 04 con una línea:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str
    port: int = 5432
    debug: bool = False       # lee del entorno y convierte tipos
```

## 3. Hablar con APIs: httpx

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
Y admite granularidad:

```python
httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0)
```

**`raise_for_status()`.** Un 500 no lanza excepción por sí solo: te devuelve un
objeto respuesta con `status_code=500`. Si no lo compruebas, `respuesta.json()`
te dará basura o reventará lejos del origen.

**Reutiliza el cliente.** Crear un `Client` por petición tira a la basura el
pool de conexiones y el handshake TLS. Uno por proceso, o inyectado.

```python
client = httpx.Client(
    base_url="https://api.ejemplo.com",
    timeout=10.0,
    headers={"Authorization": f"Bearer {token}"},
    limits=httpx.Limits(max_connections=20),
)
```

Y en async, lo del módulo 06 aplica igual:

```python
async with httpx.AsyncClient(timeout=10.0) as client:
    respuestas = await asyncio.gather(*(client.get(u) for u in urls))
```

### Los cuatro patrones de toda integración

**Paginación.** Con un generador, quien consume decide cuándo parar:

```python
def all_pages(client, url):
    page = 1
    while True:
        datos = client.get(url, params={"page": page}).json()
        yield from datos["items"]
        if not datos["has_more"]:
            return
        page += 1
```

**Reintentos con espera creciente**, porque un 503 casi siempre es temporal:

```python
delays = [base * 2**n for n in range(attempts)]   # 1, 2, 4, 8…
```

Y respeta la cabecera `Retry-After` si el servidor la manda: es el proveedor
diciéndote exactamente cuánto esperar.

**Idempotencia.** Si reintentas un POST que sí llegó, lo haces dos veces. Los
proveedores serios aceptan una clave de idempotencia:

```python
client.post("/charges", json=datos, headers={"Idempotency-Key": str(uuid4())})
```

**Streaming**, para respuestas grandes que no caben en memoria:

```python
with client.stream("GET", url) as respuesta:
    for trozo in respuesta.iter_bytes():
        archivo.write(trozo)
```

## 4. Exponer una API: FastAPI

FastAPI no es un framework nuevo que aprender: es la composición de lo que ya
sabes. Anotaciones de tipo para declarar la entrada, Pydantic para validarla,
`async` para atender concurrentemente.

```python
from fastapi import FastAPI, HTTPException, Depends

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

Y las **dependencias** son la inyección que llevas viendo toda la ruta, ahora
con soporte del framework:

```python
def get_client() -> httpx.AsyncClient: ...

@app.get("/status")
async def status(client: httpx.AsyncClient = Depends(get_client)) -> dict:
    ...
```

En los tests, se sustituye con `app.dependency_overrides[get_client] = fake`.
Eso es doblar en la frontera, exactamente como decía el módulo 05.

```bash
uv run uvicorn app:app --reload    # y la documentación viva en /docs
```

## 5. Datos tabulares, y el criterio

```python
import pandas as pd

df = pd.read_csv("movimientos.csv", parse_dates=["fecha"])
df.head()
df.info()                                     # tipos y nulos: mira esto SIEMPRE primero
df.describe()                                 # estadísticas rápidas
df.groupby("divisa")["monto"].sum()
df[df["monto"] > 100_000].sort_values("fecha")
df["monto"].isna().sum()                      # cuántos nulos hay
```

Dos avisos que ahorran disgustos:

**Mira los tipos antes de calcular.** Una columna de montos que se leyó como
texto porque una fila traía `"N/A"` produce sumas silenciosamente absurdas.
`df.info()` lo enseña en un segundo.

**El dinero, otra vez, no en float.** Si vas a sumar importes, trabaja en
enteros de la unidad mínima o usa `Decimal`.

Y el criterio de cuándo usar qué:

| Situación | Herramienta |
|---|---|
| Explorar, y cabe en memoria | pandas |
| No cabe, o el rendimiento importa | Polars, DuckDB |
| Los datos ya están en una base | SQL, y traer solo el resultado |
| Cálculo numérico sobre matrices | NumPy |
| Unos miles de filas y lógica de negocio | Python a secas |

La línea que más veces se cruza mal: **traerse un millón de filas a Python para
filtrarlas es casi siempre un error de diseño**. Filtra donde están los datos.

Y la que se cruza mal en el otro sentido: montar pandas para procesar
doscientas filas de un CSV añade una dependencia enorme para algo que
`csv.DictReader` y un `defaultdict` resuelven mejor. Eso es lo que vas a hacer
en los ejercicios.

## 6. Por qué los ejercicios no importan nada de esto

Los tests de este módulo usan solo la biblioteca estándar. No es pereza, es la
lección del módulo 05 aplicada: **un test que necesita red no es un test
unitario, es una fuente de fallos intermitentes**.

Las piezas que vas a escribir —parsear filas, paginar, normalizar, agregar y
reintentar— son exactamente la lógica que rodea a `httpx` y a pandas, extraída
de forma que se pueda probar sin tocar la red. Que se puedan probar así no es
casualidad: es lo que pasa cuando separas el cálculo del efecto.

Si quieres ver el módulo con las librerías de verdad instaladas:

```bash
uv sync --group ia
```

## Caso real

Una integración con un proveedor de pagos funcionó seis meses y un lunes empezó
a perder transferencias. No fallaba: perdía. El informe diario cuadraba menos de
lo que debía y nadie veía errores en los logs.

Cuatro causas, las cuatro en la frontera:

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
4. **El CSV de conciliación se leía sin `encoding`.** En el contenedor, la
   codificación por defecto no era UTF-8, y las referencias con tilde no
   cruzaban con las del banco. Cuadraban menos, y el motivo no aparecía en
   ningún log.

Las cuatro son el mismo error de fondo: **tratar la ausencia o el fallo como si
fueran un caso normal**. Es la tríada de lectura del módulo 02 y el
`errors should never pass silently` del módulo 00, cobrados con intereses.

## Ejercicios

```bash
uv run pytest ruta/07-datos-y-apis
```

- **`ejercicios/base/filas.py`** — convertir filas de CSV en registros
  tipados, informando de la línea exacta donde algo falla.
- **`ejercicios/base/paginacion.py`** — recorrer todas las páginas de una API,
  perezosamente y sin asumir cuántas hay.
- **`ejercicios/base/normalizar.py`** — convertir un payload anidado en un
  registro plano, distinguiendo lo que falta de lo que está vacío.
- **`ejercicios/reto/reintentos.py`** — reintentos con espera creciente, con el
  reloj inyectado para poder probarlos sin esperar de verdad.
- **`ejercicios/reto/agregar.py`** — agrupar y resumir datos tabulares sin
  pandas, que es lo correcto cuando son doscientas filas.

## Resumen

- `pathlib` para rutas, `with` para archivos, `encoding="utf-8"` siempre, e
  iterar en vez de cargar entero.
- `csv.DictReader` devuelve texto: convertir es tu trabajo.
- Valida en la frontera, confía dentro. Pydantic en el borde, dataclasses en el
  núcleo.
- Pydantic convierte además de validar, e informa de todos los errores a la vez.
- Con httpx: timeout siempre, `raise_for_status()` siempre, y reutiliza el
  cliente.
- Los cuatro patrones de toda integración: paginar, reintentar con espera
  creciente, idempotencia en los POST y streaming para lo grande.
- Pagina con un generador: quien consume decide cuándo parar.
- FastAPI es composición de lo que ya sabes: anotaciones + Pydantic + async, y
  sus dependencias son la inyección de siempre.
- En pandas, mira `df.info()` antes de calcular nada. El dinero, en enteros.
- Filtra donde están los datos. Y no montes pandas para doscientas filas.
- Un test que necesita red no es un test unitario.

## Preguntas de repaso

1. ¿Qué pasa si abres archivos sin `with` en un servicio de larga vida?
2. ¿Por qué `encoding="utf-8"` explícito, si en tu máquina funciona sin él?
3. `csv.DictReader` te da `{"monto": "1500"}`. ¿Qué haces antes de sumarlo?
4. ¿Por qué un modelo de validación en la frontera no sustituye al duck typing
   de dentro, ni al revés?
5. Tu petición devuelve 500 y tu código hace `.json()` sin más. ¿Qué pasa y
   dónde te vas a enterar?
6. Reintentas un POST que sí había llegado. ¿Qué problema tienes y cómo se
   evita?
7. ¿Qué ventaja tiene que el recorrido de páginas sea un generador?
8. Escribes reintentos con `for intento in range(3)`. ¿Cuál es el error más
   común en ese bucle?
9. ¿Cómo pruebas una función que espera entre reintentos sin que el test tarde
   siete segundos?
10. Sumas una columna de importes en pandas y el total es absurdo. ¿Qué miras
    primero?
11. Tienes doscientas filas y necesitas agrupar por divisa. ¿pandas o
    `defaultdict`?

## Recursos

- [`pathlib`](https://docs.python.org/es/3/library/pathlib.html) —
  `doc-oficial` · `es` · `principiante`. Sustituye a media docena de funciones
  de `os.path`.
- [Pydantic](https://docs.pydantic.dev/) — `doc-oficial` · `en` · `intermedio`.
  Empieza por *Models* y por *Validators*.
- [HTTPX — clientes](https://www.python-httpx.org/advanced/clients/) — `doc-oficial` · `en` ·
  `intermedio`. La guía explica clientes, conexiones reutilizables y configuración compartida.
- [FastAPI — tutorial](https://fastapi.tiangolo.com/es/tutorial/) —
  `doc-oficial` · `es` · `intermedio`. En español y de los mejores que existen.
- [pandas — 10 minutos](https://pandas.pydata.org/docs/user_guide/10min.html)
  — `doc-oficial` · `en` · `principiante`. Para orientarse rápido.
- [DuckDB](https://duckdb.org/docs/) — `doc-oficial` · `en` · `intermedio`.
  SQL sobre archivos, sin servidor.

## Siguiente

Módulo 08 · Fundamentos de LLMs. A partir de aquí, la ruta cambia de tema.
