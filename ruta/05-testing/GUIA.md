# Módulo 05 · Testing

> **Prerrequisitos:** módulos 01-04<br>
> **Tiempo estimado:** 120 min<br>
> **Si ya dominas esto:** salta al módulo 06

Este módulo tiene una particularidad: **sus tests son el material didáctico**.
Llevas cuatro módulos resolviendo ejercicios contra tests que otra persona
escribió. Aquí toca mirarlos por dentro, entender por qué están escritos así, y
empezar a escribir los tuyos.

Ábrelos mientras lees:

```bash
ruta/05-testing/tests/base/test_dias_habiles.py
ruta/05-testing/tests/base/test_validador.py
ruta/05-testing/tests/reto/test_libro.py
```

## Qué vas a poder hacer al terminar

- Escribir tests con pytest
- Usar fixtures y parametrize
- Escribir el test antes que el código

## 1. Para qué se prueba de verdad

El malentendido más extendido es que se prueba para encontrar bugs. Se prueba
para otra cosa, mucho más valiosa:

> **No se prueba para encontrar bugs. Se prueba para poder cambiar el código
> sin miedo.**

Un test no es una red que atrapa errores hoy: es la infraestructura que hace
seguro el cambio de mañana. Refactorizar, añadir una funcionalidad, actualizar
una dependencia — todo eso se vuelve posible sin la parálisis del "¿qué voy a
romper?".

Una suite de tests es lo que convierte el código de un edificio que no se puede
tocar sin que se derrumbe en uno que se puede reformar. Es la misma inversión
que los tipos del módulo 04: pagar rigor por adelantado para comprar libertad
después.

## 2. pytest: `assert` a secas

```python
def test_business_days_between_una_semana_completa():
    assert business_days_between(date(2026, 3, 2), date(2026, 3, 9)) == 5
```

Sin `assertEqual`, sin heredar de nada, sin clases. Una función que empieza por
`test_` y un `assert`. Cuando falla, pytest reescribe la expresión y te enseña
los dos valores:

```text
E       assert 4 == 5
E        +  where 4 = business_days_between(datetime.date(2026, 3, 2), ...)
```

**El nombre del test es documentación ejecutable.** `test_business_days_between_una_semana_completa`
dice qué invariante se rompió sin que tengas que leer el cuerpo. Compáralo con
`test_1` o `test_funciona`.

Y cada test verifica **una cosa**. El antipatrón es el test gigante que
comprueba diez y cuyo fallo no te dice cuál de las diez — tan inútil como el
`except Exception: pass` del módulo 00.

## 3. `parametrize`: la tabla de casos como datos

Cuando el mismo test se repite con distintos valores, no lo copies:

```python
@pytest.mark.parametrize(
    ("cents", "esperado"),
    [
        (0, "0.00"),
        (1_500, "15.00"),
        (99, "0.99"),
        (-500, "-5.00"),
    ],
)
def test_format_money(cents, esperado):
    assert format_money(cents) == esperado
```

Eso son **cuatro tests**, no uno: pytest los ejecuta por separado y te dice
exactamente cuál falló. Separas la lógica de la prueba de los datos que la
ejercen, que es el mismo principio de diseño que llevas aplicando desde el
módulo 02.

## 4. `pytest.raises`: los errores también son comportamiento

Que tu función falle bien es parte de su contrato, y se prueba igual:

```python
def test_no_se_puede_retirar_de_mas():
    with pytest.raises(InsufficientFunds):
        Account("Ana", 1_000).withdraw(5_000)
```

Y puedes ir más allá, comprobando que el mensaje sirve para algo:

```python
def test_el_error_dice_cuanto_habia():
    with pytest.raises(InsufficientFunds) as error:
        Account("Ana", 1_000).withdraw(5_000)

    assert "1000" in str(error.value)
```

Ese test parece pedante hasta la primera vez que lees un log a las tres de la
mañana y el error solo dice `ValueError`.

## 5. Fixtures: el ciclo de vida de lo que el test necesita

Una fixture prepara algo, se lo entrega al test y luego lo recoge:

```python
@pytest.fixture
def libro():
    ledger = Ledger()
    ledger.add("TR-001", 1_500)
    ledger.add("TR-002", 2_500)
    return ledger


def test_el_saldo_suma_las_entradas(libro):
    assert libro.balance == 4_000
```

El test pide `libro` como parámetro y pytest se lo construye. Cada test recibe
**uno nuevo**: no hay estado compartido que haga que un test pase o falle según
el orden en que se ejecuten.

Cuando además hay que limpiar, se usa `yield`:

```python
@pytest.fixture
def base_de_datos():
    conexion = conectar()
    yield conexion       # aquí corre el test
    conexion.cerrar()    # y esto se ejecuta siempre, aunque el test falle
```

Es exactamente el patrón de los context managers: preparar, ceder el control,
recoger. La fixture `solution` que usan todos los ejercicios de este
repositorio está escrita así — ábrela en `conftest.py`, ya la entiendes entera.

## 6. La pirámide: qué probar y a qué nivel

```text
        ╱╲          pocos    end-to-end: lentos, frágiles, insustituibles
       ╱  ╲                  para saber si el sistema entero vive
      ╱────╲       algunos   integración: ¿hablan bien dos piezas reales?
     ╱      ╲
    ╱────────╲     muchos    unitarios: dominio puro, milisegundos,
   ╱__________╲              ninguna dependencia externa
```

La base es ancha porque los tests unitarios del dominio son baratos, rápidos y
precisos: cuando falla uno, sabes exactamente qué se rompió. Los de arriba son
caros y difusos, pero son los únicos que responden "¿esto funciona de verdad?".

De aquí sale un consejo de diseño que vale más que la propia pirámide: **si algo
es difícil de probar, casi siempre está mal diseñado**. Una función que lee un
archivo, llama a una API, calcula y escribe en base de datos es imposible de
probar bien. Separa el cálculo puro de los efectos y el cálculo se vuelve
trivial de probar.

## 7. Mocking: en la frontera, no en el dominio

Un mock sustituye una dependencia real (la base de datos, un LLM) por un doble
controlado. La disciplina cabe en una frase: **se mockea en la frontera, no en
el dominio**.

El dominio puro no necesita mocks — no tiene nada que mockear, y esa es su
virtud. Lo que se sustituye son los adaptadores: el cliente HTTP, el
repositorio. Si te ves parcheando funciones internas de tu propio módulo para
poder probarlo, el problema no es el test.

## 8. TDD: rojo, verde, refactor

1. **Rojo.** Escribe el test. Ejecútalo y compruébalo fallando. Un test que
   nunca has visto fallar puede que no pruebe nada.
2. **Verde.** Escribe el código mínimo que lo hace pasar.
3. **Refactor.** Ahora arréglalo bien, con la red puesta.

Es exactamente el ciclo que llevas haciendo desde el módulo 01: los ejercicios
te llegan en rojo a propósito.

## Caso real

Una función de conciliación tenía cobertura del 94% y una suite verde. Un
cambio de una línea la rompió en producción sin que ningún test se enterara.

Al mirar la suite, tres patologías:

```python
# 1. El test que no prueba nada
def test_reconcile():
    resultado = reconcile(movimientos, registros)
    assert resultado is not None          # ¿y qué? Casi nada es None

# 2. El test que prueba el mock
def test_guarda_en_base_de_datos():
    db = Mock()
    guardar(db, transferencia)
    db.save.assert_called_once()          # prueba que llamaste, no que funcione

# 3. El test gigante
def test_flujo_completo():
    ...  # 80 líneas, 14 asserts
    # cuando falla, dice "falló test_flujo_completo". Gracias.
```

Los tres suben la cobertura y ninguno da confianza. La cobertura mide qué
líneas se ejecutaron, no si comprobaste algo útil sobre ellas. Es un indicador
de dónde **no** has mirado, no una nota.

El arreglo no fue escribir más tests, fue escribir menos y mejores: la lógica de
conciliación se extrajo a una función pura y se probó con veinte casos
parametrizados, incluidos los límites que nadie había considerado — la lista
vacía, las referencias duplicadas, el movimiento sin contraparte.

## Ejercicios

```bash
uv run pytest ruta/05-testing
```

Antes de resolverlos, **lee los tests**. Cada uno demuestra una técnica:

- **`ejercicios/base/dias_habiles.py`** — sus tests usan `parametrize` a fondo:
  mira cómo una tabla de casos sustituye a diez funciones copiadas.
- **`ejercicios/base/validador.py`** — sus tests usan `pytest.raises` y
  comprueban la jerarquía de excepciones, no solo que "falle".
- **`ejercicios/reto/libro.py`** — sus tests usan una fixture. Fíjate en que
  cada test recibe un libro nuevo.

## Resumen

- No se prueba para encontrar bugs: se prueba para poder cambiar sin miedo.
- pytest usa `assert` a secas y reescribe la expresión cuando falla.
- El nombre del test es documentación ejecutable. Un test, una cosa.
- `parametrize` convierte la tabla de casos en datos: N tests con una función.
- Los errores son parte del contrato: se prueban con `pytest.raises`, y merece
  la pena comprobar que el mensaje sirve.
- Las fixtures gestionan el ciclo de vida; con `yield` limpian siempre, falle o
  no el test.
- La pirámide: muchos unitarios, algunos de integración, pocos de extremo a
  extremo.
- Si algo es difícil de probar, casi siempre está mal diseñado.
- Se mockea en la frontera, nunca en el dominio.
- La cobertura dice dónde no has mirado; no dice que lo que miraste esté bien.

## Preguntas de repaso

1. ¿Por qué un test que nunca has visto fallar es sospechoso?
2. Tienes ocho casos que ejercen la misma lógica con distintos valores. ¿Copias
   el test ocho veces?
3. ¿Qué diferencia hay entre una fixture con `return` y una con `yield`?
4. Un compañero dice que su módulo tiene 100% de cobertura. ¿Qué le preguntas?
5. Para probar una función que lee un archivo, llama a una API y calcula un
   total, ¿qué cambiarías antes de escribir un solo test?
6. ¿Por qué mockear una función interna de tu propio módulo es una señal de
   alarma?

## Recursos

- [Documentación de pytest](https://docs.pytest.org/) — `doc-oficial` · `en` ·
  `intermedio`. Empieza por *Get Started* y por la página de fixtures.
- [`unittest.mock`](https://docs.python.org/es/3/library/unittest.mock.html) —
  `doc-oficial` · `es` · `intermedio`. Para cuando toque doblar una frontera.
- [Hypothesis](https://hypothesis.readthedocs.io/) — `doc-oficial` · `en` ·
  `avanzado`. Property-based testing: en vez de los ejemplos que se te ocurren,
  declaras qué debe ser siempre cierto y la herramienta busca el contraejemplo.

## Siguiente

Módulo 06 · Async y concurrencia.
