"""Repo de la Biblioteca Comunitaria de Kalinabis.

Cuatro tablas:
  biblioteca_entradas      — el conocimiento documentado
  biblioteca_fuentes       — citas/fuentes de cada entrada
  biblioteca_contribuciones — ediciones y expansiones propuestas
  biblioteca_resonancias   — marcas de validación comunitaria (anónimas)
"""

from datetime import datetime
from hashlib import sha256
from typing import Optional

from base_datos._helpers import (
    _conexion_bib as _conexion,
    _ph_bib as _ph,
    _serial_bib as _serial,
    _id_ultimo_bib,
)


# ── Pesos de resonancia ────────────────────────────────────────────────────

PESOS_RESONANCIA = {
    "reconozco": 0.5,
    "verifico":  1.0,
    "cuestiono": -0.5,
    "amplio":    0.2,
}

TIPOS_RESONANCIA = set(PESOS_RESONANCIA.keys())
TIPOS_FUENTE = {
    "texto_primario", "libro", "articulo",
    "tradicion_oral", "experiencia_directa",
}
TIPOS_CONTRIBUCION = {"expansion", "correccion", "fuente", "cuestionamiento"}
ESTADOS_ENTRADA = {"semilla", "brote", "arbol", "canon", "humus"}


# ── Schema ─────────────────────────────────────────────────────────────────

def _inicializar_local():
    """Crea las tablas de biblioteca en el adaptador local.

    Solo para desarrollo sin SUPABASE_DB_URL. En producción, usar
    migrations/biblioteca_supabase.sql directamente en Supabase.
    """
    pk = f"{_serial()} PRIMARY KEY"
    with _conexion() as (con, cur):
        _crear_tablas(cur, pk)


def _crear_tablas(cur, pk: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS biblioteca_entradas (
            id           {pk},
            titulo       TEXT NOT NULL,
            slug         TEXT NOT NULL UNIQUE,
            dominio      TEXT NOT NULL,
            contenido    TEXT NOT NULL,
            estado       TEXT NOT NULL DEFAULT 'semilla',
            fuentes_count INTEGER NOT NULL DEFAULT 0,
            resonancia   REAL NOT NULL DEFAULT 0.0,
            hash_autor   TEXT,
            creado_en    TEXT NOT NULL,
            actualizado_en TEXT NOT NULL
        )
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS biblioteca_fuentes (
            id          {pk},
            entrada_id  INTEGER NOT NULL
                            REFERENCES biblioteca_entradas(id),
            tipo        TEXT NOT NULL,
            referencia  TEXT NOT NULL,
            verificada  INTEGER NOT NULL DEFAULT 0,
            creado_en   TEXT NOT NULL
        )
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS biblioteca_contribuciones (
            id              {pk},
            entrada_id      INTEGER NOT NULL
                                REFERENCES biblioteca_entradas(id),
            tipo            TEXT NOT NULL,
            contenido       TEXT NOT NULL,
            estado          TEXT NOT NULL DEFAULT 'pendiente',
            resonancia_pro  INTEGER NOT NULL DEFAULT 0,
            resonancia_contra INTEGER NOT NULL DEFAULT 0,
            hash_autor      TEXT,
            creado_en       TEXT NOT NULL
        )
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS biblioteca_resonancias (
            id           {pk},
            entrada_id   INTEGER NOT NULL
                             REFERENCES biblioteca_entradas(id),
            tipo         TEXT NOT NULL,
            hash_proyecto TEXT NOT NULL,
            creado_en    TEXT NOT NULL,
            UNIQUE (entrada_id, hash_proyecto, tipo)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bib_entradas_slug
        ON biblioteca_entradas (slug)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bib_entradas_dominio
        ON biblioteca_entradas (dominio)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bib_fuentes_entrada
        ON biblioteca_fuentes (entrada_id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bib_contrib_entrada
        ON biblioteca_contribuciones (entrada_id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bib_reson_entrada
        ON biblioteca_resonancias (entrada_id)
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS biblioteca_constelaciones (
            id             {pk},
            nombre         TEXT NOT NULL,
            descripcion    TEXT,
            criterio       TEXT,
            hash_proyecto  TEXT NOT NULL,
            color          TEXT NOT NULL DEFAULT 'indigo',
            creado_en      TEXT NOT NULL,
            actualizado_en TEXT NOT NULL
        )
    """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS biblioteca_constelacion_entradas (
            id               {pk},
            constelacion_id  INTEGER NOT NULL
                                 REFERENCES biblioteca_constelaciones(id)
                                 ON DELETE CASCADE,
            entrada_id       INTEGER NOT NULL
                                 REFERENCES biblioteca_entradas(id)
                                 ON DELETE CASCADE,
            nota             TEXT,
            orden            INTEGER NOT NULL DEFAULT 0,
            creado_en        TEXT NOT NULL,
            UNIQUE (constelacion_id, entrada_id)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bib_constel_proyecto
        ON biblioteca_constelaciones (hash_proyecto)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bib_constel_entradas_constel
        ON biblioteca_constelacion_entradas (constelacion_id)
    """)


# ── Helpers internos ───────────────────────────────────────────────────────

def _calcular_estado(entrada: dict) -> str:
    """Recalcula el estado según las reglas del Bosque del Saber.

    El estado 'canon' nunca es recalculado — solo lo asigna sembrar_canon().
    """
    if entrada["estado"] == "canon":
        return "canon"

    fuentes_ok = entrada.get("_fuentes_verificadas", 0)
    resonancia = entrada["resonancia"]
    cuestionamientos = entrada.get("_cuestionamientos_abiertos", 0)

    if fuentes_ok >= 3 and resonancia >= 5.0 and cuestionamientos == 0:
        return "arbol"
    if fuentes_ok >= 1 and resonancia >= 1.0:
        return "brote"
    if resonancia <= -2.0:
        return "humus"
    return "semilla"


def _row_to_entrada(row) -> dict:
    return {
        "id":             row[0],
        "titulo":         row[1],
        "slug":           row[2],
        "dominio":        row[3],
        "contenido":      row[4],
        "estado":         row[5],
        "fuentes_count":  row[6],
        "resonancia":     row[7],
        "hash_autor":     row[8],
        "creado_en":      row[9],
        "actualizado_en": row[10],
    }


# ── EntradaRepo ────────────────────────────────────────────────────────────

class EntradaRepo:
    T = "biblioteca_entradas"

    @classmethod
    def crear(cls, titulo: str, slug: str, dominio: str,
              contenido: str, hash_autor: Optional[str] = None) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.T} "
                f"(titulo, slug, dominio, contenido, estado, "
                f"fuentes_count, resonancia, hash_autor, "
                f"creado_en, actualizado_en) "
                f"VALUES ({_ph(10)})",
                (titulo, slug, dominio, contenido, "semilla",
                 0, 0.0, hash_autor, ahora, ahora),
            )
        return cls.por_slug(slug)

    @classmethod
    def crear_canon(cls, titulo: str, slug: str, dominio: str,
                    contenido: str) -> dict:
        """Inserta o actualiza una entrada con estado 'canon'."""
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id FROM {cls.T} WHERE slug = {_ph(1)}",
                (slug,),
            )
            row = cur.fetchone()
            if row:
                cur.execute(
                    f"UPDATE {cls.T} SET contenido = {_ph(1)}, "
                    f"actualizado_en = {_ph(1)} WHERE slug = {_ph(1)}",
                    (contenido, ahora, slug),
                )
            else:
                cur.execute(
                    f"INSERT INTO {cls.T} "
                    f"(titulo, slug, dominio, contenido, estado, "
                    f"fuentes_count, resonancia, hash_autor, "
                    f"creado_en, actualizado_en) "
                    f"VALUES ({_ph(10)})",
                    (titulo, slug, dominio, contenido, "canon",
                     0, 0.0, None, ahora, ahora),
                )
        return cls.por_slug(slug)

    @classmethod
    def por_slug(cls, slug: str) -> Optional[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, titulo, slug, dominio, contenido, estado, "
                f"fuentes_count, resonancia, hash_autor, "
                f"creado_en, actualizado_en "
                f"FROM {cls.T} WHERE slug = {_ph(1)}",
                (slug,),
            )
            row = cur.fetchone()
            return _row_to_entrada(row) if row else None

    @classmethod
    def listar(cls, dominio: Optional[str] = None,
               estado: Optional[str] = None,
               q: Optional[str] = None,
               hash_autor: Optional[str] = None,
               limite: int = 50,
               offset: int = 0) -> list[dict]:
        conds, params = [], []

        if dominio:
            conds.append(f"dominio = {_ph(1)}")
            params.append(dominio)
        if estado:
            conds.append(f"estado = {_ph(1)}")
            params.append(estado)
        if q:
            conds.append(f"(titulo LIKE {_ph(1)} OR contenido LIKE {_ph(1)})")
            params += [f"%{q}%", f"%{q}%"]
        if hash_autor:
            conds.append(f"hash_autor = {_ph(1)}")
            params.append(hash_autor)

        where = ("WHERE " + " AND ".join(conds)) if conds else ""
        params += [limite, offset]

        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, titulo, slug, dominio, contenido, estado, "
                f"fuentes_count, resonancia, hash_autor, "
                f"creado_en, actualizado_en "
                f"FROM {cls.T} {where} "
                f"ORDER BY resonancia DESC, creado_en DESC "
                f"LIMIT {_ph(1)} OFFSET {_ph(1)}",
                params,
            )
            return [_row_to_entrada(r) for r in cur.fetchall()]

    @classmethod
    def listar_dominios(cls) -> list[str]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT DISTINCT dominio FROM {cls.T} "
                f"WHERE estado != 'humus' ORDER BY dominio"
            )
            return [r[0] for r in cur.fetchall()]

    @classmethod
    def _actualizar_estado(cls, entrada_id: int, slug: str):
        """Recalcula y persiste el estado de una entrada."""
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT estado, resonancia FROM {cls.T} WHERE id = {_ph(1)}",
                (entrada_id,),
            )
            row = cur.fetchone()
            if not row or row[0] == "canon":
                return
            cur.execute(
                f"SELECT COUNT(*) FROM biblioteca_fuentes "
                f"WHERE entrada_id = {_ph(1)}",
                (entrada_id,),
            )
            fuentes_ok = cur.fetchone()[0]
            cur.execute(
                f"SELECT COUNT(*) FROM biblioteca_contribuciones "
                f"WHERE entrada_id = {_ph(1)} AND tipo = 'cuestionamiento' "
                f"AND estado = 'pendiente'",
                (entrada_id,),
            )
            cuestionamientos = cur.fetchone()[0]

            entrada_tmp = {
                "estado": row[0],
                "resonancia": row[1],
                "_fuentes_verificadas": fuentes_ok,
                "_cuestionamientos_abiertos": cuestionamientos,
            }
            nuevo_estado = _calcular_estado(entrada_tmp)
            ahora = datetime.now().isoformat()
            cur.execute(
                f"UPDATE {cls.T} SET estado = {_ph(1)}, "
                f"actualizado_en = {_ph(1)} WHERE id = {_ph(1)}",
                (nuevo_estado, ahora, entrada_id),
            )


# ── FuenteRepo ─────────────────────────────────────────────────────────────

class FuenteRepo:
    T = "biblioteca_fuentes"

    @classmethod
    def agregar(cls, entrada_id: int, tipo: str,
                referencia: str) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.T} "
                f"(entrada_id, tipo, referencia, verificada, creado_en) "
                f"VALUES ({_ph(5)})",
                (entrada_id, tipo, referencia, 0, ahora),
            )
            fuente_id = _id_ultimo_bib(cur)
            cur.execute(
                "UPDATE biblioteca_entradas SET fuentes_count = fuentes_count + 1 "
                f"WHERE id = {_ph(1)}",
                (entrada_id,),
            )
        EntradaRepo._actualizar_estado(entrada_id, "")
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, entrada_id, tipo, referencia, verificada, creado_en "
                f"FROM {cls.T} WHERE id = {_ph(1)}",
                (fuente_id,),
            )
            r = cur.fetchone()
            return {
                "id": r[0], "entrada_id": r[1], "tipo": r[2],
                "referencia": r[3], "verificada": bool(r[4]),
                "creado_en": r[5],
            }

    @classmethod
    def listar(cls, entrada_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, entrada_id, tipo, referencia, verificada, creado_en "
                f"FROM {cls.T} WHERE entrada_id = {_ph(1)} "
                f"ORDER BY creado_en ASC",
                (entrada_id,),
            )
            return [
                {"id": r[0], "entrada_id": r[1], "tipo": r[2],
                 "referencia": r[3], "verificada": bool(r[4]),
                 "creado_en": r[5]}
                for r in cur.fetchall()
            ]


# ── ContribucionRepo ───────────────────────────────────────────────────────

class ContribucionRepo:
    T = "biblioteca_contribuciones"

    @classmethod
    def proponer(cls, entrada_id: int, tipo: str, contenido: str,
                 hash_autor: Optional[str] = None) -> dict:
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.T} "
                f"(entrada_id, tipo, contenido, estado, "
                f"resonancia_pro, resonancia_contra, hash_autor, creado_en) "
                f"VALUES ({_ph(8)})",
                (entrada_id, tipo, contenido, "pendiente",
                 0, 0, hash_autor, ahora),
            )
            cid = _id_ultimo_bib(cur)
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, entrada_id, tipo, contenido, estado, "
                f"resonancia_pro, resonancia_contra, hash_autor, creado_en "
                f"FROM {cls.T} WHERE id = {_ph(1)}",
                (cid,),
            )
            r = cur.fetchone()
            return _row_to_contrib(r)

    @classmethod
    def listar_pendientes(cls, entrada_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, entrada_id, tipo, contenido, estado, "
                f"resonancia_pro, resonancia_contra, hash_autor, creado_en "
                f"FROM {cls.T} "
                f"WHERE entrada_id = {_ph(1)} AND estado = 'pendiente' "
                f"ORDER BY creado_en DESC",
                (entrada_id,),
            )
            return [_row_to_contrib(r) for r in cur.fetchall()]


def _row_to_contrib(r) -> dict:
    return {
        "id": r[0], "entrada_id": r[1], "tipo": r[2],
        "contenido": r[3], "estado": r[4],
        "resonancia_pro": r[5], "resonancia_contra": r[6],
        "hash_autor": r[7], "creado_en": r[8],
    }


# ── ResonanciaRepo ─────────────────────────────────────────────────────────

class ResonanciaRepo:
    T = "biblioteca_resonancias"

    @classmethod
    def marcar(cls, entrada_id: int, tipo: str,
               hash_proyecto: str) -> dict:
        """Añade una marca (idempotente por UNIQUE). Actualiza resonancia y estado."""
        ahora = datetime.now().isoformat()
        peso = PESOS_RESONANCIA[tipo]

        with _conexion() as (con, cur):
            try:
                cur.execute(
                    f"INSERT INTO {cls.T} "
                    f"(entrada_id, tipo, hash_proyecto, creado_en) "
                    f"VALUES ({_ph(4)})",
                    (entrada_id, tipo, hash_proyecto, ahora),
                )
                inserted = True
            except Exception:
                inserted = False

            if inserted:
                cur.execute(
                    f"UPDATE biblioteca_entradas "
                    f"SET resonancia = resonancia + {_ph(1)}, "
                    f"actualizado_en = {_ph(1)} "
                    f"WHERE id = {_ph(1)}",
                    (peso, ahora, entrada_id),
                )

        EntradaRepo._actualizar_estado(entrada_id, "")

        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT resonancia, estado FROM biblioteca_entradas "
                f"WHERE id = {_ph(1)}",
                (entrada_id,),
            )
            r = cur.fetchone()
            return {
                "nueva_resonancia": round(r[0], 2),
                "estado": r[1],
                "ya_marcada": not inserted,
            }

    @classmethod
    def conteo(cls, entrada_id: int) -> dict[str, int]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT tipo, COUNT(*) FROM {cls.T} "
                f"WHERE entrada_id = {_ph(1)} GROUP BY tipo",
                (entrada_id,),
            )
            return {r[0]: r[1] for r in cur.fetchall()}

    @classmethod
    def por_proyecto(cls, hash_proyecto: str) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT r.tipo, r.creado_en, e.slug, e.titulo "
                f"FROM {cls.T} r "
                f"JOIN biblioteca_entradas e ON e.id = r.entrada_id "
                f"WHERE r.hash_proyecto = {_ph(1)} "
                f"ORDER BY r.creado_en DESC",
                (hash_proyecto,),
            )
            return [
                {"tipo": r[0], "fecha": r[1], "slug": r[2], "titulo": r[3]}
                for r in cur.fetchall()
            ]


# ── ConstelacionRepo ───────────────────────────────────────────────────────

def _row_to_constelacion(row) -> dict:
    return {
        "id":             row[0],
        "nombre":         row[1],
        "descripcion":    row[2],
        "criterio":       row[3],
        "hash_proyecto":  row[4],
        "color":          row[5],
        "creado_en":      row[6],
        "actualizado_en": row[7],
    }


def _row_to_constelacion_entrada(row) -> dict:
    return {
        "id":              row[0],
        "constelacion_id": row[1],
        "entrada_id":      row[2],
        "nota":            row[3],
        "orden":           row[4],
        "creado_en":       row[5],
        "slug":            row[6] if len(row) > 6 else None,
        "titulo":          row[7] if len(row) > 7 else None,
        "dominio":         row[8] if len(row) > 8 else None,
        "estado":          row[9] if len(row) > 9 else None,
    }


COLORES_CONSTELACION = {
    "indigo", "violeta", "escarlata", "dorado", "esmeralda",
    "obsidiana", "plata", "cobre", "azul", "rojo",
}


class ConstelacionRepo:
    T  = "biblioteca_constelaciones"
    TE = "biblioteca_constelacion_entradas"

    @classmethod
    def crear(cls, nombre: str, hash_proyecto: str,
              descripcion: Optional[str] = None,
              criterio: Optional[str] = None,
              color: str = "indigo") -> dict:
        if color not in COLORES_CONSTELACION:
            color = "indigo"
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            cur.execute(
                f"INSERT INTO {cls.T} "
                f"(nombre, descripcion, criterio, hash_proyecto, color, "
                f"creado_en, actualizado_en) "
                f"VALUES ({_ph(7)})",
                (nombre, descripcion, criterio, hash_proyecto, color,
                 ahora, ahora),
            )
            cid = _id_ultimo_bib(cur)
        return cls._obtener_por_id(cid)

    @classmethod
    def listar(cls, hash_proyecto: str) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT c.id, c.nombre, c.descripcion, c.criterio, "
                f"c.hash_proyecto, c.color, c.creado_en, c.actualizado_en, "
                f"COUNT(ce.id) AS total_entradas "
                f"FROM {cls.T} c "
                f"LEFT JOIN {cls.TE} ce ON ce.constelacion_id = c.id "
                f"WHERE c.hash_proyecto = {_ph(1)} "
                f"GROUP BY c.id "
                f"ORDER BY c.actualizado_en DESC",
                (hash_proyecto,),
            )
            rows = cur.fetchall()
        resultado = []
        for r in rows:
            d = _row_to_constelacion(r)
            d["total_entradas"] = r[8]
            resultado.append(d)
        return resultado

    @classmethod
    def obtener(cls, constelacion_id: int,
                hash_proyecto: str) -> Optional[dict]:
        constelacion = cls._obtener_por_id(constelacion_id)
        if not constelacion or constelacion["hash_proyecto"] != hash_proyecto:
            return None
        constelacion["entradas"] = cls.entradas_de(constelacion_id)
        return constelacion

    @classmethod
    def actualizar(cls, constelacion_id: int, hash_proyecto: str,
                   nombre: Optional[str] = None,
                   descripcion: Optional[str] = None,
                   criterio: Optional[str] = None,
                   color: Optional[str] = None) -> Optional[dict]:
        constelacion = cls._obtener_por_id(constelacion_id)
        if not constelacion or constelacion["hash_proyecto"] != hash_proyecto:
            return None

        ahora = datetime.now().isoformat()
        campos, vals = [], []
        if nombre is not None:
            campos.append(f"nombre = {_ph(1)}")
            vals.append(nombre)
        if descripcion is not None:
            campos.append(f"descripcion = {_ph(1)}")
            vals.append(descripcion)
        if criterio is not None:
            campos.append(f"criterio = {_ph(1)}")
            vals.append(criterio)
        if color is not None and color in COLORES_CONSTELACION:
            campos.append(f"color = {_ph(1)}")
            vals.append(color)
        if not campos:
            return constelacion

        campos.append(f"actualizado_en = {_ph(1)}")
        vals.append(ahora)
        vals.append(constelacion_id)

        with _conexion() as (con, cur):
            cur.execute(
                f"UPDATE {cls.T} SET {', '.join(campos)} "
                f"WHERE id = {_ph(1)}",
                vals,
            )
        return cls._obtener_por_id(constelacion_id)

    @classmethod
    def eliminar(cls, constelacion_id: int, hash_proyecto: str) -> bool:
        constelacion = cls._obtener_por_id(constelacion_id)
        if not constelacion or constelacion["hash_proyecto"] != hash_proyecto:
            return False
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM {cls.T} WHERE id = {_ph(1)}",
                (constelacion_id,),
            )
        return True

    @classmethod
    def agregar_entrada(cls, constelacion_id: int, entrada_id: int,
                        hash_proyecto: str,
                        nota: Optional[str] = None,
                        orden: int = 0) -> Optional[dict]:
        constelacion = cls._obtener_por_id(constelacion_id)
        if not constelacion or constelacion["hash_proyecto"] != hash_proyecto:
            return None
        ahora = datetime.now().isoformat()
        with _conexion() as (con, cur):
            try:
                cur.execute(
                    f"INSERT INTO {cls.TE} "
                    f"(constelacion_id, entrada_id, nota, orden, creado_en) "
                    f"VALUES ({_ph(5)})",
                    (constelacion_id, entrada_id, nota, orden, ahora),
                )
                eid = _id_ultimo_bib(cur)
            except Exception:
                # ya existe — actualiza la nota si se provee
                if nota is not None:
                    cur.execute(
                        f"UPDATE {cls.TE} SET nota = {_ph(1)} "
                        f"WHERE constelacion_id = {_ph(1)} "
                        f"AND entrada_id = {_ph(1)}",
                        (nota, constelacion_id, entrada_id),
                    )
                return cls._obtener_entrada_pivot(constelacion_id, entrada_id)
        return cls._obtener_entrada_pivot_por_id(eid)

    @classmethod
    def quitar_entrada(cls, constelacion_id: int, entrada_id: int,
                       hash_proyecto: str) -> bool:
        constelacion = cls._obtener_por_id(constelacion_id)
        if not constelacion or constelacion["hash_proyecto"] != hash_proyecto:
            return False
        with _conexion() as (con, cur):
            cur.execute(
                f"DELETE FROM {cls.TE} "
                f"WHERE constelacion_id = {_ph(1)} AND entrada_id = {_ph(1)}",
                (constelacion_id, entrada_id),
            )
        return True

    @classmethod
    def entradas_de(cls, constelacion_id: int) -> list[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT ce.id, ce.constelacion_id, ce.entrada_id, "
                f"ce.nota, ce.orden, ce.creado_en, "
                f"e.slug, e.titulo, e.dominio, e.estado "
                f"FROM {cls.TE} ce "
                f"JOIN biblioteca_entradas e ON e.id = ce.entrada_id "
                f"WHERE ce.constelacion_id = {_ph(1)} "
                f"ORDER BY ce.orden ASC, ce.creado_en ASC",
                (constelacion_id,),
            )
            return [_row_to_constelacion_entrada(r) for r in cur.fetchall()]

    # ── helpers internos ───────────────────────────────────────────────────

    @classmethod
    def _obtener_por_id(cls, constelacion_id: int) -> Optional[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT id, nombre, descripcion, criterio, hash_proyecto, "
                f"color, creado_en, actualizado_en "
                f"FROM {cls.T} WHERE id = {_ph(1)}",
                (constelacion_id,),
            )
            row = cur.fetchone()
            return _row_to_constelacion(row) if row else None

    @classmethod
    def _obtener_entrada_pivot(cls, constelacion_id: int,
                               entrada_id: int) -> Optional[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT ce.id, ce.constelacion_id, ce.entrada_id, "
                f"ce.nota, ce.orden, ce.creado_en, "
                f"e.slug, e.titulo, e.dominio, e.estado "
                f"FROM {cls.TE} ce "
                f"JOIN biblioteca_entradas e ON e.id = ce.entrada_id "
                f"WHERE ce.constelacion_id = {_ph(1)} "
                f"AND ce.entrada_id = {_ph(1)}",
                (constelacion_id, entrada_id),
            )
            row = cur.fetchone()
            return _row_to_constelacion_entrada(row) if row else None

    @classmethod
    def _obtener_entrada_pivot_por_id(cls, pivot_id: int) -> Optional[dict]:
        with _conexion() as (con, cur):
            cur.execute(
                f"SELECT ce.id, ce.constelacion_id, ce.entrada_id, "
                f"ce.nota, ce.orden, ce.creado_en, "
                f"e.slug, e.titulo, e.dominio, e.estado "
                f"FROM {cls.TE} ce "
                f"JOIN biblioteca_entradas e ON e.id = ce.entrada_id "
                f"WHERE ce.id = {_ph(1)}",
                (pivot_id,),
            )
            row = cur.fetchone()
            return _row_to_constelacion_entrada(row) if row else None
