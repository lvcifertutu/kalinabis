"""Adapter de test: respuestas simuladas, sin llamadas a APIs reales.

Permite inyectarse en Invocador para probar toda la lógica de orquestación
(armado de contexto, persistencia, parsing) sin necesitar GROQ_API_KEY.
"""

from invocacion.adapters.base import AdapterBase
from invocacion.interface import RespuestaIA

# Respuesta JSON por defecto, compatible con decidir_entidad().
_RESPUESTA_DEFAULT = '{"deidad": "tutu", "estado": "alma", "razon": "test"}'


class ClienteTest(AdapterBase):
    def __init__(self, respuesta_default: str = _RESPUESTA_DEFAULT):
        self.respuesta_default = respuesta_default
        self.respuestas: list[str] = []
        self.historial_llamadas: list[dict] = []

    def encolar(self, texto: str) -> "ClienteTest":
        """Encola una respuesta para la próxima llamada a chat()."""
        self.respuestas.append(texto)
        return self

    def verificar(self) -> tuple[bool, str]:
        return True, "Cliente de test (sin API real)"

    def chat(
        self,
        system: str,
        messages: list,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> RespuestaIA:
        self.historial_llamadas.append({
            "system": system,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        })
        texto = (
            self.respuestas.pop(0)
            if self.respuestas
            else self.respuesta_default
        )
        return RespuestaIA(
            texto=texto,
            metadata={
                "provider": "test",
                "llamada_num": len(self.historial_llamadas),
            },
        )
