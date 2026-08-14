# Módulo 08 · Fundamentos de LLMs

> **Prerrequisitos:** módulos 01-07<br>
> **Tiempo estimado:** 240 min<br>
> **Si ya dominas esto:** salta al módulo 09

A partir de aquí la ruta cambia de tema, pero no de método. Un LLM es una
dependencia externa más: lenta, cara, no determinista y con una API. Todo lo
del módulo 07 —validar en la frontera, timeouts, reintentos, paginación— aplica
igual, y ahora además hay que lidiar con que la respuesta no sea la misma dos
veces.

## Qué vas a poder hacer al terminar

- Explicar qué es un token, un embedding y una ventana de contexto
- Llamar a un modelo con el SDK de Claude y controlar su coste
- Escribir prompts que den resultados repetibles
- Definir herramientas y manejar tool use con seguridad
- Obtener salida estructurada y validarla
- Montar un RAG básico y saber qué decide su calidad
- Evaluar un sistema con LLM sin engañarte

## 1. Qué hay debajo: tokens, vectores y atención

### Tokens

El modelo no ve caracteres ni palabras: ve **tokens**, trozos de texto de unos
cuatro caracteres de media en inglés y algo menos en español. `"conciliación"`
puede ser tres tokens; `"the"` es uno.

Todo lo demás se deriva de eso: la **ventana de contexto** se mide en tokens, el
precio se cobra por token de entrada y de salida, y `max_tokens` limita la
salida.

Contar tokens con `len(texto) / 4` es una aproximación de servilleta, útil para
presupuestar y nada más.

### Embeddings

Un **embedding** es un vector de números que representa el significado de un
texto. La propiedad que lo hace útil: **los textos parecidos quedan cerca en ese
espacio**, aunque no compartan ni una palabra.

```text
"transferencia rechazada"   → [0.21, -0.03, 0.88, ...]
"el pago no se completó"    → [0.19, -0.05, 0.91, ...]   ← cerca
"receta de tortilla"        → [-0.7,  0.44, 0.02, ...]   ← lejos
```

"Cerca" se mide casi siempre con la **similitud coseno**: el coseno del ángulo
entre los dos vectores, que vale 1 si apuntan igual, 0 si son perpendiculares y
-1 si son opuestos. Es aritmética de instituto, y la vas a implementar en el
ejercicio `similitud`.

De ahí sale la búsqueda semántica, y de la búsqueda semántica sale el RAG.

### Atención, en un párrafo

La arquitectura *transformer* que hay debajo tiene una idea central: al procesar
cada token, el modelo **mira todos los demás y decide a cuáles prestar
atención**. Eso es lo que le permite resolver a qué se refiere un "ella" que
apareció treinta palabras antes.

La consecuencia práctica que sí te afecta: ese mecanismo compara cada token con
todos los demás, así que **el coste crece con el cuadrado de la longitud**.
Duplicar el contexto no duplica el trabajo: lo cuadruplica. Por eso un prompt
gigante no solo cuesta más dinero, también tarda más de lo que parece.

## 2. La llamada mínima

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
print(respuesta.usage)        # tokens de entrada y salida: tu factura
print(respuesta.stop_reason)  # 'end_turn' | 'max_tokens' | 'tool_use'
```

Cinco cosas que conviene fijar desde el principio:

**El `system` va aparte, no dentro de `messages`.** Es donde se define el rol y
las reglas. Los mensajes son la conversación.

**La conversación no tiene memoria.** El modelo no recuerda nada entre
llamadas: en cada petición le mandas el historial completo. Toda la "memoria"
de un chatbot la construyes tú.

**`max_tokens` es un límite de salida**, no un objetivo. Si se agota, la
respuesta se corta a media frase — y por eso hay que mirar `stop_reason`. Si
vale `"max_tokens"`, tienes una respuesta truncada, no una respuesta.

**Pagas por tokens de entrada y de salida.** Como el historial se reenvía
entero en cada turno, una conversación larga cuesta cada vez más. De ahí que el
primer ejercicio sea recortarlo.

**El streaming existe y cambia la experiencia**, no el coste:

```python
with client.messages.stream(model=..., max_tokens=1024, messages=[...]) as stream:
    for texto in stream.text_stream:
        print(texto, end="", flush=True)
```

Es el `async for` sobre un generador asíncrono del módulo 06: un flujo de
tokens que se consume según llega.

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

Lo que hace que funcione: el rol es explícito, las categorías son cerradas, hay
una salida para el caso "no sé" (sin ella el modelo inventará una categoría) y
el formato de respuesta está acotado.

### Las técnicas que de verdad mueven la aguja

**Ejemplos (*few-shot*).** Enseñar dos o tres casos resueltos vale más que
media página de instrucciones:

```text
Ejemplos:
"PAGO NOMINA MARZO ACME SA" → NOMINA
"TRANSF A JUAN PEREZ" → PERSONAL
```

**Pedir el razonamiento antes de la respuesta.** Para tareas con varios pasos,
dejar que el modelo "piense en voz alta" antes de concluir mejora bastante el
acierto — y te deja auditar por qué decidió lo que decidió.

**Delimitar con etiquetas.** Cuando metes un documento dentro del prompt,
márcalo:

```text
<documento>
{contenido}
</documento>

Responde solo con lo que aparezca en el documento.
```

Eso reduce la confusión entre tus instrucciones y el contenido — y es la
primera línea de defensa contra la **inyección de prompt**, que es cuando el
texto que procesas trae instrucciones dentro. Ese texto es entrada no confiable,
exactamente igual que un payload de red.

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

Tres avisos que valen dinero real:

- **La `description` es el prompt de la herramienta.** Una descripción vaga
  hace que el modelo la use cuando no toca, o no la use cuando sí. Es donde más
  se gana afinando.
- **Nunca ejecutes a ciegas lo que el modelo pida.** Los argumentos que llegan
  son entrada no confiable. Valídalos en la frontera, con lo del módulo 07.
- **Separa las herramientas que leen de las que escriben.** Una que consulta un
  saldo puede ejecutarse sin más; una que mueve dinero necesita confirmación
  humana. Esa distinción se diseña, no se improvisa.

## 5. Salida estructurada

Pedir "responde en JSON" y esperar lo mejor es frágil. Hay dos formas robustas:

**Usar el propio mecanismo de herramientas** para forzar la forma: defines una
herramienta cuyo esquema es la estructura que quieres y el modelo la "llama".

**Validar lo que llegue**, siempre:

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

## 6. RAG: recuperar antes de generar

Cuando el conocimiento no cabe en el prompt: se trocea el corpus, se convierte
cada trozo en un embedding, se guardan, y en cada pregunta se buscan los trozos
más parecidos y se mandan como contexto.

```text
documentos → trocear → embeddings → índice
                                       │
pregunta → embedding → buscar los k más cercanos → prompt con esos trozos → LLM
```

### Lo que decide la calidad

**El troceo**, y es el paso menos glamuroso. Trozos muy grandes traen ruido;
muy pequeños pierden el contexto que daba sentido a la frase. Por eso se usa
**solapamiento**: cada trozo repite el final del anterior para que una idea
partida por la mitad siga completa en alguno de los dos. Ese es tu reto `rag`.

Y trocear por **estructura** (párrafos, secciones) casi siempre gana a trocear
por número de caracteres, porque respeta las unidades de significado.

**Cuántos trozos recuperas.** Pocos y te falta contexto; muchos y el ruido
tapa la señal —y encima el coste crece con el cuadrado, como vimos. Entre tres
y diez suele ser el rango razonable.

**Qué metadatos guardas con cada trozo.** De dónde salió, de qué documento, de
qué fecha. Sin eso no puedes citar la fuente, y un RAG que no cita es un RAG que
no se puede auditar.

### El error de fondo

RAG no es "el modelo ahora sabe más". Es "**le he puesto delante el texto
relevante**". Si la recuperación trae el trozo equivocado, el modelo responderá
con seguridad sobre el trozo equivocado. Por eso, cuando un RAG falla, el
sospechoso número uno es la recuperación, no el modelo.

## 7. Evaluar sin engañarse

Un sistema con LLM que no se mide es un sistema que no se puede mejorar: no
sabes si un cambio en el prompt fue mejor o peor, solo que "parecía mejor".

Lo mínimo que funciona:

**Un conjunto de casos con su respuesta esperada.** Veinte casos reales bien
elegidos valen más que doscientos inventados. Se guardan en el repositorio, como
datos.

**Una métrica que se pueda calcular sin juicio humano** siempre que se pueda:
¿acertó la categoría? ¿el JSON valida? ¿el número que citó aparece en los datos
de entrada?

**Y solo cuando no queda otra**, un modelo como juez — sabiendo que un juez que
también es un LLM tiene sus propios sesgos, y que hay que revisar sus veredictos
de vez en cuando a mano.

Lo que **no** funciona: `assert respuesta.text == "NOMINA"` en un test unitario.
La salida no es determinista, el test será intermitente, y alguien acabará
borrándolo.

## 8. Lo que hay que aceptar

- **No es determinista.** Prueba lo que rodea al modelo: que el prompt se
  construye bien, que los argumentos se validan, que la salida se parsea o falla
  con criterio.
- **Falla como cualquier red.** Timeouts, 429, 529. Reintentos con espera
  creciente — el ejercicio del módulo 07.
- **Puede inventar.** Un dato que no estaba en el contexto puede aparecer con
  toda la seguridad del mundo. Si el resultado importa, hace falta verificación
  independiente — y en el módulo 10 verás que la verificación con código gana a
  la verificación con otro modelo.
- **Cuesta.** Por token, entrada y salida. Un bucle de agente mal acotado puede
  gastar mucho muy rápido, y por eso todo bucle lleva tope.

## Caso real

Un clasificador de transferencias funcionaba bien en las pruebas y en
producción daba resultados raros una vez de cada veinte. Cuatro causas:

1. **El historial crecía sin recorte.** A partir de cierto punto, la petición
   pasaba de la ventana y la API devolvía error; el código lo capturaba y
   devolvía `"DESCONOCIDA"`. Un error de programación disfrazado de resultado
   del negocio.
2. **No había categoría de escape** en el prompt inicial. El modelo, obligado a
   elegir entre cuatro, inventaba una quinta cuando no encajaba ninguna.
3. **La salida se parseaba con `.strip().upper()`** y se usaba directamente. Un
   día el modelo respondió con la categoría más una frase de cortesía y esa
   cadena entera acabó guardada como categoría en la base de datos.
4. **Nadie miraba `stop_reason`.** Algunas respuestas venían truncadas por
   `max_tokens`, y una categoría cortada a la mitad pasaba la validación de
   "no está vacío".

Ninguna de las cuatro es un problema del modelo. Las cuatro son el código de
alrededor: recorte, prompt, validación de la frontera y comprobar el motivo de
parada.

## Ejercicios

```bash
uv run pytest ruta/08-llms-fundamentos
```

Los tests no llaman a ninguna API: no necesitas clave ni conexión. Prueban lo
que se puede probar, que es justamente lo que rodea al modelo.

- **`ejercicios/base/mensajes.py`** — construir la petición recortando el
  historial para que quepa, sin tocar el mensaje de sistema.
- **`ejercicios/base/herramientas.py`** — generar el esquema de una herramienta
  a partir de la firma de una función.
- **`ejercicios/base/similitud.py`** — similitud coseno y recuperar los k más
  cercanos. Es el corazón de la búsqueda semántica, y es aritmética.
- **`ejercicios/reto/rag.py`** — trocear texto con solapamiento.
- **`ejercicios/reto/plantilla.py`** — rellenar un prompt con variables sin que
  el contenido pueda inyectar instrucciones.

Si quieres además hablar con el modelo de verdad:

```bash
uv sync --group ia
cp .env.example .env    # y pon tu ANTHROPIC_API_KEY
```

## Resumen

- El modelo ve tokens; de ahí salen la ventana, el precio y `max_tokens`.
- Un embedding coloca los textos parecidos cerca; "cerca" se mide con similitud
  coseno.
- El coste de atención crece con el **cuadrado** de la longitud: un prompt
  gigante cuesta más de lo que parece.
- El modelo no recuerda: el historial se manda entero en cada llamada.
- Mira `stop_reason`: si es `max_tokens`, tienes una respuesta truncada.
- Un prompt es una especificación: rol explícito, opciones cerradas, salida
  para "no sé" y formato acotado. Los ejemplos valen más que las instrucciones.
- Delimita el contenido con etiquetas: es la primera defensa contra la
  inyección de prompt.
- En tool use, el modelo **decide**; ejecutas tú. Separa lo que lee de lo que
  escribe.
- Valida la salida estructurada. Nunca sigas con lo que no pudiste parsear.
- En RAG, el troceo con solapamiento decide más calidad que el modelo elegido,
  y cuando falla el sospechoso es la recuperación.
- Sin casos de evaluación guardados, no sabes si un cambio mejoró algo.
- Acepta lo que es: no determinista, falible, caro. Prueba el código de
  alrededor, no la respuesta.

## Preguntas de repaso

1. ¿Por qué una conversación larga cuesta más en cada turno aunque tus
   preguntas sean igual de cortas?
2. Duplicas el tamaño del contexto. ¿Cuánto más trabajo supone, y por qué?
3. Al recortar el historial para que quepa, ¿qué mensaje no se toca nunca?
4. ¿Qué le falta a un prompt de clasificación que obliga a elegir entre cuatro
   categorías?
5. Procesas correos de clientes con un LLM y uno trae "ignora tus
   instrucciones y…". ¿Qué haces?
6. El modelo pide llamar a `delete_account` con una cuenta. ¿Qué haces antes de
   ejecutarlo?
7. ¿Por qué se solapan los trozos en RAG?
8. Tu RAG responde con seguridad algo que no está en los documentos. ¿Por dónde
   empiezas a mirar?
9. Tu compañero escribe `assert respuesta.text == "NOMINA"` en un test. ¿Qué le
   dices, y qué le propones en su lugar?
10. ¿Qué información te da `stop_reason` y por qué importa?

## Recursos

- [Documentación de la API de Claude](https://docs.anthropic.com/es/api/) —
  `doc-oficial` · `es` · `intermedio`. La referencia de `messages`, herramientas
  y streaming.
- [Tool use](https://docs.anthropic.com/es/docs/build-with-claude/tool-use) —
  `doc-oficial` · `es` · `intermedio`. El ida y vuelta, con sus formatos.
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  — `artículo` · `en` · `intermedio`. Cuándo hace falta un agente y cuándo basta
  una cadena. Léelo antes del módulo 09.
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
  — `artículo` · `en` · `avanzado`. La arquitectura explicada con dibujos. Es
  el mejor material que existe para entender qué hay debajo.
- [Tokenizador interactivo](https://platform.openai.com/tokenizer) —
  `doc-oficial` · `en` · `principiante`. Para ver con los ojos cómo se parte tu
  texto.

## Siguiente

Módulo 09 · Agentes con LangGraph, donde el ida y vuelta de las herramientas se
convierte en un bucle con estado.
