# ═══════════════════════════════════════════════════════════════════════════
#  SERVIDOR — KALINABIS
#  Backend con Groq API + proyectos anónimos + esferas colectivas
#
#  USO:
#    1. Setear GROQ_API_KEY en el entorno
#    2. cd C:\grimorio
#    3. python servidor.py
#    4. Abre http://localhost:5000
# ═══════════════════════════════════════════════════════════════════════════

import os
import json
import time
from pathlib import Path
from collections import defaultdict
from threading import Lock

# Cargar variables de entorno desde .env.local
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env.local")

from flask import Flask, request, jsonify, send_from_directory, make_response, Response

from config import Config
from proyectos import GeneradorCodigos, Cifrador, Proyecto
from esferas import GestorEsferas
from base_datos.esferas import (
    EsferaRepo, RelacionRepo, EventoRepo, HumusRepo, OfrendaRepo, ConvergenciaRepo,
    UMBRAL_CONVERGENCIA, VENTANA_CONVERGENCIA_H,
    TIPOS_RELACION, _narrativa_evento,
)
from geografia import GestorGeografico
from presentacion_deidades import formatear_presentacion

BASE_DIR = Path(__file__).parent

app = Flask(__name__, static_folder=str(BASE_DIR))
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB max por request


# ═══════════════════════════════════════════════════════════════════════════
#  CORS — after_request para agregar headers a todas las respuestas
# ═══════════════════════════════════════════════════════════════════════════

import re as _re

# El front Next puede correr en cualquier puerto 3000-3009 en dev.
_ORIGEN_LOCAL = _re.compile(r"^http://(localhost|127\.0\.0\.1):\d+$")


@app.after_request
def _agregar_cors(response: Response) -> Response:
    """Refleja el origin de localhost para que el front Next (cualquier
    puerto de dev) pueda hacer fetch al backend. Usa X-Project-Code, no
    cookies, así que reflejar el origin es seguro aquí."""
    origen = request.headers.get("Origin", "")
    if origen and _ORIGEN_LOCAL.match(origen):
        response.headers["Access-Control-Allow-Origin"] = origen
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, X-Project-Code"
        )
        response.headers["Access-Control-Max-Age"] = "3600"
    return response


# ═══════════════════════════════════════════════════════════════════════════
#  SEGURIDAD: Rate limiting + validación
# ═══════════════════════════════════════════════════════════════════════════

_rate_limit_lock = Lock()
_rate_limit_data: dict[str, list[float]] = defaultdict(list)

# Config: (ventana_segundos, max_requests)
_RATE_LIMITS = {
    "/api/proyecto/nuevo":  (3600, 5),  # 5 por hora (anti-spam proyectos)
    "/api/consultar":       (60, 10),   # 10 por minuto
    "/api/tarot/leer":      (60, 5),    # 5 por minuto
    "/api/astral/calcular": (60, 3),    # cálculo pesado
    "/api/sigilo":          (60, 10),
    "/api/sigilo/":         (60, 15),
    "/api/mensajes/quemar": (60, 20),
    "/api/decisiones":      (60, 10),
    "/api/bosque/ciclo":    (300, 1),   # 1 cada 5 min (mantenimiento)
    "/api/geografia/eje":   (60, 5),
    "/api/iching/consulta":    (60, 5),
    "/api/geomancia/lectura":  (60, 5),
    "/api/servitors/crear":   (3600, 10),  # 10 servitors por hora
    "/api/servitors/invocar": (60, 8),
    "/api/discord/oraculo":   (60, 5),
    "/api/sync/nueva":        (3600, 20),
    "/api/sync/confirmar":    (60, 30),
    "/api/rayos/test":        (3600, 5),
    "/api/paradigm/iniciar":  (3600, 3),
    "/api/paradigm/checkin":  (60, 10),
    "default":              (60, 30),
}

# Límites de tamaño de input
_MAX_MESSAGE_LEN = 4000
_MAX_TITULO_LEN = 200
_MAX_CONTENIDO_LEN = 10000


def _check_rate_limit(key: str, ventana: int, max_req: int) -> tuple[bool, int]:
    """Retorna (permitido, segundos_hasta_reset)."""
    ahora = time.time()
    with _rate_limit_lock:
        timestamps = _rate_limit_data[key]
        # Limpiar timestamps viejos
        cutoff = ahora - ventana
        _rate_limit_data[key] = [t for t in timestamps if t > cutoff]
        if len(_rate_limit_data[key]) >= max_req:
            mas_viejo = _rate_limit_data[key][0]
            return False, int(ventana - (ahora - mas_viejo)) + 1
        _rate_limit_data[key].append(ahora)
        return True, 0


def _get_rate_limit_config(path: str) -> tuple[int, int]:
    for prefix, cfg in _RATE_LIMITS.items():
        if prefix != "default" and path.startswith(prefix):
            return cfg
    return _RATE_LIMITS["default"]


def _limitar_request():
    """Decorator: aplica rate limit por proyecto (o IP si no hay proyecto)."""
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def wrapper(*args, **kwargs):
            proyecto_header = request.headers.get("X-Project-Code", "")
            if proyecto_header:
                key = f"proyecto:{proyecto_header}:{request.path}"
            else:
                key = f"ip:{request.remote_addr}:{request.path}"
            ventana, max_req = _get_rate_limit_config(request.path)
            permitido, retry = _check_rate_limit(key, ventana, max_req)
            if not permitido:
                return jsonify({
                    "error": f"Demasiadas requests. Esperá {retry}s.",
                    "retry_after": retry,
                }), 429
            return f(*args, **kwargs)
        return wrapper
    return decorator


def _validar_string(s, nombre: str, max_len: int) -> str | None:
    """Valida que sea string y dentro del largo máximo. Retorna mensaje de error o None."""
    if not isinstance(s, str):
        return f"'{nombre}' debe ser texto"
    if len(s) > max_len:
        return f"'{nombre}' demasiado largo (max {max_len} chars)"
    return None

# ── Importar cosmología ────────────────────────────────────────────────────
import sys
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "src"))

from grimorio_base import (
    DEIDADES, ARBOLES_DEIDADES,
    INVOCACIONES_DIRECTAS, sembrar_memoria_artemisa,
    CHAKRAS, ARBOL_VIDA_SEPHIROTH, ARBOL_MUERTE_QLIPHOTH,
    CHAKRAS_ARTEMISA_SOCIAL, RUEDA_COLORES,
)
from base_datos.schema   import inicializar_db
from base_datos.proyecto import ProyectoRepo, ConversacionRepo
from base_datos.esferas  import EsferaRepo
from base_datos.practicas import ServitorRepo, SyncRepo, ParadigmaRepo
from base_datos.usuario  import UsuarioRepo, ExpRepo, LogroRepo
from base_datos.grimorio import GrimorioRepo, SigiloRepo
from base_datos.legacy import (
    DecisionRepo, GrimorioLegadoRepo, SigiloLegadoRepo,
    CartaNatalRepo, estadisticas,
)
from luna import luna_hoy
from tarot import ARCANOS, POSICIONES, carta_por_n
from astral import (
    CIUDADES, calcular_carta_natal, KERYKEION_OK
)

# ── Módulos de features (Fase 1/2/3): divinación + magia del caos ───────────
from runas import RUNAS, tirada as runas_tirada, posiciones_3, posiciones_9, SYSTEM_VOLVA
from gnosis import METODOS_GNOSIS, recomendar_metodo, guia_texto, SYSTEM_VOID_WALKER
from iching import consulta as iching_consulta, SYSTEM_YIJING, TRIGRAMAS
from geomancia import lectura as geo_lectura, SYSTEM_GEOMANTE, FIGURAS as GEO_FIGURAS, CASAS as GEO_CASAS
from servitors import (
    calcular_intensidad, calcular_estado, enriquecer,
    nueva_intensidad_feed, SYSTEM_SERVITOR, DEIDADES_VALIDAS,
    render_servitor, sistema_descripcion_estado,
)
from discordia import oraculo as discord_oraculo, render_oraculo, SYSTEM_ERIS
from sync import (
    enriquecer_sync, colectiva_resumen, render_sync,
    CATEGORIAS as SYNC_CATEGORIAS,
)
from rayos import (
    calcular_rayo, perfil_rayo, distribucion as rayos_distribucion,
    render_rayo, PREGUNTAS_TEST, OCTAGRAM, SYSTEM_ORACULO_RAYO,
)
from paradigms import (
    enriquecer_paradigma, render_paradigma, calcular_progreso,
    PARADIGMAS, SYSTEM_PSICONAUTA, DURACION_DIAS as PARADIGM_DIAS,
)

# Módulo de invocación IA (encapsula el proveedor tras una interface).
from invocacion import invocador
# Identidad de proyecto encapsulada (header, cifrado, proyecto-vs-legacy).
from proyecto_contexto import ContextoProyecto

from base_datos.biblioteca import EntradaRepo, FuenteRepo, ContribucionRepo, ResonanciaRepo
from biblioteca import (
    sembrar_canon, obtener_entrada_completa,
    validar_nueva_entrada, validar_fuente,
    validar_resonancia, validar_contribucion,
    _hash as _bib_hash, _slugify,
)


def _ia(system, messages, **kw) -> str:
    """Puente a la IA para endpoints de features: devuelve el texto crudo.

    Reemplaza el antiguo `groq_client.chat(...)`. El adapter concreto está
    detrás de `invocador` (intercambiable: Groq / offline / test)."""
    return invocador.cliente_ia.chat(system, messages, **kw).texto

# ── Inicializar ────────────────────────────────────────────────────────────
inicializar_db()
sembrado = sembrar_memoria_artemisa()
if sembrado:
    print("  · Memoria de Artemisa sembrada")
n_canon = sembrar_canon()
if n_canon:
    print(f"  · Biblioteca: {n_canon} entradas canónicas sembradas")


def _sembrar_proyecto_demo() -> None:
    """Crea el proyecto 'demo' si no existe (usado por el frontend de Fase 3)."""
    demo = Proyecto(codigo="demo")
    if not ProyectoRepo.existe(demo.hash):
        metadatos = json.dumps({"nombre": "Demo Kalinabis", "creado_con": "seed"})
        cifrado = Cifrador.cifrar(metadatos, "demo")
        ProyectoRepo.crear(demo.hash, cifrado)
        print("  · Proyecto 'demo' sembrado (Fase 3 frontend)")


_sembrar_proyecto_demo()

errores_config = Config.verificar()
for err in errores_config:
    print(f"  [!] {err}")


# ═══════════════════════════════════════════════════════════════════════════
#  HELPER — PROYECTO DESDE HEADER
# ═══════════════════════════════════════════════════════════════════════════

def _contexto() -> ContextoProyecto:
    return ContextoProyecto.desde_headers(request.headers)


def _proyecto_requerido(ctx: ContextoProyecto):
    err = ctx.requerir()
    if err:
        datos, status = err
        return jsonify(datos), status
    return None


# ═══════════════════════════════════════════════════════════════════════════
#  RUTAS HTML
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/")
@app.route("/terminal")
def index():
    return send_from_directory(str(BASE_DIR / "front_terminal"), "index.html")


@app.route("/clasico")
def clasico():
    return send_from_directory(str(BASE_DIR), "grimorio.html")


# ═══════════════════════════════════════════════════════════════════════════
#  API — PROYECTOS
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/proyecto/nuevo", methods=["POST"])
@_limitar_request()
def proyecto_nuevo():
    codigo = GeneradorCodigos.generar()
    proyecto = Proyecto(codigo=codigo)

    if ProyectoRepo.existe(proyecto.hash):
        # Colisión extremadamente rara
        return proyecto_nuevo()

    d = request.json or {}
    if not isinstance(d, dict):
        d = {}
    nombre = d.get("nombre", "Proyecto sin nombre")
    if e := _validar_string(nombre, "nombre", 100):
        return jsonify({"error": e}), 400
    metadatos = json.dumps({"nombre": nombre, "creado_con": "kalinabis"})
    cifrado = Cifrador.cifrar(metadatos, codigo)
    ProyectoRepo.crear(proyecto.hash, cifrado)

    return jsonify({
        "ok": True,
        "codigo": codigo,
        "hash": proyecto.hash[:12],
        "aviso": "Guardá este código. Es tu única llave de acceso. "
                 "El servidor no lo guarda."
    })


@app.route("/api/proyecto/verificar", methods=["POST"])
def proyecto_verificar():
    ctx = _contexto()
    if not ctx.activo:
        return jsonify({"existe": False})

    cifrado = ProyectoRepo.obtener_metadatos(ctx.hash)
    if not cifrado:
        return jsonify({"existe": False})

    descifrado = ctx.descifrar(cifrado)
    if not descifrado:
        return jsonify({"existe": False, "error": "código incorrecto"})

    metadatos = json.loads(descifrado)
    return jsonify({
        "existe": True,
        "hash": ctx.hash[:12],
        "metadatos": metadatos,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  API — INVOCACIÓN
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/consultar", methods=["POST", "OPTIONS"])
@_limitar_request()
def consultar():
    # Manejar OPTIONS para preflight CORS
    if request.method == "OPTIONS":
        return "", 204

    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err
    proyecto = ctx.proyecto

    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "JSON inválido"}), 400
    mensaje = data.get("mensaje", "").strip()
    entidad_forzada = data.get("entidad")
    ubicacion = data.get("ubicacion")
    concepto = data.get("concepto")

    if not mensaje:
        return jsonify({"error": "mensaje vacío"}), 400

    err = _validar_string(mensaje, "mensaje", _MAX_MESSAGE_LEN)
    if err:
        return jsonify({"error": err}), 400
    if ubicacion and (e := _validar_string(ubicacion, "ubicacion", 200)):
        return jsonify({"error": e}), 400
    if concepto and (e := _validar_string(concepto, "concepto", 200)):
        return jsonify({"error": e}), 400

    # Procesar comandos (/, /manifestar, /ayuda, /generar)
    if mensaje.startswith("/"):
        return _procesar_comando(mensaje, proyecto)

    entidad = entidad_forzada
    modo = "directo"

    if not entidad:
        msg_lower = mensaje.lower()
        for nombre, palabras in INVOCACIONES_DIRECTAS.items():
            if any(p in msg_lower for p in palabras):
                entidad = nombre
                modo = "directo"
                break

    if not entidad:
        entidad, estado_r, razon = _tutu_decide(mensaje)
        modo = "tutu"
        # Fallback a tutu si decidir_entidad devuelve algo inválido
        if entidad not in DEIDADES and entidad != "tutu":
            entidad = "tutu"
            estado_r = "alma"
    else:
        razon = "invocación directa del practicante"
        estado_r = "cuerpo" if entidad != "tutu" else "alma"

    if entidad == "tutu":
        respuesta = _invocar_tutu(mensaje, proyecto)
        estado_r = "alma"
    else:
        respuesta = _invocar_deidad(entidad, mensaje, proyecto)
        estado_r = "cuerpo"

    DecisionRepo.guardar(mensaje, entidad, estado_r, modo, razon)

    esferas_activadas = GestorEsferas.marcar_por_invocacion(
        entidad=entidad,
        ubicacion=ubicacion,
        concepto=concepto,
        proyecto_hash=proyecto.hash,
    )

    # Incluir presentación visual de la deidad
    presentacion = formatear_presentacion(entidad, estado_r) if entidad != "tutu" else ""

    return jsonify({
        "entidad": entidad,
        "estado": estado_r,
        "modo": modo,
        "razon": razon,
        "respuesta": respuesta,
        "presentacion": presentacion,
        "esferas_activadas": esferas_activadas,
        "eje_del_mundo": GestorGeografico.eje_del_mundo_para(ubicacion),
    })


def _tutu_decide(mensaje: str):
    return invocador.decidir_entidad(mensaje)


def _contexto_vivo(
    nombre_deidad: str,
    proyecto_hash: str | None = None,
) -> tuple[list[dict], list[dict]]:
    """Obtiene el estado del bosque y fragmentos de biblioteca para una deidad.

    Si proyecto_hash está presente, enriquece las esferas emergentes con las
    ofrendas de las esferas que este mago visitó recientemente.
    """
    from invocacion.contexto import ContextoManager
    try:
        esferas = GestorEsferas.listar_activas(amplitud_min=1.0)
        emergentes = sorted(esferas, key=lambda x: -x.get("amplitud_actual", 0))[:5]
    except Exception:
        emergentes = []

    # Enriquecer con ofrendas de las esferas visitadas por este mago
    if proyecto_hash and emergentes:
        try:
            visitadas = OfrendaRepo.esferas_visitadas_por_proyecto(
                proyecto_hash, limite=3
            )
            visitadas_idx = {
                (v["tipo_esfera"], v["clave_esfera"]) for v in visitadas
            }
            for e in emergentes:
                if (e["tipo"], e["clave_unica"]) in visitadas_idx:
                    ofrendas = OfrendaRepo.listar(e["tipo"], e["clave_unica"], limite=3)
                    e["ofrendas_recientes"] = ofrendas
                    e["visitada_por_mago"] = True
        except Exception:
            pass

    try:
        from base_datos.biblioteca import EntradaRepo as _BibRepo
        dominios = ContextoManager.dominios_deidad(nombre_deidad)
        entradas = []
        for dom in dominios[:2]:
            entradas += _BibRepo.listar(dominio=dom, limite=2)
        entradas = sorted(entradas, key=lambda x: -x.get("resonancia", 0))[:2]
    except Exception:
        entradas = []
    return emergentes, entradas


def _invocar_deidad(nombre: str, mensaje: str, proyecto: Proyecto) -> str:
    if nombre not in DEIDADES:
        return f"Entidad desconocida: {nombre}"
    esferas, entradas = _contexto_vivo(nombre, proyecto_hash=proyecto.hash)
    return invocador.invocar_deidad(
        nombre, mensaje, proyecto,
        esferas_bosque=esferas or None,
        entradas_biblioteca=entradas or None,
    ).texto


def _invocar_tutu(mensaje: str, proyecto: Proyecto) -> str:
    esferas, _ = _contexto_vivo("tutu", proyecto_hash=proyecto.hash)
    return invocador.invocar_tutu(mensaje, proyecto,
                                   esferas_bosque=esferas or None).texto


def _procesar_comando(mensaje: str, proyecto: Proyecto) -> tuple[dict, int]:
    """Procesa comandos que comienzan con /."""
    partes = mensaje.split(maxsplit=1)
    cmd = partes[0].lower()
    args = partes[1] if len(partes) > 1 else ""

    # /ayuda — muestra comandos disponibles
    if cmd == "/ayuda" or cmd == "/help":
        respuesta = (
            "Comandos disponibles:\n"
            "/manifestar <diosa> — Manifiesta una diosa en el altar\n"
            "  Ej: /manifestar lilith, /manifestar isis\n"
            "/generar <diosa> — Regenera el sprite de una diosa\n"
            "  Ej: /generar lilith\n"
            "/ayuda — Muestra esta lista\n"
            "\nDiosas disponibles: lilith, isis, afrodita, artemisa\n"
            "O habla con Tutu normalmente — él decide qué diosa manifestar."
        )
        return jsonify({
            "entidad": "tutu",
            "respuesta": respuesta,
            "estado": "alma",
            "modo": "comando",
            "razon": "comando /ayuda"
        }), 200

    # /manifestar <diosa> — manifiesta una diosa específica
    elif cmd == "/manifestar":
        if not args:
            return jsonify({
                "error": "Uso: /manifestar <diosa>",
                "ejemplo": "/manifestar lilith"
            }), 400

        diosa = args.lower().strip()
        if diosa not in DEIDADES:
            return jsonify({
                "error": f"Diosa desconocida: {diosa}",
                "disponibles": list(DEIDADES.keys())
            }), 400

        # Obtener saludo inicial de la diosa
        saludo = DEIDADES[diosa].get("saludo", "Bienvenido a mi altar.")
        return jsonify({
            "entidad": diosa,
            "respuesta": saludo,
            "estado": "cuerpo",
            "modo": "manifestacion",
            "razon": f"comando /manifestar {diosa}"
        }), 200

    # /generar <diosa> — Regenera sprite (requeriría script local)
    elif cmd == "/generar":
        if not args:
            return jsonify({
                "error": "Uso: /generar <diosa>",
                "ejemplo": "/generar lilith"
            }), 400

        diosa = args.lower().strip()
        if diosa not in DEIDADES:
            return jsonify({
                "error": f"Diosa desconocida: {diosa}",
                "disponibles": list(DEIDADES.keys())
            }), 400

        # Llamar al script local (esto se ejecutaría en background idealmente)
        respuesta = (
            f"Regenerando sprite de {diosa.upper()}...\n"
            f"Usa: python tools/gen_sprite_detailed.py --diosa {diosa}\n"
            f"O con HF API: python tools/gen_sprite_hf.py --diosa {diosa}"
        )
        return jsonify({
            "entidad": "tutu",
            "respuesta": respuesta,
            "estado": "alma",
            "modo": "comando",
            "razon": f"comando /generar {diosa}"
        }), 200

    # Comando desconocido
    else:
        return jsonify({
            "error": f"Comando desconocido: {cmd}",
            "hint": "Escribe /ayuda para ver los comandos disponibles"
        }), 400


# ═══════════════════════════════════════════════════════════════════════════
#  API — ESFERAS
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/esferas", methods=["GET"])
def get_esferas():
    tipo = request.args.get("tipo")
    esferas = GestorEsferas.listar_activas(tipo=tipo)
    return jsonify({
        "esferas": esferas,
        "total": len(esferas),
    })


@app.route("/api/esferas", methods=["POST"])
def post_esferas():
    ctx = _contexto()
    d = request.json
    tipo = d.get("tipo", "").strip()
    clave = d.get("clave", "").strip()
    metadata = d.get("metadata", {})

    if not tipo or not clave:
        return jsonify({"error": "tipo y clave son requeridos"}), 400

    try:
        resultado = GestorEsferas.marcar(
            tipo=tipo,
            clave_unica=clave,
            metadata=metadata,
            proyecto_hash=ctx.hash,
        )
        return jsonify({"ok": True, "esfera": resultado})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ═══════════════════════════════════════════════════════════════════════════
#  API — BOSQUE (mapa vivo + salud)
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/bosque/mapa", methods=["GET"])
def get_bosque_mapa():
    mapa = GestorEsferas.obtener_mapa()
    return jsonify(mapa)


@app.route("/api/bosque/voz", methods=["GET"])
def get_bosque_voz():
    """La voz del bosque — lectura IA del estado colectivo actual.

    No es una deidad. No responde preguntas. Es el bosque observándose a sí mismo.
    Puede recibir ?modo=breve|profundo para ajustar la extensión.
    """
    # Reunir el estado completo del bosque
    try:
        esferas = GestorEsferas.listar_activas(amplitud_min=0.1)
    except Exception:
        esferas = []

    try:
        eventos = EventoRepo.listar(limite=20)
        for ev in eventos:
            ev["narrativa"] = _narrativa_evento(ev)
    except Exception:
        eventos = []

    try:
        humus = HumusRepo.listar(limite=15)
    except Exception:
        humus = []

    try:
        relaciones = RelacionRepo.listar_todas(fuerza_min=0.5)
    except Exception:
        relaciones = []

    try:
        ConvergenciaRepo.expirar_antiguas()
        convergencias = ConvergenciaRepo.listar_activas(limite=10)
    except Exception:
        convergencias = []

    if not esferas and not eventos and not humus:
        return jsonify({
            "voz": "El bosque está en silencio. Todavía no hay energía colectiva suficiente para leer.",
            "estado": {"esferas": 0, "eventos": 0, "humus": 0},
        })

    try:
        respuesta = invocador.voz_bosque(
            esferas=esferas,
            eventos=eventos,
            humus=humus,
            relaciones=relaciones,
            convergencias=convergencias,
        )
        voz = respuesta.texto
    except Exception as exc:
        return jsonify({"error": f"No se pudo invocar la voz del bosque: {exc}"}), 500

    return jsonify({
        "voz": voz,
        "estado": {
            "esferas_vivas": len(esferas),
            "eventos_recientes": len(eventos),
            "humus": len(humus),
            "relaciones_activas": len(relaciones),
            "emergentes": [
                {"tipo": e["tipo"], "clave": e["clave_unica"], "amplitud": e.get("amplitud_actual", 0)}
                for e in esferas if e.get("amplitud_actual", 0) >= 3.5
            ],
        },
    })


@app.route("/api/bosque/convergencias", methods=["GET"])
def get_bosque_convergencias():
    """Señales colectivas activas: pares de esferas que N proyectos independientes
    marcaron juntos dentro de la ventana de 24h sin coordinarse entre sí."""
    ConvergenciaRepo.expirar_antiguas()
    convergencias = ConvergenciaRepo.listar_activas(limite=30)

    enriquecidas = []
    for c in convergencias:
        # Leer amplitudes actuales de ambas esferas para dar contexto
        ea = EsferaRepo.obtener(c["tipo_a"], c["clave_a"])
        eb = EsferaRepo.obtener(c["tipo_b"], c["clave_b"])
        enriquecidas.append({
            **c,
            "esfera_a": {
                "amplitud": ea["amplitud"] if ea else None,
                "fase": ea["fase_decaimiento"] if ea else "disuelta",
            },
            "esfera_b": {
                "amplitud": eb["amplitud"] if eb else None,
                "fase": eb["fase_decaimiento"] if eb else "disuelta",
            },
            "narrativa": _narrativa_convergencia(c),
        })

    return jsonify({
        "convergencias": enriquecidas,
        "total": len(enriquecidas),
        "umbral": UMBRAL_CONVERGENCIA,
        "ventana_horas": VENTANA_CONVERGENCIA_H,
    })


def _narrativa_convergencia(c: dict) -> str:
    n = c["n_proyectos"]
    a = f"{c['tipo_a']}:{c['clave_a']}"
    b = f"{c['tipo_b']}:{c['clave_b']}"
    magos = "magos" if n != 1 else "mago"
    return (
        f"{n} {magos} independientes marcaron {a} y {b} "
        f"dentro de las mismas {VENTANA_CONVERGENCIA_H}h — "
        f"señal colectiva sin coordinación explícita."
    )


@app.route("/api/bosque/eventos", methods=["GET"])
def get_bosque_eventos():
    """Crónica del bosque — registro histórico de eventos significativos."""
    tipo_evento = request.args.get("tipo_evento")
    tipo_esfera = request.args.get("tipo_esfera")
    clave_esfera = request.args.get("clave_esfera")
    limite = min(int(request.args.get("limite", 30)), 100)
    offset = int(request.args.get("offset", 0))
    cronica = request.args.get("cronica", "false").lower() == "true"

    if cronica:
        eventos = EventoRepo.cronica(limite=limite)
    else:
        eventos = EventoRepo.listar(
            tipo_evento=tipo_evento,
            tipo_esfera=tipo_esfera,
            clave_esfera=clave_esfera,
            limite=limite,
            offset=offset,
        )
        for ev in eventos:
            ev["narrativa"] = _narrativa_evento(ev)

    return jsonify({
        "eventos": eventos,
        "total": len(eventos),
    })


@app.route("/api/bosque/esferas/<tipo>/<clave>/interior", methods=["GET"])
def get_esfera_interior(tipo: str, clave: str):
    """El interior de una esfera como espacio colectivo:
    datos de la esfera + ofrendas de todos los magos + relaciones + últimos eventos."""
    tipo = tipo.lower().strip()
    clave = clave.lower().strip()

    esfera = EsferaRepo.obtener(tipo, clave)
    if not esfera:
        return jsonify({"error": "Esfera no encontrada"}), 404

    from esferas import Esfera as _EsferaModel
    esfera_viva = _EsferaModel(
        tipo=esfera["tipo"], clave_unica=esfera["clave_unica"],
        metadata=esfera.get("metadata", {}),
        amplitud=esfera["amplitud"],
        fase_decaimiento=esfera["fase_decaimiento"],
        created_at=esfera.get("created_at", ""),
        updated_at=esfera.get("updated_at", ""),
    ).a_dict()

    ofrendas = OfrendaRepo.listar(tipo, clave, limite=30)
    relaciones = RelacionRepo.listar_de(tipo, clave)
    eventos = EventoRepo.listar(tipo_esfera=tipo, clave_esfera=clave, limite=10)
    for ev in eventos:
        ev["narrativa"] = _narrativa_evento(ev)

    # ¿Esta esfera nació sobre humus de una vida anterior?
    humus_anterior = HumusRepo.obtener(tipo, clave)

    return jsonify({
        "esfera": esfera_viva,
        "ofrendas": ofrendas,
        "ofrendas_total": OfrendaRepo.conteo(tipo, clave),
        "relaciones": relaciones,
        "eventos": eventos,
        "humus_anterior": humus_anterior,
    })


@app.route("/api/bosque/esferas/<tipo>/<clave>/entrar", methods=["POST"])
def post_esfera_entrar(tipo: str, clave: str):
    """Un mago entra a una esfera. Puede dejar una ofrenda.
    Entrar amplifica la esfera y opcionalmente carga su contexto en el altar."""
    ctx = _contexto()
    tipo = tipo.lower().strip()
    clave = clave.lower().strip()

    if tipo not in GestorEsferas.TIPOS_VALIDOS:
        return jsonify({"error": f"Tipo inválido: {tipo}"}), 400

    data = request.get_json(silent=True) or {}
    texto_ofrenda = (data.get("ofrenda") or "").strip()
    entidad_activa = (data.get("entidad") or "").strip() or None

    # Amplificar la esfera al entrar (presencia = energía)
    proyecto_hash = ctx.hash if ctx.activo else None
    try:
        esfera_actualizada = GestorEsferas.marcar(
            tipo, clave,
            metadata={"visitada_por": entidad_activa} if entidad_activa else None,
            proyecto_hash=proyecto_hash,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Registrar ofrenda si la hay
    ofrenda_guardada = None
    if texto_ofrenda and len(texto_ofrenda) <= 1000:
        ofrenda_guardada = OfrendaRepo.dejar(
            tipo, clave,
            texto=texto_ofrenda,
            proyecto_hash=proyecto_hash,
            entidad=entidad_activa,
        )

    # Contexto de la esfera para llevar al altar
    ofrendas_recientes = OfrendaRepo.listar(tipo, clave, limite=5)
    contexto_esfera = _contexto_esfera_para_altar(
        esfera_actualizada, ofrendas_recientes
    )

    return jsonify({
        "esfera": esfera_actualizada,
        "ofrenda": ofrenda_guardada,
        "contexto_altar": contexto_esfera,
        "ofrendas_recientes": ofrendas_recientes,
    })


def _contexto_esfera_para_altar(esfera: dict, ofrendas: list[dict]) -> str:
    """Genera el bloque de contexto que se inyecta en el altar
    cuando un mago viene de una esfera del bosque."""
    tipo = esfera["tipo"]
    clave = esfera["clave_unica"]
    amp = esfera.get("amplitud_actual", esfera.get("amplitud", 0))
    bloque = (
        f"\n\n═══ VIENES DEL BOSQUE ═══\n"
        f"El mago acaba de salir de la esfera colectiva {tipo}:{clave} "
        f"(amplitud {amp:.2f}).\n"
    )
    if ofrendas:
        bloque += "Lo que otros magos dejaron allí:\n"
        for o in ofrendas[:3]:
            ent = o.get("entidad") or "un mago anónimo"
            bloque += f'  · [{ent}]: "{o["texto"]}"\n'
    bloque += "═════════════════════════\n"
    return bloque


@app.route("/api/bosque/relaciones", methods=["GET"])
def get_bosque_relaciones():
    """Grafo de relaciones tipadas entre esferas de distintos tipos."""
    tipo = request.args.get("tipo")
    clave = request.args.get("clave")
    fuerza_min = float(request.args.get("fuerza_min", 0.5))

    if tipo and clave:
        relaciones = RelacionRepo.listar_de(tipo.lower(), clave.lower())
    else:
        relaciones = RelacionRepo.listar_todas(fuerza_min=fuerza_min)

    return jsonify({
        "relaciones": relaciones,
        "total": len(relaciones),
        "tipos_disponibles": sorted(TIPOS_RELACION),
    })


@app.route("/api/bosque/salud", methods=["GET"])
def get_bosque_salud():
    esferas = GestorEsferas.listar_activas()

    por_tipo: dict[str, list[dict]] = {}
    for e in esferas:
        t = e["tipo"]
        if t not in por_tipo:
            por_tipo[t] = []
        por_tipo[t].append(e)

    total_amp = sum(e["amplitud_actual"] for e in esferas)
    promedio_amp = total_amp / len(esferas) if esferas else 0

    en_letargo = sum(1 for e in esferas if e["fase_viva"] == "letargo")
    disolviendo = sum(1 for e in esferas if e["fase_viva"] == "disolviendo")
    activas = sum(1 for e in esferas if e["fase_viva"] == "activa")

    return jsonify({
        "total_esferas": len(esferas),
        "activas": activas,
        "en_letargo": en_letargo,
        "disolviendo": disolviendo,
        "promedio_amplitud": promedio_amp,
        "distribucion_por_tipo": {t: len(v) for t, v in por_tipo.items()},
        "esferas_mas_fuertes": sorted(
            [{"label": f"{e['tipo']}: {e['clave_unica']}",
              "amplitud": e["amplitud_actual"]}
             for e in esferas],
            key=lambda x: -x["amplitud"]
        )[:10],
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    })


@app.route("/api/bosque/ciclo", methods=["POST"])
def post_bosque_ciclo():
    """Ejecuta manualmente el ciclo de decaimiento."""
    resultado = GestorEsferas.ejecutar_ciclo_decaimiento()
    return jsonify(resultado)


@app.route("/api/bosque/estratos", methods=["GET"])
def get_bosque_estratos():
    """Los 4 estratos narrativos del bosque.

    Estrato 1 — emergentes  (amplitud >= 3.5): árboles que tocan el cielo
    Estrato 2 — dosel       (amplitud 2.0-3.5): maduros, plenos
    Estrato 3 — sotobosque  (amplitud < 2.0, vivas): jóvenes o en letargo
    Estrato 4 — humus       (disueltas): suelo fértil, con su causa de muerte
    """
    esferas = GestorEsferas.listar_activas()

    emergentes, dosel, sotobosque = [], [], []
    for e in esferas:
        a = e["amplitud_actual"]
        if a >= 3.5:
            emergentes.append(e)
        elif a >= 2.0:
            dosel.append(e)
        else:
            sotobosque.append(e)

    # Estrato humus: esferas muertas con su historia
    humus_raw = HumusRepo.listar(limite=30)
    humus = []
    for h in humus_raw:
        narrativa = _narrativa_humus(h)
        humus.append({**h, "narrativa": narrativa})

    # Atmósfera elemental
    elementales = [e for e in esferas if e["tipo"] == "elemental"]
    atm_por_elem: dict[str, float] = {}
    for e in elementales:
        c = e["clave_unica"]
        atm_por_elem[c] = atm_por_elem.get(c, 0) + e["amplitud_actual"]

    ELEM_DEIDAD = {"fuego": "isis", "agua": "lilith", "aire": "afrodita", "tierra": "artemisa"}
    elemento_dominante = max(atm_por_elem, key=atm_por_elem.get) if atm_por_elem else None
    atmosfera = {
        "elemento": elemento_dominante,
        "deidad": ELEM_DEIDAD.get(elemento_dominante, "") if elemento_dominante else "",
        "equilibrio": len(atm_por_elem) >= 3,
    } if atm_por_elem else {"elemento": None, "deidad": "", "equilibrio": False}

    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    return jsonify({
        "estratos": {
            "emergentes":  sorted(emergentes, key=lambda x: -x["amplitud_actual"])[:10],
            "dosel":       sorted(dosel,      key=lambda x: -x["amplitud_actual"])[:15],
            "sotobosque":  sorted(sotobosque, key=lambda x: -x["amplitud_actual"])[:20],
            "humus":       humus,
        },
        "conteos": {
            "emergentes":  len(emergentes),
            "dosel":       len(dosel),
            "sotobosque":  len(sotobosque),
            "humus":       len(humus),
        },
        "atmosfera": atmosfera,
        "luna":      luna_ctx,
    })


def _narrativa_humus(h: dict) -> str:
    tipo = h["tipo"]
    clave = h["clave_unica"]
    causa = h.get("causa", "desconocida")
    dias = h.get("dias_activa", 0)
    ofrendas = h.get("ofrendas_count", 0)
    absorbida_por = h.get("absorbida_por")

    base = f"{tipo}:{clave} vivió {dias:.0f} días"
    if ofrendas:
        base += f", recibió {ofrendas} {'ofrenda' if ofrendas == 1 else 'ofrendas'}"

    if causa == "absorbida" and absorbida_por:
        return f"{base} — fue absorbida por {absorbida_por}. Su energía vive allí."
    if causa == "decaimiento_natural":
        return f"{base} — se disolvió en silencio. Nadie vino al final."
    return f"{base} — su humus queda en el suelo."


@app.route("/api/bosque/marcar", methods=["POST"])
@_limitar_request()
def post_bosque_marcar():
    """Marcar una esfera bajo el Canelo — acto de resonancia deliberado."""
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    tipo   = (d.get("tipo") or "").strip().lower()
    clave  = (d.get("clave") or "").strip()[:200]

    TIPOS_VALIDOS = {"geo", "elemental", "tematica", "resonancia"}
    if tipo not in TIPOS_VALIDOS:
        return jsonify({"error": f"tipo inválido. Opciones: {', '.join(sorted(TIPOS_VALIDOS))}"}), 400
    if not clave:
        return jsonify({"error": "clave requerida"}), 400

    try:
        esfera = GestorEsferas.marcar(tipo, clave, {}, ctx.hash)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "esfera":  esfera,
        "mensaje": f"Marcado bajo el Canelo: {tipo}/{clave} · amplitud {esfera['amplitud_actual']:.2f}",
    })


# ═══════════════════════════════════════════════════════════════════════════
#  API — GEOGRAFÍA
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/geografia/ecorregiones", methods=["GET"])
def get_ecorregiones():
    return jsonify({
        "ecorregiones": GestorGeografico.listar_todas(),
        "total": len(GestorGeografico._ecorregiones),
    })


@app.route("/api/geografia/eje", methods=["POST"])
def get_eje_del_mundo():
    d = request.json
    ubicacion = d.get("ubicacion", "")
    return jsonify(GestorGeografico.eje_del_mundo_para(ubicacion))


# ═══════════════════════════════════════════════════════════════════════════
#  API — CARTA NATAL (por proyecto)
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/astral/calcular", methods=["POST"])
@_limitar_request()
def post_calcular_natal():
    ctx = _contexto()

    if not KERYKEION_OK:
        return jsonify({"error": "kerykeion no instalado"}), 500

    d = request.json
    if not isinstance(d, dict):
        return jsonify({"error": "JSON inválido"}), 400

    # Validación de rangos
    try:
        anio = int(d.get("anio", 0))
        mes = int(d.get("mes", 0))
        dia = int(d.get("dia", 0))
        hora = int(d.get("hora", 0))
        minuto = int(d.get("minuto", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "fecha/hora inválida"}), 400
    if not (1900 <= anio <= 2030 and 1 <= mes <= 12 and 1 <= dia <= 31 and 0 <= hora <= 23 and 0 <= minuto <= 59):
        return jsonify({"error": "fecha/hora fuera de rango"}), 400

    carta = calcular_carta_natal(
        d.get("nombre", "Consultante"),
        d.get("anio"), d.get("mes"), d.get("dia"),
        d.get("hora"), d.get("minuto"),
        d.get("lat"), d.get("lng"), d.get("tz"),
    )
    if "error" in carta:
        return jsonify(carta), 400

    if ctx.activo:
        cifrado = ctx.cifrar(json.dumps(carta))
        ProyectoRepo.guardar_carta_natal(
            ctx.hash, cifrado,
            nombre=d.get("nombre", "Consultante")
        )
    else:
        CartaNatalRepo.guardar(
            d.get("nombre", "Consultante"),
            int(d.get("anio")), int(d.get("mes")), int(d.get("dia")),
            int(d.get("hora")), int(d.get("minuto")),
            d.get("lugar", ""), float(d.get("lat")), float(d.get("lng")),
            d.get("tz"), json.dumps(carta),
        )

    return jsonify(carta)


@app.route("/api/astral/guardada", methods=["GET"])
def get_natal_guardada():
    ctx = _contexto()

    if ctx.activo:
        cifrado = ProyectoRepo.obtener_carta_natal(ctx.hash)
        if not cifrado:
            return jsonify({"existe": False})
        datos_str = ctx.descifrar(cifrado)
        if not datos_str:
            return jsonify({"existe": False})
        datos = json.loads(datos_str)
        return jsonify({
            "existe": True,
            "datos": datos,
            "cifrado": True,
        })
    else:
        carta = CartaNatalRepo.leer()
        if not carta:
            return jsonify({"existe": False})
        datos = {}
        if carta.get("datos"):
            try:
                datos = json.loads(carta["datos"])
            except Exception:
                pass
        return jsonify({
            "existe": True,
            "nombre": carta["nombre"],
            "lugar": carta["lugar"],
            "fecha": (f"{carta['dia']:02d}/{carta['mes']:02d}/"
                      f"{carta['anio']} {carta['hora']:02d}:"
                      f"{carta['minuto']:02d}"),
            "datos": datos,
            "cifrado": False,
        })


# ═══════════════════════════════════════════════════════════════════════════
#  API — TAROT
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/tarot/arcanos", methods=["GET"])
def get_arcanos():
    return jsonify({"arcanos": ARCANOS, "posiciones": POSICIONES})


@app.route("/api/tarot/leer/<entidad>", methods=["POST"])
@_limitar_request()
def tarot_leer(entidad):
    ctx = _contexto()
    entidad = entidad.lower()
    d = request.json
    if not isinstance(d, dict):
        return jsonify({"error": "JSON inválido"}), 400
    cartas = d.get("cartas", [])
    if not isinstance(cartas, list) or len(cartas) > 10:
        return jsonify({"error": "cartas debe ser lista de máx 10"}), 400

    if entidad != "tutu" and entidad not in DEIDADES:
        return jsonify({"error": "entidad desconocida"}), 400

    respuesta = invocador.leer_tarot(entidad, cartas, ctx.proyecto)
    return jsonify({"respuesta": respuesta.texto, "entidad": entidad})


# ═══════════════════════════════════════════════════════════════════════════
#  API — GRIMORIO / SIGILOS / LUNA / COSMOLOGÍA (con soporte legacy)
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/grimorio", methods=["GET"])
def get_grimorio():
    return jsonify(GrimorioLegadoRepo.leer(limite=30))


@app.route("/api/grimorio", methods=["POST"])
def post_grimorio():
    d = request.json
    if not isinstance(d, dict):
        return jsonify({"error": "JSON inválido"}), 400
    titulo = d.get("titulo", "Sin título")
    contenido = d.get("contenido", "")
    if e := _validar_string(titulo, "titulo", _MAX_TITULO_LEN):
        return jsonify({"error": e}), 400
    if e := _validar_string(contenido, "contenido", _MAX_CONTENIDO_LEN):
        return jsonify({"error": e}), 400
    GrimorioLegadoRepo.escribir(
        titulo=titulo,
        contenido=contenido,
        entidad=d.get("entidad"),
        tipo=d.get("tipo", "entrada"),
    )
    return jsonify({"ok": True})


@app.route("/api/decisiones", methods=["GET"])
def get_decisiones():
    return jsonify(DecisionRepo.historial(limite=15))


@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify(estadisticas())


@app.route("/api/memoria/<entidad>", methods=["GET"])
def get_memoria(entidad):
    ctx = _contexto()
    entidad = entidad.lower()
    memoria = ctx.cargar_memoria(entidad)
    return jsonify(memoria[-12:])


@app.route("/api/cerrar/<entidad>", methods=["POST"])
def cerrar_ritual(entidad):
    ctx = _contexto()
    entidad = entidad.lower()
    n = ctx.limpiar_memoria(entidad)
    return jsonify({"ok": True, "intercambios": n})


@app.route("/api/mensajes/quemar", methods=["POST"])
@_limitar_request()
def quemar_mensaje():
    ctx = _contexto()
    if not ctx.activo:
        return jsonify({"error": "proyecto requerido"}), 401
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "JSON inválido"}), 400
    msg_id = data.get("id")
    if not isinstance(msg_id, int):
        return jsonify({"error": "id debe ser entero"}), 400
    ok = ConversacionRepo.eliminar_mensaje(ctx.hash, msg_id)
    return jsonify({"ok": ok})


@app.route("/api/luna", methods=["GET"])
def get_luna():
    return jsonify(luna_hoy())


@app.route("/api/sigilos", methods=["GET"])
def get_sigilos():
    return jsonify(SigiloLegadoRepo.listar(limite=50))


@app.route("/api/sigilo", methods=["POST"])
@_limitar_request()
def post_sigilo():
    d = request.json
    if not isinstance(d, dict):
        return jsonify({"error": "JSON inválido"}), 400
    intencion = d.get("intencion", "")
    imagen = d.get("imagen", "")
    if e := _validar_string(intencion, "intencion", _MAX_TITULO_LEN):
        return jsonify({"error": e}), 400
    if e := _validar_string(imagen, "imagen", _MAX_CONTENIDO_LEN):
        return jsonify({"error": e}), 400
    sid = SigiloLegadoRepo.guardar(
        intencion=intencion,
        imagen=imagen,
        entidad=d.get("entidad"),
        origen=d.get("origen", "practicante"),
    )
    return jsonify({"ok": True, "id": sid})


@app.route("/api/sigilo/cargar/<int:sid>", methods=["POST"])
@_limitar_request()
def post_cargar_sigilo(sid):
    SigiloLegadoRepo.cargar(sid)
    return jsonify({"ok": True})


@app.route("/api/sigilo/quemar/<int:sid>", methods=["POST"])
@_limitar_request()
def post_quemar_sigilo(sid):
    SigiloLegadoRepo.quemar(sid)
    return jsonify({"ok": True})


@app.route("/api/sigilo/regalo/<entidad>", methods=["POST"])
def post_regalo_sigilo(entidad):
    ctx = _contexto()
    entidad = entidad.lower()

    if entidad != "tutu" and entidad not in DEIDADES:
        return jsonify({"error": "entidad desconocida"}), 400

    memoria = ctx.cargar_memoria(entidad)
    intencion = invocador.generar_intencion_sigilo(entidad, memoria)
    return jsonify({"intencion": intencion, "entidad": entidad})


@app.route("/api/astral/ciudades", methods=["GET"])
def get_ciudades():
    return jsonify({
        "disponible": KERYKEION_OK,
        "ciudades": {nombre: {"lat": c[0], "lng": c[1], "tz": c[2]}
                     for nombre, c in CIUDADES.items()},
    })


@app.route("/api/cosmologia", methods=["GET"])
def get_cosmologia():
    arboles_publicos = {}
    for k, v in ARBOLES_DEIDADES.items():
        arboles_publicos[k] = {
            "nombre": v["nombre"],
            "cultura": v["cultura"],
            "esencia": v["esencia"],
            "resonancia": v["resonancia"],
            "niveles": v["niveles"],
        }
        if "chakras_sociales" in v:
            arboles_publicos[k]["chakras_sociales"] = v["chakras_sociales"]

    return jsonify({
        "chakras": CHAKRAS,
        "chakras_social": CHAKRAS_ARTEMISA_SOCIAL,
        "sephiroth": ARBOL_VIDA_SEPHIROTH,
        "qliphoth": ARBOL_MUERTE_QLIPHOTH,
        "arboles_deidades": arboles_publicos,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  EXCEPTION HANDLERS — evita fugar stack traces al cliente
# ═══════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "ruta no encontrada"}), 404


@app.errorhandler(405)
def handle_405(e):
    return jsonify({"error": "método no permitido"}), 405


@app.errorhandler(413)
def handle_413(e):
    return jsonify({"error": "request demasiado grande (max 1 MB)"}), 413


@app.errorhandler(400)
def handle_400(e):
    return jsonify({"error": "solicitud inválida"}), 400


@app.errorhandler(500)
def handle_500(e):
    print(f"[ERROR 500] {e}", flush=True)
    return jsonify({"error": "error interno del servidor"}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    from werkzeug.exceptions import HTTPException
    if isinstance(e, HTTPException):
        return jsonify({"error": "error inesperado"}), e.code
    print(f"[ERROR NO CONTROLADO] {type(e).__name__}: {e}", flush=True)
    return jsonify({"error": "error inesperado"}), 500


# ═══════════════════════════════════════════════════════════════════════════
#  API — RUNAS (Elder Futhark)
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/runas/tirada", methods=["POST"])
@_limitar_request()
def api_runas_tirada():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    tipo = d.get("tipo", 3)
    pregunta = d.get("pregunta", "")

    if isinstance(tipo, str) and tipo.isdigit():
        tipo = int(tipo)
    n = 9 if tipo == 9 else 3

    runas = runas_tirada(n)
    posiciones = posiciones_9() if n == 9 else posiciones_3()

    # Contexto lunar
    luna = luna_hoy()
    luna_ctx = f"Luna: {luna.get('fase', {}).get('nombre', '?')} · {luna.get('fecha', '')}"

    # Deidad del proyecto (la más invocada) para personalizar la voz
    deidad_ctx = ""
    try:
        stats = estadisticas()
        votos = stats.get("votos_deidades", {})
        if votos:
            deidad_ctx = f"Deidad resonante del practicante: {max(votos, key=votos.get)}"
    except Exception:
        pass

    # Armar texto de runas para el LLM
    runas_texto = "\n".join([
        f"Posición {i+1} ({posiciones[i]}): {r['glyph']} {r['nombre']}"
        f" {'[INVERTIDA]' if r['invertida_activa'] else ''} — {r['significado_activo']}"
        for i, r in enumerate(runas)
    ])

    system = SYSTEM_VOLVA
    messages = [{
        "role": "user",
        "content": (
            f"Pregunta del practicante: {pregunta or '(sin pregunta explícita)'}\n\n"
            f"Tirada de {n} runas:\n{runas_texto}\n\n"
            f"{luna_ctx}\n{deidad_ctx}\n\n"
            "Dame la lectura completa."
        )
    }]

    narrativa = _ia(system, messages, max_tokens=500, temperature=0.85)

    return jsonify({
        "runas": runas,
        "posiciones": posiciones,
        "narrativa": narrativa,
        "tipo": n,
        "pregunta": pregunta,
        "luna": luna_ctx,
    })


@app.route("/api/runas/lista", methods=["GET"])
def api_runas_lista():
    return jsonify(RUNAS)


# ═══════════════════════════════════════════════════════════════════════════
#  API — GNOSIS
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/gnosis/metodos", methods=["GET"])
def api_gnosis_metodos():
    return jsonify(METODOS_GNOSIS)


@app.route("/api/gnosis/recomendar", methods=["POST"])
@_limitar_request()
def api_gnosis_recomendar():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    deidad = d.get("deidad", "tutu")
    fobias = d.get("fobias", [])

    metodo = recomendar_metodo(deidad, fobias)

    # LLM personaliza la recomendación
    system = SYSTEM_VOID_WALKER
    messages = [{
        "role": "user",
        "content": (
            f"El practicante trabaja con la deidad {deidad.upper()}.\n"
            f"Fobias/contraindicaciones: {', '.join(fobias) if fobias else 'ninguna'}.\n"
            f"El método recomendado es: {metodo['nombre']} ({metodo['familia']}).\n"
            f"Explícale en 2-3 párrafos por qué este método específico le conviene "
            f"y cómo prepararse para su primera vez."
        )
    }]

    explicacion = _ia(system, messages, max_tokens=300, temperature=0.75)

    return jsonify({
        "metodo": metodo,
        "explicacion": explicacion,
    })


@app.route("/api/gnosis/guia", methods=["POST"])
@_limitar_request()
def api_gnosis_guia():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    metodo_clave = d.get("metodo", "meditacion_vacia")
    observacion = d.get("observacion", "")

    metodo = guia_texto(metodo_clave)
    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    system = SYSTEM_VOID_WALKER
    if observacion:
        msg_content = (
            f"El practicante realizó gnosis con el método '{metodo['nombre']}' "
            f"y reporta: '{observacion}'\n"
            f"Luna actual: {luna_ctx}\n"
            "Interpreta qué nivel de gnosis alcanzó y qué significa lo que observó."
        )
    else:
        msg_content = (
            f"Guía detallada para el método '{metodo['nombre']}' ({metodo['familia']}).\n"
            f"Luna actual: {luna_ctx}\n"
            "Dá instrucciones paso a paso y señales de que 'entraste'."
        )

    messages = [{"role": "user", "content": msg_content}]
    respuesta = _ia(system, messages, max_tokens=400, temperature=0.8)

    return jsonify({
        "metodo": metodo,
        "respuesta": respuesta,
        "luna": luna_ctx,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  API — I CHING
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/iching/consulta", methods=["POST"])
@_limitar_request()
def api_iching_consulta():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    pregunta = (d.get("pregunta") or "").strip()[:_MAX_MESSAGE_LEN]

    resultado = iching_consulta(pregunta or None)

    hex_actual = resultado["hexagrama_actual"]
    hex_futuro = resultado.get("hexagrama_futuro")
    cambiantes = resultado["lineas_cambiantes"]
    trigramas  = resultado["trigramas"]

    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    # Construir mensaje para el LLM
    hex_info = (
        f"HEXAGRAMA ACTUAL: #{hex_actual.get('num')} {hex_actual.get('nombre_zh')} "
        f"— {hex_actual.get('nombre')}\n"
        f"Trigramas: {trigramas['superior']['nombre']} ({trigramas['superior']['atrib']}) "
        f"sobre {trigramas['inferior']['nombre']} ({trigramas['inferior']['atrib']})\n"
        f"Juicio: {hex_actual.get('juicio')}\n"
        f"Imagen: {hex_actual.get('imagen')}\n"
    )

    if cambiantes:
        lineas_txt = ", ".join(str(i + 1) for i in cambiantes)
        hex_info += f"\nLÍNEAS CAMBIANTES: posiciones {lineas_txt}\n"

    if hex_futuro:
        hex_info += (
            f"\nHEXAGRAMA FUTURO: #{hex_futuro.get('num')} {hex_futuro.get('nombre_zh')} "
            f"— {hex_futuro.get('nombre')}\n"
            f"Juicio futuro: {hex_futuro.get('juicio')}\n"
        )

    msg_content = (
        f"Pregunta del practicante: {pregunta or '(sin pregunta explícita)'}\n\n"
        f"{hex_info}\n"
        f"Luna actual: {luna_ctx}\n\n"
        "Entrega la lectura completa."
    )

    narrativa = _ia(
        SYSTEM_YIJING,
        [{"role": "user", "content": msg_content}],
        max_tokens=500,
        temperature=0.82,
    )

    return jsonify({
        "hexagrama_actual":  hex_actual,
        "hexagrama_futuro":  hex_futuro,
        "lineas":            resultado["lineas"],
        "lineas_cambiantes": cambiantes,
        "display_actual":    resultado["display_actual"],
        "display_futuro":    resultado["display_futuro"],
        "trigramas":         trigramas,
        "narrativa":         narrativa,
        "pregunta":          pregunta,
        "luna":              luna_ctx,
    })


@app.route("/api/iching/hexagramas", methods=["GET"])
def api_iching_hexagramas():
    from iching import HEXAGRAMAS
    return jsonify(HEXAGRAMAS)


# ═══════════════════════════════════════════════════════════════════════════
#  API — GEOMANCIA
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/geomancia/lectura", methods=["POST"])
@_limitar_request()
def api_geomancia_lectura():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    pregunta   = (d.get("pregunta") or "").strip()[:_MAX_MESSAGE_LEN]
    casa_foco  = int(d.get("casa_foco", 1))

    resultado = geo_lectura(pregunta or None, casa_foco)

    luna     = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    juez     = resultado["juez"]
    td       = resultado["testigo_der"]
    ti       = resultado["testigo_izq"]
    casas    = resultado["casas"]

    # Construir contexto para el LLM
    casas_relevantes = []
    for num in [1, casa_foco, 10, 7]:
        if num in casas:
            c = casas[num]
            casas_relevantes.append(
                f"Casa {num} ({c['dominio']}): {c['figura']['nombre']} — {c['figura']['significado'][:80]}"
            )
    casas_relevantes = list(dict.fromkeys(casas_relevantes))  # dedup preservando orden

    msg_content = (
        f"Pregunta: {pregunta or '(sin pregunta explícita)'}\n\n"
        f"JUEZ: {juez['figura']['nombre']} ({juez['figura']['nombre_es']}) — "
        f"{juez['figura']['significado']}\n\n"
        f"TESTIGO DERECHO: {td['figura']['nombre']} ({td['figura']['caracter']}) — "
        f"{td['figura']['significado'][:100]}\n"
        f"TESTIGO IZQUIERDO: {ti['figura']['nombre']} ({ti['figura']['caracter']}) — "
        f"{ti['figura']['significado'][:100]}\n\n"
        f"CASAS RELEVANTES:\n" + "\n".join(casas_relevantes) + "\n\n"
        f"Luna: {luna_ctx}\n\n"
        "Entrega la lectura completa."
    )

    narrativa = _ia(
        SYSTEM_GEOMANTE,
        [{"role": "user", "content": msg_content}],
        max_tokens=500,
        temperature=0.80,
    )

    return jsonify({
        "madres":      resultado["madres"],
        "hijas":       resultado["hijas"],
        "sobrinas":    resultado["sobrinas"],
        "testigo_der": td,
        "testigo_izq": ti,
        "juez":        juez,
        "sentencia":   resultado["sentencia"],
        "casas":       casas,
        "casa_foco":   casa_foco,
        "narrativa":   narrativa,
        "pregunta":    pregunta,
        "luna":        luna_ctx,
    })


@app.route("/api/geomancia/figuras", methods=["GET"])
def api_geomancia_figuras():
    return jsonify(GEO_FIGURAS)


# ═══════════════════════════════════════════════════════════════════════════
#  API — SERVITORS
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/servitors/crear", methods=["POST"])
@_limitar_request()
def api_servitors_crear():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    nombre       = (d.get("nombre") or "").strip()[:60]
    funcion      = (d.get("funcion") or "").strip()[:_MAX_MESSAGE_LEN]
    forma        = (d.get("forma") or "").strip()[:500]
    deidad_padre = (d.get("deidad_padre") or "ninguna").strip().lower()

    if not nombre:
        return jsonify({"error": "nombre requerido"}), 400
    if not funcion:
        return jsonify({"error": "funcion requerida"}), 400
    if deidad_padre not in DEIDADES_VALIDAS:
        deidad_padre = "ninguna"

    if not forma:
        forma = f"Entidad de {deidad_padre.capitalize()}, forma etérea indefinida"

    servitor = ServitorRepo.crear(
        ctx.hash, nombre, funcion, forma,
        None if deidad_padre == "ninguna" else deidad_padre
    )
    if not servitor:
        return jsonify({"error": "Ya existe un servitor con ese nombre"}), 409

    # Proyectar la intención del servitor al bosque colectivo
    clave_intencion = " ".join(funcion.split()[:4]).lower()[:40]
    try:
        GestorEsferas.marcar("intencion", clave_intencion,
                             {"servitor": nombre, "proyecto": ctx.hash[:8]},
                             ctx.hash)
    except Exception:
        pass

    return jsonify({"servitor": enriquecer(servitor), "display": render_servitor(enriquecer(servitor))})


@app.route("/api/servitors/lista", methods=["GET"])
def api_servitors_lista():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    servitors = ServitorRepo.listar(ctx.hash)
    enriquecidos = [enriquecer(s) for s in servitors]
    return jsonify({"servitors": enriquecidos})


@app.route("/api/servitors/estado/<nombre>", methods=["GET"])
def api_servitors_estado(nombre: str):
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    nombre = nombre.strip()[:60]
    servitor = ServitorRepo.obtener(ctx.hash, nombre)
    if not servitor:
        return jsonify({"error": "Servitor no encontrado"}), 404

    enriq = enriquecer(servitor)
    return jsonify({
        "servitor": enriq,
        "display":  render_servitor(enriq),
        "descripcion_estado": sistema_descripcion_estado(enriq["estado_vivo"]),
    })


@app.route("/api/servitors/feed", methods=["POST"])
def api_servitors_feed():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    nombre = (d.get("nombre") or "").strip()[:60]
    if not nombre:
        return jsonify({"error": "nombre requerido"}), 400

    servitor = ServitorRepo.obtener(ctx.hash, nombre)
    if not servitor:
        return jsonify({"error": "Servitor no encontrado"}), 404

    enriq = enriquecer(servitor)
    if enriq["estado_vivo"] == "disuelto":
        return jsonify({"error": "El servitor ya está disuelto — no puede ser alimentado"}), 409

    nueva_i    = nueva_intensidad_feed(enriq["intensidad_actual"])
    nuevo_est  = calcular_estado(nueva_i, "activo")

    actualizado = ServitorRepo.actualizar_intensidad(
        ctx.hash, nombre, nueva_i, nuevo_est, actualizar_feed=True
    )
    enriq_nuevo = enriquecer(actualizado)

    # Feed refuerza la esfera de intención en el bosque
    clave_intencion = " ".join(
        (enriq_nuevo.get("funcion") or nombre).split()[:4]
    ).lower()[:40]
    try:
        GestorEsferas.marcar("intencion", clave_intencion,
                             {"servitor": nombre, "feed": True},
                             ctx.hash)
    except Exception:
        pass

    return jsonify({
        "servitor":           enriq_nuevo,
        "display":            render_servitor(enriq_nuevo),
        "intensidad_anterior":enriq["intensidad_actual"],
        "intensidad_nueva":   nueva_i,
    })


@app.route("/api/servitors/disolver", methods=["POST"])
def api_servitors_disolver():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    nombre = (d.get("nombre") or "").strip()[:60]
    if not nombre:
        return jsonify({"error": "nombre requerido"}), 400

    servitor = ServitorRepo.obtener(ctx.hash, nombre)
    if not servitor:
        return jsonify({"error": "Servitor no encontrado"}), 404

    ServitorRepo.actualizar_intensidad(ctx.hash, nombre, 0.0, "disuelto")

    return jsonify({
        "ok":     True,
        "nombre": nombre,
        "mensaje": f"El servitor {nombre} ha sido disuelto. Su energía retorna al caos primordial.",
    })


@app.route("/api/servitors/invocar", methods=["POST"])
@_limitar_request()
def api_servitors_invocar():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    nombre   = (d.get("nombre") or "").strip()[:60]
    pregunta = (d.get("pregunta") or "").strip()[:_MAX_MESSAGE_LEN]

    if not nombre:
        return jsonify({"error": "nombre requerido"}), 400

    servitor = ServitorRepo.obtener(ctx.hash, nombre)
    if not servitor:
        return jsonify({"error": "Servitor no encontrado"}), 404

    enriq = enriquecer(servitor)
    if enriq["estado_vivo"] == "disuelto":
        return jsonify({"error": "El servitor está disuelto — no puede ser invocado"}), 409

    deidad = servitor.get("deidad_padre") or "autónomo"
    system = SYSTEM_SERVITOR.format(
        funcion=servitor["funcion"],
        forma=servitor["forma"],
        deidad_padre=deidad,
        intensidad=enriq["porcentaje"],
    )

    msg_content = pregunta or f"Practicante invoca al servitor {nombre}. ¿Qué tienes para decirle sobre tu misión?"

    respuesta = _ia(
        system,
        [{"role": "user", "content": msg_content}],
        max_tokens=300,
        temperature=0.9,
    )

    return jsonify({
        "servitor":  enriq,
        "display":   render_servitor(enriq),
        "respuesta": respuesta,
        "pregunta":  pregunta,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  API — ORÁCULO DE LA DISCORDIA
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/discord/oraculo", methods=["GET"])
@_limitar_request()
def api_discord_oraculo():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    resultado = discord_oraculo()

    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    runa    = resultado["runa"]
    señal   = resultado["señal"]
    tension = f"{resultado['tension_a']} ↔ {resultado['tension_b']}"
    deidad  = resultado["deidad_sombra"].upper()

    msg_content = (
        f"La señal caótica de Eris para este momento:\n\n"
        f"SEÑAL: {señal}\n"
        f"RUNA: {runa['glyph']} {runa['nombre']} — {runa['significado']}\n"
        f"TENSIÓN ACTIVA: {tension}\n"
        f"DEIDAD SOMBRA: {deidad}\n"
        f"Luna actual: {luna_ctx}\n\n"
        "Entrega el mensaje de Eris."
    )

    mensaje = _ia(
        SYSTEM_ERIS,
        [{"role": "user", "content": msg_content}],
        max_tokens=200,
        temperature=0.95,
    )

    return jsonify({
        "runa":         runa,
        "señal":        señal,
        "tension_a":    resultado["tension_a"],
        "tension_b":    resultado["tension_b"],
        "deidad_sombra": resultado["deidad_sombra"],
        "mensaje":      mensaje,
        "display":      render_oraculo(resultado),
        "luna":         luna_ctx,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  API — SYNCHRONICIDADES
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/sync/nueva", methods=["POST"])
@_limitar_request()
def api_sync_nueva():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    signo     = (d.get("signo") or "").strip()[:200]
    categoria = (d.get("categoria") or "otro").strip().lower()
    dias      = max(1, min(90, int(d.get("dias", 7))))

    if not signo:
        return jsonify({"error": "signo requerido"}), 400
    if categoria not in SYNC_CATEGORIAS:
        categoria = "otro"

    from datetime import timedelta
    from datetime import datetime as _dt
    plazo = (_dt.now() + timedelta(days=dias)).isoformat()

    luna = luna_hoy()
    fase_lunar = luna.get("fase", {}).get("nombre")

    sync = SyncRepo.crear(ctx.hash, signo, categoria, plazo, fase_lunar)
    enriquecida = enriquecer_sync(sync)

    # La posibilidad existe en el bosque — esfera con amplitud base
    try:
        GestorEsferas.marcar("sincronicidad", categoria,
                             {"signo": signo[:60], "fase": fase_lunar},
                             ctx.hash)
    except Exception:
        pass

    return jsonify({
        "sync":    enriquecida,
        "display": render_sync(enriquecida),
        "mensaje": f"Sync registrada. Observa durante {dias} días: '{signo}'.",
    })


@app.route("/api/sync/confirmar", methods=["POST"])
@_limitar_request()
def api_sync_confirmar():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    sync_id = d.get("id")
    nota    = (d.get("nota") or "").strip()[:500]

    if not sync_id:
        return jsonify({"error": "id requerido"}), 400

    sync = SyncRepo.confirmar(int(sync_id), ctx.hash, nota or None)
    if not sync:
        return jsonify({"error": "Sync no encontrada"}), 404

    enriquecida = enriquecer_sync(sync)

    # La confirmación amplifica la esfera — el patrón se vuelve real en el bosque
    try:
        GestorEsferas.marcar("sincronicidad", sync.get("categoria", "otro"),
                             {"confirmada": True, "signo": sync.get("signo_esperado", "")[:60]},
                             ctx.hash)
        GestorEsferas.marcar("sincronicidad", sync.get("categoria", "otro"),
                             {"segundo_mark": True}, ctx.hash)
    except Exception:
        pass

    return jsonify({
        "sync":    enriquecida,
        "display": render_sync(enriquecida),
        "mensaje": "¡La synchronicidad fue confirmada. El patrón se repite.",
    })


@app.route("/api/sync/lista", methods=["GET"])
def api_sync_lista():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    syncs = SyncRepo.listar(ctx.hash)
    return jsonify({"syncs": [enriquecer_sync(s) for s in syncs]})


@app.route("/api/sync/colectiva", methods=["GET"])
def api_sync_colectiva():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    todas = SyncRepo.todas_recientes(dias=30)
    resumen = colectiva_resumen(todas)

    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    return jsonify({
        "resumen":  resumen,
        "luna":     luna_ctx,
        "periodo":  "últimos 30 días",
    })


# ═══════════════════════════════════════════════════════════════════════════
#  API — 8 RAYOS DEL OCTAGRAM
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/rayos/preguntas", methods=["GET"])
def api_rayos_preguntas():
    return jsonify({"preguntas": PREGUNTAS_TEST, "instrucciones": "Puntúa cada pregunta del 1 (no resuena) al 5 (resuena profundamente)."})


@app.route("/api/rayos/test", methods=["POST"])
@_limitar_request()
def api_rayos_test():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    respuestas = d.get("respuestas", [])

    if len(respuestas) != 8:
        return jsonify({"error": "Se requieren exactamente 8 respuestas (1-5)"}), 400

    try:
        respuestas = [max(1, min(5, int(r))) for r in respuestas]
    except (ValueError, TypeError):
        return jsonify({"error": "Las respuestas deben ser números del 1 al 5"}), 400

    rayo_id    = calcular_rayo(respuestas)
    rayo       = perfil_rayo(rayo_id)
    distrib    = rayos_distribucion(respuestas)
    score_natal = respuestas[rayo_id - 1]

    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    top3 = distrib[:3]
    distrib_txt = "\n".join([
        f"  {d['glyph']} {d['nombre']}: {d['score']}/5"
        for d in top3
    ])

    msg_content = (
        f"Rayo natal del practicante: {rayo['nombre']} (puntuación {score_natal}/5)\n\n"
        f"Distribución top 3:\n{distrib_txt}\n\n"
        f"Descripción del rayo natal:\n{rayo['descripcion']}\n\n"
        f"Deidades afines: {', '.join(rayo.get('deidades', []))}\n"
        f"Virtud: {rayo.get('virtud', '')}\n"
        f"Sombra: {rayo.get('sombra', '')}\n\n"
        f"Luna: {luna_ctx}\n\n"
        "Entrega el perfil mágico de este practicante según su rayo natal."
    )

    interpretacion = _ia(
        SYSTEM_ORACULO_RAYO,
        [{"role": "user", "content": msg_content}],
        max_tokens=300,
        temperature=0.78,
    )

    return jsonify({
        "rayo_id":       rayo_id,
        "rayo":          rayo,
        "score_natal":   score_natal,
        "distribucion":  distrib,
        "interpretacion": interpretacion,
        "display":       render_rayo(rayo, score_natal),
        "luna":          luna_ctx,
    })


@app.route("/api/rayos/catalogo", methods=["GET"])
def api_rayos_catalogo():
    return jsonify({"rayos": list(OCTAGRAM.values())})


# ═══════════════════════════════════════════════════════════════════════════
#  API — PARADIGM SHIFTING
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/paradigm/catalogo", methods=["GET"])
def api_paradigm_catalogo():
    return jsonify({"paradigmas": list(PARADIGMAS.values())})


@app.route("/api/paradigm/iniciar", methods=["POST"])
@_limitar_request()
def api_paradigm_iniciar():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    paradigma_id = int(d.get("paradigma_id", 0))

    if paradigma_id not in PARADIGMAS:
        return jsonify({"error": f"paradigma_id inválido (1-{len(PARADIGMAS)})"}), 400

    paradigma_def = PARADIGMAS[paradigma_id]

    # Verificar si ya tiene uno activo
    activo = ParadigmaRepo.obtener_activo(ctx.hash)
    if activo:
        return jsonify({
            "error": "Ya tienes un paradigma activo. Complétalo o abandónalo primero.",
            "paradigma_activo": enriquecer_paradigma(activo),
        }), 409

    paradigma = ParadigmaRepo.iniciar(
        ctx.hash, paradigma_id,
        paradigma_def["nombre"], paradigma_def["deidad_guia"]
    )
    if not paradigma:
        return jsonify({"error": "Error al iniciar el paradigma"}), 500

    enriquecido = enriquecer_paradigma(paradigma)

    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    msg_content = (
        f"El practicante inicia el Paradigma: {paradigma_def['nombre']}\n"
        f"Subtítulo: {paradigma_def['subtitulo']}\n\n"
        f"Descripción del paradigma:\n{paradigma_def['descripcion']}\n\n"
        f"Ritual de entrada: {paradigma_def['ritual_entrada']}\n"
        f"Deidad guía: {paradigma_def['deidad_guia'].upper()}\n"
        f"Luna del inicio: {luna_ctx}\n\n"
        "Es el DÍA 1. Guía al practicante en el ritual de entrada y explica qué cambiará en su percepción."
    )

    orientacion = _ia(
        SYSTEM_PSICONAUTA,
        [{"role": "user", "content": msg_content}],
        max_tokens=300,
        temperature=0.80,
    )

    return jsonify({
        "paradigma":    enriquecido,
        "paradigma_def": paradigma_def,
        "orientacion":  orientacion,
        "display":      render_paradigma(enriquecido),
        "luna":         luna_ctx,
    })


@app.route("/api/paradigm/checkin", methods=["POST"])
@_limitar_request()
def api_paradigm_checkin():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    d = request.json or {}
    paradigma_id = d.get("paradigma_id")
    nota         = (d.get("nota") or "").strip()[:_MAX_MESSAGE_LEN]

    # Si no viene paradigma_id, usar el activo
    if paradigma_id is None:
        activo = ParadigmaRepo.obtener_activo(ctx.hash)
        if not activo:
            return jsonify({"error": "No tienes ningún paradigma activo"}), 404
        paradigma_id = activo["paradigma_id"]

    paradigma_id = int(paradigma_id)
    paradigma    = ParadigmaRepo.obtener(ctx.hash, paradigma_id)
    if not paradigma:
        return jsonify({"error": "Paradigma no encontrado"}), 404

    progreso = calcular_progreso(paradigma["fecha_inicio"])
    dia_actual = progreso["dia_actual"]

    if not nota:
        nota = f"Check-in día {dia_actual} sin observaciones."

    paradigma = ParadigmaRepo.agregar_checkin(
        ctx.hash, paradigma_id, nota, dia_actual
    )
    enriquecido = enriquecer_paradigma(paradigma)

    # Si completó los 30 días, marcar como integrado
    if progreso["completado"]:
        ParadigmaRepo.integrar(ctx.hash, paradigma_id)
        enriquecido["estado"] = "integrado"

    paradigma_def = PARADIGMAS.get(paradigma_id, {})
    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    tipo_checkin = "INTEGRACIÓN (día 30)" if progreso["completado"] else f"día {dia_actual}"

    msg_content = (
        f"Paradigma: {paradigma_def.get('nombre', '')} — check-in {tipo_checkin}\n"
        f"Práctica diaria del paradigma: {paradigma_def.get('practica_diaria', '')}\n"
        f"Reporte del practicante: {nota}\n"
        f"Progreso: {dia_actual}/{PARADIGM_DIAS} días ({progreso['porcentaje']}%)\n"
        f"Luna: {luna_ctx}\n\n"
        "Responde al check-in del practicante."
    )

    respuesta = _ia(
        SYSTEM_PSICONAUTA,
        [{"role": "user", "content": msg_content}],
        max_tokens=280,
        temperature=0.78,
    )

    return jsonify({
        "paradigma":  enriquecido,
        "dia_actual": dia_actual,
        "completado": progreso["completado"],
        "respuesta":  respuesta,
        "display":    render_paradigma(enriquecido),
        "luna":       luna_ctx,
    })


@app.route("/api/paradigm/estado", methods=["GET"])
def api_paradigm_estado():
    ctx = _contexto()
    err = _proyecto_requerido(ctx)
    if err:
        return err

    paradigmas = ParadigmaRepo.listar(ctx.hash)
    enriquecidos = [enriquecer_paradigma(p) for p in paradigmas]
    activo = next((p for p in enriquecidos if p["estado"] == "activo"), None)

    return jsonify({
        "paradigmas": enriquecidos,
        "activo":     activo,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  FASE 2: ENDPOINTS USUARIO/EXP/GRIMORIO
# ═══════════════════════════════════════════════════════════════════════════

# Constantes Capa 1
CAPA1_MAX_TITULO = 255
CAPA1_MAX_CONTENIDO = 10000
CAPA1_MAX_INTENCION = 500
CAPA1_EXP_NUEVA_ENTRADA = 5
CAPA1_EXP_NUEVO_SIGILO = 10
CAPA1_EXP_CARGAR_SIGILO = 25
ESTADO_SIGILO_CREADO = "creado"
ESTADO_SIGILO_CARGADO = "cargado"

# ── CAPA 2: LA MESA (Mago Personal) ───────────────────────────────────────
CAPA2_MAX_ARCANO = 255  # Máximo length para nombre de arcano
CAPA2_EXP_NUEVA_TIRADA = 5  # Exp por tirada tarot (balance con Capa 1)
CAPA2_EXP_CARGAR_ORACULO = 10  # Exp por oráculo (runas, I Ching, etc.)
CAPA2_EXP_CHAT_DEIDAD = 3  # Exp por mensaje con deidad

# ── CAPA 3: EL ÁRBOL (Colectivo) ──────────────────────────────────────────
CAPA3_MAX_INTENCION = 500  # Máximo length para intención de semilla
CAPA3_MAX_DESCRIPCION = 500  # Máximo length para descripción de sincronicidad
CAPA3_MAX_RITUAL = 280  # Máximo length para el ritual de micorriza
CAPA3_EXP_SEMILLA = 10  # Exp por sembrar un sigilo en El Árbol
CAPA3_EXP_SYNC = 5  # Exp por registrar una sincronicidad
CAPA3_EXP_MICORRIZA = 25  # Exp por conectar con otro mago (a ambos)
CAPA3_SEMILLAS_LIMITE = 50  # Máximo de semillas en listado colectivo
CAPA3_SYNC_LIMITE = 50  # Máximo de sincronicidades en listado colectivo
ESFERA_TIPOS_VALIDOS = ("geo", "elemental", "tematica", "resonancia",
                        "intencion", "sincronicidad", "conocimiento", "paradigma")

_USUARIO_CACHE = {}  # Caché temporal: proyecto_hash → user_id
_USUARIO_CACHE_LOCK = Lock()

def _obtener_o_crear_usuario_proyecto(proyecto_hash: str) -> int:
    """Obtener o crear usuario asociado a proyecto (idempotente en la sesión, thread-safe).

    Nota: Caché en memoria solo para sesión. Para persistencia real,
    guardar user_id en proyecto metadatos via ProyectoRepo.
    """
    global _USUARIO_CACHE

    with _USUARIO_CACHE_LOCK:
        if proyecto_hash in _USUARIO_CACHE:
            return _USUARIO_CACHE[proyecto_hash]

        nombre_mago = f"Mago-{proyecto_hash[:12]}"
        usuario = UsuarioRepo.crear(nombre_mago=nombre_mago)
        _USUARIO_CACHE[proyecto_hash] = usuario["id"]
        return usuario["id"]


def requiere_usuario_capa1(f):
    """Decorator: obtiene/crea usuario del proyecto y lo pasa a la función.

    Inyecta `user_id` como parámetro a la función decorada.
    """
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        ctx = _contexto()
        err = _proyecto_requerido(ctx)
        if err:
            return err
        user_id = _obtener_o_crear_usuario_proyecto(ctx.hash)
        return f(user_id=user_id, *args, **kwargs)

    return wrapper


def requiere_usuario_capa2(f):
    """Decorator: igual a requiere_usuario_capa1 (mismo patrón para Capa 2).

    Inyecta `user_id` como parámetro a la función decorada.
    """
    return requiere_usuario_capa1(f)


@app.route("/api/capa1/usuario/actual", methods=["GET"])
@requiere_usuario_capa1
def api_capa1_usuario_actual(user_id: int) -> tuple[dict, int]:
    """Obtener o crear usuario para proyecto actual."""
    usuario = UsuarioRepo.obtener(user_id)
    return jsonify({"usuario": usuario}), 200


@app.route("/api/capa1/grimorio/nueva", methods=["POST"])
@requiere_usuario_capa1
def api_capa1_grimorio_nueva(user_id: int) -> tuple[dict, int]:
    """Crear nueva entrada en grimorio."""
    data = request.get_json() or {}
    titulo = data.get("titulo", "").strip()
    contenido = data.get("contenido", "").strip()
    tags = data.get("tags", "").strip()

    if not titulo or len(titulo) > CAPA1_MAX_TITULO:
        return jsonify({"error": f"Título inválido (1-{CAPA1_MAX_TITULO} chars)"}), 400
    if not contenido or len(contenido) > CAPA1_MAX_CONTENIDO:
        return jsonify({"error": f"Contenido inválido (1-{CAPA1_MAX_CONTENIDO} chars)"}), 400

    entrada = GrimorioRepo.crear(user_id, titulo, contenido, tags or None)
    ExpRepo.agregar_exp(user_id, "grimorio", CAPA1_EXP_NUEVA_ENTRADA)

    return jsonify({"entrada": entrada}), 201


@app.route("/api/capa1/grimorio", methods=["GET"])
@requiere_usuario_capa1
def api_capa1_grimorio_listar(user_id: int) -> tuple[dict, int]:
    """Listar entradas del grimorio."""
    entradas = GrimorioRepo.listar_por_usuario(user_id)
    return jsonify({"entradas": entradas, "total": len(entradas)}), 200


@app.route("/api/capa1/exp", methods=["GET"])
@requiere_usuario_capa1
def api_capa1_exp(user_id: int) -> tuple[dict, int]:
    """Obtener progreso de experiencia (Capa 1: Grimorio)."""
    exp = ExpRepo.obtener(user_id, "grimorio")
    if not exp:
        exp = ExpRepo.crear_o_actualizar(user_id, "grimorio", 0, 1)
    return jsonify({"exp": exp}), 200


@app.route("/api/capa1/sigilo/dibujar", methods=["POST"])
@requiere_usuario_capa1
def api_capa1_sigilo_dibujar(user_id: int) -> tuple[dict, int]:
    """Dibujar nuevo sigilo."""
    data = request.get_json() or {}
    intencion = data.get("intencion", "").strip()
    dibujo = data.get("dibujo", "").strip()

    if not intencion or len(intencion) > CAPA1_MAX_INTENCION:
        return jsonify({"error": f"Intención inválida (1-{CAPA1_MAX_INTENCION} chars)"}), 400
    if not dibujo:
        return jsonify({"error": "Dibujo requerido"}), 400

    sigilo = SigiloRepo.crear_dibujado(user_id, intencion, dibujo)
    ExpRepo.agregar_exp(user_id, "grimorio", CAPA1_EXP_NUEVO_SIGILO)

    return jsonify({"sigilo": sigilo}), 201


@app.route("/api/capa1/sigilos", methods=["GET"])
@requiere_usuario_capa1
def api_capa1_sigilos_listar(user_id: int) -> tuple[dict, int]:
    """Listar sigilos activos (sin cargar)."""
    sigilos = SigiloRepo.listar_por_usuario(user_id, estado=ESTADO_SIGILO_CREADO)
    return jsonify({"sigilos": sigilos, "total": len(sigilos)}), 200


@app.route("/api/capa1/sigilo/<int:sigilo_id>/cargar", methods=["POST"])
@requiere_usuario_capa1
def api_capa1_sigilo_cargar(user_id: int, sigilo_id: int) -> tuple[dict, int]:
    """Cargar sigilo (desaparece del dashboard, se olvida)."""
    sigilo = SigiloRepo.cargar(sigilo_id)

    if not sigilo:
        return jsonify({"error": "Sigilo no encontrado"}), 404

    ExpRepo.agregar_exp(sigilo["user_id"], "grimorio", CAPA1_EXP_CARGAR_SIGILO)

    return jsonify({"sigilo": sigilo}), 200


# ── CAPA 2: LA MESA (Mago Personal) ─────────────────────────────────────────

@app.route("/api/capa2/tarot/nueva", methods=["POST"])
@requiere_usuario_capa2
def api_capa2_tarot_nueva(user_id: int) -> tuple[dict, int]:
    """Crear nueva tirada de tarot personal."""
    from base_datos.altar import TarotRepo

    data = request.get_json() or {}
    arcano_principal = data.get("arcano_principal", "").strip()
    posiciones = data.get("posiciones", {})
    interpretacion = data.get("interpretacion", "").strip()

    if not arcano_principal or len(arcano_principal) > CAPA2_MAX_ARCANO:
        return jsonify({"error": f"Arcano inválido (1-{CAPA2_MAX_ARCANO} chars)"}), 400
    if not isinstance(posiciones, dict) or not posiciones:
        return jsonify({"error": "Posiciones requeridas (dict no vacío)"}), 400

    tirada_id = TarotRepo.crear(user_id, arcano_principal, posiciones,
                                interpretacion or None)
    ExpRepo.agregar_exp(user_id, "tarot", CAPA2_EXP_NUEVA_TIRADA)

    return jsonify({"tirada_id": tirada_id, "exp_ganada": CAPA2_EXP_NUEVA_TIRADA}), 201


@app.route("/api/capa2/tarot", methods=["GET"])
@requiere_usuario_capa2
def api_capa2_tarot_listar(user_id: int) -> tuple[dict, int]:
    """Listar tiradas de tarot del usuario."""
    from base_datos.altar import TarotRepo

    tiradas = TarotRepo.listar_por_usuario(user_id)
    return jsonify({"tiradas": tiradas, "total": len(tiradas)}), 200


@app.route("/api/capa2/oraculo/nueva", methods=["POST"])
@requiere_usuario_capa2
def api_capa2_oraculo_nueva(user_id: int) -> tuple[dict, int]:
    """Consultar oráculo personal (runas, I Ching, geomancia)."""
    from base_datos.altar import OráculoRepo

    data = request.get_json() or {}
    tipo = data.get("tipo", "").strip().lower()
    pregunta = data.get("pregunta", "").strip()

    tipos_validos = ["runas", "iching", "geomancia"]
    if tipo not in tipos_validos:
        return jsonify({"error": f"Tipo inválido. Válidos: {', '.join(tipos_validos)}"}), 400
    if not pregunta:
        return jsonify({"error": "Pregunta requerida"}), 400

    resultado = _generar_resultado_oraculo(tipo, pregunta)

    oraculo_id = OráculoRepo.crear(user_id, tipo, pregunta, resultado)
    ExpRepo.agregar_exp(user_id, "oraculo", CAPA2_EXP_CARGAR_ORACULO)

    return jsonify({"oraculo_id": oraculo_id, "exp_ganada": CAPA2_EXP_CARGAR_ORACULO}), 201


@app.route("/api/capa2/oraculo", methods=["GET"])
@requiere_usuario_capa2
def api_capa2_oraculo_listar(user_id: int) -> tuple[dict, int]:
    """Listar oráculos del usuario, opcionalmente filtrado por tipo."""
    from base_datos.altar import OráculoRepo

    tipo = request.args.get("tipo", "").strip().lower()

    if tipo:
        oráculos = OráculoRepo.listar_por_tipo(user_id, tipo)
    else:
        oráculos = OráculoRepo.listar_por_usuario(user_id)

    return jsonify({"oráculos": oráculos, "total": len(oráculos)}), 200


def _generar_resultado_oraculo(tipo: str, pregunta: str) -> dict:
    """Generar resultado de oráculo basado en tipo (mock para TB #7)."""
    if tipo == "runas":
        return {
            "runas": ["Fehu", "Isa"],
            "significado": "Abundancia y pausa reflexiva",
            "consejo": "Considera lo que tienes y lo que necesita descanso"
        }
    elif tipo == "iching":
        return {
            "hexagrama": 11,
            "nombre": "Tai",
            "interpretacion": "La paz prevalece",
            "línea": 2
        }
    elif tipo == "geomancia":
        return {
            "figuras": ["Acquisitio", "Laetitia"],
            "casa": "Primera",
            "significado": "Adquisición y alegría"
        }
    return {}


@app.route("/api/capa2/deidad/<nombre>/hablar", methods=["POST"])
@requiere_usuario_capa2
def api_capa2_hablar_deidad(user_id: int, nombre: str) -> tuple[dict, int]:
    """Conversar con deidad personal."""
    from base_datos.altar import ConversacionCapaRepo

    nombre = nombre.lower().capitalize()  # "lilith" → "Lilith"
    deidades_validas = ["Lilith", "Artemisa", "Afrodita", "Isis"]

    if nombre not in deidades_validas:
        return jsonify({"error": f"Deidad inválida. Válidas: {', '.join(deidades_validas)}"}), 400

    data = request.get_json() or {}
    mensaje = data.get("mensaje", "").strip()

    if not mensaje:
        return jsonify({"error": "Mensaje requerido"}), 400

    # Guardar mensaje del usuario
    ConversacionCapaRepo.guardar_mensaje(user_id, nombre, "user", mensaje)

    # Generar respuesta de deidad (mock para TB #8)
    respuesta = _generar_respuesta_deidad(nombre, mensaje)

    # Guardar respuesta de deidad
    ConversacionCapaRepo.guardar_mensaje(user_id, nombre, "deidad", respuesta)

    ExpRepo.agregar_exp(user_id, "deidad", CAPA2_EXP_CHAT_DEIDAD)

    return jsonify({"respuesta": respuesta, "exp_ganada": CAPA2_EXP_CHAT_DEIDAD}), 200


@app.route("/api/capa2/deidad/<nombre>/historial", methods=["GET"])
@requiere_usuario_capa2
def api_capa2_historial_deidad(user_id: int, nombre: str) -> tuple[dict, int]:
    """Obtener historial de conversación con deidad."""
    from base_datos.altar import ConversacionCapaRepo

    nombre = nombre.lower().capitalize()
    deidades_validas = ["Lilith", "Artemisa", "Afrodita", "Isis"]

    if nombre not in deidades_validas:
        return jsonify({"error": f"Deidad inválida. Válidas: {', '.join(deidades_validas)}"}), 400

    historial = ConversacionCapaRepo.obtener_historial(user_id, nombre)
    return jsonify({"historial": historial, "total": len(historial)}), 200


def _generar_respuesta_deidad(nombre: str, mensaje: str) -> str:
    """Generar respuesta de deidad (mock para TB #8, mejora en producción con IA)."""
    respuestas = {
        "Lilith": "Tu libertad es tu poder. ¿Qué cadenas te atan?",
        "Artemisa": "La claridad viene de la acción. Caza lo que es tuyo.",
        "Afrodita": "El amor que buscas comienza en ti. Cultiva tu belleza interior.",
        "Isis": "La magia de la transformación ya está en tus manos. Recuerda quien eres.",
    }
    return respuestas.get(nombre, "Escucho tu pregunta. Reflexiona profundamente.")


@app.route("/api/capa2/servitor/crear", methods=["POST"])
@requiere_usuario_capa2
def api_capa2_servitor_crear(user_id: int) -> tuple[dict, int]:
    """Crear nuevo servitor personal."""
    from base_datos.altar import ServitorCapaRepo

    data = request.get_json() or {}
    nombre = data.get("nombre", "").strip()
    intencion = data.get("intencion", "").strip()

    if not nombre:
        return jsonify({"error": "Nombre del servitor requerido"}), 400
    if not intencion:
        return jsonify({"error": "Intención requerida"}), 400

    servitor_id = ServitorCapaRepo.crear(user_id, nombre, intencion)

    return jsonify({"servitor_id": servitor_id, "exp_ganada": 0}), 201


@app.route("/api/capa2/servitor", methods=["GET"])
@requiere_usuario_capa2
def api_capa2_servitor_listar(user_id: int) -> tuple[dict, int]:
    """Listar servitors del usuario."""
    from base_datos.altar import ServitorCapaRepo

    servitors = ServitorCapaRepo.listar_por_usuario(user_id)
    return jsonify({"servitors": servitors, "total": len(servitors)}), 200


@app.route("/api/capa2/servitor/<int:servitor_id>/evocar", methods=["POST"])
@requiere_usuario_capa2
def api_capa2_servitor_evocar(user_id: int, servitor_id: int) -> tuple[dict, int]:
    """Evocar servitor (aumentar energía)."""
    from base_datos.altar import ServitorCapaRepo

    servitor = ServitorCapaRepo.evocar(servitor_id)

    if not servitor:
        return jsonify({"error": "Servitor no encontrado"}), 404

    if servitor['user_id'] != user_id:
        return jsonify({"error": "Servitor no pertenece a este usuario"}), 403

    ExpRepo.agregar_exp(user_id, "servitor", 5)

    return jsonify({"energia": servitor["energia"], "exp_ganada": 5}), 200


# ── CAPA 3: EL ÁRBOL (Colectivo - Bosque Vivo) ──────────────────────────────

@app.route("/api/capa3/esferas", methods=["GET"])
@requiere_usuario_capa2
def api_capa3_esferas_listar(user_id: int) -> tuple[dict, int]:
    """Listar esferas del usuario (opcionalmente filtrado por tipo)."""
    from base_datos.bosque import EsferaCapaRepo

    tipo = request.args.get("tipo", "").strip().lower()

    if tipo:
        esferas = EsferaCapaRepo.listar_por_tipo(user_id, tipo)
    else:
        esferas = EsferaCapaRepo.listar_por_usuario(user_id)

    return jsonify({"esferas": esferas, "total": len(esferas)}), 200


@app.route("/api/capa3/semilla/sigilo", methods=["POST"])
@requiere_usuario_capa2
def api_capa3_semilla_sigilo(user_id: int) -> tuple[dict, int]:
    """Sembrar un sigilo de Capa 1 en El Árbol (Capa 3)."""
    from base_datos.bosque import SigiloAportadoRepo, EsferaCapaRepo

    data = request.get_json() or {}
    sigilo_dibujado_id = data.get("sigilo_dibujado_id")
    esfera_tipo = (data.get("esfera_tipo", "") or "").strip().lower()
    esfera_clave = (data.get("esfera_clave", "") or "").strip().lower()
    intencion = (data.get("intencion", "") or "").strip()

    if not isinstance(sigilo_dibujado_id, int):
        return jsonify({"error": "sigilo_dibujado_id requerido"}), 400
    if esfera_tipo not in ESFERA_TIPOS_VALIDOS:
        return jsonify({"error": "esfera_tipo inválido"}), 400
    if not esfera_clave:
        return jsonify({"error": "esfera_clave requerida"}), 400

    # El sigilo debe existir y pertenecer al usuario (privacidad).
    sigilo = SigiloRepo.obtener(sigilo_dibujado_id)
    if not sigilo or sigilo["user_id"] != user_id:
        return jsonify({"error": "Sigilo no encontrado"}), 404

    # La intención por defecto es la del sigilo original (snapshot).
    if not intencion:
        intencion = sigilo["intencion"]
    if len(intencion) > CAPA3_MAX_INTENCION:
        return jsonify({"error": f"Intención > {CAPA3_MAX_INTENCION} chars"}), 400

    esfera_id = EsferaCapaRepo.obtener_o_crear(user_id, esfera_tipo, esfera_clave)
    semilla_id = SigiloAportadoRepo.aportar(
        user_id, sigilo_dibujado_id, esfera_id, intencion
    )
    ExpRepo.agregar_exp(user_id, "arbol", CAPA3_EXP_SEMILLA)

    return jsonify({
        "semilla_id": semilla_id,
        "estado": "germinando",
        "esfera_id": esfera_id,
        "exp_ganada": CAPA3_EXP_SEMILLA,
    }), 201


@app.route("/api/capa3/semillas", methods=["GET"])
@requiere_usuario_capa2
def api_capa3_semillas_listar(user_id: int) -> tuple[dict, int]:
    """Listar semillas del colectivo (anónimas) o de una esfera concreta."""
    from base_datos.bosque import SigiloAportadoRepo

    esfera_id = request.args.get("esfera_id", "").strip()

    if esfera_id.isdigit():
        semillas = SigiloAportadoRepo.listar_por_esfera(int(esfera_id))
    else:
        semillas = SigiloAportadoRepo.listar_anonimos(CAPA3_SEMILLAS_LIMITE)

    return jsonify({"semillas": semillas, "total": len(semillas)}), 200


@app.route("/api/capa3/sync/registrar", methods=["POST"])
@requiere_usuario_capa2
def api_capa3_sync_registrar(user_id: int) -> tuple[dict, int]:
    """Registrar una sincronicidad observada (captura la fase lunar de hoy)."""
    from base_datos.bosque import SincronicidadCapaRepo
    from luna import calcular_fase

    data = request.get_json() or {}
    descripcion = (data.get("descripcion", "") or "").strip()
    categoria = (data.get("categoria", "") or "").strip().lower() or "general"

    if not descripcion:
        return jsonify({"error": "descripcion requerida"}), 400
    if len(descripcion) > CAPA3_MAX_DESCRIPCION:
        return jsonify({"error": f"Descripción > {CAPA3_MAX_DESCRIPCION} chars"}), 400
    if len(categoria) > 50:
        return jsonify({"error": "categoria > 50 chars"}), 400

    fase_lunar = calcular_fase()["clave"]
    sync_id = SincronicidadCapaRepo.registrar(
        user_id, descripcion, categoria, fase_lunar
    )
    ExpRepo.agregar_exp(user_id, "arbol", CAPA3_EXP_SYNC)

    return jsonify({
        "sync_id": sync_id,
        "fase_lunar": fase_lunar,
        "exp_ganada": CAPA3_EXP_SYNC,
    }), 201


@app.route("/api/capa3/sync", methods=["GET"])
@requiere_usuario_capa2
def api_capa3_sync_listar(user_id: int) -> tuple[dict, int]:
    """Listar sincronicidades del colectivo (anónimas), filtrable por fase."""
    from base_datos.bosque import SincronicidadCapaRepo

    fase = request.args.get("fase", "").strip().lower()
    confirmadas = request.args.get("confirmadas", "").strip() == "1"

    if fase:
        syncs = SincronicidadCapaRepo.listar_por_fase(fase, CAPA3_SYNC_LIMITE)
    elif confirmadas:
        syncs = SincronicidadCapaRepo.listar_confirmadas(CAPA3_SYNC_LIMITE)
    else:
        syncs = SincronicidadCapaRepo.listar_recientes(CAPA3_SYNC_LIMITE)

    return jsonify({"sincronicidades": syncs, "total": len(syncs)}), 200


@app.route("/api/capa3/sync/confirmar", methods=["POST"])
@requiere_usuario_capa2
def api_capa3_sync_confirmar(user_id: int) -> tuple[dict, int]:
    """Confirmar una sincronicidad (el colectivo la valida)."""
    from base_datos.bosque import SincronicidadCapaRepo

    data = request.get_json() or {}
    sync_id = data.get("sync_id")

    if not isinstance(sync_id, int):
        return jsonify({"error": "sync_id requerido"}), 400

    sync = SincronicidadCapaRepo.confirmar(sync_id)
    if not sync:
        return jsonify({"error": "Sincronicidad no encontrada"}), 404

    return jsonify({"sincronicidad": sync}), 200


@app.route("/api/capa3/micorriza/conectar", methods=["POST"])
@requiere_usuario_capa2
def api_capa3_micorriza_conectar(user_id: int) -> tuple[dict, int]:
    """Crear conexión ritual (micorriza) entre el mago actual y otro."""
    from base_datos.bosque import MicorrizaRepo

    data = request.get_json() or {}
    otro_mago_id = data.get("otro_mago_id")
    ritual = (data.get("ritual", "") or "").strip()

    if not isinstance(otro_mago_id, int):
        return jsonify({"error": "otro_mago_id requerido"}), 400
    if otro_mago_id == user_id:
        return jsonify({"error": "No puedes conectarte contigo mismo"}), 400
    if not ritual:
        return jsonify({"error": "ritual requerido"}), 400
    if len(ritual) > CAPA3_MAX_RITUAL:
        return jsonify({"error": f"Ritual > {CAPA3_MAX_RITUAL} chars"}), 400

    # El otro mago debe existir (privacidad: no se revela nada de él).
    otro = UsuarioRepo.obtener(otro_mago_id)
    if not otro:
        return jsonify({"error": "Mago no encontrado"}), 404

    # Idempotente: si ya hay conexión activa, no duplicar ni re-otorgar exp.
    existente = MicorrizaRepo.obtener_activa_entre(user_id, otro_mago_id)
    if existente:
        return jsonify({
            "micorriza_id": existente["id"],
            "ya_conectados": True,
            "exp_ganada": 0,
        }), 200

    micorriza_id = MicorrizaRepo.conectar(user_id, otro_mago_id, ritual)
    # El cruce nutre a ambos magos.
    ExpRepo.agregar_exp(user_id, "arbol", CAPA3_EXP_MICORRIZA)
    ExpRepo.agregar_exp(otro_mago_id, "arbol", CAPA3_EXP_MICORRIZA)

    return jsonify({
        "micorriza_id": micorriza_id,
        "ya_conectados": False,
        "exp_ganada": CAPA3_EXP_MICORRIZA,
    }), 201


@app.route("/api/capa3/micorriza", methods=["GET"])
@requiere_usuario_capa2
def api_capa3_micorriza_listar(user_id: int) -> tuple[dict, int]:
    """Listar conexiones activas del mago (nombre del otro, sin datos privados)."""
    from base_datos.bosque import MicorrizaRepo

    activas = MicorrizaRepo.listar_activas(user_id)

    conexiones = []
    for c in activas:
        otro = UsuarioRepo.obtener(c["otro_mago_id"])
        conexiones.append({
            "id": c["id"],
            "otro_mago": otro["nombre_mago"] if otro else "Mago desconocido",
            "ritual": c["ritual"],
            "created_at": c["created_at"],
        })

    return jsonify({"conexiones": conexiones, "total": len(conexiones)}), 200


# ═══════════════════════════════════════════════════════════════════════════
#  BIBLIOTECA COMUNITARIA
# ═══════════════════════════════════════════════════════════════════════════

_MAX_CONTENIDO_BIBLIOTECA = 100_000
_MAX_FUENTE_LEN = 1000
_MAX_CONTRIB_LEN = 20_000


@app.route("/api/biblioteca/dominios", methods=["GET"])
def bib_dominios():
    return jsonify({"dominios": EntradaRepo.listar_dominios()}), 200


@app.route("/api/biblioteca/entradas", methods=["GET"])
def bib_listar():
    dominio = request.args.get("dominio") or None
    estado  = request.args.get("estado") or None
    q       = request.args.get("q") or None
    try:
        limite  = min(int(request.args.get("limite", 50)), 100)
        offset  = max(int(request.args.get("offset", 0)), 0)
    except ValueError:
        return jsonify({"error": "limite/offset deben ser enteros"}), 400

    entradas = EntradaRepo.listar(
        dominio=dominio, estado=estado, q=q,
        limite=limite, offset=offset,
    )
    return jsonify({"entradas": entradas, "total": len(entradas)}), 200


@app.route("/api/biblioteca/entradas/<slug>", methods=["GET"])
def bib_obtener(slug: str):
    entrada = obtener_entrada_completa(slug)
    if not entrada:
        return jsonify({"error": "Entrada no encontrada"}), 404
    return jsonify(entrada), 200


@app.route("/api/biblioteca/entradas", methods=["POST"])
@_limitar_request()
def bib_crear():
    ctx = _contexto()
    if not ctx.activo:
        return jsonify({"error": "Se requiere X-Project-Code para contribuir"}), 401

    data = request.get_json(silent=True) or {}
    error = validar_nueva_entrada(data)
    if error:
        return jsonify({"error": error}), 400

    slug = _slugify(data["titulo"])
    if EntradaRepo.por_slug(slug):
        slug = f"{slug}-{_bib_hash(data['titulo'])[:6]}"

    entrada = EntradaRepo.crear(
        titulo=data["titulo"],
        slug=slug,
        dominio=data["dominio"],
        contenido=data["contenido"],
        hash_autor=ctx.hash,
    )
    return jsonify(entrada), 201


@app.route("/api/biblioteca/entradas/<slug>/fuente", methods=["POST"])
@_limitar_request()
def bib_agregar_fuente(slug: str):
    entrada = EntradaRepo.por_slug(slug)
    if not entrada:
        return jsonify({"error": "Entrada no encontrada"}), 404

    data = request.get_json(silent=True) or {}
    error = validar_fuente(data)
    if error:
        return jsonify({"error": error}), 400

    fuente = FuenteRepo.agregar(
        entrada_id=entrada["id"],
        tipo=data["tipo"],
        referencia=data["referencia"],
    )
    entrada_actualizada = EntradaRepo.por_slug(slug)
    return jsonify({
        "fuente": fuente,
        "estado_entrada": entrada_actualizada["estado"],
    }), 201


@app.route("/api/biblioteca/entradas/<slug>/resonancia", methods=["POST"])
@_limitar_request()
def bib_resonancia(slug: str):
    ctx = _contexto()
    if not ctx.activo:
        return jsonify({"error": "Se requiere X-Project-Code para resonar"}), 401

    entrada = EntradaRepo.por_slug(slug)
    if not entrada:
        return jsonify({"error": "Entrada no encontrada"}), 404

    data = request.get_json(silent=True) or {}
    error = validar_resonancia(data)
    if error:
        return jsonify({"error": error}), 400

    resultado = ResonanciaRepo.marcar(
        entrada_id=entrada["id"],
        tipo=data["tipo"],
        hash_proyecto=ctx.hash,
    )

    # Resonar conocimiento amplifica la esfera de ese dominio en el bosque
    if not resultado.get("ya_marcada"):
        try:
            GestorEsferas.marcar(
                "conocimiento", entrada["dominio"],
                {"entrada": slug, "resonancia": data["tipo"]},
                ctx.hash,
            )
        except Exception:
            pass

    return jsonify(resultado), 200


@app.route("/api/biblioteca/entradas/<slug>/contribuir", methods=["POST"])
@_limitar_request()
def bib_contribuir(slug: str):
    ctx = _contexto()
    if not ctx.activo:
        return jsonify({"error": "Se requiere X-Project-Code para contribuir"}), 401

    entrada = EntradaRepo.por_slug(slug)
    if not entrada:
        return jsonify({"error": "Entrada no encontrada"}), 404

    data = request.get_json(silent=True) or {}
    error = validar_contribucion(data)
    if error:
        return jsonify({"error": error}), 400

    contrib = ContribucionRepo.proponer(
        entrada_id=entrada["id"],
        tipo=data["tipo"],
        contenido=data["contenido"],
        hash_autor=ctx.hash,
    )
    return jsonify(contrib), 201


@app.route("/api/biblioteca/entradas/<slug>/contribuciones", methods=["GET"])
def bib_contribuciones(slug: str):
    entrada = EntradaRepo.por_slug(slug)
    if not entrada:
        return jsonify({"error": "Entrada no encontrada"}), 404
    pendientes = ContribucionRepo.listar_pendientes(entrada["id"])
    return jsonify({"contribuciones": pendientes}), 200


# ═══════════════════════════════════════════════════════════════════════════
#  ARTEMISA — MAPA PLANETARIO
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/artemisa/mapa-planetario", methods=["GET"])
def artemisa_mapa_planetario():
    """Skill especial de Artemisa: superpone esferas geo del bosque con
    correspondencias chakra/sephiroth para producir un mapa del mundo vivo."""
    try:
        from grimorio_base import CHAKRAS, CHAKRAS_ARTEMISA_SOCIAL, ARBOL_VIDA_SEPHIROTH
    except ImportError:
        return jsonify({"error": "grimorio_base no disponible"}), 500

    # Chakras como niveles del planeta (Cuerpo / Alma / Espíritu)
    cuerpo_planetario = {}
    for n, c in CHAKRAS.items():
        cuerpo_planetario[str(n)] = {
            "chakra": c["nombre"],
            "ubicacion": c["ubicacion"],
            "dominio_individual": c["dominio"],
            "dominio_planetario": CHAKRAS_ARTEMISA_SOCIAL.get(n, ""),
            "capa": "cuerpo" if n <= 3 else ("alma" if n <= 5 else "espiritu"),
        }

    # Sephiroth superpuestos sobre el cuerpo planetario
    arbol_planetario = {}
    for n, s in ARBOL_VIDA_SEPHIROTH.items():
        arbol_planetario[str(n)] = {
            "sephira": s["nombre"],
            "significado": s["significado"],
        }

    # Esferas geo activas del bosque (el pulso físico del planeta)
    try:
        geo_esferas = GestorEsferas.listar_activas(tipo="geo", amplitud_min=0.1)
        geo_esferas_sorted = sorted(geo_esferas, key=lambda x: -x.get("amplitud_actual", 0))
    except Exception:
        geo_esferas_sorted = []

    # Esferas de intención y sincronicidad (Alma del planeta)
    try:
        alma_esferas = []
        for tipo_alma in ("intencion", "sincronicidad"):
            alma_esferas += GestorEsferas.listar_activas(tipo=tipo_alma, amplitud_min=0.1)
        alma_esferas = sorted(alma_esferas, key=lambda x: -x.get("amplitud_actual", 0))[:10]
    except Exception:
        alma_esferas = []

    # Entradas de conocimiento verificado (Espíritu del planeta)
    try:
        from base_datos.biblioteca import EntradaRepo as _BibRepo
        espiritu_entradas = _BibRepo.listar(dominio="artemisa_energia_planetaria", limite=10)
        espiritu_entradas += _BibRepo.listar(dominio="cuerpo_energetico", limite=5)
        espiritu_entradas = sorted(espiritu_entradas, key=lambda x: -x.get("resonancia", 0))[:8]
    except Exception:
        espiritu_entradas = []

    return jsonify({
        "cuerpo_planetario": cuerpo_planetario,
        "arbol_planetario": arbol_planetario,
        "pulso": {
            "cuerpo": geo_esferas_sorted,
            "alma": alma_esferas,
            "espiritu": [
                {"slug": e["slug"], "titulo": e["titulo"],
                 "estado": e["estado"], "resonancia": e.get("resonancia", 0)}
                for e in espiritu_entradas
            ],
        },
        "interpretacion": (
            "Cuerpo = ecorregiones activas (chakras 1-3). "
            "Alma = intenciones y sincronicidades colectivas (chakras 4-5). "
            "Espíritu = conocimiento verificado en la biblioteca (chakras 6-7)."
        ),
        "guardiana": "artemisa",
    }), 200


# ═══════════════════════════════════════════════════════════════════════════
#  PROYECTO — ESTADO UNIFICADO
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/proyecto/estado", methods=["GET"])
def proyecto_estado():
    """Estado unificado de un proyecto: esferas, servitors, syncs,
    última consulta y entradas de biblioteca relacionadas."""
    ctx = _contexto()
    if not ctx.activo:
        return jsonify({"error": "Proyecto requerido"}), 401

    resultado: dict = {"proyecto": True}

    # Esferas marcadas por este proyecto
    try:
        from base_datos.esferas import EsferaRepo
        marcas = EsferaRepo.marcas_por_proyecto(ctx.hash)
        resultado["esferas_proyecto"] = marcas
    except Exception:
        resultado["esferas_proyecto"] = []

    # Top esferas colectivas para contexto
    try:
        todas = GestorEsferas.listar_activas(amplitud_min=1.0)
        resultado["esferas_colectivas_top"] = sorted(
            todas, key=lambda x: -x.get("amplitud_actual", 0)
        )[:5]
    except Exception:
        resultado["esferas_colectivas_top"] = []

    # Servitors activos de este proyecto
    try:
        from base_datos.practicas import ServitorRepo as _ServRepo
        resultado["servitors"] = _ServRepo.listar(ctx.hash)
    except Exception:
        resultado["servitors"] = []

    # Syncs recientes de este proyecto
    try:
        from base_datos.practicas import SyncRepo as _SyncRepo
        resultado["syncs"] = _SyncRepo.listar(ctx.hash)[:5]
    except Exception:
        resultado["syncs"] = []

    # Última conversación (timestamp de último mensaje)
    try:
        from base_datos.proyecto import ConversacionRepo
        ultima = ConversacionRepo.ultima_actividad(ctx.hash)
        resultado["ultima_consulta"] = ultima
    except Exception:
        resultado["ultima_consulta"] = None

    # Entradas biblioteca creadas o resonadas por este proyecto
    try:
        from base_datos.biblioteca import EntradaRepo as _BibRepo, ResonanciaRepo as _ResRepo
        creadas = _BibRepo.listar(hash_autor=ctx.hash, limite=10)
        resonadas = _ResRepo.por_proyecto(ctx.hash)
        resultado["biblioteca"] = {
            "creadas": [{"slug": e["slug"], "titulo": e["titulo"], "estado": e["estado"]}
                        for e in creadas],
            "resonadas": resonadas,
        }
    except Exception:
        resultado["biblioteca"] = {"creadas": [], "resonadas": []}

    return jsonify(resultado), 200


# ═══════════════════════════════════════════════════════════════════════════
#  VERIFICAR GROQ
# ═══════════════════════════════════════════════════════════════════════════

def _verificar_groq():
    return invocador.cliente_ia.verificar()




# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print()
    print("=" * 55)
    print("  KALINABIS - Servidor con Groq API")
    print("=" * 55)
    print()

    ok, msg = _verificar_groq()
    if ok:
        print(f"  [OK] {msg}")
    else:
        print(f"  [!] {msg}")
        print("  El servidor arrancara pero las invocaciones no funcionaran")
        print("  hasta que configures GROQ_API_KEY en el entorno.")
        print()
    print("  Abre en tu navegador:")
    print("  -> http://localhost:5000")
    print()
    print("  Nuevas rutas:")
    print("  -> POST /api/proyecto/nuevo     - crear proyecto")
    print("  -> GET  /api/esferas            - esferas activas")
    print("  -> GET  /api/bosque/mapa        - grafo vivo del bosque")
    print("  -> GET  /api/bosque/salud       - metricas de salud")
    print("  -> POST /api/bosque/ciclo       - ejecutar decaimiento")
    print()
    print("  Header requerido: X-Project-Code")
    print("  Para detener: Ctrl+C")
    print()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
