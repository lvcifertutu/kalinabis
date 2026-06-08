"""Repos de Capa 1 — El Grimorio personal: entradas y sigilos dibujados."""

from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


def _crear_tablas(cur, pk: str):
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
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sigilos_dibujados_estado
        ON sigilos_dibujados (estado)
    """)


class GrimorioRepo:
    TABLA = "grimorio_entradas"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_id": r[1],
            "titulo": r[2],
            "contenido": r[3],
            "tags": r[4],
            "created_at": r[5],
            "updated_at": r[6],
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
            "id": r[0],
            "user_id": r[1],
            "intencion": r[2],
            "dibujo": r[3],
            "metodo_carga": r[4],
            "estado": r[5],
            "created_at": r[6],
            "updated_at": r[7],
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
