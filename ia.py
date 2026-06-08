"""DEPRECADO — usar el paquete `invocacion`.

Este módulo se mantiene solo por compatibilidad. La lógica de IA vive ahora
en `invocacion/` (adapters intercambiables + orquestador `invocador`).

    Antes:  from ia import ia_client
    Ahora:  from invocacion import invocador
"""

import warnings

from invocacion.interface import ClienteIA, RespuestaIA  # noqa: F401
from invocacion.adapters.groq import ClienteGroq  # noqa: F401
from invocacion import invocador

warnings.warn(
    "ia.py está deprecado. Usá: from invocacion import invocador",
    DeprecationWarning,
    stacklevel=2,
)

# Alias retrocompatible al cliente del singleton.
ia_client: ClienteIA = invocador.cliente_ia
