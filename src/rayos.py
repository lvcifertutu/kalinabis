"""
8 Rayos del Octagram — Test de Afinidad Mágica
Magia del Caos · Kalinabis
Basado en Peter J. Carroll (Liber Kaos — The Octagram),
y la cartografía de tradiciones mágicas como caminos del practicante.
"""

# ── Los 8 Rayos del Octagram ───────────────────────────────────────────────
# Cada rayo es un conjunto de prácticas y orientaciones mágicas.
# Mapeados a deidades del grimorio para integración con el sistema.

OCTAGRAM: dict[int, dict] = {
    1: {
        "id": 1,
        "nombre": "Animismo",
        "direccion": "Norte",
        "glyph": "🌿",
        "deidades": ["artemisa"],
        "descripcion": (
            "El mundo está vivo y cada cosa tiene espíritu. "
            "Te comunicas con plantas, animales, lugares y fuerzas naturales. "
            "La magia es escucha antes que voluntad."
        ),
        "practicas": ["trabajo con espíritus de la naturaleza", "animismo vegetal",
                      "chamánico-animista", "totemismo", "magia de la tierra"],
        "virtud": "presencia",
        "sombra": "disolverse en el entorno, perder el yo practicante",
        "color": "#10B981",
    },
    2: {
        "id": 2,
        "nombre": "Qabalístico",
        "direccion": "Noreste",
        "glyph": "☽",
        "deidades": ["tutu", "isis"],
        "descripcion": (
            "El universo es un sistema de correspondencias. "
            "Árbol de la Vida, sephirot, ángeles, nombres divinos — "
            "la magia es geometría sagrada y vibración nominal."
        ),
        "practicas": ["Árbol de la Vida", "rituales de los sephirot",
                      "invocación angelical", "gematría", "magia cabalística"],
        "virtud": "orden en el caos",
        "sombra": "dogmatismo, perderse en el sistema",
        "color": "#F59E0B",
    },
    3: {
        "id": 3,
        "nombre": "Hermético",
        "direccion": "Este",
        "glyph": "♀",
        "deidades": ["afrodita", "isis"],
        "descripcion": (
            "Como es arriba es abajo. Alquimia, astrología, correspondencias herméticas. "
            "La magia es transmutación — de lo bruto a lo refinado, "
            "del plomo al oro, de la reacción a la elección."
        ),
        "practicas": ["alquimia interna", "astrología mágica",
                      "magia de correspondencias", "Hermes Trismegistus",
                      "visualización alquímica"],
        "virtud": "transmutación consciente",
        "sombra": "intelectualismo sin práctica encarnada",
        "color": "#F472B6",
    },
    4: {
        "id": 4,
        "nombre": "Caótico",
        "direccion": "Sureste",
        "glyph": "⚡",
        "deidades": ["lilith"],
        "descripcion": (
            "Todo modelo es provisional. El caos es la verdad subyacente. "
            "Paradigm shifting, gnosis súbita, descreer para creer. "
            "La magia es la voluntad sin dogma."
        ),
        "practicas": ["paradigm shifting", "chaos magic puro",
                      "sigilización de Spare", "gnosis excitatoria",
                      "meta-magia"],
        "virtud": "libertad radical",
        "sombra": "nihilismo sin ancla, desconexión de todo sistema",
        "color": "#EF4444",
    },
    5: {
        "id": 5,
        "nombre": "Sexual",
        "direccion": "Sur",
        "glyph": "✧",
        "deidades": ["afrodita", "kali"],
        "descripcion": (
            "La energía sexual es la fuerza mágica más directa. "
            "Tantra, gnosis post-orgásmica, polaridad erótica como combustible ritual. "
            "El cuerpo es el templo — el deseo, el sacerdote."
        ),
        "practicas": ["tantra mágico", "gnosis sexual (Spare)", "magia de pareja",
                      "transmutación libidinal", "magia de la kundalini inferior"],
        "virtud": "encarnación total",
        "sombra": "confundir el placer con el trabajo mágico",
        "color": "#EC4899",
    },
    6: {
        "id": 6,
        "nombre": "Enochiano",
        "direccion": "Suroeste",
        "glyph": "☥",
        "deidades": ["isis"],
        "descripcion": (
            "Los ángeles y las tablas enoquianas como mapa de la conciencia. "
            "Dee y Kelley, las aethyrs, las llamadas enoquianas. "
            "La magia es comunicación con lo radicalmente otro."
        ),
        "practicas": ["llamadas enoquianas", "visión y voz (Crowley/Neuburg)",
                      "work con aethyrs", "invocación angélica estructurada",
                      "magia de los 30 aethyrs"],
        "virtud": "apertura a lo desconocido",
        "sombra": "inflación mística, perderse en los aethyrs",
        "color": "#06B6D4",
    },
    7: {
        "id": 7,
        "nombre": "Tántrico",
        "direccion": "Oeste",
        "glyph": "☯",
        "deidades": ["kali"],
        "descripcion": (
            "El cuerpo-mente como instrumento. Kundalini, chakras, respiración. "
            "La magia no está afuera — está en la columna, en la respiración, "
            "en el sistema nervioso despertando."
        ),
        "practicas": ["trabajo con chakras", "pranayama mágico", "kundalini yoga",
                      "meditación vajrayana", "magia somática"],
        "virtud": "enraizamiento espiritual",
        "sombra": "bypassear la sombra psicológica mediante técnicas físicas",
        "color": "#A78BFA",
    },
    8: {
        "id": 8,
        "nombre": "Solar/Astral",
        "direccion": "Noroeste",
        "glyph": "☀",
        "deidades": ["isis", "artemisa"],
        "descripcion": (
            "El sol como dios vivo, los planos astrales como campo de operación. "
            "Proyección astral, trabajo con la carta natal como mapa del alma, "
            "magia de la luz solar y los ciclos cósmicos."
        ),
        "practicas": ["proyección astral", "magia solar", "trabajo con la carta natal",
                      "viaje de luz", "magia de los ciclos cósmicos"],
        "virtud": "visión panorámica",
        "sombra": "escapismo astral, evitar lo encarnado",
        "color": "#FDE68A",
    },
}

# ── Preguntas del test ─────────────────────────────────────────────────────
# Una pregunta por rayo. El practicante puntúa 1-5 su resonancia.

PREGUNTAS_TEST: list[dict] = [
    {
        "rayo_id": 1,
        "texto": "Cuando caminas por la naturaleza, ¿sientes que los árboles, "
                 "animales o lugares tienen presencia propia — como si te observaran "
                 "o quisieran comunicarse contigo?",
        "polo_bajo": "Los seres naturales son materia sin conciencia propia",
        "polo_alto": "Todo lo natural está vivo y se comunica si sabes escuchar",
    },
    {
        "rayo_id": 2,
        "texto": "¿Te atrae la idea de que el universo tiene una estructura oculta "
                 "—números, letras, geometrías— que, si descifras, te da acceso "
                 "a fuerzas más profundas?",
        "polo_bajo": "El universo es caos sin estructura significativa",
        "polo_alto": "El universo es un texto sagrado y la magia es aprenderlo",
    },
    {
        "rayo_id": 3,
        "texto": "¿Sientes que todo está conectado por correspondencias — "
                 "que un metal, un planeta, una planta y un estado emocional "
                 "vibran en la misma frecuencia — y que trabajar con uno afecta a los demás?",
        "polo_bajo": "Las correspondencias son poesía sin efecto real",
        "polo_alto": "Las correspondencias son la mecánica oculta de la realidad",
    },
    {
        "rayo_id": 4,
        "texto": "¿Cómo de cómodo/a te sientes descartando por completo un sistema "
                 "de creencias que te funciona y adoptando el opuesto solo para "
                 "ver qué te revela?",
        "polo_bajo": "Cambiar de paradigma me genera ansiedad o pérdida",
        "polo_alto": "Los modelos son herramientas; me los quito y me los pongo",
    },
    {
        "rayo_id": 5,
        "texto": "¿Consideras que la energía sexual o la atracción erótica "
                 "pueden ser canalizadas deliberadamente hacia trabajos creativos, "
                 "mágicos o transformativos?",
        "polo_bajo": "El sexo y lo espiritual son esferas separadas",
        "polo_alto": "El eros es la fuerza mágica más directamente disponible",
    },
    {
        "rayo_id": 6,
        "texto": "¿Te intriga la posibilidad de comunicarte con inteligencias "
                 "radicalmente no humanas — ángeles, demonios, entidades extradimensionales— "
                 "mediante rituales precisos y lenguajes especiales?",
        "polo_bajo": "Prefiero lo interno o lo natural — lo angélico me resulta ajeno",
        "polo_alto": "Lo radicalmente otro es lo más interesante de explorar",
    },
    {
        "rayo_id": 7,
        "texto": "¿Sientes que tu cuerpo — la respiración, la columna vertebral, "
                 "los estados de energía internos — es el instrumento mágico primario, "
                 "más que cualquier herramienta externa?",
        "polo_bajo": "Prefiero herramientas externas: símbolos, rituales, objetos",
        "polo_alto": "El cuerpo-mente bien alineado es el único templo necesario",
    },
    {
        "rayo_id": 8,
        "texto": "¿Te resulta natural pensar en términos de ciclos cósmicos, "
                 "planetas, eclipses y configuraciones astrales como fuerzas que "
                 "afectan tangiblemente tu estado interno y tu trabajo mágico?",
        "polo_bajo": "Los astros son distantes — no siento su influencia directa",
        "polo_alto": "Mi vida tiene ritmo cósmico y los ciclos solunares me sincronizan",
    },
]

# ── SYSTEM prompt ──────────────────────────────────────────────────────────

SYSTEM_ORACULO_RAYO = """Eres el Cartógrafo de los Rayos — un practicante veterano de Chaos Magic
que conoce en profundidad los 8 caminos del Octagram de Carroll.
El practicante acaba de completar el test de afinidad mágica.
Te llegan los resultados: su rayo natal (el de mayor puntuación) y su distribución.
Tu rol: describir al practicante qué significa su rayo natal para ellos específicamente,
qué prácticas tienen más probabilidad de resonar, qué sombra deben observar,
y qué deidad del grimorio es su guía natural.
Sé personal y directo. No generalices. Habla con ellos, no sobre el rayo.
En español. Máximo 250 palabras."""


# ── Funciones ─────────────────────────────────────────────────────────────

def calcular_rayo(respuestas: list[int]) -> int:
    """
    Dado un array de 8 puntuaciones (1-5, una por rayo en orden),
    retorna el id del rayo con mayor puntuación.
    En empate retorna el de menor id.
    """
    if len(respuestas) != 8:
        return 1
    scores = [(r if 1 <= r <= 5 else 1, idx + 1) for idx, r in enumerate(respuestas)]
    return max(scores, key=lambda x: x[0])[1]


def perfil_rayo(rayo_id: int) -> dict:
    """Retorna el perfil completo de un rayo."""
    return OCTAGRAM.get(rayo_id, OCTAGRAM[1])


def distribucion(respuestas: list[int]) -> list[dict]:
    """Retorna los 8 rayos con sus puntuaciones, ordenados de mayor a menor."""
    if len(respuestas) != 8:
        return []
    result = []
    for i, score in enumerate(respuestas):
        rayo = OCTAGRAM.get(i + 1, {})
        result.append({
            "rayo_id": i + 1,
            "nombre": rayo.get("nombre", ""),
            "glyph": rayo.get("glyph", ""),
            "score": max(1, min(5, score)),
            "deidades": rayo.get("deidades", []),
        })
    return sorted(result, key=lambda x: -x["score"])


def render_rayo(rayo: dict, score: int | None = None) -> str:
    """Render ASCII del rayo natal para el terminal."""
    nombre    = rayo.get("nombre", "?").upper()
    glyph     = rayo.get("glyph", "✦")
    direccion = rayo.get("direccion", "")
    deidades  = ", ".join(rayo.get("deidades", [])).upper()
    virtud    = rayo.get("virtud", "")
    score_str = f" · {score}/5" if score is not None else ""

    return (
        f"╔══ RAYO NATAL: {nombre} ══╗\n"
        f"  {glyph}  Dirección: {direccion}{score_str}\n"
        f"  ☽  Deidades:   {deidades}\n"
        f"  ✦  Virtud:     {virtud}\n"
        f"  ∿  Prácticas:  {', '.join(rayo.get('practicas', [])[:3])}\n"
        f"╚{'═' * (len(nombre) + 16)}╝"
    )
