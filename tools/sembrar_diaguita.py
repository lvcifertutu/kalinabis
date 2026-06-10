"""Siembra las entradas Diaguita en la biblioteca como entradas canon."""
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

env_path = Path(__file__).parent.parent / ".env.local"
for line in env_path.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

from base_datos.biblioteca import EntradaRepo

BIBLIOTECA = Path(__file__).parent.parent / "biblioteca"

ENTRADAS = [
    {"titulo": "Cosmologia Diaguita — Pachamama, los Cerros y el Cosmos Calchaqui", "slug": "cosmologia-diaguita", "dominio": "cosmologia", "archivo": BIBLIOTECA / "cosmologia" / "COSMOLOGIA_DIAGUITA.md"},
    {"titulo": "Seres Sagrados Diaguita — Pachamama, los Apus y el Panteon del NOA", "slug": "seres-sagrados-diaguita", "dominio": "deidades", "archivo": BIBLIOTECA / "deidades" / "SERES_SAGRADOS_DIAGUITA.md"},
    {"titulo": "Seres Magicos Diaguita — El Coquena, la Salamanca y los Seres del NOA", "slug": "seres-magicos-diaguita", "dominio": "seres_magicos", "archivo": BIBLIOTECA / "seres_magicos" / "SERES_DIAGUITA.md"},
]

for e in ENTRADAS:
    contenido = e["archivo"].read_text(encoding="utf-8")
    entrada = EntradaRepo.crear_canon(titulo=e["titulo"], slug=e["slug"], dominio=e["dominio"], contenido=contenido)
    if entrada:
        print(f"ok  {e['slug']} - estado: {entrada.get('estado')} | {len(contenido)} chars")
    else:
        print(f"ERR {e['slug']} - no se pudo crear")
