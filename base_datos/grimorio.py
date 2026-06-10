"""Repos del Grimorio personal.

Capa 1 — El Grimorio personal: entradas y sigilos dibujados (legacy).
Capa 2 — EsferaGrimorio: configuración cosmológica personal del mago por esfera.
"""

from datetime import datetime

from base_datos._helpers import _conexion, _ph, _serial, ADAPTADOR

# ─── Atributos RPG disponibles ────────────────────────────────────────────────

ARQUETIPOS = {"guerrero", "mago", "sanador", "sacerdotisa", "trickster", "buscador"}
ELEMENTOS   = {"fuego", "agua", "aire", "tierra", "eter"}
CHAKRAS_VALIDOS = {
    "raiz", "sacro", "plexo_solar", "corazon",
    "garganta", "tercer_ojo", "corona",
}
SEPHIROTH_VALIDOS = {
    "malkuth", "yesod", "hod", "netzach", "tiferet",
    "geburah", "chesed", "binah", "hokhmah", "keter",
}


def _crear_tablas(cur, pk: str):
    # ── Legacy ──────────────────────────────────────────────────────────────
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS grimorio_entradas (
            id              {pk},
            user_id         INTEGER NOT NULL,
            titulo          VARCHAR(255) NOT NULL,
            contenido       TEXT NOT NULL,
            tags            VARCHAR(255),
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_grimorio_entradas_user_id
        ON grimorio_entradas (user_id)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS sigilos_dibujados (
            id              {pk},
            user_id         INTEGER NOT NULL,
            intencion       TEXT NOT NULL,
            dibujo          TEXT NOT NULL,
            metodo_carga    VARCHAR(50),
            estado          VARCHAR(20) NOT NULL DEFAULT 'creado',
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sigilos_dibujados_user_id
        ON sigilos_dibujados (user_id)
    """)

    # ── Grimorio por esfera ──────────────────────────────────────────────────
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS esfera_grimorio (
            id                  {pk},
            hash_proyecto       TEXT NOT NULL UNIQUE,
            nombre_mago         TEXT,
            intencion           TEXT,
            arquetipo           TEXT,
            elemento            TEXT,
            chakra_activo       TEXT,
            sephira_trabajo     TEXT,
            nivel_voluntad      INTEGER NOT NULL DEFAULT 1,
            nivel_intuicion     INTEGER NOT NULL DEFAULT 1,
            nivel_sombra        INTEGER NOT NULL DEFAULT 1,
            nivel_manifestacion INTEGER NOT NULL DEFAULT 1,
            fecha_nacimiento    TEXT,
            lugar_nacimiento    TEXT,
            lat_nacimiento      REAL,
            lon_nacimiento      REAL,
            creado_en           TEXT NOT NULL,
            actualizado_en      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_esfera_grimorio_hash
        ON esfera_grimorio (hash_proyecto)
    """)

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS esfera_grimorio_deidades (
            id                  {pk},
            grimorio_id         INTEGER NOT NULL
                                    REFERENCES esfera_grimorio(id) ON DELETE CASCADE,
            nombre_entidad      TEXT NOT NULL,
            contexto_personal   TEXT,
            orden               INTEGER NOT NULL DEFAULT 0,
            creado_en           TEXT NOT NULL,
            UNIQUE (grimorio_id, nombre_entidad)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_esfera_grimorio_deidades_gid
        ON esfera_grimorio_deidades (grimorio_id)
    """)

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS esfera_grimorio_reliquias (
            id                      {pk},
            hash_proyecto_origen    TEXT NOT NULL,
            nombre                  TEXT NOT NULL,
            nombre_entidad          TEXT NOT NULL,
            descripcion             TEXT,
            portable                INTEGER NOT NULL DEFAULT 1,
            creado_en               TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_esfera_grimorio_reliquias_origen
        ON esfera_grimorio_reliquias (hash_proyecto_origen)
    """)


# ─── Helpers internos ─────────────────────────────────────────────────────────

def _fila_a_grimorio(r) -> dict:
    return {
        "id": r[0], "hash_proyecto": r[1],
        "nombre_mago": r[2], "intencion": r[3],
        "arquetipo": r[4], "elemento": r[5],
        "chakra_activo": r[6], "sephira_trabajo": r[7],
        "nivel_voluntad": r[8], "nivel_intuicion": r[9],
        "nivel_sombra": r[10], "nivel_manifestacion": r[11],
        "fecha_nacimiento": r[12], "lugar_nacimiento": r[13],
        "lat_nacimiento": r[14], "lon_nacimiento": r[15],
        "creado_en": r[16], "actualizado_en": r[17],
        "deidades": [],
    }

def _fila_a_deidad(r) -> dict:
    return {
        "id": r[0], "grimorio_id": r[1],
        "nombre_entidad": r[2], "contexto_personal": r[3],
        "orden": r[4], "creado_en": r[5],
    }

def _fila_a_reliquia(r) -> dict:
    return {
        "id": r[0], "hash_proyecto_origen": r[1],
        "nombre": r[2], "nombre_entidad": r[3],
        "descripcion": r[4], "portable": bool(r[5]),
        "creado_en": r[6],
    }

_COLS_GRIMORIO = (
    "id, hash_proyecto, nombre_mago, intencion, arquetipo, elemento, "
    "chakra_activo, sephira_trabajo, nivel_voluntad, nivel_intuicion, "
    "nivel_sombra, nivel_manifestacion, fecha_nacimiento, lugar_nacimiento, "
    "lat_nacimiento, lon_nacimiento, creado_en, actualizado_en"
)


# ─── EsferaGrimorioRepo ───────────────────────────────────────────────────────

class EsferaGrimorioRepo:

    @classmethod
    def obtener_o_crear(cls, hash_proyecto: str) -> dict:
        """Devuelve el grimorio del mago. Si no existe, lo crea vacío."""
        g = cls.obtener(hash_proyecto)
        if g:
            return g
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO esfera_grimorio "
                f"(hash_proyecto, creado_en, actualizado_en) "
                f"VALUES ({_ph(3)})",
                (hash_proyecto, ahora, ahora),
            )
            gid = ADAPTADOR.id_ultimo_insertado(cur)
        return cls._cargar_con_deidades(gid)

    @classmethod
    def obtener(cls, hash_proyecto: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {_COLS_GRIMORIO} FROM esfera_grimorio "
                f"WHERE hash_proyecto = {_ph(1)}",
                (hash_proyecto,),
            )
            row = cur.fetchone()
        if not row:
            return None
        g = _fila_a_grimorio(row)
        g["deidades"] = cls._deidades_de(g["id"])
        return g

    @classmethod
    def actualizar(cls, hash_proyecto: str, **campos) -> dict:
        """Actualiza campos del grimorio. Sólo actualiza los que se pasen."""
        permitidos = {
            "nombre_mago", "intencion", "arquetipo", "elemento",
            "chakra_activo", "sephira_trabajo",
            "nivel_voluntad", "nivel_intuicion",
            "nivel_sombra", "nivel_manifestacion",
            "fecha_nacimiento", "lugar_nacimiento",
            "lat_nacimiento", "lon_nacimiento",
        }
        actualizables = {k: v for k, v in campos.items() if k in permitidos}
        if not actualizables:
            return cls.obtener_o_crear(hash_proyecto)

        ahora = datetime.now().isoformat()
        actualizables["actualizado_en"] = ahora
        set_clause = ", ".join(f"{k} = {_ph(1)}" for k in actualizables)
        valores = list(actualizables.values()) + [hash_proyecto]

        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE esfera_grimorio SET {set_clause} "
                f"WHERE hash_proyecto = {_ph(1)}",
                valores,
            )
        return cls.obtener_o_crear(hash_proyecto)

    @classmethod
    def agregar_deidad(cls, hash_proyecto: str, nombre_entidad: str,
                       contexto_personal: str | None = None,
                       orden: int = 0) -> dict:
        """Agrega una entidad al grimorio. Idempotente: actualiza contexto si ya existe."""
        g = cls.obtener_o_crear(hash_proyecto)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id FROM esfera_grimorio_deidades "
                f"WHERE grimorio_id = {_ph(1)} AND nombre_entidad = {_ph(1)}",
                (g["id"], nombre_entidad),
            )
            existente = cur.fetchone()
            if existente:
                cur.execute(
                    f"UPDATE esfera_grimorio_deidades "
                    f"SET contexto_personal = {_ph(1)}, orden = {_ph(1)} "
                    f"WHERE id = {_ph(1)}",
                    (contexto_personal, orden, existente[0]),
                )
            else:
                cur.execute(
                    f"INSERT INTO esfera_grimorio_deidades "
                    f"(grimorio_id, nombre_entidad, contexto_personal, orden, creado_en) "
                    f"VALUES ({_ph(5)})",
                    (g["id"], nombre_entidad, contexto_personal, orden, ahora),
                )
        return cls.obtener(hash_proyecto)

    @classmethod
    def quitar_deidad(cls, hash_proyecto: str, nombre_entidad: str) -> dict:
        g = cls.obtener_o_crear(hash_proyecto)
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM esfera_grimorio_deidades "
                f"WHERE grimorio_id = {_ph(1)} AND nombre_entidad = {_ph(1)}",
                (g["id"], nombre_entidad),
            )
        return cls.obtener(hash_proyecto)

    @classmethod
    def _cargar_con_deidades(cls, grimorio_id: int) -> dict:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {_COLS_GRIMORIO} FROM esfera_grimorio WHERE id = {_ph(1)}",
                (grimorio_id,),
            )
            row = cur.fetchone()
        if not row:
            return {}
        g = _fila_a_grimorio(row)
        g["deidades"] = cls._deidades_de(grimorio_id)
        return g

    @classmethod
    def _deidades_de(cls, grimorio_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT id, grimorio_id, nombre_entidad, contexto_personal, orden, creado_en "
                f"FROM esfera_grimorio_deidades WHERE grimorio_id = {_ph(1)} "
                "ORDER BY orden ASC, creado_en ASC",
                (grimorio_id,),
            )
            return [_fila_a_deidad(r) for r in cur.fetchall()]


# ─── ReliquiaRepo ─────────────────────────────────────────────────────────────

class ReliquiaRepo:

    @classmethod
    def crear(cls, hash_proyecto_origen: str, nombre: str,
              nombre_entidad: str, descripcion: str | None = None,
              portable: bool = True) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO esfera_grimorio_reliquias "
                f"(hash_proyecto_origen, nombre, nombre_entidad, descripcion, portable, creado_en) "
                f"VALUES ({_ph(6)})",
                (hash_proyecto_origen, nombre, nombre_entidad,
                 descripcion, int(portable), ahora),
            )
            rid = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.obtener(rid)

    @classmethod
    def obtener(cls, reliquia_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT id, hash_proyecto_origen, nombre, nombre_entidad, "
                f"descripcion, portable, creado_en FROM esfera_grimorio_reliquias "
                f"WHERE id = {_ph(1)}",
                (reliquia_id,),
            )
            row = cur.fetchone()
        return _fila_a_reliquia(row) if row else None

    @classmethod
    def listar(cls, hash_proyecto_origen: str) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT id, hash_proyecto_origen, nombre, nombre_entidad, "
                f"descripcion, portable, creado_en FROM esfera_grimorio_reliquias "
                f"WHERE hash_proyecto_origen = {_ph(1)} ORDER BY creado_en DESC",
                (hash_proyecto_origen,),
            )
            return [_fila_a_reliquia(r) for r in cur.fetchall()]

    @classmethod
    def listar_portables(cls) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT id, hash_proyecto_origen, nombre, nombre_entidad, "
                "descripcion, portable, creado_en FROM esfera_grimorio_reliquias "
                "WHERE portable = 1 ORDER BY creado_en DESC"
            )
            return [_fila_a_reliquia(r) for r in cur.fetchall()]


# ─── Legacy repos (sin cambios) ───────────────────────────────────────────────

class GrimorioRepo:
    TABLA = "grimorio_entradas"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0], "user_id": r[1], "titulo": r[2],
            "contenido": r[3], "tags": r[4],
            "created_at": r[5], "updated_at": r[6],
        }

    @classmethod
    def crear(cls, user_id: int, titulo: str, contenido: str,
              tags: str | None = None) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, titulo, contenido, tags, created_at, updated_at) "
                f"VALUES ({_ph(6)})",
                (user_id, titulo, contenido, tags, ahora, ahora)
            )
            entrada_id = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.obtener(entrada_id)

    @classmethod
    def obtener(cls, entrada_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, titulo, contenido, tags, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE id = {p}",
                (entrada_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_por_usuario(cls, user_id: int, limite: int = 20) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, titulo, contenido, tags, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (user_id, limite)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]


class SigiloRepo:
    TABLA = "sigilos_dibujados"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0], "user_id": r[1], "intencion": r[2],
            "dibujo": r[3], "metodo_carga": r[4],
            "estado": r[5], "created_at": r[6], "updated_at": r[7],
        }

    @classmethod
    def crear_dibujado(cls, user_id: int, intencion: str, dibujo: str,
                       metodo_carga: str | None = None) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, intencion, dibujo, metodo_carga, estado, created_at, updated_at) "
                f"VALUES ({_ph(7)})",
                (user_id, intencion, dibujo, metodo_carga, "creado", ahora, ahora)
            )
            sigilo_id = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.obtener(sigilo_id)

    @classmethod
    def obtener(cls, sigilo_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, intencion, dibujo, metodo_carga, "
                f"estado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE id = {p}",
                (sigilo_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_por_usuario(cls, user_id: int, estado: str | None = None,
                           limite: int = 20) -> list[dict]:
        with _conexion() as (con, cur):
            if estado:
                cur.execute(
                    f"SELECT id, user_id, intencion, dibujo, metodo_carga, "
                    f"estado, created_at, updated_at "
                    f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND estado = {_ph(1)} "
                    f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                    (user_id, estado, limite)
                )
            else:
                cur.execute(
                    f"SELECT id, user_id, intencion, dibujo, metodo_carga, "
                    f"estado, created_at, updated_at "
                    f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND estado = 'creado' "
                    f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                    (user_id, limite)
                )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def cargar(cls, sigilo_id: int) -> dict | None:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado = 'cargado', updated_at = {_ph(1)} "
                f"WHERE id = {_ph(1)}",
                (ahora, sigilo_id)
            )
        return cls.obtener(sigilo_id)
