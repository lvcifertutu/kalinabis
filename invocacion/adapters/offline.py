"""Adapter offline: fallback sin ninguna API externa.

No se usa en el camino por defecto (ese rol lo cubre ClienteGroq sin key),
sino que está disponible para inyectarse explícitamente cuando se quiere
correr el sistema sin depender de ningún proveedor.
"""

from invocacion.adapters.base import AdapterBase
from invocacion.interface import RespuestaIA

_MENSAJE = (
    "[Modo offline] El oráculo está en silencio: no hay proveedor de IA "
    "configurado. Configura una key para recibir respuestas."
)


class ClienteOffline(AdapterBase):
    def verificar(self) -> tuple[bool, str]:
        return True, "Modo offline disponible (sin proveedor externo)"

    def chat(
        self,
        system: str,
        messages: list,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> RespuestaIA:
        return RespuestaIA(
            texto=_MENSAJE,
            es_offline=True,
            validado=False,
            metadata={"provider": "offline"},
        )
