#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST: Conexión a HF + comparación de modelos para mejorar calidad de pixel art.
"""

import os
import sys
import io

# Fix encoding Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import json
from pathlib import Path

# ============================================================================
# 1. VERIFICAR CREDENCIALES
# ============================================================================

def check_hf_token() -> str | None:
    """Busca HF_TOKEN en variables de entorno."""
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN")
    if token:
        print(f"✓ Token HF encontrado ({len(token)} chars)")
        return token
    print("✗ NO hay token HF. Configura HF_TOKEN en PowerShell:")
    print("  $env:HF_TOKEN = 'hf_xxxxxxxxxxxxx'")
    print("  Obtén token en: https://huggingface.co/settings/tokens")
    return None


# ============================================================================
# 2. MODELOS DISPONIBLES PARA PIXEL ART
# ============================================================================

MODELS = {
    "kohbanye/pixel-art-style": {
        "desc": "Pixel Art Style (Stable Diffusion 1.5)",
        "type": "SD1.5 fine-tuned",
        "speed": "⚡ Rápido (5-10s)",
        "quality": "⭐⭐⭐ Basico (puede ser genérico)",
        "serverless": True,
        "cost": "Bajo",
    },
    "nerijs/pixel-art-xl": {
        "desc": "Pixel Art XL (LoRA SDXL)",
        "type": "SDXL LoRA",
        "speed": "⚡⚡ Medio (15-25s)",
        "quality": "⭐⭐⭐⭐ Muy bueno",
        "serverless": "Incierto (LoRA)",
        "cost": "Medio",
    },
    "artificialguintelligence/DreamShaper": {
        "desc": "DreamShaper (SDXL fine-tuned)",
        "type": "SDXL fine-tuned",
        "speed": "⚡⚡ Medio (15-25s)",
        "quality": "⭐⭐⭐⭐ Excelente",
        "serverless": True,
        "cost": "Medio",
    },
    "stabilityai/stable-diffusion-xl-base-1.0": {
        "desc": "SDXL Base (genérico + post-pixelado)",
        "type": "SDXL base",
        "speed": "⚡⚡⚡ Lento en API",
        "quality": "⭐⭐⭐⭐⭐ Alto (pixelas después)",
        "serverless": False,
        "cost": "Local (gratis si tienes GPU)",
    },
    "playgroundai/playground-v2.5": {
        "desc": "Playground v2.5 (genérico + pixelado)",
        "type": "Genérico mejorado",
        "speed": "⚡⚡ Medio",
        "quality": "⭐⭐⭐⭐ Bueno",
        "serverless": True,
        "cost": "Medio",
    },
}


# ============================================================================
# 3. PROBAR CONEXIÓN A HF
# ============================================================================

def test_hf_connection(token: str, model: str) -> bool:
    """Prueba si el modelo está disponible en HF API."""
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}

    # GET para verificar disponibilidad (sin generar imagen)
    resp = requests.get(url, headers=headers, timeout=10)

    if resp.status_code == 200:
        print(f"  ✓ {model}: DISPONIBLE")
        return True
    elif resp.status_code == 404:
        print(f"  ✗ {model}: NO ENCONTRADO")
        return False
    elif resp.status_code == 401:
        print(f"  ✗ {model}: TOKEN INVÁLIDO")
        return False
    elif resp.status_code == 503:
        print(f"  ⏳ {model}: Modelo cargando (intentar luego)")
        return True
    else:
        print(f"  ? {model}: Status {resp.status_code}")
        return False


def test_hf_generation(token: str, model: str) -> bool:
    """Prueba generación real con un prompt pequeño."""
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "image/png"}

    # Prompt pequeño para prueba rápida
    payload = {
        "inputs": "pixelart, 16-bit, goddess character, full body",
        "parameters": {
            "negative_prompt": "blurry, low quality",
            "num_inference_steps": 25,
            "guidance_scale": 7.0,
        },
        "options": {"wait_for_model": True},
    }

    print(f"  Generando con {model}...", end=" ", flush=True)

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)

        if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("image"):
            size_mb = len(resp.content) / (1024*1024)
            print(f"✓ OK ({size_mb:.1f}MB)")
            return True
        elif resp.status_code == 503:
            print(f"⏳ Cargando modelo (reintentar)")
            return False
        else:
            print(f"✗ Error {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return False


# ============================================================================
# 4. MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("TEST: Hugging Face + Modelos de Pixel Art")
    print("=" * 70)

    # Verificar token
    token = check_hf_token()
    print()

    if not token:
        print("\n📌 SOLUCIÓN: Configura el token HF")
        print("   1. Ve a https://huggingface.co/settings/tokens")
        print("   2. Crea un token (rol: read)")
        print("   3. En PowerShell:")
        print("      $env:HF_TOKEN = 'hf_xxxxx'")
        print("   4. Corre este script de nuevo")
        return

    # Mostrar modelos
    print("\n" + "=" * 70)
    print("MODELOS DISPONIBLES PARA PIXEL ART")
    print("=" * 70)

    for model, info in MODELS.items():
        print(f"\n📦 {info['desc']}")
        print(f"   Tipo: {info['type']}")
        print(f"   Velocidad: {info['speed']}")
        print(f"   Calidad: {info['quality']}")
        print(f"   Serverless: {info['serverless']}")
        print(f"   Coste: {info['cost']}")

    # Probar disponibilidad
    print("\n" + "=" * 70)
    print("PROBANDO DISPONIBILIDAD EN HF API")
    print("=" * 70 + "\n")

    available = {}
    for model in MODELS:
        if test_hf_connection(token, model):
            available[model] = MODELS[model]

    # Probar generación
    print("\n" + "=" * 70)
    print("PROBANDO GENERACIÓN (modelo rápido)")
    print("=" * 70 + "\n")

    if "kohbanye/pixel-art-style" in available:
        test_hf_generation(token, "kohbanye/pixel-art-style")
    elif "artificialguintelligence/DreamShaper" in available:
        test_hf_generation(token, "artificialguintelligence/DreamShaper")

    # Recomendaciones
    print("\n" + "=" * 70)
    print("RECOMENDACIÓN PARA MEJORAR CALIDAD")
    print("=" * 70 + "\n")

    recommendations = {
        "DreamShaper": "artificialguintelligence/DreamShaper (SDXL, excelente calidad, accesible)",
        "nerijs/pixel-art-xl": "nerijs/pixel-art-xl (LoRA SDXL, muy bueno)",
        "kohbanye": "kohbanye/pixel-art-style (rápido, básico, usar como fallback)",
    }

    print("✅ MEJOR OPCIÓN ACTUAL (HF API):")
    print(f"   → {recommendations['DreamShaper']}")
    print("\n📋 USO:")
    print("   python tools/gen_sprite_hf.py --diosa lilith --model artificialguintelligence/DreamShaper")

    print("\n✅ MEJOR OPCIÓN A FUTURO (Local, si tienes GPU):")
    print(f"   → {recommendations['nerijs/pixel-art-xl']}")
    print("     (Requiere: pip install diffusers torch transformers)")
    print("     python tools/gen_sprite_pixelart_xl.py --diosa lilith")

    print("\n✅ PARA PIXEL ART PROGRAMÁTICO (Sin IA, consistente):")
    print("   → gen_sprite_enhanced.py (128x128 dibujado a mano con PIL)")
    print("     python tools/gen_sprite_enhanced.py --diosa lilith --frame idle")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
