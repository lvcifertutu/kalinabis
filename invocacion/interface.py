"""Contratos del módulo de invocación IA.

Define la interface que todos los adapters de IA deben cumplir y la
respuesta estandarizada que devuelven, de modo que el resto del sistema
no conozca el proveedor concreto (Groq, offline, test, etc.).
"""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class RespuestaIA:
    """Respuesta estandarizada de cualquier adapter de IA.

    Attributes:
        texto: El contenido textual devuelto por el modelo.
        es_offline: True si la respuesta proviene de un fallback sin API.
        validado: False si hubo un error o la respuesta no es confiable.
        metadata: Información auxiliar (proveedor, modelo, error, etc.).
    """

    texto: str
    es_offline: bool = False
    validado: bool = True
    metadata: dict = field(default_factory=dict)


class ClienteIA(Protocol):
    """Interface que todos los adapters de IA deben implementar."""

    def verificar(self) -> tuple[bool, str]:
        """Verifica disponibilidad del proveedor.

        Returns:
            (disponible, mensaje) — mensaje legible para diagnóstico.
        """
        ...

    def chat(
        self,
        system: str,
        messages: list,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> RespuestaIA:
        """Invoca el modelo y devuelve siempre una RespuestaIA."""
        ...
