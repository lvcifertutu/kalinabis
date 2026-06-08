"""Repo de esferas colectivas (El Árbol global) y sus marcas de proyecto."""

import json
from datetime import datetime

from base_datos._helpers import _conexion, _ph, MODO_PG


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS esferas (
            id              {pk},
            tipo            TEXT NOT NULL,
            clave_unica     TEXT NOT NULL,
            metadata_json   TEXT,
            amplitud        REAL NOT NULL DEFAULT 1.0,
            fase_decaimiento TEXT DEFAULT 'activa',
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL,
            UNIQUE (tipo, clave_unica)
        )
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS marcas_esfera (
            id              {pk},
            tipo_esfera     TEXT NOT NULL,
            clave_esfera    TEXT NOT NULL,
            proyecto_hash   TEXT NOT NULL,
            timestamp       TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_esferas_tipo
        ON esferas (tipo)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_esferas_clave
        ON esferas (tipo, clave_unica)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_marcas_esfera_tipo
        ON marcas_esfera (tipo_esfera, clave_esfera)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS relaciones_esfera (
            id              {pk},
            tipo_a          TEXT NOT NULL,
            clave_a         TEXT NOT NULL,
            tipo_b          TEXT NOT NULL,
            clave_b         TEXT NOT NULL,
            tipo_relacion   TEXT NOT NULL,
            fuerza          REAL NOT NULL DEFAULT 1.0,
            proyecto_hash   TEXT,
            creado_en       TEXT NOT NULL,
            UNIQUE (tipo_a, clave_a, tipo_b, clave_b, tipo_relacion)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_rel_esfera_a
        ON relaciones_esfera (tipo_a, clave_a)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_rel_esfera_b
        ON relaciones_esfera (tipo_b, clave_b)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS bosque_eventos (
            id          {pk},
            tipo_evento TEXT NOT NULL,
            tipo_esfera TEXT NOT NULL,
            clave_esfera TEXT NOT NULL,
            detalle_json TEXT,
            amplitud_momento REAL,
            proyecto_hash TEXT,
            entidad TEXT,
            ocurrido_en TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bosque_eventos_clave
        ON bosque_eventos (tipo_esfera, clave_esfera)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bosque_eventos_tipo
        ON bosque_eventos (tipo_evento)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bosque_eventos_fecha
        ON bosque_eventos (ocurrido_en)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS bosque_convergencias (
            id              {pk},
            tipo_a          TEXT NOT NULL,
            clave_a         TEXT NOT NULL,
            tipo_b          TEXT NOT NULL,
            clave_b         TEXT NOT NULL,
            n_proyectos     INTEGER NOT NULL DEFAULT 3,
            primera_vez     TEXT NOT NULL,
            ultima_vez      TEXT NOT NULL,
            activa          INTEGER NOT NULL DEFAULT 1,
            UNIQUE (tipo_a, clave_a, tipo_b, clave_b)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_convergencias_activas
        ON bosque_convergencias (activa, ultima_vez)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS humus_bosque (
            id              {pk},
            tipo            TEXT NOT NULL,
            clave_unica     TEXT NOT NULL,
            causa           TEXT NOT NULL,
            amplitud_final  REAL NOT NULL DEFAULT 0.0,
            dias_activa     REAL NOT NULL DEFAULT 0.0,
            ofrendas_count  INTEGER NOT NULL DEFAULT 0,
            absorbida_por   TEXT,
            disuelto_en     TEXT NOT NULL,
            UNIQUE (tipo, clave_unica)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_humus_tipo
        ON humus_bosque (tipo)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS esfera_ofrendas (
            id              {pk},
            tipo_esfera     TEXT NOT NULL,
            clave_esfera    TEXT NOT NULL,
            texto           TEXT NOT NULL,
            proyecto_hash   TEXT,
            entidad         TEXT,
            creado_en       TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_ofrendas_esfera
        ON esfera_ofrendas (tipo_esfera, clave_esfera)
    """)


class EsferaRepo:
    TABLA = "esferas"
    TABLA_MARCAS = "marcas_esfera"

    INCREMENTO_MARCA = 0.3
    AMPLITUD_MAX = 5.0

    @classmethod
    def crear_o_actualizar(cls, tipo: str, clave_unica: str,
                           metadata: dict | None = None) -> dict:
        ahora = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else "{}"
        with _conexion() as (con, cur):
            if MODO_PG:
                cur.execute(
                    f"INSERT INTO {cls.TABLA} "
                    f"(tipo, clave_unica, metadata_json, amplitud, "
                    f"fase_decaimiento, created_at, updated_at) "
                    f"VALUES ({_ph(7)}) "
                    f"ON CONFLICT (tipo, clave_unica) DO UPDATE SET "
                    f"amplitud = LEAST({cls.TABLA}.amplitud + %s, %s), "
                    f"fase_decaimiento = 'activa', updated_at = %s",
                    (tipo, clave_unica, metadata_json,
                     cls.INCREMENTO_MARCA, cls.AMPLITUD_MAX,
                     ahora, ahora)
                )
            else:
                existe = cls.obtener(tipo, clave_unica)
                if existe:
                    amp_antes = existe["amplitud"]
                    nueva_amp = min(amp_antes + cls.INCREMENTO_MARCA, cls.AMPLITUD_MAX)
                    cur.execute(
                        f"UPDATE {cls.TABLA} SET "
                        f"amplitud = {_ph(1)}, fase_decaimiento = 'activa', "
                        f"updated_at = {_ph(1)} "
                        f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                        (nueva_amp, ahora, tipo, clave_unica)
                    )
                    # Evento: esfera_maxima (solo al cruzar el umbral)
                    if amp_antes < cls.AMPLITUD_MAX and nueva_amp >= cls.AMPLITUD_MAX:
                        cls._registrar_evento_lazy(
                            "esfera_maxima", tipo, clave_unica, nueva_amp
                        )
                else:
                    # ¿Hay humus acumulado en este lugar? Si sí, la esfera nace más fuerte
                    bonus = HumusRepo.bonus_inicial(tipo, clave_unica)
                    amp_inicial = round(1.0 + bonus, 4)
                    cur.execute(
                        f"INSERT INTO {cls.TABLA} "
                        f"(tipo, clave_unica, metadata_json, amplitud, "
                        f"fase_decaimiento, created_at, updated_at) "
                        f"VALUES ({_ph(7)})",
                        (tipo, clave_unica, metadata_json, amp_inicial,
                         "activa", ahora, ahora)
                    )
                    cls._registrar_evento_lazy(
                        "esfera_nace", tipo, clave_unica, amp_inicial,
                        detalle={"humus_bonus": bonus} if bonus > 0 else None,
                    )
        return cls.obtener(tipo, clave_unica)

    @classmethod
    def _registrar_evento_lazy(cls, tipo_evento: str, tipo_esfera: str,
                               clave_esfera: str, amplitud: float,
                               detalle: dict | None = None, **kwargs) -> None:
        EventoRepo.registrar(
            tipo_evento, tipo_esfera, clave_esfera,
            amplitud_momento=amplitud,
            detalle=detalle,
            **kwargs,
        )

    @classmethod
    def obtener(cls, tipo: str, clave_unica: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                f"fase_decaimiento, created_at, updated_at "
                f"FROM {cls.TABLA} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica)
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "tipo": row[0],
                "clave_unica": row[1],
                "metadata": json.loads(row[2]) if row[2] else {},
                "amplitud": row[3],
                "fase_decaimiento": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }

    @classmethod
    def listar_activas(cls, tipo: str | None = None,
                       amplitud_minima: float = 0.01) -> list[dict]:
        with _conexion() as (con, cur):
            if tipo:
                cur.execute(
                    f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                    f"fase_decaimiento, created_at, updated_at "
                    f"FROM {cls.TABLA} "
                    f"WHERE tipo = {_ph(1)} AND amplitud >= {_ph(1)} "
                    f"ORDER BY amplitud DESC",
                    (tipo, amplitud_minima)
                )
            else:
                cur.execute(
                    f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                    f"fase_decaimiento, created_at, updated_at "
                    f"FROM {cls.TABLA} "
                    f"WHERE amplitud >= {_ph(1)} "
                    f"ORDER BY amplitud DESC",
                    (amplitud_minima,)
                )
            return [
                {
                    "tipo": r[0],
                    "clave_unica": r[1],
                    "metadata": json.loads(r[2]) if r[2] else {},
                    "amplitud": r[3],
                    "fase_decaimiento": r[4],
                    "created_at": r[5],
                    "updated_at": r[6],
                }
                for r in cur.fetchall()
            ]

    @classmethod
    def agregar_marca(cls, tipo_esfera: str, clave_esfera: str,
                      proyecto_hash: str):
        p = _ph(4)
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.TABLA_MARCAS} "
                f"(tipo_esfera, clave_esfera, proyecto_hash, timestamp) "
                f"VALUES ({p})",
                (tipo_esfera, clave_esfera, proyecto_hash, ahora)
            )

    @classmethod
    def contar_marcas_recientes(cls, tipo_esfera: str, clave_esfera: str,
                                desde_dias: int = 30) -> int:
        from datetime import timedelta
        limite = (datetime.now() - timedelta(days=desde_dias)).isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT COUNT(DISTINCT proyecto_hash) FROM {cls.TABLA_MARCAS} "
                f"WHERE tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)} "
                f"AND timestamp >= {_ph(1)}",
                (tipo_esfera, clave_esfera, limite)
            )
            return cur.fetchone()[0]

    @classmethod
    def aplicar_decaimiento(cls, tipo: str, clave_unica: str,
                            factor: float = 0.9,
                            amplitud_minima: float = 0.01):
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT amplitud FROM {cls.TABLA} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica)
            )
            row = cur.fetchone()
            if not row:
                return
            nueva = max(row[0] * factor, amplitud_minima)
            fase = "activa" if nueva > 0.1 else "latente"
            ahora = datetime.now().isoformat()
            cur.execute(
                f"UPDATE {cls.TABLA} SET amplitud = {_ph(1)}, "
                f"fase_decaimiento = {_ph(1)}, updated_at = {_ph(1)} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (nueva, fase, ahora, tipo, clave_unica)
            )

    @classmethod
    def listar_todas(cls) -> list[dict]:
        """Todas las esferas sin filtro de amplitud (incluye disolviendo/disuelta)."""
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo, clave_unica, metadata_json, amplitud, "
                f"fase_decaimiento, created_at, updated_at "
                f"FROM {cls.TABLA} ORDER BY amplitud DESC"
            )
            return [
                {
                    "tipo": r[0], "clave_unica": r[1],
                    "metadata": json.loads(r[2]) if r[2] else {},
                    "amplitud": r[3], "fase_decaimiento": r[4],
                    "created_at": r[5], "updated_at": r[6],
                }
                for r in cur.fetchall()
            ]

    @classmethod
    def actualizar_fase_decaimiento(cls, tipo: str, clave_unica: str,
                                    amp_nueva: float, nueva_fase: str) -> None:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.TABLA} SET "
                f"amplitud = {_ph(1)}, fase_decaimiento = {_ph(1)}, updated_at = {_ph(1)} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (amp_nueva, nueva_fase, ahora, tipo, clave_unica),
            )

    @classmethod
    def marcas_por_proyecto(cls, proyecto_hash: str) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo_esfera, clave_esfera, timestamp FROM {cls.TABLA_MARCAS} "
                f"WHERE proyecto_hash = {_ph(1)} ORDER BY timestamp DESC",
                (proyecto_hash,)
            )
            return [
                {"tipo": r[0], "clave": r[1], "timestamp": r[2]}
                for r in cur.fetchall()
            ]

    @classmethod
    def eliminar(cls, tipo: str, clave_unica: str):
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM {cls.TABLA} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica)
            )
            cur.execute(
                f"DELETE FROM {cls.TABLA_MARCAS} "
                f"WHERE tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)}",
                (tipo, clave_unica)
            )


# ── Tipos de relación entre esferas ────────────────────────────────────────
#
#   convoca   — una intención activa convoca energía en un lugar (intencion→geo)
#   toca      — una sincronicidad revela un elemento latente (sincronicidad→elemental)
#   ancla     — conocimiento biblioteca fundamenta un concepto (conocimiento→tematica)
#   coemerge   — dos esferas distintas marcadas por el mismo proyecto en < 1 hora
#   polariza   — elementales opuestos en alta tensión simultánea (fuego↔agua, tierra↔aire)
#   amplifica  — una esfera de conocimiento eleva una temática del mismo dominio

TIPOS_RELACION = frozenset([
    "convoca", "toca", "ancla", "coemergencia", "polariza", "amplifica",
    "resuena",   # convergencia colectiva: N proyectos tocaron ambas esferas
])

PARES_POLARES = {
    frozenset(["fuego", "agua"]),
    frozenset(["tierra", "aire"]),
}

INCREMENTO_FUERZA = 0.5
FUERZA_MAX = 5.0


class RelacionRepo:
    T = "relaciones_esfera"

    @classmethod
    def crear_o_fortalecer(
        cls,
        tipo_a: str, clave_a: str,
        tipo_b: str, clave_b: str,
        tipo_relacion: str,
        proyecto_hash: str | None = None,
    ) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, fuerza FROM {cls.T} "
                f"WHERE tipo_a = {_ph(1)} AND clave_a = {_ph(1)} "
                f"AND tipo_b = {_ph(1)} AND clave_b = {_ph(1)} "
                f"AND tipo_relacion = {_ph(1)}",
                (tipo_a, clave_a, tipo_b, clave_b, tipo_relacion),
            )
            row = cur.fetchone()
            if row:
                nueva_fuerza = min(row[1] + INCREMENTO_FUERZA, FUERZA_MAX)
                cur.execute(
                    f"UPDATE {cls.T} SET fuerza = {_ph(1)} WHERE id = {_ph(1)}",
                    (nueva_fuerza, row[0]),
                )
                return {"tipo_relacion": tipo_relacion, "fuerza": nueva_fuerza, "nueva": False}
            else:
                cur.execute(
                    f"INSERT INTO {cls.T} "
                    f"(tipo_a, clave_a, tipo_b, clave_b, tipo_relacion, fuerza, proyecto_hash, creado_en) "
                    f"VALUES ({_ph(8)})",
                    (tipo_a, clave_a, tipo_b, clave_b, tipo_relacion,
                     1.0, proyecto_hash, ahora),
                )
                return {"tipo_relacion": tipo_relacion, "fuerza": 1.0, "nueva": True}

    @classmethod
    def listar_de(cls, tipo: str, clave: str) -> list[dict]:
        """Retorna todas las relaciones donde esta esfera es origen o destino."""
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo_a, clave_a, tipo_b, clave_b, tipo_relacion, fuerza, creado_en "
                f"FROM {cls.T} "
                f"WHERE (tipo_a = {_ph(1)} AND clave_a = {_ph(1)}) "
                f"   OR (tipo_b = {_ph(1)} AND clave_b = {_ph(1)}) "
                f"ORDER BY fuerza DESC",
                (tipo, clave, tipo, clave),
            )
            return [
                {"tipo_a": r[0], "clave_a": r[1],
                 "tipo_b": r[2], "clave_b": r[3],
                 "tipo_relacion": r[4], "fuerza": r[5], "creado_en": r[6]}
                for r in cur.fetchall()
            ]

    @classmethod
    def listar_todas(cls, fuerza_min: float = 0.5) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo_a, clave_a, tipo_b, clave_b, tipo_relacion, fuerza, creado_en "
                f"FROM {cls.T} WHERE fuerza >= {_ph(1)} ORDER BY fuerza DESC",
                (fuerza_min,),
            )
            return [
                {"tipo_a": r[0], "clave_a": r[1],
                 "tipo_b": r[2], "clave_b": r[3],
                 "tipo_relacion": r[4], "fuerza": r[5], "creado_en": r[6]}
                for r in cur.fetchall()
            ]


# ── Tipos de evento del bosque ──────────────────────────────────────────────
#
#   esfera_nace       — primera vez que se registra esta esfera
#   esfera_maxima     — esfera alcanza amplitud máxima (5.0)
#   esfera_disuelve   — esfera llega a amplitud 0 tras decaimiento
#   rito_origen       — esfera nació durante una invocación (entidad conocida)
#   polarizacion      — dos elementales opuestos alcanzan tensión simultánea
#   coemergencia      — dos esferas de distinto tipo surgen en la misma hora de proyecto

TIPOS_EVENTO = frozenset([
    "esfera_nace", "esfera_maxima", "esfera_disuelve",
    "rito_origen", "polarizacion", "coemergencia",
    "convergencia",   # señal colectiva: N proyectos independientes tocaron el mismo par
])


class EventoRepo:
    T = "bosque_eventos"

    @classmethod
    def registrar(
        cls,
        tipo_evento: str,
        tipo_esfera: str,
        clave_esfera: str,
        amplitud_momento: float = 0.0,
        detalle: dict | None = None,
        proyecto_hash: str | None = None,
        entidad: str | None = None,
    ) -> None:
        ahora = datetime.now().isoformat()
        detalle_json = json.dumps(detalle, ensure_ascii=False) if detalle else None
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.T} "
                f"(tipo_evento, tipo_esfera, clave_esfera, detalle_json, "
                f"amplitud_momento, proyecto_hash, entidad, ocurrido_en) "
                f"VALUES ({_ph(8)})",
                (tipo_evento, tipo_esfera, clave_esfera, detalle_json,
                 amplitud_momento, proyecto_hash, entidad, ahora),
            )

    @classmethod
    def listar(
        cls,
        tipo_evento: str | None = None,
        tipo_esfera: str | None = None,
        clave_esfera: str | None = None,
        limite: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        conds, params = [], []
        if tipo_evento:
            conds.append(f"tipo_evento = {_ph(1)}")
            params.append(tipo_evento)
        if tipo_esfera:
            conds.append(f"tipo_esfera = {_ph(1)}")
            params.append(tipo_esfera)
        if clave_esfera:
            conds.append(f"clave_esfera = {_ph(1)}")
            params.append(clave_esfera)
        where = ("WHERE " + " AND ".join(conds)) if conds else ""
        params += [limite, offset]
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo_evento, tipo_esfera, clave_esfera, detalle_json, "
                f"amplitud_momento, proyecto_hash, entidad, ocurrido_en "
                f"FROM {cls.T} {where} "
                f"ORDER BY ocurrido_en DESC "
                f"LIMIT {_ph(1)} OFFSET {_ph(1)}",
                params,
            )
            return [
                {
                    "tipo_evento": r[0],
                    "tipo_esfera": r[1],
                    "clave_esfera": r[2],
                    "detalle": json.loads(r[3]) if r[3] else {},
                    "amplitud_momento": r[4],
                    "proyecto_hash": r[5],
                    "entidad": r[6],
                    "ocurrido_en": r[7],
                }
                for r in cur.fetchall()
            ]

    @classmethod
    def cronica(cls, limite: int = 20) -> list[dict]:
        """Últimos eventos significativos del bosque, enriquecidos con texto narrativo."""
        eventos = cls.listar(limite=limite)
        for ev in eventos:
            ev["narrativa"] = _narrativa_evento(ev)
        return eventos


UMBRAL_CONVERGENCIA = 3       # proyectos independientes mínimos para señal
VENTANA_CONVERGENCIA_H = 24  # horas de ventana temporal


class ConvergenciaRepo:
    T = "bosque_convergencias"

    @classmethod
    def _par_normalizado(cls, ta: str, ca: str, tb: str, cb: str) -> tuple:
        """Ordena lexicográficamente para que (A,B) y (B,A) sean el mismo par."""
        if (ta, ca) <= (tb, cb):
            return ta, ca, tb, cb
        return tb, cb, ta, ca

    @classmethod
    def detectar_para(
        cls,
        tipo: str,
        clave: str,
        ventana_horas: int = VENTANA_CONVERGENCIA_H,
        umbral: int = UMBRAL_CONVERGENCIA,
    ) -> list[dict]:
        """Detecta convergencias nuevas o reforzadas para una esfera recién marcada.

        Algoritmo:
        1. Encuentra proyectos que marcaron (tipo, clave) en la ventana.
        2. Si hay < umbral proyectos, no hay señal posible — termina.
        3. Busca qué otras esferas esos proyectos también marcaron en la ventana.
        4. Filtra las que tengan >= umbral proyectos en común.
        5. Registra/actualiza cada par como convergencia.

        Retorna la lista de convergencias detectadas (nuevas o reforzadas).
        """
        from datetime import timedelta
        limite = (datetime.now() - timedelta(hours=ventana_horas)).isoformat()

        with _conexion() as (con, cur):
            # Paso 1: proyectos que marcaron esta esfera en la ventana
            cur.execute(
                f"SELECT DISTINCT proyecto_hash FROM marcas_esfera "
                f"WHERE tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)} "
                f"AND timestamp >= {_ph(1)} AND proyecto_hash IS NOT NULL",
                (tipo, clave, limite),
            )
            proyectos = [r[0] for r in cur.fetchall()]

        if len(proyectos) < umbral:
            return []

        # Paso 2: qué otras esferas esos proyectos también marcaron
        ph_list = ",".join(_ph(1) for _ in proyectos)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo_esfera, clave_esfera, COUNT(DISTINCT proyecto_hash) "
                f"FROM marcas_esfera "
                f"WHERE proyecto_hash IN ({ph_list}) "
                f"AND NOT (tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)}) "
                f"AND timestamp >= {_ph(1)} "
                f"GROUP BY tipo_esfera, clave_esfera "
                f"HAVING COUNT(DISTINCT proyecto_hash) >= {_ph(1)}",
                (*proyectos, tipo, clave, limite, umbral),
            )
            pares = [(r[0], r[1], r[2]) for r in cur.fetchall()]

        ahora = datetime.now().isoformat()
        detectadas = []
        for tipo_b, clave_b, n in pares:
            ta, ca, tb, cb = cls._par_normalizado(tipo, clave, tipo_b, clave_b)
            with _conexion() as (con, cur):
                cur.execute(
                    f"SELECT id, n_proyectos FROM {cls.T} "
                    f"WHERE tipo_a = {_ph(1)} AND clave_a = {_ph(1)} "
                    f"AND tipo_b = {_ph(1)} AND clave_b = {_ph(1)}",
                    (ta, ca, tb, cb),
                )
                row = cur.fetchone()
                if row:
                    nueva = n > row[1]  # refuerzo si más proyectos que antes
                    cur.execute(
                        f"UPDATE {cls.T} SET n_proyectos = {_ph(1)}, "
                        f"ultima_vez = {_ph(1)}, activa = 1 WHERE id = {_ph(1)}",
                        (n, ahora, row[0]),
                    )
                else:
                    nueva = True
                    cur.execute(
                        f"INSERT INTO {cls.T} "
                        f"(tipo_a, clave_a, tipo_b, clave_b, n_proyectos, "
                        f"primera_vez, ultima_vez, activa) "
                        f"VALUES ({_ph(8)})",
                        (ta, ca, tb, cb, n, ahora, ahora, 1),
                    )
            detectadas.append({
                "tipo_a": ta, "clave_a": ca,
                "tipo_b": tb, "clave_b": cb,
                "n_proyectos": n,
                "nueva": nueva,
                "detectada_en": ahora,
            })
        return detectadas

    @classmethod
    def listar_activas(cls, limite: int = 20) -> list[dict]:
        """Convergencias activas ordenadas por número de proyectos y recencia."""
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo_a, clave_a, tipo_b, clave_b, n_proyectos, "
                f"primera_vez, ultima_vez "
                f"FROM {cls.T} WHERE activa = 1 "
                f"ORDER BY n_proyectos DESC, ultima_vez DESC "
                f"LIMIT {_ph(1)}",
                (limite,),
            )
            return [
                {
                    "tipo_a": r[0], "clave_a": r[1],
                    "tipo_b": r[2], "clave_b": r[3],
                    "n_proyectos": r[4],
                    "primera_vez": r[5],
                    "ultima_vez":  r[6],
                }
                for r in cur.fetchall()
            ]

    @classmethod
    def expirar_antiguas(cls, ventana_horas: int = VENTANA_CONVERGENCIA_H) -> int:
        """Marca como inactivas las convergencias cuya última señal fue hace > ventana."""
        from datetime import timedelta
        limite = (datetime.now() - timedelta(hours=ventana_horas)).isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.T} SET activa = 0 "
                f"WHERE ultima_vez < {_ph(1)} AND activa = 1",
                (limite,),
            )
            return cur.rowcount


class HumusRepo:
    T = "humus_bosque"

    # Bonus de amplitud inicial cuando nace una esfera sobre humus propio
    BONUS_HUMUS = 0.5
    BONUS_HUMUS_ABSORBIDA = 0.2   # menor si murió siendo absorbida (energía ya fue a otra)

    @classmethod
    def depositar(
        cls,
        tipo: str,
        clave_unica: str,
        causa: str,
        amplitud_final: float,
        dias_activa: float,
        ofrendas_count: int = 0,
        absorbida_por: str | None = None,
    ) -> None:
        """Registra el humus de una esfera disuelta. Idempotente (UNIQUE en tipo+clave)."""
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            # Si ya existe (esfera renacida y vuelta a morir) actualizar acumulando
            cur.execute(
                f"SELECT id, dias_activa, ofrendas_count FROM {cls.T} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica),
            )
            row = cur.fetchone()
            if row:
                cur.execute(
                    f"UPDATE {cls.T} SET "
                    f"causa = {_ph(1)}, amplitud_final = {_ph(1)}, "
                    f"dias_activa = {_ph(1)}, ofrendas_count = {_ph(1)}, "
                    f"absorbida_por = {_ph(1)}, disuelto_en = {_ph(1)} "
                    f"WHERE id = {_ph(1)}",
                    (
                        causa,
                        amplitud_final,
                        row[1] + dias_activa,          # acumula días totales
                        row[2] + ofrendas_count,        # acumula ofrendas totales
                        absorbida_por,
                        ahora,
                        row[0],
                    ),
                )
            else:
                cur.execute(
                    f"INSERT INTO {cls.T} "
                    f"(tipo, clave_unica, causa, amplitud_final, dias_activa, "
                    f"ofrendas_count, absorbida_por, disuelto_en) "
                    f"VALUES ({_ph(8)})",
                    (tipo, clave_unica, causa, amplitud_final, dias_activa,
                     ofrendas_count, absorbida_por, ahora),
                )

    @classmethod
    def bonus_inicial(cls, tipo: str, clave_unica: str) -> float:
        """Retorna el bonus de amplitud que el humus acumulado otorga a una esfera nueva."""
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT causa, dias_activa, ofrendas_count FROM {cls.T} "
                f"WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica),
            )
            row = cur.fetchone()
            if not row:
                return 0.0
            causa, dias, ofrendas = row
            base = cls.BONUS_HUMUS if causa != "absorbida" else cls.BONUS_HUMUS_ABSORBIDA
            # Bonus adicional proporcional a días de vida y ofrendas
            extra = min(dias / 30.0 * 0.1 + ofrendas * 0.05, 0.8)
            return round(base + extra, 2)

    @classmethod
    def obtener(cls, tipo: str, clave_unica: str) -> dict | None:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo, clave_unica, causa, amplitud_final, dias_activa, "
                f"ofrendas_count, absorbida_por, disuelto_en "
                f"FROM {cls.T} WHERE tipo = {_ph(1)} AND clave_unica = {_ph(1)}",
                (tipo, clave_unica),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "tipo": row[0], "clave_unica": row[1], "causa": row[2],
                "amplitud_final": row[3], "dias_activa": row[4],
                "ofrendas_count": row[5], "absorbida_por": row[6],
                "disuelto_en": row[7],
            }

    @classmethod
    def listar(cls, tipo: str | None = None, limite: int = 50) -> list[dict]:
        conds, params = [], []
        if tipo:
            conds.append(f"tipo = {_ph(1)}")
            params.append(tipo)
        where = ("WHERE " + " AND ".join(conds)) if conds else ""
        params.append(limite)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo, clave_unica, causa, amplitud_final, dias_activa, "
                f"ofrendas_count, absorbida_por, disuelto_en "
                f"FROM {cls.T} {where} "
                f"ORDER BY disuelto_en DESC LIMIT {_ph(1)}",
                params,
            )
            return [
                {
                    "tipo": r[0], "clave_unica": r[1], "causa": r[2],
                    "amplitud_final": r[3], "dias_activa": r[4],
                    "ofrendas_count": r[5], "absorbida_por": r[6],
                    "disuelto_en": r[7],
                }
                for r in cur.fetchall()
            ]


class OfrendaRepo:
    T = "esfera_ofrendas"

    @classmethod
    def dejar(
        cls,
        tipo_esfera: str,
        clave_esfera: str,
        texto: str,
        proyecto_hash: str | None = None,
        entidad: str | None = None,
    ) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.T} "
                f"(tipo_esfera, clave_esfera, texto, proyecto_hash, entidad, creado_en) "
                f"VALUES ({_ph(6)})",
                (tipo_esfera, clave_esfera, texto, proyecto_hash, entidad, ahora),
            )
        return {"tipo_esfera": tipo_esfera, "clave_esfera": clave_esfera,
                "texto": texto, "creado_en": ahora}

    @classmethod
    def listar(
        cls,
        tipo_esfera: str,
        clave_esfera: str,
        limite: int = 30,
    ) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT texto, entidad, creado_en "
                f"FROM {cls.T} "
                f"WHERE tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)} "
                f"ORDER BY creado_en DESC LIMIT {_ph(1)}",
                (tipo_esfera, clave_esfera, limite),
            )
            return [
                {"texto": r[0], "entidad": r[1], "creado_en": r[2]}
                for r in cur.fetchall()
            ]

    @classmethod
    def conteo(cls, tipo_esfera: str, clave_esfera: str) -> int:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT COUNT(*) FROM {cls.T} "
                f"WHERE tipo_esfera = {_ph(1)} AND clave_esfera = {_ph(1)}",
                (tipo_esfera, clave_esfera),
            )
            return cur.fetchone()[0]

    @classmethod
    def esferas_visitadas_por_proyecto(
        cls, proyecto_hash: str, limite: int = 5
    ) -> list[dict]:
        """Esferas donde este proyecto dejó ofrenda recientemente."""
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT DISTINCT tipo_esfera, clave_esfera, MAX(creado_en) as ultima "
                f"FROM {cls.T} "
                f"WHERE proyecto_hash = {_ph(1)} "
                f"GROUP BY tipo_esfera, clave_esfera "
                f"ORDER BY ultima DESC LIMIT {_ph(1)}",
                (proyecto_hash, limite),
            )
            return [
                {"tipo_esfera": r[0], "clave_esfera": r[1], "ultima_visita": r[2]}
                for r in cur.fetchall()
            ]


def _narrativa_evento(ev: dict) -> str:
    """Genera una frase descriptiva para mostrar en el registro del bosque."""
    tipo = ev["tipo_evento"]
    esfera = f"{ev['tipo_esfera']}:{ev['clave_esfera']}"
    amp = ev.get("amplitud_momento", 0)
    entidad = ev.get("entidad") or "lo desconocido"
    detalle = ev.get("detalle") or {}

    if tipo == "esfera_nace":
        return f"Nació una nueva esfera — {esfera} (amplitud inicial {amp:.2f})"
    if tipo == "esfera_maxima":
        return f"La esfera {esfera} alcanzó su amplitud máxima — el bosque vibra"
    if tipo == "esfera_disuelve":
        return f"La esfera {esfera} se disolvió — su humus queda en el suelo"
    if tipo == "rito_origen":
        return (f"La esfera {esfera} emergió del rito de {entidad} — "
                f"nació marcada por {detalle.get('ubicacion', 'el vacío')}")
    if tipo == "polarizacion":
        otro = detalle.get("esfera_polar", "?")
        return (f"Tensión polar detectada: {esfera} y {otro} se oponen "
                f"con fuerza {detalle.get('fuerza_polar', 0):.2f}")
    if tipo == "coemergencia":
        otro = detalle.get("esfera_par", "?")
        return f"Co-emergencia: {esfera} y {otro} brotaron juntas en la misma hora"
    if tipo == "convergencia":
        n = detalle.get("n_proyectos", "?")
        par_b = detalle.get("par_b", "?")
        return (
            f"Señal colectiva: {n} proyectos independientes "
            f"convergieron en {esfera} y {par_b} — algo emerge sin coordinación"
        )
    return f"Evento {tipo} en {esfera}"
