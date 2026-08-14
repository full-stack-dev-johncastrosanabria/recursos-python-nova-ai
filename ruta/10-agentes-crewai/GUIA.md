# Módulo 10 · Agentes con CrewAI

> **Prerrequisitos:** módulos 01-08, y el 09 si quieres comparar ambos enfoques<br>
> **Tiempo estimado:** 180 min<br>
> **Si ya dominas esto:** salta al módulo 11

CrewAI es el otro modelo de orquestación. Donde LangGraph piensa en máquinas de
estado, CrewAI piensa en **equipos**: agentes con un rol, un objetivo y unas
herramientas, que se van pasando el trabajo.

Los dos resuelven el mismo problema con metáforas distintas. Entender la
diferencia —y cuándo ninguno de los dos hace falta— es el objetivo del módulo.

## Qué vas a poder hacer al terminar

- Definir agentes con rol, objetivo y contexto
- Componer tareas y encadenarlas
- Delegar trabajo entre agentes
- Contrastar el modelo de CrewAI con el de LangGraph

## 1. El modelo: roles, tareas y una tripulación

```python
from crewai import Agent, Task, Crew

investigador = Agent(
    role="Analista de conciliación",
    goal="Encontrar por qué una transferencia no cuadra",
    backstory="Llevas años cerrando cierres contables en banca.",
    tools=[buscar_movimiento, consultar_historial],
)

redactor = Agent(
    role="Redactor de informes",
    goal="Explicar los hallazgos en lenguaje claro para el equipo financiero",
    backstory="Traduces jerga técnica a decisiones de negocio.",
    tools=[],
)

investigar = Task(
    description="Investiga la discrepancia de la referencia {ref}",
    expected_output="Una explicación de la causa probable, con evidencia",
    agent=investigador,
)

redactar = Task(
    description="Redacta el informe para el equipo financiero",
    expected_output="Un resumen de tres párrafos, sin jerga",
    agent=redactor,
    context=[investigar],          # recibe la salida de la tarea anterior
)

crew = Crew(agents=[investigador, redactor], tasks=[investigar, redactar])
resultado = crew.kickoff(inputs={"ref": "TR-0042"})
```

Las tres piezas y para qué sirve cada una:

**El agente** es un rol con herramientas. `role`, `goal` y `backstory` no son
adorno: acaban en el prompt del sistema y son lo que hace que el agente se
comporte como un analista y no como un asistente genérico.

**La tarea** es una unidad de trabajo con un resultado esperado.
`expected_output` importa más de lo que parece: sin él, el agente decide por su
cuenta qué formato entregar, y la siguiente tarea recibe algo distinto cada vez.

**El `context`** es cómo se encadenan: la salida de una tarea entra como
contexto de la siguiente. Ese encadenamiento es el corazón del modelo, y es lo
que vas a implementar.

## 2. Secuencial o jerárquico

```python
crew = Crew(agents=[...], tasks=[...], process=Process.sequential)
```

En **secuencial**, las tareas se ejecutan en orden y cada una recibe lo que
produjeron las anteriores. Es predecible, barato de razonar y suficiente para
la mayoría de los casos.

En **jerárquico**, un agente gestor decide qué delegar y a quién. Suena
atractivo y conviene mirarlo con desconfianza: añade una llamada al modelo por
cada decisión de delegación, y esas decisiones también se pueden equivocar. Un
`if` en Python no se equivoca ni cuesta tokens.

## 3. Especialización: por qué varios agentes y no uno

El argumento de fondo a favor de dividir no es que quede elegante. Es que **un
agente con demasiadas herramientas y un prompt gigante se vuelve errático**:
elige mal la herramienta, se confunde de objetivo, se distrae. Es el principio
de responsabilidad única del módulo 03 aplicado a agentes, forzado además por
un límite físico — la ventana de contexto.

Los tres patrones que justifican tener más de uno:

**Especialización con contexto acotado.** Cada agente ve solo lo suyo y tiene
solo las herramientas que necesita. Es el que más veces se paga.

**Orquestador y trabajadores.** Uno descompone la tarea, otros la ejecutan en
paralelo, el primero integra. Útil cuando las subtareas son de verdad
independientes.

**Generador y verificador.** Uno produce, otro revisa. Sirve para acotar
invenciones cuando el resultado importa — pero recuerda que el verificador
también es un modelo que puede equivocarse.

## 4. El criterio, dicho sin adornos

Cada agente que añades multiplica tres cosas: **coste** (una llamada más por
paso), **latencia** (en serie, se suman) e **imprevisibilidad** (un modelo no
determinista más). Y la coordinación entre ellos es superficie de fallo nueva.

La disciplina que se deriva: **el mínimo número de agentes que resuelva el
problema**. La mayoría de las tareas que se plantean como "sistema multiagente"
son una cadena determinista con una o dos llamadas a modelo en los puntos donde
de verdad hace falta juicio.

Y para elegir entre los dos frameworks:

| | CrewAI | LangGraph |
|---|---|---|
| Metáfora | equipo con roles | máquina de estados |
| Flujo | lineal o jerárquico | grafo con ramas y ciclos |
| Punto fuerte | prototipar rápido | control y auditabilidad |
| Encaja cuando | la tarea se divide en roles claros | el flujo tiene estructura compleja |

Para un sistema en producción que toca datos reales, la auditabilidad suele
pesar más: poder mirar el grafo, probar cada transición y saber por qué se tomó
un camino. Para explorar una idea en una tarde, el modelo de roles va más
rápido.

## Caso real

Un equipo montó una tripulación de cinco agentes para generar el informe
semanal: uno extraía datos, otro calculaba métricas, otro buscaba anomalías,
otro redactaba y otro revisaba.

Funcionaba, y tenía dos problemas. Costaba unos doce dólares por informe
semanal, y una vez de cada cinco el agente redactor inventaba una cifra que no
estaba en los datos.

Al desmontarlo, la pregunta de siempre: **¿cuáles de estos cinco pasos
necesitan juicio?** Extraer datos es una consulta SQL. Calcular métricas es
aritmética. Buscar anomalías, tal como estaba definido, eran tres reglas de
umbral. Redactar sí se beneficia de un modelo. Revisar cifras es comparar
números — y hacerlo con un modelo era precisamente por qué las cifras
inventadas pasaban el filtro.

La versión final: cuatro pasos deterministas y **un agente redactor** que
recibe las cifras ya calculadas y tiene prohibido inventarlas, más una
verificación final en código que comprueba que todo número del texto aparece en
los datos de entrada. Céntimos por informe, y cero cifras inventadas — porque
la verificación dejó de ser un juicio y pasó a ser una comprobación.

La moraleja del módulo, y de la ruta entera: **el sistema multiagente elegante
de la demo suele ser el sistema frágil y caro de producción**. Usa un modelo
donde haga falta juicio; usa código donde haga falta certeza.

## Ejercicios

```bash
uv run pytest ruta/10-agentes-crewai
```

Como en el módulo 09, implementas el modelo, no el framework: sin instalar nada
ni gastar tokens.

- **`ejercicios/base/asignacion.py`** — elegir qué agente hace una tarea según
  las herramientas que requiere, prefiriendo al más especializado.
- **`ejercicios/base/equipo.py`** — encadenar tareas pasando el contexto
  acumulado, que es el corazón del modelo de CrewAI.
- **`ejercicios/reto/presupuesto.py`** — un orquestador que se detiene cuando
  se le acaba el presupuesto, y dice qué quedó sin hacer.

## Resumen

- CrewAI modela equipos: agentes con rol, objetivo y herramientas que se pasan
  trabajo; LangGraph modela máquinas de estado.
- `role`, `goal` y `backstory` acaban en el prompt: no son decoración.
- `expected_output` estabiliza lo que recibe la tarea siguiente.
- El `context` encadena tareas. Secuencial es predecible; jerárquico añade una
  llamada al modelo por cada decisión de delegación.
- Se divide en varios agentes porque uno con demasiadas herramientas se vuelve
  errático, no porque quede elegante.
- Cada agente multiplica coste, latencia e imprevisibilidad.
- Usa un modelo donde haga falta juicio y código donde haga falta certeza.
- Para producción con datos reales, la auditabilidad de un grafo suele pesar
  más que la velocidad de prototipo de los roles.

## Preguntas de repaso

1. ¿Por qué `backstory` cambia el comportamiento de un agente?
2. Tienes cinco agentes en cadena. ¿Qué le pasa a la latencia y por qué?
3. ¿Cuál es el argumento técnico —no estético— para dividir en varios agentes?
4. Un agente verificador revisa las cifras de un informe y aun así se cuelan
   inventadas. ¿Qué cambiarías?
5. Proceso secuencial o jerárquico para un flujo de tres pasos fijos. ¿Cuál y
   por qué?
6. ¿Cuándo elegirías LangGraph antes que CrewAI?

## Recursos

- [CrewAI — documentación](https://docs.crewai.com/) — `doc-oficial` · `en` ·
  `intermedio`. Los conceptos de agente, tarea y crew, con ejemplos que corren.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. La escalera de complejidad. Es el mejor
  antídoto contra montar cinco agentes para lo que resuelve una función.

## Siguiente

Módulo 11 · Proyecto final, donde se junta todo.
