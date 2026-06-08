"""Contexto de identidad de proyecto.

Encapsula tras una sola interface lo que antes se filtraba por todas las
rutas: resolver y validar el header X-Project-Code, tocar la actividad,
cifrar/descifrar con el código del proyecto (AES-256-GCM) y decidir entre
el almacén por-proyecto y el almacén legacy (modo anónimo).

Es agnóstico del framework web: `requerir()` devuelve datos planos y deja
que la capa HTTP los formatee.
"""

from typing import Optional

from proyectos import Cifrador, Proyecto
from base_datos.proyecto import ProyectoRepo, ConversacionRepo
from base_datos.legacy import ConversacionLegadoRepo as _ConvLegado

HEADER = "X-Project-Code"


class ContextoProyecto:
    """Identidad de proyecto resuelta para una request (o modo anónimo)."""

    def __init__(self, proyecto: Optional[Proyecto]):
        self.proyecto = proyecto

    @classmethod
    def desde_headers(cls, headers) -> "ContextoProyecto":
        """Resuelve el header a un proyecto válido, o modo anónimo (None)."""
        codigo = headers.get(HEADER)
        proyecto = None
        if codigo:
            candidato = Proyecto(codigo=codigo)
            if ProyectoRepo.existe(candidato.hash):
                proyecto = candidato
        return cls(proyecto)

    @property
    def activo(self) -> bool:
        """True si hay un proyecto válido; False en modo anónimo/legacy."""
        return self.proyecto is not None

    @property
    def hash(self) -> Optional[str]:
        return self.proyecto.hash if self.proyecto else None

    def requerir(self) -> Optional[tuple[dict, int]]:
        """Exige proyecto. Devuelve (error, status) si falta; si no, toca
        actividad y devuelve None."""
        if not self.proyecto:
            return (
                {"error": f"Header {HEADER} requerido o código inválido"},
                401,
            )
        ProyectoRepo.actualizar_actividad(self.proyecto.hash)
        return None

    # ── Cifrado (requiere proyecto activo) ──────────────────────────────

    def cifrar(self, datos: str) -> str:
        return Cifrador.cifrar(datos, self.proyecto.codigo)

    def descifrar(self, cifrado: str) -> Optional[str]:
        return Cifrador.descifrar(cifrado, self.proyecto.codigo)

    # ── Memoria: por-proyecto o legacy ──────────────────────────────────

    def cargar_memoria(self, entidad: str) -> list:
        if self.proyecto:
            return ConversacionRepo.cargar(self.proyecto.hash, entidad)
        return _ConvLegado.cargar(entidad)

    def limpiar_memoria(self, entidad: str) -> int:
        if self.proyecto:
            return ConversacionRepo.limpiar(self.proyecto.hash, entidad)
        return _ConvLegado.limpiar(entidad)
