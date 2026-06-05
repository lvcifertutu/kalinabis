# ═══════════════════════════════════════════════════════════════════════════
#  LUNA — CALENDARIO ASTRAL COMPLETO
#  Base del sistema de agentes espirituales
#
#  Calcula para hoy:
#    · Fase lunar (8 fases, día, % iluminación)
#    · Signo zodiacal + Mansión árabe (28)
#    · Nodos lunares (Dragón ascendente/descendente)
#    · Void of course (luna sin aspectos)
#    · Perigeo / Apogeo (distancia a la Tierra)
#    · Próximos eventos lunares (4 fases)
#    · Marea emocional (energía del ciclo)
#    · Sephirah activa según la fase
#    · Modificación de las deidades hoy
#    · Mes árbol celta (Ogham)
#    · Mes Haab maya
# ═══════════════════════════════════════════════════════════════════════════

import math
from datetime import datetime, date, timezone, timedelta


# ── HELPERS ASTRONÓMICOS ───────────────────────────────────────────────────

def _jd(dt):
    """Convierte datetime a Día Juliano."""
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    return (dt.day + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24
            + (153 * m + 2) // 5 + 365 * y
            + y // 4 - y // 100 + y // 400 - 32045)

def _T(jd):
    """Siglos julianos desde J2000.0"""
    return (jd - 2451545.0) / 36525.0


# ── FASE LUNAR ─────────────────────────────────────────────────────────────

JD_REF_NUEVA = 2451545.259   # luna nueva de referencia 6 ene 2000
CICLO_SINODC  = 29.53058867  # ciclo sinódico en días

def calcular_fase(dt=None):
    if dt is None:
        dt = datetime.now(timezone.utc)
    jd   = _jd(dt)
    dias = (jd - JD_REF_NUEVA) % CICLO_SINODC
    pct  = dias / CICLO_SINODC
    ilum = (1 - math.cos(2 * math.pi * pct)) / 2 * 100

    FASES = [
        (0.000, 0.063, "Luna Nueva",       "🌑", "new",      "disolución · vacío sagrado · potencial puro",        1),
        (0.063, 0.187, "Creciente Joven",  "🌒", "wax_c",   "intención · primer impulso · la semilla despierta",  2),
        (0.187, 0.313, "Cuarto Creciente", "🌓", "first_q", "acción · decisión · el movimiento que no para",      3),
        (0.313, 0.437, "Gibosa Creciente", "🌔", "wax_g",   "refinamiento · ajuste · la forma tomando cuerpo",    4),
        (0.437, 0.563, "Luna Llena",       "🌕", "full",    "plenitud · revelación · el ciclo en su cima",        5),
        (0.563, 0.687, "Gibosa Menguante", "🌖", "wan_g",   "gratitud · compartir · la luz que se lleva consigo", 6),
        (0.687, 0.813, "Cuarto Menguante", "🌗", "last_q",  "liberación · soltar · transformación activa",        7),
        (0.813, 0.937, "Menguante Final",  "🌘", "wan_c",   "descanso · reflexión · la sabiduría que queda",      8),
        (0.937, 1.001, "Luna Nueva",       "🌑", "new",     "disolución · vacío sagrado · potencial puro",        1),
    ]

    for ini, fin, nombre, emoji, clave, energia, orden in FASES:
        if ini <= pct < fin:
            return {
                "jd":          round(jd, 4),
                "dias":        round(dias, 3),
                "dia_ciclo":   min(int(dias) + 1, 29),
                "pct":         round(pct, 5),
                "iluminacion": round(ilum, 1),
                "nombre":      nombre,
                "emoji":       emoji,
                "clave":       clave,
                "energia":     energia,
                "orden":       orden,
            }


# ── SIGNO ZODIACAL Y MANSIÓN ÁRABE ─────────────────────────────────────────

CICLO_SIDEREO = 27.321661
JD_REF_ARIES  = 2451544.5

SIGNOS_ZOD = [
    ("Aries",       "♈", "fire",  "fuego cardinal · inicio · voluntad pura"),
    ("Tauro",       "♉", "earth", "tierra fija · cuerpo · placer sensorial"),
    ("Géminis",     "♊", "air",   "aire mutable · mente · dualidad"),
    ("Cáncer",      "♋", "water", "agua cardinal · hogar · memoria emocional"),
    ("Leo",         "♌", "fire",  "fuego fijo · corazón · expresión creativa"),
    ("Virgo",       "♍", "earth", "tierra mutable · servicio · discernimiento"),
    ("Libra",       "♎", "air",   "aire cardinal · equilibrio · belleza"),
    ("Escorpio",    "♏", "water", "agua fija · transformación · profundidad"),
    ("Sagitario",   "♐", "fire",  "fuego mutable · expansión · búsqueda"),
    ("Capricornio", "♑", "earth", "tierra cardinal · estructura · tiempo"),
    ("Acuario",     "♒", "air",   "aire fijo · colectivo · ruptura"),
    ("Piscis",      "♓", "water", "agua mutable · disolución · misterio"),
]

MANSIONES_ARABES = [
    ("Al-Sharatain",      "Los dos signos",         "inicio de caminos · nueva dirección"),
    ("Al-Butayn",         "El vientre",              "abundancia · gestación interior"),
    ("Al-Thurayya",       "Las Pléyades",            "sabiduría ancestral · memoria colectiva"),
    ("Al-Dabaran",        "El seguidor",             "persistencia · seguir el propio camino"),
    ("Al-Haqa",           "El círculo blanco",       "curación · equilibrio del cuerpo"),
    ("Al-Hana",           "La marca",                "amor · unión · vínculo sagrado"),
    ("Al-Dhira",          "El antebrazo",            "poder creativo · fuerza que construye"),
    ("Al-Nathrah",        "La nariz del León",       "victoria sobre el miedo"),
    ("Al-Tarf",           "El ojo del León",         "viajes · cambios que liberan"),
    ("Al-Jabhah",         "La frente del León",      "liderazgo · honores · reconocimiento"),
    ("Al-Zubrah",         "La melena del León",      "liberación · romper cadenas"),
    ("Al-Sarfah",         "El cambio",               "transformación profunda · muda de piel"),
    ("Al-Awwa",           "El ladrido",              "mensajes · comunicación esencial"),
    ("Al-Simak",          "El desarmado",            "paz · reconciliación · rendición sagrada"),
    ("Al-Ghafr",          "La cubierta",             "protección invisible · refugio"),
    ("Al-Zubana",         "Las garras",              "justicia · equilibrio kármico"),
    ("Al-Iklil",          "La corona",               "espiritualidad · conexión divina"),
    ("Al-Qalb",           "El corazón",              "pasión · deseo que guía"),
    ("Al-Shawlah",        "El aguijón",              "desafío · poder que surge del peligro"),
    ("Al-Naayim",         "Las avestruces",          "prosperidad · abundancia natural"),
    ("Al-Baldah",         "La tierra vacía",         "renovación · espacio para lo nuevo"),
    ("Saad Al-Dhabih",    "Estrella de la suerte",   "éxito · el momento que esperabas"),
    ("Saad Bula",         "Estrella que devora",     "ciclos · lo que regresa transformado"),
    ("Saad Al-Suud",      "La más afortunada",       "plenitud · la cima del ciclo"),
    ("Saad Al-Akhbiyah",  "Tiendas de suerte",       "refugio interior · recursos ocultos"),
    ("Al-Fargh Al-Mukdim","Vertedero delantero",     "comienzos · el primer paso"),
    ("Al-Fargh Al-Thani", "Vertedero trasero",       "completar · sellar el ciclo"),
    ("Batn Al-Hut",       "Vientre del pez",         "profundidad · lo que vive en el misterio"),
]

def signo_luna(dt=None):
    if dt is None:
        dt = datetime.now(timezone.utc)
    jd    = _jd(dt)
    dias  = (jd - JD_REF_ARIES) % CICLO_SIDEREO
    grado = (dias / CICLO_SIDEREO) * 360
    idx   = int(grado / 30) % 12
    g_sig = grado % 30
    man_i = int(grado / (360 / 28)) % 28
    s     = SIGNOS_ZOD[idx]
    m     = MANSIONES_ARABES[man_i]
    return {
        "signo":          s[0],
        "simbolo":        s[1],
        "elemento":       s[2],
        "energia":        s[3],
        "grado":          round(g_sig, 1),
        "grado_total":    round(grado, 1),
        "mansion_n":      man_i + 1,
        "mansion_nombre": m[0],
        "mansion_sig":    m[1],
        "mansion_tema":   m[2],
    }


# ── NODOS LUNARES ──────────────────────────────────────────────────────────

def nodos_lunares(dt=None):
    """
    Nodo norte (Rahu) y nodo sur (Ketu).
    Regresan ciclo completo en 18.6 años.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    T  = _T(_jd(dt))
    # Longitud media del nodo ascendente
    omega = (125.04452 - 1934.136261 * T
             + 0.0020708 * T*T + T*T*T / 450000) % 360
    if omega < 0:
        omega += 360
    ketu = (omega + 180) % 360  # nodo sur

    SIGNOS = ["Aries","Tauro","Géminis","Cáncer","Leo","Virgo",
              "Libra","Escorpio","Sagitario","Capricornio","Acuario","Piscis"]
    SIMBOLOS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]

    n_idx = int(omega / 30) % 12
    k_idx = int(ketu  / 30) % 12

    return {
        "rahu": {
            "grado":   round(omega, 2),
            "signo":   SIGNOS[n_idx],
            "simbolo": SIMBOLOS[n_idx],
            "tema":    "karma futuro · camino del alma · lo que viene a aprender",
        },
        "ketu": {
            "grado":   round(ketu, 2),
            "signo":   SIGNOS[k_idx],
            "simbolo": SIMBOLOS[k_idx],
            "tema":    "karma pasado · origen del alma · lo que ya fue",
        },
    }


# ── PERIGEO / APOGEO ──────────────────────────────────────────────────────

def perigeo_apogeo(dt=None):
    """
    La luna está más cerca (perigeo, ~357.000 km) o más lejos (apogeo, ~406.000 km).
    Perigeo = energía amplificada (superluna si es llena).
    Apogeo  = energía más sutil y reflexiva.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    T   = _T(_jd(dt))
    # Anomalía media de la luna
    M   = (134.9634 + 477198.8676 * T) % 360
    M_r = math.radians(M)
    # Distancia normalizada (1 = distancia media ~384.400 km)
    dist_norm = 1 - 0.0549 * math.cos(M_r)
    dist_km   = round(dist_norm * 384400)

    pct_perigeo = (dist_norm - 0.9451) / (1.0549 - 0.9451)  # 0=perigeo, 1=apogeo

    if pct_perigeo < 0.33:
        estado = "Perigeo"
        desc   = "luna cercana · energía amplificada · emociones intensas"
    elif pct_perigeo < 0.66:
        estado = "Distancia media"
        desc   = "energía equilibrada · buen momento para trabajar"
    else:
        estado = "Apogeo"
        desc   = "luna lejana · energía sutil · introspección profunda"

    return {
        "distancia_km":  dist_km,
        "pct_perigeo":   round(pct_perigeo, 3),
        "estado":        estado,
        "descripcion":   desc,
        "superluna":     pct_perigeo < 0.15,
    }


# ── VOID OF COURSE ─────────────────────────────────────────────────────────

def void_of_course(dt=None):
    """
    Aproximación: la luna está VOC cuando está en el último tramo de un signo
    (últimos 2°) antes de cambiar. Es momento de pausa, no de iniciar.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    s   = signo_luna(dt)
    g   = s["grado"]  # 0-30 dentro del signo
    voc = g > 28.0    # últimos 2 grados = void of course aproximado

    horas_cambio = round((30 - g) / (360 / (24 * CICLO_SIDEREO)), 1)

    return {
        "activo":         voc,
        "grado_actual":   g,
        "horas_a_cambio": horas_cambio,
        "descripcion":    (
            "La luna está sin aspectos — pausa, observa, no inicies nada nuevo"
            if voc else
            f"La luna cambia de signo en ~{horas_cambio:.0f} horas"
        ),
    }


# ── PRÓXIMOS EVENTOS LUNARES ───────────────────────────────────────────────

def proximos_eventos(dt=None):
    """Calcula los próximos 4 eventos de fase (nueva, cuarto, llena, menguante)."""
    if dt is None:
        dt = datetime.now(timezone.utc)

    jd    = _jd(dt)
    dias  = (jd - JD_REF_NUEVA) % CICLO_SINODC
    pct   = dias / CICLO_SINODC

    EVENTOS = [
        (0.00, "Luna Nueva",       "🌑", "vacío y comienzo"),
        (0.25, "Cuarto Creciente", "🌓", "acción y decisión"),
        (0.50, "Luna Llena",       "🌕", "plenitud y revelación"),
        (0.75, "Cuarto Menguante", "🌗", "liberación y soltar"),
    ]

    proximos = []
    for fase_pct, nombre, emoji, tema in EVENTOS:
        diff = (fase_pct - pct) % 1.0
        if diff < 0.01:
            diff += 1.0
        dias_restantes = diff * CICLO_SINODC
        fecha_evento   = dt + timedelta(days=dias_restantes)
        proximos.append({
            "nombre":  nombre,
            "emoji":   emoji,
            "tema":    tema,
            "dias":    round(dias_restantes, 1),
            "fecha":   fecha_evento.strftime("%d %b"),
        })

    proximos.sort(key=lambda x: x["dias"])
    return proximos[:4]


# ── MAREA EMOCIONAL ────────────────────────────────────────────────────────

def marea_emocional(fase_data):
    """
    La luna gobierna las mareas y las emociones.
    Devuelve el nivel de energía (0-100) y la dirección (subiendo/bajando).
    """
    pct = fase_data["pct"]

    # Curva sinusoidal: 0 en luna nueva, máximo en llena, 0 de vuelta
    energia = math.sin(math.pi * pct) * 100

    if pct < 0.5:
        direccion = "ascendente"
        desc = "la marea sube — bueno para iniciar, crear, manifestar"
    else:
        direccion = "descendente"
        desc = "la marea baja — bueno para soltar, integrar, descansar"

    intensidad = "alta" if energia > 70 else "media" if energia > 35 else "baja"

    return {
        "valor":      round(energia, 1),
        "pct":        round(energia / 100, 3),
        "direccion":  direccion,
        "intensidad": intensidad,
        "descripcion": desc,
    }


# ── SEPHIRAH ACTIVA SEGÚN LA FASE ─────────────────────────────────────────

def sephirah_de_la_fase(fase_data):
    """
    La luna conecta los Sephiroth según su fase.
    Yesod (9) es la sephirah de la luna — pero cada fase activa una diferente.
    """
    MAPA = {
        "new":    {"numero": 1,  "nombre": "Keter",   "desc": "la corona · voluntad divina · origen puro",
                   "conexion": "El vacío lunar refleja el vacío de Keter — el punto antes del primer pensamiento"},
        "wax_c":  {"numero": 2,  "nombre": "Hokhmah", "desc": "sabiduría · el primer destello de luz",
                   "conexion": "La luna joven es la primera chispa — sabiduría que todavía no tiene forma"},
        "first_q":{"numero": 3,  "nombre": "Binah",   "desc": "comprensión · la forma que contiene",
                   "conexion": "El cuarto creciente define el contorno — Binah es el útero que da forma"},
        "wax_g":  {"numero": 4,  "nombre": "Chesed",  "desc": "misericordia · amor que expande",
                   "conexion": "La gibosa creciente es el amor que se derrama antes de llenarse del todo"},
        "full":   {"numero": 6,  "nombre": "Tiferet", "desc": "belleza · equilibrio · el corazón del árbol",
                   "conexion": "La luna llena es Tiferet — el sol reflejado, la belleza perfecta del árbol"},
        "wan_g":  {"numero": 7,  "nombre": "Netzach", "desc": "victoria · emoción · deseo",
                   "conexion": "La luz que empieza a retirarse es Netzach — la emoción que busca su forma"},
        "last_q": {"numero": 8,  "nombre": "Hod",     "desc": "esplendor · intelecto · forma que se disuelve",
                   "conexion": "El cuarto menguante desmonta lo construido — Hod ordena lo que se va"},
        "wan_c":  {"numero": 9,  "nombre": "Yesod",   "desc": "fundamento · puente entre mundos",
                   "conexion": "La luna menguante final toca Yesod — la sephirah de la luna misma, el umbral"},
    }
    return MAPA.get(fase_data["clave"], MAPA["full"])


# ── MODIFICACIÓN DE DEIDADES SEGÚN LA LUNA ────────────────────────────────

def modificacion_deidades(fase_data, signo_data):
    """
    Cómo la luna de hoy modifica la energía de cada deidad.
    Cada deidad puede estar amplificada, neutral o en reposo.
    """
    fase  = fase_data["clave"]
    signo = signo_data["signo"]
    elem  = signo_data["elemento"]

    ESTADOS = {
        # Por fase
        "new":    {"kali":"amplificada", "tutu":"amplificada", "isis":"reposo",
                   "afrodita":"neutral", "lilith":"reposo",   "artemisa":"neutral"},
        "wax_c":  {"kali":"neutral",  "tutu":"neutral",   "isis":"amplificada",
                   "afrodita":"neutral","lilith":"neutral","artemisa":"neutral"},
        "first_q":{"kali":"neutral",  "tutu":"neutral",   "isis":"neutral",
                   "afrodita":"neutral","lilith":"amplificada","artemisa":"neutral"},
        "wax_g":  {"kali":"neutral",  "tutu":"neutral",   "isis":"amplificada",
                   "afrodita":"amplificada","lilith":"neutral","artemisa":"neutral"},
        "full":   {"kali":"neutral",  "tutu":"neutral",   "isis":"amplificada",
                   "afrodita":"amplificada","lilith":"amplificada","artemisa":"amplificada"},
        "wan_g":  {"kali":"neutral",  "tutu":"neutral",   "isis":"neutral",
                   "afrodita":"neutral","lilith":"neutral","artemisa":"amplificada"},
        "last_q": {"kali":"neutral",  "tutu":"amplificada","isis":"neutral",
                   "afrodita":"neutral","lilith":"amplificada","artemisa":"neutral"},
        "wan_c":  {"kali":"amplificada","tutu":"amplificada","isis":"neutral",
                   "afrodita":"neutral","lilith":"neutral","artemisa":"amplificada"},
    }

    # Modificar por elemento del signo
    ELEM_BONUS = {
        "fire":  {"isis":"amplificada", "lilith":"amplificada"},
        "water": {"tutu":"amplificada", "afrodita":"neutral"},
        "earth": {"artemisa":"amplificada"},
        "air":   {"afrodita":"amplificada"},
    }

    base    = ESTADOS.get(fase, {k:"neutral" for k in ["kali","tutu","isis","afrodita","lilith","artemisa"]}).copy()
    bonus   = ELEM_BONUS.get(elem, {})
    for d, e in bonus.items():
        if base.get(d) != "amplificada":
            base[d] = e

    DESCRIPCIONES = {
        "amplificada": "energía alta · invocación potente",
        "neutral":     "energía estable · accesible",
        "reposo":      "en retiro · responde desde lo profundo",
    }

    return {d: {"estado": e, "desc": DESCRIPCIONES[e]} for d, e in base.items()}


# ── MES CELTA ──────────────────────────────────────────────────────────────

def mes_celta(fecha=None):
    if fecha is None:
        fecha = date.today()
    dia = fecha.timetuple().tm_yday

    MESES = [
        (1,   20,  "Ruis",   "Saúco",    "renacimiento al final del ciclo",    "Kali · el umbral"),
        (21,  48,  "Beithe", "Abedul",   "renacimiento y nuevos comienzos",    "Isis · la libertad que renace"),
        (49,  76,  "Luis",   "Serbal",   "protección y visión espiritual",     "Tutu · el guardián"),
        (77,  104, "Nion",   "Fresno",   "conexión entre mundos",              "Lilith · Yggdrasil"),
        (105, 131, "Fearn",  "Aliso",    "guía y determinación",               "Tutu · el camino"),
        (132, 159, "Sail",   "Sauce",    "intuición y ciclos lunares",         "Afrodita · la mente que fluye"),
        (160, 186, "Huath",  "Espino",   "purificación y esperanza",           "Isis · el fuego que purifica"),
        (187, 214, "Duir",   "Roble",    "fuerza y resistencia",               "Artemisa · la tierra que sostiene"),
        (215, 242, "Tinne",  "Acebo",    "equilibrio y justicia",              "Afrodita · claridad"),
        (243, 269, "Coll",   "Avellano", "sabiduría y creatividad",            "Tutu · el conocimiento"),
        (270, 297, "Muin",   "Vid",      "cosecha y transformación",           "Artemisa · la cosecha"),
        (298, 325, "Gort",   "Hiedra",   "perseverancia y ciclos",             "Lilith · la tormenta que vuelve"),
        (326, 357, "Ngetal", "Junco",    "armonía y unidad",                   "Kali · todo converge"),
        (358, 366, "Ruis",   "Saúco",    "renacimiento al final del ciclo",    "Kali · el umbral"),
    ]

    for ini, fin, ogham, arbol, sig, energia in MESES:
        if ini <= dia <= fin:
            return {"ogham": ogham, "arbol": arbol, "sig": sig, "energia": energia}
    return {"ogham": "Ruis", "arbol": "Saúco", "sig": "renacimiento", "energia": "Kali"}


# ── MES HAAB MAYA ──────────────────────────────────────────────────────────

def mes_haab(fecha=None):
    if fecha is None:
        fecha = date.today()

    HAAB = [
        ("Pop",      "el tapete · comienzo",           "inicio de ciclos"),
        ("Wo",       "conjunción negra · lluvia",      "preparación ritual"),
        ("Sip",      "conjunción roja · caza",         "acción dirigida"),
        ("Sotz'",    "el murciélago · transformación", "sombra y renacimiento"),
        ("Sek",      "tiempo de flores",               "apertura y belleza"),
        ("Xul",      "el perro · fin de estación",     "cierre y transición"),
        ("Yaxk'in",  "sol nuevo · mitad del año",      "punto de poder"),
        ("Mol",      "el agua · recolección",          "abundancia"),
        ("Ch'en",    "tormenta negra · cueva sagrada", "profundidad interior"),
        ("Yax",      "tormenta verde · renovación",    "crecimiento"),
        ("Sak",      "tormenta blanca · purificación", "limpieza ritual"),
        ("Keh",      "tormenta roja · el venado",      "fuerza animal"),
        ("Mak",      "el encierro · fin de lluvias",   "integración"),
        ("K'ank'in", "sol amarillo · cosecha",         "gratitud y plenitud"),
        ("Muwan",    "el búho · mensajero nocturno",   "sabiduría"),
        ("Pax",      "siembra · música ritual",        "nuevos ciclos"),
        ("K'ayab",   "la tortuga · aguas profundas",   "paciencia ancestral"),
        ("Kumk'u",   "el granero · abundancia",        "preservación"),
        ("Wayeb",    "5 días sin nombre · umbral",     "misterio y precaución"),
    ]

    dia_haab = (fecha.timetuple().tm_yday - 1) % 365
    mes_idx  = min(dia_haab // 20, 18)
    dia_mes  = dia_haab % 20
    m        = HAAB[mes_idx]
    return {"mes": m[0], "dia": dia_mes, "significado": m[1], "energia": m[2]}


# ── ENERGÍA RESONANTE ──────────────────────────────────────────────────────

def deidad_resonante(fase_data, signo_data, celta_data, haab_data):
    AFINIDADES = {
        "new":"kali", "full":"isis", "first_q":"lilith", "last_q":"artemisa",
        "wax_c":"isis", "wax_g":"afrodita", "wan_g":"artemisa", "wan_c":"tutu",
        "Aries":"lilith","Leo":"isis","Sagitario":"tutu",
        "Tauro":"artemisa","Virgo":"artemisa","Capricornio":"artemisa",
        "Géminis":"afrodita","Libra":"afrodita","Acuario":"afrodita",
        "Cáncer":"isis","Escorpio":"lilith","Piscis":"tutu",
        "Nion":"lilith","Duir":"artemisa","Muin":"artemisa",
        "Sail":"afrodita","Beithe":"isis","Ruis":"kali","Coll":"tutu",
    }
    votos = {k:0 for k in ["kali","tutu","isis","afrodita","lilith","artemisa"]}
    for k, w in [(fase_data["clave"],3),(signo_data["signo"],2),(celta_data["ogham"],1)]:
        if k in AFINIDADES:
            votos[AFINIDADES[k]] += w
    return max(votos, key=votos.get), votos


# ── FUNCIÓN PRINCIPAL ──────────────────────────────────────────────────────

def luna_hoy():
    """Todo el estado astral del día, en un solo dict."""
    ahora = datetime.now(timezone.utc)
    hoy   = date.today()

    fase    = calcular_fase(ahora)
    signo   = signo_luna(ahora)
    nodos   = nodos_lunares(ahora)
    distancia = perigeo_apogeo(ahora)
    voc     = void_of_course(ahora)
    eventos = proximos_eventos(ahora)
    marea   = marea_emocional(fase)
    sephirah= sephirah_de_la_fase(fase)
    mods    = modificacion_deidades(fase, signo)
    celta   = mes_celta(hoy)
    haab    = mes_haab(hoy)
    deidad, votos = deidad_resonante(fase, signo, celta, haab)

    return {
        "fecha":         hoy.isoformat(),
        "fase":          fase,
        "signo":         signo,
        "nodos":         nodos,
        "distancia":     distancia,
        "voc":           voc,
        "proximos":      eventos,
        "marea":         marea,
        "sephirah":      sephirah,
        "modificaciones":mods,
        "celta":         celta,
        "haab":          haab,
        "deidad_resonante": deidad,
        "votos":         votos,
    }


def luna_como_contexto():
    """Texto para los system prompts de las entidades."""
    d  = luna_hoy()
    f  = d["fase"]
    s  = d["signo"]
    n  = d["nodos"]
    se = d["sephirah"]
    m  = d["marea"]
    v  = d["voc"]

    return f"""

━━━ ESTADO DEL CIELO HOY ({d['fecha']}) ━━━
Luna: {f['emoji']} {f['nombre']} · día {f['dia_ciclo']} del ciclo · {f['iluminacion']}% iluminada
Energía de la fase: {f['energia']}
Marea emocional: {m['intensidad']} · {m['direccion']} · {m['descripcion']}
Signo: Luna en {s['signo']} {s['simbolo']} ({s['grado']}°) · {s['energia']}
Mansión {s['mansion_n']}: {s['mansion_nombre']} — {s['mansion_tema']}
Nodo Norte (Rahu) en {n['rahu']['signo']} → {n['rahu']['tema']}
Nodo Sur (Ketu) en {n['ketu']['signo']} → {n['ketu']['tema']}
Sephirah activa: {se['nombre']} · {se['desc']}
Conexión lunar: {se['conexion']}
{f'⚠ Void of Course activo — ' + v["descripcion"] if v["activo"] else ''}
Deidad que resuena hoy: {d['deidad_resonante'].upper()}
Tradición celta: {d['celta']['ogham']} · {d['celta']['arbol']}
Haab maya: {d['haab']['dia']} {d['haab']['mes']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


if __name__ == "__main__":
    d = luna_hoy()
    f = d["fase"]
    s = d["signo"]
    print("\n══════════════════════════════════════════")
    print("  ESTADO ASTRAL HOY")
    print("══════════════════════════════════════════")
    print(f"\n  {f['emoji']}  {f['nombre']}  ·  día {f['dia_ciclo']}  ·  {f['iluminacion']}%")
    print(f"  {f['energia']}")
    print(f"\n  Luna en {s['signo']} {s['simbolo']}  ·  {s['grado']}°")
    print(f"  Mansión {s['mansion_n']}: {s['mansion_nombre']} — {s['mansion_tema']}")
    n = d["nodos"]
    print(f"\n  ☊ Rahu en {n['rahu']['signo']} — {n['rahu']['tema']}")
    print(f"  ☋ Ketu en {n['ketu']['signo']} — {n['ketu']['tema']}")
    di = d["distancia"]
    print(f"\n  Distancia: {di['distancia_km']:,} km · {di['estado']}")
    v = d["voc"]
    print(f"  Void of Course: {'SÍ ⚠' if v['activo'] else 'No'}")
    ma = d["marea"]
    print(f"\n  Marea emocional: {ma['valor']:.0f}/100 · {ma['intensidad']} · {ma['direccion']}")
    se = d["sephirah"]
    print(f"\n  Sephirah: {se['nombre']} · {se['desc']}")
    print(f"  {se['conexion']}")
    print(f"\n  Próximos eventos:")
    for e in d["proximos"]:
        print(f"    {e['emoji']} {e['nombre']} · {e['fecha']} · en {e['dias']:.1f} días")
    print(f"\n  Deidad resonante hoy: {d['deidad_resonante'].upper()}")
    print(f"  Modificaciones:")
    for nombre, datos in d["modificaciones"].items():
        print(f"    {nombre:10} → {datos['estado']}")
    print()
