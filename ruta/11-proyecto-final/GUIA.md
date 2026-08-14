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

- Construir un agente que resuelva un problema real de Nova AI
- Cubrirlo con tests
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
                                                         │             con tope de pasos)
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

Los tres ejercicios son el núcleo puro del sistema: las piezas sin efectos, las
que se prueban en milisegundos y sobre las que se apoya todo lo demás.

**Detección** — un motor de reglas. Cada regla es una función que mira una
transferencia y dice si salta. Que las reglas sean datos y no `if` incrustados
es lo que permite añadir una sin tocar el motor, y probarlas una por una.

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
| Agente investigador | Bucle con herramientas (`buscar_movimiento`, `historial_cuenta`) y **tope de pasos** | 09 |
| Concurrencia | Investigar varias discrepancias a la vez, con semáforo | 06 |
| Reintentos | El modelo devuelve 429 o 529: espera creciente | 07 |
| Interfaz | Un comando de consola, o un endpoint con FastAPI | 07 |
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
      proceso** con un mensaje que nombra el campo y la línea.
- [ ] Los tests del núcleo corren sin red y en menos de un segundo.
- [ ] El informe es determinista: dos ejecuciones sobre los mismos datos
      producen el mismo texto.
- [ ] Nada de claves en el repositorio; `.env.example` documenta cuáles hacen
      falta.

## 4. El error que más se comete en este proyecto

Empezar por el agente.

Es lo más divertido y es lo último que hay que hacer. Si empiezas por ahí,
acabas con un sistema donde el modelo hace cosas que una intersección de
conjuntos resolvía —y encima con incertidumbre y coste—, y donde no puedes
distinguir un fallo de tus datos de un fallo del modelo.

El orden que funciona: parsear, conciliar, detectar e informar, **todo con
tests**, y comprobar cuántas discrepancias quedan sin explicar. Sobre ese
número decides si el agente merece la pena. A veces la respuesta es que no, y
esa también es una conclusión de ingeniería válida.

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
- **`ejercicios/reto/pipeline.py`** — componer las etapas con las piezas
  inyectadas.

## Resumen

- Usa un modelo donde haga falta juicio; usa código donde haga falta certeza.
- Empieza por el pipeline determinista y mide cuánto queda sin explicar. Sobre
  ese número decides si hace falta un agente.
- Las reglas como datos, no como `if` incrustados: se añaden y se prueban una
  por una.
- Una regla con un bug no debe tumbar el proceso nocturno entero.
- El informe determinista es lo que te deja comparar hoy con ayer.
- Inyecta las piezas en el pipeline: lo hace testeable sin montar el sistema.
- Todo agente lleva tope de pasos y de presupuesto.
- El sistema debe arrancar y ser útil sin clave de API.
- Separar las etapas es lo que te permite saber cuál falló.

## Preguntas de repaso

1. ¿Por qué empezar por el agente es el error más común de este proyecto?
2. Una de tus reglas de detección lanza una excepción a las tres de la mañana.
   ¿Qué debería pasar con las otras reglas y con el informe?
3. ¿Qué ganas haciendo que el informe sea determinista?
4. ¿Por qué el pipeline recibe `detect` y `render` como argumentos en vez de
   importarlos?
5. Tu sistema tarda cuatro minutos y cuesta doce dólares por ejecución. ¿Cuál
   es la primera pregunta que te haces?
6. ¿Cómo pruebas el agente investigador sin gastar tokens?

## Recursos

- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. Vuelve a leerlo ahora: dice cosas
  distintas cuando ya has construido uno.
- [`csv` — biblioteca estándar](https://docs.python.org/es/3/library/csv.html)
  — `doc-oficial` · `es` · `principiante`. Para la etapa de parseo; no hace
  falta pandas para leer un archivo de movimientos.
- [Documentación de la API de Claude](https://docs.anthropic.com/es/api/) —
  `doc-oficial` · `es` · `intermedio`. Para la etapa de investigación.

## Siguiente

Se acabó la ruta. Si algo de lo que has escrito aquí te parece que le serviría
a quien venga detrás, [CONTRIBUTING.md](../../CONTRIBUTING.md) explica cómo
subirlo.
