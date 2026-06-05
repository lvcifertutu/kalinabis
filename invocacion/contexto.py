"""Armado centralizado de system prompts con sus contextos dinámicos.

Reúne en un solo lugar la composición que antes se repetía en servidor.py:
base de la entidad + luna + rueda + carta natal + instrucciones específicas.
"""

from grimorio_base import DEIDADES, TUTU_SYSTEM, RUEDA_COMO_CONTEXTO
from luna import luna_como_contexto
from astral import carta_natal_como_contexto

# Instrucciones específicas preservadas tal cual desde servidor.py.
INSTRUCCION_TAROT = (
    "\n\nEl consultante ha extendido una tirada de tres cartas ante ti. "
    "Lee la tirada completa desde tu naturaleza — une el pasado, el presente "
    "y el futuro en una sola voz. Considera la luna de hoy y, si la conoces, "
    "su carta natal. Habla con profundidad pero sin exceder un párrafo o dos."
)

INSTRUCCION_SIGILO = (
    "\n\nEl practicante te pide un sigilo. Basándote en lo que han hablado, "
    "regálale una intención breve y poderosa (máximo 8 palabras) que capture "
    "lo que su alma necesita ahora. Responde SOLO con la intención en mayúsculas, "
    "sin comillas ni explicación. Ejemplo: VEO CON CLARIDAD MI CAMINO"
)


class ContextoManager:
    """Compone system prompts a partir de la entidad y los contextos vivos."""

    @staticmethod
    def _base_entidad(nombre_entidad: str) -> str:
        """System prompt base de una entidad (tutu o deidad)."""
        if nombre_entidad == "tutu":
            return TUTU_SYSTEM
        if nombre_entidad in DEIDADES:
            return DEIDADES[nombre_entidad]["system_prompt"]
        raise ValueError(f"Entidad desconocida: {nombre_entidad}")

    @staticmethod
    def para_deidad(nombre: str, carta_natal: dict | None = None) -> str:
        """Conversación normal con una deidad: base + luna + rueda + carta."""
        system = (
            DEIDADES[nombre]["system_prompt"]
            + luna_como_contexto()
            + RUEDA_COMO_CONTEXTO
        )
        if carta_natal:
            system += carta_natal_como_contexto(carta_natal)
        return system

    @staticmethod
    def para_tutu() -> str:
        """Conversación con Tutu: base + luna + rueda."""
        return TUTU_SYSTEM + luna_como_contexto() + RUEDA_COMO_CONTEXTO

    @staticmethod
    def para_tarot(nombre_entidad: str, carta_natal: dict | None = None) -> str:
        """Lectura de tarot: base + luna + carta + instrucción de tirada."""
        system = ContextoManager._base_entidad(nombre_entidad)
        system += luna_como_contexto()
        if carta_natal:
            system += carta_natal_como_contexto(carta_natal)
        system += INSTRUCCION_TAROT
        return system

    @staticmethod
    def para_sigilo(nombre_entidad: str) -> str:
        """Regalo de sigilo: base + luna + instrucción de intención."""
        system = ContextoManager._base_entidad(nombre_entidad)
        system += luna_como_contexto()
        system += INSTRUCCION_SIGILO
        return system
