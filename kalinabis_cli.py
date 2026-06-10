#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KALINABIS CLI — sistema ritual en terminal pura.

Ejecutar:  python kalinabis_cli.py
"""

import sys
import os

# Forzar UTF-8 en Windows para que los caracteres especiales no se rompan
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
import json
import time
from pathlib import Path
from datetime import datetime

# ── Entorno ──────────────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env.local")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.prompt import Prompt, Confirm
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

# ── Sistema Kalinabis ────────────────────────────────────────────────────────
from base_datos.schema import inicializar_db
from base_datos.esferas import EsferaRepo, RelacionRepo, EventoRepo, HumusRepo, ConvergenciaRepo
from base_datos.proyecto import ProyectoRepo, ConversacionRepo
from base_datos.biblioteca import EntradaRepo
from base_datos.manifestacion import ManifestacionRepo, CheckinRepo
from base_datos.sigilo_proyecto import SigiloOperativoRepo, letras_carroll, glifo_ascii
from proyectos import GeneradorCodigos, Cifrador, Proyecto
from esferas import GestorEsferas
from invocacion.invocador import Invocador
from src.biblioteca import sembrar_canon
from grimorio_bosque import ELEMENTO_DEIDAD, SERES_POR_ELEMENTO, ARBOLES_POR_DEIDAD
from luna import luna_como_contexto

console = Console()

# ── Paleta ───────────────────────────────────────────────────────────────────
COLORES = {
    "isis":     "bright_yellow",
    "afrodita": "magenta",
    "lilith":   "cyan",
    "artemisa": "green",
    "tutu":     "white",
    "bosque":   "dark_green",
    "titulo":   "bold bright_white",
    "dim":      "dim white",
    "warn":     "yellow",
    "error":    "bold red",
    "ok":       "bold green",
}

ICONOS = {
    "isis":     "🔥",
    "afrodita": "🌬",
    "lilith":   "💧",
    "artemisa": "🌿",
    "tutu":     "🌀",
    "bosque":   "🌲",
    "esfera":   "◉",
    "humus":    "💀",
    "ser":      "✦",
    "arbol":    "🌳",
    "biblioteca": "📚",
}

ELEMENTOS = {
    "isis": "FUEGO · Norte",
    "afrodita": "AIRE · Este",
    "lilith": "AGUA · Sur",
    "artemisa": "TIERRA · Oeste",
}

# ── Estado global ─────────────────────────────────────────────────────────────
_invocador = Invocador()
_proyecto_activo: Proyecto | None = None
_deidad_activa: str | None = None


# ═══════════════════════════════════════════════════════════════════════════
#  UTILIDADES VISUALES
# ═══════════════════════════════════════════════════════════════════════════

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def cabecera():
    console.print()
    t = Text()
    t.append("  K A L I N A B I S  ", style="bold black on bright_white")
    t.append("  CHAOS DAEMON TERMINAL  ", style="bold bright_white on black")
    console.print(t)
    luna = luna_como_contexto()
    luna_linea = luna.strip().split("\n")[1] if luna.strip() else ""
    if luna_linea:
        console.print(f"  [dim]{luna_linea.strip()}[/dim]")
    console.print()


def separador(titulo: str = "", color: str = "dim white"):
    if titulo:
        console.print(Rule(f"[{color}] {titulo} [/{color}]", style=color))
    else:
        console.print(Rule(style=color))


def esperar(msg: str = ""):
    console.print()
    Prompt.ask(f"[dim]{msg or 'presiona enter para continuar'}[/dim]", default="")


def pensar(msg: str = "invocando..."):
    """Muestra spinner mientras el modelo piensa."""
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn(f"[cyan]{msg}[/cyan]"),
        transient=True,
        console=console,
    )


# ═══════════════════════════════════════════════════════════════════════════
#  PROYECTO
# ═══════════════════════════════════════════════════════════════════════════

def _seleccionar_o_crear_proyecto() -> Proyecto | None:
    global _proyecto_activo

    separador("PROYECTO", "dim white")
    console.print("[dim]Un proyecto es tu identidad anónima en el sistema.[/dim]")
    console.print()

    opcion = Prompt.ask(
        "  [white]¿Tienes código de proyecto?[/white]",
        choices=["s", "n"],
        default="n",
    )

    if opcion == "s":
        codigo = Prompt.ask("  [white]Código[/white]").strip().lower()
        p = Proyecto(codigo=codigo)
        if not ProyectoRepo.existe(p.hash):
            console.print("[yellow]  Código no encontrado. Se creará uno nuevo.[/yellow]")
            return _crear_proyecto()
        ProyectoRepo.actualizar_actividad(p.hash)
        _proyecto_activo = p
        console.print(f"[green]  ✓ Proyecto cargado[/green]")
        return _proyecto_activo
    else:
        return _crear_proyecto()


def _crear_proyecto() -> Proyecto:
    global _proyecto_activo
    codigo = GeneradorCodigos.generar()
    _proyecto_activo = Proyecto(codigo=codigo)
    metadatos = json.dumps({"nombre": "cli", "creado_con": "kalinabis_cli"})
    cifrado = Cifrador.cifrar(metadatos, codigo)
    ProyectoRepo.crear(_proyecto_activo.hash, cifrado)
    console.print()
    console.print(Panel(
        f"[bold white]Tu código es:[/bold white]\n\n"
        f"[bold bright_yellow]  {codigo}  [/bold bright_yellow]\n\n"
        f"[dim]Guárdalo. Es tu única llave.[/dim]",
        border_style="yellow",
        padding=(1, 4),
    ))
    return _proyecto_activo


# ═══════════════════════════════════════════════════════════════════════════
#  BOSQUE
# ═══════════════════════════════════════════════════════════════════════════

def _estado_bosque_tabla():
    """Muestra el ecosistema completo en terminal."""
    esferas = EsferaRepo.listar_activas()
    humus = HumusRepo.listar(limite=5)
    eventos = EventoRepo.listar(limite=8)
    relaciones = RelacionRepo.listar_activas() if hasattr(RelacionRepo, "listar_activas") else []

    # Tabla de esferas
    tabla = Table(
        title="ESFERAS VIVAS",
        box=box.MINIMAL_DOUBLE_HEAD,
        border_style="green",
        title_style="bold green",
        show_lines=False,
    )
    tabla.add_column("TIPO", style="green", width=16)
    tabla.add_column("CLAVE", style="dim white", width=22)
    tabla.add_column("AMP", justify="right", style="bright_white", width=6)
    tabla.add_column("FASE", width=12)
    tabla.add_column("MINERAL", style="dim", width=12)

    def _fase_color(fase: str) -> str:
        return {
            "activa": "green",
            "letargo": "yellow",
            "disolviendo": "red",
        }.get(fase, "white")

    if not esferas:
        tabla.add_row("[dim]sin esferas[/dim]", "", "", "", "")
    else:
        for e in esferas[:12]:
            fase = e.get("fase_viva") or e.get("fase_decaimiento", "activa")
            amp = e.get("amplitud_actual", e.get("amplitud", 0))
            mineral = (e.get("metadata") or {}).get("mineral", "—")
            tabla.add_row(
                e["tipo"],
                e["clave_unica"][:22],
                f"{amp:.2f}",
                f"[{_fase_color(fase)}]{fase}[/{_fase_color(fase)}]",
                mineral,
            )

    console.print(tabla)

    # Humus
    if humus:
        console.print()
        console.print("[dim]── HUMUS RECIENTE ──[/dim]")
        for h in humus[:4]:
            causa = h.get("causa", "?")
            console.print(
                f"  [dim]💀 {h['tipo']}:{h['clave_unica'][:20]}  "
                f"causa={causa}  "
                f"{h.get('dias_activa', 0):.0f}d[/dim]"
            )

    # Convergencias
    try:
        convergencias = ConvergenciaRepo.listar_activas() if hasattr(ConvergenciaRepo, "listar_activas") else []
        if convergencias:
            console.print()
            console.print(f"[yellow]⚡ {len(convergencias)} convergencia(s) activa(s)[/yellow]")
            for c in convergencias[:3]:
                console.print(
                    f"  [yellow]{c['n_proyectos']} proyectos: "
                    f"{c['tipo_a']}:{c['clave_a']} + {c['tipo_b']}:{c['clave_b']}[/yellow]"
                )
    except Exception:
        pass

    # Seres activos (de grimorio_bosque)
    console.print()
    console.print("[dim]── SERES DETECTADOS ──[/dim]")
    _mostrar_seres_detectados(esferas)


def _mostrar_seres_detectados(esferas: list):
    """Detecta qué seres del grimorio están presentes según condiciones reales."""
    if not esferas:
        console.print("  [dim]El bosque está vacío.[/dim]")
        return

    amps = [e.get("amplitud_actual", e.get("amplitud", 0)) for e in esferas]
    amp_max = max(amps) if amps else 0
    amp_prom = sum(amps) / len(amps) if amps else 0

    presentes = []

    # Kodama: esferas viejas con alta amplitud
    viejas = [e for e in esferas if _dias_desde(e.get("created_at", "")) > 30]
    if viejas:
        presentes.append(("Kodama", "tierra", f"habita {len(viejas)} esfera(s) antigua(s)"))

    # Tomte: esferas en letargo
    en_letargo = [e for e in esferas if (e.get("fase_viva") or "") == "letargo"]
    if en_letargo:
        presentes.append(("Tomte / Nisse", "tierra", f"custodia {len(en_letargo)} esfera(s) dormida(s)"))

    # Ljósálfar: amplitud alta
    altas = [e for e in esferas if e.get("amplitud_actual", 0) >= 2.5]
    if altas:
        presentes.append(("Ljósálfar", "fuego", f"habita {len(altas)} esfera(s) brillante(s)"))

    # Hongo: siempre si hay movimiento
    if len(esferas) >= 2:
        presentes.append(("Red Micelial", "universal", f"conecta {len(esferas)} esferas"))

    # Yaksha: si hay esferas recientes
    recientes = [e for e in esferas if _dias_desde(e.get("created_at", "")) < 3]
    if recientes:
        presentes.append(("Yaksha", "tierra", f"amplifica {len(recientes)} esfera(s) nueva(s)"))

    # Sila Jinn: si hay micorrizas (simplificado)
    if len(esferas) >= 3:
        presentes.append(("Sila (Jinn del aire)", "aire", "se mueve libremente entre esferas"))

    if not presentes:
        console.print("  [dim]ningún ser detectado[/dim]")
    else:
        for nombre, elemento, desc in presentes:
            color = COLORES.get(ELEMENTOS.get(elemento, "tierra").split(" ")[0].lower(), "dim")
            icono = {"fuego": "🔥", "agua": "💧", "tierra": "🌿", "aire": "🌬", "universal": "✦"}.get(elemento, "◉")
            console.print(f"  {icono} [dim]{nombre}[/dim]  [dim italic]{desc}[/dim]")


def _dias_desde(iso: str) -> float:
    if not iso:
        return 0.0
    try:
        d = datetime.fromisoformat(iso)
        return (datetime.now() - d).total_seconds() / 86400
    except Exception:
        return 0.0


def _voz_del_bosque():
    """Invoca la voz del bosque y la muestra."""
    esferas_raw = EsferaRepo.listar_activas()
    humus_raw = HumusRepo.listar(limite=20)
    eventos_raw = EventoRepo.listar(limite=20)

    # Construir dicts que espera el invocador
    esferas = [dict(e) for e in esferas_raw] if esferas_raw else []
    humus = [dict(h) for h in humus_raw] if humus_raw else []
    eventos = [dict(ev) for ev in eventos_raw] if eventos_raw else []
    relaciones: list = []
    try:
        relaciones = [dict(r) for r in RelacionRepo.listar_activas()]
    except Exception:
        pass
    convergencias: list = []
    try:
        convergencias = [dict(c) for c in ConvergenciaRepo.listar_activas()]
    except Exception:
        pass

    with pensar("el bosque habla..."):
        time.sleep(0.3)
        respuesta = _invocador.voz_bosque(
            esferas=esferas,
            eventos=eventos,
            humus=humus,
            relaciones=relaciones,
            convergencias=convergencias,
        )

    console.print()
    console.print(Panel(
        f"[green]{respuesta.texto}[/green]",
        title="[bold green]VOZ DEL BOSQUE[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))
    if respuesta.es_offline:
        console.print("[dim]  (modo offline)[/dim]")


_DEIDADES_ORDEN = ["isis", "afrodita", "lilith", "artemisa"]
_PULSOS_DEIDAD = {
    "isis":     "luz · purificación",
    "afrodita": "reproducción · vínculo",
    "lilith":   "humedad · sombra",
    "artemisa": "fertilidad · raíces",
}


def _asegurar_esferas_deidad():
    """Crea o refuerza las esferas permanentes de cada deidad en el bosque."""
    for nombre in _DEIDADES_ORDEN:
        EsferaRepo.crear_o_actualizar(
            tipo="deidad",
            clave_unica=nombre,
            metadata={"elemento": ELEMENTO_DEIDAD.get(nombre, ""), "pulso": _PULSOS_DEIDAD.get(nombre, "")},
        )


def _panel_esferas_deidad() -> None:
    """Muestra las cuatro esferas de deidad como parte viva del bosque."""
    esferas = {
        e["clave_unica"]: e
        for e in EsferaRepo.listar_activas(tipo="deidad")
    }

    console.print()
    separador("ESFERAS DE LAS DEIDADES", "dim green")
    console.print()

    for i, nombre in enumerate(_DEIDADES_ORDEN, 1):
        esf = esferas.get(nombre, {})
        color = COLORES[nombre]
        icono = ICONOS[nombre]
        elem = ELEMENTO_DEIDAD.get(nombre, "")
        amp = esf.get("amplitud", 0.0)
        pulso = _PULSOS_DEIDAD.get(nombre, "")

        # Barra de amplitud visual
        barra_llena = int(amp / 5.0 * 12)
        barra = "█" * barra_llena + "░" * (12 - barra_llena)

        console.print(
            f"  [{color}]{i}[/{color}]  {icono}  [{color}]{nombre.upper():10}[/{color}]"
            f"  [{color}]{barra}[/{color}]  [dim]{amp:.2f}[/dim]"
            f"  [dim]{elem}  ·  {pulso}[/dim]"
        )

    console.print()


def _conversacion_esfera_deidad(nombre: str):
    """Conversación directa con una deidad desde su esfera en el bosque."""
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    color = COLORES[nombre]
    icono = ICONOS[nombre]
    elem = ELEMENTOS.get(nombre, "")
    pulso = _PULSOS_DEIDAD.get(nombre, "")

    # Reforzar la esfera al entrar
    EsferaRepo.crear_o_actualizar(
        tipo="deidad",
        clave_unica=nombre,
        metadata={"elemento": ELEMENTO_DEIDAD.get(nombre, ""), "pulso": pulso},
    )

    limpiar()
    cabecera()
    separador(f"{icono}  ESFERA DE {nombre.upper()}", color)
    console.print()
    console.print(f"  [{color}]{elem}[/{color}]  [dim]{pulso}[/dim]")
    console.print()

    # Memoria de conversaciones previas en esta esfera
    memoria = ConversacionRepo.cargar(_proyecto_activo.hash, nombre)
    if memoria:
        console.print(f"  [dim]── {len(memoria)} mensajes en la esfera ──[/dim]")
        for m in memoria[-4:]:
            rol = nombre if m["role"] == "assistant" else "tú"
            estilo = f"dim {color}" if m["role"] == "assistant" else "dim white"
            console.print(f"  [{estilo}]{rol}:[/{estilo}] [dim]{m['content'][:90]}[/dim]")
        console.print()

    esferas_bosque = []
    try:
        raw = EsferaRepo.listar_activas()
        esferas_bosque = [dict(e) for e in raw]
    except Exception:
        pass

    separador("", color)
    console.print()
    console.print(f"  [dim]Estás en la esfera de {nombre}. Habla directamente. 'salir' para volver.[/dim]")
    console.print()

    while True:
        try:
            mensaje = Prompt.ask(f"  [white]tú[/white]")
        except (KeyboardInterrupt, EOFError):
            break

        if mensaje.strip().lower() in ("salir", "exit", "q", "0"):
            break

        if not mensaje.strip():
            continue

        with pensar(f"{nombre} responde desde su esfera..."):
            time.sleep(0.2)
            try:
                respuesta = _invocador.invocar_deidad(
                    nombre=nombre,
                    mensaje=mensaje,
                    proyecto=_proyecto_activo,
                    esferas_bosque=esferas_bosque,
                )
                respuesta_texto = respuesta.texto
                es_offline = respuesta.es_offline
            except Exception as e:
                respuesta_texto = f"[error: {e}]"
                es_offline = False

        console.print()
        console.print(Panel(
            f"[{color}]{respuesta_texto}[/{color}]",
            title=f"[{color}]{icono} {nombre}[/{color}]",
            border_style=color,
            padding=(0, 2),
        ))
        if es_offline:
            console.print("  [dim](offline)[/dim]")
        console.print()

        # Cada mensaje refuerza ligeramente la esfera
        EsferaRepo.crear_o_actualizar(
            tipo="deidad",
            clave_unica=nombre,
            metadata={"elemento": ELEMENTO_DEIDAD.get(nombre, ""), "pulso": pulso},
        )


def menu_bosque():
    _asegurar_esferas_deidad()

    while True:
        limpiar()
        cabecera()
        separador(f"{ICONOS['bosque']} EL BOSQUE", "green")
        console.print()
        _estado_bosque_tabla()
        _panel_esferas_deidad()
        separador()
        console.print()
        console.print("  [green]1[/green]  Esfera de ISIS")
        console.print("  [green]2[/green]  Esfera de AFRODITA")
        console.print("  [green]3[/green]  Esfera de LILITH")
        console.print("  [green]4[/green]  Esfera de ARTEMISA")
        console.print()
        console.print("  [dim]5  Voz del bosque[/dim]")
        console.print("  [dim]6  Ver seres por elemento[/dim]")
        console.print("  [dim]7  Ver árboles del bosque[/dim]")
        console.print("  [dim]8  Plantar esfera[/dim]")
        console.print("  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask("  [green]>[/green]", default="0")

        mapa_deidad = {"1": "isis", "2": "afrodita", "3": "lilith", "4": "artemisa"}
        if op in mapa_deidad:
            _conversacion_esfera_deidad(mapa_deidad[op])
        elif op == "5":
            console.print()
            _voz_del_bosque()
            esperar()
        elif op == "6":
            _menu_seres()
        elif op == "7":
            _menu_arboles()
        elif op == "8":
            _plantar_esfera()
        elif op == "0":
            break


def _menu_seres():
    limpiar()
    cabecera()
    separador("SERES DEL BOSQUE — por elemento", "dim")
    console.print()

    for elemento, seres in SERES_POR_ELEMENTO.items():
        deidad = {v: k for k, v in ELEMENTO_DEIDAD.items()}.get(elemento, "")
        color = COLORES.get(deidad, "white")
        icono = {"fuego": "🔥", "agua": "💧", "tierra": "🌿", "aire": "🌬", "universal": "✦"}.get(elemento, "◉")
        console.print(f"\n{icono} [{color}]{elemento.upper()}[/{color}]" +
                      (f"  [dim]— {deidad.upper()}[/dim]" if deidad else ""))
        for s in seres:
            rareza_color = {"comun": "dim", "infrecuente": "white", "raro": "yellow", "singular": "bold bright_yellow"}.get(s["rareza"], "white")
            console.print(
                f"  [{rareza_color}]{s['nombre']}[/{rareza_color}]"
                f"  [dim]{s['tradicion']}[/dim]"
                f"  [dim italic]{s['rareza']}[/dim italic]"
            )
            console.print(f"    [dim]{s['efecto']}[/dim]")

    esperar()


def _menu_arboles():
    limpiar()
    cabecera()
    separador("ÁRBOLES Y DEIDADES", "dim")
    console.print()

    for deidad, arboles in ARBOLES_POR_DEIDAD.items():
        color = COLORES.get(deidad, "white")
        icono = ICONOS.get(deidad, "")
        elem = ELEMENTO_DEIDAD.get(deidad, "")
        console.print(f"\n{icono} [{color}]{deidad.upper()}[/{color}]  [dim]{elem}[/dim]")
        for a in arboles:
            local = "★ " if a.get("nota_local") else "  "
            console.print(
                f"  {local}[white]{a['nombre_comun']}[/white]"
                f"  [dim italic]{a['nombre_cientifico']}[/dim italic]"
            )
            console.print(
                f"      [dim]↳ {a['deidad_local']}  →  resonancia: {', '.join(a['resonancia_global'])}[/dim]"
            )

    console.print()
    console.print("[dim]★ = nativo o significativo en Santiago[/dim]")
    esperar()


def _plantar_esfera():
    if not _proyecto_activo:
        console.print("[yellow]  Necesitas un proyecto activo para plantar.[/yellow]")
        esperar()
        return

    console.print()
    separador("PLANTAR ESFERA", "green")
    console.print()
    console.print("[dim]Una esfera es una intención que se planta en el bosque colectivo.[/dim]")
    console.print()

    tipo = Prompt.ask("  [green]Tipo de esfera[/green]  [dim](ej: intencion, sombra, relacion)[/dim]")
    clave = Prompt.ask("  [green]Clave única[/green]  [dim](describe tu intención en pocas palabras)[/dim]")

    minerales = ["cuarzo", "obsidiana", "malaquita", "granito", "pirita", "selenita", "hematita", "labradorita"]
    console.print()
    console.print("  [dim]Substrato mineral:[/dim]")
    for i, m in enumerate(minerales, 1):
        console.print(f"  [dim]{i}[/dim] {m}")

    mineral_op = Prompt.ask("  [green]Mineral[/green]  [dim](número o nombre)[/dim]", default="1")
    if mineral_op.isdigit() and 1 <= int(mineral_op) <= len(minerales):
        mineral = minerales[int(mineral_op) - 1]
    else:
        mineral = mineral_op.lower().strip() or "cuarzo"

    gestor = GestorEsferas()
    try:
        resultado = gestor.registrar_marca(
            tipo=tipo.strip(),
            clave_unica=clave.strip(),
            proyecto_hash=_proyecto_activo.hash,
            metadata={"mineral": mineral},
        )
        console.print()
        console.print(f"[green]  ✓ Esfera plantada[/green]  "
                      f"[white]{tipo}:{clave}[/white]  "
                      f"[dim]sobre {mineral}[/dim]")
        if resultado.get("convergencia"):
            console.print(f"  [yellow]⚡ ¡Convergencia detectada![/yellow]")
    except Exception as e:
        console.print(f"[red]  Error: {e}[/red]")

    esperar()


# ═══════════════════════════════════════════════════════════════════════════
#  ALTAR — conversación con deidades
# ═══════════════════════════════════════════════════════════════════════════

def _cabecera_altar():
    """Muestra las cuatro deidades manifestadas como presencias, no como opciones."""
    deidades = [
        ("isis",     "🔥", "FUEGO"),
        ("afrodita", "🌬", "AIRE"),
        ("lilith",   "💧", "AGUA"),
        ("artemisa", "🌿", "TIERRA"),
    ]
    partes = []
    for nombre, icono, elem in deidades:
        color = COLORES[nombre]
        t = Text()
        t.append(f" {icono} ", style=color)
        t.append(nombre.upper(), style=f"bold {color}")
        t.append(f" {elem} ", style=f"dim {color}")
        partes.append(t)

    # Separador central con TUTU
    console.print()
    fila = Text("  ")
    for p in partes:
        fila.append_text(p)
        fila.append("  ·  ", style="dim white")
    console.print(fila)
    console.print()
    console.print("  [dim]Las deidades están presentes. Sólo TUTU puede hablar por ellas.[/dim]")
    console.print()


def _altar_canal_tutu():
    """Conversación con TUTU como único canal del altar.

    Flujo interno:
      1. TUTU escucha al practicante.
      2. TUTU decide qué deidad es relevante.
      3. TUTU invoca a esa deidad internamente (sin mostrarlo).
      4. TUTU canaliza la respuesta de la deidad en su propia voz.
    """
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    esferas_bosque = []
    try:
        raw = EsferaRepo.listar_activas()
        esferas_bosque = [dict(e) for e in raw]
    except Exception:
        pass

    console.print("  [dim]Escribe tu mensaje. 'sigilo' para pedir una intención. 'quién' para saber qué deidad está presente. 'salir' para volver.[/dim]")
    console.print()

    _deidad_activa_canal: str | None = None

    while True:
        try:
            mensaje = Prompt.ask("  [white]tú[/white]")
        except (KeyboardInterrupt, EOFError):
            break

        if mensaje.strip().lower() in ("salir", "exit", "q", "0"):
            break

        if not mensaje.strip():
            continue

        # Comando: sigilo
        if mensaje.strip().lower() == "sigilo":
            with pensar("tutu escucha el humo..."):
                time.sleep(0.2)
                deidad_sig = _deidad_activa_canal or "tutu"
                try:
                    mem = ConversacionRepo.cargar(_proyecto_activo.hash, "tutu")
                    texto = _invocador.generar_intencion_sigilo(deidad_sig, mem)
                except Exception as e:
                    texto = f"[error: {e}]"
            console.print()
            console.print(Panel(
                f"[bold white]  ✦ {texto} ✦  [/bold white]",
                title="[dim]sigilo — a través del humo[/dim]",
                border_style="dim white",
                padding=(1, 4),
            ))
            console.print()
            continue

        # Comando: quién
        if mensaje.strip().lower() == "quién" or mensaje.strip().lower() == "quien":
            if _deidad_activa_canal:
                color = COLORES.get(_deidad_activa_canal, "white")
                icono = ICONOS.get(_deidad_activa_canal, "◉")
                console.print(f"\n  [{color}]{icono} {_deidad_activa_canal.upper()}[/{color}] [dim]está presente en este momento.[/dim]\n")
            else:
                console.print("\n  [dim]Tutu aún no ha sentido cuál deidad domina.[/dim]\n")
            continue

        # Flujo principal: TUTU escucha → detecta deidad → canaliza
        respuesta_texto = ""
        es_offline = False
        with pensar("tutu escucha el humo..."):
            time.sleep(0.2)
            try:
                # Paso 1: detectar qué deidad está activa con este mensaje
                deidad, *_ = _invocador.decidir_entidad(mensaje)
                _deidad_activa_canal = deidad

                # Paso 2: invocar la deidad internamente para obtener su respuesta
                resp_deidad = _invocador.invocar_deidad(
                    nombre=deidad,
                    mensaje=mensaje,
                    proyecto=_proyecto_activo,
                    esferas_bosque=esferas_bosque,
                )

                # Paso 3: TUTU canaliza — envuelve la voz de la deidad en su propio lenguaje
                mensaje_canal = (
                    f"El practicante preguntó: «{mensaje}»\n\n"
                    f"En el humo percibo a {deidad.capitalize()} respondiendo:\n"
                    f"«{resp_deidad.texto}»\n\n"
                    f"Canaliza esto en tu propia voz como Tutu. "
                    f"No repitas la respuesta textualmente — transmútala. "
                    f"Una sola pregunta al final, si la hay."
                )
                resp_tutu = _invocador.invocar_tutu(
                    mensaje=mensaje_canal,
                    proyecto=_proyecto_activo,
                    esferas_bosque=esferas_bosque,
                )
                respuesta_texto = resp_tutu.texto
                es_offline = resp_tutu.es_offline

            except Exception as e:
                respuesta_texto = f"[error: {e}]"
                es_offline = False
                deidad = None

        console.print()

        # Mostrar qué deidad está activa (sutil, como presencia)
        if _deidad_activa_canal:
            color_d = COLORES.get(_deidad_activa_canal, "dim")
            icono_d = ICONOS.get(_deidad_activa_canal, "·")
            console.print(f"  [dim]{icono_d} [{color_d}]{_deidad_activa_canal}[/{color_d}] presente en el humo[/dim]")

        console.print(Panel(
            f"[white]{respuesta_texto}[/white]",
            title="[bold white]🌀 tutu[/bold white]",
            border_style="white",
            padding=(0, 2),
        ))
        if es_offline:
            console.print("  [dim](offline)[/dim]")
        console.print()


def menu_altar():
    global _proyecto_activo

    if not _proyecto_activo:
        limpiar()
        cabecera()
        _seleccionar_o_crear_proyecto()

    limpiar()
    cabecera()
    separador("🕯  ALTAR", "dim white")
    _cabecera_altar()

    if _proyecto_activo:
        console.print(f"  [dim]proyecto: {_proyecto_activo.codigo}[/dim]")
        console.print()

    separador("🌀  TUTU — el humo habla", "white")
    console.print()
    _altar_canal_tutu()


# ═══════════════════════════════════════════════════════════════════════════
#  BIBLIOTECA
# ═══════════════════════════════════════════════════════════════════════════

def menu_bibliotecario():
    """Tutu (u otra entidad) revisa y completa los libros de la Biblioteca."""
    from pathlib import Path
    from tools.bibliotecario import revisar_biblioteca, NOMBRES_REGLAS

    entidad_actual = "tutu"

    while True:
        limpiar()
        cabecera()
        separador("📚 BIBLIOTECARIO", "dim white")
        console.print()
        color_e = COLORES.get(entidad_actual, "white")
        icono_e = ICONOS.get(entidad_actual, "◉")
        console.print(f"  [dim]bibliotecario:[/dim]  [{color_e}]{icono_e} {entidad_actual}[/{color_e}]")
        console.print()

        resultados = revisar_biblioteca()
        total = len(resultados)
        ok = sum(1 for r in resultados if r.ok)

        console.print(f"  [dim]libros revisados: {total}  —  en orden: {ok}  —  con problemas: {total - ok}[/dim]")
        console.print()

        for res in resultados:
            if res.ok:
                console.print(f"  [green]✓[/green]  {res.nombre}")
            else:
                console.print(f"  [yellow]✗[/yellow]  {res.nombre}")
                for regla in res.faltantes:
                    console.print(f"      [dim]→ {NOMBRES_REGLAS[regla]}[/dim]")

        console.print()
        separador()
        console.print()
        console.print("  [white]1[/white]  Corregir todos los libros con problemas")
        console.print("  [white]2[/white]  Cambiar entidad bibliotecaria")
        console.print("  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask("  [white]>[/white]", default="0").strip()

        if op == "0":
            break

        elif op == "2":
            console.print()
            for i, nombre in enumerate(_DEIDADES_ORDEN + ["tutu"], 1):
                c = COLORES.get(nombre, "white")
                console.print(f"  [white]{i}[/white]  [{c}]{ICONOS.get(nombre,'◉')} {nombre}[/{c}]")
            console.print()
            sel = Prompt.ask("  [white]>[/white]", default="1").strip()
            opciones = _DEIDADES_ORDEN + ["tutu"]
            if sel.isdigit() and 1 <= int(sel) <= len(opciones):
                entidad_actual = opciones[int(sel) - 1]

        elif op == "1":
            con_problemas = [r for r in resultados if not r.ok]
            if not con_problemas:
                console.print("\n  [green]Todos los libros están en orden.[/green]")
                esperar()
                continue

            for res in con_problemas:
                limpiar()
                cabecera()
                separador(f"📚 {res.nombre}", "dim white")
                console.print()
                console.print(f"  [dim]problemas:[/dim]  " + "  ·  ".join(
                    NOMBRES_REGLAS[r] for r in res.faltantes
                ))
                console.print()

                if not Confirm.ask(
                    f"  [{color_e}]¿{entidad_actual.capitalize()} corrige este libro?[/{color_e}]",
                    default=True
                ):
                    continue

                contenido = res.ruta.read_text(encoding="utf-8")
                titulo = res.ruta.stem.replace("_", " ").title()

                for regla in res.faltantes:
                    with pensar(f"{entidad_actual} trabajando en «{NOMBRES_REGLAS[regla]}»..."):
                        try:
                            respuesta = _invocador.completar_libro(
                                titulo=titulo,
                                contenido=contenido,
                                seccion_faltante=regla if regla != "titulo_mayusculas" else "titulo_mayusculas",
                                entidad=entidad_actual,
                            )
                            texto_generado = respuesta.texto.strip()
                        except Exception as e:
                            console.print(f"[red]  Error: {e}[/red]")
                            continue

                    console.print()
                    console.print(Panel(
                        texto_generado,
                        title=f"[{color_e}]{icono_e} {entidad_actual} — sugerencia[/{color_e}]",
                        border_style=color_e,
                        padding=(1, 2),
                    ))
                    console.print()

                    if regla == "titulo_mayusculas":
                        if Confirm.ask("  [white]¿Aplicar título en mayúsculas?[/white]", default=True):
                            lineas = contenido.splitlines()
                            for i, linea in enumerate(lineas):
                                if linea.startswith("# "):
                                    lineas[i] = "# " + linea[2:].upper()
                                    break
                            contenido = "\n".join(lineas)
                            res.ruta.write_text(contenido, encoding="utf-8")
                            console.print("  [green]✓ Título corregido.[/green]")

                    elif regla == "fuentes_presentes":
                        if Confirm.ask("  [white]¿Agregar esta sección al libro?[/white]", default=True):
                            if not contenido.endswith("\n"):
                                contenido += "\n"
                            contenido += "\n" + texto_generado + "\n"
                            res.ruta.write_text(contenido, encoding="utf-8")
                            console.print("  [green]✓ Sección FUENTES agregada.[/green]")

                    else:
                        if Confirm.ask("  [white]¿Agregar esta sección al libro?[/white]", default=True):
                            if not contenido.endswith("\n"):
                                contenido += "\n"
                            contenido += "\n" + texto_generado + "\n"
                            res.ruta.write_text(contenido, encoding="utf-8")
                            console.print(f"  [green]✓ Sección agregada.[/green]")

            esperar()


_ESTADO_COLOR = {
    "canon":   "bright_yellow",
    "arbol":   "green",
    "brote":   "cyan",
    "semilla": "dim",
    "humus":   "red",
}
_PAGINA_CHARS = 2000


def _leer_entrada(entrada: dict) -> None:
    """Muestra el contenido de una entrada con paginación simple."""
    contenido = entrada.get("contenido", "")
    titulo = entrada.get("titulo", "sin título")
    dominio = entrada.get("dominio", "")
    paginas = [contenido[i:i + _PAGINA_CHARS] for i in range(0, max(len(contenido), 1), _PAGINA_CHARS)]
    total = len(paginas)

    for n, pagina in enumerate(paginas, 1):
        limpiar()
        subtitulo = f"[dim]{dominio}[/dim]  —  pág {n}/{total}" if total > 1 else f"[dim]{dominio}[/dim]"
        console.print(Panel(
            pagina,
            title=f"[bold white]{titulo}[/bold white]",
            subtitle=subtitulo,
            border_style="dim yellow",
            padding=(1, 2),
        ))
        console.print()
        if n < total:
            console.print("  [dim]Enter → siguiente página   q → salir[/dim]")
            tecla = Prompt.ask("  [white]>[/white]", default="").strip().lower()
            if tecla == "q":
                return
        else:
            esperar()


def menu_biblioteca():
    filtro_dominio: str | None = None

    while True:
        limpiar()
        cabecera()
        separador(f"{ICONOS['biblioteca']} LIBRERÍA PERSONAL", "bright_yellow")
        console.print()

        entradas = EntradaRepo.listar(limite=200)

        # Agrupar por dominio
        dominios: dict[str, list] = {}
        for e in entradas:
            dominios.setdefault(e["dominio"], []).append(e)

        lista_filtrada = entradas if not filtro_dominio else [
            e for e in entradas if e["dominio"] == filtro_dominio
        ]

        if not entradas:
            console.print("  [dim]La biblioteca está vacía.[/dim]")
            console.print()
            console.print("  [white]1[/white]  Sembrar canon")
            console.print("  [dim]0  Volver[/dim]")
            console.print()
            op = Prompt.ask("  [white]>[/white]", default="0")
            if op == "1":
                n = sembrar_canon()
                console.print(f"[green]  ✓ {n} entradas sembradas[/green]")
                esperar()
            elif op == "0":
                break
            continue

        # Mostrar filtro activo
        if filtro_dominio:
            console.print(f"  [dim]dominio: [/dim][bright_yellow]{filtro_dominio}[/bright_yellow]  [dim](f → quitar filtro)[/dim]")
            console.print()

        # Mostrar índice numerado
        indice: dict[str, dict] = {}
        num = 1
        for dom, ents in sorted(dominios.items()):
            if filtro_dominio and dom != filtro_dominio:
                continue
            console.print(f"  [dim]── {dom} ──[/dim]")
            for e in ents:
                color = _ESTADO_COLOR.get(e["estado"], "white")
                console.print(
                    f"  [white]{num:>3}[/white]  "
                    f"[{color}]{e['estado']:8}[/{color}]  "
                    f"[white]{e['titulo']}[/white]"
                )
                indice[str(num)] = e
                num += 1
            console.print()

        separador()
        console.print()
        console.print("  [dim]Escribe un número para leer · f → filtrar dominio · b → sembrar canon · g → bibliotecario · 0 → volver[/dim]")
        console.print()

        op = Prompt.ask("  [white]>[/white]", default="0").strip().lower()

        if op == "0":
            break
        elif op == "f":
            doms_lista = sorted(dominios.keys())
            console.print()
            for i, d in enumerate(doms_lista, 1):
                console.print(f"  [white]{i}[/white]  {d}")
            console.print("  [dim]0  Todos[/dim]")
            console.print()
            sel = Prompt.ask("  [white]>[/white]", default="0").strip()
            if sel == "0":
                filtro_dominio = None
            elif sel.isdigit() and 1 <= int(sel) <= len(doms_lista):
                filtro_dominio = doms_lista[int(sel) - 1]
        elif op == "b":
            n = sembrar_canon()
            console.print(f"[green]  ✓ {n} entradas sembradas[/green]")
            esperar()
        elif op == "g":
            menu_bibliotecario()
        elif op in indice:
            _leer_entrada(indice[op])
        else:
            # Búsqueda por texto
            coincidencias = [
                e for e in lista_filtrada
                if op in e["titulo"].lower() or op in e.get("dominio", "").lower()
            ]
            if len(coincidencias) == 1:
                _leer_entrada(coincidencias[0])
            elif len(coincidencias) > 1:
                console.print()
                for i, e in enumerate(coincidencias, 1):
                    console.print(f"  [white]{i}[/white]  {e['titulo']}")
                console.print()
                sel = Prompt.ask("  [white]>[/white]", default="1").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(coincidencias):
                    _leer_entrada(coincidencias[int(sel) - 1])


# ═══════════════════════════════════════════════════════════════════════════
#  AYNI — RECIPROCIDAD
# ═══════════════════════════════════════════════════════════════════════════

from base_datos.ayni import AyniRepo, UMBRAL_DEUDA_NOTABLE

_ICONO_AYNI = "⚖"

_TIPOS_OFRENDA_CLI = {
    "1": ("agua",     "Agua",      "verter, ofrenda líquida, hidratación"),
    "2": ("tierra",   "Tierra",    "piedra, semilla, enterrar algo"),
    "3": ("fuego",    "Fuego",     "vela, incienso, quemar papel"),
    "4": ("aire",     "Aire",      "canto, soplo, palabra hablada"),
    "5": ("acto",     "Acto",      "acción concreta en el mundo"),
    "6": ("tiempo",   "Tiempo",    "tiempo dedicado a alguien o algo"),
    "7": ("creacion", "Creación",  "escritura, dibujo, música"),
    "8": ("silencio", "Silencio",  "meditación, contemplación, ayuno"),
}

_BALANCE_BARRA_WIDTH = 20


def _barra_balance(balance: int) -> str:
    """Barra visual del balance ayni centrada en cero."""
    centro = _BALANCE_BARRA_WIDTH // 2
    if balance >= 0:
        llenos = min(balance, centro)
        barra = "░" * (centro - llenos) + "█" * llenos + "|" + "░" * centro
        color = "green" if balance > 0 else "dim"
    else:
        vacios = min(-balance, centro)
        barra = "░" * centro + "|" + "█" * vacios + "░" * (centro - vacios)
        color = "yellow" if balance > UMBRAL_DEUDA_NOTABLE else "red"
    return f"[{color}]{barra}[/{color}]  [{color}]{balance:+d}[/{color}]"


def menu_ayni():
    global _proyecto_activo

    if not _proyecto_activo:
        limpiar()
        cabecera()
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    while True:
        limpiar()
        cabecera()
        separador(f"{_ICONO_AYNI} AYNI — RECIPROCIDAD", "green")
        console.print()

        assert _proyecto_activo is not None
        bal = AyniRepo.balance(_proyecto_activo.hash)
        abiertas = AyniRepo.deudas_abiertas(_proyecto_activo.hash)

        console.print(f"  [dim]balance:[/dim]  {_barra_balance(bal)}")
        console.print(f"  [dim]deudas abiertas: {len(abiertas)}[/dim]")
        if bal <= UMBRAL_DEUDA_NOTABLE:
            console.print(f"  [red]  El ayni pide reciprocidad — hay deuda significativa.[/red]")
        elif bal > 3:
            console.print(f"  [green]  Crédito de ayni — das más de lo que pides.[/green]")
        console.print()

        separador()
        console.print()
        console.print(f"  [green]1[/green]  Hacer ofrenda")
        console.print(f"  [green]2[/green]  Ver deudas abiertas")
        console.print(f"  [green]3[/green]  Historial")
        console.print()
        console.print(f"  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask(f"  [green]>[/green]", default="0")

        if op == "1":
            limpiar()
            cabecera()
            _hacer_ofrenda()
            esperar()
        elif op == "2":
            limpiar()
            cabecera()
            _ver_deudas_ayni()
            esperar()
        elif op == "3":
            limpiar()
            cabecera()
            _historial_ayni()
            esperar()
        elif op == "0":
            break


def _hacer_ofrenda():
    global _proyecto_activo
    assert _proyecto_activo is not None

    console.print()
    separador("OFRENDA", "green")
    console.print()
    console.print("[dim]Una ofrenda es un acto real de reciprocidad — no simbólico, sino concreto.[/dim]")
    console.print()

    # Tipo
    for k, (_, nombre, desc) in _TIPOS_OFRENDA_CLI.items():
        console.print(f"  [green]{k}[/green]  [white]{nombre:10}[/white]  [dim]{desc}[/dim]")
    console.print()
    tipo_op = Prompt.ask("  [green]Tipo[/green]",
                         choices=list(_TIPOS_OFRENDA_CLI.keys()), default="1")
    tipo_slug, tipo_nombre, _ = _TIPOS_OFRENDA_CLI[tipo_op]

    # Descripción
    console.print()
    descripcion = Prompt.ask(f"  [green]¿Qué ofrendas concretamente?[/green]").strip()
    if not descripcion:
        console.print("[yellow]  Descripción vacía. Cancelado.[/yellow]")
        return

    # Peso (cuánta deuda cierra)
    console.print()
    console.print("  [dim]Peso de la ofrenda — qué tan significativa es para ti:[/dim]")
    console.print("  [dim]1 = gesto pequeño   2 = acto real   3 = ofrenda significativa[/dim]")
    peso_str = Prompt.ask("  [green]Peso[/green]", choices=["1", "2", "3"], default="1")
    peso = int(peso_str)

    # Vincular a deuda específica (opcional)
    abiertas = AyniRepo.deudas_abiertas(_proyecto_activo.hash)
    deuda_id: int | None = None
    if abiertas:
        console.print()
        console.print(f"  [dim]¿Vincular a una deuda abierta? (enter para ofrenda libre)[/dim]")
        for d in abiertas[:6]:
            console.print(f"    [dim]#{d['id']}  {d['tipo_origen']:12}  "
                          f"peso {d['peso']}  «{d['descripcion'][:45]}»[/dim]")
        console.print()
        id_str = Prompt.ask("  [green]ID deuda[/green]  [dim](enter para ninguna)[/dim]",
                            default="").strip()
        if id_str.isdigit():
            candidata = AyniRepo.deuda_por_id(int(id_str))
            if candidata and candidata["proyecto_hash"] == _proyecto_activo.hash:
                deuda_id = int(id_str)

    AyniRepo.registrar_ofrenda(
        proyecto_hash=_proyecto_activo.hash,
        tipo=tipo_slug,
        descripcion=descripcion,
        peso=peso,
        deuda_id=deuda_id,
    )

    bal_nuevo = AyniRepo.balance(_proyecto_activo.hash)
    console.print()
    msg = f"[green]  ✓ Ofrenda de {tipo_nombre} registrada.[/green]"
    if deuda_id:
        msg += f"  [dim]Deuda #{deuda_id} cerrada.[/dim]"
    console.print(msg)
    console.print(f"  [dim]Balance ayni ahora:[/dim]  {_barra_balance(bal_nuevo)}")


def _ver_deudas_ayni():
    assert _proyecto_activo is not None

    abiertas = AyniRepo.deudas_abiertas(_proyecto_activo.hash)
    console.print()
    separador("DEUDAS ABIERTAS", "green")
    console.print()

    if not abiertas:
        console.print("  [dim]No hay deudas abiertas. El ayni está en equilibrio.[/dim]")
        return

    _TIPO_COLOR = {
        "manifestacion": "bright_yellow",
        "sigilo":        "yellow",
        "limpia":        "green",
        "consulta":      "dim",
    }
    for d in abiertas:
        color = _TIPO_COLOR.get(d["tipo_origen"], "white")
        console.print(
            f"  [dim]#{d['id']}[/dim]  [{color}]{d['tipo_origen']:14}[/{color}]  "
            f"[white]peso {d['peso']}[/white]  [dim]{d['created_at'][:10]}[/dim]"
        )
        console.print(f"    [dim italic]«{d['descripcion'][:70]}»[/dim italic]")
    console.print()
    total = sum(d["peso"] for d in abiertas)
    console.print(f"  [dim]Peso total de deuda abierta: {total}[/dim]")


def _historial_ayni():
    assert _proyecto_activo is not None

    deudas = AyniRepo.historial_deudas(_proyecto_activo.hash, limite=15)
    ofrendas = AyniRepo.historial_ofrendas(_proyecto_activo.hash, limite=15)

    console.print()
    separador("HISTORIAL AYNI", "green")
    console.print()

    if deudas:
        console.print("  [dim]── PETICIONES ──[/dim]")
        for d in deudas:
            estado_c = "green" if d["estado"] == "cerrada" else "yellow"
            console.print(
                f"  [{estado_c}]{'✓' if d['estado']=='cerrada' else '○'}[/{estado_c}]  "
                f"[dim]#{d['id']}  {d['tipo_origen']:12}  peso {d['peso']}  "
                f"{d['created_at'][:10]}[/dim]  "
                f"[dim italic]«{d['descripcion'][:50]}»[/dim italic]"
            )

    if ofrendas:
        console.print()
        console.print("  [dim]── OFRENDAS ──[/dim]")
        for o in ofrendas:
            console.print(
                f"  [green]✦[/green]  [dim]#{o['id']}  {o['tipo']:10}  peso {o['peso']}  "
                f"{o['created_at'][:10]}[/dim]  "
                f"[dim italic]«{o['descripcion'][:50]}»[/dim italic]"
            )

    if not deudas and not ofrendas:
        console.print("  [dim]Sin historial de ayni todavía.[/dim]")


# ═══════════════════════════════════════════════════════════════════════════
#  LIMPIA DIGITAL
# ═══════════════════════════════════════════════════════════════════════════

from base_datos.limpia import LimpiaRepo

_ICONO_LIMPIA = "🌿"

_TRADICIONES_LIMPIA = {
    "1": ("saminchakuy",  "Saminchakuy",   "andino · tierra · sami/hucha",    "artemisa"),
    "2": ("curanderismo", "Curanderismo",  "plantas · huevo · barrida",        "lilith"),
}

_ESTADO_LIMPIA_COLOR = {
    "pendiente":  "yellow",
    "completada": "green",
}


def menu_limpia():
    global _proyecto_activo

    if not _proyecto_activo:
        limpiar()
        cabecera()
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    while True:
        limpiar()
        cabecera()
        separador(f"{_ICONO_LIMPIA} LIMPIA DIGITAL", "green")
        console.print()
        console.print("[dim]Ritual de limpieza energética antes de operaciones mayores.[/dim]")
        console.print("[dim]Registra lo que arrastras, realiza el ritual guiado y reporta el cambio.[/dim]")
        console.print()

        historial = LimpiaRepo.listar(_proyecto_activo.hash, limite=5)
        pendientes = [l for l in historial if l["estado"] == "pendiente"]
        if pendientes:
            console.print(f"  [yellow]⚡ {len(pendientes)} limpia(s) pendiente(s) de cerrar[/yellow]")
            console.print()

        separador()
        console.print()
        console.print(f"  [green]1[/green]  Nueva limpia")
        console.print(f"  [green]2[/green]  Cerrar limpia pendiente")
        console.print(f"  [green]3[/green]  Historial")
        console.print()
        console.print(f"  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask(f"  [green]>[/green]", default="0")

        if op == "1":
            limpiar()
            cabecera()
            _iniciar_limpia()
            esperar()
        elif op == "2":
            limpiar()
            cabecera()
            _cerrar_limpia_pendiente()
            esperar()
        elif op == "3":
            limpiar()
            cabecera()
            _historial_limpias()
            esperar()
        elif op == "0":
            break


def _iniciar_limpia():
    global _proyecto_activo
    assert _proyecto_activo is not None

    console.print()
    separador("NUEVA LIMPIA", "green")
    console.print()
    console.print("[dim]Describe brevemente lo que estás cargando: tensión, bloqueo, miedo, relación, etc.[/dim]")
    console.print()

    estado_pre = Prompt.ask(f"  [green]{_ICONO_LIMPIA} ¿Qué arrastras?[/green]").strip()
    if not estado_pre:
        console.print("[yellow]  Descripción vacía. Cancelado.[/yellow]")
        return

    # Elegir tradición
    console.print()
    separador("TRADICIÓN", "dim")
    console.print()
    for k, (_, nombre, desc, ent_sug) in _TRADICIONES_LIMPIA.items():
        color_e = COLORES[ent_sug]
        console.print(
            f"  [green]{k}[/green]  [white]{nombre}[/white]  [dim]{desc}[/dim]  "
            f"  [{color_e}]→ {ent_sug}[/{color_e}]"
        )
    console.print()
    trad_op = Prompt.ask("  [green]Tradición[/green]", choices=["1", "2"], default="1")
    trad_slug, trad_nombre, _, entidad_sugerida = _TRADICIONES_LIMPIA[trad_op]

    # Elegir entidad guía (sugerida según tradición, pero libre)
    console.print()
    console.print(f"  [dim]Entidad guía sugerida: {entidad_sugerida}[/dim]")
    console.print(f"  [dim]  a = artemisa   l = lilith[/dim]")
    ent_op = Prompt.ask("  [green]Entidad[/green]", choices=["a", "l"],
                        default="a" if entidad_sugerida == "artemisa" else "l")
    entidad = "artemisa" if ent_op == "a" else "lilith"

    # Guardar e invocar guía
    registro = LimpiaRepo.iniciar(
        proyecto_hash=_proyecto_activo.hash,
        tradicion=trad_slug,
        entidad=entidad,
        estado_pre=estado_pre,
    )

    esferas_bosque = []
    try:
        esferas_bosque = [dict(e) for e in EsferaRepo.listar_activas()]
    except Exception:
        pass

    console.print()
    with pensar(f"{entidad} prepara el ritual..."):
        time.sleep(0.2)
        try:
            resp = _invocador.guiar_limpia(
                tradicion=trad_slug,
                entidad=entidad,
                estado_pre=estado_pre,
                proyecto=_proyecto_activo,
                esferas_bosque=esferas_bosque,
            )
            guia_texto = resp.texto
            es_offline = resp.es_offline
        except Exception as e:
            guia_texto = f"[error: {e}]"
            es_offline = False

    color_e = COLORES[entidad]
    console.print(Panel(
        f"[{color_e}]{guia_texto}[/{color_e}]",
        title=f"[{color_e}]{ICONOS[entidad]} {entidad} — {trad_nombre}[/{color_e}]",
        border_style=color_e,
        padding=(1, 2),
    ))
    if es_offline:
        console.print("  [dim](offline)[/dim]")

    console.print()
    console.print(f"[green]  ✓ Limpia #{registro['id']} iniciada.[/green]  "
                  f"[dim]Realiza el ritual y vuelve a cerrarla con 'Cerrar limpia pendiente'.[/dim]")
    try:
        from base_datos.ayni import AyniRepo as _AyniRepo
        _AyniRepo.registrar_deuda(
            _proyecto_activo.hash, "limpia",
            f"limpia {registro['tradicion']}", origen_id=registro["id"],
        )
    except Exception:
        pass


def _cerrar_limpia_pendiente():
    global _proyecto_activo
    assert _proyecto_activo is not None

    pendientes = [l for l in LimpiaRepo.listar(_proyecto_activo.hash) if l["estado"] == "pendiente"]
    if not pendientes:
        console.print()
        console.print("  [dim]No hay limpias pendientes de cerrar.[/dim]")
        return

    console.print()
    separador("CERRAR LIMPIA", "green")
    console.print()

    for l in pendientes:
        color_e = COLORES.get(l["entidad"], "white")
        console.print(
            f"  [green]#{l['id']}[/green]  [{color_e}]{l['entidad']}[/{color_e}]  "
            f"[dim]{l['tradicion']}  {l['created_at'][:10]}[/dim]"
        )
        console.print(f"    [dim italic]«{l['estado_pre'][:70]}»[/dim italic]")
        console.print()

    id_str = Prompt.ask("  [green]ID de la limpia[/green]").strip()
    if not id_str.isdigit():
        console.print("[yellow]  ID inválido.[/yellow]")
        return

    l = LimpiaRepo.por_id(int(id_str))
    if not l or l["proyecto_hash"] != _proyecto_activo.hash or l["estado"] != "pendiente":
        console.print("[yellow]  Limpia no encontrada o ya cerrada.[/yellow]")
        return

    console.print()
    console.print(f"  [dim italic]Antes: «{l['estado_pre']}»[/dim italic]")
    console.print()
    estado_post = Prompt.ask(f"  [green]{_ICONO_LIMPIA} ¿Qué sientes ahora? ¿Qué se movió?[/green]").strip()
    if not estado_post:
        console.print("[yellow]  Descripción vacía. Cancelado.[/yellow]")
        return

    LimpiaRepo.completar(l["id"], estado_post)

    esferas_bosque = []
    try:
        esferas_bosque = [dict(e) for e in EsferaRepo.listar_activas()]
    except Exception:
        pass

    with pensar(f"{l['entidad']} cierra el ciclo..."):
        time.sleep(0.2)
        try:
            resp = _invocador.cerrar_limpia(
                tradicion=l["tradicion"],
                entidad=l["entidad"],
                estado_pre=l["estado_pre"],
                estado_post=estado_post,
                proyecto=_proyecto_activo,
                esferas_bosque=esferas_bosque,
            )
            cierre_texto = resp.texto
            es_offline = resp.es_offline
        except Exception as e:
            cierre_texto = f"[error: {e}]"
            es_offline = False

    console.print()
    entidad = l["entidad"]
    color_e = COLORES.get(entidad, "green")
    console.print(Panel(
        f"[{color_e}]{cierre_texto}[/{color_e}]",
        title=f"[{color_e}]{ICONOS.get(entidad, _ICONO_LIMPIA)} {entidad} — cierre[/{color_e}]",
        border_style=color_e,
        padding=(1, 2),
    ))
    if es_offline:
        console.print("  [dim](offline)[/dim]")

    # Evento en el bosque
    try:
        EventoRepo.registrar(
            tipo_evento="rito_origen",
            tipo_esfera="limpia",
            clave_esfera=f"limpia_{l['id']}",
            detalle={"tradicion": l["tradicion"], "entidad": entidad},
            proyecto_hash=_proyecto_activo.hash,
            entidad=entidad,
        )
    except Exception:
        pass

    console.print()
    console.print(f"[green]  ✓ Limpia #{l['id']} completada.[/green]")


def _historial_limpias():
    assert _proyecto_activo is not None
    historial = LimpiaRepo.listar(_proyecto_activo.hash)
    if not historial:
        console.print()
        console.print("  [dim]Sin limpias registradas.[/dim]")
        return

    console.print()
    separador("HISTORIAL DE LIMPIAS", "green")
    console.print()

    for l in historial:
        color_estado = _ESTADO_LIMPIA_COLOR.get(l["estado"], "white")
        color_e = COLORES.get(l["entidad"], "white")
        console.print(
            f"  [dim]#{l['id']}[/dim]  "
            f"[{color_estado}]{l['estado']:10}[/{color_estado}]  "
            f"[{color_e}]{l['entidad']:8}[/{color_e}]  "
            f"[dim]{l['tradicion']:12}  {l['created_at'][:10]}[/dim]"
        )
        console.print(f"    [dim italic]antes:  «{l['estado_pre'][:65]}»[/dim italic]")
        if l.get("estado_post"):
            console.print(f"    [dim italic]después: «{l['estado_post'][:65]}»[/dim italic]")
        console.print()


# ═══════════════════════════════════════════════════════════════════════════
#  MANIFESTACIÓN
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
#  SIGILO OPERATIVO — ciclo completo Carroll
# ═══════════════════════════════════════════════════════════════════════════

_METODOS_GNOSIS_CLI = {
    "1": ("meditacion_vacia",    "Meditación Vacía",            "inhibitoria"),
    "2": ("hiperventilacion",    "Hiperventilación Controlada", "excitatoria"),
    "3": ("movimiento_extatico", "Movimiento Extático",         "excitatoria"),
    "4": ("risa_banishing",      "Risa del Caos",               "excitatoria"),
    "5": ("privacion_sensorial", "Privación Sensorial",         "inhibitoria"),
    "6": ("orgasmo",             "Orgasmo Mágico",              "excitatoria"),
}

_ESTADO_SIGILO_COLOR = {
    "creado":   ("dim white",     "sin cargar"),
    "olvidado": ("yellow",        "en olvido"),
    "revelado": ("bright_yellow", "revelado"),
    "quemado":  ("dim",           "quemado"),
}

_ICONO_SIGILO = "◈"


def _mostrar_glifo(glifo: str, letras: str, color: str = "bright_yellow"):
    """Renderiza el glifo en un panel visual."""
    console.print(Panel(
        f"[{color}]{glifo}[/{color}]",
        title=f"[dim]{letras}[/dim]",
        border_style=color,
        padding=(0, 2),
        expand=False,
    ))


def _crear_sigilo_nuevo():
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    console.print()
    separador("CREAR SIGILO", "bright_yellow")
    console.print()
    console.print("[dim]Método Carroll: se eliminan vocales y letras repetidas de tu intención.[/dim]")
    console.print("[dim]El resultado son las letras que forman el glifo.[/dim]")
    console.print()

    intencion = Prompt.ask("  [bright_yellow]Intención[/bright_yellow]  [dim](presente, positiva, concreta)[/dim]").strip()
    if not intencion:
        console.print("[yellow]  Intención vacía. Cancelado.[/yellow]")
        return

    letras = letras_carroll(intencion)
    glifo = glifo_ascii(letras)

    console.print()
    console.print("  [dim]Letras Carroll:[/dim]")
    console.print(f"  [{COLORES['isis']}]{letras}[/{COLORES['isis']}]")
    console.print()
    console.print("  [dim]Glifo generado:[/dim]")
    _mostrar_glifo(glifo, letras, COLORES["isis"])

    console.print()
    console.print("[dim]Días de olvido — cuánto tiempo el sistema ocultará la intención:[/dim]")
    console.print("  [dim]7  = una semana    14 = dos semanas    21 = luna nueva a luna nueva[/dim]")
    dias_str = Prompt.ask("  [bright_yellow]Días de olvido[/bright_yellow]", default="14")
    try:
        dias_olvido = max(3, min(90, int(dias_str)))
    except ValueError:
        dias_olvido = 14

    console.print()
    if not Confirm.ask(
        f"  [bright_yellow]¿Crear sigilo con {dias_olvido} días de olvido?[/bright_yellow]",
        default=True,
    ):
        console.print("[dim]  Cancelado.[/dim]")
        return

    s = SigiloOperativoRepo.crear(
        proyecto_hash=_proyecto_activo.hash,
        intencion=intencion,
        dias_olvido=dias_olvido,
    )
    console.print()
    console.print(f"[bright_yellow]  ✓ Sigilo #{s['id']} creado.[/bright_yellow]  "
                  f"[dim]Pendiente de carga.[/dim]")
    try:
        from base_datos.ayni import AyniRepo as _AyniRepo
        _AyniRepo.registrar_deuda(
            _proyecto_activo.hash, "sigilo",
            f"sigilo {s['letras_base']}", origen_id=s["id"],
        )
    except Exception:
        pass


def _realizar_carga_sigilo():
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    creados = SigiloOperativoRepo.listar(_proyecto_activo.hash, estado="creado")
    if not creados:
        console.print()
        console.print("  [dim]No hay sigilos pendientes de carga.[/dim]")
        return

    console.print()
    separador("CARGAR SIGILO", "bright_yellow")
    console.print()
    console.print("[dim]Sigilos sin cargar:[/dim]")
    console.print()
    for s in creados:
        console.print(f"  [bright_yellow]#{s['id']}[/bright_yellow]  "
                      f"[dim]{s['letras_base']}[/dim]  "
                      f"[dim italic]creado {s['created_at'][:10]}[/dim italic]")

    console.print()
    id_str = Prompt.ask("  [bright_yellow]ID del sigilo a cargar[/bright_yellow]").strip()
    if not id_str.isdigit():
        console.print("[yellow]  ID inválido.[/yellow]")
        return

    s = SigiloOperativoRepo.por_id(int(id_str))
    if not s or s["proyecto_hash"] != _proyecto_activo.hash:
        console.print("[yellow]  Sigilo no encontrado.[/yellow]")
        return
    if s["estado"] != "creado":
        console.print("[yellow]  Este sigilo ya fue cargado.[/yellow]")
        return

    # Mostrar glifo
    console.print()
    _mostrar_glifo(s["glifo"], s["letras_base"])
    console.print()

    # Elegir método de gnosis
    separador("MÉTODO DE GNOSIS", "dim")
    console.print()
    for k, (_, nombre, familia) in _METODOS_GNOSIS_CLI.items():
        fam_color = "cyan" if familia == "inhibitoria" else "magenta"
        console.print(f"  [bright_yellow]{k}[/bright_yellow]  [white]{nombre}[/white]  "
                      f"[{fam_color}]{familia}[/{fam_color}]")
    console.print()
    met_op = Prompt.ask("  [bright_yellow]Método[/bright_yellow]",
                        choices=list(_METODOS_GNOSIS_CLI.keys()), default="1")
    metodo_slug, metodo_nombre, _ = _METODOS_GNOSIS_CLI[met_op]

    # Confirmar días de olvido
    console.print()
    dias_actual = s["dias_olvido"]
    dias_str = Prompt.ask(
        f"  [bright_yellow]Días de olvido[/bright_yellow]  [dim](actual: {dias_actual})[/dim]",
        default=str(dias_actual),
    )
    try:
        dias_olvido = max(3, min(90, int(dias_str)))
    except ValueError:
        dias_olvido = dias_actual

    # Guía de carga por IA
    esferas_bosque = []
    try:
        esferas_bosque = [dict(e) for e in EsferaRepo.listar_activas()]
    except Exception:
        pass

    console.print()
    with pensar("preparando el ritual de carga..."):
        time.sleep(0.2)
        try:
            resp = _invocador.guiar_carga_sigilo(
                metodo_gnosis=metodo_nombre,
                glifo=s["glifo"],
                letras=s["letras_base"],
                proyecto=_proyecto_activo,
                esferas_bosque=esferas_bosque,
            )
            guia_texto = resp.texto
        except Exception as e:
            guia_texto = f"[error: {e}]"

    console.print(Panel(
        f"[cyan]{guia_texto}[/cyan]",
        title=f"[cyan]💧 lilith — guía de carga · {metodo_nombre}[/cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))

    console.print()
    console.print("[dim]Realiza el método indicado ahora.[/dim]")
    console.print("[dim]Cuando termines y hayas proyectado el glifo en el pico de gnosis:[/dim]")
    console.print()

    if not Confirm.ask("  [bright_yellow]¿El sigilo fue cargado?[/bright_yellow]", default=True):
        console.print("[dim]  Cancelado. El sigilo queda pendiente.[/dim]")
        return

    # Activar olvido
    SigiloOperativoRepo.cargar(s["id"], metodo_slug, dias_olvido)

    from datetime import datetime, timedelta
    fecha_rev = (datetime.now() + timedelta(days=dias_olvido)).strftime("%Y-%m-%d")

    console.print()
    console.print(Panel(
        f"[bright_yellow]El sigilo ha sido cargado.[/bright_yellow]\n\n"
        f"[dim]La intención queda oculta por {dias_olvido} días.\n"
        f"Se revelará el [white]{fecha_rev}[/white].\n"
        f"No pienses en él. Eso es el olvido.[/dim]",
        border_style="bright_yellow",
        padding=(1, 2),
    ))


def _ver_sigilos():
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    todos = SigiloOperativoRepo.listar(_proyecto_activo.hash)
    if not todos:
        console.print()
        console.print("  [dim]No hay sigilos creados aún.[/dim]")
        return

    console.print()
    separador("SIGILOS", "bright_yellow")

    revelaciones = SigiloOperativoRepo.revelaciones_pendientes(_proyecto_activo.hash)
    if revelaciones:
        console.print()
        console.print(f"  [bright_yellow]⚡ {len(revelaciones)} sigilo(s) listo(s) para revelar[/bright_yellow]")

    console.print()
    for s in todos:
        color, estado_desc = _ESTADO_SIGILO_COLOR.get(s["estado"], ("white", s["estado"]))
        dias_rest = SigiloOperativoRepo.dias_restantes_olvido(s)

        if s["estado"] == "olvidado":
            # Intención oculta — mostrar solo el glifo y letras
            if dias_rest > 0:
                tiempo_str = f"[yellow]revela en {dias_rest:.0f}d[/yellow]"
            else:
                tiempo_str = "[bright_yellow]⚡ listo para revelar[/bright_yellow]"
            console.print(
                f"\n  [bright_yellow]{_ICONO_SIGILO}[/bright_yellow]  "
                f"[dim]#{s['id']}[/dim]  "
                f"[{color}]{estado_desc}[/{color}]  {tiempo_str}"
            )
            console.print(f"  [dim]letras: {s['letras_base']}[/dim]")
            console.print(f"  [dim]intención: {'█' * min(20, len(s['intencion']))}[/dim]")
            _mostrar_glifo(s["glifo"], s["letras_base"], "yellow")

        elif s["estado"] == "creado":
            console.print(
                f"\n  [dim]{_ICONO_SIGILO}[/dim]  "
                f"[dim]#{s['id']}[/dim]  [{color}]{estado_desc}[/{color}]  "
                f"[dim]{s['created_at'][:10]}[/dim]"
            )
            console.print(f"  [dim]intención: {s['intencion'][:60]}[/dim]")
            console.print(f"  [dim]letras: {s['letras_base']}[/dim]")

        else:
            # revelado o quemado — intención visible
            console.print(
                f"\n  [{color}]{_ICONO_SIGILO}[/{color}]  "
                f"[dim]#{s['id']}[/dim]  [{color}]{estado_desc}[/{color}]  "
                f"[dim]{s['created_at'][:10]}[/dim]"
            )
            console.print(f"  [dim italic]«{s['intencion'][:70]}»[/dim italic]")
            if s["estado"] == "revelado":
                _mostrar_glifo(s["glifo"], s["letras_base"], "bright_yellow")
            if s.get("resultado"):
                console.print(f"  [dim]resultado: {s['resultado'][:80]}[/dim]")


def _revelar_y_quemar_sigilo():
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    # Buscar sigilos revelables (olvido vencido) o ya revelados
    listos = SigiloOperativoRepo.revelaciones_pendientes(_proyecto_activo.hash)
    ya_revelados = SigiloOperativoRepo.listar(_proyecto_activo.hash, estado="revelado")

    if not listos and not ya_revelados:
        console.print()
        olvidados = SigiloOperativoRepo.listar(_proyecto_activo.hash, estado="olvidado")
        if olvidados:
            s = olvidados[0]
            dias = SigiloOperativoRepo.dias_restantes_olvido(s)
            console.print(f"  [dim]El sigilo más próximo se revela en {dias:.1f} días.[/dim]")
        else:
            console.print("  [dim]No hay sigilos para revelar.[/dim]")
        return

    console.print()
    separador("REVELAR / QUEMAR", "bright_yellow")
    console.print()

    opciones = listos + ya_revelados
    for s in opciones:
        estado_str = "listo para revelar" if s in listos else "revelado"
        console.print(f"  [bright_yellow]#{s['id']}[/bright_yellow]  "
                      f"[dim]{estado_str}  letras: {s['letras_base']}[/dim]")

    console.print()
    id_str = Prompt.ask("  [bright_yellow]ID del sigilo[/bright_yellow]").strip()
    if not id_str.isdigit():
        console.print("[yellow]  ID inválido.[/yellow]")
        return

    sigilo_id = int(id_str)
    s = SigiloOperativoRepo.por_id(sigilo_id)
    if not s or s["proyecto_hash"] != _proyecto_activo.hash:
        console.print("[yellow]  Sigilo no encontrado.[/yellow]")
        return

    # Intentar revelar si está en olvido
    if s["estado"] == "olvidado":
        s = SigiloOperativoRepo.revelar(sigilo_id)
        if s is None:
            raw = SigiloOperativoRepo.por_id(sigilo_id) or {}
            dias = SigiloOperativoRepo.dias_restantes_olvido(raw)
            console.print(f"[yellow]  Todavía en olvido. Faltan {dias:.1f} días.[/yellow]")
            return

    if s["estado"] not in ("revelado",):
        console.print("[yellow]  Este sigilo no está en estado revelado.[/yellow]")
        return

    # Mostrar sigilo completo por primera vez
    console.print()
    console.print(Panel(
        f"[bright_yellow]Intención original:[/bright_yellow]\n\n"
        f"[white italic]«{s['intencion']}»[/white italic]",
        border_style="bright_yellow",
        padding=(1, 3),
    ))
    console.print()
    _mostrar_glifo(s["glifo"], s["letras_base"])
    console.print()

    console.print("[dim]El ciclo se cierra. ¿Qué ocurrió desde que cargaste este sigilo?[/dim]")
    console.print()
    resultado = Prompt.ask("  [bright_yellow]Resultado / observación[/bright_yellow]").strip()
    if not resultado:
        console.print("[yellow]  Observación vacía. El sigilo queda revelado.[/yellow]")
        return

    # IA interpreta y cierra
    esferas_bosque = []
    try:
        esferas_bosque = [dict(e) for e in EsferaRepo.listar_activas()]
    except Exception:
        pass

    with pensar("isis cierra el ciclo..."):
        time.sleep(0.2)
        try:
            resp = _invocador.interpretar_resultado_sigilo(
                intencion=s["intencion"],
                letras=s["letras_base"],
                metodo_gnosis=s.get("metodo_gnosis") or "desconocido",
                dias_olvido=s["dias_olvido"],
                resultado=resultado,
                proyecto=_proyecto_activo,
                esferas_bosque=esferas_bosque,
            )
            cierre_texto = resp.texto
        except Exception as e:
            cierre_texto = f"[error: {e}]"

    console.print()
    console.print(Panel(
        f"[{COLORES['isis']}]{cierre_texto}[/{COLORES['isis']}]",
        title=f"[{COLORES['isis']}]{ICONOS['isis']} isis — cierre del sigilo[/{COLORES['isis']}]",
        border_style=COLORES["isis"],
        padding=(1, 2),
    ))

    # Quemar
    console.print()
    if Confirm.ask("  [bright_yellow]¿Quemar el sigilo y cerrar el ciclo?[/bright_yellow]", default=True):
        SigiloOperativoRepo.quemar(sigilo_id, resultado)

        # Evento en el bosque
        try:
            EventoRepo.registrar(
                tipo_evento="esfera_disuelve",
                tipo_esfera="sigilo",
                clave_esfera=f"sigilo_{sigilo_id}",
                detalle={"letras": s["letras_base"], "resultado": resultado[:60]},
                proyecto_hash=_proyecto_activo.hash,
            )
        except Exception:
            pass

        console.print()
        console.print(f"[bright_yellow]  ✓ Sigilo #{sigilo_id} quemado.[/bright_yellow]  "
                      f"[dim]El ciclo está cerrado.[/dim]")


def menu_sigilo_operativo():
    global _proyecto_activo

    if not _proyecto_activo:
        limpiar()
        cabecera()
        _seleccionar_o_crear_proyecto()

    while True:
        limpiar()
        cabecera()
        separador(f"{_ICONO_SIGILO} SIGILO", "bright_yellow")
        console.print()
        console.print("[dim]Ciclo Carroll completo: intención → glifo → gnosis → olvido → revelación → quema.[/dim]")
        console.print()

        if _proyecto_activo:
            creados = len(SigiloOperativoRepo.listar(_proyecto_activo.hash, estado="creado"))
            olvidados = SigiloOperativoRepo.listar(_proyecto_activo.hash, estado="olvidado")
            listos = SigiloOperativoRepo.revelaciones_pendientes(_proyecto_activo.hash)

            resumen = f"  [dim]sin cargar: {creados}  en olvido: {len(olvidados)}[/dim]"
            if listos:
                resumen += f"  [bright_yellow]⚡ {len(listos)} listo(s)[/bright_yellow]"
            console.print(resumen)
            console.print()

        separador()
        console.print()
        console.print(f"  [bright_yellow]1[/bright_yellow]  Crear sigilo")
        console.print(f"  [bright_yellow]2[/bright_yellow]  Cargar sigilo  [dim](ritual de gnosis)[/dim]")
        console.print(f"  [bright_yellow]3[/bright_yellow]  Ver sigilos")
        console.print(f"  [bright_yellow]4[/bright_yellow]  Revelar y quemar")
        console.print()
        console.print(f"  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask(f"  [bright_yellow]>[/bright_yellow]", default="0")

        if op == "1":
            limpiar()
            cabecera()
            _crear_sigilo_nuevo()
            esperar()
        elif op == "2":
            limpiar()
            cabecera()
            _realizar_carga_sigilo()
            esperar()
        elif op == "3":
            limpiar()
            cabecera()
            _ver_sigilos()
            esperar()
        elif op == "4":
            limpiar()
            cabecera()
            _revelar_y_quemar_sigilo()
            esperar()
        elif op == "0":
            break


_TIPOS_MANIFESTACION = {
    "1": ("peticion",      "una solicitud al universo",              "🙏"),
    "2": ("decreto",       "una declaración de lo que ya es",        "⚡"),
    "3": ("transmutacion", "convertir una sombra en su opuesto",     "🔄"),
}

_ESTADO_RESULTADO_OPTS = {
    "1": ("senal",    "recibí una señal",     "green"),
    "2": ("cumplida", "se cumplió",           "bright_yellow"),
    "3": ("en_curso", "en movimiento",        "cyan"),
    "4": ("sin_senal","sin señal todavía",    "dim"),
}


def _declarar_manifestacion():
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    console.print()
    separador("DECLARAR MANIFESTACIÓN", "bright_yellow")
    console.print()
    console.print("[dim]Una manifestación es una intención declarada ante una entidad testigo.[/dim]")
    console.print()

    # Tipo
    for k, (tipo, desc, icono) in _TIPOS_MANIFESTACION.items():
        console.print(f"  [bright_yellow]{k}[/bright_yellow]  {icono}  [white]{tipo}[/white]  [dim]{desc}[/dim]")
    console.print()
    tipo_op = Prompt.ask("  [bright_yellow]Tipo[/bright_yellow]", choices=list(_TIPOS_MANIFESTACION.keys()), default="1")
    tipo, _, icono_tipo = _TIPOS_MANIFESTACION[tipo_op]

    # Intención
    console.print()
    console.print(f"  [dim]Escribe tu intención con claridad y en tiempo presente.[/dim]")
    intencion = Prompt.ask(f"  [bright_yellow]{icono_tipo} Intención[/bright_yellow]").strip()
    if not intencion:
        console.print("[yellow]  Intención vacía. Cancelado.[/yellow]")
        return

    # Entidad testigo
    console.print()
    separador("ENTIDAD TESTIGO", "dim")
    console.print()
    deidades_opciones = {
        "1": "isis", "2": "afrodita", "3": "lilith", "4": "artemisa", "5": "tutu"
    }
    for k, nombre in deidades_opciones.items():
        color = COLORES[nombre]
        icono = ICONOS[nombre]
        elem = ELEMENTOS.get(nombre, "")
        console.print(f"  [{color}]{k}[/{color}]  {icono}  [{color}]{nombre}[/{color}]  [dim]{elem}[/dim]")
    console.print()
    ent_op = Prompt.ask("  [bright_yellow]Testigo[/bright_yellow]", choices=list(deidades_opciones.keys()), default="1")
    entidad = deidades_opciones[ent_op]

    # Confirmar
    console.print()
    console.print(Panel(
        f"[bright_yellow]{icono_tipo} {tipo.upper()}[/bright_yellow]\n\n"
        f"[white]«{intencion}»[/white]\n\n"
        f"[dim]testigo: {ICONOS[entidad]} {entidad}[/dim]",
        border_style="bright_yellow",
        padding=(1, 3),
    ))
    console.print()
    if not Confirm.ask("  [bright_yellow]¿Declarar esta manifestación?[/bright_yellow]", default=True):
        console.print("[dim]  Cancelado.[/dim]")
        return

    # Guardar
    m_id = ManifestacionRepo.crear(
        proyecto_hash=_proyecto_activo.hash,
        tipo=tipo,
        intencion=intencion,
        entidad_testigo=entidad,
    )

    # Registrar como evento en el bosque
    try:
        from base_datos.esferas import EventoRepo as EvR
        EvR.registrar(
            tipo_evento="manifestacion",
            tipo_esfera="intencion",
            clave_esfera=f"manifestacion_{m_id}",
            detalle={"tipo": tipo, "intencion": intencion[:80]},
            proyecto_hash=_proyecto_activo.hash,
            entidad=entidad,
        )
    except Exception:
        pass

    # La entidad testifica (IA)
    esferas_bosque = []
    try:
        esferas_bosque = [dict(e) for e in EsferaRepo.listar_activas()]
    except Exception:
        pass

    with pensar(f"{entidad} es testigo..."):
        time.sleep(0.2)
        try:
            respuesta = _invocador.testificar_manifestacion(
                entidad=entidad,
                tipo=tipo,
                intencion=intencion,
                proyecto=_proyecto_activo,
                esferas_bosque=esferas_bosque,
            )
            texto_testigo = respuesta.texto
            es_offline = respuesta.es_offline
        except Exception as e:
            texto_testigo = f"[error: {e}]"
            es_offline = False

    console.print()
    color_e = COLORES[entidad]
    console.print(Panel(
        f"[{color_e}]{texto_testigo}[/{color_e}]",
        title=f"[{color_e}]{ICONOS[entidad]} {entidad} — testigo[/{color_e}]",
        border_style=color_e,
        padding=(1, 2),
    ))
    if es_offline:
        console.print("  [dim](offline)[/dim]")

    console.print()
    console.print(f"[bright_yellow]  ✓ Manifestación #{m_id} declarada.[/bright_yellow]  "
                  f"[dim]Check-ins en T+7, T+30, T+90 días.[/dim]")
    try:
        from base_datos.ayni import AyniRepo as _AyniRepo
        _AyniRepo.registrar_deuda(
            _proyecto_activo.hash, "manifestacion",
            f"{tipo}: {intencion[:60]}", origen_id=m_id,
        )
    except Exception:
        pass


def _ver_manifestaciones():
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    todas = ManifestacionRepo.listar(_proyecto_activo.hash)
    if not todas:
        console.print()
        console.print("  [dim]No hay manifestaciones declaradas aún.[/dim]")
        return

    console.print()
    separador("MANIFESTACIONES", "bright_yellow")
    console.print()

    _ESTADO_COLOR = {
        "activa":      "bright_yellow",
        "cumplida":    "green",
        "abandonada":  "dim",
        "transmutada": "cyan",
    }

    for m in todas:
        color_estado = _ESTADO_COLOR.get(m["estado"], "white")
        color_e = COLORES.get(m["entidad_testigo"], "white")
        icono_e = ICONOS.get(m["entidad_testigo"], "◉")
        checkins = CheckinRepo.por_manifestacion(m["id"])
        hechos = {c["t_dias"] for c in checkins}
        prog = "/".join(
            f"[green]T+{d}✓[/green]" if d in hechos else f"[dim]T+{d}[/dim]"
            for d in (7, 30, 90)
        )
        console.print(
            f"  [dim]#{m['id']}[/dim]  "
            f"[white]{m['tipo']:12}[/white]  "
            f"[{color_estado}]{m['estado']:10}[/{color_estado}]  "
            f"{icono_e} [{color_e}]{m['entidad_testigo']:8}[/{color_e}]"
        )
        console.print(f"    [dim italic]«{m['intencion'][:70]}»[/dim italic]")
        console.print(f"    {prog}  [dim]{m['created_at'][:10]}[/dim]")
        console.print()


def _checkin_manifestacion():
    global _proyecto_activo

    if not _proyecto_activo:
        _seleccionar_o_crear_proyecto()
        if not _proyecto_activo:
            return

    # Primero mostrar pendientes urgentes, luego dejar elegir cualquiera
    pendientes = ManifestacionRepo.checkins_pendientes(_proyecto_activo.hash)
    activas = ManifestacionRepo.listar(_proyecto_activo.hash, estado="activa")

    if not activas:
        console.print()
        console.print("  [dim]No hay manifestaciones activas.[/dim]")
        return

    console.print()
    separador("CHECK-IN", "bright_yellow")
    console.print()

    if pendientes:
        console.print(f"  [yellow]⚡ {len(pendientes)} check-in(s) pendiente(s) por fecha:[/yellow]")
        for p in pendientes:
            console.print(
                f"    [dim]#{p['id']}[/dim]  [white]{p['tipo']}[/white]  "
                f"T+{p['_t_dias']}  [dim italic]«{p['intencion'][:50]}»[/dim italic]"
            )
        console.print()

    console.print("  [dim]Manifestaciones activas:[/dim]")
    for m in activas:
        hechos = {c["t_dias"] for c in CheckinRepo.por_manifestacion(m["id"])}
        prox = next((d for d in (7, 30, 90) if d not in hechos), None)
        prox_str = f"T+{prox}" if prox else "completo"
        console.print(
            f"    [bright_yellow]#{m['id']}[/bright_yellow]  "
            f"[white]{m['tipo']:12}[/white]  "
            f"[dim]próximo: {prox_str}  «{m['intencion'][:45]}»[/dim]"
        )

    console.print()
    m_id_str = Prompt.ask("  [bright_yellow]ID de manifestación[/bright_yellow]").strip()
    if not m_id_str.isdigit():
        console.print("[yellow]  ID inválido.[/yellow]")
        return

    m = ManifestacionRepo.por_id(int(m_id_str))
    if not m or m["proyecto_hash"] != _proyecto_activo.hash:
        console.print("[yellow]  Manifestación no encontrada.[/yellow]")
        return

    # Determinar qué check-in toca
    hechos = {c["t_dias"] for c in CheckinRepo.por_manifestacion(m["id"])}
    disponibles = [d for d in (7, 30, 90) if d not in hechos]
    if not disponibles:
        console.print("  [green]  Esta manifestación ya tiene todos sus check-ins registrados.[/green]")
        # Igual permitir cambiar estado
    else:
        console.print()
        console.print(f"  [dim]Check-ins disponibles:[/dim]")
        for i, d in enumerate(disponibles, 1):
            console.print(f"    [bright_yellow]{i}[/bright_yellow]  T+{d} días")
        op_t = Prompt.ask("  [bright_yellow]Check-in[/bright_yellow]",
                          choices=[str(i) for i in range(1, len(disponibles)+1)], default="1")
        t_dias = disponibles[int(op_t) - 1]

        console.print()
        console.print(f"  [dim italic]«{m['intencion']}»[/dim italic]")
        console.print()
        observacion = Prompt.ask(f"  [bright_yellow]¿Qué observas a T+{t_dias} días?[/bright_yellow]").strip()
        if not observacion:
            console.print("[yellow]  Observación vacía. Cancelado.[/yellow]")
            return

        console.print()
        for k, (_, desc, color) in _ESTADO_RESULTADO_OPTS.items():
            console.print(f"  [{color}]{k}[/{color}]  {desc}")
        er_op = Prompt.ask("  [bright_yellow]Estado[/bright_yellow]",
                           choices=list(_ESTADO_RESULTADO_OPTS.keys()), default="3")
        estado_resultado, _, _ = _ESTADO_RESULTADO_OPTS[er_op]

        CheckinRepo.registrar(m["id"], t_dias, observacion, estado_resultado)

        # Si el resultado es cumplida, cerrar la manifestación
        if estado_resultado == "cumplida":
            ManifestacionRepo.cambiar_estado(m["id"], "cumplida")
            console.print(f"\n  [green]✓ Manifestación #{m['id']} cerrada como cumplida.[/green]")
        else:
            console.print(f"\n  [bright_yellow]✓ Check-in T+{t_dias} registrado.[/bright_yellow]")

        # IA interpreta el check-in
        esferas_bosque = []
        try:
            esferas_bosque = [dict(e) for e in EsferaRepo.listar_activas()]
        except Exception:
            pass

        with pensar(f"{m['entidad_testigo']} lee tu check-in..."):
            time.sleep(0.2)
            try:
                respuesta = _invocador.interpretar_checkin(
                    entidad=m["entidad_testigo"],
                    tipo=m["tipo"],
                    intencion=m["intencion"],
                    t_dias=t_dias,
                    observacion=observacion,
                    proyecto=_proyecto_activo,
                    esferas_bosque=esferas_bosque,
                )
                texto_interp = respuesta.texto
            except Exception as e:
                texto_interp = f"[error: {e}]"

        console.print()
        entidad = m["entidad_testigo"]
        color_e = COLORES.get(entidad, "white")
        console.print(Panel(
            f"[{color_e}]{texto_interp}[/{color_e}]",
            title=f"[{color_e}]{ICONOS.get(entidad, '◉')} {entidad}[/{color_e}]",
            border_style=color_e,
            padding=(0, 2),
        ))


def menu_manifestar():
    global _proyecto_activo

    if not _proyecto_activo:
        limpiar()
        cabecera()
        _seleccionar_o_crear_proyecto()

    while True:
        limpiar()
        cabecera()
        separador("⚡ MANIFESTACIÓN", "bright_yellow")
        console.print()
        console.print("[dim]Declara intenciones en el mundo con una entidad como testigo.[/dim]")
        console.print("[dim]Check-ins a T+7 / T+30 / T+90 días para evaluar el movimiento.[/dim]")
        console.print()

        # Resumen rápido
        if _proyecto_activo:
            activas = ManifestacionRepo.listar(_proyecto_activo.hash, estado="activa")
            pendientes = ManifestacionRepo.checkins_pendientes(_proyecto_activo.hash)
            console.print(f"  [dim]activas: {len(activas)}[/dim]", end="")
            if pendientes:
                console.print(f"  [yellow]  ⚡ {len(pendientes)} check-in(s) pendiente(s)[/yellow]")
            else:
                console.print()
            console.print()

        separador()
        console.print()
        console.print("  [bright_yellow]1[/bright_yellow]  Declarar nueva manifestación")
        console.print("  [bright_yellow]2[/bright_yellow]  Ver manifestaciones")
        console.print("  [bright_yellow]3[/bright_yellow]  Hacer check-in")
        console.print()
        console.print("  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask("  [bright_yellow]>[/bright_yellow]", default="0")

        if op == "1":
            limpiar()
            cabecera()
            _declarar_manifestacion()
            esperar()
        elif op == "2":
            limpiar()
            cabecera()
            _ver_manifestaciones()
            esperar()
        elif op == "3":
            limpiar()
            cabecera()
            _checkin_manifestacion()
            esperar()
        elif op == "0":
            break


# ═══════════════════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def menu_altar_trabajo():
    """Sub-menú del Altar: conversación, manifestar, sigilo, limpia, ayni."""
    while True:
        limpiar()
        cabecera()
        separador("🕯  ALTAR — lugar de trabajo", "bright_yellow")
        console.print()
        if _proyecto_activo:
            console.print(f"  [dim]proyecto: {_proyecto_activo.codigo}[/dim]")
            console.print()

        console.print(f"  [bright_yellow]1[/bright_yellow]  🔥  ALTAR         [dim]deidades · canal · conversación[/dim]")
        console.print(f"  [bright_yellow]2[/bright_yellow]  ⚡  MANIFESTAR    [dim]petición · decreto · transmutación[/dim]")
        console.print(f"  [bright_yellow]3[/bright_yellow]  {_ICONO_SIGILO}  SIGILO       [dim]Carroll · gnosis · olvido · quema[/dim]")
        console.print(f"  [bright_yellow]4[/bright_yellow]  {_ICONO_LIMPIA}  LIMPIA       [dim]saminchakuy · curanderismo[/dim]")
        console.print(f"  [bright_yellow]5[/bright_yellow]  {_ICONO_AYNI}  AYNI         [dim]reciprocidad · ofrendas · balance[/dim]")
        console.print()
        console.print(f"  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask("  [white]>[/white]", default="0")

        if op == "1":
            menu_altar()
        elif op == "2":
            menu_manifestar()
        elif op == "3":
            menu_sigilo_operativo()
        elif op == "4":
            menu_limpia()
        elif op == "5":
            menu_ayni()
        elif op == "0":
            return


def menu_bosque_proyecto():
    """Sub-menú del Bosque y Proyecto."""
    while True:
        limpiar()
        cabecera()
        separador("🌲  BOSQUE Y PROYECTO", "green")
        console.print()

        console.print(f"  [green]1[/green]  🌲  BOSQUE        [dim]ecosistema · seres · voz del bosque[/dim]")
        console.print(f"  [dim]2     PROYECTO     gestionar código de acceso[/dim]")
        console.print()
        console.print(f"  [dim]0  Volver[/dim]")
        console.print()

        op = Prompt.ask("  [white]>[/white]", default="0")

        if op == "1":
            menu_bosque()
        elif op == "2":
            limpiar()
            cabecera()
            _seleccionar_o_crear_proyecto()
            esperar()
        elif op == "0":
            return


def menu_principal():
    while True:
        limpiar()
        cabecera()

        esferas = EsferaRepo.listar_activas()
        n_esferas = len(esferas)

        tabla_estado = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        tabla_estado.add_column(style="dim")
        tabla_estado.add_column(style="white")
        tabla_estado.add_row("esferas vivas", str(n_esferas))
        tabla_estado.add_row("entradas biblioteca", str(len(EntradaRepo.listar(limite=100))))
        if _proyecto_activo:
            tabla_estado.add_row("proyecto", _proyecto_activo.codigo)
        console.print(tabla_estado)
        console.print()

        separador()
        console.print()
        console.print(f"  [white]1[/white]  📚  LIBRERÍA      [dim]conocimiento · minerales · árboles · seres[/dim]")
        console.print(f"  [bright_yellow]2[/bright_yellow]  🕯  ALTAR         [dim]conversación · manifestar · sigilo · limpia · ayni[/dim]")
        console.print(f"  [green]3[/green]  🌲  BOSQUE        [dim]ecosistema · seres · proyecto[/dim]")
        console.print()
        console.print(f"  [dim]0  Salir[/dim]")
        console.print()

        op = Prompt.ask("  [white]>[/white]", default="0")

        if op == "1":
            menu_biblioteca()
        elif op == "2":
            menu_altar_trabajo()
        elif op == "3":
            menu_bosque_proyecto()
        elif op == "0":
            console.print()
            console.print("[dim]  cerrando...[/dim]")
            console.print()
            sys.exit(0)


# ═══════════════════════════════════════════════════════════════════════════
#  ARRANQUE
# ═══════════════════════════════════════════════════════════════════════════

def bienvenida():
    """Diálogo de bienvenida con selección de proyecto al inicio."""
    global _proyecto_activo

    limpiar()
    console.print()
    console.print(Panel(
        "[bold bright_white]K A L I N A B I S[/bold bright_white]\n\n"
        "[dim]sistema ritual · caos · bosque colectivo[/dim]",
        border_style="dim yellow",
        padding=(1, 6),
        expand=False,
    ))
    console.print()
    time.sleep(0.4)

    console.print("  [dim]El sistema despierta.[/dim]")
    console.print()

    opcion = Prompt.ask(
        "  [white]¿Tienes un código de proyecto?[/white]",
        choices=["s", "n", "omitir"],
        default="n",
    )

    if opcion == "s":
        limpiar()
        cabecera()
        codigo = Prompt.ask("  [white]Ingresa tu código[/white]").strip().lower()
        p = Proyecto(codigo=codigo)
        if not ProyectoRepo.existe(p.hash):
            console.print()
            console.print("[yellow]  Código no encontrado.[/yellow]")
            time.sleep(0.8)
            if Confirm.ask("  ¿Crear proyecto nuevo con este código?", default=False):
                _proyecto_activo = p
                metadatos = json.dumps({"nombre": "cli", "creado_con": "kalinabis_cli"})
                cifrado = Cifrador.cifrar(metadatos, codigo)
                ProyectoRepo.crear(p.hash, cifrado)
                console.print(f"[green]  ✓ Proyecto creado: {codigo}[/green]")
            else:
                _crear_proyecto()
        else:
            ProyectoRepo.actualizar_actividad(p.hash)
            _proyecto_activo = p
            console.print(f"[green]  ✓ Proyecto cargado: {codigo}[/green]")
        time.sleep(0.6)

    elif opcion == "n":
        limpiar()
        cabecera()
        console.print("  [dim]Se creará un proyecto nuevo para ti.[/dim]")
        console.print()
        _crear_proyecto()
        time.sleep(1.2)

    # "omitir" → continúa sin proyecto activo


def main():
    inicializar_db()

    # Sembrar canon silenciosamente si la biblioteca está vacía
    try:
        if not EntradaRepo.listar(limite=1):
            sembrar_canon()
    except Exception:
        pass

    bienvenida()
    menu_principal()


if __name__ == "__main__":
    main()
