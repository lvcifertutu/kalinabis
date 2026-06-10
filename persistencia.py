"""Adapters de persistencia: ocultan el dialecto del motor concreto.

El resto del sistema (base_datos.py y sus repos) habla con un `AdaptadorBD`
uniforme y no sabe si detrás hay SQLite o PostgreSQL. Las diferencias de
dialecto —placeholder de parámetros, tipo auto-incremental, conexión y cómo
se obtiene el último id insertado— viven aquí, detrás de la interface.

No cambia el schema: solo concentra el seam que antes se filtraba como
`if MODO_PG` por todo base_datos.py.
"""

import os
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path

DATABASE_URL = os.environ.get("DATABASE_URL", "")
SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL", "")
DB_PATH = Path(__file__).parent / "grimorio.db"


class AdaptadorBD(ABC):
    """Interface de persistencia común a todos los motores."""

    es_postgres: bool = False

    @abstractmethod
    def _conectar(self):
        """Abre y devuelve una conexión cruda del driver."""
        ...

    @contextmanager
    def conexion(self):
        """Context manager que entrega (con, cur), hace commit y cierra."""
        con = self._conectar()
        cur = con.cursor()
        try:
            yield con, cur
            con.commit()
        finally:
            cur.close()
            con.close()

    @abstractmethod
    def placeholder(self, n: int = 1) -> str:
        """Placeholders de parámetros separados por coma (`?` o `%s`)."""
        ...

    @abstractmethod
    def tipo_serial(self) -> str:
        """Tipo de columna auto-incremental del motor."""
        ...

    @abstractmethod
    def id_ultimo_insertado(self, cur) -> int:
        """Id de la última fila insertada en esta conexión."""
        ...


class AdaptadorSQLite(AdaptadorBD):
    es_postgres = False

    def __init__(self, ruta=DB_PATH):
        import sqlite3
        self._sqlite3 = sqlite3
        self._ruta = str(ruta)

    def _conectar(self):
        return self._sqlite3.connect(self._ruta)

    def placeholder(self, n: int = 1) -> str:
        return ", ".join(["?"] * n)

    def tipo_serial(self) -> str:
        return "INTEGER"

    def id_ultimo_insertado(self, cur) -> int:
        cur.execute("SELECT last_insert_rowid()")
        return cur.fetchone()[0]


class AdaptadorPostgres(AdaptadorBD):
    es_postgres = True

    def __init__(self, url: str):
        import psycopg2
        import psycopg2.extras  # noqa: F401  (paridad con el import original)
        self._psycopg2 = psycopg2
        # Render entrega postgres:// pero psycopg2 necesita postgresql://
        self._url = url.replace("postgres://", "postgresql://", 1)

    def _conectar(self):
        return self._psycopg2.connect(self._url)

    def placeholder(self, n: int = 1) -> str:
        return ", ".join(["%s"] * n)

    def tipo_serial(self) -> str:
        return "SERIAL"

    def id_ultimo_insertado(self, cur) -> int:
        cur.execute("SELECT lastval()")
        return cur.fetchone()[0]


def crear_adaptador() -> AdaptadorBD:
    """Selecciona el adapter según el entorno: Postgres si hay DATABASE_URL."""
    if DATABASE_URL:
        return AdaptadorPostgres(DATABASE_URL)
    return AdaptadorSQLite()


def crear_adaptador_biblioteca() -> AdaptadorBD:
    """Adapter para la biblioteca colectiva: Supabase si hay SUPABASE_DB_URL,
    si no cae al adaptador local (útil en desarrollo sin Supabase)."""
    if SUPABASE_DB_URL:
        return AdaptadorPostgres(SUPABASE_DB_URL)
    return crear_adaptador()


# Adapters activos del proceso (seleccionados una vez al importar).
ADAPTADOR: AdaptadorBD = crear_adaptador()
ADAPTADOR_BIBLIOTECA: AdaptadorBD = crear_adaptador_biblioteca()
