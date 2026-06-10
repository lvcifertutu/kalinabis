"""Siembra las entradas de la tradicion hindu en la biblioteca como entradas canon."""
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
    {"titulo": "Cosmologia Hindu — El Brahman, los Yugas y el Eterno Retorno", "slug": "cosmologia-hindu", "dominio": "cosmologia", "archivo": BIBLIOTECA / "cosmologia" / "COSMOLOGIA_HINDU.md"},
    {"titulo": "Deidades Hindues — La Trimurti, los Deva y el Panteon Infinito", "slug": "deidades-hindues", "dominio": "deidades", "archivo": BIBLIOTECA / "deidades" / "DEIDADES_HINDUES.md"},
    {"titulo": "Seres Magicos Hindues — Nagas, Devas, Asuras y el Bestiario Sagrado", "slug": "seres-hindues", "dominio": "seres_magicos", "archivo": BIBLIOTECA / "seres_magicos" / "SERES_HINDUES.md"},
]

for e in ENTRADAS:
    contenido = e["archivo"].read_text(encoding="utf-8")
    entrada = EntradaRepo.crear_canon(titulo=e["titulo"], slug=e["slug"], dominio=e["dominio"], contenido=contenido)
    if entrada:
        print(f"ok  {e['slug']} - estado: {entrada.get('estado')} | {len(contenido)} chars")
    else:
        print(f"ERR {e['slug']} - no se pudo crear")
