"""Inicialización del esquema completo de la base de datos.

inicializar_db() delega en _crear_tablas() de cada módulo de dominio,
manteniendo el schema junto al código que lo usa.

La biblioteca colectiva vive en Supabase (SUPABASE_DB_URL).
Si no hay SUPABASE_DB_URL, se inicializa localmente para desarrollo.
En producción, usar migrations/biblioteca_supabase.sql.
"""

from base_datos._helpers import _conexion, _serial
from base_datos import legacy, proyecto, esferas, practicas
from base_datos import usuario, grimorio, altar, bosque, biblioteca
from base_datos import manifestacion
from base_datos import sigilo_proyecto
from base_datos import limpia
from base_datos import ayni
from persistencia import SUPABASE_DB_URL


def inicializar_db():
    """Crea todas las tablas si no existen. Idempotente."""
    pk = f"{_serial()} PRIMARY KEY"

    with _conexion() as (con, cur):
        legacy._crear_tablas(cur, pk)
        proyecto._crear_tablas(cur, pk)
        esferas._crear_tablas(cur, pk)
        practicas._crear_tablas(cur, pk)
        usuario._crear_tablas(cur, pk)
        grimorio._crear_tablas(cur, pk)
        altar._crear_tablas(cur, pk)
        bosque._crear_tablas(cur, pk)
        manifestacion._crear_tablas(cur, pk)
        sigilo_proyecto._crear_tablas(cur, pk)
        limpia._crear_tablas(cur, pk)
        ayni._crear_tablas(cur, pk)

    if not SUPABASE_DB_URL:
        biblioteca._inicializar_local()
