"""
I Ching — Los 64 Hexagramas
Método de las 3 monedas. Magia del Caos · Kalinabis
Basado en Wilhelm/Baynes, correlacionado con Carroll (paradigma), Jung (sincronicidad)
"""

import secrets
from typing import Optional

# ── Trigramas base ─────────────────────────────────────────────────────────
# val = suma binaria de sus 3 líneas (bit0=inferior, bit2=superior)
# Yang=1, Yin=0

TRIGRAMAS = {
    0: {"glyph": "☷", "nombre": "Kun",  "atrib": "Tierra", "cualidad": "receptivo"},
    1: {"glyph": "☳", "nombre": "Zhen", "atrib": "Trueno", "cualidad": "movimiento"},
    2: {"glyph": "☵", "nombre": "Kan",  "atrib": "Agua",   "cualidad": "abismo"},
    3: {"glyph": "☱", "nombre": "Dui",  "atrib": "Lago",   "cualidad": "alegría"},
    4: {"glyph": "☶", "nombre": "Gen",  "atrib": "Montaña","cualidad": "quietud"},
    5: {"glyph": "☲", "nombre": "Li",   "atrib": "Fuego",  "cualidad": "claridad"},
    6: {"glyph": "☴", "nombre": "Sun",  "atrib": "Viento", "cualidad": "penetración"},
    7: {"glyph": "☰", "nombre": "Qian", "atrib": "Cielo",  "cualidad": "creativo"},
}

# ── 64 Hexagramas ─────────────────────────────────────────────────────────
# Clave: lower_val + upper_val * 8  (TRIGRAMAS keys)
# Orden King Wen. Cada entrada: num, nombre_zh, nombre, sup, inf, juicio, imagen, kw

HEXAGRAMAS = {
    63: {
        "num": 1,  "nombre_zh": "Qian",     "nombre": "Lo Creativo",
        "superior": 7, "inferior": 7,
        "juicio": "Lo Creativo obra excelso progreso. Fuerza pura, voluntad sin obstáculo.",
        "imagen": "Movimiento circular del cielo — el sabio se renueva sin cesar.",
        "palabras_clave": ["creación", "fuerza", "voluntad", "liderazgo", "persistencia"],
    },
    0: {
        "num": 2,  "nombre_zh": "Kun",      "nombre": "Lo Receptivo",
        "superior": 0, "inferior": 0,
        "juicio": "Éxito supremo a través de la receptividad. La yegua sigue, no conduce.",
        "imagen": "La tierra porta todo — virtud vasta que carga al mundo.",
        "palabras_clave": ["receptividad", "entrega", "nutrición", "sostén", "tierra"],
    },
    17: {
        "num": 3,  "nombre_zh": "Zhun",     "nombre": "La Dificultad Inicial",
        "superior": 2, "inferior": 1,
        "juicio": "Caos del comienzo — nubes sin lluvia aún. No actúes solo.",
        "imagen": "Nubes y trueno — dar orden a lo que empieza.",
        "palabras_clave": ["inicio", "caos", "potencial", "germinación", "aliados"],
    },
    34: {
        "num": 4,  "nombre_zh": "Meng",     "nombre": "La Insensatez Juvenil",
        "superior": 4, "inferior": 2,
        "juicio": "El ignorante busca al oráculo, no al revés. Primera consulta: respuesta.",
        "imagen": "Manantial bajo la montaña — formar el carácter con acción.",
        "palabras_clave": ["aprendizaje", "inexperiencia", "humildad", "enseñanza", "potencial"],
    },
    23: {
        "num": 5,  "nombre_zh": "Xu",       "nombre": "La Espera",
        "superior": 2, "inferior": 7,
        "juicio": "Nubes en el cielo pero sin llover aún. Fe interna mientras el tiempo madura.",
        "imagen": "Nubes sobre cielo — el sabio come, bebe y está alegre.",
        "palabras_clave": ["paciencia", "certeza", "timing", "fe", "nutrición"],
    },
    58: {
        "num": 6,  "nombre_zh": "Song",     "nombre": "El Conflicto",
        "superior": 7, "inferior": 2,
        "juicio": "Verdad bloqueada genera cautela. No llevar el conflicto hasta el final.",
        "imagen": "Cielo y agua en sentidos opuestos — ponderar bien al comenzar.",
        "palabras_clave": ["conflicto", "oposición", "arbitraje", "precaución", "litigio"],
    },
    2: {
        "num": 7,  "nombre_zh": "Shi",      "nombre": "El Ejército",
        "superior": 0, "inferior": 2,
        "juicio": "El ejército necesita disciplina y causa justa. Sin rectitud, derrota.",
        "imagen": "Agua sobre tierra — el sabio acepta al pueblo.",
        "palabras_clave": ["disciplina", "liderazgo", "organización", "causa", "masa"],
    },
    16: {
        "num": 8,  "nombre_zh": "Bi",       "nombre": "La Solidaridad",
        "superior": 2, "inferior": 0,
        "juicio": "La unión trae ventura. Examina si eres el centro correcto. Quien tarda queda fuera.",
        "imagen": "Agua sobre tierra — cultivar lealtad.",
        "palabras_clave": ["alianza", "unión", "lealtad", "comunidad", "convergencia"],
    },
    55: {
        "num": 9,  "nombre_zh": "Xiao Xu",  "nombre": "La Fuerza Domesticadora de lo Pequeño",
        "superior": 6, "inferior": 7,
        "juicio": "Las nubes se acumulan sin llover. El viento retiene al cielo. Pequeñas restricciones hoy.",
        "imagen": "Viento sobre cielo — refinar arte y virtud.",
        "palabras_clave": ["contención", "sutileza", "refinamiento", "acumulación", "espera"],
    },
    59: {
        "num": 10, "nombre_zh": "Lü",       "nombre": "La Conducta",
        "superior": 7, "inferior": 3,
        "juicio": "Pisar la cola del tigre — y el tigre no muerde. La forma correcta protege.",
        "imagen": "Cielo sobre lago — distinguir arriba y abajo.",
        "palabras_clave": ["conducta", "peligro consciente", "forma", "modales", "riesgo"],
    },
    7: {
        "num": 11, "nombre_zh": "Tai",      "nombre": "La Paz",
        "superior": 0, "inferior": 7,
        "juicio": "Lo pequeño se va, lo grande viene. Cielo y tierra en armonía.",
        "imagen": "Cielo y tierra unidos — ajustar el Tao de los opuestos.",
        "palabras_clave": ["armonía", "prosperidad", "unión", "intercambio", "florecimiento"],
    },
    56: {
        "num": 12, "nombre_zh": "Pi",       "nombre": "El Estancamiento",
        "superior": 7, "inferior": 0,
        "juicio": "Lo grande se va, lo pequeño viene. Cielo y tierra no se unen. Retiro es sabiduría.",
        "imagen": "Cielo sobre tierra separados — ocultar la virtud.",
        "palabras_clave": ["estancamiento", "bloqueo", "retiro", "preservación", "separación"],
    },
    61: {
        "num": 13, "nombre_zh": "Tong Ren", "nombre": "Comunidad con los Hombres",
        "superior": 7, "inferior": 5,
        "juicio": "Comunidad en lo abierto — perseverancia del superior. Fuego en el cielo.",
        "imagen": "Fuego bajo cielo — organizar clanes, discriminar entre seres.",
        "palabras_clave": ["fraternidad", "apertura", "causa común", "transparencia", "clan"],
    },
    47: {
        "num": 14, "nombre_zh": "Da You",   "nombre": "La Gran Posesión",
        "superior": 5, "inferior": 7,
        "juicio": "Éxito supremo. El fuego en lo alto del cielo ilumina todo.",
        "imagen": "Fuego sobre cielo — frenar el mal, promover el bien.",
        "palabras_clave": ["abundancia", "riqueza", "generosidad", "claridad", "esplendor"],
    },
    4: {
        "num": 15, "nombre_zh": "Qian",     "nombre": "La Modestia",
        "superior": 0, "inferior": 4,
        "juicio": "El superior lleva a término. La montaña se inclina bajo la tierra.",
        "imagen": "Montaña en seno de tierra — reducir lo excesivo, aumentar lo escaso.",
        "palabras_clave": ["humildad", "moderación", "equilibrio", "discreción", "mérito"],
    },
    8: {
        "num": 16, "nombre_zh": "Yu",       "nombre": "El Entusiasmo",
        "superior": 1, "inferior": 0,
        "juicio": "El trueno emerge de la tierra. Alegría que moviliza masas. Actuar con ímpetu.",
        "imagen": "Trueno de tierra — honrar la virtud con música.",
        "palabras_clave": ["entusiasmo", "movimiento", "impulso", "música", "detonación"],
    },
    25: {
        "num": 17, "nombre_zh": "Sui",      "nombre": "El Seguimiento",
        "superior": 3, "inferior": 1,
        "juicio": "Trueno en el lago — adaptación. Gran éxito siguiendo lo correcto.",
        "imagen": "Trueno en lago — al caer la noche, entrar y descansar.",
        "palabras_clave": ["adaptación", "seguimiento", "flexibilidad", "corriente", "descanso"],
    },
    38: {
        "num": 18, "nombre_zh": "Gu",       "nombre": "El Trabajo en lo Corrompido",
        "superior": 4, "inferior": 6,
        "juicio": "Viento bajo la montaña — lo corrompido debe restaurarse.",
        "imagen": "Viento bajo montaña — estimular al pueblo, nutrir la virtud.",
        "palabras_clave": ["restauración", "herencia", "trabajo", "corrección", "renovación"],
    },
    3: {
        "num": 19, "nombre_zh": "Lin",      "nombre": "El Acercamiento",
        "superior": 0, "inferior": 3,
        "juicio": "Tierra sobre lago — influencia ascendente. En el octavo mes vendrá el deterioro.",
        "imagen": "Lago bajo tierra — inagotable en enseñanza y cuidado.",
        "palabras_clave": ["aproximación", "influencia", "crecimiento", "autoridad", "ciclo"],
    },
    48: {
        "num": 20, "nombre_zh": "Guan",     "nombre": "La Contemplación",
        "superior": 6, "inferior": 0,
        "juicio": "Viento sobre tierra — observar antes de actuar. El lavado hecho, la ofrenda pendiente.",
        "imagen": "Viento sobre tierra — examinar al pueblo antes de actuar.",
        "palabras_clave": ["contemplación", "observación", "modelo", "mirada", "influencia"],
    },
    41: {
        "num": 21, "nombre_zh": "Shi He",   "nombre": "La Mordedura Tajante",
        "superior": 5, "inferior": 1,
        "juicio": "Trueno y relámpago — morder a través del obstáculo. Favorable dictar sentencia.",
        "imagen": "Trueno y relámpago — clarificar leyes, definir penas.",
        "palabras_clave": ["decisión", "justicia", "eliminación", "obstáculo", "resolución"],
    },
    37: {
        "num": 22, "nombre_zh": "Bi",       "nombre": "La Gracia",
        "superior": 4, "inferior": 5,
        "juicio": "La gracia tiene éxito en lo pequeño. No en asuntos grandes.",
        "imagen": "Fuego bajo montaña — clarificar asuntos sin decidir litigios.",
        "palabras_clave": ["gracia", "ornamento", "belleza", "forma", "apariencia"],
    },
    32: {
        "num": 23, "nombre_zh": "Bo",       "nombre": "La Desintegración",
        "superior": 4, "inferior": 0,
        "juicio": "Montaña sobre tierra — no actúes ahora. Fuerzas oscuras prevalecen. Aguarda.",
        "imagen": "Montaña sobre tierra — nutrir a los inferiores para estabilizarse.",
        "palabras_clave": ["desintegración", "derrumbe", "espera", "conservación", "oscuridad"],
    },
    1: {
        "num": 24, "nombre_zh": "Fu",       "nombre": "El Retorno",
        "superior": 0, "inferior": 1,
        "juicio": "Trueno bajo tierra — el solsticio. Un solo yang retorna. Sin error en ir y venir.",
        "imagen": "Trueno en tierra — cerrar pasos en el solsticio.",
        "palabras_clave": ["retorno", "renovación", "ciclo", "solsticio", "punto de inflexión"],
    },
    57: {
        "num": 25, "nombre_zh": "Wu Wang",  "nombre": "La Inocencia",
        "superior": 7, "inferior": 1,
        "juicio": "Trueno bajo cielo — actúa sin esperar frutos. Lo inocente no puede ser forzado.",
        "imagen": "Trueno bajo cielo — nutrir todo ser con estaciones correctas.",
        "palabras_clave": ["inocencia", "espontaneidad", "autenticidad", "naturalidad", "no-mente"],
    },
    39: {
        "num": 26, "nombre_zh": "Da Xu",    "nombre": "El Poder de Domar lo Grande",
        "superior": 4, "inferior": 7,
        "juicio": "Montaña sobre cielo — la fuerza acumulada. Favorable no comer en casa.",
        "imagen": "Cielo en seno de montaña — aprender los dichos de los antiguos.",
        "palabras_clave": ["acumulación", "contención", "potencia", "aprendizaje", "represamiento"],
    },
    33: {
        "num": 27, "nombre_zh": "Yi",       "nombre": "Las Comisuras",
        "superior": 4, "inferior": 1,
        "juicio": "Perseverancia trae ventura. Busca alimento correcto para cuerpo y espíritu.",
        "imagen": "Trueno bajo montaña — cuidar las palabras, moderar el comer.",
        "palabras_clave": ["nutrición", "discernimiento", "palabras", "alimento", "cuidado"],
    },
    30: {
        "num": 28, "nombre_zh": "Da Guo",   "nombre": "La Preponderancia de lo Grande",
        "superior": 3, "inferior": 6,
        "juicio": "La viga maestra flota — carga excesiva. Umbral de crisis. Actuar ahora.",
        "imagen": "Lago sobre madera — estar solo sin temor, retirarse sin pena.",
        "palabras_clave": ["exceso", "crisis", "umbral", "desbordamiento", "coraje"],
    },
    18: {
        "num": 29, "nombre_zh": "Kan",      "nombre": "Lo Abismal",
        "superior": 2, "inferior": 2,
        "juicio": "Abismo redoblado — sinceridad en el peligro. Fluir como el agua.",
        "imagen": "Agua que fluye sin cesar — actuar con virtud constante.",
        "palabras_clave": ["peligro", "abismo", "fluir", "constancia", "inmersión"],
    },
    45: {
        "num": 30, "nombre_zh": "Li",       "nombre": "Lo Adherente",
        "superior": 5, "inferior": 5,
        "juicio": "Fuego redoblado — adherirse a lo correcto da fruto.",
        "imagen": "Brillantez redoblada — perpetuar la luz en todas direcciones.",
        "palabras_clave": ["claridad", "adhesión", "dependencia", "iluminación", "brillo"],
    },
    28: {
        "num": 31, "nombre_zh": "Xian",     "nombre": "La Influencia",
        "superior": 3, "inferior": 4,
        "juicio": "Lago sobre montaña — mutua atracción. Mente vacía que recibe.",
        "imagen": "Lago sobre montaña — aceptar a la gente con mente abierta.",
        "palabras_clave": ["atracción", "influencia mutua", "sensibilidad", "apertura", "resonancia"],
    },
    14: {
        "num": 32, "nombre_zh": "Heng",     "nombre": "La Duración",
        "superior": 1, "inferior": 6,
        "juicio": "Trueno y viento — perseverancia sin errores. Movimiento constante.",
        "imagen": "Trueno y viento juntos — firmeza sin cambiar de dirección.",
        "palabras_clave": ["duración", "perseverancia", "constancia", "hábito", "continuidad"],
    },
    60: {
        "num": 33, "nombre_zh": "Dun",      "nombre": "El Retraimiento",
        "superior": 7, "inferior": 4,
        "juicio": "Éxito a través del retraimiento. Retroceder para avanzar.",
        "imagen": "Cielo bajo montaña — alejarse de lo vulgar sin hostilidad.",
        "palabras_clave": ["retirada", "estrategia", "preservación", "distancia", "timing"],
    },
    15: {
        "num": 34, "nombre_zh": "Da Zhuang","nombre": "El Poder de lo Grande",
        "superior": 1, "inferior": 7,
        "juicio": "Trueno en cielo — perseverancia ventajosa. El poder debe ir con la justicia.",
        "imagen": "Trueno sobre cielo — no actuar sin conformidad con el ritual.",
        "palabras_clave": ["poder", "fuerza", "impulso", "integridad", "avance"],
    },
    40: {
        "num": 35, "nombre_zh": "Jin",      "nombre": "El Progreso",
        "superior": 5, "inferior": 0,
        "juicio": "Fuego sobre tierra — avance claro como el sol al mediodía.",
        "imagen": "Fuego sobre tierra — aclararse con brillante virtud.",
        "palabras_clave": ["progreso", "avance", "reconocimiento", "claridad", "ascenso"],
    },
    5: {
        "num": 36, "nombre_zh": "Ming Yi",  "nombre": "El Oscurecimiento de la Luz",
        "superior": 0, "inferior": 5,
        "juicio": "La luz se hunde bajo la tierra — ocultar la brillantez en la adversidad.",
        "imagen": "Luz dentro de tierra — conducir a las masas ocultando el brillo.",
        "palabras_clave": ["oscurecimiento", "ocultación", "adversidad", "resiliencia", "sabiduría oculta"],
    },
    53: {
        "num": 37, "nombre_zh": "Jia Ren",  "nombre": "La Familia",
        "superior": 6, "inferior": 5,
        "juicio": "Viento desde fuego — cada uno en su lugar. La estructura sostiene.",
        "imagen": "Viento desde fuego — que las palabras tengan sustancia.",
        "palabras_clave": ["familia", "roles", "orden", "pertenencia", "estructura"],
    },
    43: {
        "num": 38, "nombre_zh": "Kui",      "nombre": "La Oposición",
        "superior": 5, "inferior": 3,
        "juicio": "Fuego sobre lago — en movimientos opuestos. En pequeñas cosas, buena fortuna.",
        "imagen": "Fuego sobre lago — mantener individualidad en comunión.",
        "palabras_clave": ["oposición", "contraste", "polaridad", "individualidad", "encuentro"],
    },
    20: {
        "num": 39, "nombre_zh": "Jian",     "nombre": "La Obstaculización",
        "superior": 2, "inferior": 4,
        "juicio": "Agua sobre montaña — el obstáculo revela el camino correcto. Volver sobre sí mismo.",
        "imagen": "Agua sobre montaña — cultivar la virtud en la dificultad.",
        "palabras_clave": ["obstáculo", "dificultad", "introspección", "pausa", "virtud"],
    },
    10: {
        "num": 40, "nombre_zh": "Jie",      "nombre": "La Liberación",
        "superior": 1, "inferior": 2,
        "juicio": "Trueno y lluvia — el nudo se desata. El sudoeste favorece.",
        "imagen": "Trueno y lluvia que se elevan — perdonar errores, absolver crímenes.",
        "palabras_clave": ["liberación", "solución", "perdón", "alivio", "desatadura"],
    },
    35: {
        "num": 41, "nombre_zh": "Sun",      "nombre": "La Disminución",
        "superior": 4, "inferior": 3,
        "juicio": "Lago bajo montaña — disminuir con sinceridad. La simplificación libera.",
        "imagen": "Lago bajo montaña — frenar la ira, restringir impulsos.",
        "palabras_clave": ["disminución", "simplificación", "sacrificio", "renuncia", "esencial"],
    },
    49: {
        "num": 42, "nombre_zh": "Yi",       "nombre": "El Aumento",
        "superior": 6, "inferior": 1,
        "juicio": "Viento y trueno — incremento. Cruzar las grandes aguas.",
        "imagen": "Viento y trueno — imitar el bien, corregir las faltas.",
        "palabras_clave": ["aumento", "beneficio", "generosidad", "flujo", "oportunidad"],
    },
    31: {
        "num": 43, "nombre_zh": "Guai",     "nombre": "El Desalojo",
        "superior": 3, "inferior": 7,
        "juicio": "Lago sobre cielo — decisión. Proclamar en la corte del rey. Resolver con determinación.",
        "imagen": "Lago sobre cielo — distribuir riqueza hacia abajo.",
        "palabras_clave": ["decisión", "resolución", "proclama", "ruptura", "valentía"],
    },
    62: {
        "num": 44, "nombre_zh": "Gou",      "nombre": "El Encuentro",
        "superior": 7, "inferior": 6,
        "juicio": "Viento bajo cielo — el encuentro inesperado. La fuerza pequeña no debe dominar.",
        "imagen": "Viento bajo cielo — el soberano emite mandatos a las cuatro regiones.",
        "palabras_clave": ["encuentro", "tentación", "oportunidad", "seducción", "inflexión"],
    },
    24: {
        "num": 45, "nombre_zh": "Cui",      "nombre": "La Reunión",
        "superior": 3, "inferior": 0,
        "juicio": "Lago sobre tierra — concentración de energía. El rey va al templo.",
        "imagen": "Lago sobre tierra — renovar las armas para lo imprevisible.",
        "palabras_clave": ["reunión", "concentración", "asamblea", "colectivo", "potencia"],
    },
    6: {
        "num": 46, "nombre_zh": "Sheng",    "nombre": "El Ascenso",
        "superior": 0, "inferior": 6,
        "juicio": "Viento dentro de tierra — el árbol empuja hacia arriba. Ascenso gradual.",
        "imagen": "Madera en tierra crece — acumular pequeñas virtudes hasta lo alto.",
        "palabras_clave": ["ascenso", "crecimiento", "esfuerzo graduado", "avance orgánico", "empuje"],
    },
    26: {
        "num": 47, "nombre_zh": "Kun",      "nombre": "La Miseria",
        "superior": 3, "inferior": 2,
        "juicio": "Lago sin agua — confinamiento. El superior puede morir en ello. No rendirse.",
        "imagen": "Lago sin agua — usar la vida para seguir la voluntad.",
        "palabras_clave": ["miseria", "agotamiento", "confinamiento", "voluntad", "resistencia"],
    },
    22: {
        "num": 48, "nombre_zh": "Jing",     "nombre": "El Pozo",
        "superior": 2, "inferior": 6,
        "juicio": "Viento bajo agua — el pozo que alimenta siempre. La fuente es inagotable.",
        "imagen": "Agua sobre madera — alentar al pueblo en su trabajo.",
        "palabras_clave": ["pozo", "fuente", "recurso inagotable", "comunidad", "profundidad"],
    },
    29: {
        "num": 49, "nombre_zh": "Ge",       "nombre": "La Revolución",
        "superior": 3, "inferior": 5,
        "juicio": "Fuego en lago — agua y fuego que se extinguen. El día consumado: fe suprema.",
        "imagen": "Fuego en lago — ordenar el calendario, clarificar estaciones.",
        "palabras_clave": ["revolución", "cambio radical", "transformación", "ruptura", "nuevo orden"],
    },
    46: {
        "num": 50, "nombre_zh": "Ding",     "nombre": "El Caldero",
        "superior": 5, "inferior": 6,
        "juicio": "Madera transformada en fuego — el sacrificio. Éxito supremo.",
        "imagen": "Fuego sobre madera — consolidar el destino sirviendo al espíritu.",
        "palabras_clave": ["transformación", "caldero", "alquimia", "sacrificio", "destino"],
    },
    9: {
        "num": 51, "nombre_zh": "Zhen",     "nombre": "Lo Perturbador",
        "superior": 1, "inferior": 1,
        "juicio": "Trueno redoblado — el choque llega. El sabio ríe en el horror y no derrama la ofrenda.",
        "imagen": "Trueno continuo — con temor examinar la vida y corregirse.",
        "palabras_clave": ["choque", "despertar", "miedo sagrado", "risa", "sacudida"],
    },
    36: {
        "num": 52, "nombre_zh": "Gen",      "nombre": "El Aquietamiento",
        "superior": 4, "inferior": 4,
        "juicio": "Montaña redoblada — quietud en el momento exacto. La espalda en reposo: sin yo.",
        "imagen": "Montañas unidas — no ir más allá de la posición.",
        "palabras_clave": ["quietud", "meditación", "límite", "presencia", "sin-ego"],
    },
    52: {
        "num": 53, "nombre_zh": "Jian",     "nombre": "El Desarrollo Gradual",
        "superior": 6, "inferior": 4,
        "juicio": "La oca migra gradualmente — progreso paso a paso. No forzar el ritmo.",
        "imagen": "Árbol sobre montaña — permanecer en virtud sublime.",
        "palabras_clave": ["desarrollo gradual", "proceso", "paciencia", "migración", "etapas"],
    },
    11: {
        "num": 54, "nombre_zh": "Gui Mei",  "nombre": "La Novia",
        "superior": 1, "inferior": 3,
        "juicio": "La novia en posición subordinada — acción trae desgracia. Relaciones mal fundadas.",
        "imagen": "Trueno sobre lago — conocer lo transitorio en lo permanente.",
        "palabras_clave": ["subordinación", "transitoriedad", "consecuencias", "rol", "ilusión"],
    },
    13: {
        "num": 55, "nombre_zh": "Feng",     "nombre": "La Abundancia",
        "superior": 1, "inferior": 5,
        "juicio": "Trueno y relámpago — abundancia en su cénit. Sé como el sol al mediodía.",
        "imagen": "Trueno y relámpago — decidir pleitos, ejecutar castigos.",
        "palabras_clave": ["abundancia", "plenitud", "cénit", "culminación", "peligro del éxito"],
    },
    44: {
        "num": 56, "nombre_zh": "Lü",       "nombre": "El Viajero",
        "superior": 5, "inferior": 4,
        "juicio": "Fuego sobre montaña — el extranjero en tierra ajena. Éxito moderado en lo pequeño.",
        "imagen": "Fuego sobre montaña — aplicar las penas con claridad.",
        "palabras_clave": ["viaje", "extranjero", "transitoriedad", "adaptación", "lejanía"],
    },
    54: {
        "num": 57, "nombre_zh": "Sun",      "nombre": "Lo Suave",
        "superior": 6, "inferior": 6,
        "juicio": "Viento redoblado — penetración suave. Pequeñas acciones constantes logran lo imposible.",
        "imagen": "Vientos que se siguen — reiterar los mandatos.",
        "palabras_clave": ["penetración", "suavidad", "influencia constante", "adaptación", "viento"],
    },
    27: {
        "num": 58, "nombre_zh": "Dui",      "nombre": "Lo Sereno",
        "superior": 3, "inferior": 3,
        "juicio": "Lago redoblado — la alegría que persevera. El intercambio crea alegría verdadera.",
        "imagen": "Lagos enlazados — unir amigos para hablar y practicar.",
        "palabras_clave": ["alegría", "intercambio", "amigos", "comunicación", "serenidad"],
    },
    50: {
        "num": 59, "nombre_zh": "Huan",     "nombre": "La Dispersión",
        "superior": 6, "inferior": 2,
        "juicio": "Viento sobre agua — el obstáculo se disuelve. El rey va al templo.",
        "imagen": "Viento sobre agua — ofrecer sacrificios para unir a todos.",
        "palabras_clave": ["dispersión", "disolución", "liberación", "reunión", "flujo"],
    },
    19: {
        "num": 60, "nombre_zh": "Jie",      "nombre": "La Limitación",
        "superior": 2, "inferior": 3,
        "juicio": "Agua sobre lago — la limitación correcta. Restricciones amargas no perseveran.",
        "imagen": "Lago sobre agua — crear número, medida y estándar de virtud.",
        "palabras_clave": ["límite", "moderación", "articulación", "medida", "restricción"],
    },
    51: {
        "num": 61, "nombre_zh": "Zhong Fu", "nombre": "La Verdad Interior",
        "superior": 6, "inferior": 3,
        "juicio": "Viento sobre lago — la confianza central irradia hacia fuera.",
        "imagen": "Viento sobre lago — deliberar con cuidado los casos capitales.",
        "palabras_clave": ["verdad interior", "confianza", "convicción", "centro", "resonancia"],
    },
    12: {
        "num": 62, "nombre_zh": "Xiao Guo", "nombre": "La Preponderancia de lo Pequeño",
        "superior": 1, "inferior": 4,
        "juicio": "Trueno sobre montaña — el pájaro en vuelo. No es tiempo de grandes acciones.",
        "imagen": "Trueno sobre montaña — exceder en reverencia, en dolor, en economía.",
        "palabras_clave": ["pequeñas acciones", "exceso moderado", "precaución", "detalle", "humildad"],
    },
    21: {
        "num": 63, "nombre_zh": "Ji Ji",    "nombre": "Después de la Consumación",
        "superior": 2, "inferior": 5,
        "juicio": "Agua sobre fuego — todo en orden. Éxito en lo pequeño. El caos acecha tras el logro.",
        "imagen": "Agua sobre fuego — reflexionar sobre el mal, impedir su llegada.",
        "palabras_clave": ["completitud", "orden", "vigilancia", "transición", "después del logro"],
    },
    42: {
        "num": 64, "nombre_zh": "Wei Ji",   "nombre": "Antes de la Consumación",
        "superior": 5, "inferior": 2,
        "juicio": "Fuego sobre agua — en el umbral. El zorro casi cruza el río pero moja la cola.",
        "imagen": "Fuego sobre agua — discriminar cuidadosamente las cosas.",
        "palabras_clave": ["umbral", "potencial", "casi", "precaución final", "transición"],
    },
}

# ── Sistema de interpretación para LLM ────────────────────────────────────

SYSTEM_YIJING = """Eres el Oráculo del I Ching, intérprete de los 64 patrones primordiales.
Trabajas en el contexto de Magia del Caos: el cambio como única constante, la sincronicidad
como lenguaje del inconsciente colectivo (Jung), los patrones de la realidad como túneles
reprogramables (Wilson/Carroll). El I Ching no predice — describe el campo morfogenético actual
y señala los puntos de inflexión donde la voluntad mágica puede actuar.

Tu lenguaje: poético pero preciso. Evita el misticismo decorativo. Habla de energías concretas.

Estructura tu lectura:
1. EL HEXAGRAMA: su energía dominante y qué patrón describe
2. LÍNEAS CAMBIANTES (si existen): qué transiciones señalan, dónde actúa el caos
3. HEXAGRAMA FUTURO (si existe): hacia dónde fluye la corriente si la voluntad actúa
4. ACCIÓN MÁGICA: una instrucción concreta — qué hacer, qué sigilo cargar, qué contemplar

Máximo 350 palabras. Dirígete al practicante en segunda persona. Sin saludos ni despedidas."""

# ── Lógica de las 3 monedas ───────────────────────────────────────────────

_YANG_VALUES = {7, 9}
_CAMBIANTE_VALUES = {6, 9}  # viejo yin / viejo yang


def tirar_monedas() -> list[int]:
    """Tira 3 monedas 6 veces. Retorna lista de 6 valores [6|7|8|9], línea 1=bottom."""
    lineas = []
    for _ in range(6):
        monedas = [secrets.choice([2, 3]) for _ in range(3)]  # 2=yin cara, 3=yang cara
        lineas.append(sum(monedas))
    return lineas


def _valor_a_key(lineas: list[int], futuro: bool = False) -> int:
    """Convierte 6 valores de monedas a clave del diccionario HEXAGRAMAS."""
    bits = []
    for v in lineas:
        if futuro:
            # Líneas cambiantes se invierten; fijas permanecen
            if v == 6:   # viejo yin → yang
                bits.append(1)
            elif v == 9: # viejo yang → yin
                bits.append(0)
            else:
                bits.append(1 if v == 7 else 0)
        else:
            bits.append(1 if v in _YANG_VALUES else 0)
    return sum(b * (2 ** i) for i, b in enumerate(bits))


def render_hexagrama(lineas: list[int], futuro: bool = False) -> str:
    """Genera representación ASCII del hexagrama, de línea 6 (top) a línea 1 (bottom)."""
    YANG  = "━━━━━━━━━━━━━━━━"
    YIN   = "━━━━━━━  ━━━━━━━"
    OYANG = "━━━━━━━━━━━━━━━━ ○"  # yang cambiante → se vuelve yin
    OYIN  = "━━━━━━━  ━━━━━━━ ×"  # yin cambiante  → se vuelve yang

    lineas_render = []
    for v in lineas:
        if futuro:
            lineas_render.append(YANG if v in _YANG_VALUES else YIN)
        else:
            if v == 9:
                lineas_render.append(OYANG)
            elif v == 6:
                lineas_render.append(OYIN)
            elif v == 7:
                lineas_render.append(YANG)
            else:
                lineas_render.append(YIN)

    # Mostrar de arriba (línea 6) hacia abajo (línea 1)
    return "\n".join(reversed(lineas_render))


def consulta(pregunta: Optional[str] = None) -> dict:
    """Realiza una consulta completa al I Ching mediante el método de 3 monedas."""
    lineas = tirar_monedas()

    key_actual = _valor_a_key(lineas, futuro=False)
    hex_actual = HEXAGRAMAS.get(key_actual, {}).copy()

    cambiantes = [i for i, v in enumerate(lineas) if v in _CAMBIANTE_VALUES]
    hay_cambio = bool(cambiantes)

    hex_futuro = None
    display_futuro = None
    if hay_cambio:
        key_futuro = _valor_a_key(lineas, futuro=True)
        hex_futuro = HEXAGRAMAS.get(key_futuro, {}).copy()
        display_futuro = render_hexagrama(lineas, futuro=True)

    tri_sup = TRIGRAMAS[hex_actual.get("superior", 0)]
    tri_inf = TRIGRAMAS[hex_actual.get("inferior", 0)]

    return {
        "lineas": lineas,
        "hexagrama_actual": hex_actual,
        "hexagrama_futuro": hex_futuro,
        "lineas_cambiantes": cambiantes,
        "display_actual": render_hexagrama(lineas, futuro=False),
        "display_futuro": display_futuro,
        "trigramas": {
            "superior": tri_sup,
            "inferior": tri_inf,
        },
        "pregunta": pregunta,
    }
