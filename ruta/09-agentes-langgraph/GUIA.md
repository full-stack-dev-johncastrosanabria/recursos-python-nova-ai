# Módulo 09 · Agentes con LangGraph

> **Prerrequisitos:** módulos 01-08
> **Tiempo estimado:** 180 min
> **Si ya dominas esto:** salta al módulo 10

En el módulo 08 el modelo te pedía llamar a una herramienta y tú se lo
resolvías. Si eso se repite —pedir, ejecutar, volver a preguntar— ya tienes un
agente. Este módulo va de darle estructura a ese bucle.

Y empieza con una advertencia que conviene tomarse en serio: **la mayoría de
los flujos no necesitan un framework de agentes**. Vas a aprender el modelo de
LangGraph, y también cuándo el código plano del módulo 08 era suficiente.

## Qué vas a poder hacer al terminar

- Modelar un flujo como grafo de estado
- Definir nodos y transiciones condicionales
- Persistir estado con checkpoints
- Insertar un paso de human-in-the-loop

## 1. El bucle de agente, sin framework

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

## 2. El modelo de LangGraph: un grafo de estado

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

## 3. Nodos, aristas y transiciones condicionales

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

## 4. Ciclos y presupuesto

El ciclo `pensar → herramienta → pensar` es lo que hace útil a un agente, y
también lo que puede salir caro. Dos protecciones:

```python
app.invoke(estado_inicial, {"recursion_limit": 25})
```

Y además, una condición de salida en tu propia lógica —por número de pasos, por
tokens gastados o por tiempo— porque el límite del framework te salva del
bucle infinito, no de gastar veinte llamadas para algo que debía costar dos.

## 5. Checkpoints y human-in-the-loop

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
enviar— ese punto de control no es opcional. Un modelo puede equivocarse; un
modelo con permiso para transferir y sin supervisión puede equivocarse caro.

## 6. Cuándo NO usar un framework

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
- **`ejercicios/reto/ciclo.py`** — el bucle de agente completo, con un modelo
  de mentira que responde según un guion.

## Resumen

- Un agente es un bucle: el modelo pide, tú ejecutas, le devuelves el
  resultado. Diecisiete líneas sin framework.
- Todo bucle de agente lleva tope de pasos. Sin él, un modelo confundido gasta
  hasta que alguien lo mira.
- Un grafo de LangGraph es un pliegue sobre un estado: nodos como transiciones
  y reducers acumulando.
- Un nodo devuelve una **actualización**, no el estado entero; por eso los
  nodos no necesitan conocerse.
- Las claves con reducer acumulan; las que no tienen, se reemplazan.
- La función que decide la siguiente arista es código normal y se prueba sin
  modelo ni red.
- Los checkpoints dan continuidad entre peticiones, reanudación y el punto
  donde para un humano. Para acciones con consecuencias, no es opcional.
- Adopta el framework con evidencia de que se paga, no por costumbre.
- Cada agente extra multiplica coste, latencia e imprevisibilidad.

## Preguntas de repaso

1. ¿Por qué todo bucle de agente necesita un tope de pasos?
2. Un nodo devuelve `{"messages": [uno]}`. ¿Se pierden los mensajes anteriores?
   ¿De qué depende?
3. ¿Qué parte de un grafo se puede probar sin modelo ni red?
4. Tu agente puede ejecutar `transferir_dinero`. ¿Qué añades antes de
   desplegarlo?
5. Un flujo tiene tres pasos en cadena y ninguna rama. ¿Framework o código
   plano?
6. Te piden un sistema de cinco agentes. ¿Cuál es la primera pregunta que
   haces?

## Recursos

- [LangGraph — documentación](https://langchain-ai.github.io/langgraph/) —
  `doc-oficial` · `en` · `intermedio`. Empieza por los tutoriales: el modelo de
  estado se entiende mejor con el código delante.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. La escalera de complejidad: cadena,
  routing, paralelo, orquestador, agente. Léelo antes de elegir.
- [Tool use en la API de Claude](https://docs.anthropic.com/es/docs/build-with-claude/tool-use)
  — `doc-oficial` · `es` · `intermedio`. El ida y vuelta, con sus formatos.

## Siguiente

Módulo 10 · Agentes con CrewAI, el otro modelo de orquestación.
