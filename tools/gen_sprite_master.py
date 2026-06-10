#!/usr/bin/env python3
"""Generador maestro de sprites con fallback automático.

Intenta generar sprites en este orden:
1. SDXL (mejor calidad, más lento, requiere ~6GB)
2. Enhanced (calidad buena, rápido)
3. Local (básico, muy rápido)

Cae al siguiente modo si el anterior falla.
"""

import argparse
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).parent

GENERATORS = [
    ("sdxl", "gen_sprite_pixelart_xl.py", "~2min/diosa, máxima calidad"),
    ("enhanced", "gen_sprite_enhanced.py", "~1seg/diosa, buena calidad"),
    ("local", "gen_sprite_local.py", "~0.5seg/diosa, básico"),
]

DEITIES = ["lilith", "isis", "afrodita", "artemisa", "tutu"]


def run_generator(script: str, diosa: str, timeout: int = 300) -> bool:
    """Ejecuta un generador de sprites. Retorna True si tiene éxito."""
    try:
        result = subprocess.run(
            [sys.executable, str(TOOLS / script), "--diosa", diosa],
            timeout=timeout,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"    [ERROR] {e}")
        return False


def main():
    ap = argparse.ArgumentParser(
        description="Genera sprites con fallback automático entre modos."
    )
    ap.add_argument(
        "--diosa",
        required=True,
        help="Diosa a generar (lilith | isis | afrodita | artemisa | tutu | todas)",
    )
    ap.add_argument(
        "--prefer",
        choices=["sdxl", "enhanced", "local"],
        default="sdxl",
        help="Modo preferido (default: sdxl con fallback automático)",
    )
    ap.add_argument(
        "--force-mode",
        choices=["sdxl", "enhanced", "local"],
        help="Forzar modo específico sin fallback",
    )
    args = ap.parse_args()

    # Determinar orden de generadores
    if args.force_mode:
        generator_order = [
            g for g in GENERATORS if g[0] == args.force_mode
        ]
        if not generator_order:
            print(f"[!] Modo desconocido: {args.force_mode}")
            sys.exit(1)
    else:
        # Reordenar según preferencia
        prefer_idx = next(
            i for i, g in enumerate(GENERATORS) if g[0] == args.prefer
        )
        generator_order = (
            GENERATORS[prefer_idx:] + GENERATORS[:prefer_idx]
        )

    # Determinar diosas objetivo
    objetivos = (
        DEITIES if args.diosa == "todas" else [args.diosa]
    )

    print(f"[*] Generando sprites con fallback automático")
    print(f"    Preferencia: {args.prefer}")
    print(f"    Diosas: {', '.join(objetivos)}")
    print()

    for diosa in objetivos:
        print(f"[{diosa.upper()}]")
        for i, (mode, script, desc) in enumerate(generator_order):
            print(f"  Intentando {mode}... ({desc})")
            if run_generator(script, diosa, timeout=600):
                print(f"  ✓ {mode} completado")
                break
        else:
            print(
                f"  [!] FALLO: Todos los generadores fallaron para {diosa}"
            )

    print("\n[OK] Generación completada")


if __name__ == "__main__":
    main()
