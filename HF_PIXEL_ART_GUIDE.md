# 🎨 Guía: Mejora de Calidad de Pixel Art con Hugging Face

## 📊 Estado Actual

```
Sin token HF → Solo puedes usar:
  ✓ gen_sprite_enhanced.py (dibujo PIL, 128x128, consistente)
  ✓ gen_sprite_pixelart_xl.py (SDXL local si tienes GPU)
  ✗ gen_sprite_hf.py (requiere token)
```

---

## 🚀 OPCIÓN 1: Configurar Token HF (RECOMENDADO)

**Paso 1:** Crea token en Hugging Face
- Ve a: https://huggingface.co/settings/tokens
- Click "New token"
- Rol: **read**
- Copia el token (empieza con `hf_`)

**Paso 2:** Configura en PowerShell (este proyecto)
```powershell
$env:HF_TOKEN = 'hf_xxxxxxxxxxxxxxxxxxx'
```

**Paso 3:** Prueba la conexión
```bash
python tools/test_hf_quality.py
```

**Paso 4:** Usa el generador con mejor modelo
```bash
# Opción A: DreamShaper (SDXL, excelente)
python tools/gen_sprite_hf.py --diosa lilith --model artificialguintelligence/DreamShaper

# Opción B: Pixel Art XL (LoRA especializado)
python tools/gen_sprite_hf.py --diosa lilith --model nerijs/pixel-art-xl

# Opción C: Pixel Art Style (básico pero rápido)
python tools/gen_sprite_hf.py --diosa lilith --model kohbanye/pixel-art-style
```

### Ventajas:
- ✅ Modelos entrenados especializados
- ✅ Rápido (5-30s por imagen)
- ✅ Calidad consistente
- ✅ Sin dependencias locales

### Desventajas:
- ❌ Requiere cuenta/token
- ❌ Límite gratuito (~30,000 llamadas/mes)
- ❌ Requiere internet

---

## 🎨 OPCIÓN 2: Pixel Art Programático (SIN IA, GRATIS)

**Usa:** `gen_sprite_enhanced.py`

```bash
# Generar sprites de todas las diosas
python tools/gen_sprite_enhanced.py --diosa todas

# Generar frames específicos
python tools/gen_sprite_enhanced.py --diosa lilith --frame idle
python tools/gen_sprite_enhanced.py --diosa lilith --frame blink
python tools/gen_sprite_enhanced.py --diosa lilith --frame speak
```

### Ventajas:
- ✅ 100% consistente (mismo código = mismo sprite)
- ✅ Editable fácilmente (modificas colores en el código)
- ✅ Sin internet, sin costo
- ✅ Reproducible

### Desventajas:
- ❌ Requiere dibujar en Python
- ❌ Menos detalle artístico
- ❌ Requiere ajustes manuales

### Customize:
Abre `tools/gen_sprite_enhanced.py` y modifica:
```python
DIOSAS = {
    "lilith": {
        "base": (100, 30, 150),       # Color púrpura
        "light": (180, 100, 220),     # Más claro
        "dark": (60, 10, 80),         # Más oscuro
        # ... etc
    }
}
```

---

## 🖥️ OPCIÓN 3: SDXL Local (Si tienes GPU)

**Usa:** `gen_sprite_pixelart_xl.py`

**Requisitos:**
```bash
# Instala PyTorch + Diffusers
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers safetensors
```

**Primera vez:** Descarga el modelo (~6GB, solo una vez)
```bash
python tools/gen_sprite_pixelart_xl.py --diosa lilith
# Tarda: ~3min descarga + ~1min generación = 4min total
```

**Siguientes veces:** Más rápido (~1min por imagen)

### Ventajas:
- ✅ Máxima calidad visual
- ✅ Sin límites de uso
- ✅ Sin internet necesario (después de descargar)
- ✅ Personalizable (ajustar prompts)

### Desventajas:
- ❌ Requiere GPU (NVIDIA RTX 2060+)
- ❌ ~6GB espacio en disco
- ❌ Primera ejecución lenta

---

## 📊 COMPARATIVA RÁPIDA

| Aspecto | HF API | Programático | Local SDXL |
|---------|--------|--------------|-----------|
| **Calidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidad** | ⚡⚡ (5-30s) | ⚡⚡⚡ (instant) | ⚡ (30-60s) |
| **Costo** | Gratis* | Gratis | Gratis |
| **Setup** | Token HF | Nada | pip + GPU |
| **Consistencia** | Variable | 100% | 100% |
| **Customizable** | Prompts | Código PIL | Prompts |

*HF API tiene límite gratuito mensual

---

## 🎯 RECOMENDACIÓN: FLUJO HÍBRIDO

Para máxima calidad + consistencia:

```
1. Generar con HF API + DreamShaper (buena calidad inicial)
   python tools/gen_sprite_hf.py --diosa lilith --model artificialguintelligence/DreamShaper

2. Editar en Aseprite/Piskel para:
   - Ajustar colores
   - Mejorar detalles
   - Crear frames blink/speak consistentes

3. Guardar como: lilith-idle.png, lilith-blink.png, lilith-speak.png
```

---

## 🔧 PRÓXIMOS PASOS

### Si quieres HF API (recomendado):
1. Crea token en https://huggingface.co/settings/tokens
2. Configura en PowerShell: `$env:HF_TOKEN = 'hf_xxx'`
3. Prueba: `python tools/test_hf_quality.py`
4. Genera: `python tools/gen_sprite_hf.py --diosa todas`

### Si prefieres local:
1. Instala PyTorch con GPU support
2. Ejecuta: `python tools/gen_sprite_pixelart_xl.py --diosa lilith`
3. Personaliza prompts en el archivo

### Si quieres lo más simple:
1. Ejecuta: `python tools/gen_sprite_enhanced.py --diosa todas`
2. Modifica colores en el código según necesites

---

## ⚠️ NOTAS

- **HF API**: Límite gratuito es generoso (~30K calls/mes)
- **SDXL Local**: Requiere NVIDIA GPU; CPU es demasiado lento
- **Programático**: Perfecto para prototipado y consistency
- **Hybrid**: Lo mejor es generar + editar manualmente en Aseprite

---

## 📚 RECURSOS

- **Hugging Face Inference API:** https://huggingface.co/docs/api-inference
- **DreamShaper Model:** https://huggingface.co/artificialguintelligence/DreamShaper
- **Pixel Art XL LoRA:** https://huggingface.co/nerijs/pixel-art-xl
- **Aseprite** (editor pixel art): https://www.aseprite.org/
- **Piskel** (web-based, gratis): https://www.piskelapp.com/

