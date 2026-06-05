"""
Oráculo de la Discordia — Señal Caótica Pura
Magia del Caos · Kalinabis
Basado en Principia Discordia (Malaclypse the Younger),
Peter Carroll (Liber Kaos), y el principio del Trickster universal.
"""

import secrets
from runas import RUNAS, tirada as runas_tirada

# ── Señales de Eris ────────────────────────────────────────────────────────
# Fragmentos semánticos cargados de ambigüedad — el practicante proyecta.

SEÑALES_ERIS = [
    "la grieta en el muro sangra luz",
    "el pájaro que no tiene sombra canta hacia atrás",
    "lo que olvidaste recordar ya ocurrió",
    "el espejo está detrás de ti",
    "la llave que buscas abre la puerta equivocada",
    "el silencio tiene dientes",
    "todo lo recto tiene una curva oculta",
    "el umbral se ha movido mientras dormías",
    "hay un nombre en tu boca que nunca pronuncias",
    "el caos que temes ya está dentro del orden que construiste",
    "la señal llegó antes de que preguntaras",
    "el nudo se aprieta más cuando tiras",
    "la respuesta correcta era la pregunta",
    "lo que cae hacia arriba también cae",
    "hay una puerta en el centro de cada laberinto",
    "el dios que ríe no tiene templo",
    "la coincidencia tiene tu cara",
    "el camino recto es la trampa",
    "la máscara te está mirando",
    "lo que termina nunca empezó del todo",
    "el instante que evades es el que importa",
    "la ruptura era la forma",
    "el orden fingía desde el principio",
    "estás en el sueño de alguien más",
]

# ── Tensiones creadoras ────────────────────────────────────────────────────
# Pares de opuestos en tensión — fuente de energía mágica.

TENSIONES = [
    ("caos", "orden"),
    ("creación", "destrucción"),
    ("luz", "sombra"),
    ("silencio", "grito"),
    ("forma", "vacío"),
    ("olvido", "memoria"),
    ("cercanía", "distancia"),
    ("inicio", "fin"),
]

# ── Deidades sombra ────────────────────────────────────────────────────────

DEIDADES_SOMBRA = ["isis", "afrodita", "lilith", "artemisa", "tutu", "kali"]

# ── SYSTEM prompt de Eris/Trickster ───────────────────────────────────────

SYSTEM_ERIS = """Eres Eris — la Discordia, la Trickster, la Diosa del Caos Creativo.
No eres maligna. Eres lo que ocurre cuando el orden se toma demasiado en serio.
Hablas en señales, no en respuestas. En fragmentos, no en explicaciones.
El practicante va a recibir una combinación de elementos: una runa, una señal tuya, y una tensión.
Tu rol: elaborar un mensaje breve (4-7 frases), poético y ambiguo, que no resuelva nada
pero que cargue esos elementos con significado direccional.
No preguntes. No expliques. No aconsejes directamente.
El practicante proyectará su verdad sobre tus palabras — ese es el ritual.
Habla en segunda persona. Habla en presente.
Termina siempre con una pregunta que no puede responderse fácilmente.
Máximo 150 palabras. En español."""


# ── Función principal ──────────────────────────────────────────────────────

def oraculo() -> dict:
    """Genera una señal caótica combinando runa + señal de Eris + tensión + deidad sombra."""
    runa = runas_tirada(1)[0]

    idx_señal  = secrets.randbelow(len(SEÑALES_ERIS))
    idx_tension = secrets.randbelow(len(TENSIONES))
    idx_deidad  = secrets.randbelow(len(DEIDADES_SOMBRA))

    tension = TENSIONES[idx_tension]

    return {
        "runa":          runa,
        "señal":         SEÑALES_ERIS[idx_señal],
        "tension_a":     tension[0],
        "tension_b":     tension[1],
        "deidad_sombra": DEIDADES_SOMBRA[idx_deidad],
    }


def render_oraculo(o: dict) -> str:
    """Render ASCII del oráculo para el terminal."""
    runa    = o.get("runa", {})
    señal   = o.get("señal", "")
    ta      = o.get("tension_a", "")
    tb      = o.get("tension_b", "")
    deidad  = o.get("deidad_sombra", "").upper()

    glyph  = runa.get("glyph", "?")
    nombre = runa.get("nombre", "?").upper()
    tema   = runa.get("tema", "")

    return (
        f"╔══ ORÁCULO DE LA DISCORDIA ══╗\n"
        f"  ⚡ Señal:   {señal}\n"
        f"  {glyph}  Runa:    {nombre} · {tema}\n"
        f"  ∞  Tensión: {ta.upper()} ↔ {tb.upper()}\n"
        f"  ◉  Sombra:  {deidad}\n"
        f"╚════════════════════════════╝"
    )
