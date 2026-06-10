#!/usr/bin/env python3
"""Post-procesamiento de sprites generados con SDXL.

Mejora calidad de sprites mediante:
- Aumento de constraste local
- Reducción de ruido
- Ajuste de colores para mejor legibilidad
- Detección y mejora de bordes
"""

import argparse
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

SPRITES_DIR = Path(__file__).parent.parent / "public" / "sprites"


def enhance_sprite(image: Image.Image) -> Image.Image:
    """Aplica mejoras a un sprite para mejor visualización."""
    # 1. Reducir ruido con filtro mediano (preserva bordes)
    img_array = np.array(image)
    if image.mode == 'RGBA':
        # Aplicar filtro solo a los canales RGB, preservar alpha
        from scipy import ndimage
        for i in range(3):
            img_array[:, :, i] = ndimage.median_filter(img_array[:, :, i], size=2)
    image = Image.fromarray(img_array.astype('uint8'))

    # 2. Aumentar contraste
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)

    # 3. Aumentar saturación (si no es RGBA)
    if image.mode != 'RGBA':
        image = image.convert('RGB')
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.15)

    # 4. Sharpening moderado
    image = image.filter(ImageFilter.SHARPEN)

    return image


def process_sprites(pattern: str = "*-idle.png") -> None:
    """Procesa todos los sprites que coincidan con el patrón."""
    SPRITES_DIR.mkdir(parents=True, exist_ok=True)

    sprites = list(SPRITES_DIR.glob(pattern))
    if not sprites:
        print(f"[!] No sprites encontrados con patrón: {pattern}")
        return

    print(f"[*] Mejorando {len(sprites)} sprites...")

    for sprite_path in sprites:
        try:
            img = Image.open(sprite_path)
            enhanced = enhance_sprite(img)
            enhanced.save(sprite_path)
            print(f"    [OK] {sprite_path.name}")
        except Exception as e:
            print(f"    [ERROR] {sprite_path.name}: {e}")

    print("[OK] Post-procesamiento completado")


def main():
    ap = argparse.ArgumentParser(
        description="Post-procesa sprites SDXL para mejor visualización."
    )
    ap.add_argument(
        "--pattern",
        default="*-idle.png",
        help="Patrón de archivo para procesar (default: *-idle.png)",
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help="Procesar todos los sprites (*.png)",
    )
    args = ap.parse_args()

    pattern = "*.png" if args.all else args.pattern
    process_sprites(pattern)


if __name__ == "__main__":
    main()
