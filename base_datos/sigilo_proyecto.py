"""Repo de sigilos operativos vinculados a proyecto (ciclo completo Carroll).

Ciclo: creado → cargado → olvidado → revelado → quemado
Durante el olvido la intención se oculta — solo el glifo es visible.
"""

from datetime import datetime, timedelta

from base_datos._helpers import _conexion, _ph, ADAPTADOR


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS sigilos_operativos (
            id              {pk},
            proyecto_hash   TEXT NOT NULL,
            intencion       TEXT NOT NULL,
            letras_base     TEXT NOT NULL,
            glifo           TEXT NOT NULL,
            metodo_gnosis   TEXT,
            estado          TEXT NOT NULL DEFAULT 'creado',
            dias_olvido     INTEGER NOT NULL DEFAULT 14,
            fecha_carga     TEXT,
            fecha_revelacion TEXT,
            resultado       TEXT,
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sigilos_op_proyecto
        ON sigilos_operativos (proyecto_hash)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sigilos_op_estado
        ON sigilos_operativos (estado)
    """)


def letras_carroll(intencion: str) -> str:
    """Método Carroll: elimina vocales y letras repetidas. Devuelve consonantes únicas en mayúsculas."""
    vocales = set("aeiouáéíóúüàèìòù")
    vistas: set[str] = set()
    resultado = []
    for c in intencion.lower():
        if c.isalpha() and c not in vocales and c not in vistas:
            resultado.append(c.upper())
            vistas.add(c)
    return "".join(resultado)


def glifo_ascii(letras: str) -> str:
    """Genera un glifo ASCII de 3 líneas a partir de las letras Carroll."""
    pad = (letras + "·" * 8)[:8]
    tl, t, tr = pad[7], pad[0], pad[1]
    l,      r = pad[6],         pad[2]
    bl, b, br = pad[5], pad[4], pad[3]
    return (
        f" {tl} {t} {tr}\n"
        f" {l} ⬡ {r}\n"
        f" {bl} {b} {br}"
    )


class SigiloOperativoRepo:
    TABLA = "sigilos_operativos"

    @classmethod
    def crear(cls, proyecto_hash: str, intencion: str,
              dias_olvido: int = 14) -> dict:
        letras = letras_carroll(intencion)
        glifo = glifo_ascii(letras)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"""INSERT INTO {cls.TABLA}
                    (proyecto_hash, intencion, letras_base, glifo,
                     estado, dias_olvido, created_at, updated_at)
                    VALUES ({_ph(8)})""",
                (proyecto_hash, intencion, letras, glifo,
                 "creado", dias_olvido, ahora, ahora),
            )
            sigilo_id = ADAPTADOR.id_ultimo_insertado(cur)
        return cls.por_id(sigilo_id)

    @classmethod
    def por_id(cls, sigilo_id: int) -> dict | None:
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(f"SELECT * FROM {cls.TABLA} WHERE id = {p}", (sigilo_id,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))

    @classmethod
    def listar(cls, proyecto_hash: str, estado: str | None = None) -> list[dict]:
        p = _ph(1)
        with _conexion() as (con, cur):
            if estado:
                cur.execute(
                    f"SELECT * FROM {cls.TABLA} WHERE proyecto_hash={p} AND estado={p} "
                    f"ORDER BY created_at DESC",
                    (proyecto_hash, estado),
                )
            else:
                cur.execute(
                    f"SELECT * FROM {cls.TABLA} WHERE proyecto_hash={p} "
                    f"ORDER BY created_at DESC",
                    (proyecto_hash,),
                )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    @classmethod
    def cargar(cls, sigilo_id: int, metodo_gnosis: str, dias_olvido: int) -> dict | None:
        ahora = datetime.now()
        revelacion = (ahora + timedelta(days=dias_olvido)).isoformat()
        ahora_iso = ahora.isoformat()
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"""UPDATE {cls.TABLA}
                    SET estado='olvidado', metodo_gnosis={p},
                        dias_olvido={p}, fecha_carga={p},
                        fecha_revelacion={p}, updated_at={p}
                    WHERE id={p}""",
                (metodo_gnosis, dias_olvido, ahora_iso, revelacion, ahora_iso, sigilo_id),
            )
        return cls.por_id(sigilo_id)

    @classmethod
    def revelar(cls, sigilo_id: int) -> dict | None:
        """Marca como revelado si ya pasó fecha_revelacion. Devuelve None si aún en olvido."""
        s = cls.por_id(sigilo_id)
        if not s:
            return None
        if s["estado"] not in ("olvidado",):
            return s  # ya está revelado o en otro estado
        if s["fecha_revelacion"]:
            ahora = datetime.now()
            revelacion = datetime.fromisoformat(s["fecha_revelacion"])
            if ahora < revelacion:
                return None  # todavía en olvido
        ahora_iso = datetime.now().isoformat()
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado='revelado', updated_at={p} WHERE id={p}",
                (ahora_iso, sigilo_id),
            )
        return cls.por_id(sigilo_id)

    @classmethod
    def quemar(cls, sigilo_id: int, resultado: str) -> dict | None:
        ahora = datetime.now().isoformat()
        p = _ph(1)
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET estado='quemado', resultado={p}, updated_at={p} "
                f"WHERE id={p}",
                (resultado, ahora, sigilo_id),
            )
        return cls.por_id(sigilo_id)

    @classmethod
    def dias_restantes_olvido(cls, sigilo: dict) -> float:
        """Días que faltan para revelar. Negativo = ya pasó."""
        if not sigilo.get("fecha_revelacion"):
            return 0.0
        revelacion = datetime.fromisoformat(sigilo["fecha_revelacion"])
        delta = (revelacion - datetime.now()).total_seconds() / 86400
        return round(delta, 1)

    @classmethod
    def revelaciones_pendientes(cls, proyecto_hash: str) -> list[dict]:
        """Sigilos en olvido cuyo plazo ya venció."""
        olvidados = cls.listar(proyecto_hash, estado="olvidado")
        return [s for s in olvidados if cls.dias_restantes_olvido(s) <= 0]
