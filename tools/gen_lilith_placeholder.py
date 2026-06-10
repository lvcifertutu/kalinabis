# -*- coding: utf-8 -*-
"""Genera PNG placeholder de pixel art para Lilith (idle/blink/speak).

Es un placeholder para validar el pipeline de sprites end-to-end. Reemplazá
los PNG resultantes por tu arte IA pixelado final (mismos nombres).

Salida: public/sprites/lilith-idle.png, -blink.png, -speak.png
"""

from pathlib import Path
from PIL import Image

OUT = Path(__file__).parent.parent / "public" / "sprites"
OUT.mkdir(parents=True, exist_ok=True)

SCALE = 8          # cada "pixel" lógico = 8x8 px reales
GRID = 16          # lienzo lógico 16x16  ->  128x128 px

# Paleta (Lilith = cyan / La Sombra)
PAL = {
    " ": None,                  # transparente
    "H": (3, 60, 64, 255),      # pelo / sombra (teal oscuro)
    "O": (5, 120, 128, 255),    # contorno / párpado
    "F": (10, 190, 200, 255),   # cara (cyan medio)
    "E": (120, 255, 255, 255),  # ojo (cyan brillante)
    "W": (235, 255, 255, 255),  # brillo
    "M": (4, 40, 44, 255),      # boca (oscuro)
}

# Mapa base 16x16. Las filas de ojos/boca se sobrescriben por variante.
BASE = [
    "                ",
    "   H        H   ",
    "  HHH      HHH  ",
    "  HHHHHHHHHHHH  ",
    " HHFFFFFFFFFFHH ",
    " HFFFFFFFFFFFFH ",
    " HFFFFFFFFFFFFH ",  # ojos (fila 6)
    " HFFFFFFFFFFFFH ",  # ojos (fila 7)
    " HFFFFFFFFFFFFH ",
    " HFFFFFFFFFFFFH ",  # boca (fila 9)
    " HFFFFFFFFFFFFH ",  # boca (fila 10)
    " HFFFFFFFFFFFFH ",
    "  HFFFFFFFFFFH  ",
    "  HHFFFFFFFFHH  ",
    "   HHFFFFFFHH   ",
    "    HHHHHHHH     "[:16],
]

# Ojos abiertos (filas 6 y 7)
EYES_OPEN = {
    6: " HFFEWEFFEWEFFH "[:16],
    7: " HFFEEFFFFEEFFH "[:16],
}
# Ojos cerrados (parpadeo): párpado bajo, fila 7 una línea
EYES_SHUT = {
    6: " HFFFFFFFFFFFFH ",
    7: " HFFOOFFFFOOFFH ",
}
# Boca cerrada (idle/blink)
MOUTH_CLOSED = {
    9:  " HFFFFFFFFFFFFH ",
    10: " HFFFFMMMMFFFFH ",
}
# Boca abierta (speak)
MOUTH_OPEN = {
    9:  " HFFFFMMMMFFFFH ",
    10: " HFFFMMOOMMFFFH "[:16],
}


def build(rows_override: dict) -> list[str]:
    rows = list(BASE)
    for i, line in rows_override.items():
        rows[i] = (line + " " * GRID)[:GRID]
    return rows


def render(rows: list[str], path: Path) -> None:
    img = Image.new("RGBA", (GRID * SCALE, GRID * SCALE), (0, 0, 0, 0))
    px = img.load()
    for y, line in enumerate(rows):
        for x, ch in enumerate(line[:GRID]):
            color = PAL.get(ch)
            if color is None:
                continue
            for dy in range(SCALE):
                for dx in range(SCALE):
                    px[x * SCALE + dx, y * SCALE + dy] = color
    img.save(path)
    print(f"  [OK] {path.name}")


def main() -> None:
    idle = build({**EYES_OPEN, **MOUTH_CLOSED})
    blink = build({**EYES_SHUT, **MOUTH_CLOSED})
    speak = build({**EYES_OPEN, **MOUTH_OPEN})

    render(idle, OUT / "lilith-idle.png")
    render(blink, OUT / "lilith-blink.png")
    render(speak, OUT / "lilith-speak.png")
    print("Listo. Reemplazá estos PNG por tu arte IA pixelado (mismos nombres).")


if __name__ == "__main__":
    main()
