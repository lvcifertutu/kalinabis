#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genera sprites pixel art locales (offline, sin HF)."""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).parent.parent / "public" / "sprites"

DIOSAS = {
    "lilith": {"color": (50, 0, 80), "name": "Lilith"},
    "isis": {"color": (200, 140, 0), "name": "Isis"},
    "afrodita": {"color": (255, 100, 150), "name": "Aphrodite"},
    "artemisa": {"color": (100, 150, 50), "name": "Artemis"},
    "tutu": {"color": (200, 100, 50), "name": "Tutu"},
}

def gen_sprite(diosa: str, frame: str) -> None:
    """Genera sprites pixel art mejorados con más detalle."""
    info = DIOSAS[diosa]
    color = info["color"]
    name = info["name"]

    # Canvas 96x96 (mismo que HF)
    img = Image.new("RGBA", (96, 96), (220, 220, 220, 255))
    draw = ImageDraw.Draw(img)

    # Colores derivados del color base
    color_light = tuple(min(c + 60, 255) for c in color)
    color_dark = tuple(max(c - 40, 0) for c in color)

    # CABEZA
    draw.ellipse([34, 6, 62, 28], fill=color, outline=(0, 0, 0), width=1)

    # CABELLO (según diosa)
    if name == "Lilith":
        # Pelo largo y ondulado
        draw.rectangle([32, 10, 36, 26], fill=color_dark)
        draw.rectangle([60, 10, 64, 26], fill=color_dark)
        draw.ellipse([30, 8, 66, 18], fill=color_dark, outline=(0, 0, 0), width=1)

    # OJOS (según frame)
    if frame == "idle":
        draw.ellipse([40, 14, 44, 18], fill=(255, 255, 255), outline=(0, 0, 0))
        draw.ellipse([52, 14, 56, 18], fill=(255, 255, 255), outline=(0, 0, 0))
        draw.ellipse([41, 15, 43, 17], fill=(0, 0, 0))
        draw.ellipse([53, 15, 55, 17], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(40, 16), (44, 16)], fill=(0, 0, 0), width=2)
        draw.line([(52, 16), (56, 16)], fill=(0, 0, 0), width=2)

    # BOCA (según frame)
    if frame == "idle":
        draw.line([(45, 22), (51, 22)], fill=(0, 0, 0), width=1)
    elif frame == "speak":
        draw.ellipse([46, 21, 50, 24], fill=(100, 0, 0))

    # CUERPO (torso mejorado)
    draw.rectangle([30, 28, 66, 65], fill=color, outline=(0, 0, 0), width=2)
    # Detalle de ropa
    draw.rectangle([32, 30, 64, 35], fill=color_light, outline=(0, 0, 0), width=1)

    # BRAZOS mejorados
    draw.rectangle([24, 32, 30, 58], fill=color, outline=(0, 0, 0), width=1)
    draw.rectangle([66, 32, 72, 58], fill=color, outline=(0, 0, 0), width=1)
    # Manos
    draw.rectangle([24, 58, 30, 62], fill=color_light, outline=(0, 0, 0), width=1)
    draw.rectangle([66, 58, 72, 62], fill=color_light, outline=(0, 0, 0), width=1)

    # PIERNAS
    draw.rectangle([36, 65, 43, 90], fill=color_dark, outline=(0, 0, 0), width=1)
    draw.rectangle([53, 65, 60, 90], fill=color_dark, outline=(0, 0, 0), width=1)
    # Zapatos
    draw.rectangle([35, 88, 44, 92], fill=(50, 50, 50), outline=(0, 0, 0), width=1)
    draw.rectangle([52, 88, 61, 92], fill=(50, 50, 50), outline=(0, 0, 0), width=1)

    # ACCESORIOS (según diosa)
    if name == "Lilith":
        # Collar/símbolo
        draw.ellipse([46, 25, 50, 29], fill=(100, 200, 255), outline=(0, 0, 0))

    OUT.mkdir(parents=True, exist_ok=True)
    destino = OUT / f"{diosa}-{frame}.png"
    img.save(destino)
    print(f"[OK] {destino}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diosa", required=True, help="lilith | isis | afrodita | artemisa | tutu | todas")
    ap.add_argument("--frame", default="idle", help="idle | blink | speak")
    args = ap.parse_args()

    objetivos = list(DIOSAS) if args.diosa == "todas" else [args.diosa]

    for diosa in objetivos:
        if diosa not in DIOSAS:
            print(f"[!] Diosa desconocida: {diosa}")
            continue

        # Si es "todas", genera los 3 frames
        frames = ["idle", "blink", "speak"] if args.diosa == "todas" else [args.frame]
        for frame in frames:
            gen_sprite(diosa, frame)

if __name__ == "__main__":
    main()
