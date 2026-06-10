#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera sprites pixel art detallados con características específicas por diosa."""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).parent.parent / "public" / "sprites"

# Definiciones de diosas con colores y características
DIOSAS = {
    "lilith": {
        "name": "Lilith",
        "primary": (80, 20, 120),      # Púrpura oscuro
        "secondary": (150, 50, 200),   # Púrpura claro
        "accent": (0, 200, 255),       # Teal
        "skin": (200, 150, 180),
    },
    "isis": {
        "name": "Isis",
        "primary": (200, 150, 0),      # Oro
        "secondary": (255, 200, 100),  # Oro claro
        "accent": (255, 255, 255),     # Blanco
        "skin": (210, 160, 120),
    },
    "afrodita": {
        "name": "Aphrodite",
        "primary": (255, 100, 150),    # Rosa coral
        "secondary": (255, 150, 180),  # Rosa claro
        "accent": (255, 200, 100),     # Dorado
        "skin": (240, 180, 160),
    },
    "artemisa": {
        "name": "Artemis",
        "primary": (80, 140, 60),      # Verde oscuro
        "secondary": (120, 180, 80),   # Verde claro
        "accent": (200, 140, 0),       # Bronceado
        "skin": (200, 160, 120),
    },
    "tutu": {
        "name": "Tutu",
        "primary": (200, 80, 20),      # Rojo naranja
        "secondary": (240, 120, 60),   # Naranja
        "accent": (100, 180, 60),      # Verde hoja
        "skin": (220, 160, 140),
    },
}

def draw_lilith(draw, w, h, colors, frame):
    """Dibuja sprite de Lilith: diosa de tormenta, gótica."""
    # Cabeza
    head_y, head_h = 6, 20
    draw.ellipse([32, head_y, 64, head_y + head_h], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # Cabello largo y ondulado (teal/púrpura)
    draw.rectangle([28, head_y + 2, 32, head_y + 18], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.rectangle([64, head_y + 2, 68, head_y + 18], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.polygon([(30, head_y - 2), (34, head_y - 4), (40, head_y - 2), (44, head_y + 2)],
                 fill=colors["primary"], outline=(0, 0, 0))
    draw.polygon([(52, head_y - 2), (56, head_y - 4), (62, head_y - 2), (66, head_y + 2)],
                 fill=colors["primary"], outline=(0, 0, 0))

    # Ojos (según frame)
    if frame in ("idle", "speak"):
        # Ojos grandes y intensos
        draw.ellipse([38, head_y + 6, 44, head_y + 12], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([52, head_y + 6, 58, head_y + 12], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([39, head_y + 7, 43, head_y + 11], fill=colors["accent"])  # Iris teal
        draw.ellipse([53, head_y + 7, 57, head_y + 11], fill=colors["accent"])
        draw.ellipse([40, head_y + 8, 42, head_y + 10], fill=(0, 0, 0))  # Pupila
        draw.ellipse([54, head_y + 8, 56, head_y + 10], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(38, head_y + 9), (44, head_y + 9)], fill=(0, 0, 0), width=2)
        draw.line([(52, head_y + 9), (58, head_y + 9)], fill=(0, 0, 0), width=2)

    # Boca
    if frame == "idle":
        draw.line([(44, head_y + 16), (52, head_y + 16)], fill=(100, 0, 0), width=2)
    elif frame == "speak":
        draw.ellipse([46, head_y + 15, 50, head_y + 19], fill=(100, 0, 0))

    # Torso (ropa púrpura con detalles)
    draw.rectangle([26, 28, 70, 68], fill=colors["primary"], outline=(0, 0, 0), width=2)
    # Detalles de ropa (tiras/ornamentos)
    draw.rectangle([28, 30, 68, 34], fill=colors["secondary"], outline=(0, 0, 0), width=1)
    draw.line([(48, 30), (48, 68)], fill=colors["accent"], width=1)  # Línea central teal

    # Brazos
    draw.rectangle([18, 32, 26, 60], fill=colors["primary"], outline=(0, 0, 0), width=2)
    draw.rectangle([70, 32, 78, 60], fill=colors["primary"], outline=(0, 0, 0), width=2)
    # Manos
    draw.rectangle([18, 60, 26, 66], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([70, 60, 78, 66], fill=colors["skin"], outline=(0, 0, 0), width=1)
    # Collar/símbolo
    draw.ellipse([44, 26, 52, 32], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.line([(48, 27), (48, 31)], fill=(0, 0, 0), width=1)

    # Piernas (púrpura oscuro)
    draw.rectangle([34, 68, 42, 90], fill=colors["primary"], outline=(0, 0, 0), width=1)
    draw.rectangle([54, 68, 62, 90], fill=colors["primary"], outline=(0, 0, 0), width=1)
    # Botas
    draw.rectangle([32, 88, 44, 94], fill=(30, 30, 30), outline=(0, 0, 0), width=1)
    draw.rectangle([52, 88, 64, 94], fill=(30, 30, 30), outline=(0, 0, 0), width=1)

def draw_isis(draw, w, h, colors, frame):
    """Dibuja sprite de Isis: diosa madre egipcia, dorada."""
    # Corona dorada con sol
    draw.polygon([(32, 2), (40, 0), (48, 2), (56, 0), (64, 2), (62, 8), (56, 6), (48, 8), (40, 6), (34, 8)],
                 fill=colors["primary"], outline=(0, 0, 0), width=1)

    # Cabeza
    draw.ellipse([32, 10, 64, 30], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # Cabello largo
    draw.rectangle([28, 14, 32, 28], fill=colors["primary"])
    draw.rectangle([64, 14, 68, 28], fill=colors["primary"])

    # Ojos (dulces, amables)
    if frame in ("idle", "speak"):
        draw.ellipse([38, 16, 44, 22], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([52, 16, 58, 22], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([39, 18, 43, 21], fill=(200, 100, 0))
        draw.ellipse([53, 18, 57, 21], fill=(200, 100, 0))
        draw.ellipse([40, 19, 42, 20], fill=(0, 0, 0))
        draw.ellipse([54, 19, 56, 20], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(38, 19), (44, 19)], fill=(0, 0, 0), width=2)
        draw.line([(52, 19), (58, 19)], fill=(0, 0, 0), width=2)

    # Boca (sonrisa)
    if frame == "idle":
        draw.arc([(44, 24), (52, 28)], 0, 180, fill=(150, 50, 0), width=1)
    elif frame == "speak":
        draw.ellipse([46, 24, 50, 28], fill=(150, 50, 0))

    # Torso (vestido blanco y oro)
    draw.rectangle([26, 30, 70, 70], fill=colors["accent"], outline=(0, 0, 0), width=2)
    # Detalles dorados
    draw.rectangle([28, 32, 68, 36], fill=colors["primary"], outline=(0, 0, 0), width=1)
    draw.rectangle([28, 50, 68, 54], fill=colors["primary"], outline=(0, 0, 0), width=1)

    # Brazos
    draw.rectangle([18, 35, 26, 62], fill=colors["accent"], outline=(0, 0, 0), width=2)
    draw.rectangle([70, 35, 78, 62], fill=colors["accent"], outline=(0, 0, 0), width=2)

    # Manos
    draw.rectangle([18, 62, 26, 68], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([70, 62, 78, 68], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # Ankh (en mano derecha)
    draw.ellipse([72, 58, 76, 62], fill=colors["primary"], outline=(0, 0, 0), width=1)
    draw.rectangle([74, 62, 76, 70], fill=colors["primary"], outline=(0, 0, 0), width=1)

    # Piernas
    draw.rectangle([34, 70, 42, 90], fill=colors["primary"], outline=(0, 0, 0), width=1)
    draw.rectangle([54, 70, 62, 90], fill=colors["primary"], outline=(0, 0, 0), width=1)
    # Sandalias
    draw.rectangle([32, 88, 44, 92], fill=colors["primary"], outline=(0, 0, 0), width=1)
    draw.rectangle([52, 88, 64, 92], fill=colors["primary"], outline=(0, 0, 0), width=1)

def draw_afrodita(draw, w, h, colors, frame):
    """Dibuja sprite de Afrodita: diosa del amor, con alas."""
    # Cabello ondulado
    draw.polygon([(32, 6), (36, 2), (40, 4), (44, 2), (48, 4), (52, 2), (56, 4), (60, 2), (64, 6), (62, 12), (50, 10), (48, 12), (46, 10)],
                 fill=colors["secondary"], outline=(0, 0, 0), width=1)

    # Cabeza
    draw.ellipse([32, 10, 64, 30], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # Corona de flores
    draw.ellipse([34, 8, 62, 14], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.ellipse([37, 6, 40, 9], fill=(255, 100, 150), outline=(0, 0, 0), width=1)
    draw.ellipse([56, 6, 59, 9], fill=(255, 100, 150), outline=(0, 0, 0), width=1)

    # Ojos (dulces y luminosos)
    if frame in ("idle", "speak"):
        draw.ellipse([38, 16, 44, 22], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([52, 16, 58, 22], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([39, 17, 43, 21], fill=(100, 200, 255))
        draw.ellipse([53, 17, 57, 21], fill=(100, 200, 255))
    elif frame == "blink":
        draw.line([(38, 19), (44, 19)], fill=(0, 0, 0), width=2)
        draw.line([(52, 19), (58, 19)], fill=(0, 0, 0), width=2)

    # Boca (sonrisa)
    if frame == "idle":
        draw.arc([(44, 24), (52, 28)], 0, 180, fill=(200, 80, 120), width=1)
    elif frame == "speak":
        draw.ellipse([46, 24, 50, 28], fill=(200, 80, 120))

    # Torso (vestido rosa)
    draw.rectangle([28, 30, 68, 68], fill=colors["primary"], outline=(0, 0, 0), width=2)
    # Detalles
    draw.polygon([(48, 32), (52, 30), (56, 32), (52, 34)], fill=colors["accent"])
    draw.polygon([(40, 32), (44, 30), (48, 32), (44, 34)], fill=colors["accent"])

    # Alas (pequeñas e iridiscentes)
    draw.polygon([(16, 40), (24, 36), (26, 44)], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.polygon([(80, 40), (72, 36), (70, 44)], fill=colors["accent"], outline=(0, 0, 0), width=1)

    # Brazos
    draw.rectangle([20, 35, 28, 58], fill=colors["primary"], outline=(0, 0, 0), width=2)
    draw.rectangle([68, 35, 76, 58], fill=colors["primary"], outline=(0, 0, 0), width=2)

    # Manos
    draw.rectangle([20, 58, 28, 64], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([68, 58, 76, 64], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # Piernas
    draw.rectangle([36, 68, 44, 88], fill=colors["secondary"], outline=(0, 0, 0), width=1)
    draw.rectangle([52, 68, 60, 88], fill=colors["secondary"], outline=(0, 0, 0), width=1)
    # Sandalias flores
    draw.rectangle([34, 86, 46, 92], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.rectangle([50, 86, 62, 92], fill=colors["accent"], outline=(0, 0, 0), width=1)

def draw_artemisa(draw, w, h, colors, frame):
    """Dibuja sprite de Artemisa: cazadora, con verde y marrón."""
    # Cabello (castaño con hojas)
    draw.ellipse([(32, 6), (64, 28)], fill=colors["primary"], outline=(0, 0, 0), width=2)
    draw.polygon([(36, 4), (40, 2), (44, 4)], fill=colors["accent"])
    draw.polygon([(52, 4), (56, 2), (60, 4)], fill=colors["accent"])

    # Corona de hojas
    draw.polygon([(30, 8), (34, 6), (38, 8), (42, 6), (46, 8), (50, 6), (54, 8), (58, 6), (62, 8)],
                 fill=colors["accent"], outline=(0, 0, 0), width=1)

    # Cabeza
    draw.ellipse([34, 12, 62, 28], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # Ojos (alerta, fuertes)
    if frame in ("idle", "speak"):
        draw.ellipse([40, 17, 46, 23], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([50, 17, 56, 23], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([41, 18, 45, 22], fill=colors["primary"])
        draw.ellipse([51, 18, 55, 22], fill=colors["primary"])
        draw.ellipse([42, 19, 44, 21], fill=(0, 0, 0))
        draw.ellipse([52, 19, 54, 21], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(40, 20), (46, 20)], fill=(0, 0, 0), width=2)
        draw.line([(50, 20), (56, 20)], fill=(0, 0, 0), width=2)

    # Boca (serena)
    if frame == "idle":
        draw.line([(45, 25), (51, 25)], fill=(100, 50, 0), width=1)
    elif frame == "speak":
        draw.ellipse([46, 24, 50, 28], fill=(100, 50, 0))

    # Torso (vestido verde)
    draw.rectangle([28, 30, 68, 68], fill=colors["primary"], outline=(0, 0, 0), width=2)
    # Cinturón marrón
    draw.rectangle([26, 50, 70, 54], fill=colors["accent"], outline=(0, 0, 0), width=2)

    # Brazos
    draw.rectangle([20, 35, 28, 60], fill=colors["secondary"], outline=(0, 0, 0), width=2)
    draw.rectangle([68, 35, 76, 60], fill=colors["secondary"], outline=(0, 0, 0), width=2)

    # Manos
    draw.rectangle([20, 60, 28, 66], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([68, 60, 76, 66], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # Canasta de manzanas (en mano izquierda)
    draw.rectangle([14, 58, 20, 68], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.ellipse([12, 56, 16, 60], fill=(200, 50, 50), outline=(0, 0, 0), width=1)
    draw.ellipse([14, 54, 18, 58], fill=(200, 50, 50), outline=(0, 0, 0), width=1)

    # Piernas
    draw.rectangle([36, 68, 44, 88], fill=colors["primary"], outline=(0, 0, 0), width=1)
    draw.rectangle([52, 68, 60, 88], fill=colors["primary"], outline=(0, 0, 0), width=1)
    # Botas
    draw.rectangle([34, 86, 46, 92], fill=(100, 80, 40), outline=(0, 0, 0), width=1)
    draw.rectangle([50, 86, 62, 92], fill=(100, 80, 40), outline=(0, 0, 0), width=1)

def draw_tutu(draw, w, h, colors, frame):
    """Dibuja sprite de Tutu: escriba, con corona de hojas brillantes."""
    # Corona viva de hojas y flores
    draw.polygon([(36, 4), (42, 2), (48, 4), (54, 2), (60, 4), (58, 8), (52, 6), (48, 8), (44, 6), (38, 8)],
                 fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.ellipse([40, 2, 44, 6], fill=(255, 150, 100), outline=(0, 0, 0), width=1)
    draw.ellipse([52, 2, 56, 6], fill=(255, 150, 100), outline=(0, 0, 0), width=1)

    # Cabeza
    draw.ellipse([34, 10, 62, 28], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # Cabello (rojo-naranja ondulado)
    draw.rectangle([30, 12, 34, 26], fill=colors["primary"])
    draw.rectangle([62, 12, 66, 26], fill=colors["primary"])

    # Ojos (curiosos, inteligentes)
    if frame in ("idle", "speak"):
        draw.ellipse([40, 16, 46, 22], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([50, 16, 56, 22], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([41, 17, 45, 21], fill=(150, 100, 200))
        draw.ellipse([51, 17, 55, 21], fill=(150, 100, 200))
        draw.ellipse([42, 18, 44, 20], fill=(0, 0, 0))
        draw.ellipse([52, 18, 54, 20], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(40, 19), (46, 19)], fill=(0, 0, 0), width=2)
        draw.line([(50, 19), (56, 19)], fill=(0, 0, 0), width=2)

    # Boca (pensativa)
    if frame == "idle":
        draw.line([(44, 25), (52, 25)], fill=(200, 100, 50), width=1)
    elif frame == "speak":
        draw.ellipse([46, 24, 50, 28], fill=(200, 100, 50))

    # Torso (túnica roja con bordados)
    draw.rectangle([26, 30, 70, 70], fill=colors["primary"], outline=(0, 0, 0), width=2)
    # Bordados verdes (patrón)
    draw.line([(30, 40), (66, 40)], fill=colors["accent"], width=1)
    draw.line([(30, 50), (66, 50)], fill=colors["accent"], width=1)
    draw.line([(48, 32), (48, 68)], fill=colors["accent"], width=1)

    # Brazos
    draw.rectangle([18, 35, 26, 60], fill=colors["primary"], outline=(0, 0, 0), width=2)
    draw.rectangle([70, 35, 78, 60], fill=colors["primary"], outline=(0, 0, 0), width=2)

    # Manos
    draw.rectangle([18, 60, 26, 66], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([70, 60, 78, 66], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # Libro en mano izquierda
    draw.rectangle([12, 55, 18, 72], fill=(150, 100, 50), outline=(0, 0, 0), width=2)
    draw.line([(15, 55), (15, 72)], fill=(255, 200, 0), width=1)
    draw.line([(13, 60), (17, 60)], fill=(255, 200, 0), width=1)
    draw.line([(13, 65), (17, 65)], fill=(255, 200, 0), width=1)

    # Pluma en mano derecha
    draw.line([(76, 55), (80, 50)], fill=(100, 100, 100), width=2)
    draw.polygon([(78, 48), (80, 52), (82, 50)], fill=(255, 200, 0))

    # Piernas
    draw.rectangle([36, 70, 44, 88], fill=colors["primary"], outline=(0, 0, 0), width=1)
    draw.rectangle([52, 70, 60, 88], fill=colors["primary"], outline=(0, 0, 0), width=1)
    # Sandalias
    draw.rectangle([34, 86, 46, 92], fill=(100, 80, 40), outline=(0, 0, 0), width=1)
    draw.rectangle([50, 86, 62, 92], fill=(100, 80, 40), outline=(0, 0, 0), width=1)

DRAWERS = {
    "lilith": draw_lilith,
    "isis": draw_isis,
    "afrodita": draw_afrodita,
    "artemisa": draw_artemisa,
    "tutu": draw_tutu,
}

def gen_sprite(diosa: str, frame: str) -> None:
    """Genera sprite pixel art detallado."""
    if diosa not in DIOSAS:
        print(f"[!] Diosa desconocida: {diosa}")
        return

    info = DIOSAS[diosa]
    colors = {
        "primary": info["primary"],
        "secondary": info["secondary"],
        "accent": info["accent"],
        "skin": info["skin"],
    }

    # Canvas 96x96
    img = Image.new("RGBA", (96, 96), (230, 230, 230, 255))
    draw = ImageDraw.Draw(img)

    # Dibuja según diosa
    drawer = DRAWERS.get(diosa)
    if drawer:
        drawer(draw, 96, 96, colors, frame)

    OUT.mkdir(parents=True, exist_ok=True)
    destino = OUT / f"{diosa}-{frame}.png"
    img.save(destino)
    print(f"[OK] {destino}")

def main():
    ap = argparse.ArgumentParser(description="Genera sprites pixel art detallados.")
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
