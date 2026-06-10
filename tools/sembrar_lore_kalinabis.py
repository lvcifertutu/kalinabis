"""Siembra el lore canon de Kalinabis en la biblioteca de Supabase.

Ejecutar: python tools/sembrar_lore_kalinabis.py
Idempotente — salta entradas cuyo slug ya existe.
"""
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

env_path = Path(__file__).parent.parent / ".env.local"
for line in env_path.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

from base_datos.biblioteca import EntradaRepo

BIBLIOTECA = Path(__file__).parent.parent / "biblioteca" / "lore_kalinabis"

ENTRADAS = [
    {
        "titulo": "Kali — La Matriz Primordial en Kalinabis",
        "slug": "kalinabis-kali",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_KALI.md",
    },
    {
        "titulo": "Tutu — El Hijo del Humo, Orquestador del Sistema",
        "slug": "kalinabis-tutu",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_TUTU.md",
    },
    {
        "titulo": "Isis — Guardiana del Norte en Kalinabis",
        "slug": "kalinabis-isis",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_ISIS.md",
    },
    {
        "titulo": "Afrodita — Guardiana del Este en Kalinabis",
        "slug": "kalinabis-afrodita",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_AFRODITA.md",
    },
    {
        "titulo": "Lilith — Guardiana del Sur en Kalinabis",
        "slug": "kalinabis-lilith",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_LILITH.md",
    },
    {
        "titulo": "Artemisa — Guardiana del Oeste en Kalinabis",
        "slug": "kalinabis-artemisa",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_ARTEMISA.md",
    },
    {
        "titulo": "La Rueda de los Ocho Colores — Magia del Caos en Kalinabis",
        "slug": "kalinabis-rueda-colores",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_RUEDA_COLORES.md",
    },
    {
        "titulo": "La Estructura del Sistema Kalinabis",
        "slug": "kalinabis-estructura",
        "dominio": "lore_kalinabis",
        "archivo": BIBLIOTECA / "KALINABIS_ESTRUCTURA.md",
    },
]

ok = 0
skip = 0
for e in ENTRADAS:
    if not e["archivo"].exists():
        print(f"  err archivo no encontrado: {e['archivo']}")
        continue
    contenido = e["archivo"].read_text(encoding="utf-8")
    try:
        entrada = EntradaRepo.crear_canon(
            titulo=e["titulo"],
            slug=e["slug"],
            dominio=e["dominio"],
            contenido=contenido,
        )
        print(f"  ok  {e['slug']} (id={entrada['id']})")
        ok += 1
    except Exception as exc:
        if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
            print(f"  --  {e['slug']} (ya existe)")
            skip += 1
        else:
            print(f"  err {e['slug']}: {exc}")

print(f"\n{ok} sembradas · {skip} ya existían · lore_kalinabis completo")
