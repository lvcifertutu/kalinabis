"""Metadatos del sistema + árboles cósmicos de cada deidad."""

SISTEMA_META = {
    "nombre":    "Kalinabis",
    "tradicion": "Magia del caos — cosmología personal",
    "version":   "2.0 — grimorio como motor de transformación",
    "principio": "El sistema de creencias es la herramienta, no el contenido",
    "estados": {
        "espiritu": {
            "principio": "Taoismo",
            "entidad":   "Kali",
            "manifestacion": "el humo",
        },
        "alma": {
            "principio": "Chakras + Sephiroth + Qliphoth",
            "entidad":   "Tutu",
            "manifestacion": "la pregunta que sabe",
        },
        "cuerpo": {
            "principio": "Cerebro triuno + Mente colectiva",
            "entidades": ["Isis", "Afrodita", "Lilith", "Artemisa"],
            "manifestacion": "la experiencia vivida",
        },
    },
    "arboles": {
        "isis":     "Ished egipcio (Persea sagrada)",
        "afrodita": "Cosmos griego (olivo de Atenea)",
        "lilith":   "Yggdrasil nórdico (fresno cósmico, 9 mundos)",
        "artemisa": "Yaxché maya (Ceiba sagrada, 13 cielos + 9 niveles Xibalbá)",
    },
}

ARBOLES_DEIDADES = {
    "isis": {
        "nombre":   "Ished — La Persea Sagrada",
        "cultura":  "Antiguo Egipto",
        "especie":  "Persea (Mimusops Schimperi) — árbol de hojas perennes",
        "esencia":  "El árbol donde se escriben los destinos y se conoce el Plan Divino",
        "deidad_vinculo": "isis",
    },
    "afrodita": {
        "nombre":   "El Cosmos Helénico — El Olivo de Atenea",
        "cultura":  "Grecia Antigua",
        "especie":  "Olivo (Olea europaea) — árbol de Atenea, símbolo de sabiduría",
        "esencia":  "El universo en capas donde la mente puede ascender del olvido a la claridad suprema",
        "deidad_vinculo": "afrodita",
    },
    "lilith": {
        "nombre":   "Yggdrasil — El Fresno Cósmico",
        "cultura":  "Mitología Nórdica",
        "especie":  "Fresno (Fraxinus excelsior) — el árbol más grande del cosmos",
        "esencia":  "El árbol que contiene nueve mundos en caos permanente y sobrevive al fin del mundo",
        "deidad_vinculo": "lilith",
    },
    "artemisa": {
        "nombre":   "Yaxché — La Ceiba Sagrada",
        "cultura":  "Civilización Maya",
        "especie":  "Ceiba (Ceiba pentandra) — el árbol más alto de la selva maya",
        "esencia":  "El eje del cosmos que conecta 13 cielos, la tierra viva y 9 niveles del inframundo",
        "deidad_vinculo": "artemisa",
    },
}
