"""
Synchronicidades — Registro y Seguimiento de Coincidencias Significativas
Magia del Caos · Kalinabis
Basado en Carl Jung (Synchronicity), Robert Anton Wilson (Reality Tunnels),
y la práctica caótica de llevar un diario de señales.
"""

from datetime import datetime
from typing import Optional

# ── Estados del ciclo de vida ──────────────────────────────────────────────

ESTADO_ESPERANDO  = "esperando"
ESTADO_CONFIRMADA = "confirmada"
ESTADO_EXPIRADA   = "expirada"

# ── Categorías de signos ────────────────────────────────────────────────────

CATEGORIAS = [
    "animal",
    "número",
    "persona",
    "objeto",
    "sueño",
    "frase",
    "color",
    "lugar",
    "acontecimiento",
    "otro",
]

# ── Textos de sabor por estado ─────────────────────────────────────────────

TEXTOS_ESTADO = {
    ESTADO_ESPERANDO:  "El signo está en camino. Permanece atento sin buscar.",
    ESTADO_CONFIRMADA: "La coincidencia se manifestó. El universo habla en patrones.",
    ESTADO_EXPIRADA:   "El plazo pasó sin confirmación. ¿O la señal fue demasiado sutil?",
}


# ── Funciones de cálculo ───────────────────────────────────────────────────

def calcular_estado_sync(plazo: str, estado_db: str) -> str:
    """Determina el estado real de la sync según el plazo actual."""
    if estado_db in (ESTADO_CONFIRMADA, ESTADO_EXPIRADA):
        return estado_db
    try:
        fecha_plazo = datetime.fromisoformat(plazo)
    except (ValueError, TypeError):
        return ESTADO_ESPERANDO
    if datetime.now() > fecha_plazo:
        return ESTADO_EXPIRADA
    return ESTADO_ESPERANDO


def dias_restantes(plazo: str) -> int:
    """Días que quedan hasta el plazo. Negativo si ya expiró."""
    try:
        fecha_plazo = datetime.fromisoformat(plazo)
        delta = fecha_plazo - datetime.now()
        return delta.days
    except (ValueError, TypeError):
        return 0


def enriquecer_sync(sync: dict) -> dict:
    """Agrega estado_vivo y días restantes al dict de la sync."""
    if not sync:
        return sync
    s = dict(sync)
    s["estado_vivo"]    = calcular_estado_sync(s.get("plazo", ""), s.get("estado", ""))
    s["dias_restantes"] = dias_restantes(s.get("plazo", ""))
    s["texto_estado"]   = TEXTOS_ESTADO.get(s["estado_vivo"], "")
    return s


def colectiva_resumen(syncs: list[dict]) -> dict:
    """
    Agrega estadísticas colectivas de las syncs de todos los proyectos.
    Retorna top signos, tasa de confirmación, y distribución por fase lunar.
    """
    if not syncs:
        return {"total": 0, "confirmadas": 0, "tasa": 0.0,
                "top_signos": [], "por_fase": {}}

    total       = len(syncs)
    confirmadas = sum(1 for s in syncs if s.get("estado") == ESTADO_CONFIRMADA)
    tasa        = round(confirmadas / total, 2) if total else 0.0

    # Contar frecuencia de signos
    conteo_signos: dict[str, int] = {}
    for s in syncs:
        signo = (s.get("signo_esperado") or "").strip().lower()
        if signo:
            conteo_signos[signo] = conteo_signos.get(signo, 0) + 1
    top_signos = sorted(conteo_signos.items(), key=lambda x: -x[1])[:5]

    # Distribución por fase lunar
    por_fase: dict[str, dict] = {}
    for s in syncs:
        fase = s.get("fase_lunar") or "desconocida"
        if fase not in por_fase:
            por_fase[fase] = {"total": 0, "confirmadas": 0}
        por_fase[fase]["total"] += 1
        if s.get("estado") == ESTADO_CONFIRMADA:
            por_fase[fase]["confirmadas"] += 1

    return {
        "total":       total,
        "confirmadas": confirmadas,
        "tasa":        tasa,
        "top_signos":  [{"signo": s, "count": c} for s, c in top_signos],
        "por_fase":    por_fase,
    }


def render_sync(sync: dict) -> str:
    """Render ASCII de una synchronicidad para el terminal."""
    signo    = (sync.get("signo_esperado") or "?")[:50]
    estado   = sync.get("estado_vivo", sync.get("estado", "?"))
    dias     = sync.get("dias_restantes", 0)
    cat      = sync.get("categoria") or "otro"
    sid      = sync.get("id", "?")

    ICONOS = {
        ESTADO_ESPERANDO:  "◈",
        ESTADO_CONFIRMADA: "✓",
        ESTADO_EXPIRADA:   "✕",
    }
    icono = ICONOS.get(estado, "?")

    dias_txt = (
        f"+{dias}d restantes" if dias > 0
        else ("hoy expira" if dias == 0 else f"{abs(dias)}d expirado")
    )

    return (
        f"╔══ SYNC #{sid} ══╗\n"
        f"  {icono} Estado: {estado.upper()}\n"
        f"  ◎ Signo:  {signo}\n"
        f"  ∷ Cat:    {cat}\n"
        f"  ⌚ Plazo:  {dias_txt}\n"
        f"╚{'═' * (len(str(sid)) + 10)}╝"
    )
