"""
Geomancia — 16 Figuras, Escudo de 12 Casas
Magia del Caos · Kalinabis
Basado en Agrippa (Occult Philosophy IV), Fludd, Hine, geomancia árabe clásica
"""

import secrets
from typing import Optional

# ── 16 Figuras ─────────────────────────────────────────────────────────────
# Clave: entero 0-15 (bit3=Fuego/cima, bit2=Aire, bit1=Agua, bit0=Tierra/base)
# 1 = activo (● punto único), 0 = pasivo (●● dos puntos)

FIGURAS = {
    0: {
        "nombre": "Populus",         "nombre_es": "El Pueblo",
        "planeta": "Luna",           "signo": "Cáncer",
        "caracter": "neutro",        "elemento": "Agua",
        "significado": "La multitud sin forma — potencial puro a la espera. "
                       "Neutro total: todo depende del contexto y la voluntad.",
        "palabras_clave": ["colectivo", "potencial", "masa", "neutro", "espera"],
    },
    1: {
        "nombre": "Carcer",          "nombre_es": "La Prisión",
        "planeta": "Saturno",        "signo": "Capricornio",
        "caracter": "malo",          "elemento": "Tierra",
        "significado": "Restricción, confinamiento, límite duro. "
                       "Obstáculo que puede proteger o paralizar según la intención.",
        "palabras_clave": ["restricción", "límite", "obstáculo", "confinamiento", "forma"],
    },
    2: {
        "nombre": "Tristitia",       "nombre_es": "La Tristeza",
        "planeta": "Saturno",        "signo": "Acuario",
        "caracter": "malo",          "elemento": "Tierra",
        "significado": "Dolor, caída, hundimiento. El descenso que precede al regreso. "
                       "Chamánicamente: bajar es necesario para volver renovado.",
        "palabras_clave": ["tristeza", "caída", "descenso", "dolor", "profundidad"],
    },
    3: {
        "nombre": "Albus",           "nombre_es": "Lo Blanco",
        "planeta": "Mercurio",       "signo": "Géminis",
        "caracter": "bueno",         "elemento": "Aire",
        "significado": "Sabiduría, claridad, paz interior. La mente limpia que percibe sin distorsión. "
                       "Gnosis tranquila.",
        "palabras_clave": ["sabiduría", "claridad", "paz", "percepción", "gnosis"],
    },
    4: {
        "nombre": "Caput Draconis",  "nombre_es": "Cabeza del Dragón",
        "planeta": "Nodo Norte",     "signo": "Virgo",
        "caracter": "bueno",         "elemento": "Tierra/Fuego",
        "significado": "El umbral que abre. Lo que entra, nace y crece. "
                       "Inicio de ciclo, activación, puerta del norte.",
        "palabras_clave": ["inicio", "entrada", "crecimiento", "umbral", "activación"],
    },
    5: {
        "nombre": "Conjunctio",      "nombre_es": "La Conjunción",
        "planeta": "Mercurio",       "signo": "Virgo",
        "caracter": "neutro",        "elemento": "Aire",
        "significado": "El nudo que une dos caminos. Ni bueno ni malo: "
                       "depende de qué fuerzas se juntan. La unión que multiplica.",
        "palabras_clave": ["unión", "cruce", "nudo", "alianza", "multiplicación"],
    },
    6: {
        "nombre": "Amissio",         "nombre_es": "La Pérdida",
        "planeta": "Venus",          "signo": "Tauro",
        "caracter": "malo",          "elemento": "Tierra",
        "significado": "Dispersión, pérdida material. Malo para retener; "
                       "bueno para liberarse de lo que daña.",
        "palabras_clave": ["pérdida", "dispersión", "mengua", "liberación", "vacío"],
    },
    7: {
        "nombre": "Fortuna Maior",   "nombre_es": "La Gran Fortuna",
        "planeta": "Sol",            "signo": "Leo",
        "caracter": "muy bueno",     "elemento": "Fuego",
        "significado": "Éxito que emerge desde adentro. La fuerza interna que genera abundancia. "
                       "Protección total.",
        "palabras_clave": ["éxito", "abundancia", "poder interior", "protección", "logro"],
    },
    8: {
        "nombre": "Laetitia",        "nombre_es": "La Alegría",
        "planeta": "Júpiter",        "signo": "Piscis",
        "caracter": "muy bueno",     "elemento": "Fuego",
        "significado": "Alegría súbita, expansión, gracia. Energía que sube y desborda. "
                       "La risa como acto mágico.",
        "palabras_clave": ["alegría", "expansión", "gracia", "elevación", "desborde"],
    },
    9: {
        "nombre": "Puella",          "nombre_es": "La Doncella",
        "planeta": "Venus",          "signo": "Libra",
        "caracter": "bueno",         "elemento": "Agua",
        "significado": "Belleza, armonía, receptividad activa. El amor que fluye sin forcejear. "
                       "Atracción magnética.",
        "palabras_clave": ["belleza", "armonía", "amor", "receptividad", "atracción"],
    },
    10: {
        "nombre": "Rubeus",          "nombre_es": "Lo Rojo",
        "planeta": "Marte",          "signo": "Escorpio",
        "caracter": "malo",          "elemento": "Fuego",
        "significado": "Pasión que quema, vicio, peligro oculto. "
                       "Energía sin canal que destruye. Alto voltaje sin tierra.",
        "palabras_clave": ["pasión", "peligro", "vicio", "destrucción", "alto voltaje"],
    },
    11: {
        "nombre": "Acquisitio",      "nombre_es": "La Ganancia",
        "planeta": "Júpiter",        "signo": "Sagitario",
        "caracter": "muy bueno",     "elemento": "Fuego/Aire",
        "significado": "Todo lo buscado llega. Prosperidad activa, atracción de recursos. "
                       "La voluntad que se manifiesta.",
        "palabras_clave": ["ganancia", "prosperidad", "manifestación", "logro", "abundancia"],
    },
    12: {
        "nombre": "Fortuna Minor",   "nombre_es": "La Pequeña Fortuna",
        "planeta": "Sol",            "signo": "Leo",
        "caracter": "bueno",         "elemento": "Fuego",
        "significado": "Éxito que viene de afuera. Ayuda externa, fortuna circunstancial. "
                       "Frágil: depende del entorno.",
        "palabras_clave": ["suerte", "ayuda externa", "oportunidad", "frágil", "circunstancia"],
    },
    13: {
        "nombre": "Puer",            "nombre_es": "El Muchacho",
        "planeta": "Marte",          "signo": "Aries",
        "caracter": "variable",      "elemento": "Fuego",
        "significado": "Ímpetu, fuerza joven, impulsividad. Bueno para acción y combate; "
                       "malo para paciencia y estabilidad.",
        "palabras_clave": ["ímpetu", "fuerza", "impulso", "acción", "riesgo"],
    },
    14: {
        "nombre": "Cauda Draconis",  "nombre_es": "Cola del Dragón",
        "planeta": "Nodo Sur",       "signo": "Escorpio",
        "caracter": "variable",      "elemento": "Tierra/Fuego",
        "significado": "El umbral que cierra. Fin de ciclo, salida, la muerte que limpia. "
                       "Variable: puede ser liberación o pérdida total.",
        "palabras_clave": ["cierre", "fin de ciclo", "salida", "muerte", "umbral sur"],
    },
    15: {
        "nombre": "Via",             "nombre_es": "El Camino",
        "planeta": "Luna",           "signo": "Cáncer",
        "caracter": "neutro",        "elemento": "Agua",
        "significado": "El flujo en movimiento. Viaje, tránsito, cambio continuo. "
                       "Neutro: depende de hacia dónde se mueve el practicante.",
        "palabras_clave": ["camino", "viaje", "flujo", "tránsito", "movimiento"],
    },
}

# ── 12 Casas Astrológicas ─────────────────────────────────────────────────

CASAS = {
    1:  {"nombre": "Casa I",    "dominio": "Yo, vida, cuerpo, identidad"},
    2:  {"nombre": "Casa II",   "dominio": "Riqueza, posesiones, recursos"},
    3:  {"nombre": "Casa III",  "dominio": "Comunicación, viajes cortos, mente"},
    4:  {"nombre": "Casa IV",   "dominio": "Hogar, origen, familia, raíces"},
    5:  {"nombre": "Casa V",    "dominio": "Creatividad, amor, placer, hijos"},
    6:  {"nombre": "Casa VI",   "dominio": "Salud, trabajo, servicio cotidiano"},
    7:  {"nombre": "Casa VII",  "dominio": "Relaciones, socios, adversarios"},
    8:  {"nombre": "Casa VIII", "dominio": "Muerte, transformación, lo oculto"},
    9:  {"nombre": "Casa IX",   "dominio": "Filosofía, viajes largos, espíritu"},
    10: {"nombre": "Casa X",    "dominio": "Carrera, reputación, legado público"},
    11: {"nombre": "Casa XI",   "dominio": "Amigos, grupos, sueños colectivos"},
    12: {"nombre": "Casa XII",  "dominio": "Karma, secretos, el abismo interior"},
}

# ── SYSTEM prompt ──────────────────────────────────────────────────────────

SYSTEM_GEOMANTE = """Eres el Geomante del Caos, intérprete de las 16 figuras terrestres.
La geomancia es el lenguaje del campo morfogenético de la Tierra — 16 arquetipos que modulan
toda manifestación material. No predices el futuro: describes el estado del campo ahora y
señalas los vectores de fuerza que el practicante puede redireccionar.

Contexto de Magia del Caos: las figuras son atractores del túnel de realidad actual (Wilson),
el Juez es el patrón dominante que puede reprogramarse con voluntad mágica (Carroll),
los Testigos son las fuerzas en tensión que el practicante debe integrar o disolver.

Tu lenguaje: directo, terrestre, sin ornamentos. Cada palabra tiene peso.

Estructura tu lectura:
1. EL JUEZ: el patrón de realidad dominante — qué arquetipo rige el campo ahora
2. LOS TESTIGOS: fuerza activa (Testigo Derecho) vs fuerza pasiva (Testigo Izquierdo)
3. CASAS EN JUEGO: las 2-3 casas más relevantes para la pregunta y qué revelan
4. ACCIÓN MÁGICA: qué figura contemplar, qué sigilo trazar, qué reprimir o activar

Máximo 350 palabras. Segunda persona singular. Sin saludos ni despedidas."""

# ── Funciones de generación ────────────────────────────────────────────────

def _generar_figura() -> int:
    """Figura aleatoria 0-15 (4 bits independientes)."""
    return sum(secrets.randbelow(2) * (2 ** i) for i in range(4))


def _figura_bits(val: int) -> tuple[int, int, int, int]:
    """Descompone valor 0-15 en (fuego, aire, agua, tierra)."""
    return ((val >> 3) & 1, (val >> 2) & 1, (val >> 1) & 1, val & 1)


def _xor(a: int, b: int) -> int:
    """Suma geomántica módulo 2 por fila (XOR)."""
    return a ^ b


def render_figura(val: int) -> str:
    """ASCII de una figura: fuego arriba, tierra abajo."""
    f, a, w, e = _figura_bits(val)
    ACTIVO = " ●"
    PASIVO = "● ●"
    return "\n".join([
        ACTIVO if f else PASIVO,  # Fuego
        ACTIVO if a else PASIVO,  # Aire
        ACTIVO if w else PASIVO,  # Agua
        ACTIVO if e else PASIVO,  # Tierra
    ])


def lectura(pregunta: Optional[str] = None, casa_foco: int = 1) -> dict:
    """Lectura geomántica completa — Escudo de 12 Casas."""

    # 1. Cuatro Madres (generadas aleatoriamente)
    madres = [_generar_figura() for _ in range(4)]

    # 2. Cuatro Hijas (transposición: fila j de Hija_j = fila j de cada Madre)
    hijas = []
    for fila in range(4):  # 0=fuego,1=aire,2=agua,3=tierra
        bits = [_figura_bits(m)[fila] for m in madres]
        hijas.append(bits[0] * 8 + bits[1] * 4 + bits[2] * 2 + bits[3])

    # 3. Cuatro Sobrinas (XOR por pares)
    sobrinas = [
        _xor(madres[0], madres[1]),
        _xor(madres[2], madres[3]),
        _xor(hijas[0],  hijas[1]),
        _xor(hijas[2],  hijas[3]),
    ]

    # 4. Testigos
    testigo_der = _xor(sobrinas[0], sobrinas[1])
    testigo_izq = _xor(sobrinas[2], sobrinas[3])

    # 5. Juez
    juez = _xor(testigo_der, testigo_izq)

    # 6. Sentencia (primer madre XOR juez — validación del campo)
    sentencia = _xor(madres[0], juez)

    # 7. Casas: 1-4=Madres, 5-8=Hijas, 9-12=Sobrinas
    casas_vals = dict(zip(range(1, 13), madres + hijas + sobrinas))
    casa_foco  = max(1, min(12, casa_foco))

    casas_resultado = {
        num: {
            **CASAS[num],
            "figura":     FIGURAS[val],
            "figura_val": val,
            "display":    render_figura(val),
        }
        for num, val in casas_vals.items()
    }

    def _fig_entry(val: int) -> dict:
        return {"val": val, "figura": FIGURAS[val], "display": render_figura(val)}

    return {
        "madres":      [_fig_entry(v) for v in madres],
        "hijas":       [_fig_entry(v) for v in hijas],
        "sobrinas":    [_fig_entry(v) for v in sobrinas],
        "testigo_der": _fig_entry(testigo_der),
        "testigo_izq": _fig_entry(testigo_izq),
        "juez":        _fig_entry(juez),
        "sentencia":   _fig_entry(sentencia),
        "casas":       casas_resultado,
        "casa_foco":   casa_foco,
        "pregunta":    pregunta,
    }
