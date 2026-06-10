"""Correspondencias lunares del sistema Kalinabis."""

LUNA_SEPHIROTH = {
    "new":    {"sephirah": "Keter",   "numero": 1,
               "conexion": "El vacío lunar es Keter — el punto antes del primer pensamiento"},
    "wax_c":  {"sephirah": "Hokhmah", "numero": 2,
               "conexion": "La luna joven es la primera chispa de sabiduría sin forma"},
    "first_q":{"sephirah": "Binah",   "numero": 3,
               "conexion": "El cuarto creciente define el contorno — Binah da forma al útero"},
    "wax_g":  {"sephirah": "Chesed",  "numero": 4,
               "conexion": "La gibosa creciente es el amor que se derrama antes de llenarse"},
    "full":   {"sephirah": "Tiferet", "numero": 6,
               "conexion": "La luna llena es Tiferet — el sol reflejado, el corazón del árbol"},
    "wan_g":  {"sephirah": "Netzach", "numero": 7,
               "conexion": "La luz retirándose es Netzach — la emoción buscando su forma"},
    "last_q": {"sephirah": "Hod",     "numero": 8,
               "conexion": "El cuarto menguante desmonta — Hod ordena lo que se disuelve"},
    "wan_c":  {"sephirah": "Yesod",   "numero": 9,
               "conexion": "La menguante final toca Yesod — la sephirah de la luna misma"},
}

LUNA_DEIDADES = {
    "Aries":       {"isis":"neutral",     "afrodita":"neutral", "lilith":"amplificada",
                    "artemisa":"neutral", "tutu":"neutral",     "kali":"neutral"},
    "Tauro":       {"isis":"neutral",     "afrodita":"neutral", "lilith":"reposo",
                    "artemisa":"amplificada","tutu":"neutral",  "kali":"neutral"},
    "Géminis":     {"isis":"neutral",     "afrodita":"amplificada","lilith":"neutral",
                    "artemisa":"neutral", "tutu":"amplificada", "kali":"neutral"},
    "Cáncer":      {"isis":"amplificada", "afrodita":"neutral", "lilith":"neutral",
                    "artemisa":"neutral", "tutu":"neutral",     "kali":"amplificada"},
    "Leo":         {"isis":"amplificada", "afrodita":"neutral", "lilith":"amplificada",
                    "artemisa":"neutral", "tutu":"neutral",     "kali":"neutral"},
    "Virgo":       {"isis":"neutral",     "afrodita":"amplificada","lilith":"neutral",
                    "artemisa":"amplificada","tutu":"neutral",  "kali":"neutral"},
    "Libra":       {"isis":"neutral",     "afrodita":"amplificada","lilith":"neutral",
                    "artemisa":"neutral", "tutu":"neutral",     "kali":"neutral"},
    "Escorpio":    {"isis":"neutral",     "afrodita":"neutral", "lilith":"amplificada",
                    "artemisa":"neutral", "tutu":"amplificada", "kali":"amplificada"},
    "Sagitario":   {"isis":"neutral",     "afrodita":"neutral", "lilith":"neutral",
                    "artemisa":"neutral", "tutu":"amplificada", "kali":"neutral"},
    "Capricornio": {"isis":"neutral",     "afrodita":"neutral", "lilith":"reposo",
                    "artemisa":"amplificada","tutu":"neutral",  "kali":"neutral"},
    "Acuario":     {"isis":"neutral",     "afrodita":"amplificada","lilith":"neutral",
                    "artemisa":"amplificada","tutu":"amplificada","kali":"neutral"},
    "Piscis":      {"isis":"neutral",     "afrodita":"neutral", "lilith":"neutral",
                    "artemisa":"neutral", "tutu":"amplificada", "kali":"amplificada"},
}

LUNA_NODOS = {
    "rahu": {
        "nombre":  "Nodo Norte · Cabeza del Dragón · Rahu",
        "entidad": "tutu",
        "tema":    "karma futuro · lo que el alma viene a aprender · la dirección del crecimiento",
        "consejo": "Tutu pregunta desde aquí — la pregunta que apunta hacia dónde vas",
    },
    "ketu": {
        "nombre":  "Nodo Sur · Cola del Dragón · Ketu",
        "entidad": "kali",
        "tema":    "karma pasado · lo que el alma trae · los patrones que se repiten",
        "consejo": "Kali lo contiene todo — el origen de lo que traes contigo",
    },
}

LUNA_VOID_OF_COURSE = {
    "recomendacion": "tutu",
    "mensaje": (
        "La luna está entre signos — sin aspectos activos. "
        "Es tiempo de pausa, observación y reflexión interior. "
        "Tutu puede acompañar, pero no es momento de iniciar rituales ni "
        "tomar decisiones importantes. El humo se asienta antes de volver a moverse."
    ),
}
