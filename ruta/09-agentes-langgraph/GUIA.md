# Módulo 09 · Agentes con LangGraph

> **Prerrequisitos:** módulos 01-08<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 10

En el módulo 08 el modelo te pedía llamar a una herramienta y tú se lo
resolvías. Si eso se repite —pedir, ejecutar, volver a preguntar— ya tienes un
agente. Este módulo va de darle estructura a ese bucle.

Y empieza con una advertencia que conviene tomarse en serio: **la mayoría de
los flujos no necesitan un framework de agentes**. Vas a aprender el modelo de
LangGraph, y también cuándo el código plano del módulo 08 era suficiente.

## Qué vas a poder hacer al terminar

- Elegir el patrón adecuado antes de escribir código
- Modelar un flujo como grafo de estado
- Definir nodos y transiciones condicionales
- Persistir estado con checkpoints
- Insertar un paso de human-in-the-loop
- Gestionar la memoria de una conversación larga
- Observar y depurar un agente en producción

## 1. La escalera: cinco patrones antes del agente

Antes de montar un agente, mira si tu problema encaja en algo más simple. Están
ordenados de menos a más complejidad, y **casi siempre el correcto es el más
alto de la lista que resuelva el problema**:

**1. Cadena.** Pasos fijos, en orden. Extraer → clasificar → redactar. Sin
decisiones. Es una función que llama a tres funciones.

**2. Enrutamiento.** Se decide una vez a dónde va, y luego se sigue una cadena.
La decisión puede tomarla un modelo… o unas reglas. Es el ejercicio
`enrutador`, y su lección es que **la mitad de los enrutamientos que se
implementan con un LLM son cuatro `if`**.

**3. Paralelización.** Varias subtareas independientes a la vez, y luego se
juntan. Es el `gather` del módulo 06, con llamadas a un modelo dentro.

**4. Orquestador y trabajadores.** Un paso descompone la tarea en subtareas que
no se conocían de antemano, otros las ejecutan, el primero integra. Aquí ya hace
falta un modelo para decidir la descomposición.

**5. Agente.** Bucle abierto: el modelo decide qué hacer a continuación, con
herramientas, hasta que considera que terminó. Máxima capacidad y máxima
imprevisibilidad.

La pregunta que ordena todo: **¿cuántas de las decisiones de mi flujo necesitan
juicio de verdad?** Si la respuesta es "ninguna", no necesitas un agente:
necesitas una cadena con una o dos llamadas al modelo en los puntos donde hay
ambigüedad real.

## 2. El bucle de agente, sin framework

```python
def run_agent(model, tools, user_message, max_steps=5):
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_steps):
        respuesta = model(messages)

        if respuesta["type"] == "text":
            return respuesta["text"]

        resultado = tools[respuesta["name"]](**respuesta["input"])
        messages.append({"role": "assistant", "content": respuesta})
        messages.append({"role": "user", "content": str(resultado)})

    raise RuntimeError("el agente no terminó dentro del presupuesto de pasos")
```

Eso es un agente completo. Diecisiete líneas. Fíjate en el `max_steps`: **todo
bucle de agente lleva tope**. Sin él, un modelo que se confunda puede quedarse
llamando herramientas indefinidamente, y cada vuelta cuesta dinero.

Para una cadena simple o un routing, esto es todo lo que hace falta, y es más
claro y más testeable que cualquier framework. Empezar aquí y migrar cuando la
complejidad lo justifique es casi siempre mejor que empezar con el framework y
descubrir que peleas contra sus abstracciones.

## 3. El modelo de LangGraph: un grafo de estado

Cuando el flujo deja de ser lineal —hay ramas según lo que decida el modelo,
ciclos con condiciones de salida no triviales, puntos donde tiene que aprobar
un humano— mantener eso a mano se convierte en un enredo de banderas.

LangGraph lo modela como un **grafo**: los nodos son pasos y las aristas son
transiciones, con un estado que fluye y se va actualizando.

```text
        ┌──────────┐
        │  inicio  │
        └────┬─────┘
             ▼
      ┌─────────────┐      ¿necesita herramienta?
      │   pensar    │──────────────┐
      └──────┬──────┘              ▼
             │ no              ┌────────────┐
             ▼                 │ ejecutar   │
        ┌─────────┐            │ herramienta│
        │ terminar│            └──────┬─────┘
        └─────────┘                   │
             ▲                        │
             └────────────────────────┘   (ciclo: vuelve a pensar)
```

Y aquí está la idea que desarma la novedad aparente: **un grafo de LangGraph es
un pliegue sobre un estado**. Los nodos son transiciones, y el estado se
acumula con *reducers* — funciones que combinan lo que había con lo que
devuelve el nodo. Es el mismo `reduce` de siempre, con herramientas de
visualización encima.

```python
from typing import Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]   # los nodos AÑADEN mensajes
    steps: Annotated[int, add]       # y suman pasos
    answer: str                      # esto se REEMPLAZA (sin reducer)
```

Esa distinción es lo que vas a implementar en el primer ejercicio: una clave
con reducer acumula, una clave sin reducer se sobrescribe.

## 4. Nodos, aristas y transiciones condicionales

```python
from langgraph.graph import StateGraph, END

def pensar(state: State) -> dict:
    respuesta = model(state["messages"])
    return {"messages": [respuesta], "steps": 1}   # una ACTUALIZACIÓN, no el estado

def ejecutar_herramienta(state: State) -> dict:
    ultima = state["messages"][-1]
    resultado = tools[ultima["name"]](**ultima["input"])
    return {"messages": [{"role": "user", "content": str(resultado)}]}

def decidir(state: State) -> str:
    return "herramienta" if state["messages"][-1]["type"] == "tool_use" else END

grafo = StateGraph(State)
grafo.add_node("pensar", pensar)
grafo.add_node("herramienta", ejecutar_herramienta)
grafo.set_entry_point("pensar")
grafo.add_conditional_edges("pensar", decidir)
grafo.add_edge("herramienta", "pensar")      # el ciclo

app = grafo.compile()
```

Dos detalles que importan más de lo que parecen:

**Un nodo devuelve una actualización, no el estado entero.** Devolver
`{"messages": [uno]}` no borra los anteriores: el reducer los concatena. Es lo
que permite que los nodos no sepan nada del resto del grafo.

**La función de decisión es código normal.** Se prueba con un test unitario,
sin modelo ni red. Esa es la ventaja principal del modelo de grafo: el flujo se
puede inspeccionar y probar en vez de emerger de una conversación.

## 5. Ciclos y presupuesto

El ciclo `pensar → herramienta → pensar` es lo que hace útil a un agente, y
también lo que puede salir caro. Tres protecciones, y hacen falta las tres:

```python
app.invoke(estado_inicial, {"recursion_limit": 25})
```

Ese límite del framework te salva del bucle infinito. **No te salva de gastar
veinte llamadas para algo que debía costar dos**, así que añade las tuyas:

- **Por pasos**, como en el bucle a mano.
- **Por tokens gastados**, acumulando `usage` en el estado y cortando al llegar
  al presupuesto.
- **Por tiempo**, con el `timeout` del módulo 06.

Un agente sin presupuesto es una tarjeta de crédito sin límite en manos de algo
no determinista.

## 6. Memoria: qué recuerda y cuánto cuesta

El modelo no recuerda nada, así que "memoria" significa "qué le vuelvo a
mandar". Y como el historial se reenvía entero, la memoria **es** el coste.

Cuatro estrategias, de menos a más elaborada:

**Ventana deslizante.** Te quedas con los últimos N mensajes. Simple y
suficiente para conversaciones cortas. Es lo que hiciste en `mensajes`.

**Resumen progresivo.** Cuando el historial pasa de un umbral, se pide al modelo
que resuma lo viejo y se sustituye por el resumen. Conserva el hilo a cambio de
una llamada extra y de perder detalle.

**Memoria por hechos.** Se extraen datos concretos ("la cuenta del cliente es
CR01-0002") a un almacén aparte y se inyectan cuando hacen falta. Más trabajo,
mucho más control.

**Recuperación sobre el historial.** El historial completo se indexa y se
recuperan los fragmentos relevantes, como un RAG sobre la propia conversación.

La regla práctica: empieza por la ventana. Sube de nivel cuando tengas una
queja concreta —"se olvidó de lo que le dije al principio"— y no antes.

## 7. Checkpoints y human-in-the-loop

Un checkpointer guarda el estado después de cada nodo:

```python
from langgraph.checkpoint.memory import MemorySaver

app = grafo.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "conversacion-42"}}

app.invoke({"messages": [...]}, config)   # y más tarde, en otra petición:
app.invoke({"messages": [nuevo]}, config) # continúa donde lo dejó
```

Eso da tres cosas: conversaciones que sobreviven entre peticiones HTTP,
reanudación tras un fallo sin repetir el trabajo hecho, y la posibilidad de
**parar el grafo para que intervenga un humano**:

```python
app = grafo.compile(checkpointer=MemorySaver(), interrupt_before=["transferir"])
```

Con eso, el grafo se detiene antes de ejecutar la transferencia y espera
aprobación. Para cualquier acción con consecuencias —mover dinero, borrar,
enviar— ese punto de control no es opcional.

Y el criterio de dónde ponerlo: **donde la acción sea irreversible**. Consultar
un saldo no necesita aprobación; transferirlo, sí. Esa distinción es la misma
que la del módulo 08 entre herramientas que leen y herramientas que escriben.

## 8. Observar un agente en producción

Un agente que falla y no deja rastro es imposible de arreglar. Lo mínimo que
hay que registrar por ejecución:

- **Cada paso**: qué herramienta pidió, con qué argumentos, qué devolvió.
- **Los tokens** de entrada y salida acumulados, que son la factura.
- **El motivo de terminación**: respondió, se agotó el presupuesto, falló.
- **Un identificador de traza** que permita reconstruir la ejecución entera.

Con eso puedes responder las tres preguntas que siempre se hacen: por qué
respondió eso, cuánto costó, y en qué paso se torció.

LangGraph permite además ir emitiendo los pasos intermedios según ocurren:

```python
async for evento in app.astream(estado, config):
    logger.info("paso: %s", evento)
```

Es el generador asíncrono del módulo 06, otra vez.

## 9. Cuándo NO usar un framework

Sé honesto con el criterio:

**No lo uses** si el flujo es una cadena o un routing simple. Código plano y la
librería del modelo es más claro, más testeable y no te ata a una API joven que
va a cambiar.

**Considéralo** cuando el flujo tenga estructura de verdad compleja —varios
pasos con estado compartido, ramas condicionales sobre decisiones del modelo,
ciclos con salidas no triviales, intervención humana en medio— o cuando
necesites la infraestructura transversal que trae (persistencia,
observabilidad, reanudación, streaming de pasos) y reimplementarla cueste más
que la dependencia.

La regla: **adopta el framework con la evidencia de que su estructura se paga,
no con la expectativa de que "así se hacen los agentes"**.

## Caso real

Un equipo modeló la conciliación entera como un sistema de agentes: uno
parseaba el archivo, otro cruzaba las referencias, otro investigaba las
discrepancias y otro redactaba el informe.

Funcionaba. Costaba unos ocho dólares por ejecución, tardaba cuatro minutos y
fallaba de forma distinta cada vez.

Al revisarlo, la pregunta correcta resultó ser otra: **¿cuáles de esos cuatro
pasos necesitan juicio?** Parsear un archivo es determinista. Cruzar
referencias es la intersección de conjuntos del módulo 02. Redactar el informe
es una plantilla. Solo investigar discrepancias que no cuadran por razones no
obvias requiere un modelo.

La versión final: un pipeline determinista de tres pasos, y **un único agente
acotado** para la investigación, con tope de pasos y las herramientas justas.
Céntimos por ejecución, segundos en vez de minutos, y un resultado que se puede
auditar porque tres de las cuatro etapas son código normal con tests.

La lección generaliza: cada agente que añades multiplica coste, latencia e
imprevisibilidad, y la coordinación entre ellos es superficie de fallo nueva.
**El sistema multiagente elegante de la demo suele ser el sistema frágil y caro
de producción.**

## Ejercicios

```bash
uv run pytest ruta/09-agentes-langgraph
```

No necesitas instalar LangGraph ni tener clave de API: vas a implementar el
**modelo**, que es lo que hay que entender. El framework es una implementación
de esto con persistencia y visualización encima.

- **`ejercicios/base/estado.py`** — los reducers: qué claves acumulan y cuáles
  se reemplazan.
- **`ejercicios/base/grafo.py`** — el ejecutor del grafo, con transiciones
  condicionales, ciclos y tope de pasos.
- **`ejercicios/base/enrutador.py`** — enrutar por reglas antes de gastar una
  llamada al modelo.
- **`ejercicios/reto/ciclo.py`** — el bucle de agente completo, con un modelo
  de mentira que responde según un guion.

## Resumen

- Antes del agente están la cadena, el enrutamiento, la paralelización y el
  orquestador. Elige el más simple que resuelva el problema.
- La mitad de los enrutamientos que se implementan con un LLM son cuatro `if`.
- Un agente es un bucle: el modelo pide, tú ejecutas, le devuelves el
  resultado. Diecisiete líneas sin framework.
- Todo bucle de agente lleva tope de pasos, de tokens y de tiempo.
- Un grafo de LangGraph es un pliegue sobre un estado: nodos como transiciones
  y reducers acumulando.
- Un nodo devuelve una **actualización**, no el estado entero.
- La función que decide la siguiente arista es código normal y se prueba sin
  modelo ni red.
- La memoria es el coste. Empieza por la ventana deslizante y sube de nivel
  ante una queja concreta.
- Los checkpoints dan continuidad, reanudación y el punto donde para un humano.
  Ese punto va donde la acción es irreversible.
- Registra cada paso, los tokens y el motivo de terminación, o no podrás
  arreglar nada.
- Adopta el framework con evidencia de que se paga, no por costumbre.

## Preguntas de repaso

1. Tu flujo tiene tres pasos fijos y ninguna decisión. ¿Qué patrón usas?
2. Necesitas mandar cada correo entrante a uno de cuatro tratamientos según su
   asunto. ¿Hace falta un modelo?
3. ¿Por qué todo bucle de agente necesita tope, y por qué no basta con el del
   framework?
4. Un nodo devuelve `{"messages": [uno]}`. ¿Se pierden los mensajes anteriores?
   ¿De qué depende?
5. ¿Qué parte de un grafo se puede probar sin modelo ni red?
6. Tu agente "se olvida" de lo que le dijeron al principio de una conversación
   larga. ¿Qué estrategia de memoria pruebas primero?
7. Tu agente puede ejecutar `transferir_dinero`. ¿Qué añades antes de
   desplegarlo, y dónde exactamente?
8. Un agente dio una respuesta rara en producción. ¿Qué necesitas haber
   registrado para poder averiguar por qué?
9. Te piden un sistema de cinco agentes. ¿Cuál es la primera pregunta que
   haces?

## Recursos

- [LangGraph — documentación](https://langchain-ai.github.io/langgraph/) —
  `doc-oficial` · `en` · `intermedio`. Empieza por los tutoriales: el modelo de
  estado se entiende mejor con el código delante.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. La escalera de complejidad de la sección
  1, contada por quienes la formalizaron. Léelo antes de elegir.
- [Tool use en la API de Claude](https://docs.anthropic.com/es/docs/build-with-claude/tool-use)
  — `doc-oficial` · `es` · `intermedio`. El ida y vuelta, con sus formatos.

## Siguiente

Módulo 10 · Agentes con CrewAI, el otro modelo de orquestación.
