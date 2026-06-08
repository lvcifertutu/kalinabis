"""Base común para los adapters de IA."""

import json
from abc import ABC, abstractmethod

from invocacion.interface import RespuestaIA


class AdapterBase(ABC):
    """Clase base con utilidades compartidas por los adapters.

    Concentra el formateo de mensajes y el parsing tolerante de JSON,
    evitando que cada adapter reimplemente esa lógica.
    """

    def _formatar_mensajes(self, system: str, messages: list) -> list:
        """Convierte (system, messages) al formato estándar de chat.

        Normaliza cada rol a 'user'/'assistant' y antepone el system.
        """
        msgs = [{"role": "system", "content": system}]
        for m in messages:
            role = "assistant" if m.get("role") == "assistant" else "user"
            msgs.append({"role": role, "content": m.get("content", "")})
        return msgs

    def _parsear_json_desde_texto(
        self, texto: str, fallback: dict | None = None
    ) -> dict:
        """Extrae un objeto JSON embebido en texto libre (markdown, etc.)."""
        try:
            inicio = texto.find("{")
            fin = texto.rfind("}") + 1
            if inicio >= 0 and fin > inicio:
                return json.loads(texto[inicio:fin])
        except Exception:
            pass
        return fallback or {}

    @abstractmethod
    def verificar(self) -> tuple[bool, str]:
        ...

    @abstractmethod
    def chat(
        self,
        system: str,
        messages: list,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> RespuestaIA:
        ...
