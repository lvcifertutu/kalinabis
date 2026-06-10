"""Repos de manifestación: intenciones declaradas con testigo divino y sus check-ins."""

import json
from datetime import datetime, timedelta

from base_datos._helpers import _conexion, _ph


_DIAS_CHECKIN = (7, 30, 90)


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS manifestaciones (
            id              {pk},
            proyecto_hash   TEXT NOT NULL,
            tipo            TEXT NOT NULL,
            intencion       TEXT NOT NULL,
            entidad_testigo TEXT NOT NULL,
            estado          TEXT NOT NULL DEFAULT 'activa',
            fecha_limite    TEXT,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_manifestaciones_proyecto
        ON manifestaciones (proyecto_hash)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_manifestaciones_estado
        ON manifestaciones (estado)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS manifestacion_checkins (
            id                  {pk},
            manifestacion_id    INTEGER NOT NULL,
            t_dias              INTEGER NOT NULL,
            observacion         TEXT,
            estado_resultado    TEXT NOT NULL DEFAULT 'pendiente',
            created_at          TEXT NOT NULL,
            UNIQUE (manifestacion_id, t_dias)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_checkins_manifestacion
        ON manifestacion_checkins (manifestacion_id)
    """)


class ManifestacionRepo:
    TABLA = "manifestaciones"

    @classmethod
    def crear(cls, proyecto_hash: str, tipo: str, intencion: str,
              entidad_testigo: str) -> int:
        p = _ph(1)
        ahora = datetime.now().isoformat()
        # Fecha límite a 90 días (el último check-in)
        limite = (datetime.now() + timedelta(days=90)).isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"""INSERT INTO {cls.TABLA}
                    (proyecto_hash, tipo, intencion, entidad_testigo,
                     estado, fecha_limite, created_at, updated_at)
                    VALUES ({p},{p},{p},{p},'activa',{p},{p},{p})""",
                (proyecto_hash, tipo, intencion, entidad_testigo,
                 limite, ahora, ahora)
            )
            if hasattr(cur, "lastrowid"):
                return cur.lastrowid  # SQLite
            cur.execute("SELECT lastval()")
            return cur.fetchone()[0]  # Postgres

    @classmethod
    def listar(cls, proyecto_hash: str, estado: str | None = None) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            if estado:
                cur.execute(
                    f"SELECT * FROM {cls.TABLA} WHERE proyecto_hash={p} AND estado={p} ORDER BY created_at DESC",
                    (proyecto_hash, estado)
                )
            else:
                cur.execute(
                    f"SELECT * FROM {cls.TABLA} WHERE proyecto_hash={p} ORDER BY created_at DESC",
                    (proyecto_hash,)
                )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    @classmethod
    def por_id(cls, manifestacion_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT * FROM {cls.TABLA} WHERE id={p}",
                (manifestacion_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))

    @classmethod
    def cambiar_estado(cls, manifestacion_id: int, estado: str) -> None:
        p = _ph(1)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado={p}, updated_at={p} WHERE id={p}",
                (estado, ahora, manifestacion_id)
            )

    @classmethod
    def checkins_pendientes(cls, proyecto_hash: str) -> list[dict]:
        """Manifestaciones activas con check-ins vencidos aún sin registrar."""
        todas = cls.listar(proyecto_hash, estado="activa")
        pendientes = []
        ahora = datetime.now()
        for m in todas:
            creado = datetime.fromisoformat(m["created_at"])
            hechos = {c["t_dias"] for c in CheckinRepo.por_manifestacion(m["id"])}
            for dias in _DIAS_CHECKIN:
                if dias not in hechos:
                    vence = creado + timedelta(days=dias)
                    if ahora >= vence:
                        pendientes.append({**m, "_t_dias": dias, "_vencio": vence})
                        break  # Solo el primer check-in pendiente por manifestación
        return pendientes


class CheckinRepo:
    TABLA = "manifestacion_checkins"

    @classmethod
    def registrar(cls, manifestacion_id: int, t_dias: int,
                  observacion: str, estado_resultado: str) -> None:
        p = _ph(1)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"""INSERT OR REPLACE INTO {cls.TABLA}
                    (manifestacion_id, t_dias, observacion, estado_resultado, created_at)
                    VALUES ({p},{p},{p},{p},{p})""",
                (manifestacion_id, t_dias, observacion, estado_resultado, ahora)
            )

    @classmethod
    def por_manifestacion(cls, manifestacion_id: int) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT * FROM {cls.TABLA} WHERE manifestacion_id={p} ORDER BY t_dias",
                (manifestacion_id,)
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
