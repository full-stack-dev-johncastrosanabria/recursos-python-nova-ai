# Módulo 05 · Testing

> **Prerrequisitos:** módulos 01-04<br>
> **Tiempo estimado:** 240 min<br>
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
- Usar fixtures, `parametrize`, marcas y `conftest.py`
- Comparar valores aproximados sin falsos negativos
- Escribir dobles de prueba y saber dónde ponerlos
- Leer un informe de cobertura sin sacar conclusiones equivocadas
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

### Por qué no puedes evitarlo

Hay una tentación razonable: "el código es sencillo, lo he leído y está bien".
El problema es que **leer tu propio código no es una prueba independiente**.
Sabes lo que quisiste escribir, y eso te hace ver lo que quisiste, no lo que
hay. Es el mismo motivo por el que no se corrigen los propios exámenes.

Y hay una segunda razón, menos obvia y más importante: **el código que hoy es
sencillo no lo va a ser dentro de un año**. Los tests que escribes ahora, sobre
lo fácil, son los que van a sostener lo difícil cuando llegue.

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

**El nombre del test es documentación ejecutable.**
`test_business_days_between_una_semana_completa` dice qué invariante se rompió
sin que tengas que leer el cuerpo. Compáralo con `test_1` o `test_funciona`.

Y cada test verifica **una cosa**. El antipatrón es el test gigante que
comprueba diez y cuyo fallo no te dice cuál de las diez — tan inútil como el
`except Exception: pass` del módulo 00.

### Cómo se ejecutan

```bash
uv run pytest                          # todo
uv run pytest ruta/05-testing          # una carpeta
uv run pytest -k "validador"           # los que lleven eso en el nombre
uv run pytest -x                       # para en el primer fallo
uv run pytest --lf                     # solo los que fallaron la última vez
uv run pytest -q                       # salida breve
uv run pytest -v                       # el nombre de cada test
uv run pytest --durations=5            # los cinco más lentos
```

`--lf` (*last failed*) es el que más tiempo ahorra en el día a día: arreglas,
lo vuelves a lanzar y solo corre lo que estaba roto.

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

Cuando un caso necesita nombre propio, se le pone:

```python
@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        pytest.param("", 0, id="cadena vacía"),
        pytest.param("   ", 0, id="solo espacios"),
    ],
)
def test_contar(entrada, esperado): ...
```

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

# o, más corto, con una expresión regular:
def test_el_error_menciona_el_saldo():
    with pytest.raises(InsufficientFunds, match="1000"):
        Account("Ana", 1_000).withdraw(5_000)
```

Ese test parece pedante hasta la primera vez que lees un log a las tres de la
mañana y el error solo dice `ValueError`.

Un aviso que este repositorio aprendió por las malas: **`NotImplementedError`
hereda de `RuntimeError`**. Un `pytest.raises(RuntimeError)` pasa contra un stub
sin resolver, y el test parece verde sin probar nada. Por eso varios tests de la
ruta añaden `match=`.

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
recoger.

### Alcance: cuántas veces se construye

```python
@pytest.fixture(scope="session")     # una vez para toda la ejecución
def contenedor_postgres(): ...

@pytest.fixture(scope="module")      # una vez por archivo de tests
def datos_grandes(): ...

@pytest.fixture                      # (por defecto) una vez por test
def libro(): ...
```

El criterio: **por defecto siempre**, y subes el alcance solo cuando construirlo
es caro y de verdad es de solo lectura. Una fixture de sesión que los tests
modifican reintroduce el acoplamiento por orden que las fixtures venían a
eliminar.

### `conftest.py`: fixtures compartidas

Una fixture definida en `conftest.py` está disponible para todos los tests de
esa carpeta y sus subcarpetas, sin importar nada.

La fixture `solution` que usan todos los ejercicios de este repositorio está
escrita así — ábrela en el `conftest.py` de la raíz, ya la entiendes entera.

### Fixtures que ya vienen

```python
def test_escribe_un_archivo(tmp_path):          # carpeta temporal, se borra sola
    destino = tmp_path / "salida.txt"
    destino.write_text("hola")
    assert destino.read_text() == "hola"

def test_lee_el_entorno(monkeypatch):           # cambia entorno/atributos y lo deshace
    monkeypatch.setenv("DEBUG", "1")
    assert config.debug is True

def test_imprime_algo(capsys):                  # captura lo que va a stdout
    saludar("Ana")
    assert "Ana" in capsys.readouterr().out
```

`tmp_path` y `monkeypatch` resuelven el 90% de los casos donde uno se plantea
usar un mock.

## 6. Marcas: clasificar y saltar

```python
@pytest.mark.slow
def test_procesa_un_millon_de_filas(): ...

@pytest.mark.skip(reason="pendiente de la API v2")
def test_futuro(): ...

@pytest.mark.skipif(sys.platform == "win32", reason="rutas POSIX")
def test_permisos(): ...

@pytest.mark.xfail(reason="bug conocido #142", strict=True)
def test_caso_roto(): ...
```

`xfail` es más honesto que `skip` para un bug conocido: el test **se ejecuta**,
y con `strict=True` te avisa si un día empieza a pasar — que es justo cuando
quieres enterarte.

Las marcas propias se declaran en `pyproject.toml` y sirven para separar
ejecuciones:

```toml
[tool.pytest.ini_options]
markers = ["slow: tests que tardan más de un segundo"]
```

```bash
uv run pytest -m "not slow"      # el ciclo rápido mientras programas
uv run pytest                    # todo, en el CI
```

## 7. Comparar cosas que no son exactas

Los `float` no se comparan con `==` — el módulo 01 explicó por qué:

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert resultado == pytest.approx(97.88, rel=1e-3)
assert [0.1 + 0.2, 1.0] == pytest.approx([0.3, 1.0])   # también sobre listas
```

`approx` acepta tolerancia relativa (`rel`) y absoluta (`abs`). La relativa es
la correcta casi siempre; la absoluta hace falta cuando el valor esperado es
cero, porque un porcentaje de cero es cero. Vas a implementarlo tú en el
ejercicio `comparar`, que es la mejor forma de no volver a usarlo mal.

## 8. Dobles de prueba: en la frontera, no en el dominio

Un **doble** sustituye una dependencia real (la base de datos, un LLM) por algo
controlado. Hay varios tipos y conviene distinguirlos:

| Tipo | Qué hace |
|---|---|
| **Stub** | devuelve respuestas fijas |
| **Fake** | implementación simplificada pero funcional (un repositorio en memoria) |
| **Spy** | registra cómo lo llamaron, para comprobarlo después |
| **Mock** | un spy con expectativas declaradas de antemano |

La disciplina cabe en una frase: **se dobla en la frontera, no en el dominio**.

El dominio puro no necesita dobles — no tiene nada que doblar, y esa es su
virtud. Lo que se sustituye son los adaptadores: el cliente HTTP, el
repositorio, el reloj. Si te ves parcheando funciones internas de tu propio
módulo para poder probarlo, el problema no es el test.

Y la forma más limpia de doblar algo casi nunca es una librería de mocking: es
**inyectarlo**. Lo llevas haciendo desde el módulo 07 con el reloj de los
reintentos y desde el 11 con el pipeline. Cuando una dependencia entra por
parámetro, el doble es una función normal de tres líneas.

```python
def test_reintenta_dos_veces():
    esperas = []
    solution.retry(operacion_que_falla(2), sleeper=esperas.append)
    assert esperas == [1.0, 2.0]
```

Sin `unittest.mock`, sin parches, sin magia. Eso es tu ejercicio `doble`.

## 9. La pirámide: qué probar y a qué nivel

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

## 10. Cobertura: lo que mide y lo que no

```bash
uv run pytest --cov=novatools --cov-report=term-missing
```

La cobertura dice **qué líneas se ejecutaron** durante la suite. Y nada más.
No dice si comprobaste algo útil sobre ellas.

```python
def test_inutil():
    reconcile(movimientos, registros)     # 100% de cobertura de reconcile
                                          # cero afirmaciones
```

Por eso el número es un **mapa de dónde no has mirado**, no una nota. Un 60%
con tests buenos vale más que un 95% con tests que no afirman nada. Lo útil de
verdad es `--cov-report=term-missing`: la lista de líneas que ningún test
ejecuta, que suele señalar ramas de error olvidadas.

## 11. Propiedades en vez de ejemplos

El testing por ejemplos prueba los casos que se te ocurren. El **testing basado
en propiedades** declara qué debe ser cierto *siempre* y deja que una
herramienta busque el contraejemplo:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_ordenar_conserva_la_longitud(numeros):
    assert len(sorted(numeros)) == len(numeros)

@given(st.integers(), st.integers())
def test_sumar_dinero_es_conmutativo(a, b):
    assert Money(a) + Money(b) == Money(b) + Money(a)
```

Hypothesis genera cientos de entradas, incluidas las que a un humano no se le
ocurren: el cero, el negativo, la lista vacía, el número enorme, el texto con
emojis. Y cuando encuentra un fallo hace *shrinking*: reduce el contraejemplo al
mínimo que lo reproduce, así que no te dice "falla con [4823, -991, 0, 17]"
sino "falla con [0]".

El cambio de mentalidad es el valor real: pasas de *¿qué ejemplos pruebo?* a
**¿qué tiene que ser siempre verdad?**

## 12. TDD: rojo, verde, refactor

1. **Rojo.** Escribe el test. Ejecútalo y compruébalo fallando. Un test que
   nunca has visto fallar puede que no pruebe nada.
2. **Verde.** Escribe el código mínimo que lo hace pasar.
3. **Refactor.** Ahora arréglalo bien, con la red puesta.

Es exactamente el ciclo que llevas haciendo desde el módulo 01: los ejercicios
te llegan en rojo a propósito.

Y cuando encuentres un bug en producción, el orden correcto es el mismo:
**primero el test que lo reproduce**, luego el arreglo. Ese test es lo que
garantiza que no vuelva.

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

Los tres suben la cobertura y ninguno da confianza. El arreglo no fue escribir
más tests, fue escribir menos y mejores: la lógica de conciliación se extrajo a
una función pura y se probó con veinte casos parametrizados, incluidos los
límites que nadie había considerado — la lista vacía, las referencias
duplicadas, el movimiento sin contraparte.

## Ejercicios

```bash
uv run pytest ruta/05-testing
```

Antes de resolverlos, **lee los tests**. Cada uno demuestra una técnica:

- **`ejercicios/base/dias_habiles.py`** — sus tests usan `parametrize` a fondo:
  mira cómo una tabla de casos sustituye a diez funciones copiadas.
- **`ejercicios/base/validador.py`** — sus tests usan `pytest.raises` y
  comprueban la jerarquía de excepciones, no solo que "falle".
- **`ejercicios/base/comparar.py`** — implementar lo que hace `pytest.approx`,
  para no volver a usarlo mal.
- **`ejercicios/reto/libro.py`** — sus tests usan una fixture. Fíjate en que
  cada test recibe un libro nuevo.
- **`ejercicios/reto/doble.py`** — escribir un spy y un reloj falso a mano, sin
  librería de mocking.

## Resumen

- No se prueba para encontrar bugs: se prueba para poder cambiar sin miedo.
- Leer tu propio código no es una prueba independiente.
- pytest usa `assert` a secas y reescribe la expresión cuando falla.
- El nombre del test es documentación ejecutable. Un test, una cosa.
- `--lf` ejecuta solo lo que falló: es el que más tiempo ahorra.
- `parametrize` convierte la tabla de casos en datos: N tests con una función.
- Los errores son parte del contrato: `pytest.raises`, y con `match=` cuando el
  mensaje importa. Ojo: `NotImplementedError` es un `RuntimeError`.
- Las fixtures gestionan el ciclo de vida; con `yield` limpian siempre. Alcance
  por defecto salvo que construir sea caro y de solo lectura.
- `conftest.py` comparte fixtures sin imports. `tmp_path` y `monkeypatch`
  evitan la mayoría de los mocks.
- `xfail(strict=True)` es más honesto que `skip` para un bug conocido.
- Los `float` se comparan con `approx`; la tolerancia absoluta hace falta
  cuando el esperado es cero.
- Se dobla en la frontera, nunca en el dominio, y casi siempre inyectando en
  vez de parcheando.
- La cobertura dice dónde no has mirado; no dice que lo que miraste esté bien.
- Property-based testing cambia "¿qué ejemplos pruebo?" por "¿qué debe ser
  siempre verdad?".
- Ante un bug: primero el test que lo reproduce, después el arreglo.

## Preguntas de repaso

1. ¿Por qué un test que nunca has visto fallar es sospechoso?
2. Tienes ocho casos que ejercen la misma lógica con distintos valores. ¿Copias
   el test ocho veces?
3. ¿Qué diferencia hay entre una fixture con `return` y una con `yield`?
4. ¿Cuándo subirías el alcance de una fixture a `session`, y qué riesgo asumes?
5. Escribes `pytest.raises(RuntimeError)` contra una función sin implementar y
   el test pasa. ¿Qué ocurrió?
6. ¿Por qué `assert resultado == 0.3` puede fallar y `approx` no?
7. Un compañero dice que su módulo tiene 100% de cobertura. ¿Qué le preguntas?
8. Para probar una función que lee un archivo, llama a una API y calcula un
   total, ¿qué cambiarías antes de escribir un solo test?
9. ¿Por qué mockear una función interna de tu propio módulo es una señal de
   alarma?
10. ¿Qué ventaja tiene `xfail(strict=True)` sobre `skip` para un bug conocido?
11. Encuentras un bug en producción. ¿Qué escribes primero?

## Recursos

- [Documentación de pytest](https://docs.pytest.org/) — `doc-oficial` · `en` ·
  `intermedio`. Empieza por *Get Started* y por la página de fixtures.
- [Fixtures de pytest](https://docs.pytest.org/en/stable/how-to/fixtures.html)
  — `doc-oficial` · `en` · `intermedio`. Alcances, `yield`, y las que ya vienen.
- [`unittest.mock`](https://docs.python.org/es/3/library/unittest.mock.html) —
  `doc-oficial` · `es` · `intermedio`. Para cuando toque doblar una frontera y
  la inyección no baste.
- [Hypothesis](https://hypothesis.readthedocs.io/) — `doc-oficial` · `en` ·
  `avanzado`. Property-based testing, con su capítulo sobre cómo elegir
  propiedades.
- [coverage.py](https://coverage.readthedocs.io/) — `doc-oficial` · `en` ·
  `intermedio`. Qué mide exactamente y cómo configurar qué se excluye.

## Siguiente

Módulo 06 · Async y concurrencia.
