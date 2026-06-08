"""Repos de identidad y progresión del mago: Usuario, Exp y Logros."""

from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS usuarios (
            id              {pk},
            nombre_mago     VARCHAR(255) NOT NULL,
            modelo          VARCHAR(50) NOT NULL DEFAULT 'aprendiz',
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS exp_usuarios (
            id              {pk},
            user_id         INTEGER NOT NULL,
            capa            VARCHAR(50) NOT NULL,
            exp             INTEGER NOT NULL DEFAULT 0,
            nivel           INTEGER NOT NULL DEFAULT 1,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL,
            UNIQUE (user_id, capa)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_exp_usuarios_user_id
        ON exp_usuarios (user_id)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS logros (
            id              {pk},
            user_id         INTEGER NOT NULL,
            capa            VARCHAR(50) NOT NULL,
            nombre_logro    VARCHAR(255) NOT NULL,
            created_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_logros_user_id
        ON logros (user_id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_logros_user_capa
        ON logros (user_id, capa)
    """)


class UsuarioRepo:
    TABLA = "usuarios"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "nombre_mago": r[1],
            "modelo": r[2],
            "created_at": r[3],
            "updated_at": r[4],
        }

    @classmethod
    def crear(cls, nombre_mago: str, modelo: str = "aprendiz") -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(nombre_mago, modelo, created_at, updated_at) "
                f"VALUES ({_ph(4)})",
                (nombre_mago, modelo, ahora, ahora)
            )
            user_id = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.obtener(user_id)

    @classmethod
    def obtener(cls, user_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, nombre_mago, modelo, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE id = {p}",
                (user_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None


class ExpRepo:
    TABLA = "exp_usuarios"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_id": r[1],
            "capa": r[2],
            "exp": r[3],
            "nivel": r[4],
            "created_at": r[5],
            "updated_at": r[6],
        }

    @classmethod
    def crear_o_actualizar(cls, user_id: int, capa: str,
                           exp: int = 0, nivel: int = 1) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND capa = {_ph(1)}",
                (user_id, capa)
            )
            existe = cur.fetchone()
            if existe:
                cur.execute(
                    f"UPDATE {cls.TABLA} SET exp = {_ph(1)}, nivel = {_ph(1)}, "
                    f"updated_at = {_ph(1)} WHERE user_id = {_ph(1)} AND capa = {_ph(1)}",
                    (exp, nivel, ahora, user_id, capa)
                )
            else:
                cur.execute(
                    f"INSERT INTO {cls.TABLA} "
                    f"(user_id, capa, exp, nivel, created_at, updated_at) "
                    f"VALUES ({_ph(6)})",
                    (user_id, capa, exp, nivel, ahora, ahora)
                )
        return cls.obtener(user_id, capa)

    @classmethod
    def obtener(cls, user_id: int, capa: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, capa, exp, nivel, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND capa = {_ph(1)}",
                (user_id, capa)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def agregar_exp(cls, user_id: int, capa: str, cantidad: int):
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET exp = exp + {_ph(1)}, "
                f"updated_at = {_ph(1)} WHERE user_id = {_ph(1)} AND capa = {_ph(1)}",
                (cantidad, ahora, user_id, capa)
            )

    @classmethod
    def listar_por_usuario(cls, user_id: int) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, capa, exp, nivel, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {p} ORDER BY capa ASC",
                (user_id,)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def obtener_todas_capas(cls, user_id: int) -> dict:
        return {e["capa"]: e for e in cls.listar_por_usuario(user_id)}


class LogroRepo:
    TABLA = "logros"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_id": r[1],
            "capa": r[2],
            "nombre_logro": r[3],
            "created_at": r[4],
        }

    @classmethod
    def registrar(cls, user_id: int, capa: str, nombre_logro: str) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, capa, nombre_logro, created_at) "
                f"VALUES ({_ph(4)})",
                (user_id, capa, nombre_logro, ahora)
            )
            logro_id = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.obtener(logro_id)

    @classmethod
    def obtener(cls, logro_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, capa, nombre_logro, created_at "
                f"FROM {cls.TABLA} WHERE id = {p}",
                (logro_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_por_usuario(cls, user_id: int) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, capa, nombre_logro, created_at "
                f"FROM {cls.TABLA} WHERE user_id = {p} ORDER BY created_at DESC",
                (user_id,)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def obtener_ultimo(cls, user_id: int, capa: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, capa, nombre_logro, created_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND capa = {_ph(1)} "
                f"ORDER BY created_at DESC LIMIT 1",
                (user_id, capa)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None
