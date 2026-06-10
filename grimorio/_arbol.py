"""Mapas estructurales: chakras, sephiroth, qliphoth, cerebro triuno."""

CHAKRAS = {
    1: {"nombre": "Muladhara",    "ubicacion": "raíz",        "dominio": "supervivencia · seguridad · instinto"},
    2: {"nombre": "Svadhisthana", "ubicacion": "sacro",       "dominio": "creación · placer · emoción"},
    3: {"nombre": "Manipura",     "ubicacion": "plexo solar", "dominio": "voluntad · poder personal · acción"},
    4: {"nombre": "Anahata",      "ubicacion": "corazón",     "dominio": "amor · compasión · conexión"},
    5: {"nombre": "Vishuddha",    "ubicacion": "garganta",    "dominio": "expresión · verdad · comunicación"},
    6: {"nombre": "Ajna",         "ubicacion": "tercer ojo",  "dominio": "intuición · visión interior · claridad"},
    7: {"nombre": "Sahasrara",    "ubicacion": "corona",      "dominio": "conciencia pura · unión con el origen"},
}

CHAKRAS_ARTEMISA_SOCIAL = {
    1: "supervivencia tribal — el grupo que protege",
    2: "creatividad colectiva — el arte que une",
    3: "voluntad comunitaria — la acción coordinada",
    4: "amor universal — la compasión entre pueblos",
    5: "expresión cultural — el lenguaje compartido",
    6: "intuición colectiva — la sabiduría ancestral",
    7: "conciencia de especie — la mente que recuerda todo",
}

ARBOL_VIDA_SEPHIROTH = {
    1:  {"nombre": "Keter",   "significado": "corona — voluntad divina — el origen que quiere crear"},
    2:  {"nombre": "Hokhmah", "significado": "sabiduría — el primer destello de conciencia"},
    3:  {"nombre": "Binah",   "significado": "comprensión — la forma que contiene"},
    4:  {"nombre": "Chesed",  "significado": "misericordia — amor que expande"},
    5:  {"nombre": "Geburah", "significado": "fuerza — justicia que limita"},
    6:  {"nombre": "Tiferet", "significado": "belleza — equilibrio entre fuerzas"},
    7:  {"nombre": "Netzach", "significado": "victoria — emoción — deseo"},
    8:  {"nombre": "Hod",     "significado": "esplendor — intelecto — forma"},
    9:  {"nombre": "Yesod",   "significado": "fundamento — puente entre mundos"},
    10: {"nombre": "Malkuth", "significado": "reino — manifestación — la tierra"},
}

ARBOL_MUERTE_QLIPHOTH = {
    1:  {"nombre": "Thumiel",    "sombra_de": "Keter",   "significado": "dualidad — la unidad que se divide"},
    2:  {"nombre": "Ghagiel",    "sombra_de": "Hokhmah", "significado": "confusión del poder divino"},
    3:  {"nombre": "Sathariel",  "sombra_de": "Binah",   "significado": "ocultamiento — comprensión negada"},
    4:  {"nombre": "Gamchicoth", "sombra_de": "Chesed",  "significado": "devorador — misericordia distorsionada"},
    5:  {"nombre": "Golachab",   "sombra_de": "Geburah", "significado": "fuego incendiario — fuerza sin límite"},
    6:  {"nombre": "Thagirion",  "sombra_de": "Tiferet", "significado": "ego — autoexaltación — belleza corrompida"},
    7:  {"nombre": "A'arab Zaraq","sombra_de": "Netzach", "significado": "impulso caótico — deseo descontrolado"},
    8:  {"nombre": "Samael",     "sombra_de": "Hod",     "significado": "engaño — el intelecto que miente"},
    9:  {"nombre": "Gamaliel",   "sombra_de": "Yesod",   "significado": "ilusiones oscuras — sueños distorsionados"},
    10: {"nombre": "Lilith/Nehemoth", "sombra_de": "Malkuth", "significado": "sombra del reino — lo que no se ve en la tierra"},
}

CEREBRO_TRIUNO = {
    "reptiliano": {
        "descripcion": "instinto · supervivencia · territorialidad · ritual",
        "deidad_afinidad": "Lilith",
        "nota": "el más antiguo — actúa antes de que la mente piense",
    },
    "mamifero": {
        "descripcion": "emoción · vínculo · memoria afectiva · cuidado",
        "deidad_afinidad": "Isis",
        "nota": "el sistema límbico — donde vive el amor y el miedo",
    },
    "humano": {
        "descripcion": "razón · lenguaje · abstracción · planificación",
        "deidad_afinidad": "Afrodita",
        "nota": "el neocórtex — donde la mente puede observarse a sí misma",
    },
    "colectivo": {
        "descripcion": "inconsciente colectivo · arquetipos · memoria ancestral · conciencia social",
        "deidad_afinidad": "Artemisa",
        "nota": "el cuarto cerebro que MacLean no nombró — la mente de la especie",
    },
}
