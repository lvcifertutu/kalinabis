"""GrimorioMotor — motor de transformación.

Convierte (grimorio_mago + biblioteca + luna + esferas) en el contexto
de invocación de una entidad. Es el único lugar donde el lore de biblioteca
se teje con la configuración personal del mago.
"""

from __future__ import annotations


class GrimorioMotor:
    """Transforma el grimorio del mago en contexto de invocación."""

    @staticmethod
    def contexto_mago(grimorio: dict | None) -> str:
        """Genera el bloque de contexto del mago para el system prompt."""
        if not grimorio:
            return ""

        nombre = grimorio.get("nombre_mago", "").strip()
        intencion = grimorio.get("intencion", "").strip()
        arquetipo = grimorio.get("arquetipo", "").strip()
        elemento = grimorio.get("elemento", "").strip()
        sephira = grimorio.get("sephira_trabajo", "").strip()
        chakra = grimorio.get("chakra_activo", "").strip()

        atributos = {
            "voluntad":    grimorio.get("nivel_voluntad", 1),
            "intuicion":   grimorio.get("nivel_intuicion", 1),
            "sombra":      grimorio.get("nivel_sombra", 1),
            "manifestacion": grimorio.get("nivel_manifestacion", 1),
        }
        barra_atr = "  ".join(
            f"{k}: {'●' * v}{'○' * (10 - v)}"
            for k, v in atributos.items()
            if isinstance(v, int)
        )

        deidades_del_mago = grimorio.get("deidades", [])

        lineas = ["\n\n═══ GRIMORIO DEL MAGO ═══"]
        if nombre:
            lineas.append(f"Nombre mágico: {nombre}")
        if arquetipo:
            lineas.append(f"Arquetipo: {arquetipo}")
        if elemento:
            lineas.append(f"Elemento dominante: {elemento}")
        if sephira:
            lineas.append(f"Sephira de trabajo: {sephira}")
        if chakra:
            lineas.append(f"Chakra activo: {chakra}")
        if intencion:
            lineas.append(f"Intención de la esfera: {intencion}")
        if barra_atr:
            lineas.append(f"Atributos: {barra_atr}")
        if deidades_del_mago:
            lineas.append("Deidades de su esfera:")
            for d in deidades_del_mago[:6]:
                nombre_d = d.get("nombre_entidad", "")
                ctx = (d.get("contexto_personal") or "").strip()
                if ctx:
                    lineas.append(f"  · {nombre_d} — {ctx[:120]}")
                else:
                    lineas.append(f"  · {nombre_d}")

        lineas.append("═══════════════════════════\n")
        return "\n".join(lineas)

    @staticmethod
    def contexto_relacion_con_deidad(nombre_deidad: str, grimorio: dict | None) -> str:
        """Extrae el contexto personal del mago con esta deidad específica."""
        if not grimorio:
            return ""
        deidades = grimorio.get("deidades", [])
        for d in deidades:
            if d.get("nombre_entidad", "").lower() == nombre_deidad.lower():
                ctx = (d.get("contexto_personal") or "").strip()
                nombre_mago = grimorio.get("nombre_mago", "").strip()
                if ctx or nombre_mago:
                    partes = []
                    if nombre_mago:
                        partes.append(
                            f"\n\nEl practicante que te invoca se llama «{nombre_mago}» en esta esfera."
                        )
                    if ctx:
                        partes.append(
                            f"Su relación personal contigo: {ctx}"
                        )
                    return "".join(partes)
        if grimorio.get("nombre_mago"):
            return f"\n\nEl practicante que te invoca se llama «{grimorio['nombre_mago']}» en esta esfera."
        return ""

    @staticmethod
    def nombre_mago(grimorio: dict | None) -> str:
        if not grimorio:
            return ""
        return (grimorio.get("nombre_mago") or "").strip()
