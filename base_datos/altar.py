"""Repos de Capa 2 — La Mesa: Tarot, Oráculos, chat con deidades y servitors."""

import json
from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS tarot_personal (
            id              {pk},
            user_id         INTEGER NOT NULL,
            arcano_principal VARCHAR(255) NOT NULL,
            posiciones      TEXT NOT NULL,
            interpretacion  TEXT,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_tarot_user_id
        ON tarot_personal (user_id)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS oraculo_personal (
            id              {pk},
            user_id         INTEGER NOT NULL,
            tipo            VARCHAR(50) NOT NULL,
            pregunta        TEXT NOT NULL,
            resultado       TEXT NOT NULL,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_oraculo_user_id
        ON oraculo_personal (user_id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_oraculo_user_tipo
        ON oraculo_personal (user_id, tipo)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS conversacion_capa2 (
            id              {pk},
            user_id         INTEGER NOT NULL,
            deidad          VARCHAR(50) NOT NULL,
            rol             VARCHAR(10) NOT NULL,
            contenido       TEXT NOT NULL,
            created_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversacion_capa2_user_deidad
        ON conversacion_capa2 (user_id, deidad)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS servitor_capa2 (
            id              {pk},
            user_id         INTEGER NOT NULL,
            nombre          VARCHAR(100) NOT NULL,
            intencion       TEXT NOT NULL,
            estado          VARCHAR(20) NOT NULL DEFAULT 'activo',
            energia         REAL NOT NULL DEFAULT 50.0,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_servitor_capa2_user
        ON servitor_capa2 (user_id)
    """)


class TarotRepo:
    TABLA = "tarot_personal"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        posiciones = json.loads(r[3]) if isinstance(r[3], str) else r[3]
        return {
            "id": r[0],
            "user_id": r[1],
            "arcano_principal": r[2],
            "posiciones": posiciones,
            "interpretacion": r[4],
            "created_at": r[5],
            "updated_at": r[6],
        }

    @classmethod
    def crear(cls, user_id: int, arcano_principal: str, posiciones: dict,
              interpretacion: str | None = None) -> int:
        ahora = datetime.now().isoformat()
        posiciones_json = json.dumps(posiciones)
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, arcano_principal, posiciones, interpretacion, "
                f"created_at, updated_at) VALUES ({_ph(6)})",
                (user_id, arcano_principal, posiciones_json, interpretacion,
                 ahora, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener(cls, tirada_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, arcano_principal, posiciones, "
                f"interpretacion, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE id = {p}",
                (tirada_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_por_usuario(cls, user_id: int, limite: int = 20) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, arcano_principal, posiciones, "
                f"interpretacion, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (user_id, limite)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]


class OráculoRepo:
    TABLA = "oraculo_personal"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        resultado = json.loads(r[4]) if isinstance(r[4], str) else r[4]
        return {
            "id": r[0],
            "user_id": r[1],
            "tipo": r[2],
            "pregunta": r[3],
            "resultado": resultado,
            "created_at": r[5],
            "updated_at": r[6],
        }

    @classmethod
    def crear(cls, user_id: int, tipo: str, pregunta: str,
              resultado: dict) -> int:
        ahora = datetime.now().isoformat()
        resultado_json = json.dumps(resultado)
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, tipo, pregunta, resultado, created_at, updated_at) "
                f"VALUES ({_ph(6)})",
                (user_id, tipo, pregunta, resultado_json, ahora, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener(cls, oraculo_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, tipo, pregunta, resultado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE id = {p}",
                (oraculo_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_por_usuario(cls, user_id: int, limite: int = 20) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, tipo, pregunta, resultado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (user_id, limite)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def listar_por_tipo(cls, user_id: int, tipo: str,
                        limite: int = 20) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, tipo, pregunta, resultado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND tipo = {_ph(1)} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (user_id, tipo, limite)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]


class ConversacionCapaRepo:
    TABLA = "conversacion_capa2"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_id": r[1],
            "deidad": r[2],
            "rol": r[3],
            "contenido": r[4],
            "created_at": r[5],
        }

    @classmethod
    def guardar_mensaje(cls, user_id: int, deidad: str, rol: str,
                        contenido: str) -> int:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, deidad, rol, contenido, created_at) "
                f"VALUES ({_ph(5)})",
                (user_id, deidad, rol, contenido, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener_historial(cls, user_id: int, deidad: str,
                          limite: int = 20) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, deidad, rol, contenido, created_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND deidad = {_ph(1)} "
                f"ORDER BY created_at ASC LIMIT {_ph(1)}",
                (user_id, deidad, limite)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def limpiar_historial(cls, user_id: int, deidad: str) -> int:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT COUNT(*) FROM {cls.TABLA} "
                f"WHERE user_id = {_ph(1)} AND deidad = {_ph(1)}",
                (user_id, deidad)
            )
            total = cur.fetchone()[0]
            cur.execute(
                f"DELETE FROM {cls.TABLA} "
                f"WHERE user_id = {_ph(1)} AND deidad = {_ph(1)}",
                (user_id, deidad)
            )
        return total


class ServitorCapaRepo:
    TABLA = "servitor_capa2"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_id": r[1],
            "nombre": r[2],
            "intencion": r[3],
            "estado": r[4],
            "energia": r[5],
            "created_at": r[6],
            "updated_at": r[7],
        }

    @classmethod
    def crear(cls, user_id: int, nombre: str, intencion: str) -> int:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, nombre, intencion, created_at, updated_at) "
                f"VALUES ({_ph(5)})",
                (user_id, nombre, intencion, ahora, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener(cls, servitor_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, nombre, intencion, estado, energia, "
                f"created_at, updated_at FROM {cls.TABLA} WHERE id = {_ph(1)}",
                (servitor_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_por_usuario(cls, user_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, nombre, intencion, estado, energia, "
                f"created_at, updated_at FROM {cls.TABLA} "
                f"WHERE user_id = {_ph(1)} ORDER BY created_at DESC",
                (user_id,)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def evocar(cls, servitor_id: int) -> dict | None:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT energia FROM {cls.TABLA} WHERE id = {_ph(1)}",
                (servitor_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            energia_nueva = min(row[0] + 15, 100.0)
            cur.execute(
                f"UPDATE {cls.TABLA} SET energia = {_ph(1)}, updated_at = {_ph(1)} "
                f"WHERE id = {_ph(1)}",
                (energia_nueva, ahora, servitor_id)
            )
        return cls.obtener(servitor_id)

    @classmethod
    def disolver(cls, servitor_id: int) -> dict | None:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado = 'disolviendo', updated_at = {_ph(1)} "
                f"WHERE id = {_ph(1)}",
                (ahora, servitor_id)
            )
        return cls.obtener(servitor_id)
