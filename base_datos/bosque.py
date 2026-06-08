"""Repos de Capa 3 — El Bosque colectivo: Esferas personales, Semillas, Sincronicidades, Micorriza."""

import json
from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS esfera_capa3 (
            id              {pk},
            user_id         INTEGER NOT NULL,
            tipo            VARCHAR(50) NOT NULL,
            clave_unica     VARCHAR(100) NOT NULL,
            metadata_json   TEXT,
            amplitud        REAL NOT NULL DEFAULT 1.0,
            estado          VARCHAR(20) NOT NULL DEFAULT 'activa',
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL,
            UNIQUE (user_id, clave_unica)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_esfera_capa3_user
        ON esfera_capa3 (user_id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_esfera_capa3_tipo
        ON esfera_capa3 (user_id, tipo)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS sigilo_aportado (
            id                  {pk},
            user_id             INTEGER NOT NULL,
            sigilo_dibujado_id  INTEGER NOT NULL,
            esfera_capa3_id     INTEGER NOT NULL,
            intencion           TEXT NOT NULL,
            estado              VARCHAR(20) NOT NULL DEFAULT 'germinando',
            created_at          TEXT NOT NULL,
            updated_at          TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sigilo_aportado_esfera
        ON sigilo_aportado (esfera_capa3_id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sigilo_aportado_user
        ON sigilo_aportado (user_id)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS sincronicidad_capa3 (
            id           {pk},
            user_id      INTEGER NOT NULL,
            descripcion  TEXT NOT NULL,
            categoria    VARCHAR(50) NOT NULL DEFAULT 'general',
            fase_lunar   VARCHAR(20) NOT NULL,
            confirmada   INTEGER NOT NULL DEFAULT 0,
            created_at   TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sincronicidad_capa3_fase
        ON sincronicidad_capa3 (fase_lunar)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sincronicidad_capa3_user
        ON sincronicidad_capa3 (user_id)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS micorriza (
            id          {pk},
            user_a_id   INTEGER NOT NULL,
            user_b_id   INTEGER NOT NULL,
            ritual      TEXT NOT NULL,
            estado      VARCHAR(20) NOT NULL DEFAULT 'activa',
            created_at  TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_micorriza_a
        ON micorriza (user_a_id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_micorriza_b
        ON micorriza (user_b_id)
    """)


class EsferaCapaRepo:
    TABLA = "esfera_capa3"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        metadata = json.loads(r[4]) if isinstance(r[4], str) else r[4] or {}
        return {
            "id": r[0],
            "user_id": r[1],
            "tipo": r[2],
            "clave_unica": r[3],
            "metadata": metadata,
            "amplitud": r[5],
            "estado": r[6],
            "created_at": r[7],
            "updated_at": r[8],
        }

    @classmethod
    def crear(cls, user_id: int, tipo: str, clave: str,
              metadata: dict | None = None) -> int:
        ahora = datetime.now().isoformat()
        metadata_json = json.dumps(metadata or {})
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, tipo, clave_unica, metadata_json, created_at, updated_at) "
                f"VALUES ({_ph(6)})",
                (user_id, tipo, clave, metadata_json, ahora, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener(cls, esfera_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, tipo, clave_unica, metadata_json, "
                f"amplitud, estado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE id = {_ph(1)}",
                (esfera_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def obtener_por_clave(cls, user_id: int, clave: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, tipo, clave_unica, metadata_json, "
                f"amplitud, estado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND clave_unica = {_ph(1)}",
                (user_id, clave)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def obtener_o_crear(cls, user_id: int, tipo: str, clave: str,
                        metadata: dict | None = None) -> int:
        existente = cls.obtener_por_clave(user_id, clave)
        if existente:
            return existente["id"]
        return cls.crear(user_id, tipo, clave, metadata)

    @classmethod
    def listar_por_usuario(cls, user_id: int, estado: str = "activa") -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, tipo, clave_unica, metadata_json, "
                f"amplitud, estado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND estado = {_ph(1)} "
                f"ORDER BY amplitud DESC",
                (user_id, estado)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def listar_por_tipo(cls, user_id: int, tipo: str) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, user_id, tipo, clave_unica, metadata_json, "
                f"amplitud, estado, created_at, updated_at "
                f"FROM {cls.TABLA} WHERE user_id = {_ph(1)} AND tipo = {_ph(1)} "
                f"AND estado = 'activa' ORDER BY amplitud DESC",
                (user_id, tipo)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def marcar_resonancia(cls, esfera_id: int, cantidad: float = 0.1) -> dict | None:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT amplitud FROM {cls.TABLA} WHERE id = {_ph(1)}",
                (esfera_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            cur.execute(
                f"UPDATE {cls.TABLA} SET amplitud = {_ph(1)}, updated_at = {_ph(1)} "
                f"WHERE id = {_ph(1)}",
                (row[0] + cantidad, ahora, esfera_id)
            )
        return cls.obtener(esfera_id)


class SigiloAportadoRepo:
    TABLA = "sigilo_aportado"
    ESTADOS_VALIDOS = ("germinando", "brotado", "enraizado", "disolviendo")

    _COLS = ("id, user_id, sigilo_dibujado_id, esfera_capa3_id, "
             "intencion, estado, created_at, updated_at")

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_id": r[1],
            "sigilo_dibujado_id": r[2],
            "esfera_capa3_id": r[3],
            "intencion": r[4],
            "estado": r[5],
            "created_at": r[6],
            "updated_at": r[7],
        }

    @staticmethod
    def _fila_a_dict_anonimo(r) -> dict:
        return {
            "id": r[0],
            "esfera_capa3_id": r[3],
            "intencion": r[4],
            "estado": r[5],
            "created_at": r[6],
        }

    @classmethod
    def aportar(cls, user_id: int, sigilo_dibujado_id: int,
                esfera_capa3_id: int, intencion: str) -> int:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, sigilo_dibujado_id, esfera_capa3_id, intencion, "
                f"created_at, updated_at) VALUES ({_ph(6)})",
                (user_id, sigilo_dibujado_id, esfera_capa3_id, intencion,
                 ahora, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener(cls, aportado_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} WHERE id = {_ph(1)}",
                (aportado_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_anonimos(cls, limite: int = 50) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (limite,)
            )
            return [cls._fila_a_dict_anonimo(r) for r in cur.fetchall()]

    @classmethod
    def listar_por_usuario(cls, user_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} WHERE user_id = {_ph(1)} "
                f"ORDER BY created_at DESC",
                (user_id,)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def listar_por_esfera(cls, esfera_capa3_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} "
                f"WHERE esfera_capa3_id = {_ph(1)} ORDER BY created_at DESC",
                (esfera_capa3_id,)
            )
            return [cls._fila_a_dict_anonimo(r) for r in cur.fetchall()]

    @classmethod
    def transitar_estado(cls, aportado_id: int, nuevo_estado: str) -> dict | None:
        if nuevo_estado not in cls.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado inválido: {nuevo_estado}. "
                f"Válidos: {', '.join(cls.ESTADOS_VALIDOS)}"
            )
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado = {_ph(1)}, updated_at = {_ph(1)} "
                f"WHERE id = {_ph(1)}",
                (nuevo_estado, ahora, aportado_id)
            )
        return cls.obtener(aportado_id)


class SincronicidadCapaRepo:
    TABLA = "sincronicidad_capa3"
    _COLS = ("id, user_id, descripcion, categoria, fase_lunar, "
             "confirmada, created_at")

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_id": r[1],
            "descripcion": r[2],
            "categoria": r[3],
            "fase_lunar": r[4],
            "confirmada": bool(r[5]),
            "created_at": r[6],
        }

    @staticmethod
    def _fila_a_dict_anonimo(r) -> dict:
        return {
            "id": r[0],
            "descripcion": r[2],
            "categoria": r[3],
            "fase_lunar": r[4],
            "confirmada": bool(r[5]),
            "created_at": r[6],
        }

    @classmethod
    def registrar(cls, user_id: int, descripcion: str, categoria: str,
                  fase_lunar: str) -> int:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_id, descripcion, categoria, fase_lunar, created_at) "
                f"VALUES ({_ph(5)})",
                (user_id, descripcion, categoria, fase_lunar, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener(cls, sync_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} WHERE id = {_ph(1)}",
                (sync_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_por_fase(cls, fase_lunar: str, limite: int = 50) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} "
                f"WHERE fase_lunar = {_ph(1)} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (fase_lunar, limite)
            )
            return [cls._fila_a_dict_anonimo(r) for r in cur.fetchall()]

    @classmethod
    def listar_confirmadas(cls, limite: int = 50) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} WHERE confirmada = 1 "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (limite,)
            )
            return [cls._fila_a_dict_anonimo(r) for r in cur.fetchall()]

    @classmethod
    def listar_recientes(cls, limite: int = 50) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (limite,)
            )
            return [cls._fila_a_dict_anonimo(r) for r in cur.fetchall()]

    @classmethod
    def confirmar(cls, sync_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET confirmada = 1 WHERE id = {_ph(1)}",
                (sync_id,)
            )
        return cls.obtener(sync_id)


class MicorrizaRepo:
    TABLA = "micorriza"
    _COLS = "id, user_a_id, user_b_id, ritual, estado, created_at"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id": r[0],
            "user_a_id": r[1],
            "user_b_id": r[2],
            "ritual": r[3],
            "estado": r[4],
            "created_at": r[5],
        }

    @classmethod
    def conectar(cls, user_a_id: int, user_b_id: int, ritual: str) -> int:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(user_a_id, user_b_id, ritual, created_at) VALUES ({_ph(4)})",
                (user_a_id, user_b_id, ritual, ahora)
            )
            return ADAPTADOR.id_ultimo_insertado(cur)

    @classmethod
    def obtener(cls, micorriza_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} WHERE id = {_ph(1)}",
                (micorriza_id,)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def obtener_activa_entre(cls, user_x_id: int, user_y_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} "
                f"WHERE estado = 'activa' AND ("
                f"(user_a_id = {_ph(1)} AND user_b_id = {_ph(1)}) OR "
                f"(user_a_id = {_ph(1)} AND user_b_id = {_ph(1)}))",
                (user_x_id, user_y_id, user_y_id, user_x_id)
            )
            row = cur.fetchone()
            return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar_activas(cls, user_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT {cls._COLS} FROM {cls.TABLA} "
                f"WHERE estado = 'activa' AND "
                f"(user_a_id = {_ph(1)} OR user_b_id = {_ph(1)}) "
                f"ORDER BY created_at DESC",
                (user_id, user_id)
            )
            conexiones = []
            for r in cur.fetchall():
                fila = cls._fila_a_dict(r)
                otro = (fila["user_b_id"] if fila["user_a_id"] == user_id
                        else fila["user_a_id"])
                conexiones.append({
                    "id": fila["id"],
                    "otro_mago_id": otro,
                    "ritual": fila["ritual"],
                    "created_at": fila["created_at"],
                })
            return conexiones

    @classmethod
    def romper(cls, micorriza_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado = 'rota' WHERE id = {_ph(1)}",
                (micorriza_id,)
            )
        return cls.obtener(micorriza_id)
