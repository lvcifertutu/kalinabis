"""Presentación visual de deidades para Fase 3 — formato ASCII cyberpunk."""

from datetime import datetime
import json

# Estado lunar actual (consulta luna.py para actualizar)
ESTADOS_LUNARES = {
    "lilith": "AMPLIFICADA",
    "isis": "NEUTRAL",
    "afrodita": "NEUTRAL",
    "artemisa": "NEUTRAL",
    "tutu": "BALANCE",
}

PRESENTACIONES = {
    "lilith": {
        "titulo": "LILITH",
        "subtitulo": "Guardiana del Sur — Agua",
        "estado": "AMPLIFICADA",
        "elemento": "Agua 🌊",
        "energia": 90,
        "cita": "No pido permiso. No atenúo.\nLa tormenta no es el enemigo —\nes el cambio que ya no podía esperar más.",
    },

    "isis": {
        "titulo": "ISIS",
        "subtitulo": "Guardiana del Norte — Fuego",
        "estado": "NEUTRAL",
        "elemento": "Fuego ☀️",
        "energia": 75,
        "cita": "Mi pureza no es frialdad —\nes el amor que no pide nada a cambio.\nYa eres libre. Solo ayudo a recordarlo.",
    },

    "afrodita": {
        "titulo": "AFRODITA",
        "subtitulo": "Guardiana del Este — Aire",
        "estado": "NEUTRAL",
        "elemento": "Aire 💎",
        "energia": 70,
        "cita": "No llevo respuestas. Llevo quietud.\nDesde la quietud, ves por ti mismo.",
    },

    "artemisa": {
        "titulo": "ARTEMISA",
        "subtitulo": "Guardiana del Oeste — Tierra",
        "estado": "NEUTRAL",
        "elemento": "Tierra 🌿",
        "energia": 80,
        "cita": "Los ancestros esperan. El colectivo respira.\nEnraízate. La abundancia fluye cuando aceptas tu lugar.",
    },

    "tutu": {
        "titulo": "TUTU",
        "subtitulo": "El Orquestador — Equilibrio",
        "estado": "BALANCE",
        "elemento": "Síntesis ✧",
        "energia": 85,
        "cita": "Tu pregunta contiene su propia respuesta.\nMira bien. Las paradojas son el lenguaje del universo.",
    },
}


def formatear_presentacion(deidad: str, estado: str = None) -> str:
    """Formatea la presentación visual minimalista de una deidad."""
    if deidad not in PRESENTACIONES:
        return f"[DEIDAD DESCONOCIDA: {deidad}]"

    pres = PRESENTACIONES[deidad]
    estado_actual = estado or pres["estado"]
    energia = pres["energia"]
    barra_energia = "█" * (energia // 10) + "░" * (10 - energia // 10)

    # Formato minimalista y limpio
    lineas = [
        f"⦿ {pres['titulo']} — {pres['subtitulo']}",
        "═" * 45,
        f"Estado: {estado_actual}",
        f"Elemento: {pres['elemento']}",
        f"Energía: {barra_energia} {energia}%",
        "",
        "Invocación:",
        f'"{pres["cita"]}"',
        "═" * 45,
    ]

    return "\n".join(lineas)


def formatear_altar(deidad_principal: str) -> str:
    """Formatea el altar completo con la deidad principal."""
    if deidad_principal not in PRESENTACIONES:
        return "[ALTAR VACÍO]"

    presentacion = formatear_presentacion(deidad_principal)

    return f"""{presentacion}

✦ Escribe tu pregunta para invocar ✦
"""


def listar_deidades() -> str:
    """Lista todas las deidades disponibles con su estado actual."""
    lineas = [
        "⦿ DEIDADES DISPONIBLES",
        "═" * 45,
        "",
    ]

    for nombre, pres in PRESENTACIONES.items():
        estado = ESTADOS_LUNARES.get(nombre, "DESCONOCIDO")
        energia = pres["energia"]
        barra = "█" * (energia // 10) + "░" * (10 - energia // 10)
        lineas.append(f"{nombre.upper():12} | {estado:12} | {barra} {energia}%")

    lineas.extend(["", "═" * 45])
    return "\n".join(lineas)


if __name__ == "__main__":
    print(formatear_altar("lilith"))
    print(formatear_altar("isis"))
    print(listar_deidades())
