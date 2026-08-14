# Módulo 11 · Proyecto final

> **Prerrequisitos:** toda la ruta<br>
> **Tiempo estimado:** 300 min<br>
> **Si ya dominas esto:** no hay siguiente: este es el final

Vas a construir **Guardia**, un asistente de conciliación: recibe los
movimientos que reporta el banco y los registros internos, dice qué cuadra y
qué no, marca lo que parece anómalo, y solo cuando hace falta juicio le
pregunta a un modelo.

Ese "solo cuando hace falta" es la tesis del proyecto y de la ruta entera.

## Qué vas a poder hacer al terminar

- Construir un sistema completo que combine código determinista y un modelo
- Decidir con criterio qué parte necesita juicio y cuál no
- Priorizar el gasto de un agente dentro de un presupuesto
- Cubrirlo con tests que corran sin red
- Documentar cómo se ejecuta y se despliega

## 1. El sistema, y por qué está dividido así

```text
   archivo del banco ─┐
                      ├─▶ [1] parsear ──▶ [2] conciliar ──▶ [3] detectar ──┐
   registros internos ─┘     (código)        (código)         (código)      │
                                                                            ▼
                                                              ┌──────── ¿hay algo raro
                                                              │         que no se explique
                                                              │         con las reglas?
                                                              │              │
                                                        no ◀──┘              │ sí
                                                         │                   ▼
                                                         │        [4] investigar (agente,
                                                         │             con tope y presupuesto)
                                                         ▼                   │
                                                   [5] informe ◀─────────────┘
                                                      (código)
```

Cuatro de las cinco etapas son código determinista. Solo la cuarta usa un
modelo, y solo se ejecuta cuando hay algo que las reglas no explican.

Esa proporción no es casualidad, es el criterio del módulo 09 aplicado:
**usa un modelo donde haga falta juicio y código donde haga falta certeza**.
Parsear, cruzar y contar son certezas. Explicar por qué una transferencia de
hace tres días aparece hoy con otro importe es juicio.

## 2. Lo que construyes en los ejercicios

Los cuatro ejercicios son el núcleo puro del sistema: las piezas sin efectos,
las que se prueban en milisegundos y sobre las que se apoya todo lo demás.

**Detección** — un motor de reglas. Cada regla es una función que mira una
transferencia y dice si salta. Que las reglas sean datos y no `if` incrustados
es lo que permite añadir una sin tocar el motor, y probarlas una por una.

**Priorización** — decidir qué discrepancias merecen la llamada cara. Es la
tesis del proyecto convertida en función: no todas las anomalías necesitan un
modelo, y el presupuesto se gasta en las que más importan.

**Informe** — convertir el resultado en un documento legible. Determinista y
ordenado: el mismo resultado produce el mismo texto, siempre. Sin eso no puedes
comparar el informe de hoy con el de ayer.

**Pipeline** — componer las etapas. Aquí la pieza clave es que el pipeline
recibe la detección y el renderizado **como argumentos**, en vez de importarlos.
Es la inyección que ya usaste con el reloj en el módulo 07: hace el pipeline
testeable sin montar el sistema entero, y te deja cambiar el motor de reglas sin
tocarlo.

## 3. Lo que construyes tú, más allá de los ejercicios

Los tests cubren el núcleo. El proyecto completo es tuyo, y estas son las
piezas que faltan, con el módulo donde viste cada una:

| Pieza | Qué hacer | Dónde lo viste |
|---|---|---|
| Lectura de archivos | Parsear CSV del banco a registros normalizados, fallando claro si falta un campo | 07 |
| Configuración | Umbrales de las reglas y claves desde el entorno, validados al arrancar | 04 |
| Registro | `logging` con nivel configurable y sin secretos | 04 |
| Agente investigador | Bucle con herramientas (`buscar_movimiento`, `historial_cuenta`) y **tope de pasos** | 09 |
| Herramientas | Descripción que diga cuándo usarlas, argumentos validados, solo lectura | 10 |
| Concurrencia | Investigar varias discrepancias a la vez, con semáforo y timeout | 06 |
| Reintentos | El modelo devuelve 429 o 529: espera creciente | 07 |
| Verificación | Comprobar con código que el informe no cita cifras inventadas | 10 |
| Interfaz | Un comando de consola, o un endpoint con FastAPI | 04, 07 |
| Tests | Unitarios del núcleo, y del agente con un modelo guionizado | 05, 09 |

### Criterios de aceptación

Cuando termines, tu proyecto debería cumplir esto — y son los mismos criterios
con los que se revisaría en un equipo:

- [ ] El pipeline completo corre **sin clave de API** si no hay discrepancias
      que investigar. El modelo es opcional, no un requisito para arrancar.
- [ ] Ningún importe se guarda ni se calcula en `float`.
- [ ] El agente investigador tiene tope de pasos y de presupuesto, y lo dice
      cuando se le acaba.
- [ ] Un campo obligatorio que falta en el archivo de entrada **detiene el
      proceso** con un mensaje que nombra el campo y **la línea**.
- [ ] Ninguna cifra del informe puede faltar en los datos de origen, y eso se
      comprueba con código, no con un modelo.
- [ ] Los tests del núcleo corren sin red y en menos de un segundo.
- [ ] El informe es determinista: dos ejecuciones sobre los mismos datos
      producen el mismo texto.
- [ ] Cada ejecución deja un registro con los pasos, los tokens y el motivo de
      terminación.
- [ ] Nada de claves en el repositorio; `.env.example` documenta cuáles hacen
      falta.

## 4. Cómo abordarlo, en orden

El error más común es empezar por el agente. Es lo más divertido y es lo último
que hay que hacer.

**Fase 1 — el pipeline determinista.** Parsear, conciliar, detectar e informar,
todo con tests. Al terminar tendrás un sistema que ya es útil y que no cuesta
nada ejecutar.

**Fase 2 — medir.** ¿Cuántas discrepancias quedan sin explicar por las reglas?
Ese número decide si el agente merece la pena. Si son dos por ejecución, un
humano las mira en cinco minutos y el agente no se paga. Si son cuarenta, sí.

**Fase 3 — el agente, acotado.** Herramientas de solo lectura, tope de pasos,
presupuesto, y solo para las discrepancias que la fase 2 dijo que lo merecen.

**Fase 4 — endurecer.** Reintentos, timeouts, concurrencia con semáforo,
verificación de cifras, registro. Es lo que separa una demo de algo que se
puede dejar corriendo por las noches.

Si te quedas en la fase 2 y concluyes que no hace falta agente, **eso también es
terminar el proyecto**. Es una conclusión de ingeniería válida, y probablemente
la más valiosa que enseña esta ruta.

## Caso real

Este proyecto está calcado de uno real, incluido cómo empezó mal.

La primera versión fue un sistema de cuatro agentes: uno leía el archivo, otro
cruzaba, otro detectaba anomalías y otro redactaba. Doce dólares por ejecución,
cuatro minutos, y resultados distintos cada vez sobre los mismos datos — lo que
hacía imposible saber si un cambio mejoraba algo.

Al desmontarlo, la pregunta fue la del módulo 09: **¿cuáles de estos pasos
necesitan juicio?** Leer un CSV, no. Cruzar referencias, no: es `&` y `-` sobre
conjuntos. Detectar anomalías, tampoco: eran cuatro umbrales. Redactar, casi
no. Investigar una discrepancia rara, sí.

La versión final hace cuatro etapas en código, con tests que corren en medio
segundo, y llama al modelo solo para las discrepancias que las reglas no
explican — que resultaron ser tres o cuatro por ejecución, no doscientas.
Céntimos, segundos, y un informe reproducible.

Lo que se ganó no fue solo dinero: se ganó **poder depurar**. Cuando el informe
sale raro, ahora se sabe si fue el parseo, la conciliación o el modelo, porque
las tres cosas están separadas y las dos primeras tienen tests.

## Ejercicios

```bash
uv run pytest ruta/11-proyecto-final
```

- **`ejercicios/base/deteccion.py`** — el motor de reglas, incluido qué hacer
  cuando una regla tiene un bug.
- **`ejercicios/base/informe.py`** — el informe, determinista y ordenado.
- **`ejercicios/base/priorizar.py`** — decidir qué discrepancias merecen la
  llamada cara, dentro de un presupuesto.
- **`ejercicios/reto/pipeline.py`** — componer las etapas con las piezas
  inyectadas.

## Resumen

- Usa un modelo donde haga falta juicio; usa código donde haga falta certeza.
- Empieza por el pipeline determinista y **mide** cuánto queda sin explicar.
  Sobre ese número decides si hace falta un agente.
- Concluir que no hace falta agente también es terminar el proyecto.
- Las reglas como datos, no como `if` incrustados: se añaden y se prueban una
  por una.
- Una regla con un bug no debe tumbar el proceso nocturno entero.
- El presupuesto se gasta en las anomalías que más importan, no en las
  primeras que aparecen.
- El informe determinista es lo que te deja comparar hoy con ayer.
- Ninguna cifra del informe puede faltar en los datos, y eso se comprueba con
  código.
- Inyecta las piezas en el pipeline: lo hace testeable sin montar el sistema.
- Todo agente lleva tope de pasos y de presupuesto.
- El sistema debe arrancar y ser útil sin clave de API.
- Separar las etapas es lo que te permite saber cuál falló.

## Preguntas de repaso

1. ¿Por qué empezar por el agente es el error más común de este proyecto?
2. Terminas la fase 1 y quedan dos discrepancias sin explicar por ejecución.
   ¿Montas el agente?
3. Una de tus reglas de detección lanza una excepción a las tres de la mañana.
   ¿Qué debería pasar con las otras reglas y con el informe?
4. Tienes presupuesto para tres investigaciones y hay ocho anomalías. ¿Cómo
   eliges?
5. ¿Qué ganas haciendo que el informe sea determinista?
6. ¿Por qué el pipeline recibe `detect` y `render` como argumentos en vez de
   importarlos?
7. Tu redactor cita una cifra que no está en los datos. ¿Pones otro modelo a
   revisarlo?
8. Tu sistema tarda cuatro minutos y cuesta doce dólares por ejecución. ¿Cuál
   es la primera pregunta que te haces?
9. ¿Cómo pruebas el agente investigador sin gastar tokens?

## Recursos

- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. Vuelve a leerlo ahora: dice cosas
  distintas cuando ya has construido uno.
- [`csv` — biblioteca estándar](https://docs.python.org/es/3/library/csv.html)
  — `doc-oficial` · `es` · `principiante`. Para la etapa de parseo; no hace
  falta pandas para leer un archivo de movimientos.
- [`argparse`](https://docs.python.org/es/3/library/argparse.html) —
  `doc-oficial` · `es` · `intermedio`. Para la interfaz de consola, sin
  dependencias.
- [Documentación de la API de Claude](https://docs.anthropic.com/es/api/) —
  `doc-oficial` · `es` · `intermedio`. Para la etapa de investigación.

## Siguiente

Se acabó la ruta. Si algo de lo que has escrito aquí te parece que le serviría
a quien venga detrás, [CONTRIBUTING.md](../../CONTRIBUTING.md) explica cómo
subirlo.
