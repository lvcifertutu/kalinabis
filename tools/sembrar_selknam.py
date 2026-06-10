"""Siembra las entradas Selknam en la biblioteca como entradas canon."""
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
    {"titulo": "Cosmologia Selknam — Temaukel, el Hain y el Fin del Mundo del Sur", "slug": "cosmologia-selknam", "dominio": "cosmologia", "archivo": BIBLIOTECA / "cosmologia" / "COSMOLOGIA_SELKNAM.md"},
    {"titulo": "Seres Sagrados Selknam — Temaukel, Kenos y los Espiritus del Hain", "slug": "seres-sagrados-selknam", "dominio": "deidades", "archivo": BIBLIOTECA / "deidades" / "SERES_SAGRADOS_SELKNAM.md"},
    {"titulo": "Seres Magicos Selknam — Los Espiritus del Hain, el Xo'on y las Fuerzas del Territorio", "slug": "seres-magicos-selknam", "dominio": "seres_magicos", "archivo": BIBLIOTECA / "seres_magicos" / "SERES_SELKNAM.md"},
]

for e in ENTRADAS:
    contenido = e["archivo"].read_text(encoding="utf-8")
    entrada = EntradaRepo.crear_canon(titulo=e["titulo"], slug=e["slug"], dominio=e["dominio"], contenido=contenido)
    if entrada:
        print(f"ok  {e['slug']} - estado: {entrada.get('estado')} | {len(contenido)} chars")
    else:
        print(f"ERR {e['slug']} - no se pudo crear")
