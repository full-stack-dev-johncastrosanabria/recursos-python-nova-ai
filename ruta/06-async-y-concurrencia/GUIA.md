# Módulo 06 · Async y concurrencia

> **Prerrequisitos:** módulos 01-05<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 07

La concurrencia es el tema donde más gente aplica la herramienta equivocada con
más convicción. Este módulo empieza por el criterio —cuándo `async` ayuda y
cuándo estorba— porque acertar ahí vale más que dominar la sintaxis.

Y hay una razón práctica para que esté aquí, justo antes de la parte de IA: un
agente que llama a tres herramientas, o un servicio que consulta un LLM mientras
atiende a otros usuarios, es un problema de concurrencia de manual.

## Qué vas a poder hacer al terminar

- Elegir entre asyncio, hilos y procesos con criterio
- Explicar qué es el GIL y qué consecuencias tiene
- Escribir funciones async y esperarlas con await
- Lanzar tareas concurrentes con gather y TaskGroup
- Limitar la concurrencia y poner tiempos máximos
- Comunicar productores y consumidores con una cola
- Reconocer lo que bloquea el bucle de eventos

## 1. El criterio, antes que la sintaxis

Casi todo el trabajo de un programa cae en uno de dos sacos:

**Ligado a entrada/salida (I/O-bound).** El programa está *esperando*: una
respuesta HTTP, una consulta a base de datos, un archivo, tokens de un LLM. La
CPU está parada.

**Ligado a CPU (CPU-bound).** El programa está *calculando*: comprimir,
redimensionar imágenes, entrenar, hacer números.

La distinción no es académica, porque en CPython hay un candado —el **GIL**—
que impide que dos hilos ejecuten bytecode de Python a la vez.

### El GIL, sin mitos

El *Global Interpreter Lock* es un candado que protege las estructuras internas
del intérprete. Existe porque CPython gestiona la memoria contando referencias
a cada objeto, y ese contador tiene que actualizarse de forma segura; hacerlo
con un candado global es mucho más simple y más rápido en un solo hilo que
poner un candado por objeto.

Tres precisiones que casi siempre faltan:

- **El GIL es de CPython, no del lenguaje.** Es la distinción del módulo 00
  entre lenguaje e implementación.
- **El GIL se suelta durante la espera de I/O.** Mientras un hilo espera una
  respuesta de red, los demás corren. Por eso los hilos **sí** sirven para
  problemas de espera.
- **Las extensiones en C pueden soltarlo.** NumPy lo libera durante sus
  operaciones sobre arrays: por eso una multiplicación de matrices grande sí
  aprovecha varios núcleos aunque la llames desde Python.

De ahí sale toda la tabla de decisión:

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

## 2. Hilos y procesos: la misma API para los dos

Antes de `asyncio`, y todavía hoy para librerías síncronas, está
`concurrent.futures`. Lo bueno es que hilos y procesos se usan igual:

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Espera: hilos
with ThreadPoolExecutor(max_workers=10) as pool:
    resultados = list(pool.map(descargar, urls))

# Cálculo: procesos
with ProcessPoolExecutor() as pool:
    resultados = list(pool.map(comprimir, imagenes))
```

Cambiar una palabra cambia el modelo de ejecución. Y con `submit` tienes control
fino:

```python
with ThreadPoolExecutor(max_workers=5) as pool:
    futuros = {pool.submit(descargar, url): url for url in urls}

    for futuro in as_completed(futuros):     # según van terminando
        url = futuros[futuro]
        try:
            datos = futuro.result()          # aquí se relanza la excepción
        except Exception as error:
            logger.warning("falló %s: %s", url, error)
```

Dos avisos sobre procesos que ahorran una tarde: lo que se les manda tiene que
poder **serializarse** (nada de funciones anónimas ni objetos con conexiones
abiertas), y arrancar un proceso **cuesta** — para tareas de milisegundos, el
arranque domina y sale más lento que hacerlo en serie.

## 3. `async` y `await`

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

## 4. Concurrencia de verdad: `gather` y `TaskGroup`

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

La diferencia práctica con `gather`: si una tarea falla, `TaskGroup` **cancela
las hermanas y espera a que terminen de cancelarse** antes de propagar. Con
`gather` puedes acabar con tareas sueltas corriendo en segundo plano. Para
código nuevo, `TaskGroup`.

## 5. Poner límites: `Semaphore` y `timeout`

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

Y el otro límite imprescindible es el **tiempo**:

```python
try:
    datos = await asyncio.wait_for(fetch_user(1), timeout=5.0)
except TimeoutError:
    datos = None            # degradar con gracia

# desde 3.11, con la forma de context manager:
async with asyncio.timeout(5.0):
    datos = await fetch_user(1)
```

Cuando se agota el plazo, la tarea **se cancela**: recibe una
`CancelledError` en su punto de espera. Eso significa que tu código debe estar
preparado para que lo interrumpan a mitad — si estabas escribiendo en una base
de datos, un `finally` que limpie no es opcional.

Sin timeout, una petición colgada retiene su tarea para siempre. Con muchas
peticiones, eso es una fuga que acaba tumbando el proceso.

## 6. Colas: productor y consumidor

Cuando una parte del programa produce trabajo y otra lo consume, la pieza que
las une es una cola:

```python
async def productor(cola: asyncio.Queue) -> None:
    for ref in refs:
        await cola.put(ref)          # espera si la cola está llena

async def consumidor(cola: asyncio.Queue, nombre: str) -> None:
    while True:
        ref = await cola.get()       # espera si está vacía
        try:
            await procesar(ref)
        finally:
            cola.task_done()

async def main() -> None:
    cola = asyncio.Queue(maxsize=100)
    consumidores = [asyncio.create_task(consumidor(cola, f"c{i}")) for i in range(5)]

    await productor(cola)
    await cola.join()                # espera a que todo lo puesto se marque hecho

    for tarea in consumidores:
        tarea.cancel()               # los consumidores son bucles infinitos
```

El `maxsize` es lo importante: una cola sin límite es una fuga de memoria
disfrazada de diseño. Si el productor va más rápido que los consumidores —y
casi siempre va más rápido, porque leer es más barato que procesar— sin
`maxsize` la cola crece hasta que el proceso muere. Con `maxsize`, `put` espera
y el productor se frena solo. Eso se llama **contrapresión**, y es lo que
separa un pipeline que aguanta de uno que revienta con carga.

## 7. Generadores asíncronos y streaming

El módulo 00 decía que la iteración es la abstracción central. En async también:

```python
async def leer_eventos(cliente) -> AsyncIterator[dict]:
    async with cliente.stream("GET", url) as respuesta:
        async for linea in respuesta.aiter_lines():
            if linea:
                yield json.loads(linea)

async for evento in leer_eventos(cliente):
    procesar(evento)
```

Es el mismo generador perezoso del módulo 02, con `async` delante. Y es
exactamente la forma de un LLM que responde token a token: cuando en el módulo
08 veas `stream`, esto es lo que hay debajo.

## 8. Lo que rompe el bucle de eventos

Todo el modelo se sostiene sobre una premisa: **nadie bloquea**. Una sola
llamada bloqueante congela *todas* las tareas del bucle, porque hay un solo
hilo.

```python
async def malo():
    time.sleep(1)            # ← bloquea TODO el bucle un segundo
    requests.get(url)        # ← igual: librería síncrona
    json.loads(texto_de_50mb)  # ← y el cálculo pesado, también

async def bien():
    await asyncio.sleep(1)   # cede el control
    await client.get(url)    # cliente asíncrono (httpx, aiohttp)
```

¿Y si necesitas usar una librería síncrona que no puedes cambiar? Se manda a un
hilo:

```python
resultado = await asyncio.to_thread(funcion_bloqueante, argumento)
```

Y si lo que bloquea es cálculo, a un proceso:

```python
loop = asyncio.get_running_loop()
with ProcessPoolExecutor() as pool:
    resultado = await loop.run_in_executor(pool, calculo_pesado, datos)
```

### Errores frecuentes

- **Olvidar el `await`.** La corrutina no se ejecuta y Python avisa con un
  `RuntimeWarning: coroutine was never awaited`. Si ves ese aviso, búscalo: es
  siempre un bug.
- **Crear una tarea y no guardarla.** `asyncio.create_task(...)` sin asignar el
  resultado permite que el recolector de basura se la lleve a media ejecución.
  Guarda la referencia, o usa `TaskGroup`.
- **`asyncio.run` dentro de una función async.** Solo se llama una vez, en la
  raíz.

## 9. Cuándo NO usar async

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

La segunda versión añadió el semáforo y funcionó — hasta que una de las
peticiones se quedó colgada. Sin timeout, esa tarea retuvo su hueco del
semáforo indefinidamente, y el proceso fue degradándose hasta que las diez
plazas estaban ocupadas por peticiones muertas.

La versión final:

```python
async def procesar_todas(refs: list[str], limit: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(limit)

    async def una(ref: str) -> dict | None:
        async with semaphore:
            try:
                async with asyncio.timeout(5.0):
                    respuesta = await client.get(url(ref))
                    return respuesta.json()
            except TimeoutError:
                logger.warning("timeout con %s", ref)
                return None

    return await asyncio.gather(*(una(ref) for ref in refs))
```

Diez segundos, dentro del límite de tasa del proveedor, con el orden de los
resultados conservado y sin plazas que se pierdan para siempre. Las cuatro
piezas del módulo: `async` porque el problema es de espera, `gather` porque las
esperas pueden solaparse, el semáforo porque *poder* lanzar mil no significa que
debas, y el timeout porque una espera sin plazo no es una espera, es una fuga.

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
- **`ejercicios/base/temporizado.py`** — poner plazo a una espera y degradar
  con gracia cuando se agota.
- **`ejercicios/reto/resiliente.py`** — recoger todos los resultados aunque
  algunos fallen. Es lo que necesita un orquestador de herramientas.
- **`ejercicios/reto/cola.py`** — productor y consumidores con contrapresión.

## Resumen

- Primero el criterio: ¿estás esperando o estás calculando? `asyncio` para lo
  primero, procesos para lo segundo.
- El GIL es de CPython, **se suelta durante la espera de I/O**, y las
  extensiones en C pueden soltarlo. De ahí sale la tabla de decisión.
- `concurrent.futures` da la misma API para hilos y procesos. Lo que va a un
  proceso tiene que ser serializable, y arrancarlo cuesta.
- Llamar a una corrutina no la ejecuta; hace falta `await` o una tarea.
- `await` seguido de `await` es secuencial. La concurrencia se pide con
  `gather` o `TaskGroup`.
- `TaskGroup` cancela a las hermanas y espera; `gather` puede dejar tareas
  sueltas. Para código nuevo, `TaskGroup`.
- `gather` conserva el orden; con `return_exceptions=True` recoge fallos sin
  cancelar el resto.
- Un `Semaphore` limita cuántas tareas están dentro a la vez, y un `timeout`
  impide que una espera dure para siempre. Hacen falta los dos.
- Una cola sin `maxsize` es una fuga de memoria. La contrapresión es lo que
  hace que un pipeline aguante.
- `async for` sobre un generador asíncrono es lo que hay debajo del streaming
  de un LLM.
- Una sola llamada bloqueante congela el bucle entero. Para librerías
  síncronas, `asyncio.to_thread`; para cálculo, un proceso.
- `async` tiñe el código hasta la raíz. Si no estás esperando mucho, no
  compensa.

## Preguntas de repaso

1. Tu programa redimensiona 500 imágenes. ¿`asyncio`, hilos o procesos?
2. Si el GIL impide ejecutar bytecode en paralelo, ¿por qué los hilos sirven
   para descargar cien URLs?
3. ¿Por qué `a = await f(); b = await g()` no es concurrente?
4. ¿Qué pasa si dentro de una corrutina llamas a `time.sleep(2)`?
5. Lanzas 1.000 peticiones con `gather` y la API te devuelve 429. ¿Qué añades?
6. Añades el semáforo y aun así el servicio se degrada con el tiempo. ¿Qué te
   falta?
7. Una de las diez tareas de tu `gather` lanza una excepción. ¿Qué les pasa a
   las otras nueve, y cómo cambia eso con `TaskGroup`?
8. ¿Por qué una `asyncio.Queue` sin `maxsize` es peligrosa?
9. Ves un `RuntimeWarning: coroutine was never awaited`. ¿Qué ha pasado?
10. Tienes que usar una librería que solo tiene API síncrona dentro de un
    servicio async. ¿Qué haces?

## Recursos

- [`asyncio` — documentación](https://docs.python.org/es/3/library/asyncio.html)
  — `doc-oficial` · `es` · `intermedio`. Empieza por *Corutinas y tareas*.
- [`asyncio.TaskGroup`](https://docs.python.org/es/3/library/asyncio-task.html#task-groups)
  — `doc-oficial` · `es` · `intermedio`. La forma moderna, con la garantía de
  que ninguna tarea queda huérfana.
- [`concurrent.futures`](https://docs.python.org/es/3/library/concurrent.futures.html)
  — `doc-oficial` · `es` · `intermedio`. La misma API para hilos y procesos.
- [PEP 492 — async y await](https://peps.python.org/pep-0492/) —
  `doc-oficial` · `en` · `avanzado`. Por qué la sintaxis es como es.
- [httpx](https://www.python-httpx.org/async/) — `doc-oficial` · `en` ·
  `intermedio`. El cliente HTTP que habla async y que usarás en el módulo 07.

## Siguiente

Módulo 07 · Datos y APIs.
