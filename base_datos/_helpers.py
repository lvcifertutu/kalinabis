"""Helpers compartidos internos del paquete base_datos.

Importados por todos los módulos del paquete. No exponer fuera.

Dos contextos de conexión:
  - _conexion / _ph / _serial       → altar personal (SQLite o PG local)
  - _conexion_bib / _ph_bib / etc.  → biblioteca colectiva (Supabase)
"""

from persistencia import ADAPTADOR, ADAPTADOR_BIBLIOTECA, DATABASE_URL, DB_PATH

MODO_PG: bool = ADAPTADOR.es_postgres


# ── Altar personal ────────────────────────────────────────────────────────

def _conexion():
    """Context manager (con, cur): commit + close."""
    return ADAPTADOR.conexion()


def _ph(n: int = 1) -> str:
    """Placeholder según el motor: `?` SQLite / `%s` Postgres."""
    return ADAPTADOR.placeholder(n)


def _serial() -> str:
    """Tipo de columna auto-incremental según el motor."""
    return ADAPTADOR.tipo_serial()


# ── Biblioteca colectiva (Supabase) ───────────────────────────────────────

def _conexion_bib():
    """Context manager (con, cur) para la biblioteca colectiva."""
    return ADAPTADOR_BIBLIOTECA.conexion()


def _ph_bib(n: int = 1) -> str:
    """Placeholder para queries de biblioteca."""
    return ADAPTADOR_BIBLIOTECA.placeholder(n)


def _serial_bib() -> str:
    """Tipo serial para DDL de biblioteca."""
    return ADAPTADOR_BIBLIOTECA.tipo_serial()


def _id_ultimo_bib(cur) -> int:
    """Id de la última fila insertada en una conexión de biblioteca."""
    return ADAPTADOR_BIBLIOTECA.id_ultimo_insertado(cur)
