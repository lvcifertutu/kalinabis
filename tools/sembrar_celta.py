"""Siembra las entradas de la tradicion celta en la biblioteca como entradas canon."""
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
    {
        "titulo": "Cosmologia Celta - Tir na Nog los Tres Mundos y el Ciclo Eterno",
        "slug": "cosmologia-celta",
        "dominio": "cosmologia",
        "archivo": BIBLIOTECA / "cosmologia" / "COSMOLOGIA_CELTA.md",
    },
    {
        "titulo": "Tuatha De Danann - Las Deidades Celtas de Irlanda",
        "slug": "tuatha-de-danann",
        "dominio": "deidades",
        "archivo": BIBLIOTECA / "deidades" / "TUATHA_DE_DANANN.md",
    },
    {
        "titulo": "Seres del Mundo Celta - los Sidhe las Hadas y los Habitantes del Otro Mundo",
        "slug": "seres-celtas",
        "dominio": "seres_magicos",
        "archivo": BIBLIOTECA / "seres_magicos" / "SERES_CELTAS.md",
    },
]

for e in ENTRADAS:
    contenido = e["archivo"].read_text(encoding="utf-8")
    entrada = EntradaRepo.crear_canon(
        titulo=e["titulo"],
        slug=e["slug"],
        dominio=e["dominio"],
        contenido=contenido,
    )
    if entrada:
        print(f"ok  {e['slug']} - estado: {entrada.get('estado')} | {len(contenido)} chars")
    else:
        print(f"ERR {e['slug']} - no se pudo crear")
