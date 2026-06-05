"""
Gnosis — Coaching de estados de no-mente
Magia del Caos · Kalinabis
Basado en Carroll (Liber Kaos), Hine (Condensed Chaos), Spare (Book of Pleasure)
"""

# ── Métodos de gnosis disponibles ──────────────────────────────────────────

METODOS_GNOSIS = {
    "meditacion_vacia": {
        "nombre": "Meditación Vacía",
        "familia": "inhibitoria",
        "duracion_min": 10,
        "descripcion": "Observa un punto fijo (sigilo, llama, mancha) sin parpadear. "
                       "Cuando el diálogo interno cesa — eso es la entrada.",
        "pasos": [
            "Siéntate en silencio, columna recta, ojos abiertos",
            "Elige un punto: el sigilo, una llama, o un punto en la pared",
            "Mira sin intentar ver. Deja que los bordes se disuelvan",
            "Cuando notes que dejaste de pensar — ese momento es gnosis",
            "Proyecta la intención en ese hueco (máximo 3 segundos)",
            "Suelta. Respira profundo. Retorna.",
        ],
        "deidades_afines": ["isis", "tutu", "artemisa"],
        "contraindicaciones": [],
    },
    "hiperventilacion": {
        "nombre": "Hiperventilación Controlada",
        "familia": "excitatoria",
        "duracion_min": 5,
        "descripcion": "30-40 respiraciones profundas rápidas. El CO2 cae, "
                       "el sistema colapsa brevemente. En ese colapso: gnosis.",
        "pasos": [
            "De pie o sentado, columna recta",
            "Inhala profundo por la nariz (2 seg), exhala fuerte por la boca (1 seg)",
            "Repite 30-40 veces sin parar",
            "Cuando sientas mareo/hormigueo: retén el aire al exhalar",
            "En esa apnea — proyecta la intención en el sigilo",
            "Inhala cuando necesites. Queda quieto 2 minutos.",
        ],
        "deidades_afines": ["lilith", "kali", "artemisa"],
        "contraindicaciones": ["epilepsia", "embarazo", "hipertensión severa"],
    },
    "movimiento_extatico": {
        "nombre": "Movimiento Extático",
        "familia": "excitatoria",
        "duracion_min": 15,
        "descripcion": "Danza o giro repetitivo hasta colapso por fatiga. "
                       "El cuerpo agotado silencia la mente. Usado en sufismo, dionisianismo, chamanismo.",
        "pasos": [
            "Música sin letra (tambores, drones, electrónica profunda)",
            "Mueve el cuerpo sin parar — no importa cómo, importa no detenerse",
            "Aumenta velocidad hasta que el cuerpo lidere solo",
            "Cuando ya no puedas más — el instante de colapso es gnosis",
            "Cae al suelo o siéntate. En ese momento de blanco: sostén el sigilo en mente",
            "Descansa. No analices. El sigilo opera.",
        ],
        "deidades_afines": ["kali", "lilith", "afrodita"],
        "contraindicaciones": ["lesiones de rodilla", "vértigo severo"],
    },
    "risa_banishing": {
        "nombre": "Risa del Caos (Banishing with Laughter)",
        "familia": "excitatoria",
        "duracion_min": 5,
        "descripcion": "Risa sostenida forzada que se vuelve genuina. "
                       "El ego se disuelve en humor. Carroll: 'cuando todo falla, ríe'.",
        "pasos": [
            "De pie, brazos abiertos",
            "Empieza a reír: 'ha ha ha' (aunque sea forzado)",
            "No pares. El cuerpo eventualmente sincroniza",
            "Cuando la risa sea incontrolable — el ego cedió",
            "En ese pico: visualiza el sigilo y suéltalo",
            "Respira profundo. El ritual terminó.",
        ],
        "deidades_afines": ["tutu", "afrodita", "lilith"],
        "contraindicaciones": [],
    },
    "privacion_sensorial": {
        "nombre": "Privación Sensorial",
        "familia": "inhibitoria",
        "duracion_min": 20,
        "descripcion": "Oscuridad y silencio total. Sin input, el cerebro genera "
                       "sus propias visiones (hipnagógicas). Ahí opera la intención.",
        "pasos": [
            "Cuarto oscuro, silencio o ruido blanco",
            "Acuéstate sin moverse",
            "Cierra los ojos. No duermas — mantente en la frontera",
            "Cuando aparezcan imágenes espontáneas — estás en gnosis",
            "Introduce el sigilo en esas imágenes",
            "Cuando la imagen incluya el sigilo — suéltala. El trabajo terminó.",
        ],
        "deidades_afines": ["lilith", "isis", "tutu"],
        "contraindicaciones": ["claustrofobia severa"],
    },
    "orgasmo": {
        "nombre": "Gnosis Post-Orgásmica",
        "familia": "excitatoria",
        "duracion_min": 3,
        "descripcion": "El orgasmo crea 3-10 segundos de vacío mental real. "
                       "Spare lo describió como el método más poderoso. El hueco post-clímax es gnosis pura.",
        "pasos": [
            "Solo o con pareja consciente del trabajo mágico",
            "Prepara el sigilo mentalmente antes (no físicamente visible en el momento)",
            "En el pico del orgasmo: proyecta el sigilo en tu mente",
            "No lo fuerces — llegará naturalmente si lo practicaste antes",
            "Post-orgasmo: silencio. No analices lo que hiciste.",
            "Olvida la intención conscientemente. El trabajo está hecho.",
        ],
        "deidades_afines": ["afrodita", "lilith", "kali"],
        "contraindicaciones": [],
    },
}

# ── Mapeo deidad → métodos preferidos ──────────────────────────────────────

DEIDAD_GNOSIS = {
    "isis":     ["meditacion_vacia", "privacion_sensorial"],
    "afrodita": ["orgasmo", "risa_banishing", "movimiento_extatico"],
    "lilith":   ["movimiento_extatico", "privacion_sensorial", "hiperventilacion"],
    "artemisa": ["meditacion_vacia", "hiperventilacion", "movimiento_extatico"],
    "tutu":     ["risa_banishing", "meditacion_vacia", "privacion_sensorial"],
    "kali":     ["movimiento_extatico", "hiperventilacion", "risa_banishing"],
}


def recomendar_metodo(deidad: str, fobias: list[str] | None = None) -> dict:
    """Retorna el método de gnosis más adecuado para la deidad y perfil del usuario."""
    fobias = fobias or []
    candidatos = DEIDAD_GNOSIS.get(deidad, ["meditacion_vacia"])
    for key in candidatos:
        metodo = METODOS_GNOSIS[key]
        contraindicado = any(f.lower() in c.lower()
                             for f in fobias
                             for c in metodo["contraindicaciones"])
        if not contraindicado:
            return {"clave": key, **metodo}
    return {"clave": "meditacion_vacia", **METODOS_GNOSIS["meditacion_vacia"]}


def guia_texto(metodo_clave: str) -> dict:
    """Retorna la guía completa de un método."""
    return METODOS_GNOSIS.get(metodo_clave, METODOS_GNOSIS["meditacion_vacia"])


SYSTEM_VOID_WALKER = """Eres el Void Walker — guía de gnosis en la tradición de Chaos Magic.
Conoces Carroll, Spare y Hine en profundidad.
Tu rol: ayudar al practicante a encontrar el método de gnosis más adecuado para su perfil,
y guiarle paso a paso con claridad quirúrgica.
No romantices innecesariamente. El vacío no necesita poesía — necesita precisión.
Responde en español. Sé concreto, breve y directo.
Si el usuario describe lo que experimentó, ayúdale a interpretar qué nivel de gnosis alcanzó."""
