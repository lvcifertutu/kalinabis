"""Repos de alcance proyecto: identidad, conversaciones y carta natal."""

from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


def _crear_tablas(cur, pk: str):
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
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_proyectos_hash
        ON proyectos (hash_codigo)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversaciones_proyecto
        ON conversaciones_proyecto (proyecto_hash, entidad)
    """)


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
    def ultima_actividad(cls, proyecto_hash: str) -> str | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT timestamp FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} "
                f"ORDER BY id DESC LIMIT 1",
                (proyecto_hash,)
            )
            row = cur.fetchone()
            return row[0] if row else None

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
