"""Repo de limpias digitales — rituales de limpieza andino/curanderismo."""

from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


TRADICIONES = ("saminchakuy", "curanderismo")
ENTIDADES_GUIA = ("artemisa", "lilith")


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS limpias (
            id              {pk},
            proyecto_hash   TEXT NOT NULL,
            tradicion       TEXT NOT NULL,
            entidad         TEXT NOT NULL,
            estado_pre      TEXT NOT NULL,
            estado_post     TEXT,
            estado          TEXT NOT NULL DEFAULT 'pendiente',
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_limpias_proyecto
        ON limpias (proyecto_hash)
    """)


class LimpiaRepo:
    TABLA = "limpias"

    @classmethod
    def iniciar(cls, proyecto_hash: str, tradicion: str,
                entidad: str, estado_pre: str) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"""INSERT INTO {cls.TABLA}
                    (proyecto_hash, tradicion, entidad, estado_pre,
                     estado, created_at, updated_at)
                    VALUES ({_ph(7)})""",
                (proyecto_hash, tradicion, entidad, estado_pre,
                 "pendiente", ahora, ahora),
            )
            limpia_id = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.por_id(limpia_id)

    @classmethod
    def completar(cls, limpia_id: int, estado_post: str) -> dict | None:
        ahora = datetime.now().isoformat()
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado_post={p}, estado='completada', "
                f"updated_at={p} WHERE id={p}",
                (estado_post, ahora, limpia_id),
            )
        return cls.por_id(limpia_id)

    @classmethod
    def por_id(cls, limpia_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(f"SELECT * FROM {cls.TABLA} WHERE id={p}", (limpia_id,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))

    @classmethod
    def listar(cls, proyecto_hash: str, limite: int = 20) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT * FROM {cls.TABLA} WHERE proyecto_hash={p} "
                f"ORDER BY created_at DESC LIMIT {_ph(1)}",
                (proyecto_hash, limite),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
