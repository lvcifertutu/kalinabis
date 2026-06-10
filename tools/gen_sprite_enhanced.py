#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generador de sprites pixel art AVANZADO - alta calidad visual."""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).parent.parent / "public" / "sprites"

DIOSAS = {
    "lilith": {
        "name": "Lilith",
        "base": (100, 30, 150),       # púrpura base
        "light": (180, 100, 220),     # púrpura claro
        "dark": (60, 10, 80),         # púrpura oscuro
        "accent": (50, 255, 255),     # cian/teal
        "skin": (220, 160, 200),
        "hair_dark": (30, 0, 50),
    },
    "isis": {
        "name": "Isis",
        "base": (220, 160, 0),        # oro base
        "light": (255, 220, 100),     # oro claro
        "dark": (160, 100, 0),        # oro oscuro
        "accent": (255, 255, 255),    # blanco
        "skin": (230, 170, 130),
        "hair_dark": (100, 60, 0),
    },
    "afrodita": {
        "name": "Aphrodite",
        "base": (255, 120, 160),      # rosa base
        "light": (255, 200, 220),     # rosa claro
        "dark": (200, 60, 100),       # rosa oscuro
        "accent": (255, 200, 0),      # oro
        "skin": (250, 190, 170),
        "hair_dark": (200, 80, 120),
    },
    "artemisa": {
        "name": "Artemis",
        "base": (80, 160, 60),        # verde base
        "light": (150, 220, 100),     # verde claro
        "dark": (40, 100, 30),        # verde oscuro
        "accent": (200, 150, 0),      # bronce
        "skin": (220, 170, 140),
        "hair_dark": (100, 80, 40),
    },
    "tutu": {
        "name": "Tutu",
        "base": (220, 100, 40),       # naranja base
        "light": (255, 160, 80),      # naranja claro
        "dark": (160, 60, 0),         # naranja oscuro
        "accent": (100, 180, 60),     # verde hoja
        "skin": (240, 170, 140),
        "hair_dark": (180, 80, 20),
    },
}

def draw_pixel_line(draw, p1, p2, color, width=1):
    """Dibuja línea con grosor en pixel art."""
    x1, y1 = p1
    x2, y2 = p2
    if width == 1:
        draw.line([p1, p2], fill=color, width=1)
    else:
        for dx in range(-width//2, width//2+1):
            for dy in range(-width//2, width//2+1):
                draw.line([(x1+dx, y1+dy), (x2+dx, y2+dy)], fill=color, width=1)

def draw_lilith(draw, colors, frame):
    """Dibuja Lilith: diosa tormenta, gótica, intensa."""
    # CABELLO largo y ondulado (parte superior)
    draw.polygon([(30, 10), (35, 6), (40, 8), (45, 4), (50, 10), (55, 6), (60, 10)],
                 fill=colors["hair_dark"], outline=(0, 0, 0), width=1)
    # Ondas laterales del cabello
    draw.rectangle([20, 20, 25, 50], fill=colors["dark"])
    draw.rectangle([107, 20, 112, 50], fill=colors["dark"])

    # CABEZA
    draw.ellipse([35, 14, 67, 45], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # OJOS (según frame)
    if frame == "idle":
        # Ojos grandes y intensos
        draw.ellipse([42, 24, 50, 33], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([62, 24, 70, 33], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        # Iris teal
        draw.ellipse([44, 26, 48, 31], fill=colors["accent"])
        draw.ellipse([64, 26, 68, 31], fill=colors["accent"])
        # Pupila
        draw.ellipse([45, 27, 47, 30], fill=(0, 0, 0))
        draw.ellipse([65, 27, 67, 30], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(42, 28), (50, 28)], fill=(0, 0, 0), width=2)
        draw.line([(62, 28), (70, 28)], fill=(0, 0, 0), width=2)

    # NARIZ
    draw.line([(56, 32), (56, 38)], fill=(180, 130, 160), width=1)

    # BOCA
    if frame == "idle":
        draw.line([(48, 42), (64, 42)], fill=(150, 0, 30), width=2)
    elif frame == "speak":
        draw.ellipse([52, 41, 60, 46], fill=(150, 0, 30))

    # TORSO (ropa púrpura elaborada)
    draw.rectangle([25, 47, 77, 95], fill=colors["base"], outline=(0, 0, 0), width=2)
    # Detalles de ropa
    draw.rectangle([28, 50, 74, 54], fill=colors["light"])  # pecho
    draw.line([(56, 50), (56, 95)], fill=colors["accent"], width=2)  # línea central teal
    draw.rectangle([28, 70, 74, 74], fill=colors["dark"])  # cintura

    # BRAZOS
    draw.rectangle([15, 52, 25, 80], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([77, 52, 87, 80], fill=colors["base"], outline=(0, 0, 0), width=2)
    # Sombra brazos
    draw.rectangle([15, 52, 18, 80], fill=colors["dark"])
    draw.rectangle([84, 52, 87, 80], fill=colors["dark"])

    # MANOS (piel)
    draw.rectangle([15, 80, 25, 88], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([77, 80, 87, 88], fill=colors["skin"], outline=(0, 0, 0), width=1)
    # Collar/símbolo
    draw.ellipse([50, 44, 62, 50], fill=colors["accent"], outline=(0, 0, 0), width=2)
    draw.line([(56, 45), (56, 50)], fill=(0, 0, 0), width=1)

    # PIERNAS (púrpura oscuro)
    draw.rectangle([38, 95, 48, 125], fill=colors["dark"], outline=(0, 0, 0), width=1)
    draw.rectangle([64, 95, 74, 125], fill=colors["dark"], outline=(0, 0, 0), width=1)
    # Botas (negro con brillo)
    draw.rectangle([36, 122, 50, 128], fill=(20, 20, 20), outline=(0, 0, 0), width=1)
    draw.rectangle([62, 122, 76, 128], fill=(20, 20, 20), outline=(0, 0, 0), width=1)
    draw.rectangle([37, 122, 49, 124], fill=(100, 100, 100), width=0)

def draw_isis(draw, colors, frame):
    """Dibuja Isis: diosa madre, dorada, majestuosa."""
    # CORONA SOLAR (detalles)
    draw.polygon([(30, 10), (38, 4), (45, 8), (56, 4), (64, 10), (60, 16), (50, 12), (45, 14)],
                 fill=colors["base"], outline=(0, 0, 0), width=2)
    # Rayos solares
    for i in range(4):
        y = 8 + i*2
        draw.line([(28, y), (25, y)], fill=colors["light"], width=1)
        draw.line([(84, y), (87, y)], fill=colors["light"], width=1)

    # CABELLO largo (dorado oscuro)
    draw.rectangle([28, 16, 32, 50], fill=colors["hair_dark"])
    draw.rectangle([80, 16, 84, 50], fill=colors["hair_dark"])

    # CABEZA
    draw.ellipse([35, 16, 77, 48], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # OJOS (dulces)
    if frame == "idle":
        draw.ellipse([44, 26, 52, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([70, 26, 78, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([46, 28, 50, 33], fill=(200, 120, 0))
        draw.ellipse([72, 28, 76, 33], fill=(200, 120, 0))
        draw.ellipse([47, 29, 49, 32], fill=(0, 0, 0))
        draw.ellipse([73, 29, 75, 32], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(44, 30), (52, 30)], fill=(0, 0, 0), width=2)
        draw.line([(70, 30), (78, 30)], fill=(0, 0, 0), width=2)

    # NARIZ
    draw.line([(56, 34), (56, 40)], fill=(200, 150, 120), width=1)

    # BOCA (sonrisa cálida)
    if frame == "idle":
        draw.arc([(48, 40), (64, 46)], 0, 180, fill=(180, 80, 40), width=2)
    elif frame == "speak":
        draw.ellipse([52, 40, 60, 46], fill=(180, 80, 40))

    # TORSO (vestido blanco y oro)
    draw.rectangle([25, 50, 87, 105], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.rectangle([28, 52, 84, 58], fill=colors["base"])  # pecho dorado
    draw.rectangle([28, 80, 84, 86], fill=colors["base"])  # cintura dorada

    # BRAZOS
    draw.rectangle([12, 56, 25, 85], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.rectangle([87, 56, 100, 85], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.rectangle([12, 56, 15, 85], fill=(200, 200, 200))

    # MANOS
    draw.rectangle([12, 85, 25, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([87, 85, 100, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # ANKH (mano derecha, detallado)
    draw.ellipse([90, 80, 96, 86], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([93, 86, 95, 100], fill=colors["base"], outline=(0, 0, 0), width=1)
    draw.rectangle([91, 92, 97, 95], fill=colors["base"], outline=(0, 0, 0), width=1)

    # PIERNAS
    draw.rectangle([38, 105, 48, 125], fill=colors["base"], outline=(0, 0, 0), width=1)
    draw.rectangle([64, 105, 74, 125], fill=colors["base"], outline=(0, 0, 0), width=1)
    # Sandalias doradas
    draw.rectangle([36, 122, 50, 128], fill=colors["light"], outline=(0, 0, 0), width=1)
    draw.rectangle([62, 122, 76, 128], fill=colors["light"], outline=(0, 0, 0), width=1)

def draw_afrodita(draw, colors, frame):
    """Dibuja Afrodita: diosa amor, con alas."""
    # CORONA DE FLORES (colorida)
    flower_cols = [(255, 100, 150), (255, 150, 100), (100, 200, 255)]
    for i, fc in enumerate(flower_cols):
        x = 35 + i*15
        draw.ellipse([x-3, 8, x+3, 14], fill=fc, outline=(0, 0, 0), width=1)

    # CABELLO ondulado (dorado/rojo)
    draw.polygon([(30, 16), (35, 10), (40, 14), (45, 10), (50, 14), (55, 10), (60, 16)],
                 fill=colors["hair_dark"], outline=(0, 0, 0), width=1)

    # CABEZA
    draw.ellipse([35, 16, 77, 48], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # OJOS (brillantes, amorosos)
    if frame == "idle":
        draw.ellipse([44, 26, 52, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([70, 26, 78, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([46, 28, 50, 33], fill=(100, 200, 255))
        draw.ellipse([72, 28, 76, 33], fill=(100, 200, 255))
        # Brillo
        draw.ellipse([47, 27, 49, 29], fill=(255, 255, 255))
        draw.ellipse([73, 27, 75, 29], fill=(255, 255, 255))
    elif frame == "blink":
        draw.line([(44, 30), (52, 30)], fill=(0, 0, 0), width=2)
        draw.line([(70, 30), (78, 30)], fill=(0, 0, 0), width=2)

    # BOCA (sonrisa sensual)
    if frame == "idle":
        draw.arc([(48, 40), (64, 46)], 0, 180, fill=(255, 100, 150), width=2)
    elif frame == "speak":
        draw.ellipse([52, 40, 60, 46], fill=(255, 100, 150))

    # TORSO (vestido rosa elaborado)
    draw.rectangle([25, 50, 87, 105], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([28, 52, 84, 58], fill=colors["light"])
    # Diseño en V
    draw.polygon([(40, 52), (48, 65), (40, 65)], fill=colors["dark"])
    draw.polygon([(64, 52), (72, 65), (64, 65)], fill=colors["dark"])

    # ALAS (pequeñas, iridiscentes)
    draw.polygon([(15, 60), (20, 50), (23, 62)], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.polygon([(97, 60), (92, 50), (89, 62)], fill=colors["accent"], outline=(0, 0, 0), width=1)

    # BRAZOS
    draw.rectangle([12, 56, 25, 85], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([87, 56, 100, 85], fill=colors["base"], outline=(0, 0, 0), width=2)

    # MANOS
    draw.rectangle([12, 85, 25, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([87, 85, 100, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # PIERNAS
    draw.rectangle([38, 105, 48, 125], fill=colors["light"], outline=(0, 0, 0), width=1)
    draw.rectangle([64, 105, 74, 125], fill=colors["light"], outline=(0, 0, 0), width=1)
    # Sandalias florales
    draw.rectangle([36, 122, 50, 128], fill=colors["accent"], outline=(0, 0, 0), width=1)
    draw.rectangle([62, 122, 76, 128], fill=colors["accent"], outline=(0, 0, 0), width=1)
    for sx in [39, 45, 65, 71]:
        draw.ellipse([sx-2, 121, sx+2, 125], fill=(255, 100, 150), outline=(0, 0, 0), width=1)

def draw_artemisa(draw, colors, frame):
    """Dibuja Artemisa: cazadora, con corona de hojas."""
    # CORONA de hojas y ramas
    for i in range(5):
        x = 35 + i*10
        draw.polygon([(x, 8), (x+4, 4), (x+8, 8)], fill=colors["accent"], outline=(0, 0, 0), width=1)

    # CABELLO (castaño, ondulado)
    draw.polygon([(30, 16), (35, 10), (40, 14), (45, 10), (50, 14), (55, 10), (60, 16), (62, 20)],
                 fill=colors["hair_dark"], outline=(0, 0, 0), width=1)

    # CABEZA
    draw.ellipse([35, 16, 77, 48], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # OJOS (alerta, verdes)
    if frame == "idle":
        draw.ellipse([44, 26, 52, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([70, 26, 78, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([46, 28, 50, 33], fill=colors["base"])
        draw.ellipse([72, 28, 76, 33], fill=colors["base"])
        draw.ellipse([47, 29, 49, 32], fill=(0, 0, 0))
        draw.ellipse([73, 29, 75, 32], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(44, 30), (52, 30)], fill=(0, 0, 0), width=2)
        draw.line([(70, 30), (78, 30)], fill=(0, 0, 0), width=2)

    # BOCA (seria)
    if frame == "idle":
        draw.line([(48, 42), (64, 42)], fill=(150, 80, 60), width=1)
    elif frame == "speak":
        draw.ellipse([52, 40, 60, 45], fill=(150, 80, 60))

    # TORSO (vestido verde)
    draw.rectangle([25, 50, 87, 105], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([28, 52, 84, 58], fill=colors["light"])
    # Cinturón de cuero
    draw.rectangle([25, 75, 87, 80], fill=colors["accent"], outline=(0, 0, 0), width=2)

    # BRAZOS
    draw.rectangle([12, 56, 25, 85], fill=colors["light"], outline=(0, 0, 0), width=2)
    draw.rectangle([87, 56, 100, 85], fill=colors["light"], outline=(0, 0, 0), width=2)

    # MANOS
    draw.rectangle([12, 85, 25, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([87, 85, 100, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # CANASTA (mano izquierda)
    draw.rectangle([8, 75, 18, 92], fill=(160, 120, 80), outline=(0, 0, 0), width=2)
    draw.line([(13, 75), (13, 92)], fill=(200, 150, 100), width=1)
    # Manzanas en canasta
    draw.ellipse([6, 70, 12, 78], fill=(200, 50, 50), outline=(0, 0, 0), width=1)
    draw.ellipse([10, 68, 16, 76], fill=(200, 50, 50), outline=(0, 0, 0), width=1)

    # PIERNAS
    draw.rectangle([38, 105, 48, 125], fill=colors["base"], outline=(0, 0, 0), width=1)
    draw.rectangle([64, 105, 74, 125], fill=colors["base"], outline=(0, 0, 0), width=1)
    # Botas de cazadora
    draw.rectangle([36, 122, 50, 128], fill=(100, 80, 40), outline=(0, 0, 0), width=1)
    draw.rectangle([62, 122, 76, 128], fill=(100, 80, 40), outline=(0, 0, 0), width=1)

def draw_tutu(draw, colors, frame):
    """Dibuja Tutu: escriba mágico, con libro y corona viva."""
    # CORONA de hojas brillantes
    for i in range(6):
        x = 32 + i*9
        draw.polygon([(x, 8), (x+3, 2), (x+6, 8)], fill=colors["accent"], outline=(0, 0, 0), width=1)
    # Flores en corona
    for i in range(3):
        x = 38 + i*12
        draw.ellipse([x-3, 4, x+3, 10], fill=(255, 150, 100), outline=(0, 0, 0), width=1)

    # CABELLO (rojo-naranja ondulado)
    draw.rectangle([28, 16, 32, 45], fill=colors["hair_dark"])
    draw.rectangle([80, 16, 84, 45], fill=colors["hair_dark"])

    # CABEZA
    draw.ellipse([35, 16, 77, 48], fill=colors["skin"], outline=(0, 0, 0), width=2)

    # OJOS (curiosos, inteligentes)
    if frame == "idle":
        draw.ellipse([44, 26, 52, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([70, 26, 78, 35], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([46, 28, 50, 33], fill=(150, 100, 200))
        draw.ellipse([72, 28, 76, 33], fill=(150, 100, 200))
        draw.ellipse([47, 29, 49, 32], fill=(0, 0, 0))
        draw.ellipse([73, 29, 75, 32], fill=(0, 0, 0))
    elif frame == "blink":
        draw.line([(44, 30), (52, 30)], fill=(0, 0, 0), width=2)
        draw.line([(70, 30), (78, 30)], fill=(0, 0, 0), width=2)

    # BOCA (pensativa)
    if frame == "idle":
        draw.line([(48, 42), (64, 42)], fill=(200, 100, 60), width=1)
    elif frame == "speak":
        draw.ellipse([52, 40, 60, 46], fill=(200, 100, 60))

    # TORSO (túnica roja detallada)
    draw.rectangle([25, 50, 87, 105], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([28, 52, 84, 58], fill=colors["light"])
    # Bordados verdes (patrón)
    for y in [65, 75, 85]:
        for x in [35, 50, 65, 80]:
            draw.ellipse([x-2, y-2, x+2, y+2], fill=colors["accent"])

    # BRAZOS
    draw.rectangle([12, 56, 25, 85], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([87, 56, 100, 85], fill=colors["base"], outline=(0, 0, 0), width=2)
    draw.rectangle([12, 56, 15, 85], fill=colors["dark"])

    # MANOS
    draw.rectangle([12, 85, 25, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)
    draw.rectangle([87, 85, 100, 92], fill=colors["skin"], outline=(0, 0, 0), width=1)

    # LIBRO (mano izquierda, detallado)
    draw.rectangle([6, 70, 18, 95], fill=(150, 100, 50), outline=(0, 0, 0), width=2)
    draw.line([(12, 70), (12, 95)], fill=(255, 200, 0), width=2)  # lomo
    draw.line([(8, 75), (16, 75)], fill=(255, 200, 0), width=1)
    draw.line([(8, 80), (16, 80)], fill=(255, 200, 0), width=1)
    draw.line([(8, 85), (16, 85)], fill=(255, 200, 0), width=1)

    # PLUMA (mano derecha)
    draw.line([(95, 68), (102, 55)], fill=(100, 100, 100), width=2)
    draw.polygon([(100, 54), (102, 58), (104, 56)], fill=(255, 200, 0), outline=(0, 0, 0), width=1)

    # PIERNAS
    draw.rectangle([38, 105, 48, 125], fill=colors["base"], outline=(0, 0, 0), width=1)
    draw.rectangle([64, 105, 74, 125], fill=colors["base"], outline=(0, 0, 0), width=1)
    # Sandalias de viajero
    draw.rectangle([36, 122, 50, 128], fill=(100, 80, 40), outline=(0, 0, 0), width=1)
    draw.rectangle([62, 122, 76, 128], fill=(100, 80, 40), outline=(0, 0, 0), width=1)

DRAWERS = {
    "lilith": draw_lilith,
    "isis": draw_isis,
    "afrodita": draw_afrodita,
    "artemisa": draw_artemisa,
    "tutu": draw_tutu,
}

def gen_sprite(diosa: str, frame: str) -> None:
    """Genera sprite pixel art mejorado (128x128)."""
    if diosa not in DIOSAS:
        print(f"[!] Diosa desconocida: {diosa}")
        return

    info = DIOSAS[diosa]
    colors = {
        "base": info["base"],
        "light": info["light"],
        "dark": info["dark"],
        "accent": info["accent"],
        "skin": info["skin"],
        "hair_dark": info["hair_dark"],
    }

    # Canvas 128x128 (más detalle)
    img = Image.new("RGBA", (128, 128), (240, 240, 240, 255))
    draw = ImageDraw.Draw(img)

    # Dibuja según diosa
    drawer = DRAWERS.get(diosa)
    if drawer:
        drawer(draw, colors, frame)

    OUT.mkdir(parents=True, exist_ok=True)
    destino = OUT / f"{diosa}-{frame}.png"
    img.save(destino)
    print(f"[OK] {destino} (128x128)")

def main():
    ap = argparse.ArgumentParser(description="Genera sprites pixel art AVANZADOS (128x128).")
    ap.add_argument("--diosa", required=True, help="lilith | isis | afrodita | artemisa | tutu | todas")
    ap.add_argument("--frame", default="idle", help="idle | blink | speak")
    args = ap.parse_args()

    objetivos = list(DIOSAS) if args.diosa == "todas" else [args.diosa]

    for diosa in objetivos:
        if diosa not in DIOSAS:
            print(f"[!] Diosa desconocida: {diosa}")
            continue

        frames = ["idle", "blink", "speak"] if args.diosa == "todas" else [args.frame]
        for frame in frames:
            gen_sprite(diosa, frame)

if __name__ == "__main__":
    main()
