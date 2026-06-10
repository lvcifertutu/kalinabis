#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generador de sprites con nerijs/pixel-art-xl (local, sin HF API)."""

import argparse
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline
from PIL import Image

OUT = Path(__file__).parent.parent / "public" / "sprites"

# Prompts mejorados para pixel art XL
PROMPTS = {
    "lilith": (
        "pixelart, 16-bit style, full body character sprite, Lilith dark storm goddess, "
        "long windswept midnight black hair with teal streaks, pale gothic skin, intense piercing violet eyes, "
        "flowing deep teal velvet cloak with black accents, ornate silver necklace with storm symbol, "
        "confident dominant stance, high quality, detailed, centered, isolated character, "
        "plain off-white background, trending on artstation"
    ),
    "isis": (
        "pixelart, 16-bit style, full body character sprite, Isis Egyptian mother goddess, "
        "striking gold and white Egyptian headdress with solar crown, warm compassionate face, "
        "kind eyes, flowing white and gold linen dress, golden ornaments and jewelry, "
        "holding ornate golden ankh staff, graceful serene posture, high quality, detailed, centered, "
        "isolated character, plain cream background, trending on artstation"
    ),
    "afrodita": (
        "pixelart, 16-bit style, full body character sprite, Aphrodite love goddess, "
        "long flowing auburn hair, delicate beautiful face, serene dreamy eyes, luminous peachy skin, "
        "flowing coral-pink silk dress with golden trim, delicate flower crown with roses, "
        "shimmering iridescent wings, graceful pose with elegant hand gesture, full body visible, centered, "
        "soft romantic lighting with ethereal glow, high quality, detailed, "
        "plain soft-white background, isolated character, trending on artstation"
    ),
    "artemisa": (
        "pixelart, 16-bit style, full body character sprite, Artemis earth huntress, "
        "strong confident face, keen alert green eyes, warm brown skin, long braided auburn hair with leaf ornaments, "
        "sage green fitted dress, brown leather belt with bronze buckle, holding woven basket of golden apples, "
        "grounded powerful stance with one leg forward, full body visible, centered, "
        "warm natural woodland lighting, high quality, detailed, "
        "plain soft-green background, isolated character, trending on artstation"
    ),
    "tutu": (
        "pixelart, 16-bit style, full body character sprite, Tutu androgynous scribe keeper, "
        "soft curious face, warm intelligent eyes, neutral expression, flowing red linen tunic with intricate embroidered patterns, "
        "living leafy crown made of vines and small glowing flowers, holding ornate leather-bound book open with glowing pages, "
        "holding quill, thoughtful pose with one hand on chin, full body centered, balanced stance, "
        "warm magical lighting with subtle sparkles, high quality, detailed, "
        "plain soft-yellow background, isolated character, trending on artstation"
    ),
}

NEGATIVE = (
    "blurry, jpeg artifacts, watermark, signature, text overlay, multiple characters, "
    "cropped limbs, deformed body, extra limbs, realistic photo, 3d render, "
    "bad anatomy, poorly drawn, unfinished, low quality, asymmetrical, weird proportions, "
    "distorted, worst quality"
)

def load_model(device: str = "cuda") -> StableDiffusionXLPipeline:
    """Carga nerijs/pixel-art-xl. Primera vez tarda (~3GB descarga)."""
    print("[*] Cargando stabilityai/stable-diffusion-xl-base-1.0...")
    print("    (Primera vez: ~6GB descarga + ~1min carga)")

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        use_safetensors=True,
    )

    if device == "cuda" and torch.cuda.is_available():
        pipe = pipe.to("cuda")
        pipe.enable_attention_slicing()
    else:
        pipe = pipe.to("cpu")

    print("[OK] Modelo cargado")
    return pipe

def generar(diosa: str, pipe: StableDiffusionXLPipeline) -> Image.Image:
    """Genera imagen con el modelo."""
    prompt = PROMPTS[diosa]

    print(f"[{diosa}] Generando con nerijs/pixel-art-xl...")

    image = pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE,
        num_inference_steps=30,  # Rápido pero buena calidad
        guidance_scale=7.5,
        height=512,
        width=512,
    ).images[0]

    # Redimensionar a 128x128 (sprite final)
    image = image.resize((128, 128), Image.LANCZOS)

    return image

def procesar(diosa: str, frame: str, pipe: StableDiffusionXLPipeline) -> None:
    """Genera sprite para frame (idle/blink/speak usa mismo generado)."""
    img = generar(diosa, pipe)

    OUT.mkdir(parents=True, exist_ok=True)
    destino = OUT / f"{diosa}-{frame}.png"
    img.save(destino)
    print(f"    [OK] {destino}")

def main():
    ap = argparse.ArgumentParser(description="Genera sprites con nerijs/pixel-art-xl (local).")
    ap.add_argument("--diosa", required=True, help="lilith | isis | afrodita | artemisa | tutu | todas")
    args = ap.parse_args()

    # Detectar dispositivo
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[*] Usando: {device}")

    # Cargar modelo una sola vez
    pipe = load_model(device)

    # Generar
    objetivos = list(PROMPTS) if args.diosa == "todas" else [args.diosa]

    for diosa in objetivos:
        if diosa not in PROMPTS:
            print(f"[!] Diosa desconocida: {diosa}")
            continue

        try:
            # Para cada diosa, genera 3 frames (mismo sprite para todos)
            for frame in ["idle", "blink", "speak"]:
                procesar(diosa, frame, pipe)
        except Exception as e:
            print(f"    [ERROR] {e}")

if __name__ == "__main__":
    main()
