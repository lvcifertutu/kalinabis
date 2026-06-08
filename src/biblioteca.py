"""Lógica de negocio de la Biblioteca Comunitaria de Kalinabis.

Funciones de alto nivel usadas por los endpoints de servidor.py.
El seeding de las entradas canónicas también vive aquí.
"""

from pathlib import Path
from hashlib import sha256
from typing import Optional

from base_datos.biblioteca import (
    EntradaRepo, FuenteRepo, ContribucionRepo, ResonanciaRepo,
    TIPOS_RESONANCIA, TIPOS_FUENTE, TIPOS_CONTRIBUCION,
)

# ── Utilidades ──────────────────────────────────────────────────────────────

def _hash(texto: str) -> str:
    return sha256(texto.encode()).hexdigest()


def _slugify(titulo: str) -> str:
    import re
    slug = titulo.lower().strip()
    slug = re.sub(r"[áàä]", "a", slug)
    slug = re.sub(r"[éèë]", "e", slug)
    slug = re.sub(r"[íìï]", "i", slug)
    slug = re.sub(r"[óòö]", "o", slug)
    slug = re.sub(r"[úùü]", "u", slug)
    slug = re.sub(r"[ñ]", "n", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]


# ── Seeding canónico ────────────────────────────────────────────────────────

_CANON = [
    {
        "titulo": "Taoísmo Profundo",
        "slug": "taoismo-profundo",
        "dominio": "taoismo",
        "archivo": "biblioteca/taoismo/TAOISMO_PROFUNDO.md",
    },
    {
        "titulo": "Mapa del Cuerpo Energético",
        "slug": "mapa-cuerpo-energetico",
        "dominio": "cuerpo_energetico",
        "archivo": "biblioteca/cuerpo_energetico/MAPA_CUERPO.md",
    },
]


def _sembrar_grimorio() -> int:
    """Siembra entradas canónicas a partir de las estructuras de grimorio_base.py.

    Solo las que pertenecen al dominio de Artemisa como guardiana planetaria:
    chakras sociales, sephiroth, qliphoth y el mapa cuerpo/alma/espíritu del planeta.
    """
    try:
        from grimorio_base import (
            CHAKRAS, CHAKRAS_ARTEMISA_SOCIAL,
            ARBOL_VIDA_SEPHIROTH, ARBOL_MUERTE_QLIPHOTH,
        )
    except ImportError:
        return 0

    sembradas = 0

    # ── Chakras como energías planetarias (Artemisa) ─────────────────────
    lineas_chakras = ["# CHAKRAS — Mapa de Energía Planetaria\n"]
    lineas_chakras.append(
        "Los siete chakras del cuerpo individual "
        "son también los siete centros de conciencia colectiva del planeta, "
        "según la cosmología de Kalinabis.\n"
    )
    lineas_chakras.append("\n## Los siete centros\n")
    for n, c in CHAKRAS.items():
        social = CHAKRAS_ARTEMISA_SOCIAL.get(n, "")
        lineas_chakras.append(
            f"**{n}. {c['nombre']}** — {c['ubicacion']}\n"
            f"- Individual: {c['dominio']}\n"
            f"- Planetario: {social}\n"
        )
    lineas_chakras.append(
        "\n## Cuerpo / Alma / Espíritu del planeta\n\n"
        "- **Cuerpo** (chakras 1-3): Geografía, ecorregiones, elementales activos — "
        "el sustrato físico de la conciencia colectiva.\n"
        "- **Alma** (chakras 4-5): Intenciones activas, sincronicidades, "
        "servitors en el bosque — el campo emocional-relacional de la especie.\n"
        "- **Espíritu** (chakras 6-7): Conocimiento verificado en la biblioteca, "
        "entradas canónicas, resonancias de sabiduría — el campo cognitivo-espiritual.\n"
    )
    EntradaRepo.crear_canon(
        titulo="Chakras Planetarios — Artemisa y la Energía del Mundo",
        slug="artemisa-chakras-planetarios",
        dominio="artemisa_energia_planetaria",
        contenido="\n".join(lineas_chakras),
    )
    sembradas += 1

    # ── Árbol de Vida (Sephiroth) ─────────────────────────────────────────
    lineas_arbol = ["# ÁRBOL DE LA VIDA — Sephiroth\n\n"]
    lineas_arbol.append(
        "Los diez Sephiroth del Árbol de la Vida mapean tanto el cuerpo humano "
        "(Adam Kadmon) como las fuerzas que estructuran el planeta. "
        "Bajo la custodia de Artemisa.\n\n"
    )
    for n, s in ARBOL_VIDA_SEPHIROTH.items():
        lineas_arbol.append(f"**{n}. {s['nombre']}** — {s['significado']}\n")
    EntradaRepo.crear_canon(
        titulo="Árbol de la Vida — Sephiroth",
        slug="arbol-vida-sephiroth",
        dominio="artemisa_energia_planetaria",
        contenido="\n".join(lineas_arbol),
    )
    sembradas += 1

    # ── Árbol de Muerte (Qliphoth) ────────────────────────────────────────
    lineas_q = ["# ÁRBOL DE LA MUERTE — Qliphoth\n\n"]
    lineas_q.append(
        "Los Qliphoth son las sombras de los Sephiroth — "
        "las fuerzas reprimidas que esperan ser integradas. "
        "No son el mal: son la prima materia del trabajo de sombra, "
        "tanto en el individuo como en el colectivo.\n\n"
    )
    for n, q in ARBOL_MUERTE_QLIPHOTH.items():
        lineas_q.append(
            f"**{n}. {q['nombre']}** (sombra de {q['sombra_de']}) — {q['significado']}\n"
        )
    EntradaRepo.crear_canon(
        titulo="Árbol de la Muerte — Qliphoth",
        slug="arbol-muerte-qliphoth",
        dominio="artemisa_energia_planetaria",
        contenido="\n".join(lineas_q),
    )
    sembradas += 1

    return sembradas


def sembrar_canon() -> int:
    """Inserta o actualiza las entradas canónicas desde los archivos markdown.

    Idempotente: no duplica si el slug ya existe.
    Retorna cuántas entradas fueron procesadas.
    """
    base = Path(__file__).parent.parent
    sembradas = 0
    for item in _CANON:
        ruta = base / item["archivo"]
        if not ruta.exists():
            continue
        contenido = ruta.read_text(encoding="utf-8")
        EntradaRepo.crear_canon(
            titulo=item["titulo"],
            slug=item["slug"],
            dominio=item["dominio"],
            contenido=contenido,
        )
        sembradas += 1
    sembradas += _sembrar_grimorio()
    return sembradas


# ── API de consultas ────────────────────────────────────────────────────────

def obtener_entrada_completa(slug: str) -> Optional[dict]:
    """Retorna una entrada con sus fuentes, resonancias y contribuciones."""
    entrada = EntradaRepo.por_slug(slug)
    if not entrada:
        return None
    entrada["fuentes"] = FuenteRepo.listar(entrada["id"])
    entrada["resonancias"] = ResonanciaRepo.conteo(entrada["id"])
    entrada["contribuciones_pendientes"] = len(
        ContribucionRepo.listar_pendientes(entrada["id"])
    )
    return entrada


# ── Validaciones ────────────────────────────────────────────────────────────

def validar_nueva_entrada(data: dict) -> Optional[str]:
    titulo = data.get("titulo", "")
    if not isinstance(titulo, str) or not titulo.strip():
        return "Se requiere 'titulo'"
    if len(titulo) > 200:
        return "'titulo' demasiado largo (max 200)"

    dominio = data.get("dominio", "")
    if not isinstance(dominio, str) or not dominio.strip():
        return "Se requiere 'dominio'"
    if len(dominio) > 60:
        return "'dominio' demasiado largo"

    contenido = data.get("contenido", "")
    if not isinstance(contenido, str) or not contenido.strip():
        return "Se requiere 'contenido'"
    if len(contenido) > 100_000:
        return "'contenido' demasiado largo (max 100.000 chars)"

    return None


def validar_fuente(data: dict) -> Optional[str]:
    tipo = data.get("tipo", "")
    if tipo not in TIPOS_FUENTE:
        return f"'tipo' debe ser uno de: {', '.join(sorted(TIPOS_FUENTE))}"
    referencia = data.get("referencia", "")
    if not isinstance(referencia, str) or not referencia.strip():
        return "Se requiere 'referencia'"
    if len(referencia) > 1000:
        return "'referencia' demasiado larga (max 1000)"
    return None


def validar_resonancia(data: dict) -> Optional[str]:
    tipo = data.get("tipo", "")
    if tipo not in TIPOS_RESONANCIA:
        return f"'tipo' debe ser uno de: {', '.join(sorted(TIPOS_RESONANCIA))}"
    return None


def validar_contribucion(data: dict) -> Optional[str]:
    tipo = data.get("tipo", "")
    if tipo not in TIPOS_CONTRIBUCION:
        return f"'tipo' debe ser uno de: {', '.join(sorted(TIPOS_CONTRIBUCION))}"
    contenido = data.get("contenido", "")
    if not isinstance(contenido, str) or not contenido.strip():
        return "Se requiere 'contenido'"
    if len(contenido) > 20_000:
        return "'contenido' demasiado largo (max 20.000)"
    return None
