# Módulo 06 · Async y concurrencia

> **Prerrequisitos:** módulos 01-05
> **Tiempo estimado:** 120 min
> **Si ya dominas esto:** salta al módulo 07

La concurrencia es el tema donde más gente aplica la herramienta equivocada con
más convicción. Este módulo empieza por el criterio —cuándo `async` ayuda y
cuándo estorba— porque acertar ahí vale más que dominar la sintaxis.

Y hay una razón práctica para que esté aquí, justo antes de la parte de IA: un
agente que llama a tres herramientas, o un servicio que consulta un LLM mientras
atiende a otros usuarios, es un problema de concurrencia de manual.

## Qué vas a poder hacer al terminar

- Escribir funciones async y esperarlas con await
- Lanzar tareas concurrentes con asyncio
- Distinguir cuándo async ayuda y cuándo estorba

## 1. El criterio, antes que la sintaxis

Casi todo el trabajo de un programa cae en uno de dos sacos:

**Ligado a entrada/salida (I/O-bound).** El programa está *esperando*: una
respuesta HTTP, una consulta a base de datos, un archivo, tokens de un LLM. La
CPU está parada.

**Ligado a CPU (CPU-bound).** El programa está *calculando*: comprimir,
redimensionar imágenes, entrenar, hacer números.

La distinción no es académica, porque en CPython hay un candado —el **GIL**—
que impide que dos hilos ejecuten bytecode de Python a la vez. Lo importante es
que **el GIL se suelta durante la espera de I/O**. De ahí sale toda la tabla de
decisión:

| Tu problema | Herramienta | Por qué |
|---|---|---|
| Muchas esperas de red o disco | `asyncio` | miles de esperas en un hilo, sin coste por tarea |
| Esperas, pero con librerías que no son async | hilos (`ThreadPoolExecutor`) | el GIL se suelta al esperar |
| Cálculo puro y pesado | procesos (`ProcessPoolExecutor`) | cada proceso tiene su propio GIL |
| Cálculo pesado sobre arrays | NumPy y compañía | el bucle baja a C y suelta el GIL |

El error clásico es meter `async` en un problema de CPU: no gana nada y encima
bloquea el bucle de eventos, así que empeora. El error inverso —lanzar treinta
hilos para treinta peticiones HTTP— funciona, pero paga memoria y cambios de
contexto que `asyncio` no paga.

## 2. `async` y `await`

```python
import asyncio

async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.1)          # aquí cedería el control durante la espera
    return {"id": user_id, "name": "Ana"}

async def main() -> None:
    user = await fetch_user(1)
    print(user)

asyncio.run(main())
```

Tres reglas que evitan el 90% de la confusión:

**Llamar a una corrutina no la ejecuta.** `fetch_user(1)` devuelve un objeto
corrutina, igual que llamar a un generador devuelve un generador. Hace falta
`await` (o una tarea) para que corra.

**`await` solo se puede usar dentro de `async def`.** El punto de entrada al
mundo asíncrono es `asyncio.run(...)`, una sola vez, en la raíz del programa.

**`await` no es concurrencia.** Esto es secuencial y tarda 0.3 segundos:

```python
a = await fetch_user(1)
b = await fetch_user(2)
c = await fetch_user(3)
```

## 3. Concurrencia de verdad: `gather` y `TaskGroup`

Para que las tres esperas ocurran a la vez hay que decirlo:

```python
a, b, c = await asyncio.gather(
    fetch_user(1),
    fetch_user(2),
    fetch_user(3),
)   # ~0.1 s en total, no 0.3
```

`gather` conserva el orden de los resultados aunque terminen desordenadas, que
es justo lo que quieres casi siempre.

Con una lista, la forma idiomática:

```python
users = await asyncio.gather(*(fetch_user(i) for i in ids))
```

Y si una falla, por defecto `gather` propaga esa excepción y cancela el resto.
Cuando prefieras recoger todos los resultados, buenos y malos:

```python
resultados = await asyncio.gather(*tareas, return_exceptions=True)
# cada elemento es el resultado… o la excepción, sin haber interrumpido a los demás
```

Ese modo es el que querrás cuando un agente lance tres herramientas en paralelo
y una devuelva error: lo razonable es seguir con las otras dos, no tirarlo todo.

Desde 3.11 existe además `asyncio.TaskGroup`, que es la forma moderna y más
segura porque garantiza que ninguna tarea queda huérfana:

```python
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(fetch_user(1))
    t2 = tg.create_task(fetch_user(2))
# al salir del with, ambas han terminado (o el grupo ha cancelado y propagado)
```

## 4. Poner límites: `Semaphore`

Lanzar mil peticiones a la vez contra una API es una forma rápida de que te
bloqueen. El límite se pone con un semáforo:

```python
async def fetch_limited(ids: list[int], limit: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(limit)

    async def one(user_id: int) -> dict:
        async with semaphore:        # como mucho `limit` dentro a la vez
            return await fetch_user(user_id)

    return await asyncio.gather(*(one(i) for i in ids))
```

Las mil tareas se crean, pero solo diez están dentro del semáforo
simultáneamente. Es el patrón que vas a repetir cada vez que hables con una API
que tiene límites de tasa — incluidas las de LLMs.

## 5. Lo que rompe el bucle de eventos

Todo el modelo se sostiene sobre una premisa: **nadie bloquea**. Una sola
llamada bloqueante congela *todas* las tareas del bucle, porque hay un solo
hilo.

```python
async def malo():
    time.sleep(1)            # ← bloquea TODO el bucle un segundo
    requests.get(url)        # ← igual: librería síncrona

async def bien():
    await asyncio.sleep(1)   # cede el control
    await client.get(url)    # cliente asíncrono (httpx, aiohttp)
```

¿Y si necesitas usar una librería síncrona que no puedes cambiar? Se manda a un
hilo:

```python
resultado = await asyncio.to_thread(funcion_bloqueante, argumento)
```

## 6. Cuándo NO usar async

Sé honesto con el coste: `async` tiñe el código. Una función async solo se
puede esperar desde otra async, así que la decisión se propaga hacia arriba
hasta la raíz del programa.

No lo uses si tu programa hace pocas llamadas de red y no necesita atender a
nadie mientras espera — un script que consulta tres endpoints y termina se lee
mejor síncrono. Y no lo uses nunca para acelerar cálculo: eso son procesos.

La pregunta correcta no es "¿esto podría ser async?" sino **"¿estoy esperando
tanto que valga la pena la complejidad?"**.

## Caso real

Un servicio recorría 500 referencias y consultaba una API por cada una:

```python
for ref in refs:                       # 500 iteraciones
    datos = requests.get(url(ref))     # ~200 ms de espera cada una
    procesar(datos)
```

Cien segundos, de los cuales noventa y nueve la CPU estaba mirando al techo. Es
el caso de libro de I/O-bound.

La primera versión "arreglada" lanzó las 500 con `gather` a la vez. Bajó a dos
segundos… durante tres días, hasta que la API empezó a devolver 429 y el
proveedor mandó un correo. Concurrencia sin límite no es rendimiento, es un
ataque de denegación de servicio con buenas intenciones.

La versión final:

```python
async def procesar_todas(refs: list[str], limit: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(limit)

    async def una(ref: str) -> dict:
        async with semaphore:
            respuesta = await client.get(url(ref))
            return respuesta.json()

    return await asyncio.gather(*(una(ref) for ref in refs))
```

Diez segundos, dentro del límite de tasa del proveedor, y con el orden de los
resultados conservado. Las tres piezas del módulo: `async` porque el problema
es de espera, `gather` porque las esperas pueden solaparse, y el semáforo
porque *poder* lanzar mil no significa que debas.

## Ejercicios

```bash
uv run pytest ruta/06-async-y-concurrencia
```

Los tests llaman a tu código con `asyncio.run(...)`, así que no necesitas
instalar nada extra.

- **`ejercicios/base/paralelo.py`** — que tres esperas ocurran a la vez en vez
  de una detrás de otra.
- **`ejercicios/base/limitado.py`** — lo mismo, pero sin pasarte del límite.
  Sus tests miden cuántas tareas llegan a estar dentro a la vez.
- **`ejercicios/reto/resiliente.py`** — recoger todos los resultados aunque
  algunos fallen. Es lo que necesita un orquestador de herramientas.

## Resumen

- Primero el criterio: ¿estás esperando o estás calculando? `asyncio` para lo
  primero, procesos para lo segundo.
- El GIL impide ejecutar bytecode en paralelo, pero **se suelta durante la
  espera de I/O**. De ahí sale toda la tabla de decisión.
- Llamar a una corrutina no la ejecuta; hace falta `await` o una tarea.
- `await` seguido de `await` es secuencial. La concurrencia se pide con
  `gather` o `TaskGroup`.
- `gather` conserva el orden; con `return_exceptions=True` recoge fallos sin
  cancelar el resto.
- Un `Semaphore` limita cuántas tareas están dentro a la vez. Poder lanzar mil
  no significa que debas.
- Una sola llamada bloqueante congela el bucle entero. Para librerías
  síncronas, `asyncio.to_thread`.
- `async` tiñe el código hasta la raíz. Si no estás esperando mucho, no
  compensa.

## Preguntas de repaso

1. Tu programa redimensiona 500 imágenes. ¿`asyncio`, hilos o procesos?
2. ¿Por qué `a = await f(); b = await g()` no es concurrente?
3. ¿Qué pasa si dentro de una corrutina llamas a `time.sleep(2)`?
4. Lanzas 1.000 peticiones con `gather` y la API te devuelve 429. ¿Qué añades?
5. Una de las diez tareas de tu `gather` lanza una excepción. ¿Qué les pasa a
   las otras nueve, y cómo cambia eso con `return_exceptions=True`?
6. Tienes que usar una librería que solo tiene API síncrona dentro de un
   servicio async. ¿Qué haces?

## Recursos

- [`asyncio` — documentación](https://docs.python.org/es/3/library/asyncio.html)
  — `doc-oficial` · `es` · `intermedio`. Empieza por *Corutinas y tareas*.
- [PEP 492 — async y await](https://peps.python.org/pep-0492/) —
  `doc-oficial` · `en` · `avanzado`. Por qué la sintaxis es como es.
- [httpx](https://www.python-httpx.org/async/) — `doc-oficial` · `en` ·
  `intermedio`. El cliente HTTP que habla async y que usarás en el módulo 07.

## Siguiente

Módulo 07 · Datos y APIs.
