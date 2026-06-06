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

from flask import Flask, request, jsonify, send_from_directory

from config import Config
from proyectos import GeneradorCodigos, Cifrador, Proyecto
from esferas import GestorEsferas
from geografia import GestorGeografico

BASE_DIR = Path(__file__).parent

app = Flask(__name__, static_folder=str(BASE_DIR))
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB max por request


# ═══════════════════════════════════════════════════════════════════════════
#  CORS (para el terminal CRT en modo dev: localhost:7777)
# ═══════════════════════════════════════════════════════════════════════════

@app.after_request
def _add_cors(response):
    origin = request.headers.get("Origin", "")
    if origin in ("http://localhost:7777", "http://127.0.0.1:7777"):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Project-Code"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/api/<path:path>", methods=["OPTIONS"])
def _cors_preflight(path):
    origin = request.headers.get("Origin", "")
    resp = app.make_response("")
    resp.headers["Access-Control-Allow-Origin"] = origin
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Project-Code"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp, 204


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
from base_datos import (
    inicializar_db, guardar_decision, escribir_grimorio, leer_grimorio,
    historial_decisiones, estadisticas,
    guardar_sigilo, leer_sigilos, cargar_sigilo, quemar_sigilo,
    guardar_carta_natal, leer_carta_natal,
    ProyectoRepo, ConversacionRepo, EsferaRepo, ServitorRepo,
    SyncRepo, ParadigmaRepo,
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

@app.route("/api/consultar", methods=["POST"])
@_limitar_request()
def consultar():
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
    else:
        razon = "invocación directa del practicante"
        estado_r = "cuerpo" if entidad != "tutu" else "alma"

    if entidad == "tutu":
        respuesta = _invocar_tutu(mensaje, proyecto)
        estado_r = "alma"
    else:
        respuesta = _invocar_deidad(entidad, mensaje, proyecto)
        estado_r = "cuerpo"

    guardar_decision(mensaje, entidad, estado_r, modo, razon)

    esferas_activadas = GestorEsferas.marcar_por_invocacion(
        entidad=entidad,
        ubicacion=ubicacion,
        concepto=concepto,
        proyecto_hash=proyecto.hash,
    )

    return jsonify({
        "entidad": entidad,
        "estado": estado_r,
        "modo": modo,
        "razon": razon,
        "respuesta": respuesta,
        "esferas_activadas": esferas_activadas,
        "eje_del_mundo": GestorGeografico.eje_del_mundo_para(ubicacion),
    })


def _tutu_decide(mensaje: str):
    return invocador.decidir_entidad(mensaje)


def _invocar_deidad(nombre: str, mensaje: str, proyecto: Proyecto) -> str:
    if nombre not in DEIDADES:
        return f"Entidad desconocida: {nombre}"
    return invocador.invocar_deidad(nombre, mensaje, proyecto).texto


def _invocar_tutu(mensaje: str, proyecto: Proyecto) -> str:
    return invocador.invocar_tutu(mensaje, proyecto).texto


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
    """Clasifica las esferas activas en los 3 estratos del Bosque."""
    esferas = GestorEsferas.listar_activas()

    sotobosque, dosel, emergentes = [], [], []
    for e in esferas:
        a = e["amplitud_actual"]
        if a >= 3.5:
            emergentes.append(e)
        elif a >= 2.0:
            dosel.append(e)
        else:
            sotobosque.append(e)

    elementales = [e for e in esferas if e["tipo"] == "elemental"]
    atm_por_elem: dict[str, float] = {}
    for e in elementales:
        clave = e["clave_unica"]
        atm_por_elem[clave] = atm_por_elem.get(clave, 0) + e["amplitud_actual"]

    ELEM_DEIDAD = {"fuego": "isis", "agua": "lilith", "aire": "afrodita", "tierra": "artemisa"}
    ELEM_ICONO  = {"fuego": "🔥", "agua": "💧", "aire": "💨", "tierra": "🌿"}
    elemento_dominante = max(atm_por_elem, key=atm_por_elem.get) if atm_por_elem else None
    atmosfera = {
        "elemento":  elemento_dominante,
        "deidad":    ELEM_DEIDAD.get(elemento_dominante, "") if elemento_dominante else "",
        "icono":     ELEM_ICONO.get(elemento_dominante, "") if elemento_dominante else "",
        "equilibrio": len(atm_por_elem) >= 3,
    } if atm_por_elem else {"elemento": None, "deidad": "", "icono": "", "equilibrio": False}

    luna = luna_hoy()
    luna_ctx = f"{luna.get('fase', {}).get('emoji', '')} {luna.get('fase', {}).get('nombre', '')}"

    return jsonify({
        "estratos": {
            "emergentes": sorted(emergentes, key=lambda x: -x["amplitud_actual"])[:10],
            "dosel":      sorted(dosel,      key=lambda x: -x["amplitud_actual"])[:15],
            "sotobosque": sorted(sotobosque, key=lambda x: -x["amplitud_actual"])[:20],
        },
        "conteos": {
            "emergentes": len(emergentes),
            "dosel":      len(dosel),
            "sotobosque": len(sotobosque),
        },
        "atmosfera": atmosfera,
        "luna":      luna_ctx,
    })


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
        guardar_carta_natal(
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
        carta = leer_carta_natal()
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
    return jsonify(leer_grimorio(limite=30))


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
    escribir_grimorio(
        titulo=titulo,
        contenido=contenido,
        entidad=d.get("entidad"),
        tipo=d.get("tipo", "entrada"),
    )
    return jsonify({"ok": True})


@app.route("/api/decisiones", methods=["GET"])
def get_decisiones():
    return jsonify(historial_decisiones(limite=15))


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
    return jsonify(leer_sigilos(limite=50))


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
    sid = guardar_sigilo(
        intencion=intencion,
        imagen=imagen,
        entidad=d.get("entidad"),
        origen=d.get("origen", "practicante"),
    )
    return jsonify({"ok": True, "id": sid})


@app.route("/api/sigilo/cargar/<int:sid>", methods=["POST"])
@_limitar_request()
def post_cargar_sigilo(sid):
    cargar_sigilo(sid)
    return jsonify({"ok": True})


@app.route("/api/sigilo/quemar/<int:sid>", methods=["POST"])
@_limitar_request()
def post_quemar_sigilo(sid):
    quemar_sigilo(sid)
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
