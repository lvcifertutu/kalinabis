# Guía de Prompts para Sprites Pixel Art

## Cambios Realizados

Los prompts ahora incluyen:
- **Detalles visuales específicos**: ropa, accesorios, expresión, postura
- **Calificadores de estilo**: "16-bit style", "detailed pixel art", "high quality"
- **Contexto emocional**: "intense", "serene", "grounded", "ethereal"
- **Composición**: "centered", "full body visible", "isolated character"
- **Lighting**: especificado por diosa para crear atmósfera
- **Trending keywords**: "trending on artstation" para mejor calidad

## Cómo Ajustar Parámetros

### num_inference_steps
```python
# En gen_sprite_hf.py, línea ~115
"num_inference_steps": 50,  # aumentá para más detalle
```
- **30-50**: Rápido, buenos resultados básicos
- **50-75**: Balance calidad/velocidad (recomendado)
- **75+**: Muy detallado pero tarda más

### guidance_scale
```python
"guidance_scale": 7.5,  # cuán fuerte seguir el prompt
```
- **5-6**: Más creatividad del modelo, menos fidelidad al prompt
- **7-8**: Balance (recomendado)
- **9-10**: Sigue el prompt al pie, menos variación

## Técnicas de Prompt Engineering

### 1. Estructura Ganadora
```
[estilo] + [personaje] + [detalles físicos] + [ropa/accesorios] + 
[expresión/pose] + [contexto visual] + [calidad] + [composición]
```

### 2. Palabras Clave que Funcionan
- Para mejor detalle: "detailed", "intricate", "ornate", "elaborate"
- Para pixel art: "16-bit", "8-bit", "retro game", "sprite sheet"
- Para calidad: "high quality", "trending on artstation", "masterpiece"
- Para atmósfera: "dramatic lighting", "ethereal glow", "warm ambient"

### 3. Qué Evitar
- Números específicos (ej: "7 años") → ambigüedad
- Descripciones contradictorias
- Demasiados detalles (confunde al modelo)
- Colores muy raros sin referencia (ej: "xanthic purple")

## Cómo Iterar

1. **Cambia los prompts en `PROMPTS = {...}`**
2. **Genera un sprite**: `python gen_sprite_hf.py --diosa lilith`
3. **Inspecciona en `public/sprites/lilith-idle.png`**
4. **Si necesita mejora**:
   - Ajusta prompt + parámetros
   - Re-genera
   - Repite hasta satisfecho

## Alternativas de Modelos

Si `kohbanye/pixel-art-style` no da buenos resultados:

```bash
# Modelo más versátil, mejor calidad general
python gen_sprite_hf.py --diosa lilith --model stabilityai/stable-diffusion-xl-base-1.0

# Buen balance creatividad/control
python gen_sprite_hf.py --diosa lilith --model artificialguintelligence/DreamShaper
```

## Ejemplo: Mejorar Lilith

**Prompt actual:**
```
pixelartstyle, 16-bit style character sprite, Lilith Nordic storm goddess,
long wavy windswept midnight black hair with teal highlights, pale gothic skin,
intense piercing violet eyes, dominant expression, flowing deep teal velvet cloak...
```

**Ajustes posibles:**
- Agregar "masterpiece quality"
- Cambiar "teal highlights" a "electric teal streaks" (más específico)
- Agregar detalles de joyería: "ornate silver runes on cloak"
- Mejorar pose: "dynamic confident stance, one hand on weapon"

## Notas

- Los prompts mejorados tardan más en generar (50+ pasos)
- Si la conexión a HF falla, usa `gen_sprite_local.py` para placeholders
- Guardar versiones buenas: renombra .png si te gusta
- Pixelar en Piskel después para consistencia (blink/speak frames)
