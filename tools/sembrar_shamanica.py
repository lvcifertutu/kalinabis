"""Siembra las entradas del chamanismo siberiano en la biblioteca como entradas canon."""
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
    {"titulo": "Cosmologia Chamanica Siberiana — El Arbol del Mundo, los Tres Planos y el Vuelo del Alma", "slug": "cosmologia-shamanica-siberiana", "dominio": "cosmologia", "archivo": BIBLIOTECA / "cosmologia" / "COSMOLOGIA_SHAMANICA.md"},
    {"titulo": "Espiritus Chamanicos Siberianos — Tengri, los Maestros y los Auxiliares", "slug": "espiritus-shamanicos-siberianos", "dominio": "deidades", "archivo": BIBLIOTECA / "deidades" / "ESPIRITUS_SHAMANICOS.md"},
    {"titulo": "Seres Magicos Chamanicos Siberianos — Duenos de Animales, Maestros del Lugar y Entidades del Viaje", "slug": "seres-chamanicos-siberianos", "dominio": "seres_magicos", "archivo": BIBLIOTECA / "seres_magicos" / "SERES_CHAMANICOS.md"},
]

for e in ENTRADAS:
    contenido = e["archivo"].read_text(encoding="utf-8")
    entrada = EntradaRepo.crear_canon(titulo=e["titulo"], slug=e["slug"], dominio=e["dominio"], contenido=contenido)
    if entrada:
        print(f"ok  {e['slug']} - estado: {entrada.get('estado')} | {len(contenido)} chars")
    else:
        print(f"ERR {e['slug']} - no se pudo crear")
