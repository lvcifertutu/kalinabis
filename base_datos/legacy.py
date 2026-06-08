"""Repos y funciones de las tablas legacy (pre-proyecto, modo anónimo).

Estas tablas existen desde la v1 del sistema y conviven con los Repos
por-proyecto de las capas 2/3. Se mantienen para el flujo sin X-Project-Code.
"""

from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


def _crear_tablas(cur, pk: str):
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


# ── Conversación legacy ────────────────────────────────────────────────────

class ConversacionLegadoRepo:
    TABLA = "conversaciones"

    @classmethod
    def guardar(cls, entidad: str, rol: str, contenido: str,
                estado: str = None):
        p = _ph(5)
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(entidad, rol, contenido, estado, timestamp) VALUES ({p})",
                (entidad, rol, contenido, estado, datetime.now().isoformat())
            )

    @classmethod
    def cargar(cls, entidad: str) -> list:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT rol, contenido FROM {cls.TABLA} "
                f"WHERE entidad = {p} ORDER BY id ASC",
                (entidad,)
            )
            return [{"role": r, "content": c} for r, c in cur.fetchall()]

    @classmethod
    def limpiar(cls, entidad: str) -> int:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT COUNT(*) FROM {cls.TABLA} WHERE entidad = {p}",
                (entidad,)
            )
            total = cur.fetchone()[0]
            cur.execute(
                f"DELETE FROM {cls.TABLA} WHERE entidad = {p}",
                (entidad,)
            )
        return total // 2


# ── Decisiones ─────────────────────────────────────────────────────────────

class DecisionRepo:
    TABLA = "decisiones"

    @classmethod
    def guardar(cls, mensaje: str, entidad: str, estado: str,
                modo: str, razon: str):
        p = _ph(6)
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(mensaje_original, entidad_elegida, estado_realidad, "
                f"modo, razon, timestamp) VALUES ({p})",
                (mensaje, entidad, estado, modo, razon,
                 datetime.now().isoformat())
            )

    @classmethod
    def historial(cls, limite: int = 10) -> list:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT timestamp, entidad_elegida, modo, razon, "
                f"mensaje_original FROM {cls.TABLA} "
                f"ORDER BY id DESC LIMIT {p}",
                (limite,)
            )
            return [
                {"timestamp": r[0], "entidad": r[1], "modo": r[2],
                 "razon": r[3], "mensaje_original": r[4]}
                for r in cur.fetchall()
            ]


# ── Grimorio legacy ────────────────────────────────────────────────────────

class GrimorioLegadoRepo:
    TABLA = "grimorio"

    @classmethod
    def escribir(cls, titulo: str, contenido: str,
                 entidad: str = None, tipo: str = "entrada"):
        p = _ph(5)
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(titulo, contenido, entidad, tipo, timestamp) VALUES ({p})",
                (titulo, contenido, entidad, tipo, datetime.now().isoformat())
            )

    @classmethod
    def leer(cls, entidad: str = None, tipo: str = None,
             limite: int = 20) -> list:
        with _conexion() as (con, cur):
            if entidad and tipo:
                cur.execute(
                    f"SELECT timestamp, titulo, contenido, entidad, tipo "
                    f"FROM {cls.TABLA} WHERE entidad={_ph(1)} AND tipo={_ph(1)} "
                    f"ORDER BY id DESC LIMIT {_ph(1)}",
                    (entidad, tipo, limite)
                )
            elif entidad:
                cur.execute(
                    f"SELECT timestamp, titulo, contenido, entidad, tipo "
                    f"FROM {cls.TABLA} WHERE entidad={_ph(1)} "
                    f"ORDER BY id DESC LIMIT {_ph(1)}",
                    (entidad, limite)
                )
            else:
                cur.execute(
                    f"SELECT timestamp, titulo, contenido, entidad, tipo "
                    f"FROM {cls.TABLA} ORDER BY id DESC LIMIT {_ph(1)}",
                    (limite,)
                )
            return [
                {"timestamp": r[0], "titulo": r[1], "contenido": r[2],
                 "entidad": r[3], "tipo": r[4]}
                for r in cur.fetchall()
            ]


# ── Estado del alma ────────────────────────────────────────────────────────

class EstadoAlmaRepo:
    TABLA = "estado_alma"

    @classmethod
    def guardar(cls, chakra: int = None, sephirah: str = None,
                qliphah: str = None, notas: str = None):
        p = _ph(5)
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(chakra_activo, sephirah, qliphah, notas, timestamp) "
                f"VALUES ({p})",
                (chakra, sephirah, qliphah, notas, datetime.now().isoformat())
            )

    @classmethod
    def ultimo(cls) -> dict:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT chakra_activo, sephirah, qliphah, notas, timestamp "
                f"FROM {cls.TABLA} ORDER BY id DESC LIMIT 1"
            )
            row = cur.fetchone()
        if not row:
            return {"chakra": None, "sephirah": None, "qliphah": None,
                    "notas": None, "timestamp": None}
        return {"chakra": row[0], "sephirah": row[1], "qliphah": row[2],
                "notas": row[3], "timestamp": row[4]}


# ── Sigilos legacy ─────────────────────────────────────────────────────────

class SigiloLegadoRepo:
    TABLA = "sigilos"

    @classmethod
    def guardar(cls, intencion: str, imagen: str, entidad: str = None,
                origen: str = "practicante") -> int:
        p = _ph(6)
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(intencion, imagen, entidad, cargado, origen, timestamp) "
                f"VALUES ({p})",
                (intencion, imagen, entidad, 0, origen, datetime.now().isoformat())
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def listar(cls, limite: int = 50) -> list:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, intencion, imagen, entidad, cargado, origen, timestamp "
                f"FROM {cls.TABLA} ORDER BY id DESC LIMIT {_ph(1)}",
                (limite,)
            )
            return [
                {"id": r[0], "intencion": r[1], "imagen": r[2], "entidad": r[3],
                 "cargado": bool(r[4]), "origen": r[5], "timestamp": r[6]}
                for r in cur.fetchall()
            ]

    @classmethod
    def cargar(cls, sigilo_id: int):
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET cargado = 1 WHERE id = {p}",
                (sigilo_id,)
            )

    @classmethod
    def quemar(cls, sigilo_id: int):
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM {cls.TABLA} WHERE id = {p}",
                (sigilo_id,)
            )


# ── Carta natal legacy ─────────────────────────────────────────────────────

class CartaNatalRepo:
    TABLA = "carta_natal"

    @classmethod
    def guardar(cls, nombre, anio, mes, dia, hora, minuto,
                lugar, lat, lng, tz, datos_json):
        with _conexion() as (con, cur):
            cur.execute(f"DELETE FROM {cls.TABLA}")
            p = _ph(12)
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(nombre, anio, mes, dia, hora, minuto, lugar, lat, lng, tz, datos, timestamp) "
                f"VALUES ({p})",
                (nombre, anio, mes, dia, hora, minuto, lugar, lat, lng, tz,
                 datos_json, datetime.now().isoformat())
            )

    @classmethod
    def leer(cls) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT nombre, anio, mes, dia, hora, minuto, lugar, lat, lng, tz, datos "
                f"FROM {cls.TABLA} ORDER BY id DESC LIMIT 1"
            )
            row = cur.fetchone()
        if not row:
            return None
        return {
            "nombre": row[0], "anio": row[1], "mes": row[2], "dia": row[3],
            "hora": row[4], "minuto": row[5], "lugar": row[6],
            "lat": row[7], "lng": row[8], "tz": row[9], "datos": row[10],
        }


# ── Estadísticas cross-tabla ───────────────────────────────────────────────

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
