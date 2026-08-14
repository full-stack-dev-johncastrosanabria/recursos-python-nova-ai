# Módulo 10 · Agentes con CrewAI

> **Prerrequisitos:** módulos 01-08, y el 09 si quieres comparar ambos enfoques<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 11

CrewAI es el otro modelo de orquestación. Donde LangGraph piensa en máquinas de
estado, CrewAI piensa en **equipos**: agentes con un rol, un objetivo y unas
herramientas, que se van pasando el trabajo.

Los dos resuelven el mismo problema con metáforas distintas. Entender la
diferencia —y cuándo ninguno de los dos hace falta— es el objetivo del módulo.

## Qué vas a poder hacer al terminar

- Definir agentes con rol, objetivo y contexto
- Componer tareas y encadenarlas
- Diseñar herramientas que un modelo sepa usar
- Delegar trabajo entre agentes
- Poner barreras de seguridad a lo que un agente puede hacer
- Verificar con código lo que un modelo produce
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

El criterio para elegir jerárquico: cuando **no sabes de antemano** qué
subtareas hacen falta. Si las sabes, el secuencial las expresa mejor y te deja
probarlas una a una.

## 3. Diseñar herramientas que un modelo sepa usar

Una herramienta mal diseñada es la causa número uno de que un agente se
comporte de forma errática. Cinco reglas:

**Un nombre que diga qué hace.** `get_account_balance` gana a `query` y a
`do_lookup`. El modelo elige por el nombre antes que por nada.

**Una descripción que diga cuándo usarla, no solo qué hace.** Añade el caso de
uso y, si hace falta, cuándo *no* usarla:

```text
Devuelve el saldo actual de una cuenta. Úsala cuando necesites saber si hay
fondos suficientes. No sirve para el histórico de movimientos: para eso está
get_account_history.
```

**Parámetros pocos y planos.** Un objeto anidado de cuatro niveles es una
invitación a que el modelo se equivoque. Si tu herramienta necesita quince
argumentos, probablemente son tres herramientas.

**Errores que enseñan.** Cuando la herramienta falla, el mensaje que le
devuelves al modelo es su única pista para corregirse:

```python
# Inútil:   "Error"
# Útil:     "La cuenta CR1-0002 no tiene el formato CRnn-nnnn. Ejemplo: CR01-0002."
```

**Salidas acotadas.** Devolver diez mil filas llena la ventana de contexto y
tapa la señal. Devuelve lo relevante, paginado si hace falta, y dile al modelo
cuántas quedan.

## 4. Barreras: lo que un agente no puede hacer

Un agente con herramientas es código que decide qué ejecutar. Las tres barreras
que no son opcionales:

**Separar lectura de escritura.** Las herramientas que solo consultan pueden
ejecutarse libremente; las que modifican algo necesitan aprobación explícita o
una lista de comprobaciones previas. Esa distinción se diseña desde el
principio, no se parchea después.

**Validar los argumentos en la frontera.** Lo que llega del modelo es entrada no
confiable, exactamente igual que un payload de red. Es la lección del módulo 07,
y aquí se aplica sobre la propia herramienta:

```python
def transferir(cuenta_destino: str, monto_cents: int) -> dict:
    validate_account(cuenta_destino)          # el validador del módulo 05
    if monto_cents > LIMITE_SIN_APROBACION:
        raise NeedsApproval(f"{monto_cents} supera el límite automático")
    ...
```

**Presupuesto y tope.** Pasos, tokens y tiempo, como en el módulo 09. Un agente
sin presupuesto es una factura abierta.

Y una regla de fondo: **el radio de daño de una herramienta debe ser el mínimo
que resuelva el problema**. Si el agente solo necesita leer transferencias del
último mes, la herramienta no debería poder leer las de hace tres años ni las de
otro cliente.

## 5. Especialización: por qué varios agentes y no uno

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
invenciones cuando el resultado importa — pero con una advertencia enorme, que
es la sección siguiente.

## 6. Verificar con código, no con otro modelo

El patrón generador-verificador tiene una trampa que se ve poco: **si el
verificador también es un LLM, hereda la misma clase de fallos que intenta
atrapar**. Un modelo que revisa cifras puede aprobar una cifra inventada,
porque "parece razonable" es exactamente el criterio con el que se inventó.

La regla que se deriva: **verifica con código todo lo que se pueda verificar
con código**.

```python
def numeros_no_respaldados(texto: str, datos: dict) -> list[str]:
    """Devuelve los números del texto que no aparecen en los datos de origen."""
    permitidos = {str(v) for v in datos.values()}
    return [n for n in re.findall(r"\d[\d,.]*", texto) if n not in permitidos]
```

Eso es determinista, cuesta cero y no se equivoca. Y convierte "el redactor
inventó una cifra" —un problema de juicio, imposible de garantizar— en "el
informe contiene un número que no está en los datos" — una comprobación.

Es tu reto `verificador`, y es la pieza que arregló el caso real de este módulo.

Deja el modelo como verificador solo para lo que de verdad no se puede
comprobar: tono, coherencia del discurso, si una explicación se entiende.

## 7. El criterio, dicho sin adornos

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
umbral. Redactar sí se beneficia de un modelo. Y revisar cifras es comparar
números — hacerlo con un modelo era precisamente **por qué** las cifras
inventadas pasaban el filtro: el verificador tenía el mismo defecto que el
generador.

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
- **`ejercicios/reto/verificador.py`** — comprobar con código que un texto no
  contiene cifras inventadas. Es la pieza que arregló el caso real.

## Resumen

- CrewAI modela equipos: agentes con rol, objetivo y herramientas que se pasan
  trabajo; LangGraph modela máquinas de estado.
- `role`, `goal` y `backstory` acaban en el prompt: no son decoración.
- `expected_output` estabiliza lo que recibe la tarea siguiente.
- Secuencial es predecible; jerárquico solo si no sabes de antemano qué
  subtareas hacen falta.
- Una herramienta se diseña: nombre que dice qué hace, descripción que dice
  cuándo usarla, pocos parámetros planos, errores que enseñan y salidas
  acotadas.
- Separa herramientas de lectura y de escritura, valida sus argumentos como
  entrada no confiable, y dale a cada una el radio de daño mínimo.
- Se divide en varios agentes porque uno con demasiadas herramientas se vuelve
  errático, no porque quede elegante.
- **Un verificador que también es un LLM hereda los fallos que intenta
  atrapar.** Verifica con código todo lo que se pueda verificar con código.
- Cada agente multiplica coste, latencia e imprevisibilidad.
- Usa un modelo donde haga falta juicio y código donde haga falta certeza.

## Preguntas de repaso

1. ¿Por qué `backstory` cambia el comportamiento de un agente?
2. Tienes cinco agentes en cadena. ¿Qué le pasa a la latencia y por qué?
3. Tu agente elige mal entre dos herramientas parecidas. ¿Qué miras primero?
4. ¿Qué le devuelves a un modelo cuando su herramienta falla, y por qué importa
   el contenido de ese mensaje?
5. ¿Cuál es el argumento técnico —no estético— para dividir en varios agentes?
6. Un agente verificador revisa las cifras de un informe y aun así se cuelan
   inventadas. ¿Qué cambiarías?
7. Tu agente tiene una herramienta que puede leer cualquier transferencia de
   cualquier cliente. ¿Qué problema ves?
8. Proceso secuencial o jerárquico para un flujo de tres pasos fijos. ¿Cuál y
   por qué?
9. ¿Cuándo elegirías LangGraph antes que CrewAI?

## Recursos

- [CrewAI — documentación](https://docs.crewai.com/) — `doc-oficial` · `en` ·
  `intermedio`. Los conceptos de agente, tarea y crew, con ejemplos que corren.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. La escalera de complejidad. Es el mejor
  antídoto contra montar cinco agentes para lo que resuelve una función.
- [Tool use en la API de Claude](https://docs.anthropic.com/es/docs/build-with-claude/tool-use)
  — `doc-oficial` · `es` · `intermedio`. Cómo se describen las herramientas y
  qué formato tienen los resultados.

## Siguiente

Módulo 11 · Proyecto final, donde se junta todo.
