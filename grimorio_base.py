# grimorio_base.py — shim de compatibilidad
# El sistema vive ahora en el paquete grimorio/
# Este archivo re-exporta todo para no romper importadores existentes.

from grimorio import (  # noqa: F401
    KALI_RAIZ,
    CHAKRAS,
    CHAKRAS_ARTEMISA_SOCIAL,
    ARBOL_VIDA_SEPHIROTH,
    ARBOL_MUERTE_QLIPHOTH,
    CEREBRO_TRIUNO,
    DEIDADES,
    DEIDADES_VALIDAS,
    INVOCACIONES_DIRECTAS,
    TUTU_CRITERIOS,
    TUTU_SYSTEM,
    RUEDA_COLORES,
    RUEDA_COMO_CONTEXTO,
    LUNA_SEPHIROTH,
    LUNA_DEIDADES,
    LUNA_NODOS,
    LUNA_VOID_OF_COURSE,
    SISTEMA_META,
    ARBOLES_DEIDADES,
    GrimorioMotor,
)

# Legacy: sembrar_memoria_artemisa sigue disponible
def sembrar_memoria_artemisa(db_path=None):
    from base_datos.legacy import ConversacionLegadoRepo as _CL
    from grimorio._meta import ARBOLES_DEIDADES as _AD

    ya_tiene = bool(_CL.cargar("artemisa"))
    if ya_tiene:
        return False

    semilla = _AD["artemisa"].get("memoria_semilla", [])
    for msg in semilla:
        _CL.guardar("artemisa", msg["role"], msg["content"], "fundacional")
    return True


def consultar_cosmologia(consulta: str) -> dict:
    consulta = consulta.lower()
    if "estado" in consulta or "estructura" in consulta:
        return {k: v for k, v in SISTEMA_META["estados"].items()}
    if "arbol" in consulta or "árbol" in consulta:
        return SISTEMA_META["arboles"]
    if "chakra" in consulta:
        return CHAKRAS
    if "sephirot" in consulta or "vida" in consulta:
        return ARBOL_VIDA_SEPHIROTH
    if "qliphoth" in consulta or "muerte" in consulta:
        return ARBOL_MUERTE_QLIPHOTH
    if "cerebro" in consulta or "triuno" in consulta:
        return CEREBRO_TRIUNO
    if any(d in consulta for d in ["isis", "afrodita", "lilith", "artemisa"]):
        for nombre in ["isis", "afrodita", "lilith", "artemisa"]:
            if nombre in consulta:
                d = DEIDADES[nombre]
                return {
                    "direccion": d["direccion"],
                    "elemento":  d["elemento"],
                    "arbol":     d["arbol"],
                    "cerebro":   d["cerebro"],
                }
    return SISTEMA_META
