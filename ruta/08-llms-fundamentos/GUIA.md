# Módulo 08 · Fundamentos de LLMs

> **Prerrequisitos:** módulos 01-07<br>
> **Tiempo estimado:** 150 min<br>
> **Si ya dominas esto:** salta al módulo 09

A partir de aquí la ruta cambia de tema, pero no de método. Un LLM es una
dependencia externa más: lenta, cara, no determinista y con una API. Todo lo
del módulo 07 —validar en la frontera, timeouts, reintentos, paginación— aplica
igual, y ahora además hay que lidiar con que la respuesta no sea la misma dos
veces.

## Qué vas a poder hacer al terminar

- Llamar a un modelo con el SDK de Claude
- Escribir prompts que den resultados repetibles
- Definir herramientas y manejar tool use
- Obtener salida estructurada y validarla
- Montar un RAG básico

## 1. La llamada mínima

```python
import anthropic

client = anthropic.Anthropic()   # lee ANTHROPIC_API_KEY del entorno

respuesta = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="Eres un asistente de conciliación bancaria. Responde en español.",
    messages=[
        {"role": "user", "content": "¿Qué es una transferencia sin contraparte?"}
    ],
)

print(respuesta.content[0].text)
```

Cuatro cosas que conviene fijar desde el principio:

**El `system` va aparte, no dentro de `messages`.** Es donde se define el rol y
las reglas. Los mensajes son la conversación.

**La conversación no tiene memoria.** El modelo no recuerda nada entre
llamadas: en cada petición le mandas el historial completo. Toda la "memoria"
de un chatbot la construyes tú.

**`max_tokens` es un límite de salida**, no un objetivo. Si se agota, la
respuesta se corta a media frase — y hay que comprobarlo (`stop_reason`).

**Pagas por tokens de entrada y de salida.** Como el historial se reenvía
entero en cada turno, una conversación larga cuesta cada vez más. De ahí que el
primer ejercicio sea recortarlo.

## 2. Tokens y ventana de contexto

El modelo no ve caracteres ni palabras: ve **tokens**, trozos de texto de unos
cuatro caracteres de media en inglés y algo menos en español. La **ventana de
contexto** es cuántos tokens caben entre entrada y salida.

Consecuencias prácticas:

- Un documento largo no cabe. Por eso existe el RAG: en vez de mandarlo entero,
  se buscan los trozos relevantes y se mandan solo esos.
- El historial de una conversación crece hasta no caber. Hay que recortarlo, y
  la estrategia importa: quitar los mensajes más viejos es lo simple, pero el
  mensaje de sistema **nunca** se recorta.
- Contar tokens con `len(texto) / 4` es una aproximación de servilleta, útil
  para presupuestar y nada más.

## 3. Prompts que dan resultados repetibles

Un prompt no es una conversación con un humano; es una especificación.

```python
system = """Eres un clasificador de transferencias.

Clasifica cada transferencia en exactamente una categoría:
- NOMINA: pagos periódicos de salario
- PROVEEDOR: pagos a empresas por servicios
- PERSONAL: transferencias entre personas físicas
- DESCONOCIDA: no hay información suficiente

Responde únicamente con la categoría, en mayúsculas, sin explicación."""
```

Lo que hace que funcione: el rol es explícito, las categorías son cerradas,
hay una salida para el caso "no sé" (sin ella el modelo inventará una
categoría) y el formato de respuesta está acotado.

**`temperature`** controla cuánto se aparta el modelo de lo más probable. Para
clasificar, extraer o cualquier cosa que quieras repetible, `temperature=0`.
Para redactar o proponer ideas, más alta. Y aun con cero, la salida **no está
garantizada** idéntica: no lo trates como una función pura.

## 4. Tool use: cuando el modelo decide llamar a tu código

```python
tools = [
    {
        "name": "get_balance",
        "description": "Devuelve el saldo en céntimos de una cuenta",
        "input_schema": {
            "type": "object",
            "properties": {
                "account": {
                    "type": "string",
                    "description": "Número de cuenta, formato CRnn-nnnn",
                }
            },
            "required": ["account"],
        },
    }
]
```

El modelo no ejecuta nada: **decide** que quiere llamar a `get_balance` con
ciertos argumentos y te lo dice. Tú ejecutas, y le devuelves el resultado como
un mensaje nuevo. Ese ida y vuelta es el bucle de agente del módulo 09.

Dos avisos que valen dinero real:

- **La `description` es el prompt de la herramienta.** Una descripción vaga
  hace que el modelo la use cuando no toca, o no la use cuando sí. Es donde más
  se gana afinando.
- **Nunca ejecutes a ciegas lo que el modelo pida.** Los argumentos que llegan
  son entrada no confiable, exactamente igual que un payload de red. Valídalos
  en la frontera. Un modelo puede pedirte `delete_account` porque un texto que
  leyó se lo sugirió.

## 5. Salida estructurada

Pedir "responde en JSON" y esperar lo mejor es frágil. Lo robusto es usar el
propio mecanismo de herramientas para forzar la forma, o validar lo que llegue:

```python
import json
from pydantic import BaseModel, ValidationError

class Clasificacion(BaseModel):
    categoria: str
    confianza: float

try:
    resultado = Clasificacion.model_validate_json(respuesta_texto)
except (json.JSONDecodeError, ValidationError):
    ...   # reintentar, degradar, o registrar: pero nunca seguir con basura
```

Es la frontera del módulo 07 otra vez, y aquí importa más: la salida de un LLM
es, por definición, no confiable.

## 6. RAG en dos párrafos

Cuando el conocimiento no cabe en el prompt: se trocea el corpus, se convierte
cada trozo en un vector (*embedding*), se guardan, y en cada pregunta se buscan
los trozos más parecidos y se mandan como contexto.

```text
documentos → trocear → embeddings → índice
                                       │
pregunta → embedding → buscar los k más cercanos → prompt con esos trozos → LLM
```

El paso que más determina la calidad es el primero, y es el menos glamuroso:
**cómo troceas**. Trozos muy grandes traen ruido; muy pequeños pierden el
contexto que daba sentido a la frase. Por eso se usa solapamiento: cada trozo
repite el final del anterior para que una idea partida por la mitad siga
completa en alguno de los dos. Ese es tu reto de este módulo.

## 7. Lo que hay que aceptar

- **No es determinista.** No lo pruebes con `assert respuesta == "..."`.
  Prueba lo que rodea al modelo: que el prompt se construye bien, que los
  argumentos se validan, que la salida se parsea o falla con criterio.
- **Falla como cualquier red.** Timeouts, 429, 529. Reintentos con espera
  creciente — el ejercicio del módulo 07.
- **Puede inventar.** Un dato que no estaba en el contexto puede aparecer con
  toda la seguridad del mundo. Si el resultado importa, hace falta verificación
  independiente.
- **Cuesta.** Por token, entrada y salida. Un bucle de agente mal acotado puede
  gastar mucho muy rápido, y por eso todo bucle lleva tope.

## Caso real

Un clasificador de transferencias funcionaba bien en las pruebas y en
producción daba resultados raros una vez de cada veinte. Tres causas:

1. **El historial crecía sin recorte.** A partir de cierto punto, la petición
   pasaba de la ventana y la API devolvía error; el código lo capturaba y
   devolvía `"DESCONOCIDA"`. Un error de programación disfrazado de resultado
   del negocio.
2. **No había categoría de escape** en el prompt inicial. El modelo, obligado a
   elegir entre cuatro, inventaba una quinta cuando no encajaba ninguna. Al
   añadir `DESCONOCIDA` explícita, las respuestas raras cayeron en picado.
3. **La salida se parseaba con `.strip().upper()`** y se usaba directamente. Un
   día el modelo respondió con la categoría más una frase de cortesía y esa
   cadena entera acabó guardada como categoría en la base de datos.

Ninguna de las tres es un problema del modelo. Las tres son el código de
alrededor: recorte, prompt y validación de la frontera.

## Ejercicios

```bash
uv run pytest ruta/08-llms-fundamentos
```

Los tests no llaman a ninguna API: no necesitas clave ni conexión. Prueban lo
que se puede probar, que es justamente lo que rodea al modelo.

- **`ejercicios/base/mensajes.py`** — construir la petición recortando el
  historial para que quepa, sin tocar el mensaje de sistema.
- **`ejercicios/base/herramientas.py`** — generar el esquema de una herramienta
  a partir de la firma de una función. Es lo que hacen los SDKs por dentro, y
  es el módulo 00 —todo es un objeto— y el 04 —las anotaciones son datos—
  cobrados juntos.
- **`ejercicios/reto/rag.py`** — trocear texto con solapamiento.

Si quieres además hablar con el modelo de verdad:

```bash
uv sync --group ia
cp .env.example .env    # y pon tu ANTHROPIC_API_KEY
```

## Resumen

- El modelo no recuerda: el historial se manda entero en cada llamada, y por eso
  crece el coste y hay que recortarlo.
- El mensaje de sistema define el rol y las reglas, y nunca se recorta.
- Un prompt es una especificación: rol explícito, opciones cerradas, salida
  para "no sé" y formato acotado.
- `temperature=0` para lo repetible; aun así no es una función pura.
- En tool use, el modelo **decide**; ejecutas tú. Trata sus argumentos como
  entrada no confiable.
- La `description` de una herramienta es su prompt: ahí se gana precisión.
- Valida la salida estructurada. Nunca sigas con lo que no pudiste parsear.
- En RAG, el troceo con solapamiento decide más calidad que el modelo elegido.
- Acepta lo que es: no determinista, falible, caro. Prueba el código de
  alrededor, no la respuesta.

## Preguntas de repaso

1. ¿Por qué una conversación larga cuesta más en cada turno aunque tus
   preguntas sean igual de cortas?
2. Al recortar el historial para que quepa, ¿qué mensaje no se toca nunca?
3. ¿Qué le falta a un prompt de clasificación que obliga a elegir entre cuatro
   categorías?
4. El modelo pide llamar a `delete_account` con una cuenta. ¿Qué haces antes de
   ejecutarlo?
5. ¿Por qué se solapan los trozos en RAG?
6. Tu compañero escribe `assert respuesta.text == "NOMINA"` en un test. ¿Qué le
   dices?

## Recursos

- [Documentación de la API de Claude](https://docs.anthropic.com/es/api/) —
  `doc-oficial` · `es` · `intermedio`. La referencia de `messages`, herramientas
  y streaming.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. Cuándo hace falta un agente y cuándo basta
  una cadena. Léelo antes del módulo 09.
- [Tokenización, explicada](https://platform.openai.com/tokenizer) —
  `doc-oficial` · `en` · `principiante`. Para ver con los ojos cómo se parte tu
  texto.

## Siguiente

Módulo 09 · Agentes con LangGraph, donde el ida y vuelta de las herramientas se
convierte en un bucle con estado.
