"""Inicialización del esquema completo de la base de datos.

inicializar_db() delega en _crear_tablas() de cada módulo de dominio,
manteniendo el schema junto al código que lo usa.
"""

from base_datos._helpers import _conexion, _serial
from base_datos import legacy, proyecto, esferas, practicas
from base_datos import usuario, grimorio, altar, bosque, biblioteca


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
        biblioteca._crear_tablas(cur, pk)
