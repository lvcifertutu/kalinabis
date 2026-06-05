"""Adapter del proveedor Groq.

Refactor de la antigua clase ClienteGroq de ia.py: misma lógica de
inicialización perezosa y mismos mensajes de offline/error, pero ahora
devuelve RespuestaIA en lugar de un string crudo.
"""

from config import Config
from invocacion.adapters.base import AdapterBase
from invocacion.interface import RespuestaIA

# Mensaje exacto preservado del comportamiento original (ia.py).
_OFFLINE_MSG = (
    "[Modo offline] No hay GROQ_API_KEY configurada. "
    "El servidor necesita una key de Groq para responder."
)


class ClienteGroq(AdapterBase):
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self._client = None

    def _inicializar(self):
        if self._client is None and self.api_key:
            try:
                from groq import Groq
                self._client = Groq(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "Se necesita 'groq'. Ejecuta: pip install groq"
                )

    def verificar(self) -> tuple[bool, str]:
        if not self.api_key:
            return False, "GROQ_API_KEY no configurada"
        try:
            self._inicializar()
            return True, f"API key configurada - modelo: {self.model}"
        except Exception as e:
            return False, str(e)

    def chat(
        self,
        system: str,
        messages: list,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> RespuestaIA:
        if not self.api_key:
            return RespuestaIA(
                texto=_OFFLINE_MSG,
                es_offline=True,
                validado=False,
                metadata={"provider": "groq"},
            )

        self._inicializar()
        max_tok = max_tokens or Config.GROQ_MAX_TOKENS
        temp = (
            temperature
            if temperature is not None
            else Config.GROQ_TEMPERATURE
        )

        msgs = self._formatar_mensajes(system, messages)

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=msgs,
                max_tokens=max_tok,
                temperature=temp,
            )
            texto = response.choices[0].message.content
            return RespuestaIA(
                texto=texto,
                metadata={"provider": "groq", "modelo": self.model},
            )
        except Exception as e:
            return RespuestaIA(
                texto=f"[Error Groq: {e}]",
                validado=False,
                metadata={"provider": "groq", "error": str(e)},
            )
