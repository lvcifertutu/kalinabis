# 🎨 Quick Start: Generar Sprites de Deidades

## ✅ Las 3 Opciones

### OPCIÓN 1: HF API PRO (RECOMENDADO si tienes token)

**Setup (una sola vez):**
```powershell
# 1. Obtén token en https://huggingface.co/settings/tokens
# 2. Configura en PowerShell:
$env:HF_TOKEN = 'hf_xxxxxxxxxxxxxxxxxxx'
```

**Generar sprites (máxima calidad):**
```bash
# Ver modelos disponibles
python tools/gen_sprite_hf_pro.py --list-models

# Generar una diosa (DREAMSHAPER = excelente calidad)
python tools/gen_sprite_hf_pro.py --diosa lilith --quality high

# Generar todas las diosas
python tools/gen_sprite_hf_pro.py --diosa todas --quality high

# Ultra quality (tarda más pero mejor resultado)
python tools/gen_sprite_hf_pro.py --diosa lilith --quality ultra

# Con otro modelo
python tools/gen_sprite_hf_pro.py --diosa lilith --model nerijs/pixel-art-xl
```

**Resultado:** `public/sprites/lilith-idle.png` (512x512 → pixelado a 96x96)

**Ventajas:**
- ✅ Mejor calidad visual
- ✅ DreamShaper = especializado
- ✅ Rápido (15-30s)
- ✅ Prompts optimizados

---

### OPCIÓN 2: Pixel Art Programático (GRATIS, sin internet)

**Generar todas las diosas:**
```bash
python tools/gen_sprite_enhanced.py --diosa todas
```

**Generar frames individuales:**
```bash
python tools/gen_sprite_enhanced.py --diosa lilith --frame idle
python tools/gen_sprite_enhanced.py --diosa lilith --frame blink
python tools/gen_sprite_enhanced.py --diosa lilith --frame speak
```

**Resultado:** `public/sprites/lilith-idle.png`, `lilith-blink.png`, `lilith-speak.png` (128x128)

**Customizar (editar colores):**
```python
# En tools/gen_sprite_enhanced.py, modifica:
DIOSAS = {
    "lilith": {
        "base": (100, 30, 150),       # RGB: púrpura
        "light": (180, 100, 220),     # Más claro
        "dark": (60, 10, 80),         # Más oscuro
        # ... etc
    }
}
```

**Ventajas:**
- ✅ 100% consistente
- ✅ Cero dependencias
- ✅ Frames inline (idle/blink/speak)
- ✅ Editable en código

---

### OPCIÓN 3: SDXL Local (si tienes GPU NVIDIA)

**Setup (primera vez):**
```bash
# Instala PyTorch con GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers safetensors

# Primera generación descarga modelo (~6GB)
python tools/gen_sprite_pixelart_xl.py --diosa lilith
# Tarda: ~3min descarga + 1min generación = 4min total
```

**Generar sprites (muy rápido luego):**
```bash
# Una diosa
python tools/gen_sprite_pixelart_xl.py --diosa lilith --frame idle

# Todas las diosas (tarda ~5min)
python tools/gen_sprite_pixelart_xl.py --diosa todas

# Todos los frames de una diosa
for $frame in idle, blink, speak {
    python tools/gen_sprite_pixelart_xl.py --diosa lilith --frame $frame
}
```

**Resultado:** `public/sprites/lilith-idle.png` (128x128)

**Ventajas:**
- ✅ Máxima calidad
- ✅ Sin límites
- ✅ Sin internet (después de descargar)
- ✅ Personalizable

**Requisitos:**
- ❌ GPU NVIDIA (RTX 2060+)
- ❌ ~6GB espacio disco
- ❌ Primera vez: 3min

---

## 🎯 ¿Cuál Elegir?

| Situación | Opción | Comando |
|-----------|--------|---------|
| Tengo token HF | **1. HF PRO** | `python tools/gen_sprite_hf_pro.py --diosa todas --quality high` |
| No tengo GPU | **1 o 2** | `python tools/gen_sprite_enhanced.py --diosa todas` |
| Tengo GPU NVIDIA | **3. SDXL** | `python tools/gen_sprite_pixelart_xl.py --diosa todas` |
| Quiero lo más rápido | **2. Programático** | `python tools/gen_sprite_enhanced.py --diosa todas` |

---

## 🔄 Flujo Recomendado: Híbrido

1. **Generar base con HF API PRO** (calidad + velocidad)
   ```bash
   python tools/gen_sprite_hf_pro.py --diosa lilith --quality high
   ```

2. **Editar en Aseprite** para refinar:
   - Ajustar colores
   - Mejorar detalles
   - Crear frames blink/speak consistentes
   - Agregar sombras/luces

3. **Guardar final:**
   - `lilith-idle.png` (sprite base)
   - `lilith-blink.png` (ojos cerrados)
   - `lilith-speak.png` (boca abierta)

---

## 🧪 Test de Conexión HF

```bash
python tools/test_hf_quality.py
```

Esto muestra:
- ✓ Si tienes token configurado
- ✓ Qué modelos están disponibles
- ✓ Prueba de generación real

---

## 📊 Comparativa de Calidad

| Aspecto | Opción 1 (HF) | Opción 2 (PIL) | Opción 3 (SDXL) |
|---------|---------------|----------------|-----------------|
| Calidad visual | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Velocidad | ⚡⚡ | ⚡⚡⚡ | ⚡ |
| Setup | Token HF | Nada | GPU + pip |
| Costo | Gratis* | Gratis | Gratis |
| Frames | Solo idle | idle/blink/speak | Solo idle |
| Editable | Prompts | Código PIL | Prompts |

*HF API: Límite gratuito ~30K calls/mes (suficiente)

---

## 🚀 Próximos Pasos

**Si usas HF PRO:**
```bash
# 1. Configura token
$env:HF_TOKEN = 'hf_xxx'

# 2. Prueba conexión
python tools/test_hf_quality.py

# 3. Genera sprites
python tools/gen_sprite_hf_pro.py --diosa todas --quality high

# 4. Edita en Aseprite para frames blink/speak
```

**Si usas Programático:**
```bash
# 1. Genera todo
python tools/gen_sprite_enhanced.py --diosa todas

# 2. Personaliza colores en gen_sprite_enhanced.py

# 3. Listo para usar en app
```

**Si usas SDXL Local:**
```bash
# 1. Instala deps
pip install torch diffusers transformers safetensors

# 2. Primera generación (descarga modelo)
python tools/gen_sprite_pixelart_xl.py --diosa lilith

# 3. Genera resto
python tools/gen_sprite_pixelart_xl.py --diosa todas
```

---

## 📝 Notas

- Todos los sprites van a: `public/sprites/`
- Para frames blink/speak en HF o SDXL, edita con Aseprite/Piskel
- Programático ya genera 3 frames automáticamente
- HF API tiene límite gratuito generoso (30K/mes)
- SDXL local requiere GPU pero sin límites

---

## 🆘 Troubleshooting

### "ImportError: No module named 'PIL'"
```bash
pip install pillow
```

### "HF_TOKEN not found"
```powershell
$env:HF_TOKEN = 'hf_xxx'
python tools/test_hf_quality.py
```

### "CUDA not available / GPU not found"
- Opción 3 requiere GPU NVIDIA
- Usa Opción 1 o 2 en su lugar

### "Model loading is taking too long"
- Espera 1-2 min, la primera vez es normal
- HF Inference API auto-carga modelos bajo demanda

