"""Paquete grimorio — motor de transformación del sistema Kalinabis.

Exporta todos los símbolos necesarios para compatibilidad con importadores
existentes (grimorio_base.*) y añade GrimorioMotor como nuevo seam.
"""

from grimorio._kali import KALI_RAIZ
from grimorio._arbol import (
    CHAKRAS,
    CHAKRAS_ARTEMISA_SOCIAL,
    ARBOL_VIDA_SEPHIROTH,
    ARBOL_MUERTE_QLIPHOTH,
    CEREBRO_TRIUNO,
)
from grimorio._entidades import (
    DEIDADES,
    DEIDADES_VALIDAS,
    INVOCACIONES_DIRECTAS,
    TUTU_CRITERIOS,
    ENTIDADES_VALIDAS,
)
from grimorio._tutu import TUTU_SYSTEM
from grimorio._rueda import RUEDA_COLORES, RUEDA_COMO_CONTEXTO
from grimorio._luna import (
    LUNA_SEPHIROTH,
    LUNA_DEIDADES,
    LUNA_NODOS,
    LUNA_VOID_OF_COURSE,
)
from grimorio._meta import SISTEMA_META, ARBOLES_DEIDADES
from grimorio._motor import GrimorioMotor

__all__ = [
    "KALI_RAIZ",
    "CHAKRAS",
    "CHAKRAS_ARTEMISA_SOCIAL",
    "ARBOL_VIDA_SEPHIROTH",
    "ARBOL_MUERTE_QLIPHOTH",
    "CEREBRO_TRIUNO",
    "DEIDADES",
    "DEIDADES_VALIDAS",
    "INVOCACIONES_DIRECTAS",
    "TUTU_CRITERIOS",
    "ENTIDADES_VALIDAS",
    "TUTU_SYSTEM",
    "RUEDA_COLORES",
    "RUEDA_COMO_CONTEXTO",
    "LUNA_SEPHIROTH",
    "LUNA_DEIDADES",
    "LUNA_NODOS",
    "LUNA_VOID_OF_COURSE",
    "SISTEMA_META",
    "ARBOLES_DEIDADES",
    "GrimorioMotor",
]
