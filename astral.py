# ═══════════════════════════════════════════════════════════════════════════
#  ASTRAL — CARTA NATAL DEL CONSULTANTE
#  Usa kerykeion (Swiss Ephemeris / NASA JPL) — cálculo offline preciso
# ═══════════════════════════════════════════════════════════════════════════

from datetime import datetime

try:
    from kerykeion import AstrologicalSubjectFactory
    KERYKEION_OK = True
except Exception:
    KERYKEION_OK = False


# ── Ciudades precargadas (lat, lng, zona horaria) ──────────────────────────
# Capitales y grandes ciudades, énfasis en Latinoamérica y España.
CIUDADES = {
    "Santiago, Chile":          (-33.45, -70.65, "America/Santiago"),
    "Buenos Aires, Argentina":  (-34.61, -58.38, "America/Argentina/Buenos_Aires"),
    "Lima, Perú":               (-12.05, -77.04, "America/Lima"),
    "Bogotá, Colombia":         (4.71,  -74.07, "America/Bogota"),
    "Ciudad de México, México": (19.43, -99.13, "America/Mexico_City"),
    "Madrid, España":           (40.42,  -3.70, "Europe/Madrid"),
    "Barcelona, España":        (41.39,   2.17, "Europe/Madrid"),
    "Caracas, Venezuela":       (10.48, -66.90, "America/Caracas"),
    "Quito, Ecuador":           (-0.18, -78.47, "America/Guayaquil"),
    "La Paz, Bolivia":          (-16.50, -68.15, "America/La_Paz"),
    "Montevideo, Uruguay":      (-34.90, -56.16, "America/Montevideo"),
    "Asunción, Paraguay":       (-25.26, -57.58, "America/Asuncion"),
    "San José, Costa Rica":     (9.93,  -84.08, "America/Costa_Rica"),
    "Ciudad de Guatemala":      (14.63, -90.51, "America/Guatemala"),
    "La Habana, Cuba":          (23.11, -82.37, "America/Havana"),
    "Santo Domingo, R.D.":      (18.49, -69.93, "America/Santo_Domingo"),
    "San Juan, Puerto Rico":    (18.47, -66.11, "America/Puerto_Rico"),
    "Panamá, Panamá":           (8.98,  -79.52, "America/Panama"),
    "Tegucigalpa, Honduras":    (14.07, -87.19, "America/Tegucigalpa"),
    "Managua, Nicaragua":       (12.11, -86.24, "America/Managua"),
    "San Salvador, El Salvador":(13.69, -89.22, "America/El_Salvador"),
    "Medellín, Colombia":       (6.24,  -75.58, "America/Bogota"),
    "Guadalajara, México":      (20.67, -103.35,"America/Mexico_City"),
    "Monterrey, México":        (25.69, -100.32,"America/Monterrey"),
    "Córdoba, Argentina":       (-31.42, -64.18,"America/Argentina/Cordoba"),
    "Valparaíso, Chile":        (-33.05, -71.62,"America/Santiago"),
    "Concepción, Chile":        (-36.83, -73.05,"America/Santiago"),
    "Sevilla, España":          (37.39,  -5.99, "Europe/Madrid"),
    "Valencia, España":         (39.47,  -0.38, "Europe/Madrid"),
    "Miami, EE.UU.":            (25.76, -80.19, "America/New_York"),
    "Nueva York, EE.UU.":       (40.71, -74.01, "America/New_York"),
    "Los Ángeles, EE.UU.":      (34.05, -118.24,"America/Los_Angeles"),
}

SIGNO_ES = {
    "Ari": "Aries",  "Tau": "Tauro",  "Gem": "Géminis", "Can": "Cáncer",
    "Leo": "Leo",    "Vir": "Virgo",  "Lib": "Libra",   "Sco": "Escorpio",
    "Sag": "Sagitario","Cap":"Capricornio","Aqu":"Acuario","Pis":"Piscis",
}
SIGNO_SIMBOLO = {
    "Ari":"♈","Tau":"♉","Gem":"♊","Can":"♋","Leo":"♌","Vir":"♍",
    "Lib":"♎","Sco":"♏","Sag":"♐","Cap":"♑","Aqu":"♒","Pis":"♓",
}
PLANETA_ES = {
    "sun":"Sol","moon":"Luna","mercury":"Mercurio","venus":"Venus",
    "mars":"Marte","jupiter":"Júpiter","saturn":"Saturno",
    "uranus":"Urano","neptune":"Neptuno","pluto":"Plutón",
}
PLANETA_SIMBOLO = {
    "sun":"☉","moon":"☽","mercury":"☿","venus":"♀","mars":"♂",
    "jupiter":"♃","saturn":"♄","uranus":"♅","neptune":"♆","pluto":"♇",
}
CASA_NUM = {
    "First_House":1,"Second_House":2,"Third_House":3,"Fourth_House":4,
    "Fifth_House":5,"Sixth_House":6,"Seventh_House":7,"Eighth_House":8,
    "Ninth_House":9,"Tenth_House":10,"Eleventh_House":11,"Twelfth_House":12,
}


def calcular_carta_natal(nombre, anio, mes, dia, hora, minuto,
                         lat, lng, tz_str):
    """
    Calcula la carta natal completa.
    Devuelve dict con planetas, ascendente, casas.
    """
    if not KERYKEION_OK:
        return {"error": "kerykeion no está instalado"}

    try:
        s = AstrologicalSubjectFactory.from_birth_data(
            nombre or "Consultante",
            int(anio), int(mes), int(dia), int(hora), int(minuto),
            lng=float(lng), lat=float(lat), tz_str=tz_str, online=False,
        )
    except Exception as e:
        return {"error": f"No se pudo calcular: {e}"}

    planetas = {}
    for key in ["sun","moon","mercury","venus","mars","jupiter",
                "saturn","uranus","neptune","pluto"]:
        obj = getattr(s, key)
        sign = obj["sign"]
        planetas[key] = {
            "nombre":   PLANETA_ES[key],
            "simbolo":  PLANETA_SIMBOLO[key],
            "signo":    SIGNO_ES.get(sign, sign),
            "signo_sim":SIGNO_SIMBOLO.get(sign, ""),
            "grado":    round(obj["position"], 1),
            "casa":     CASA_NUM.get(obj.get("house",""), None),
            "retro":    bool(obj.get("retrograde", False)),
        }

    asc = s.first_house
    mc  = s.tenth_house
    asc_sign = asc["sign"]
    mc_sign  = mc["sign"]

    return {
        "nombre":   nombre or "Consultante",
        "planetas": planetas,
        "ascendente": {
            "signo":     SIGNO_ES.get(asc_sign, asc_sign),
            "signo_sim": SIGNO_SIMBOLO.get(asc_sign, ""),
            "grado":     round(asc["position"], 1),
        },
        "mediocielo": {
            "signo":     SIGNO_ES.get(mc_sign, mc_sign),
            "signo_sim": SIGNO_SIMBOLO.get(mc_sign, ""),
            "grado":     round(mc["position"], 1),
        },
        "sol":  planetas["sun"]["signo"],
        "luna": planetas["moon"]["signo"],
        "asc":  SIGNO_ES.get(asc_sign, asc_sign),
    }


def carta_natal_como_contexto(carta):
    """Texto de la carta natal para el system prompt de las deidades."""
    if not carta or "error" in carta:
        return ""
    p = carta["planetas"]
    lineas = [f"  {v['nombre']}: {v['signo']} {v['grado']}°"
              + (f" casa {v['casa']}" if v['casa'] else "")
              + (" R" if v['retro'] else "")
              for v in p.values()]
    return f"""

━━━ CARTA NATAL DEL CONSULTANTE ━━━
Sol en {carta['sol']} · Luna en {carta['luna']} · Ascendente {carta['asc']}
{chr(10).join(lineas)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


if __name__ == "__main__":
    print("kerykeion disponible:", KERYKEION_OK)
    print(f"Ciudades precargadas: {len(CIUDADES)}")
    carta = calcular_carta_natal("Prueba", 1990, 5, 15, 14, 30,
                                  -33.45, -70.65, "America/Santiago")
    print(f"\nSol: {carta['sol']} · Luna: {carta['luna']} · Asc: {carta['asc']}")
    for k, v in carta["planetas"].items():
        print(f"  {v['simbolo']} {v['nombre']:10} {v['signo']:12} {v['grado']:5}° "
              f"casa {v['casa']} {'R' if v['retro'] else ''}")
