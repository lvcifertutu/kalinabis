"""Siembra las entradas aztecas/mexicas en la biblioteca como entradas canon."""
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
    {"titulo": "Cosmologia Azteca - Los Cinco Soles y el Tiempo como Deuda de Sangre", "slug": "cosmologia-azteca", "dominio": "cosmologia", "archivo": BIBLIOTECA / "cosmologia" / "COSMOLOGIA_AZTECA.md"},
    {"titulo": "Dioses Aztecas - Quetzalcoatl Tezcatlipoca y el Panteon Mexica", "slug": "dioses-aztecas", "dominio": "deidades", "archivo": BIBLIOTECA / "deidades" / "DIOSES_AZTECAS.md"},
    {"titulo": "Seres del Mundo Azteca - Tzitzimitl Nahualli y los Seres del Quinto Sol", "slug": "seres-aztecas", "dominio": "seres_magicos", "archivo": BIBLIOTECA / "seres_magicos" / "SERES_AZTECAS.md"},
]
for e in ENTRADAS:
    contenido = e["archivo"].read_text(encoding="utf-8")
    entrada = EntradaRepo.crear_canon(titulo=e["titulo"], slug=e["slug"], dominio=e["dominio"], contenido=contenido)
    if entrada:
        print(f"ok  {e['slug']} - estado: {entrada.get('estado')} | {len(contenido)} chars")
    else:
        print(f"ERR {e['slug']} - no se pudo crear")
