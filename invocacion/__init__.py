"""Módulo de invocación IA de Kalinabis.

Punto único para hablar con el modelo: el resto del sistema usa el singleton
`invocador` y nunca conoce el proveedor concreto. Cambiar de Groq a otro
proveedor es reemplazar el adapter inyectado aquí.
"""

from invocacion.interface import ClienteIA, RespuestaIA
from invocacion.invocador import Invocador
from invocacion.contexto import ContextoManager
from invocacion.respuesta import ParsingRespuesta
from invocacion.adapters.groq import ClienteGroq
from invocacion.adapters.offline import ClienteOffline
from invocacion.adapters.test import ClienteTest

# Singleton global: reemplaza al antiguo ia.ia_client.
invocador = Invocador(cliente_ia=ClienteGroq())

__all__ = [
    "ClienteIA",
    "RespuestaIA",
    "Invocador",
    "ContextoManager",
    "ParsingRespuesta",
    "ClienteGroq",
    "ClienteOffline",
    "ClienteTest",
    "invocador",
]
