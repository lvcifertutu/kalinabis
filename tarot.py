# ═══════════════════════════════════════════════════════════════════════════
#  TAROT — Los 22 Arcanos Mayores
#  Significados derecho e invertido + resonancia con las deidades del sistema
# ═══════════════════════════════════════════════════════════════════════════

ARCANOS = [
    {
        "n": 0, "nombre": "El Loco", "clave": "loco",
        "derecho": "comienzos · inocencia · salto al vacío · libertad sin miedo",
        "invertido": "imprudencia · caos sin dirección · ingenuidad peligrosa",
        "deidad": "tutu",
    },
    {
        "n": 1, "nombre": "El Mago", "clave": "mago",
        "derecho": "voluntad · poder de crear · todos los elementos en tu mano",
        "invertido": "manipulación · talento desperdiciado · engaño",
        "deidad": "tutu",
    },
    {
        "n": 2, "nombre": "La Sacerdotisa", "clave": "sacerdotisa",
        "derecho": "intuición · misterio · conocimiento oculto · el velo",
        "invertido": "secretos retenidos · desconexión interior · silencio que daña",
        "deidad": "afrodita",
    },
    {
        "n": 3, "nombre": "La Emperatriz", "clave": "emperatriz",
        "derecho": "abundancia · fertilidad · madre · creación que florece",
        "invertido": "bloqueo creativo · dependencia · descuido del cuerpo",
        "deidad": "isis",
    },
    {
        "n": 4, "nombre": "El Emperador", "clave": "emperador",
        "derecho": "estructura · autoridad · orden · fundamento sólido",
        "invertido": "rigidez · control excesivo · tiranía",
        "deidad": "artemisa",
    },
    {
        "n": 5, "nombre": "El Sumo Sacerdote", "clave": "sacerdote",
        "derecho": "tradición · enseñanza · puente con lo sagrado",
        "invertido": "dogma · rebeldía necesaria · romper lo heredado",
        "deidad": "tutu",
    },
    {
        "n": 6, "nombre": "Los Enamorados", "clave": "enamorados",
        "derecho": "unión · elección del corazón · armonía · vínculo",
        "invertido": "desequilibrio · elección difícil · tentación",
        "deidad": "afrodita",
    },
    {
        "n": 7, "nombre": "El Carro", "clave": "carro",
        "derecho": "voluntad victoriosa · avance · control de fuerzas opuestas",
        "invertido": "descontrol · agresión · dirección perdida",
        "deidad": "lilith",
    },
    {
        "n": 8, "nombre": "La Justicia", "clave": "justicia",
        "derecho": "equilibrio · verdad · causa y efecto · decisión justa",
        "invertido": "injusticia · deshonestidad · evadir la responsabilidad",
        "deidad": "afrodita",
    },
    {
        "n": 9, "nombre": "El Ermitaño", "clave": "ermitano",
        "derecho": "introspección · búsqueda interior · la luz que se lleva solo",
        "invertido": "aislamiento · soledad no elegida · negar el consejo",
        "deidad": "tutu",
    },
    {
        "n": 10, "nombre": "La Rueda de la Fortuna", "clave": "rueda",
        "derecho": "ciclos · destino · cambio inevitable · el giro del tiempo",
        "invertido": "mala racha · resistirse al cambio · ciclos rotos",
        "deidad": "artemisa",
    },
    {
        "n": 11, "nombre": "La Fuerza", "clave": "fuerza",
        "derecho": "fuerza interior · valor suave · dominar la bestia con amor",
        "invertido": "duda · fuerza bruta · miedo que domina",
        "deidad": "isis",
    },
    {
        "n": 12, "nombre": "El Colgado", "clave": "colgado",
        "derecho": "rendición · ver desde otro ángulo · pausa sagrada · sacrificio",
        "invertido": "estancamiento · resistencia inútil · víctima",
        "deidad": "lilith",
    },
    {
        "n": 13, "nombre": "La Muerte", "clave": "muerte",
        "derecho": "transformación · fin necesario · renacimiento · soltar",
        "invertido": "aferrarse · miedo al cambio · transformación detenida",
        "deidad": "lilith",
    },
    {
        "n": 14, "nombre": "La Templanza", "clave": "templanza",
        "derecho": "equilibrio · mezcla justa · paciencia · sanación",
        "invertido": "exceso · desequilibrio · impaciencia",
        "deidad": "afrodita",
    },
    {
        "n": 15, "nombre": "El Diablo", "clave": "diablo",
        "derecho": "sombra · ataduras · deseo · lo que te encadena (y libera)",
        "invertido": "liberación · romper cadenas · enfrentar la sombra",
        "deidad": "lilith",
    },
    {
        "n": 16, "nombre": "La Torre", "clave": "torre",
        "derecho": "ruptura súbita · revelación · derrumbe de lo falso",
        "invertido": "desastre evitado · cambio resistido · miedo al colapso",
        "deidad": "lilith",
    },
    {
        "n": 17, "nombre": "La Estrella", "clave": "estrella",
        "derecho": "esperanza · inspiración · guía · fe renovada",
        "invertido": "desánimo · fe perdida · desconexión de la guía",
        "deidad": "afrodita",
    },
    {
        "n": 18, "nombre": "La Luna", "clave": "luna",
        "derecho": "intuición · sueños · lo inconsciente · ilusión y misterio",
        "invertido": "confusión que se disipa · miedo enfrentado · claridad que vuelve",
        "deidad": "lilith",
    },
    {
        "n": 19, "nombre": "El Sol", "clave": "sol",
        "derecho": "alegría · éxito · vitalidad · claridad luminosa",
        "invertido": "optimismo nublado · alegría pospuesta · brillo opacado",
        "deidad": "isis",
    },
    {
        "n": 20, "nombre": "El Juicio", "clave": "juicio",
        "derecho": "despertar · llamado · renacimiento · perdón",
        "invertido": "autocrítica · llamado ignorado · duda del propósito",
        "deidad": "isis",
    },
    {
        "n": 21, "nombre": "El Mundo", "clave": "mundo",
        "derecho": "plenitud · ciclo completo · integración · logro total",
        "invertido": "ciclo incompleto · falta cierre · meta cercana sin alcanzar",
        "deidad": "artemisa",
    },
]


POSICIONES = [
    {"nombre": "Pasado",   "sentido": "lo que fue · las raíces de la situación · lo que traes"},
    {"nombre": "Presente", "sentido": "el momento actual · la energía que te rodea ahora"},
    {"nombre": "Futuro",   "sentido": "hacia dónde fluye · el desenlace posible · la dirección"},
]


def carta_por_n(n):
    for a in ARCANOS:
        if a["n"] == n:
            return a
    return None


def tirada_como_contexto(cartas):
    """
    cartas = lista de dicts: [{n, invertida, posicion}, ...]
    Devuelve texto para el system prompt de la deidad que lee.
    Siempre usa el significado derecho — las cartas en Kalinabis no se invierten.
    """
    lineas = []
    for c in cartas:
        arc = carta_por_n(c["n"])
        if not arc:
            continue
        pos = POSICIONES[c["posicion"]]["nombre"]
        lineas.append(f"  {pos}: {arc['nombre']} — {arc['derecho']}")

    return "━━━ LA TIRADA ━━━\n" + "\n".join(lineas) + "\n━━━━━━━━━━━━━━━━━"


if __name__ == "__main__":
    print(f"Arcanos mayores: {len(ARCANOS)}")
    print(f"Posiciones: {[p['nombre'] for p in POSICIONES]}")
    # Tirada de ejemplo
    ejemplo = [
        {"n": 13, "invertida": False, "posicion": 0},
        {"n": 17, "invertida": False, "posicion": 1},
        {"n": 21, "invertida": True,  "posicion": 2},
    ]
    print("\n" + tirada_como_contexto(ejemplo))
