# ═══════════════════════════════════════════════════════════════════════════
#  BASE DE DATOS — GRIMORIO PERSISTENTE
#  Dual mode: PostgreSQL en producción (Render) · SQLite en local
#
#  Detección automática:
#    Si existe DATABASE_URL en el entorno → PostgreSQL (Render)
#    Si no → SQLite local (grimorio.db)
#
#  Sin cambios en el resto del código — misma API para ambos.
# ═══════════════════════════════════════════════════════════════════════════

import json
from datetime import datetime

from persistencia import ADAPTADOR, DATABASE_URL, DB_PATH

# El dialecto (SQLite/Postgres) vive en persistencia.py detrás del adapter.
MODO_PG = ADAPTADOR.es_postgres

print(f"[DB] Modo: {'PostgreSQL' if MODO_PG else 'SQLite'}")


# ── Conexión y cursor (delegan en el adapter de persistencia) ───────────────

def _conexion():
    """Context manager (con, cur): commit + close. Lo provee el adapter."""
    return ADAPTADOR.conexion()


def _ph(n: int = 1) -> str:
    """Placeholders de parámetros según el motor (`?` SQLite / `%s` Postgres)."""
    return ADAPTADOR.placeholder(n)


def _serial() -> str:
    """Tipo de columna auto-incremental según el motor."""
    return ADAPTADOR.tipo_serial()


# ── Inicialización ─────────────────────────────────────────────────────────

def inicializar_db():
    """
    Crea todas las tablas si no existen.
    Idempotente — se puede llamar múltiples veces.
    """
    pk = f"{_serial()} PRIMARY KEY"

    with _conexion() as (con, cur):

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS conversaciones (
                id        {pk},
                entidad   TEXT NOT NULL,
                rol       TEXT NOT NULL,
                contenido TEXT NOT NULL,
                estado    TEXT,
                timestamp TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS decisiones (
                id               {pk},
                mensaje_original TEXT NOT NULL,
                entidad_elegida  TEXT NOT NULL,
                estado_realidad  TEXT,
                modo             TEXT NOT NULL,
                razon            TEXT,
                timestamp        TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS grimorio (
                id        {pk},
                titulo    TEXT NOT NULL,
                contenido TEXT NOT NULL,
                entidad   TEXT,
                tipo      TEXT DEFAULT 'entrada',
                timestamp TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS estado_alma (
                id            {pk},
                chakra_activo INTEGER,
                sephirah      TEXT,
                qliphah       TEXT,
                notas         TEXT,
                timestamp     TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS sigilos (
                id        {pk},
                intencion TEXT,
                imagen    TEXT NOT NULL,
                entidad   TEXT,
                cargado   INTEGER DEFAULT 0,
                origen    TEXT DEFAULT 'practicante',
                timestamp TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS carta_natal (
                id        {pk},
                nombre    TEXT,
                anio      INTEGER, mes INTEGER, dia INTEGER,
                hora      INTEGER, minuto INTEGER,
                lugar     TEXT,
                lat       REAL, lng REAL, tz TEXT,
                datos     TEXT,
                timestamp TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS proyectos (
                id                 {pk},
                hash_codigo        TEXT NOT NULL UNIQUE,
                metadatos_cifrados TEXT NOT NULL,
                ultima_actividad   TEXT,
                created_at         TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS carta_natal_proyecto (
                id          {pk},
                hash_codigo TEXT NOT NULL UNIQUE,
                datos_cifrados TEXT NOT NULL,
                nombre      TEXT,
                timestamp   TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS esferas (
                id              {pk},
                tipo            TEXT NOT NULL,
                clave_unica     TEXT NOT NULL,
                metadata_json   TEXT,
                amplitud        REAL NOT NULL DEFAULT 1.0,
                fase_decaimiento TEXT DEFAULT 'activa',
                created_at      TEXT NOT NULL,
                updated_at      TEXT NOT NULL,
                UNIQUE (tipo, clave_unica)
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS marcas_esfera (
                id              {pk},
                tipo_esfera     TEXT NOT NULL,
                clave_esfera    TEXT NOT NULL,
                proyecto_hash   TEXT NOT NULL,
                timestamp       TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS conversaciones_proyecto (
                id            {pk},
                proyecto_hash TEXT NOT NULL,
                entidad       TEXT NOT NULL,
                rol           TEXT NOT NULL,
                contenido     TEXT NOT NULL,
                estado        TEXT,
                timestamp     TEXT NOT NULL
            )
        """)

        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_esferas_tipo
            ON esferas (tipo)
        """)

        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_esferas_clave
            ON esferas (tipo, clave_unica)
        """)

        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_marcas_esfera_tipo
            ON marcas_esfera (tipo_esfera, clave_esfera)
        """)

        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_conversaciones_proyecto
            ON conversaciones_proyecto (proyecto_hash, entidad)
        """)

        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_proyectos_hash
            ON proyectos (hash_codigo)
        """)

# ── CONVERSACIONES ─────────────────────────────────────────────────────────

def guardar_mensaje(entidad: str, rol: str, contenido: str,
                    estado: str = None):
    p = _ph(5)
    with _conexion() as (con, cur):
        cur.execute(
            f"INSERT INTO conversaciones "
            f"(entidad, rol, contenido, estado, timestamp) VALUES ({p})",
            (entidad, rol, contenido, estado, datetime.now().isoformat())
        )


def cargar_memoria(entidad: str) -> list:
    p = _ph(1)
    with _conexion() as (con, cur):
        cur.execute(
            f"SELECT rol, contenido FROM conversaciones "
            f"WHERE entidad = {p} ORDER BY id ASC",
            (entidad,)
        )
        return [{"role": r, "content": c} for r, c in cur.fetchall()]


def limpiar_memoria(entidad: str) -> int:
    p = _ph(1)
    with _conexion() as (con, cur):
        cur.execute(
            f"SELECT COUNT(*) FROM conversaciones WHERE entidad = {p}",
            (entidad,)
        )
        total = cur.fetchone()[0]
        cur.execute(
            f"DELETE FROM conversaciones WHERE entidad = {p}",
            (entidad,)
        )
    return total // 2


# ── DECISIONES ─────────────────────────────────────────────────────────────

def guardar_decision(mensaje: str, entidad: str, estado: str,
                     modo: str, razon: str):
    p = _ph(6)
    with _conexion() as (con, cur):
        cur.execute(
            f"INSERT INTO decisiones "
            f"(mensaje_original, entidad_elegida, estado_realidad, "
            f"modo, razon, timestamp) VALUES ({p})",
            (mensaje, entidad, estado, modo, razon,
             datetime.now().isoformat())
        )


def historial_decisiones(limite: int = 10) -> list:
    p = _ph(1)
    with _conexion() as (con, cur):
        cur.execute(
            f"SELECT timestamp, entidad_elegida, modo, razon, "
            f"mensaje_original FROM decisiones "
            f"ORDER BY id DESC LIMIT {p}",
            (limite,)
        )
        return [
            {"timestamp": r[0], "entidad": r[1], "modo": r[2],
             "razon": r[3], "mensaje_original": r[4]}
            for r in cur.fetchall()
        ]


# ── GRIMORIO PERSONAL ──────────────────────────────────────────────────────

def escribir_grimorio(titulo: str, contenido: str,
                      entidad: str = None, tipo: str = "entrada"):
    p = _ph(5)
    with _conexion() as (con, cur):
        cur.execute(
            f"INSERT INTO grimorio "
            f"(titulo, contenido, entidad, tipo, timestamp) VALUES ({p})",
            (titulo, contenido, entidad, tipo, datetime.now().isoformat())
        )


def leer_grimorio(entidad: str = None, tipo: str = None,
                  limite: int = 20) -> list:
    p1, p2, pl = _ph(1), _ph(2), _ph(1)
    with _conexion() as (con, cur):
        if entidad and tipo:
            cur.execute(
                f"SELECT timestamp, titulo, contenido, entidad, tipo "
                f"FROM grimorio WHERE entidad={_ph(1)} AND tipo={_ph(1)} "
                f"ORDER BY id DESC LIMIT {_ph(1)}",
                (entidad, tipo, limite)
            )
        elif entidad:
            cur.execute(
                f"SELECT timestamp, titulo, contenido, entidad, tipo "
                f"FROM grimorio WHERE entidad={_ph(1)} "
                f"ORDER BY id DESC LIMIT {_ph(1)}",
                (entidad, limite)
            )
        else:
            cur.execute(
                f"SELECT timestamp, titulo, contenido, entidad, tipo "
                f"FROM grimorio ORDER BY id DESC LIMIT {_ph(1)}",
                (limite,)
            )
        return [
            {"timestamp": r[0], "titulo": r[1], "contenido": r[2],
             "entidad": r[3], "tipo": r[4]}
            for r in cur.fetchall()
        ]


# ── ESTADO DEL ALMA ────────────────────────────────────────────────────────

def guardar_estado_alma(chakra: int = None, sephirah: str = None,
                        qliphah: str = None, notas: str = None):
    p = _ph(5)
    with _conexion() as (con, cur):
        cur.execute(
            f"INSERT INTO estado_alma "
            f"(chakra_activo, sephirah, qliphah, notas, timestamp) "
            f"VALUES ({p})",
            (chakra, sephirah, qliphah, notas, datetime.now().isoformat())
        )


def ultimo_estado_alma() -> dict:
    with _conexion() as (con, cur):
        cur.execute(
            "SELECT chakra_activo, sephirah, qliphah, notas, timestamp "
            "FROM estado_alma ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
    if not row:
        return {"chakra": None, "sephirah": None, "qliphah": None,
                "notas": None, "timestamp": None}
    return {"chakra": row[0], "sephirah": row[1], "qliphah": row[2],
            "notas": row[3], "timestamp": row[4]}


# ── ESTADÍSTICAS ───────────────────────────────────────────────────────────

def estadisticas() -> dict:
    with _conexion() as (con, cur):

        cur.execute(
            "SELECT entidad, COUNT(*) FROM conversaciones "
            "GROUP BY entidad ORDER BY COUNT(*) DESC"
        )
        por_entidad = dict(cur.fetchall())

        cur.execute("SELECT COUNT(*) FROM grimorio")
        total_grimorio = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM decisiones")
        total_consultas = cur.fetchone()[0]

        cur.execute(
            "SELECT entidad_elegida, COUNT(*) as n FROM decisiones "
            "GROUP BY entidad_elegida ORDER BY n DESC LIMIT 1"
        )
        row = cur.fetchone()
        mas_invocada = row[0] if row else None

    return {
        "mensajes_por_entidad": por_entidad,
        "entradas_grimorio":    total_grimorio,
        "total_consultas":      total_consultas,
        "entidad_mas_invocada": mas_invocada,
    }


# ── SIGILOS ────────────────────────────────────────────────────────────────

def guardar_sigilo(intencion: str, imagen: str, entidad: str = None,
                   origen: str = "practicante") -> int:
    """Guarda un sigilo. imagen = PNG en base64. Devuelve su id."""
    p = _ph(6)
    with _conexion() as (con, cur):
        cur.execute(
            f"INSERT INTO sigilos "
            f"(intencion, imagen, entidad, cargado, origen, timestamp) "
            f"VALUES ({p})",
            (intencion, imagen, entidad, 0, origen, datetime.now().isoformat())
        )
        # Recuperar el id recién insertado (el adapter sabe cómo)
        return ADAPTADOR.id_ultimo_insertado(cur)


def leer_sigilos(limite: int = 50) -> list:
    """Lista los sigilos guardados, del más reciente al más antiguo."""
    with _conexion() as (con, cur):
        cur.execute(
            f"SELECT id, intencion, imagen, entidad, cargado, origen, timestamp "
            f"FROM sigilos ORDER BY id DESC LIMIT {_ph(1)}",
            (limite,)
        )
        return [
            {"id": r[0], "intencion": r[1], "imagen": r[2], "entidad": r[3],
             "cargado": bool(r[4]), "origen": r[5], "timestamp": r[6]}
            for r in cur.fetchall()
        ]


def cargar_sigilo(sigilo_id: int):
    """Marca un sigilo como cargado (el ritual de cargar y olvidar)."""
    p = _ph(1)
    with _conexion() as (con, cur):
        cur.execute(
            f"UPDATE sigilos SET cargado = 1 WHERE id = {p}",
            (sigilo_id,)
        )


def quemar_sigilo(sigilo_id: int):
    """Elimina permanentemente un sigilo (el ritual de quemar)."""
    p = _ph(1)
    with _conexion() as (con, cur):
        cur.execute(
            f"DELETE FROM sigilos WHERE id = {p}",
            (sigilo_id,)
        )


# ── CARTA NATAL ────────────────────────────────────────────────────────────

def guardar_carta_natal(nombre, anio, mes, dia, hora, minuto,
                        lugar, lat, lng, tz, datos_json):
    """Guarda (o reemplaza) la carta natal del consultante. Solo una activa."""
    with _conexion() as (con, cur):
        cur.execute("DELETE FROM carta_natal")  # solo guardamos una
        p = _ph(12)
        cur.execute(
            f"INSERT INTO carta_natal "
            f"(nombre, anio, mes, dia, hora, minuto, lugar, lat, lng, tz, datos, timestamp) "
            f"VALUES ({p})",
            (nombre, anio, mes, dia, hora, minuto, lugar, lat, lng, tz,
             datos_json, datetime.now().isoformat())
        )


def leer_carta_natal():
    """Devuelve la carta natal guardada o None."""
    with _conexion() as (con, cur):
        cur.execute(
            "SELECT nombre, anio, mes, dia, hora, minuto, lugar, lat, lng, tz, datos "
            "FROM carta_natal ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
    if not row:
        return None
    return {
        "nombre": row[0], "anio": row[1], "mes": row[2], "dia": row[3],
        "hora": row[4], "minuto": row[5], "lugar": row[6],
        "lat": row[7], "lng": row[8], "tz": row[9], "datos": row[10],
    }


# ═══════════════════════════════════════════════════════════════════════════
#  REPOSITORIOS (nueva arquitectura OOP)
# ═══════════════════════════════════════════════════════════════════════════


class ProyectoRepo:
    TABLA = "proyectos"

    @classmethod
    def existe(cls, hash_codigo: str) -> bool:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT 1 FROM {cls.TABLA} WHERE hash_codigo = {p}",
                (hash_codigo,)
            )
            return cur.fetchone() is not None

    @classmethod
    def crear(cls, hash_codigo: str, metadatos_cifrados: str):
        p = _ph(4)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(hash_codigo, metadatos_cifrados, ultima_actividad, created_at) "
                f"VALUES ({p})",
                (hash_codigo, metadatos_cifrados, ahora, ahora)
            )

    @classmethod
    def obtener_metadatos(cls, hash_codigo: str) -> str | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT metadatos_cifrados FROM {cls.TABLA} "
                f"WHERE hash_codigo = {p}",
                (hash_codigo,)
            )
            row = cur.fetchone()
            return row[0] if row else None

    @classmethod
    def actualizar_actividad(cls, hash_codigo: str):
        p = _ph(1)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET ultima_actividad = {_ph(1)} "
                f"WHERE hash_codigo = {_ph(1)}",
                (ahora, hash_codigo)
            )

    @classmethod
    def guardar_carta_natal(cls, hash_codigo: str, datos_cifrados: str,
                            nombre: str = ""):
        p = _ph(4)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO carta_natal_proyecto "
                f"(hash_codigo, datos_cifrados, nombre, timestamp) VALUES ({p}) "
                f"ON CONFLICT (hash_codigo) DO UPDATE SET "
                f"datos_cifrados = excluded.datos_cifrados, "
                f"nombre = excluded.nombre, timestamp = excluded.timestamp",
                (hash_codigo, datos_cifrados, nombre, ahora)
            )

    @classmethod
    def obtener_carta_natal(cls, hash_codigo: str) -> str | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT datos_cifrados FROM carta_natal_proyecto "
                f"WHERE hash_codigo = {p}",
                (hash_codigo,)
            )
            row = cur.fetchone()
            return row[0] if row else None

    @classmethod
    def total_activos(cls, dias_max_inactividad: int = 60) -> int:
        from datetime import timedelta
        limite = (datetime.now() - timedelta(days=dias_max_inactividad)).isoformat()
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT COUNT(*) FROM {cls.TABLA} "
                f"WHERE ultima_actividad >= {p}",
                (limite,)
            )
            return cur.fetchone()[0]


class EsferaRepo:
    TABLA = "esferas"
    TABLA_MARCAS = "marcas_esfera"

    INCREMENTO_MARCA = 0.3
    AMPLITUD_MAX = 5.0

    @classmethod
    def crear_o_actualizar(cls, tipo: str, clave_unica: str,
                           metadata: dict | None = None) -> dict:
        ahora = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else "{}"
        with _conexion() as (con, cur):
            if MODO_PG:
                cur.execute(
                    f"INSERT INTO {cls.TABLA} "
                    f"(tipo, clave_unica, metadata_json, amplitud, "
                    f"fase_decaimiento, created_at, updated_at) "
                    f"VALUES ({_ph(7)}) "
                    f"ON CONFLICT (tipo, clave_unica) DO UPDATE SET "
                    f"amplitud = LEAST({cls.TABLA}.amplitud + %s, %s), "
                    f"fase_decaimiento = 'activa', updated_at = %s",
                    (tipo, clave_unica, metadata_json,
                     cls.INCREMENTO_MARCA, cls.AMPLITUD_MAX,
                     ahora, ahora)
                )
            else:
                existe = cls.obtener(tipo, clave_unica)
                if existe:
                    nueva_amp = min(
                        existe["amplitud"] + cls.INCREMENTO_MARCA,
                        cls.AMPLITUD_MAX
                    )
                    cur.execute(
                        f"UPDATE {cls.TABLA} SET "
                        f"amplitud = {_ph(1)}, fase_decaimiento = 'activa', "
                        f"updated_at = {_ph(1)} "
                        f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                        (nueva_amp, ahora, tipo, clave_unica)
                    )
                else:
                    cur.execute(
                        f"INSERT INTO {cls.TABLA} "
                        f"(tipo, clave_unica, metadata_json, amplitud, "
                        f"fase_decaimiento, created_at, updated_at) "
                        f"VALUES ({_ph(7)})",
                        (tipo, clave_unica, metadata_json, 1.0,
                         "activa", ahora, ahora)
                    )
        # fuera del with — asegura commit antes de la nueva conexión
        return cls.obtener(tipo, clave_unica)

    @classmethod
    def obtener(cls, tipo: str, clave_unica: str) -> dict | None:
        p = _ph(2)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                f"fase_decaimiento, created_at, updated_at "
                f"FROM {cls.TABLA} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica)
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "tipo": row[0],
                "clave_unica": row[1],
                "metadata": json.loads(row[2]) if row[2] else {},
                "amplitud": row[3],
                "fase_decaimiento": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }

    @classmethod
    def listar_activas(cls, tipo: str | None = None,
                       amplitud_minima: float = 0.01) -> list[dict]:
        with _conexion() as (con, cur):
            if tipo:
                cur.execute(
                    f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                    f"fase_decaimiento, created_at, updated_at "
                    f"FROM {cls.TABLA} "
                    f"WHERE tipo = {_ph(1)} AND amplitud >= {_ph(1)} "
                    f"ORDER BY amplitud DESC",
                    (tipo, amplitud_minima)
                )
            else:
                cur.execute(
                    f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                    f"fase_decaimiento, created_at, updated_at "
                    f"FROM {cls.TABLA} "
                    f"WHERE amplitud >= {_ph(1)} "
                    f"ORDER BY amplitud DESC",
                    (amplitud_minima,)
                )
            return [
                {
                    "tipo": r[0],
                    "clave_unica": r[1],
                    "metadata": json.loads(r[2]) if r[2] else {},
                    "amplitud": r[3],
                    "fase_decaimiento": r[4],
                    "created_at": r[5],
                    "updated_at": r[6],
                }
                for r in cur.fetchall()
            ]

    @classmethod
    def agregar_marca(cls, tipo_esfera: str, clave_esfera: str,
                      proyecto_hash: str):
        p = _ph(4)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA_MARCAS} "
                f"(tipo_esfera, clave_esfera, proyecto_hash, timestamp) "
                f"VALUES ({p})",
                (tipo_esfera, clave_esfera, proyecto_hash, ahora)
            )

    @classmethod
    def contar_marcas_recientes(cls, tipo_esfera: str, clave_esfera: str,
                                desde_dias: int = 30) -> int:
        from datetime import timedelta
        limite = (datetime.now() - timedelta(days=desde_dias)).isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT COUNT(DISTINCT proyecto_hash) FROM {cls.TABLA_MARCAS} "
                f"WHERE tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)} "
                f"AND timestamp >= {_ph(1)}",
                (tipo_esfera, clave_esfera, limite)
            )
            return cur.fetchone()[0]

    @classmethod
    def actualizar_fase_decaimiento(cls, tipo: str, clave_unica: str,
                                    nueva_amplitud: float,
                                    nueva_fase: str):
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET "
                f"amplitud = {_ph(1)}, fase_decaimiento = {_ph(1)}, "
                f"updated_at = {_ph(1)} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (nueva_amplitud, nueva_fase, ahora, tipo, clave_unica)
            )

    @classmethod
    def listar_todas(cls) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                f"fase_decaimiento, created_at, updated_at "
                f"FROM {cls.TABLA} ORDER BY updated_at DESC"
            )
            return [
                {
                    "tipo": r[0],
                    "clave_unica": r[1],
                    "metadata": json.loads(r[2]) if r[2] else {},
                    "amplitud": r[3],
                    "fase_decaimiento": r[4],
                    "created_at": r[5],
                    "updated_at": r[6],
                }
                for r in cur.fetchall()
            ]

    @classmethod
    def eliminar(cls, tipo: str, clave_unica: str):
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM {cls.TABLA} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica)
            )
            cur.execute(
                f"DELETE FROM {cls.TABLA_MARCAS} "
                f"WHERE tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)}",
                (tipo, clave_unica)
            )


class ConversacionRepo:
    TABLA = "conversaciones_proyecto"

    @classmethod
    def guardar(cls, proyecto_hash: str, entidad: str, rol: str,
                contenido: str, estado: str = None):
        p = _ph(6)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(proyecto_hash, entidad, rol, contenido, estado, timestamp) "
                f"VALUES ({p})",
                (proyecto_hash, entidad, rol, contenido, estado, ahora)
            )

    @classmethod
    def cargar(cls, proyecto_hash: str, entidad: str,
               limite: int = 50) -> list:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, rol, contenido FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} AND entidad = {_ph(1)} "
                f"ORDER BY id ASC LIMIT {_ph(1)}",
                (proyecto_hash, entidad, limite)
            )
            return [{"id": r[0], "role": r[1], "content": r[2]}
                    for r in cur.fetchall()]

    @classmethod
    def eliminar_mensaje(cls, proyecto_hash: str, mensaje_id: int) -> bool:
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM {cls.TABLA} "
                f"WHERE id = {_ph(1)} AND proyecto_hash = {_ph(1)}",
                (mensaje_id, proyecto_hash)
            )
            return cur.rowcount > 0

    @classmethod
    def limpiar(cls, proyecto_hash: str, entidad: str) -> int:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT COUNT(*) FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} AND entidad = {_ph(1)}",
                (proyecto_hash, entidad)
            )
            total = cur.fetchone()[0]
            cur.execute(
                f"DELETE FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} AND entidad = {_ph(1)}",
                (proyecto_hash, entidad)
            )
            return total // 2

    @classmethod
    def contar_por_proyecto(cls, proyecto_hash: str,
                            desde_dias: int | None = None) -> dict:
        with _conexion() as (con, cur):
            if desde_dias:
                from datetime import timedelta
                limite = (datetime.now() -
                          timedelta(days=desde_dias)).isoformat()
                cur.execute(
                    f"SELECT entidad, COUNT(*) FROM {cls.TABLA} "
                    f"WHERE proyecto_hash = {_ph(1)} "
                    f"AND timestamp >= {_ph(1)} "
                    f"GROUP BY entidad ORDER BY COUNT(*) DESC",
                    (proyecto_hash, limite)
                )
            else:
                cur.execute(
                    f"SELECT entidad, COUNT(*) FROM {cls.TABLA} "
                    f"WHERE proyecto_hash = {_ph(1)} "
                    f"GROUP BY entidad ORDER BY COUNT(*) DESC",
                    (proyecto_hash,)
                )
            return dict(cur.fetchall())

    @classmethod
    def total_mensajes(cls) -> int:
        with _conexion() as (con, cur):
            cur.execute(f"SELECT COUNT(*) FROM {cls.TABLA}")
            return cur.fetchone()[0]


# ── TEST LOCAL ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    inicializar_db()
    modo = "PostgreSQL" if MODO_PG else "SQLite"
    print(f"Base de datos inicializada · Modo: {modo}")
    if not MODO_PG:
        print(f"Archivo: {DB_PATH}")
