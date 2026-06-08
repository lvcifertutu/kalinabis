"""Harness de tests de comportamiento de Kalinabis.

Arranca la app real bajo test con adapters controlados:
  · Base de datos SQLite TEMPORAL y aislada (no toca grimorio.db real).
  · Adapter de IA falso (ClienteTest) — sin red, sin GROQ_API_KEY.
  · Flask test client — sin servidor manual, sin localhost:5000.

Esto es posible porque la persistencia (persistencia.AdaptadorBD) y la
invocación de IA (invocacion.ClienteTest) son intercambiables. El truco de
orden: redirigimos el adapter de BD ANTES de importar servidor, para que su
inicializar_db() de nivel de módulo cree el schema en la base temporal.
"""

import os
import sys
import atexit
import tempfile
from pathlib import Path

# La app vive en el directorio padre de tests/ (sin path drift hardcodeado).
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

# Forzar SQLite ignorando cualquier DATABASE_URL del entorno.
os.environ.pop("DATABASE_URL", None)

import base_datos
from persistencia import AdaptadorSQLite

# Base temporal aislada; el schema se crea acá, no en grimorio.db.
_tmp = tempfile.NamedTemporaryFile(
    prefix="kalinabis_test_", suffix=".db", delete=False
)
_tmp.close()
_DB_TEMP = _tmp.name

base_datos.ADAPTADOR = AdaptadorSQLite(ruta=_DB_TEMP)
base_datos.MODO_PG = False

# Recién ahora importamos servidor: su inicializar_db() usa la base temporal.
import servidor  # noqa: E402
from invocacion import ClienteTest  # noqa: E402


@atexit.register
def _limpiar_db_temporal():
    try:
        os.unlink(_DB_TEMP)
    except OSError:
        pass


class AppDeTest:
    """Cliente de la app con IA falsa y utilidades comunes de test."""

    def __init__(self):
        self.ia = ClienteTest()
        servidor.invocador.cliente_ia = self.ia
        self.client = servidor.app.test_client()

    def reset_rate_limit(self):
        """Limpia el estado de rate limiting (aislamiento entre tests)."""
        servidor._rate_limit_data.clear()

    def crear_proyecto(self, nombre: str = "Test") -> str:
        """Crea un proyecto y devuelve su código. Resetea rate limit antes."""
        self.reset_rate_limit()
        r = self.client.post("/api/proyecto/nuevo", json={"nombre": nombre})
        return r.get_json()["codigo"]

    @staticmethod
    def headers(codigo: str) -> dict:
        return {"X-Project-Code": codigo}
