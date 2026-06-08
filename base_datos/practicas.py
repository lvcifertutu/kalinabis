"""Repos de prácticas de alcance proyecto: Servitors, Synchronicidades, Paradigmas."""

import json
from datetime import datetime

from base_datos._helpers import _conexion, _ph


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS servitors (
            id            {pk},
            proyecto_hash TEXT NOT NULL,
            nombre        TEXT NOT NULL,
            funcion       TEXT NOT NULL,
            forma         TEXT NOT NULL,
            deidad_padre  TEXT,
            intensidad    REAL NOT NULL DEFAULT 1.0,
            estado        TEXT NOT NULL DEFAULT 'activo',
            ultimo_feed   TEXT NOT NULL,
            created_at    TEXT NOT NULL,
            UNIQUE (proyecto_hash, nombre)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_servitors_proyecto
        ON servitors (proyecto_hash)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS synchronicidades (
            id               {pk},
            proyecto_hash    TEXT NOT NULL,
            signo_esperado   TEXT NOT NULL,
            categoria        TEXT NOT NULL DEFAULT 'otro',
            plazo            TEXT NOT NULL,
            estado           TEXT NOT NULL DEFAULT 'esperando',
            fase_lunar       TEXT,
            nota_confirmacion TEXT,
            fecha_registro   TEXT NOT NULL,
            fecha_reporte    TEXT
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sync_proyecto
        ON synchronicidades (proyecto_hash)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sync_estado
        ON synchronicidades (estado)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS paradigmas_activos (
            id               {pk},
            proyecto_hash    TEXT NOT NULL,
            paradigma_id     INTEGER NOT NULL,
            paradigma_nombre TEXT NOT NULL,
            deidad_guia      TEXT,
            fecha_inicio     TEXT NOT NULL,
            estado           TEXT NOT NULL DEFAULT 'activo',
            checkins         TEXT NOT NULL DEFAULT '[]',
            UNIQUE (proyecto_hash, paradigma_id)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_paradigmas_proyecto
        ON paradigmas_activos (proyecto_hash)
    """)


class ServitorRepo:
    TABLA = "servitors"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id":            r[0],
            "proyecto_hash": r[1],
            "nombre":        r[2],
            "funcion":       r[3],
            "forma":         r[4],
            "deidad_padre":  r[5],
            "intensidad":    r[6],
            "estado":        r[7],
            "ultimo_feed":   r[8],
            "created_at":    r[9],
        }

    @classmethod
    def crear(cls, proyecto_hash: str, nombre: str, funcion: str,
              forma: str, deidad_padre: str | None = None) -> dict | None:
        ahora = datetime.now().isoformat()
        try:
            with _conexion() as (con, cur):
                cur.execute(
                    f"INSERT INTO {cls.TABLA} "
                    f"(proyecto_hash, nombre, funcion, forma, deidad_padre, "
                    f"intensidad, estado, ultimo_feed, created_at) "
                    f"VALUES ({_ph(9)})",
                    (proyecto_hash, nombre, funcion, forma, deidad_padre,
                     1.0, "activo", ahora, ahora)
                )
        except Exception:
            return None
        return cls.obtener(proyecto_hash, nombre)

    @classmethod
    def obtener(cls, proyecto_hash: str, nombre: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, nombre, funcion, forma, deidad_padre, "
                f"intensidad, estado, ultimo_feed, created_at "
                f"FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} AND nombre = {_ph(1)}",
                (proyecto_hash, nombre)
            )
            row = cur.fetchone()
        return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar(cls, proyecto_hash: str) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, nombre, funcion, forma, deidad_padre, "
                f"intensidad, estado, ultimo_feed, created_at "
                f"FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} "
                f"ORDER BY created_at DESC",
                (proyecto_hash,)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def actualizar_intensidad(cls, proyecto_hash: str, nombre: str,
                              nueva_intensidad: float, nuevo_estado: str,
                              actualizar_feed: bool = False) -> dict | None:
        ahora = datetime.now().isoformat()
        sets = [f"intensidad = {_ph(1)}", f"estado = {_ph(1)}"]
        valores = [nueva_intensidad, nuevo_estado]
        if actualizar_feed:
            sets.append(f"ultimo_feed = {_ph(1)}")
            valores.append(ahora)
        valores += [proyecto_hash, nombre]
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET {', '.join(sets)} "
                f"WHERE proyecto_hash = {_ph(1)} AND nombre = {_ph(1)}",
                valores
            )
        return cls.obtener(proyecto_hash, nombre)

    @classmethod
    def eliminar(cls, proyecto_hash: str, nombre: str) -> bool:
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} AND nombre = {_ph(1)}",
                (proyecto_hash, nombre)
            )
            return cur.rowcount > 0


class SyncRepo:
    TABLA = "synchronicidades"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        return {
            "id":                r[0],
            "proyecto_hash":     r[1],
            "signo_esperado":    r[2],
            "categoria":         r[3],
            "plazo":             r[4],
            "estado":            r[5],
            "fase_lunar":        r[6],
            "nota_confirmacion": r[7],
            "fecha_registro":    r[8],
            "fecha_reporte":     r[9],
        }

    @classmethod
    def crear(cls, proyecto_hash: str, signo: str, categoria: str,
              plazo: str, fase_lunar: str | None = None) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA} "
                f"(proyecto_hash, signo_esperado, categoria, plazo, estado, "
                f"fase_lunar, fecha_registro) "
                f"VALUES ({_ph(7)})",
                (proyecto_hash, signo, categoria, plazo,
                 "esperando", fase_lunar, ahora)
            )
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, signo_esperado, categoria, plazo, "
                f"estado, fase_lunar, nota_confirmacion, fecha_registro, fecha_reporte "
                f"FROM {cls.TABLA} WHERE proyecto_hash = {_ph(1)} "
                f"ORDER BY id DESC LIMIT 1",
                (proyecto_hash,)
            )
            row = cur.fetchone()
        return cls._fila_a_dict(row) if row else {}

    @classmethod
    def confirmar(cls, sync_id: int, proyecto_hash: str,
                  nota: str | None = None) -> dict | None:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado = {_ph(1)}, "
                f"fecha_reporte = {_ph(1)}, nota_confirmacion = {_ph(1)} "
                f"WHERE id = {_ph(1)} AND proyecto_hash = {_ph(1)}",
                ("confirmada", ahora, nota, sync_id, proyecto_hash)
            )
        return cls.obtener(sync_id, proyecto_hash)

    @classmethod
    def obtener(cls, sync_id: int, proyecto_hash: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, signo_esperado, categoria, plazo, "
                f"estado, fase_lunar, nota_confirmacion, fecha_registro, fecha_reporte "
                f"FROM {cls.TABLA} WHERE id = {_ph(1)} AND proyecto_hash = {_ph(1)}",
                (sync_id, proyecto_hash)
            )
            row = cur.fetchone()
        return cls._fila_a_dict(row) if row else None

    @classmethod
    def listar(cls, proyecto_hash: str, solo_activas: bool = False) -> list[dict]:
        with _conexion() as (con, cur):
            if solo_activas:
                cur.execute(
                    f"SELECT id, proyecto_hash, signo_esperado, categoria, plazo, "
                    f"estado, fase_lunar, nota_confirmacion, fecha_registro, fecha_reporte "
                    f"FROM {cls.TABLA} WHERE proyecto_hash = {_ph(1)} "
                    f"AND estado = {_ph(1)} ORDER BY fecha_registro DESC",
                    (proyecto_hash, "esperando")
                )
            else:
                cur.execute(
                    f"SELECT id, proyecto_hash, signo_esperado, categoria, plazo, "
                    f"estado, fase_lunar, nota_confirmacion, fecha_registro, fecha_reporte "
                    f"FROM {cls.TABLA} WHERE proyecto_hash = {_ph(1)} "
                    f"ORDER BY fecha_registro DESC LIMIT 30",
                    (proyecto_hash,)
                )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]

    @classmethod
    def todas_recientes(cls, dias: int = 30) -> list[dict]:
        """Retorna syncs de todos los proyectos para analytics colectiva."""
        from datetime import timedelta
        limite = (datetime.now() - timedelta(days=dias)).isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, signo_esperado, categoria, plazo, "
                f"estado, fase_lunar, nota_confirmacion, fecha_registro, fecha_reporte "
                f"FROM {cls.TABLA} WHERE fecha_registro >= {_ph(1)} "
                f"ORDER BY fecha_registro DESC LIMIT 200",
                (limite,)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]


class ParadigmaRepo:
    TABLA = "paradigmas_activos"

    @staticmethod
    def _fila_a_dict(r) -> dict:
        checkins = r[7]
        if isinstance(checkins, str):
            try:
                checkins = json.loads(checkins)
            except Exception:
                checkins = []
        return {
            "id":               r[0],
            "proyecto_hash":    r[1],
            "paradigma_id":     r[2],
            "paradigma_nombre": r[3],
            "deidad_guia":      r[4],
            "fecha_inicio":     r[5],
            "estado":           r[6],
            "checkins":         checkins,
        }

    @classmethod
    def iniciar(cls, proyecto_hash: str, paradigma_id: int,
                paradigma_nombre: str, deidad_guia: str | None = None) -> dict | None:
        ahora = datetime.now().isoformat()
        try:
            with _conexion() as (con, cur):
                cur.execute(
                    f"INSERT INTO {cls.TABLA} "
                    f"(proyecto_hash, paradigma_id, paradigma_nombre, "
                    f"deidad_guia, fecha_inicio, estado, checkins) "
                    f"VALUES ({_ph(7)})",
                    (proyecto_hash, paradigma_id, paradigma_nombre,
                     deidad_guia, ahora, "activo", "[]")
                )
        except Exception:
            return None
        return cls.obtener(proyecto_hash, paradigma_id)

    @classmethod
    def obtener(cls, proyecto_hash: str, paradigma_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, paradigma_id, paradigma_nombre, "
                f"deidad_guia, fecha_inicio, estado, checkins "
                f"FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} AND paradigma_id = {_ph(1)}",
                (proyecto_hash, paradigma_id)
            )
            row = cur.fetchone()
        return cls._fila_a_dict(row) if row else None

    @classmethod
    def obtener_activo(cls, proyecto_hash: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, paradigma_id, paradigma_nombre, "
                f"deidad_guia, fecha_inicio, estado, checkins "
                f"FROM {cls.TABLA} "
                f"WHERE proyecto_hash = {_ph(1)} AND estado = {_ph(1)} "
                f"ORDER BY id DESC LIMIT 1",
                (proyecto_hash, "activo")
            )
            row = cur.fetchone()
        return cls._fila_a_dict(row) if row else None

    @classmethod
    def agregar_checkin(cls, proyecto_hash: str, paradigma_id: int,
                        nota: str, dia: int) -> dict | None:
        paradigma = cls.obtener(proyecto_hash, paradigma_id)
        if not paradigma:
            return None
        checkins = list(paradigma.get("checkins") or [])
        checkins.append({
            "dia":       dia,
            "nota":      nota,
            "timestamp": datetime.now().isoformat(),
        })
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET checkins = {_ph(1)} "
                f"WHERE proyecto_hash = {_ph(1)} AND paradigma_id = {_ph(1)}",
                (json.dumps(checkins, ensure_ascii=False),
                 proyecto_hash, paradigma_id)
            )
        return cls.obtener(proyecto_hash, paradigma_id)

    @classmethod
    def integrar(cls, proyecto_hash: str, paradigma_id: int) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado = {_ph(1)} "
                f"WHERE proyecto_hash = {_ph(1)} AND paradigma_id = {_ph(1)}",
                ("integrado", proyecto_hash, paradigma_id)
            )
        return cls.obtener(proyecto_hash, paradigma_id)

    @classmethod
    def listar(cls, proyecto_hash: str) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, proyecto_hash, paradigma_id, paradigma_nombre, "
                f"deidad_guia, fecha_inicio, estado, checkins "
                f"FROM {cls.TABLA} WHERE proyecto_hash = {_ph(1)} "
                f"ORDER BY id DESC",
                (proyecto_hash,)
            )
            return [cls._fila_a_dict(r) for r in cur.fetchall()]
