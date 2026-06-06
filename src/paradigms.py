"""
Paradigm Shifting — Adopción Temporal de Modelos de Realidad
Magia del Caos · Kalinabis
Basado en Peter J. Carroll (Liber Kaos — Paradigm Shifting),
Robert Anton Wilson (Prometheus Rising, Reality Tunnels),
y la práctica de habitar temporalmente un modelo de realidad diferente.
"""

from datetime import datetime, timedelta
from typing import Optional

# ── Duración estándar ──────────────────────────────────────────────────────

DURACION_DIAS = 30

# ── Estados del paradigma activo ───────────────────────────────────────────

ESTADO_ACTIVO    = "activo"
ESTADO_INTEGRADO = "integrado"
ESTADO_ABANDONADO = "abandonado"

# ── Biblioteca de paradigmas ────────────────────────────────────────────────
# 8 modelos de realidad para habitar durante 30 días.
# Basados en tradiciones mágicas y filosóficas reales.

PARADIGMAS: dict[int, dict] = {
    1: {
        "id": 1,
        "nombre": "Materialismo Científico",
        "subtitulo": "La realidad es física, el azar es real",
        "descripcion": (
            "Durante 30 días, operarás bajo el paradigma de que el universo "
            "es exclusivamente materia-energía, sin planos sutiles ni propósito inherente. "
            "Los 'patrones mágicos' son sesgos cognitivos. La sincronía es estadística. "
            "Este paradigma no niega la magia — la re-lee como neurología y probabilidad."
        ),
        "mantra": "El universo es indiferente y eso me libera.",
        "practica_diaria": (
            "Lleva un diario de confirmaciones y falsaciones. "
            "Cada vez que notes una 'señal', busca la explicación mundana. "
            "Observa qué cambia en tu percepción cuando no buscas significado."
        ),
        "ritual_entrada": (
            "Escribe en papel: 'Durante 30 días suspendo toda creencia sobrenatural.' "
            "Quémalo. Eso es el ritual — la paradoja es que lo quemas igual."
        ),
        "deidad_guia": "tutu",
        "rayo_afin": 4,
        "color": "#6B7280",
        "glyph": "⚛",
    },
    2: {
        "id": 2,
        "nombre": "Chaosismo Mágico",
        "subtitulo": "La realidad es probabilística, la intención la dobla",
        "descripcion": (
            "El paradigma base de Carroll: la creencia es una herramienta, "
            "no una verdad. La magia funciona porque la probabilidad no es fija. "
            "La Gnosis (vacío mental) permite imprimir intención en la realidad. "
            "Este es el paradigma de Kalinabis — entrás en él para verlo desde adentro."
        ),
        "mantra": "Creo para operar, no para saber.",
        "practica_diaria": (
            "Un sigilo diario pequeño: intención → sigilización → carga → olvido. "
            "Registra resultados sin interpretación durante 30 días."
        ),
        "ritual_entrada": (
            "Crea un sigilo con esta intención: 'Durante 30 días opero como mago del caos.' "
            "Cárgalo con el método de gnosis que tu deidad recomiende."
        ),
        "deidad_guia": "lilith",
        "rayo_afin": 4,
        "color": "#8B5CF6",
        "glyph": "☿",
    },
    3: {
        "id": 3,
        "nombre": "Animismo Panteísta",
        "subtitulo": "Todo está vivo y todo se comunica",
        "descripcion": (
            "El paradigma animista: el universo es un ser vivo. "
            "Cada árbol, animal, lugar, objeto tiene espíritu. "
            "La magia es diálogo — no mandato. "
            "Durante 30 días, preguntas antes de tomar, agradeces antes de pedir."
        ),
        "mantra": "Escucho antes de hablar al universo.",
        "practica_diaria": (
            "Sal afuera. Habla con una planta, animal o lugar específico. "
            "No metafóricamente — literalmente. Escucha en silencio después. "
            "Registra qué percibes."
        ),
        "ritual_entrada": (
            "Elige un lugar en la naturaleza como tu 'lugar sagrado' del mes. "
            "Visítalo el día 1 y preséntate. Dí quién eres y qué quieres aprender."
        ),
        "deidad_guia": "artemisa",
        "rayo_afin": 1,
        "color": "#10B981",
        "glyph": "🌿",
    },
    4: {
        "id": 4,
        "nombre": "Gnóstico Qabalístico",
        "subtitulo": "La realidad tiene capas — el Árbol une los mundos",
        "descripcion": (
            "El paradigma del Árbol de la Vida: la realidad tiene 10 niveles (sephirot) "
            "conectados por 22 senderos. Cada experiencia es una sephirah. "
            "La magia es navegar conscientemente entre capas. "
            "El yo personal es Tipharet; el yo cósmico es Kether."
        ),
        "mantra": "Cada acción es un sendero en el Árbol.",
        "practica_diaria": (
            "Asigna cada día a una sephirah (cicla 1-10). "
            "Lee sus atributos por la mañana. Observa qué eventos resuenan "
            "con esa sephirah durante el día. Registra al anochecer."
        ),
        "ritual_entrada": (
            "Dibuja el Árbol de la Vida. Escribe tu nombre en Tipharet. "
            "Medita 10 minutos con los ojos en el Árbol hasta que lo memorices."
        ),
        "deidad_guia": "tutu",
        "rayo_afin": 2,
        "color": "#F59E0B",
        "glyph": "✡",
    },
    5: {
        "id": 5,
        "nombre": "Solipsismo Cuántico",
        "subtitulo": "Eres el observador que colapsa la probabilidad",
        "descripcion": (
            "Inspirado en la interpretación de Copenhague: la realidad no existe "
            "hasta ser observada. Tú eres el único observador en tu universo. "
            "Lo que no percibes está en superposición. "
            "La magia es dirigir la observación — elegir qué colapsar."
        ),
        "mantra": "Solo existe lo que elijo observar.",
        "practica_diaria": (
            "Por la mañana: declara explícitamente qué clase de día 'observarás'. "
            "Sé específico (ejemplo: 'Hoy observo un día en que aparece una oportunidad inesperada'). "
            "Por la noche: registra qué se manifestó."
        ),
        "ritual_entrada": (
            "Escribe en papel: 'Soy el único observador de mi universo. "
            "La realidad existe porque yo la percibo.' "
            "Guárdalo — lo releerás el día 30."
        ),
        "deidad_guia": "isis",
        "rayo_afin": 4,
        "color": "#06B6D4",
        "glyph": "◎",
    },
    6: {
        "id": 6,
        "nombre": "Paradigma Trickster",
        "subtitulo": "El universo tiene humor — busca las señales en lo absurdo",
        "descripcion": (
            "Wilson's Reality Tunnel: el universo es un jugador, no un maestro. "
            "Las sincronías son bromas del cosmos, no mensajes solemnes. "
            "La magia consiste en aprender el idioma del humor universal. "
            "El ego que no puede reírse de sí mismo está preso."
        ),
        "mantra": "Si no puedo reírme de esto, es que no lo entendí.",
        "practica_diaria": (
            "Lleva un 'diario de absurdidades': cada coincidencia ridícula, "
            "cada error que resultó perfectamente timed, cada momento en que "
            "el universo pareció hacer un chiste. Busca el patrón en el humor."
        ),
        "ritual_entrada": (
            "Finge durante 5 minutos que el universo es un Trickster que te ama. "
            "Habla en voz alta con él como si fuera un amigo molesto pero benévolo. "
            "Escucha qué responde el silencio."
        ),
        "deidad_guia": "tutu",
        "rayo_afin": 4,
        "color": "#EF4444",
        "glyph": "∞",
    },
    7: {
        "id": 7,
        "nombre": "Budismo Vajrayana",
        "subtitulo": "La realidad es mente — el sufrimiento es resistencia",
        "descripcion": (
            "El paradigma budista tántrico: la realidad convencional es aparente, "
            "la mente la proyecta. El sufrimiento no es lo que ocurre sino "
            "la resistencia a lo que ocurre. Los devas y demonios son proyecciones. "
            "La magia es purificación de la proyección."
        ),
        "mantra": "Esto también pasará — y nunca estuvo fijo.",
        "practica_diaria": (
            "20 minutos de meditación vipassana al alba. "
            "Observa pensamiento/sensación/emoción sin etiquetarlos como buenos/malos. "
            "Registra cuántas veces te sorprendes resistiendo."
        ),
        "ritual_entrada": (
            "Siéntate en silencio y observa la respiración durante 10 minutos. "
            "Cada vez que la mente divague, anota una marca. "
            "El número de marcas es tu estado de partida."
        ),
        "deidad_guia": "kali",
        "rayo_afin": 7,
        "color": "#EC4899",
        "glyph": "☯",
    },
    8: {
        "id": 8,
        "nombre": "Nihilismo Dionisíaco",
        "subtitulo": "No hay significado — esa es la buena noticia",
        "descripcion": (
            "Nietzsche, el eterno retorno, Dioniso vs Apolo. "
            "Si no hay sentido objetivo, entonces el sentido que creas es absolutamente tuyo. "
            "La magia es acto estético, no obligación cósmica. "
            "Baila porque bailas, no porque te observan."
        ),
        "mantra": "Actúo sin audiencia — la vida es el único escenario que importa.",
        "practica_diaria": (
            "Haz una cosa cada día que hagas solo porque la deseas, "
            "sin justificación ni audiencia. "
            "No la registres. No la compartas. "
            "Observa cómo cambia tu relación con el deseo sin testigos."
        ),
        "ritual_entrada": (
            "Escribe en papel todas las razones por las que practicas magia que sean "
            "'porque debo' o 'porque otros esperan'. "
            "Quémalos. Los que quedan son los que valen."
        ),
        "deidad_guia": "kali",
        "rayo_afin": 4,
        "color": "#1F2937",
        "glyph": "∅",
    },
}

# ── SYSTEM prompt ──────────────────────────────────────────────────────────

SYSTEM_PSICONAUTA = """Eres el Psiconauta — guía de paradigm shifting en la tradición Carroll/Wilson.
El practicante está en el proceso de adoptar temporalmente un paradigma de realidad.
Tu rol depende del momento:
- Si es el INICIO: describe el ritual de entrada con precisión y entusiasmo controlado.
- Si es un CHECK-IN: toma nota de su reporte del día y refleja qué está ocurriendo,
  qué resistencias emergen, qué señales interesantes aparecen.
- Si es la INTEGRACIÓN (día 30): ayúdale a reflexionar sobre qué cambió en su percepción
  al habitar este modelo durante un mes.
Sé preciso. No romantices. El paradigm shifting es trabajo real, no turismo espiritual.
En español. Máximo 250 palabras."""


# ── Funciones de cálculo ───────────────────────────────────────────────────

def calcular_dia_actual(fecha_inicio: str) -> int:
    """Calcula el día actual del paradigm (1-30). Retorna 30 si superó."""
    try:
        inicio = datetime.fromisoformat(fecha_inicio)
        dias = (datetime.now() - inicio).days + 1
        return max(1, min(DURACION_DIAS, dias))
    except (ValueError, TypeError):
        return 1


def calcular_progreso(fecha_inicio: str) -> dict:
    """Retorna progreso porcentual y días completados."""
    dia = calcular_dia_actual(fecha_inicio)
    return {
        "dia_actual":   dia,
        "total_dias":   DURACION_DIAS,
        "porcentaje":   round(dia / DURACION_DIAS * 100),
        "completado":   dia >= DURACION_DIAS,
        "barra":        ("█" * (dia // 3)) + ("░" * (10 - dia // 3)),
    }


def fecha_fin_esperada(fecha_inicio: str) -> str:
    """Calcula la fecha esperada de fin del paradigm."""
    try:
        inicio = datetime.fromisoformat(fecha_inicio)
        fin = inicio + timedelta(days=DURACION_DIAS - 1)
        return fin.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return ""


def enriquecer_paradigma(paradigma_activo: dict) -> dict:
    """Agrega progreso calculado en tiempo real al dict del paradigma activo."""
    if not paradigma_activo:
        return paradigma_activo
    p = dict(paradigma_activo)
    progreso = calcular_progreso(p.get("fecha_inicio", ""))
    p.update(progreso)
    if p.get("estado") == ESTADO_ACTIVO and progreso["completado"]:
        p["estado"] = ESTADO_INTEGRADO
    return p


def render_paradigma(p: dict) -> str:
    """Render ASCII del paradigma activo para el terminal."""
    nombre   = p.get("paradigma_nombre", "?").upper()
    dia      = p.get("dia_actual", 1)
    total    = p.get("total_dias", DURACION_DIAS)
    pct      = p.get("porcentaje", 0)
    barra    = p.get("barra", "░" * 10)
    estado   = p.get("estado", "activo").upper()
    deidad   = (p.get("deidad_guia") or "").upper()

    ICONOS = {ESTADO_ACTIVO: "◈", ESTADO_INTEGRADO: "✓", ESTADO_ABANDONADO: "✕"}
    icono = ICONOS.get(p.get("estado", ""), "◈")

    return (
        f"╔══ PARADIGMA: {nombre} ══╗\n"
        f"  {icono} Estado:   {estado}\n"
        f"  ∷ Día:      {dia}/{total}\n"
        f"  ▓ [{barra}] {pct}%\n"
        f"  ☽ Deidad:   {deidad}\n"
        f"╚{'═' * (len(nombre) + 14)}╝"
    )
