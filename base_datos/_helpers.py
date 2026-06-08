"""Helpers compartidos internos del paquete base_datos.

Importados por todos los módulos del paquete. No exponer fuera.
"""

from persistencia import ADAPTADOR, DATABASE_URL, DB_PATH

MODO_PG: bool = ADAPTADOR.es_postgres


def _conexion():
    """Context manager (con, cur): commit + close."""
    return ADAPTADOR.conexion()


def _ph(n: int = 1) -> str:
    """Placeholder según el motor: `?` SQLite / `%s` Postgres."""
    return ADAPTADOR.placeholder(n)


def _serial() -> str:
    """Tipo de columna auto-incremental según el motor."""
    return ADAPTADOR.tipo_serial()
