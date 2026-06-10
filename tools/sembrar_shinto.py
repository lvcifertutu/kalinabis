"""Siembra las entradas del Shinto en la biblioteca como entradas canon."""
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
    {"titulo": "Cosmologia Shinto — Los Kami, el Kojiki y la Creacion de Japon", "slug": "cosmologia-shinto", "dominio": "cosmologia", "archivo": BIBLIOTECA / "cosmologia" / "COSMOLOGIA_SHINTO.md"},
    {"titulo": "Kami Shinto — Amaterasu, Susanoo y el Panteon de los Ocho Millones", "slug": "kami-shinto", "dominio": "deidades", "archivo": BIBLIOTECA / "deidades" / "KAMI_SHINTO.md"},
    {"titulo": "Seres Magicos Shinto — Kitsune, Oni, Tengu y los Seres del Folklor Japones", "slug": "seres-shinto", "dominio": "seres_magicos", "archivo": BIBLIOTECA / "seres_magicos" / "SERES_SHINTO.md"},
]

for e in ENTRADAS:
    contenido = e["archivo"].read_text(encoding="utf-8")
    entrada = EntradaRepo.crear_canon(titulo=e["titulo"], slug=e["slug"], dominio=e["dominio"], contenido=contenido)
    if entrada:
        print(f"ok  {e['slug']} - estado: {entrada.get('estado')} | {len(contenido)} chars")
    else:
        print(f"ERR {e['slug']} - no se pudo crear")
