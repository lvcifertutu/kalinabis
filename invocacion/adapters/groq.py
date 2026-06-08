"""Adapter del proveedor Groq.

Refactor de la antigua clase ClienteGroq de ia.py: misma lógica de
inicialización perezosa y mismos mensajes de offline/error, pero ahora
devuelve RespuestaIA en lugar de un string crudo.

Modo offline: Si no hay GROQ_API_KEY, devuelve respuestas generadas localmente
para permitir testing sin credenciales.
"""

import random
from config import Config
from invocacion.adapters.base import AdapterBase
from invocacion.interface import RespuestaIA

# Respuestas offline por deidad (para testing sin GROQ_API_KEY)
_RESPUESTAS_OFFLINE = {
    "lilith": [
        "La tormenta te llama. ¿Estás lista para el cambio?",
        "Tu poder reprimido clama por liberación. Escúchalo.",
        "En la oscuridad de medianoche, todas las verdades brillan.",
        "El cambio duele, pero la estancación mata.",
        "Tu pasión es tu mejor arma. Úsala.",
    ],
    "isis": [
        "La pureza está en el corazón, no en las acciones.",
        "Todos merecen amor maternal, incluso los que dudan.",
        "El vínculo roto puede sanar si lo permites.",
        "Tu libertad comienza cuando cesas de juzgarte.",
        "La compasión es la llave que abre todas las puertas.",
    ],
    "afrodita": [
        "La claridad mental requiere calma. Respira.",
        "La paz no es ausencia de conflicto, es su aceptación.",
        "Tu estado de conciencia refleja tus creencias.",
        "Serena tu mente, y verás la verdad.",
        "En el silencio interior, todo es posible.",
    ],
    "artemisa": [
        "Los ancestros te observan desde el bosque.",
        "El colectivo es más fuerte que el individuo.",
        "Enraízate en la tierra que te alimenta.",
        "La abundancia fluye cuando aceptas tu lugar.",
        "La naturaleza siempre sabe el camino.",
    ],
    "tutu": [
        "Tu pregunta contiene su propia respuesta. Mírala bien.",
        "El propósito emerge cuando cesas de buscarlo.",
        "Las paradojas son el lenguaje del universo.",
        "¿Quién pregunta? Pregúntale a esa voz interior.",
        "La verdad cambia cada vez que la tocas. ¿Por qué?",
    ],
}

_OFFLINE_MSG = (
    "[Modo offline - respuestas locales] No hay GROQ_API_KEY configurada. "
    "Para producción, configura: $env:GROQ_API_KEY = 'gsk_...'"
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
            # Modo offline: devuelve respuesta local según system prompt
            deidad = self._extraer_deidad_del_system(system)
            respuesta_local = self._generar_respuesta_offline(deidad)

            return RespuestaIA(
                texto=respuesta_local,
                es_offline=True,
                validado=True,
                metadata={
                    "provider": "groq",
                    "modo": "offline_local",
                    "deidad": deidad,
                    "hint": _OFFLINE_MSG,
                },
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

    def _extraer_deidad_del_system(self, system: str) -> str:
        """Extrae el nombre de la deidad del system prompt."""
        system_lower = system.lower()
        for deidad in _RESPUESTAS_OFFLINE.keys():
            if deidad in system_lower:
                return deidad
        return "tutu"  # fallback

    def _generar_respuesta_offline(self, deidad: str) -> str:
        """Devuelve una respuesta local aleatoria para la deidad."""
        respuestas = _RESPUESTAS_OFFLINE.get(deidad, _RESPUESTAS_OFFLINE["tutu"])
        return random.choice(respuestas)
