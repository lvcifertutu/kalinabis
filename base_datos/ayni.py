"""Repo del sistema de ayni (reciprocidad andina).

Cada petición al universo genera una deuda que debe cerrarse con una ofrenda.
El balance ayni es visible para las entidades y condiciona su respuesta.

Balance:
  > +3  crédito — el practicante da más de lo que pide
  0..+3 equilibrio
  -1..-3 deuda leve
  < -3  deuda significativa — las entidades lo nombran
"""

from datetime import datetime

from base_datos._helpers import _conexion, _ph, ADAPTADOR


# Peso por tipo de origen
PESO_ORIGEN: dict[str, int] = {
    "manifestacion": 3,   # pedir al universo algo importante
    "sigilo":        2,   # operación mágica dirigida
    "limpia":        1,   # apoyo de limpieza
    "consulta":      1,   # pregunta a una deidad
}

TIPOS_OFRENDA = (
    "agua", "tierra", "fuego", "aire",
    "acto", "tiempo", "creacion", "silencio",
)

# Umbral a partir del cual las entidades mencionan la deuda
UMBRAL_DEUDA_NOTABLE = -3


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS ayni_deudas (
            id              {pk},
            proyecto_hash   TEXT NOT NULL,
            tipo_origen     TEXT NOT NULL,
            origen_id       INTEGER,
            descripcion     TEXT NOT NULL,
            peso            INTEGER NOT NULL DEFAULT 1,
            estado          TEXT NOT NULL DEFAULT 'abierta',
            created_at      TEXT NOT NULL,
            cerrada_at      TEXT
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_ayni_deudas_proyecto
        ON ayni_deudas (proyecto_hash)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_ayni_deudas_estado
        ON ayni_deudas (estado)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS ayni_ofrendas (
            id              {pk},
            proyecto_hash   TEXT NOT NULL,
            tipo            TEXT NOT NULL,
            descripcion     TEXT NOT NULL,
            peso            INTEGER NOT NULL DEFAULT 1,
            deuda_id        INTEGER,
            created_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_ayni_ofrendas_proyecto
        ON ayni_ofrendas (proyecto_hash)
    """)


class AyniRepo:
    """Deudas y ofrendas de un proyecto."""

    # ── Deudas ──────────────────────────────────────────────────────────

    @classmethod
    def registrar_deuda(cls, proyecto_hash: str, tipo_origen: str,
                        descripcion: str, origen_id: int | None = None) -> dict:
        peso = PESO_ORIGEN.get(tipo_origen, 1)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"""INSERT INTO ayni_deudas
                    (proyecto_hash, tipo_origen, origen_id, descripcion, peso, created_at)
                    VALUES ({_ph(6)})""",
                (proyecto_hash, tipo_origen, origen_id, descripcion, peso, ahora),
            )
            deuda_id = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.deuda_por_id(deuda_id)

    @classmethod
    def deuda_por_id(cls, deuda_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute("SELECT * FROM ayni_deudas WHERE id = " + p, (deuda_id,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))

    @classmethod
    def cerrar_deuda(cls, deuda_id: int) -> None:
        ahora = datetime.now().isoformat()
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE ayni_deudas SET estado='cerrada', cerrada_at={p} WHERE id={p}",
                (ahora, deuda_id),
            )

    @classmethod
    def deudas_abiertas(cls, proyecto_hash: str) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT * FROM ayni_deudas WHERE proyecto_hash=" + p +
                " AND estado='abierta' ORDER BY created_at DESC",
                (proyecto_hash,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    @classmethod
    def historial_deudas(cls, proyecto_hash: str, limite: int = 20) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT * FROM ayni_deudas WHERE proyecto_hash=" + p +
                " ORDER BY created_at DESC LIMIT " + _ph(1),
                (proyecto_hash, limite),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    # ── Ofrendas ─────────────────────────────────────────────────────────

    @classmethod
    def registrar_ofrenda(cls, proyecto_hash: str, tipo: str, descripcion: str,
                          peso: int = 1, deuda_id: int | None = None) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"""INSERT INTO ayni_ofrendas
                    (proyecto_hash, tipo, descripcion, peso, deuda_id, created_at)
                    VALUES ({_ph(6)})""",
                (proyecto_hash, tipo, descripcion, peso, deuda_id, ahora),
            )
            ofrenda_id = ADAPTADOR.id_ultimo_insertado(cur)
        # Si viene con deuda_id, cerrar esa deuda
        if deuda_id:
            cls.cerrar_deuda(deuda_id)
        with _conexion() as (con, cur):
            cur.execute("SELECT * FROM ayni_ofrendas WHERE id = " + _ph(1), (ofrenda_id,))
            row = cur.fetchone()
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))

    @classmethod
    def historial_ofrendas(cls, proyecto_hash: str, limite: int = 20) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT * FROM ayni_ofrendas WHERE proyecto_hash=" + p +
                " ORDER BY created_at DESC LIMIT " + _ph(1),
                (proyecto_hash, limite),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    # ── Balance ──────────────────────────────────────────────────────────

    @classmethod
    def balance(cls, proyecto_hash: str) -> int:
        """balance = total ofrendado - total pedido. Negativo = deuda."""
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                "SELECT COALESCE(SUM(peso),0) FROM ayni_deudas WHERE proyecto_hash=" + p,
                (proyecto_hash,),
            )
            total_pedido: int = cur.fetchone()[0] or 0

            cur.execute(
                "SELECT COALESCE(SUM(peso),0) FROM ayni_ofrendas WHERE proyecto_hash=" + p,
                (proyecto_hash,),
            )
            total_ofrendado: int = cur.fetchone()[0] or 0

        return total_ofrendado - total_pedido

    @classmethod
    def resumen(cls, proyecto_hash: str) -> dict:
        """Snapshot del estado ayni para el system prompt."""
        bal = cls.balance(proyecto_hash)
        abiertas = cls.deudas_abiertas(proyecto_hash)
        return {
            "balance": bal,
            "n_deudas_abiertas": len(abiertas),
            "notable": bal <= UMBRAL_DEUDA_NOTABLE,
        }
