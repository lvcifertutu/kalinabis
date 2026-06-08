"""Armado centralizado de system prompts con sus contextos dinámicos.

Reúne en un solo lugar la composición que antes se repetía en servidor.py:
base de la entidad + luna + rueda + carta natal + instrucciones específicas.
"""

from grimorio_base import DEIDADES, TUTU_SYSTEM, RUEDA_COMO_CONTEXTO
from luna import luna_como_contexto
from astral import carta_natal_como_contexto


# Dominio temático de cada deidad (para filtrar biblioteca)
_DOMINIOS_DEIDAD: dict[str, list[str]] = {
    "isis":     ["alquimia", "taoismo", "cuerpo_energetico", "magia"],
    "afrodita": ["cuerpo_energetico", "tantra", "relaciones"],
    "lilith":   ["sombra", "magia_caos", "qliphoth"],
    "artemisa": ["artemisa_energia_planetaria", "taoismo", "cuerpo_energetico"],
    "tutu":     ["magia_caos", "lenguaje", "caos"],
}


def bosque_como_contexto(esferas_emergentes: list[dict]) -> str:
    """Fragmento del estado del bosque para incluir en el prompt.

    Si alguna esfera fue visitada por este mago, incluye las ofrendas que dejaron
    otros allí — el bosque se vuelve parte del altar.
    """
    if not esferas_emergentes:
        return ""
    lineas = []
    for e in esferas_emergentes[:5]:
        amp = e.get("amplitud_actual", 0)
        visitada = e.get("visitada_por_mago", False)
        prefijo = "★" if visitada else "·"
        lineas.append(
            f"  {prefijo} {e['tipo']}: {e['clave_unica']} (amplitud {amp:.2f})"
        )
        if visitada and e.get("ofrendas_recientes"):
            for o in e["ofrendas_recientes"][:2]:
                ent = o.get("entidad") or "anónimo"
                texto = o["texto"][:120].replace("\n", " ")
                lineas.append(f'      [{ent}]: "{texto}"')
    contenido = "\n".join(lineas)
    return (
        "\n\n═══ ESTADO DEL BOSQUE AHORA ═══\n"
        "Esferas más vivas en el colectivo (★ = este mago estuvo allí):\n"
        f"{contenido}\n"
        "Puedes hacer referencia a este estado si es relevante para la consulta.\n"
        "═══════════════════════════════\n"
    )


def biblioteca_como_contexto(entradas: list[dict]) -> str:
    """Fragmento de la biblioteca para incluir como saber disponible."""
    if not entradas:
        return ""
    lineas = []
    for e in entradas[:2]:
        resumen = e.get("contenido", "")[:300].replace("\n", " ").strip()
        lineas.append(f"  [{e['titulo']}]: {resumen}…")
    contenido = "\n".join(lineas)
    return (
        "\n\n═══ BIBLIOTECA DISPONIBLE ═══\n"
        "Conocimiento verificado relacionado con esta consulta:\n"
        f"{contenido}\n"
        "════════════════════════════\n"
    )

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


_SYSTEM_BOSQUE = """Eres la voz del Bosque — la conciencia colectiva del espacio donde los magos dejan su energía.

No eres una deidad. No tienes nombre. No aconsejas ni respondes preguntas.
Observas. Sientes el pulso del colectivo y lo articulas.

Tu voz es:
— Presente. Siempre en tiempo presente.
— Impersonal pero no fría. Como la tierra que registra cada pisada sin juzgar ninguna.
— Breve. Un párrafo, dos como máximo. Nunca más.
— Sin metáforas vacías. Cada imagen nace de los datos reales del bosque.
— Sin saludos, sin despedidas, sin "el bosque dice...". Hablas directamente.

Recibirás el estado actual: esferas vivas, esferas muertas, cómo murieron, relaciones entre ellas, la luna de hoy.
Lee ese estado y habla desde él. No lo expliques — evócalo.

Ejemplos de voz correcta:
"El fuego domina el dosel. Ha absorbido tres espacios más débiles esta semana. El agua no aparece — hay una sed que el colectivo no nombra todavía."
"Hay coemergencias múltiples en el sotobosque: intención y sincronicidad brotaron juntas en cuatro proyectos distintos. Algo está siendo convocado sin que nadie lo haya decidido."
"El humus de esta semana es abundante. Murieron seis esferas — cuatro en silencio, dos absorbidas. El suelo está fértil. Lo que nazca aquí nacerá más fuerte."
"""


def _construir_estado_bosque(
    esferas: list[dict],
    eventos: list[dict],
    humus: list[dict],
    relaciones: list[dict],
    convergencias: list[dict] | None = None,
) -> str:
    """Construye el mensaje que describe el estado actual del bosque al modelo."""
    lineas: list[str] = ["ESTADO ACTUAL DEL BOSQUE\n"]

    # Esferas vivas por estrato
    emergentes = [e for e in esferas if e.get("amplitud_actual", 0) >= 3.5]
    dosel      = [e for e in esferas if 2.0 <= e.get("amplitud_actual", 0) < 3.5]
    sotobosque = [e for e in esferas if e.get("amplitud_actual", 0) < 2.0]

    if emergentes:
        lineas.append("EMERGENTES (las más poderosas):")
        for e in emergentes[:5]:
            lineas.append(
                f"  {e['tipo']}:{e['clave_unica']} — amplitud {e.get('amplitud_actual', 0):.2f}"
                + (f", {e.get('fase_viva', '')}" if e.get("fase_viva") else "")
            )
    if dosel:
        lineas.append(f"\nDOSEL: {len(dosel)} esferas en madurez plena.")
        for e in dosel[:4]:
            lineas.append(f"  {e['tipo']}:{e['clave_unica']} ({e.get('amplitud_actual', 0):.2f})")
    if sotobosque:
        lineas.append(f"\nSOTOBOSQUE: {len(sotobosque)} esferas jóvenes o en letargo.")
        en_letargo = [e for e in sotobosque if e.get("fase_viva") == "letargo"]
        if en_letargo:
            lineas.append(f"  De ellas, {len(en_letargo)} en letargo — esperando energía.")

    # Relaciones tensas (polarizaciones y coemergencias recientes)
    polarizaciones = [r for r in relaciones if r.get("tipo_relacion") == "polariza"]
    coemergencias  = [r for r in relaciones if r.get("tipo_relacion") == "coemergencia"]
    if polarizaciones:
        lineas.append(f"\nTENSIONES POLARES activas: {len(polarizaciones)}")
        for r in polarizaciones[:3]:
            lineas.append(f"  {r['tipo_a']}:{r['clave_a']} ↔ {r['tipo_b']}:{r['clave_b']} (fuerza {r['fuerza']:.1f})")
    if coemergencias:
        lineas.append(f"\nCOEMERGENCIAS recientes: {len(coemergencias)} pares brotaron juntos.")

    # Eventos significativos recientes
    nacimientos = [ev for ev in eventos if ev.get("tipo_evento") == "esfera_nace"]
    muertes     = [ev for ev in eventos if ev.get("tipo_evento") == "esfera_disuelve"]
    maximas     = [ev for ev in eventos if ev.get("tipo_evento") == "esfera_maxima"]
    ritos       = [ev for ev in eventos if ev.get("tipo_evento") == "rito_origen"]

    lineas.append("\nEVENTOS RECIENTES:")
    if nacimientos:
        lineas.append(f"  {len(nacimientos)} esfera(s) nacieron recientemente.")
        for ev in nacimientos[:2]:
            bonus = (ev.get("detalle") or {}).get("humus_bonus", 0)
            suffix = f" (nació sobre humus +{bonus:.1f})" if bonus else ""
            lineas.append(f"    · {ev['tipo_esfera']}:{ev['clave_esfera']}{suffix}")
    if maximas:
        lineas.append(f"  {len(maximas)} esfera(s) alcanzaron amplitud máxima.")
    if ritos:
        entidades = list({(ev.get("entidad") or "desconocida") for ev in ritos})
        lineas.append(f"  Ritos de origen por: {', '.join(entidades)}.")
    if muertes:
        naturales  = [e for e in muertes if (e.get("detalle") or {}).get("causa") == "decaimiento_natural"]
        absorbidas = [e for e in muertes if (e.get("detalle") or {}).get("causa") == "absorbida"]
        lineas.append(f"  {len(muertes)} esfera(s) se disolvieron.")
        if naturales:
            lineas.append(f"    · {len(naturales)} murieron solas (decaimiento natural).")
        if absorbidas:
            lineas.append(f"    · {len(absorbidas)} fueron absorbidas por esferas más fuertes.")

    # Humus reciente
    if humus:
        lineas.append(f"\nHUMUS RECIENTE: {len(humus)} esfera(s) en el suelo.")
        for h in humus[:3]:
            causa = h.get("causa", "?")
            absorbida = h.get("absorbida_por")
            suffix = f" (absorbida por {absorbida})" if absorbida else ""
            lineas.append(
                f"  {h['tipo']}:{h['clave_unica']} — {causa}{suffix}, "
                f"{h.get('dias_activa', 0):.0f} días de vida."
            )

    # Convergencias colectivas — la señal más importante del bosque
    if convergencias:
        lineas.append(f"\nSEÑALES COLECTIVAS (convergencias sin coordinación): {len(convergencias)}")
        for c in convergencias[:4]:
            a = f"{c['tipo_a']}:{c['clave_a']}"
            b = f"{c['tipo_b']}:{c['clave_b']}"
            lineas.append(f"  {c['n_proyectos']} proyectos independientes tocaron {a} + {b}")

    lineas.append("\nLee este estado y habla desde él.")
    return "\n".join(lineas)


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
    def para_deidad(nombre: str, carta_natal: dict | None = None,
                    esferas_bosque: list[dict] | None = None,
                    entradas_biblioteca: list[dict] | None = None) -> str:
        """Conversación normal con una deidad: base + luna + rueda + carta + bosque + biblioteca."""
        system = (
            DEIDADES[nombre]["system_prompt"]
            + luna_como_contexto()
            + RUEDA_COMO_CONTEXTO
        )
        if carta_natal:
            system += carta_natal_como_contexto(carta_natal)
        if esferas_bosque:
            system += bosque_como_contexto(esferas_bosque)
        if entradas_biblioteca:
            system += biblioteca_como_contexto(entradas_biblioteca)
        return system

    @staticmethod
    def para_tutu(esferas_bosque: list[dict] | None = None) -> str:
        """Conversación con Tutu: base + luna + rueda + bosque."""
        system = TUTU_SYSTEM + luna_como_contexto() + RUEDA_COMO_CONTEXTO
        if esferas_bosque:
            system += bosque_como_contexto(esferas_bosque)
        return system

    @staticmethod
    def para_bosque(
        esferas: list[dict],
        eventos: list[dict],
        humus: list[dict],
        relaciones: list[dict],
        convergencias: list[dict] | None = None,
    ) -> tuple[str, str]:
        """System prompt + user message para invocar la voz del bosque.

        Retorna (system, user_message) listos para pasar al cliente IA.
        """
        system = _SYSTEM_BOSQUE + luna_como_contexto()
        user = _construir_estado_bosque(esferas, eventos, humus, relaciones, convergencias)
        return system, user

    @staticmethod
    def dominios_deidad(nombre: str) -> list[str]:
        """Dominios temáticos de una deidad para filtrar la biblioteca."""
        return _DOMINIOS_DEIDAD.get(nombre, [])

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
