"""Reto: productor, consumidores y contrapresión.

Escribe `run_queue`, que reparte una lista de elementos entre varios
trabajadores usando una cola con tamaño limitado.

    await run_queue([1, 2, 3, 4], worker=doblar, workers=2, max_queue=2)
    -> [2, 4, 6, 8]

Reglas:

- `worker` es una función asíncrona que recibe un elemento y devuelve su
  resultado.
- Los resultados salen **en el orden de entrada**, no en el de finalización.
  Como los trabajadores terminan desordenados, tendrás que llevar la posición
  de cada elemento.
- Como mucho `workers` elementos se procesan a la vez. Sus tests lo comprueban
  contando cuántos coinciden dentro.
- La cola se crea con `maxsize=max_queue`. **Ese límite es el ejercicio**: una
  cola sin tope es una fuga de memoria disfrazada de diseño. Si el productor va
  más rápido que los consumidores —y casi siempre va más rápido, porque leer es
  más barato que procesar— la cola crece hasta que el proceso muere. Con tope,
  `put` espera y el productor se frena solo. Eso es la contrapresión.
- `workers` o `max_queue` menores que 1 son `ValueError`.
- Sin elementos, lista vacía y sin arrancar nada.
- Cuando termina, **no puede quedar ninguna tarea viva**. Los consumidores son
  bucles infinitos: hay que cancelarlos.

El esqueleto del patrón:

1. Crea la cola con su tope.
2. Arranca `workers` tareas consumidoras, cada una en un bucle
   `item = await cola.get()` … `cola.task_done()`.
3. Ve poniendo `(posicion, elemento)` en la cola.
4. `await cola.join()` para esperar a que todo lo puesto se marque hecho.
5. Cancela las tareas consumidoras.
"""

from collections.abc import Callable, Sequence


async def run_queue(
    items: Sequence, worker: Callable, workers: int = 3, max_queue: int = 10
) -> list:
    raise NotImplementedError("Borra esta línea y escribe tu solución")
