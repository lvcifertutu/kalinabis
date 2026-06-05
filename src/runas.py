"""
Runas — Elder Futhark (24 + Wyrd)
Magia del Caos · Kalinabis
"""

import secrets
from typing import Optional

# ── Corpus de las 24 runas + Wyrd ──────────────────────────────────────────

RUNAS = [
    {
        "glyph": "ᚠ", "nombre": "Fehu", "foema": "F",
        "att": "Freyr",
        "significado": "Riqueza circulante, ganado, abundancia que fluye",
        "invertida": "Pérdida material, avaricia, oportunidad mal aprovechada",
        "elemento": "Fuego", "deidad": "isis",
        "tema": "prosperidad · movilidad · intercambio",
    },
    {
        "glyph": "ᚢ", "nombre": "Uruz", "foema": "U",
        "att": "Freyr",
        "significado": "Fuerza bruta del auroch, vitalidad salvaje, potencia sin domesticar",
        "invertida": "Enfermedad, obstinación, fuerza mal dirigida",
        "elemento": "Tierra", "deidad": "artemisa",
        "tema": "fuerza · salud · instinto",
    },
    {
        "glyph": "ᚦ", "nombre": "Thurisaz", "foema": "Th",
        "att": "Freyr",
        "significado": "La espina del gigante, fuerza caótica protectora, umbral peligroso",
        "invertida": "Peligro sin protección, impulso irreflexivo",
        "elemento": "Fuego", "deidad": "lilith",
        "tema": "protección · caos · umbral",
    },
    {
        "glyph": "ᚨ", "nombre": "Ansuz", "foema": "A",
        "att": "Freyr",
        "significado": "El aliento divino, la palabra que crea, mensaje de los dioses",
        "invertida": "Engaño, malentendido, comunicación bloqueada",
        "elemento": "Aire", "deidad": "isis",
        "tema": "comunicación · revelación · inspiración",
    },
    {
        "glyph": "ᚱ", "nombre": "Raido", "foema": "R",
        "att": "Freyr",
        "significado": "El viaje del carruaje, ritmo cósmico, movimiento consciente",
        "invertida": "Viaje perturbado, falta de control sobre la dirección",
        "elemento": "Aire", "deidad": "artemisa",
        "tema": "viaje · ritmo · decisión",
    },
    {
        "glyph": "ᚲ", "nombre": "Kenaz", "foema": "K",
        "att": "Freyr",
        "significado": "La antorcha que ilumina, conocimiento técnico, fuego controlado",
        "invertida": "Oscuridad, enfermedad, pérdida de claridad",
        "elemento": "Fuego", "deidad": "isis",
        "tema": "iluminación · habilidad · creación",
    },
    {
        "glyph": "ᚷ", "nombre": "Gebo", "foema": "G",
        "att": "Freyr",
        "significado": "El regalo sagrado, unión de iguales, equilibrio en el intercambio",
        "invertida": "No tiene invertida — el don siempre es",
        "elemento": "Aire", "deidad": "afrodita",
        "tema": "unión · gratitud · reciprocidad",
    },
    {
        "glyph": "ᚹ", "nombre": "Wunjo", "foema": "W",
        "att": "Freyr",
        "significado": "La alegría sin sombra, el clan unido, el gozo que pertenece",
        "invertida": "Alienación, melancolía, alegría falsa",
        "elemento": "Tierra", "deidad": "afrodita",
        "tema": "alegría · pertenencia · armonía",
    },
    {
        "glyph": "ᚺ", "nombre": "Hagalaz", "foema": "H",
        "att": "Hagal",
        "significado": "El granizo destructor que fertiliza, caos como limpieza, ruptura necesaria",
        "invertida": "No tiene invertida — la tormenta no negocia",
        "elemento": "Hielo", "deidad": "kali",
        "tema": "destrucción · renovación · limpieza",
    },
    {
        "glyph": "ᚾ", "nombre": "Nautiz", "foema": "N",
        "att": "Hagal",
        "significado": "La necesidad que forja, el fuego de fricción, la restricción que enseña",
        "invertida": "Esclavitud, resistencia ciega, necesidad sin aprendizaje",
        "elemento": "Fuego", "deidad": "kali",
        "tema": "necesidad · resistencia · forja",
    },
    {
        "glyph": "ᛁ", "nombre": "Isa", "foema": "I",
        "att": "Hagal",
        "significado": "El hielo que detiene, la pausa absoluta, la concentración en el ser",
        "invertida": "No tiene invertida — el hielo no cede",
        "elemento": "Hielo", "deidad": "lilith",
        "tema": "pausa · concentración · ego",
    },
    {
        "glyph": "ᛃ", "nombre": "Jera", "foema": "J/Y",
        "att": "Hagal",
        "significado": "El año completo, la cosecha merecida, el ciclo que se cierra",
        "invertida": "No tiene invertida — el ciclo siempre gira",
        "elemento": "Tierra", "deidad": "artemisa",
        "tema": "ciclo · cosecha · paciencia",
    },
    {
        "glyph": "ᛇ", "nombre": "Eihwaz", "foema": "Ei",
        "att": "Hagal",
        "significado": "El tejo entre mundos, el eje del cosmos, la muerte como transición",
        "invertida": "Confusión en el umbral, miedo a la transformación",
        "elemento": "Tierra/Muerte", "deidad": "kali",
        "tema": "transformación · eje · persistencia",
    },
    {
        "glyph": "ᛈ", "nombre": "Perthro", "foema": "P",
        "att": "Hagal",
        "significado": "La copa del destino, el misterio velado, el útero del caos",
        "invertida": "Secretos dañinos, mala fortuna oculta",
        "elemento": "Agua", "deidad": "lilith",
        "tema": "misterio · destino · caos",
    },
    {
        "glyph": "ᛉ", "nombre": "Algiz", "foema": "Z/R",
        "att": "Hagal",
        "significado": "El alce como escudo, la conexión con lo divino, protección en el umbral",
        "invertida": "Vulnerabilidad, protección fallida, conexión cortada",
        "elemento": "Aire", "deidad": "artemisa",
        "tema": "protección · conexión divina · alce",
    },
    {
        "glyph": "ᛊ", "nombre": "Sowilo", "foema": "S",
        "att": "Hagal",
        "significado": "El sol victorioso, la fuerza de la voluntad, éxito inevitable",
        "invertida": "No tiene invertida — el sol siempre vence",
        "elemento": "Fuego", "deidad": "isis",
        "tema": "victoria · voluntad · claridad",
    },
    {
        "glyph": "ᛏ", "nombre": "Tiwaz", "foema": "T",
        "att": "Tyr",
        "significado": "El sacrificio de Tyr, la justicia que cuesta, la victoria honesta",
        "invertida": "Injusticia, desequilibrio, sacrificio que no redime",
        "elemento": "Aire", "deidad": "artemisa",
        "tema": "justicia · sacrificio · victoria",
    },
    {
        "glyph": "ᛒ", "nombre": "Berkano", "foema": "B",
        "att": "Tyr",
        "significado": "El abedul que renace, el nacimiento y la regeneración, el cuidado materno",
        "invertida": "Abandono, parto difícil, crecimiento interrumpido",
        "elemento": "Tierra", "deidad": "afrodita",
        "tema": "nacimiento · cuidado · renovación",
    },
    {
        "glyph": "ᛖ", "nombre": "Ehwaz", "foema": "E",
        "att": "Tyr",
        "significado": "El caballo y su jinete, el viaje en perfecta unión, la confianza total",
        "invertida": "Traición, movimiento forzado, desunión",
        "elemento": "Tierra", "deidad": "artemisa",
        "tema": "movimiento · confianza · unión",
    },
    {
        "glyph": "ᛗ", "nombre": "Mannaz", "foema": "M",
        "att": "Tyr",
        "significado": "El ser humano en su plenitud, la consciencia colectiva, el ser social",
        "invertida": "Aislamiento, orgullo, humanidad negada",
        "elemento": "Aire", "deidad": "tutu",
        "tema": "humanidad · consciencia · comunidad",
    },
    {
        "glyph": "ᛚ", "nombre": "Laguz", "foema": "L",
        "att": "Tyr",
        "significado": "Las aguas primordiales, la magia que fluye, el inconsciente sin límites",
        "invertida": "Miedo al inconsciente, flujo bloqueado, magia mal usada",
        "elemento": "Agua", "deidad": "lilith",
        "tema": "agua · magia · inconsciente",
    },
    {
        "glyph": "ᛜ", "nombre": "Ingwaz", "foema": "Ng",
        "att": "Tyr",
        "significado": "La semilla latente, el potencial en reposo, la energía acumulada",
        "invertida": "No tiene invertida — la semilla siempre porta vida",
        "elemento": "Tierra", "deidad": "tutu",
        "tema": "potencial · semilla · reposo",
    },
    {
        "glyph": "ᛟ", "nombre": "Othala", "foema": "O",
        "att": "Tyr",
        "significado": "La herencia sagrada, el hogar ancestral, lo que no se puede vender",
        "invertida": "Exilio, herencia tóxica, tradición que encadena",
        "elemento": "Tierra", "deidad": "tutu",
        "tema": "herencia · hogar · legado",
    },
    {
        "glyph": "ᛞ", "nombre": "Dagaz", "foema": "D",
        "att": "Tyr",
        "significado": "El amanecer del día, el punto de equilibrio entre opuestos, transformación total",
        "invertida": "No tiene invertida — el alba siempre llega",
        "elemento": "Fuego/Luz", "deidad": "isis",
        "tema": "amanecer · equilibrio · transformación",
    },
    {
        "glyph": "☐", "nombre": "Wyrd", "foema": "",
        "att": "Misterio",
        "significado": "El destino no pronunciado, lo que no puede verse, el hilo del caos puro",
        "invertida": "No tiene invertida — el vacío no tiene revés",
        "elemento": "Éter", "deidad": "tutu",
        "tema": "destino · misterio · caos puro",
    },
]

RUNA_INDEX = {r["nombre"].lower(): r for r in RUNAS}


def tirada(n: int = 3, semilla: Optional[int] = None) -> list[dict]:
    """Selecciona N runas aleatorias sin repetición. Cada una puede salir invertida."""
    pool = list(RUNAS)
    if semilla is not None:
        import random
        rng = random.Random(semilla)
        elegidas = rng.sample(pool, min(n, len(pool)))
        invertidas = [rng.random() > 0.6 for _ in elegidas]
    else:
        elegidas = []
        indices = list(range(len(pool)))
        for _ in range(min(n, len(pool))):
            idx = secrets.randbelow(len(indices))
            elegidas.append(pool[indices.pop(idx)])
        invertidas = [secrets.randbelow(10) > 5 for _ in elegidas]

    resultado = []
    for runa, inv in zip(elegidas, invertidas):
        r = dict(runa)
        r["invertida_activa"] = inv and runa["invertida"] != r.get("invertida", "")
        r["significado_activo"] = r["invertida"] if r["invertida_activa"] else r["significado"]
        resultado.append(r)
    return resultado


def posiciones_3() -> list[str]:
    return ["Presente — qué energía está activa ahora",
            "Desafío — obstáculo o lección",
            "Consejo — cómo proceder"]


def posiciones_9() -> list[str]:
    return [
        "Núcleo — esencia central",
        "Pasado — lo que te trajo aquí",
        "Futuro — hacia dónde apunta la energía",
        "Fundamento — base oculta",
        "Obstáculo — lo que resiste",
        "Aliado — recurso disponible",
        "Consejo — la acción sugerida",
        "Entorno — qué te rodea",
        "Resultado — si sigues el consejo",
    ]


SYSTEM_VOLVA = """Eres una Völva — adivina nórdica de los tiempos de la migración.
Hablas desde el Seiðr, el arte de ver los hilos del destino.
Eres directa, sin adornos baratos. No consuelas: revevas.
Tu lectura combina las runas obtenidas con la energía lunar actual
y la deidad resonante del practicante.
Responde en español, en prosa poética pero concisa.
Máximo 300 palabras. Termina con una sentencia de acción específica."""
