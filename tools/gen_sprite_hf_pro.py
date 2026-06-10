#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de sprites HF PRO - Calidad mejorada.

Basado en gen_sprite_hf.py pero con:
- Prompts optimizados para DreamShaper
- Parámetros de calidad superior
- Soporte para múltiples modelos
- Logging detallado

Uso:
  python tools/gen_sprite_hf_pro.py --diosa lilith --quality high
  python tools/gen_sprite_hf_pro.py --diosa todas --model artificialguintelligence/DreamShaper
"""

import argparse
import io
import os
import sys
import time
from pathlib import Path

# Fix encoding en Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
from PIL import Image

OUT = Path(__file__).parent.parent / "public" / "sprites"

# MODELOS RECOMENDADOS
MODELS_QUALITY = {
    "kohbanye/pixel-art-style": {
        "name": "Pixel Art Style",
        "speed": "fast",
        "quality": "basic",
    },
    "artificialguintelligence/DreamShaper": {
        "name": "DreamShaper (RECOMENDADO)",
        "speed": "medium",
        "quality": "excellent",
    },
    "nerijs/pixel-art-xl": {
        "name": "Pixel Art XL",
        "speed": "slow",
        "quality": "excellent",
    },
    "stabilityai/stable-diffusion-xl-base-1.0": {
        "name": "SDXL Base",
        "speed": "slow",
        "quality": "excellent",
    },
}

# PROMPTS ULTRA-OPTIMIZADOS para DreamShaper + SDXL
PROMPTS_ULTRA = {
    "lilith": {
        "base": (
            "masterpiece, best quality, 16-bit pixel art character sprite, "
            "full body standing pose, Lilith Nordic storm goddess, "
            "long flowing midnight black hair with teal electric streaks, "
            "pale translucent gothic skin, intense piercing violet eyes with power aura, "
            "sharp defined features, dominant confident expression, "
            "ornate deep teal velvet cloak flowing with wind, black silk bodysuit underneath, "
            "silver ornate necklace with mystical storm rune, "
            "centered isolated character, plain off-white background, "
            "dramatic atmospheric lighting, high contrast shadows, detailed shading, "
            "professional pixel art style, trending on artstation, 4k concept art"
        ),
    },
    "isis": {
        "base": (
            "masterpiece, best quality, 16-bit pixel art character sprite, "
            "full body standing pose, Isis Egyptian mother goddess, "
            "striking ornate Egyptian gold and white headdress with solar sun disk crown, "
            "warm compassionate mature face, kind gentle amber eyes, serene divine expression, "
            "golden honey-toned skin, elaborate heavy jewelry and golden ornaments, "
            "flowing white linen dress with gold brocade trim and intricate patterns, "
            "holding ornate golden ankh staff with sacred symbols, "
            "centered isolated character, plain cream background, "
            "warm divine golden lighting, soft ethereal glow, detailed shading, "
            "professional pixel art style, trending on artstation, 4k concept art"
        ),
    },
    "afrodita": {
        "base": (
            "masterpiece, best quality, 16-bit pixel art character sprite, "
            "full body standing pose, Aphrodite Greek love goddess, "
            "long flowing wavy auburn copper hair with natural shine, "
            "delicate beautiful ethereal face, serene dreamy aquamarine eyes, "
            "luminous peachy rose skin with natural blush, gentle kind expression, "
            "flowing coral silk dress with golden trim and delicate embroidery, "
            "delicate flower crown with blooming roses and baby's breath, "
            "shimmering translucent iridescent butterfly wings, "
            "graceful elegant pose with hand gesture, centered isolated character, "
            "plain soft-white background, soft romantic warm lighting with ethereal golden glow, "
            "professional pixel art style, trending on artstation, 4k concept art"
        ),
    },
    "artemisa": {
        "base": (
            "masterpiece, best quality, 16-bit pixel art character sprite, "
            "full body standing pose, Artemis earth huntress goddess, "
            "strong confident keen face, alert intelligent green eyes, warm brown sun-kissed skin, "
            "long thick braided auburn hair with natural leaf ornaments woven in, "
            "sage green fitted hunter dress with leather accents, "
            "brown leather belt with bronze buckle and hunter tools, "
            "holding woven basket overflowing with golden apples, "
            "grounded powerful stance with one leg forward, sure footed, "
            "centered isolated character, plain soft-green natural background, "
            "warm natural woodland sunlight, earthy tones, detailed shading, "
            "professional pixel art style, trending on artstation, 4k concept art"
        ),
    },
    "tutu": {
        "base": (
            "masterpiece, best quality, 16-bit pixel art character sprite, "
            "full body standing pose, Tutu androgynous scribe keeper of knowledge, "
            "soft curious intelligent face, warm gentle intelligent eyes, neutral serene expression, "
            "warm olive skin tone, flowing red linen tunic with intricate embroidered gold patterns, "
            "living magical crown made of intertwined vines, glowing flowers, and crystals, "
            "holding ornate leather-bound book open with glowing golden pages and runes, "
            "holding golden quill pen in other hand, thoughtful contemplative pose, "
            "one hand on chin, balanced centered stance, "
            "centered isolated character, plain soft-yellow background, "
            "warm magical lighting with subtle golden sparkles and book glow, "
            "professional pixel art style, trending on artstation, 4k concept art"
        ),
    },
}

# PROMPTS básicos (fallback si ULTRA no funciona)
PROMPTS_BASIC = {
    "lilith": "pixelartstyle, 16-bit character sprite, Lilith storm goddess, teal and purple colors, full body",
    "isis": "pixelartstyle, 16-bit character sprite, Isis goddess, gold and white Egyptian style, full body",
    "afrodita": "pixelartstyle, 16-bit character sprite, Aphrodite goddess, pink and gold romantic, full body",
    "artemisa": "pixelartstyle, 16-bit character sprite, Artemis huntress, green and bronze nature, full body",
    "tutu": "pixelartstyle, 16-bit character sprite, Tutu scribe, red and gold magical, full body",
}

# NEGATIVE PROMPTS (qué evitar)
NEGATIVE_ULTRA = (
    "blurry, jpeg artifacts, watermark, signature, text, multiple characters, "
    "cropped, partial body, deformed, distorted, bad anatomy, extra limbs, "
    "missing limbs, mutation, disfigured, poorly drawn, unfinished, "
    "low quality, sketch, ugly, dull, dark, oversaturated, "
    "realistic photo, 3d render, CGI, artificial, plastic looking, "
    "worst quality, bad quality, normal quality, low contrast"
)

NEGATIVE_BASIC = (
    "blurry, low quality, bad anatomy, poorly drawn, deformed"
)


def _token() -> str:
    """Obtiene token HF del entorno."""
    tok = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN")
    if not tok:
        print("[!] No hay token HF_TOKEN. Configura:")
        print("    PowerShell: $env:HF_TOKEN = 'hf_xxx'")
        print("    Obtén en: https://huggingface.co/settings/tokens")
        sys.exit(1)
    return tok


def generar(diosa: str, model: str, token: str, quality: str = "high") -> bytes:
    """Llama a HF Inference API con parámetros de calidad."""
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "image/png"}

    # Selecciona prompts y parámetros según calidad
    if quality == "ultra":
        prompt = PROMPTS_ULTRA.get(diosa, PROMPTS_BASIC[diosa])
        negative = NEGATIVE_ULTRA
        steps = 50
        guidance = 8.0
    elif quality == "high":
        prompt = PROMPTS_ULTRA.get(diosa, PROMPTS_BASIC[diosa])
        negative = NEGATIVE_ULTRA
        steps = 40
        guidance = 7.5
    else:  # fast
        prompt = PROMPTS_BASIC[diosa]
        negative = NEGATIVE_BASIC
        steps = 25
        guidance = 7.0

    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative,
            "num_inference_steps": steps,
            "guidance_scale": guidance,
            "width": 512,
            "height": 512,
        },
        "options": {"wait_for_model": True},
    }

    print(f"  [{diosa.upper()}] {quality.upper()} quality, {steps} steps, guidance {guidance}...", flush=True)

    for intento in range(1, 6):
        resp = requests.post(url, headers=headers, json=payload, timeout=120)

        if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("image"):
            size_mb = len(resp.content) / (1024*1024)
            print(f"    ✓ OK ({size_mb:.1f}MB)")
            return resp.content

        if resp.status_code == 503:
            print(f"    ⏳ Modelo cargando, reintento {intento}/5...", flush=True)
            time.sleep(8)
            continue

        # Error
        detalle = resp.text[:200]
        print(f"    ✗ Error {resp.status_code}: {detalle[:80]}")
        raise RuntimeError(f"HF API {resp.status_code}: {detalle}")

    raise RuntimeError("El modelo no respondió tras 5 reintentos")


def pixelar(data: bytes, size: int = 96) -> Image.Image:
    """Downscale + cuantización a look pixel art."""
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    w, h = img.size

    # Resize manteniendo aspecto
    target_h = max(1, round(size * h / w))
    img = img.resize((size, target_h), Image.NEAREST)

    # Cuantizar colores (paleta reducida = pixel art look)
    alpha = img.getchannel("A")
    rgb = img.convert("RGB").quantize(colors=32).convert("RGBA")
    rgb.putalpha(alpha)

    return rgb


def procesar(diosa: str, model: str, token: str, quality: str) -> None:
    """Genera y guarda sprite."""
    try:
        data = generar(diosa, model, token, quality)
        img = pixelar(data)

        OUT.mkdir(parents=True, exist_ok=True)
        destino = OUT / f"{diosa}-idle.png"
        img.save(destino)

        print(f"    ✓ Guardado: {destino} ({img.width}x{img.height})")
        print(f"    💡 Próximo: edita blink/speak con Aseprite/Piskel desde {diosa}-idle.png")

    except Exception as e:
        print(f"    ✗ ERROR: {e}")


def main():
    ap = argparse.ArgumentParser(
        description="Generador HF PRO - Sprites con calidad mejorada"
    )
    ap.add_argument(
        "--diosa",
        required=True,
        help="lilith | isis | afrodita | artemisa | tutu | todas",
    )
    ap.add_argument(
        "--model",
        default="artificialguintelligence/DreamShaper",
        help="Modelo HF (ver --list-models)",
    )
    ap.add_argument(
        "--quality",
        default="high",
        choices=["fast", "high", "ultra"],
        help="fast(25 steps) | high(40) | ultra(50)",
    )
    ap.add_argument(
        "--list-models",
        action="store_true",
        help="Muestra modelos disponibles",
    )

    args = ap.parse_args()

    if args.list_models:
        print("\n" + "="*70)
        print("MODELOS DISPONIBLES EN HF API")
        print("="*70)
        for model, info in MODELS_QUALITY.items():
            print(f"\n  {info['name']}")
            print(f"    Model: {model}")
            print(f"    Speed: {info['speed']} | Quality: {info['quality']}")
        print()
        return

    # Verificar token
    token = _token()

    # Procesar diosas
    objetivos = list(PROMPTS_ULTRA) if args.diosa == "todas" else [args.diosa]

    print("\n" + "="*70)
    print("GENERADOR HF PRO - PIXEL ART")
    print("="*70)
    print(f"Modelo: {args.model}")
    print(f"Calidad: {args.quality.upper()}")
    print("="*70 + "\n")

    for diosa in objetivos:
        if diosa not in PROMPTS_ULTRA:
            print(f"[!] Diosa desconocida: {diosa}")
            continue

        procesar(diosa, args.model, token, args.quality)

    print("\n" + "="*70)
    print("✓ Completado. Ahora edita los sprites en Aseprite para frames blink/speak")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
