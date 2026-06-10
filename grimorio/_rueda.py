"""La rueda de los ocho colores de la magia del caos."""

RUEDA_COLORES: dict[str, dict] = {
    "octarina": {
        "nombre": "Octarina", "subtitulo": "Magia Pura",
        "posicion": "centro / arriba", "deidad": "kali", "color_hex": "#9b59b6",
        "dominio": (
            "La magia en su estado más puro antes de tomar forma. "
            "No tiene objetivo porque lo contiene todos."
        ),
    },
    "rojo": {
        "nombre": "Rojo", "subtitulo": "Magia de la Guerra",
        "posicion": "noroeste", "deidad": "lilith", "color_hex": "#e74c3c",
        "dominio": "Fuerza, combate, voluntad que no cede. La voluntad que protege.",
    },
    "negro": {
        "nombre": "Negro", "subtitulo": "Magia de la Muerte",
        "posicion": "noreste", "deidad": "kali", "color_hex": "#2c3e50",
        "dominio": "Transformación profunda, tránsito. El umbral entre lo que fue y lo que será.",
    },
    "azul": {
        "nombre": "Azul", "subtitulo": "Magia de la Riqueza",
        "posicion": "este", "deidad": "artemisa", "color_hex": "#2980b9",
        "dominio": "Abundancia, prosperidad, flujo de recursos. La corriente que abre caminos.",
    },
    "verde": {
        "nombre": "Verde", "subtitulo": "Magia del Amor",
        "posicion": "sureste", "deidad": "isis", "color_hex": "#27ae60",
        "dominio": "Amor en todas sus formas. Atracción, sanación de vínculos, apertura del corazón.",
    },
    "amarillo": {
        "nombre": "Amarillo", "subtitulo": "Magia del Ego",
        "posicion": "sur", "deidad": "afrodita", "color_hex": "#f39c12",
        "dominio": "El yo consciente, la identidad, el poder personal.",
    },
    "naranja": {
        "nombre": "Naranja", "subtitulo": "Magia del Pensamiento",
        "posicion": "oeste", "deidad": "afrodita", "color_hex": "#e67e22",
        "dominio": "Intelecto, comunicación, aprendizaje, influencia.",
    },
    "morado": {
        "nombre": "Morado / Plata", "subtitulo": "Magia Sexual",
        "posicion": "suroeste", "deidad": "lilith", "color_hex": "#8e44ad",
        "dominio": "La fuerza vital en su expresión más intensa. Sexualidad, kundalini.",
    },
}

RUEDA_COMO_CONTEXTO = (
    "\n━━━ RUEDA DE LOS OCHO COLORES (Kalinabis) ━━━\n"
    "El sistema reconoce ocho corrientes de fuerza mágica:\n"
    "  Octarina (centro) — Magia Pura · Kali\n"
    "  Rojo    — Magia de la Guerra · Lilith\n"
    "  Negro   — Magia de la Muerte · Kali / Tutu\n"
    "  Azul    — Magia de la Riqueza · Artemisa\n"
    "  Verde   — Magia del Amor · Isis\n"
    "  Amarillo — Magia del Ego · Afrodita\n"
    "  Naranja  — Magia del Pensamiento · Afrodita\n"
    "  Morado/Plata — Magia Sexual · Lilith\n"
    "Puedes identificar qué corriente está activa en la consulta del practicante.\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
)
