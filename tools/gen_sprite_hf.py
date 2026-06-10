# -*- coding: utf-8 -*-
"""Genera el sprite base (idle) de una diosa usando un modelo de Hugging Face.

Herramienta de DISEÑO (no se usa en vivo en la app). Llama a la Inference API
de HF con un modelo de pixel art, descarga la imagen y la pixela (downscale +
paleta reducida) con Pillow. El resultado va a public/sprites/<diosa>-idle.png.

Requisitos:
  - Token de HF en entorno: HF_TOKEN (o HUGGINGFACE_API_TOKEN)
    Sacalo en https://huggingface.co/settings/tokens (rol: read)
  - pip install pillow   (requests ya viene)

Uso:
  python tools/gen_sprite_hf.py --diosa lilith
  python tools/gen_sprite_hf.py --diosa todas
  python tools/gen_sprite_hf.py --diosa afrodita --model kohbanye/pixel-art-style

Frames blink/speak: este script genera el IDLE. Derivá blink (ojos cerrados) y
speak (boca abierta) editando ese PNG en Piskel/Aseprite — así quedan
consistentes (el modelo no mantiene el mismo personaje entre generaciones).

MEJORAS DE CALIDAD:
- Prompts mejorados con más detalles visuales y estilo
- num_inference_steps: aumentá a 75+ para más detalle (pero tarda más)
- guidance_scale: 7.5 por defecto; 8-9 para seguir más el prompt, 5-6 para más creatividad
- Probá diferentes modelos:
    * kohbanye/pixel-art-style (actual, rápido pero básico)
    * stabilityai/stable-diffusion-xl (mejor calidad, más lento)
    * artificialguintelligence/DreamShaper (buen balance)
"""

import argparse
import io
import os
import sys
import time
from pathlib import Path

import requests

try:
    from PIL import Image
except ImportError:
    print("[!] Falta Pillow. Ejecutá: pip install pillow")
    sys.exit(1)

OUT = Path(__file__).parent.parent / "public" / "sprites"

# Modelo por defecto. Alternativas (pasalas con --model):
#   kohbanye/pixel-art-style          (SD1.5, trigger 'pixelartstyle')
#   nerijs/pixel-art-xl               (SDXL LoRA; puede no estar en serverless)
#   stabilityai/stable-diffusion-xl-base-1.0  (genérico + se pixela después)
# La disponibilidad en la API serverless varía; si da 404, probá otro o PRO.
DEFAULT_MODEL = "kohbanye/pixel-art-style"

# Ancho objetivo del pixel art (alto se deriva por aspecto, vertical).
TARGET_W = 96
# Paleta máxima (look pixel art). 0 = no cuantizar.
MAX_COLORS = 32

NEGATIVE = (
    "blurry, jpeg artifacts, watermark, signature, text overlay, multiple characters, "
    "cropped limbs, deformed body, extra limbs, realistic photo, 3d render, "
    "bad anatomy, poorly drawn, unfinished, low quality, pixelated blur, "
    "worst quality, distorted, asymmetrical, weird proportions"
)

# Prompts por entidad — optimizados para mejor calidad pixel art.
# Estructura: personaje + rasgos + ropa + accesorios + pose + estilo + calidad
PROMPTS = {
    "lilith": (
        "pixelartstyle, 16-bit style character sprite, Lilith Nordic storm goddess, "
        "long wavy windswept midnight black hair with teal highlights, pale gothic skin, "
        "intense piercing violet eyes, dominant expression, flowing deep teal velvet cloak "
        "with black accents, dark bodysuit, ornate silver necklace with storm symbol, "
        "full body standing pose, centered composition, confident stance, "
        "dramatic atmospheric lighting, detailed pixel art, high quality, "
        "plain off-white background, isolated character, trending on artstation"
    ),
    "isis": (
        "pixelartstyle, 16-bit style character sprite, Isis Egyptian mother goddess, "
        "striking gold and white Egyptian headdress with solar crown, gentle warm face, "
        "kind compassionate eyes, serene expression, flowing white and gold linen dress, "
        "golden ornaments and jewelry, holding ornate golden ankh staff, "
        "full body standing pose centered, graceful posture, warm divine lighting, "
        "detailed pixel art, high quality, soft elegant aesthetic, "
        "plain cream background, isolated character, trending on artstation"
    ),
    "afrodita": (
        "pixelartstyle, 16-bit style character sprite, Aphrodite love goddess, "
        "long flowing auburn hair, delicate beautiful face, serene dreamy eyes, "
        "luminous peachy skin, flowing coral-pink silk dress with golden trim, "
        "delicate flower crown with roses, shimmering iridescent wings, "
        "graceful pose with elegant hand gesture, full body visible, centered, "
        "soft romantic lighting with ethereal glow, detailed pixel art, high quality, "
        "plain soft-white background, isolated character, trending on artstation"
    ),
    "artemisa": (
        "pixelartstyle, 16-bit style character sprite, Artemis earth huntress, "
        "strong confident face, keen alert green eyes, warm brown skin, "
        "long braided auburn hair with leaf ornaments, sage green fitted dress, "
        "brown leather belt with bronze buckle, holding woven basket of golden apples, "
        "grounded powerful stance, one leg forward, full body visible, centered, "
        "warm natural woodland lighting, detailed pixel art, high quality, "
        "plain soft-green background, isolated character, trending on artstation"
    ),
    "tutu": (
        "pixelartstyle, 16-bit style character sprite, Tutu androgynous scribe keeper, "
        "soft curious face, warm intelligent eyes, neutral expression, "
        "flowing red linen tunic with intricate embroidered patterns, "
        "living leafy crown made of vines and small glowing flowers, "
        "holding ornate leather-bound book open with glowing pages, holding quill, "
        "thoughtful pose, one hand on chin, full body centered, balanced stance, "
        "warm magical lighting with subtle sparkles, detailed pixel art, high quality, "
        "plain soft-yellow background, isolated character, trending on artstation"
    ),
}


def _token() -> str:
    tok = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN")
    if not tok:
        print(
            "[!] No hay token. Seteá HF_TOKEN en el entorno:\n"
            "    PowerShell:  $env:HF_TOKEN = 'hf_xxx'\n"
            "    Token en:    https://huggingface.co/settings/tokens"
        )
        sys.exit(1)
    return tok


def generar(diosa: str, model: str, token: str) -> bytes:
    """Llama a la Inference API y devuelve los bytes de la imagen."""
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "image/png"}

    # Parámetros para mejor calidad (ajustar según modelo).
    payload = {
        "inputs": PROMPTS[diosa],
        "parameters": {
            "negative_prompt": NEGATIVE,
            "num_inference_steps": 50,  # Más pasos = más detalle (pero más lento)
            "guidance_scale": 7.5,       # Cuán fuerte seguir el prompt (7-8 es bueno)
        },
        "options": {"wait_for_model": True},
    }

    for intento in range(1, 6):
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("image"):
            return resp.content
        if resp.status_code == 503:
            print(f"    modelo cargando, reintento {intento}/5...")
            time.sleep(8)
            continue
        # Error claro
        detalle = resp.text[:300]
        raise RuntimeError(f"HF {resp.status_code}: {detalle}")
    raise RuntimeError("El modelo no respondió tras varios reintentos.")


def pixelar(data: bytes) -> Image.Image:
    """Downscale + cuantización de paleta para el look pixel art."""
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    w, h = img.size
    target_h = max(1, round(TARGET_W * h / w))
    img = img.resize((TARGET_W, target_h), Image.NEAREST)
    if MAX_COLORS:
        # Cuantizar respetando alpha: separar, cuantizar RGB, reponer alpha.
        alpha = img.getchannel("A")
        rgb = img.convert("RGB").quantize(colors=MAX_COLORS).convert("RGBA")
        rgb.putalpha(alpha)
        img = rgb
    return img


def procesar(diosa: str, model: str, token: str) -> None:
    print(f"[{diosa}] generando con {model}...")
    data = generar(diosa, model, token)
    img = pixelar(data)
    OUT.mkdir(parents=True, exist_ok=True)
    destino = OUT / f"{diosa}-idle.png"
    img.save(destino)
    print(f"    [OK] {destino}  ({img.width}x{img.height})")
    print(f"    -> derivá {diosa}-blink.png y {diosa}-speak.png editando este PNG.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Genera sprites con Hugging Face.")
    ap.add_argument(
        "--diosa",
        required=True,
        help="lilith | isis | afrodita | artemisa | tutu | todas",
    )
    ap.add_argument("--model", default=DEFAULT_MODEL, help="repo del modelo HF")
    args = ap.parse_args()

    token = _token()
    objetivos = list(PROMPTS) if args.diosa == "todas" else [args.diosa]
    for d in objetivos:
        if d not in PROMPTS:
            print(f"[!] Diosa desconocida: {d}")
            continue
        try:
            procesar(d, args.model, token)
        except Exception as e:
            print(f"    [ERROR] {e}")


if __name__ == "__main__":
    main()
