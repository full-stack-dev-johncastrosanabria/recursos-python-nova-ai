"""Reto: de un diccionario de strings a un objeto validado.

El entorno solo sabe de texto: `os.environ` devuelve strings, siempre. Pero tu
programa quiere un `port` que sea `int` y un `debug` que sea `bool`. Ese salto
—texto de fuera a tipos de dentro, validando por el camino— es exactamente lo
que hace Pydantic, que verás en el módulo 07. Hacerlo a mano una vez es la
mejor forma de entender qué te va a estar ahorrando.

Convierte `Settings` en una dataclass congelada y escribe su método de clase
`from_mapping`:

    Settings.from_mapping({"HOST": "db.internal", "PORT": "5432"})
    -> Settings(host="db.internal", port=5432, debug=False, timeout=30.0)

Campos, con sus claves de entorno y sus valores por defecto:

    host: str        <- "HOST"      obligatorio
    port: int        <- "PORT"      obligatorio
    debug: bool      <- "DEBUG"     por defecto False
    timeout: float   <- "TIMEOUT"   por defecto 30.0

Reglas:

- Si falta alguna clave obligatoria, lanza `ValueError` mencionando **todas**
  las que faltan, no solo la primera. Quien despliega quiere arreglarlo de una
  vez, no descubrir una por ejecución.
- `DEBUG` se interpreta sin distinguir mayúsculas: `"1"`, `"true"`, `"yes"` y
  `"on"` son verdadero; cualquier otra cosa es falso.
- Si `PORT` o `TIMEOUT` no se pueden convertir, lanza `ValueError` diciendo qué
  clave falló y qué valor traía. "invalid literal for int()" no le sirve a
  nadie a las tres de la mañana.
"""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass
class Settings:
    host: str
    port: int
    debug: bool = False
    timeout: float = 30.0

    @classmethod
    def from_mapping(cls, raw: Mapping[str, str]) -> "Settings":
        raise NotImplementedError("Borra esta línea y escribe tu solución")
