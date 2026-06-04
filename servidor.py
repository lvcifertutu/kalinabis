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
from typing import Optional
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

from grimorio_base import (
    DEIDADES, TUTU_SYSTEM, ARBOLES_DEIDADES,
    INVOCACIONES_DIRECTAS, sembrar_memoria_artemisa,
    CHAKRAS, ARBOL_VIDA_SEPHIROTH, ARBOL_MUERTE_QLIPHOTH,
    CHAKRAS_ARTEMISA_SOCIAL, RUEDA_COLORES, RUEDA_COMO_CONTEXTO,
)
from base_datos import (
    inicializar_db, guardar_decision, escribir_grimorio, leer_grimorio,
    historial_decisiones, estadisticas,
    guardar_sigilo, leer_sigilos, cargar_sigilo, quemar_sigilo,
    guardar_carta_natal, leer_carta_natal,
    ProyectoRepo, ConversacionRepo, EsferaRepo,
)
from luna import luna_hoy, luna_como_contexto
from tarot import ARCANOS, POSICIONES, carta_por_n, tirada_como_contexto
from astral import (
    CIUDADES, calcular_carta_natal, carta_natal_como_contexto, KERYKEION_OK
)

# ── Inicializar ────────────────────────────────────────────────────────────
inicializar_db()
sembrado = sembrar_memoria_artemisa()
if sembrado:
    print("  · Memoria de Artemisa sembrada")

errores_config = Config.verificar()
for err in errores_config:
    print(f"  [!] {err}")


# ═══════════════════════════════════════════════════════════════════════════
#  CLIENTE GROQ
# ═══════════════════════════════════════════════════════════════════════════

class ClienteGroq:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self._client = None

    def _inicializar(self):
        if self._client is None and self.api_key:
            try:
                from groq import Groq
                self._client = Groq(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "Se necesita 'groq'. "
                    "Ejecutá: pip install groq"
                )

    def chat(self, system: str, messages: list,
             max_tokens: int | None = None,
             temperature: float | None = None) -> str:
        if not self.api_key:
            return ("[Modo offline] No hay GROQ_API_KEY configurada. "
                    "El servidor necesita una key de Groq para responder.")

        self._inicializar()
        max_tok = max_tokens or Config.GROQ_MAX_TOKENS
        temp = temperature if temperature is not None else Config.GROQ_TEMPERATURE

        msgs = [{"role": "system", "content": system}]
        for m in messages:
            role = "assistant" if m.get("role") == "assistant" else "user"
            msgs.append({"role": role, "content": m.get("content", "")})

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=msgs,
                max_tokens=max_tok,
                temperature=temp,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error Groq: {e}]"


groq_client = ClienteGroq()


# ═══════════════════════════════════════════════════════════════════════════
#  HELPER — PROYECTO DESDE HEADER
# ═══════════════════════════════════════════════════════════════════════════

PROYECTO_HEADER = "X-Project-Code"


def _obtener_proyecto() -> Optional[Proyecto]:
    codigo = request.headers.get(PROYECTO_HEADER)
    if not codigo:
        return None
    proyecto = Proyecto(codigo=codigo)
    if not ProyectoRepo.existe(proyecto.hash):
        return None
    return proyecto


def _proyecto_requerido(proyecto: Optional[Proyecto]):
    if not proyecto:
        return jsonify({
            "error": f"Header {PROYECTO_HEADER} requerido o código inválido"
        }), 401
    ProyectoRepo.actualizar_actividad(proyecto.hash)


# ═══════════════════════════════════════════════════════════════════════════
#  RUTAS HTML
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
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
    proyecto = _obtener_proyecto()
    if not proyecto:
        return jsonify({"existe": False})

    cifrado = ProyectoRepo.obtener_metadatos(proyecto.hash)
    if not cifrado:
        return jsonify({"existe": False})

    descifrado = Cifrador.descifrar(cifrado, proyecto.codigo)
    if not descifrado:
        return jsonify({"existe": False, "error": "código incorrecto"})

    metadatos = json.loads(descifrado)
    return jsonify({
        "existe": True,
        "hash": proyecto.hash[:12],
        "metadatos": metadatos,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  API — INVOCACIÓN
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/api/consultar", methods=["POST"])
@_limitar_request()
def consultar():
    proyecto = _obtener_proyecto()
    err = _proyecto_requerido(proyecto)
    if err:
        return err

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
    system = """Lee el mensaje del practicante y decide qué entidad debe responder.

Entidades:
- isis     → libertad, amor materno, pureza, vínculo herido
- afrodita → claridad mental, calma, estados de conciencia, paz
- lilith   → cambio urgente, tormenta, energía reprimida, pasión
- artemisa → enraizarse, ancestros, naturaleza, colectivo, abundancia
- tutu     → propósito, cuestionamiento interior, paradojas

Responde SOLO con este JSON exacto, sin explicaciones ni markdown:
{"deidad": "nombre", "estado": "cuerpo", "razon": "frase breve"}"""

    texto = groq_client.chat(system, [{"role": "user", "content": mensaje}],
                             max_tokens=64)

    try:
        inicio = texto.find("{")
        fin = texto.rfind("}") + 1
        if inicio >= 0 and fin > inicio:
            d = json.loads(texto[inicio:fin])
            return d.get("deidad", "tutu"), d.get("estado", "cuerpo"), \
                   d.get("razon", "")
    except Exception:
        pass
    return "tutu", "alma", "decisión interna"


def _invocar_deidad(nombre: str, mensaje: str, proyecto: Proyecto) -> str:
    if nombre not in DEIDADES:
        return f"Entidad desconocida: {nombre}"

    memoria = ConversacionRepo.cargar(proyecto.hash, nombre)
    ConversacionRepo.guardar(proyecto.hash, nombre, "user", mensaje)
    memoria.append({"role": "user", "content": mensaje})

    system = (DEIDADES[nombre]["system_prompt"]
              + luna_como_contexto() + RUEDA_COMO_CONTEXTO)

    try:
        carta_cifrada = ProyectoRepo.obtener_carta_natal(proyecto.hash)
        if carta_cifrada:
            datos_carta = Cifrador.descifrar(carta_cifrada, proyecto.codigo)
            if datos_carta:
                system += carta_natal_como_contexto(json.loads(datos_carta))
    except Exception:
        pass

    texto = groq_client.chat(system=system, messages=memoria, max_tokens=1024)
    ConversacionRepo.guardar(proyecto.hash, nombre, "assistant", texto)
    return texto


def _invocar_tutu(mensaje: str, proyecto: Proyecto) -> str:
    memoria = ConversacionRepo.cargar(proyecto.hash, "tutu")
    ConversacionRepo.guardar(proyecto.hash, "tutu", "user", mensaje)
    memoria.append({"role": "user", "content": mensaje})

    system = TUTU_SYSTEM + luna_como_contexto() + RUEDA_COMO_CONTEXTO
    texto = groq_client.chat(system=system, messages=memoria, max_tokens=1024)
    ConversacionRepo.guardar(proyecto.hash, "tutu", "assistant", texto)
    return texto


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
    proyecto = _obtener_proyecto()
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
            proyecto_hash=proyecto.hash if proyecto else None,
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
    proyecto = _obtener_proyecto()

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

    if proyecto:
        cifrado = Cifrador.cifrar(
            json.dumps(carta), proyecto.codigo
        )
        ProyectoRepo.guardar_carta_natal(
            proyecto.hash, cifrado,
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
    proyecto = _obtener_proyecto()

    if proyecto:
        cifrado = ProyectoRepo.obtener_carta_natal(proyecto.hash)
        if not cifrado:
            return jsonify({"existe": False})
        datos_str = Cifrador.descifrar(cifrado, proyecto.codigo)
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
    proyecto = _obtener_proyecto()
    entidad = entidad.lower()
    d = request.json
    if not isinstance(d, dict):
        return jsonify({"error": "JSON inválido"}), 400
    cartas = d.get("cartas", [])
    if not isinstance(cartas, list) or len(cartas) > 10:
        return jsonify({"error": "cartas debe ser lista de máx 10"}), 400

    if entidad == "tutu":
        system = TUTU_SYSTEM
    elif entidad in DEIDADES:
        system = DEIDADES[entidad]["system_prompt"]
    else:
        return jsonify({"error": "entidad desconocida"}), 400

    contexto = tirada_como_contexto(cartas)
    system += luna_como_contexto()

    if proyecto:
        try:
            carta_cifrada = ProyectoRepo.obtener_carta_natal(proyecto.hash)
            if carta_cifrada:
                datos_str = Cifrador.descifrar(carta_cifrada, proyecto.codigo)
                if datos_str:
                    system += carta_natal_como_contexto(json.loads(datos_str))
        except Exception:
            pass
    else:
        carta = leer_carta_natal()
        if carta and carta.get("datos"):
            try:
                datos = json.loads(carta["datos"])
                system += carta_natal_como_contexto(datos)
            except Exception:
                pass

    system += (
        "\n\nEl consultante ha extendido una tirada de tres cartas ante ti. "
        "Lee la tirada completa desde tu naturaleza — une el pasado, el presente "
        "y el futuro en una sola voz. Considera la luna de hoy y, si la conoces, "
        "su carta natal. Habla con profundidad pero sin exceder un párrafo o dos."
    )

    prompt = f"{contexto}\n\nLee mi tirada."
    respuesta = groq_client.chat(system=system,
                                 messages=[{"role": "user", "content": prompt}],
                                 max_tokens=700)

    if proyecto:
        ConversacionRepo.guardar(proyecto.hash, entidad, "user",
                                 "[Tirada de tarot]")
        ConversacionRepo.guardar(proyecto.hash, entidad, "assistant",
                                 respuesta)
    else:
        from base_datos import guardar_mensaje
        guardar_mensaje(entidad, "user", "[Tirada de tarot]")
        guardar_mensaje(entidad, "assistant", respuesta)

    return jsonify({"respuesta": respuesta, "entidad": entidad})


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
    proyecto = _obtener_proyecto()
    entidad = entidad.lower()

    if proyecto:
        memoria = ConversacionRepo.cargar(proyecto.hash, entidad)
        return jsonify(memoria[-12:])

    from base_datos import cargar_memoria as cargar_memoria_legacy
    memoria = cargar_memoria_legacy(entidad)
    return jsonify(memoria[-12:])


@app.route("/api/cerrar/<entidad>", methods=["POST"])
def cerrar_ritual(entidad):
    proyecto = _obtener_proyecto()
    entidad = entidad.lower()

    if proyecto:
        n = ConversacionRepo.limpiar(proyecto.hash, entidad)
        return jsonify({"ok": True, "intercambios": n})

    from base_datos import limpiar_memoria as limpiar_memoria_legacy
    n = limpiar_memoria_legacy(entidad)
    return jsonify({"ok": True, "intercambios": n})


@app.route("/api/mensajes/quemar", methods=["POST"])
@_limitar_request()
def quemar_mensaje():
    proyecto = _obtener_proyecto()
    if not proyecto:
        return jsonify({"error": "proyecto requerido"}), 401
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "JSON inválido"}), 400
    msg_id = data.get("id")
    if not isinstance(msg_id, int):
        return jsonify({"error": "id debe ser entero"}), 400
    ok = ConversacionRepo.eliminar_mensaje(proyecto.hash, msg_id)
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
    proyecto = _obtener_proyecto()
    entidad = entidad.lower()

    if proyecto:
        memoria = ConversacionRepo.cargar(proyecto.hash, entidad)
    else:
        from base_datos import cargar_memoria as cargar_memoria_legacy
        memoria = cargar_memoria_legacy(entidad)

    contexto = ""
    if memoria:
        ultimos = memoria[-6:]
        contexto = "\n".join(
            f"{'Practicante' if m['role']=='user' else entidad.capitalize()}: "
            f"{m['content'][:200]}"
            for m in ultimos
        )

    if entidad == "tutu":
        system = TUTU_SYSTEM
    elif entidad in DEIDADES:
        system = DEIDADES[entidad]["system_prompt"]
    else:
        return jsonify({"error": "entidad desconocida"}), 400

    system += luna_como_contexto()
    system += (
        "\n\nEl practicante te pide un sigilo. Basándote en lo que han hablado, "
        "regálale una intención breve y poderosa (máximo 8 palabras) que capture "
        "lo que su alma necesita ahora. Responde SOLO con la intención en mayúsculas, "
        "sin comillas ni explicación. Ejemplo: VEO CON CLARIDAD MI CAMINO"
    )

    prompt = (f"Conversación reciente:\n{contexto}\n\nDame la intención del sigilo."
              if contexto else
              "Dame una intención de sigilo para quien apenas llega.")

    intencion = groq_client.chat(
        system=system,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=40,
    )
    intencion = intencion.strip().strip('"').strip("'").upper()
    intencion = intencion.split("\n")[0][:60]

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
#  VERIFICAR GROQ
# ═══════════════════════════════════════════════════════════════════════════

def _verificar_groq():
    if not Config.GROQ_API_KEY:
        return False, "GROQ_API_KEY no configurada"
    try:
        groq_client._inicializar()
        return True, f"API key configurada · modelo: {Config.GROQ_MODEL}"
    except Exception as e:
        return False, str(e)


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
