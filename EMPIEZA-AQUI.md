# Empieza aquí

Este repositorio sirve a gente con niveles muy distintos. En vez de hacerte
recorrer módulos que ya dominas, respóndete estas preguntas con honestidad.

No hay nota ni te evalúa nadie. Mentirte aquí solo te hace perder tiempo
después.

## Cómo funciona

Ve bajando. En cuanto respondas **"no"** a una pregunta, ese es tu módulo de
entrada. Empieza ahí.

Los doce módulos tienen contenido, ejercicios y tests. Puedes hacerlos en orden
o entrar por donde te toque: cada guía dice qué asume que ya sabes.

!!! tip "Antes de la primera pregunta"

    Si programas en otro lenguaje y vienes a Python, el
    [módulo 00](ruta/00-como-piensa-python/GUIA.md) no cubre sintaxis: cubre
    los cinco modelos mentales con los que se razona en este lenguaje. Es corto
    y ahorra bastante desconcierto más adelante.

## Las preguntas

**1. ¿Has escrito alguna vez código en cualquier lenguaje?**
Si no → empieza en el [módulo 01](ruta/01-fundamentos/GUIA.md). Está escrito
para alguien que nunca ha programado.

**2. ¿Puedes escribir de memoria una función en Python que reciba una lista y
devuelva su media, lanzando un error si está vacía?**
Si no → [módulo 01 · Fundamentos](ruta/01-fundamentos/GUIA.md)

**3. ¿Sabes explicar qué hace `{k: v for k, v in pares if v > 0}` sin
buscarlo?**
Si no → [módulo 02 · Estructuras de datos](ruta/02-estructuras-de-datos/GUIA.md)

**4. ¿Sabes cuándo usar un `set` en vez de una `list`, y por qué?**
Si no → [módulo 02 · Estructuras de datos](ruta/02-estructuras-de-datos/GUIA.md)

**5. ¿Has escrito una clase con `__init__` y sabes qué aporta `@dataclass`?**
Si no → [módulo 03 · POO y módulos](ruta/03-poo-y-modulos/GUIA.md)

**6. ¿Has creado un entorno virtual y gestionado dependencias de un proyecto?**
Si no → [módulo 04 · Entorno y herramientas](ruta/04-entorno-y-herramientas/GUIA.md)

**7. ¿Has escrito tests con pytest, incluyendo alguna fixture?**
Si no → [módulo 05 · Testing](ruta/05-testing/GUIA.md)

**8. ¿Sabes qué hace `await` y por qué `async` no acelera un cálculo pesado?**
Si no → [módulo 06 · Async y concurrencia](ruta/06-async-y-concurrencia/GUIA.md)

**9. ¿Has consumido una API REST desde Python y validado la respuesta?**
Si no → [módulo 07 · Datos y APIs](ruta/07-datos-y-apis/GUIA.md)

**10. ¿Has llamado a un LLM desde código y manejado tool use?**
Si no → [módulo 08 · Fundamentos de LLMs](ruta/08-llms-fundamentos/GUIA.md)

**¿Respondiste que sí a todas?**
Vete directo a [LangGraph](ruta/09-agentes-langgraph/GUIA.md) y
[CrewAI](ruta/10-agentes-crewai/GUIA.md), que es a donde va esta ruta. Y si
también los conoces, el [proyecto final](ruta/11-proyecto-final/GUIA.md) es
donde se junta todo.

## Si vas sobrado en tu módulo

Cada guía abre diciendo sus prerrequisitos y a dónde saltar si ya dominas el
tema. Y cada módulo tiene ejercicios en `ejercicios/reto/` además de los de
`ejercicios/base/`: si los de base te resultan triviales, haz solo los retos.

## Si te quedas atascado

En `soluciones/` está la versión de referencia de cada ejercicio. Míralas
**después** de intentarlo, no antes: leer una solución da la sensación de haber
aprendido sin haber aprendido.

Si crees que la guía está equivocada o poco clara, probablemente tengas razón —
quien está aprendiendo es quien detecta esos fallos. Abre un issue de tipo
*error en una guía*; no hace falta que sepas cuál es el arreglo.
