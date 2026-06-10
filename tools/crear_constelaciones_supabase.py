"""Crea las tablas de constelaciones en Supabase.

Ejecutar una sola vez: python tools/crear_constelaciones_supabase.py
Idempotente — usa CREATE TABLE IF NOT EXISTS.
"""
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

env_path = Path(__file__).parent.parent / ".env.local"
for line in env_path.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

from base_datos._helpers import _conexion_bib as _conexion

SQL = """
CREATE TABLE IF NOT EXISTS biblioteca_constelaciones (
    id             SERIAL PRIMARY KEY,
    nombre         TEXT NOT NULL,
    descripcion    TEXT,
    criterio       TEXT,
    hash_proyecto  TEXT NOT NULL,
    color          TEXT NOT NULL DEFAULT 'indigo',
    creado_en      TEXT NOT NULL,
    actualizado_en TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS biblioteca_constelacion_entradas (
    id               SERIAL PRIMARY KEY,
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
);

CREATE INDEX IF NOT EXISTS idx_bib_constel_proyecto
    ON biblioteca_constelaciones (hash_proyecto);

CREATE INDEX IF NOT EXISTS idx_bib_constel_entradas_constel
    ON biblioteca_constelacion_entradas (constelacion_id);
"""

with _conexion() as (con, cur):
    for stmt in SQL.strip().split(";"):
        stmt = stmt.strip()
        if stmt:
            cur.execute(stmt)

print("ok — tablas de constelaciones creadas en Supabase")
