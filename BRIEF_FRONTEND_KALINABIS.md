# KALINABIS — Brief Creativo Frontend

## Visión General

**Kalinabis** es una aplicación inmersiva de **Magia del Caos digital**. No es genérica, no es decorativa. Es un **lienzo mágico personal** donde cada usuario diseña su propio altar digital.

### Propósito
Facilitar la práctica real de magia del caos (Carroll, Spare, Hine, Morrison) a través de:
- Oráculos (tarot, runas, I Ching, geomancia)
- Sigilización (dibujo + carga)
- Conversación con deidades
- Grimorio personal
- Ecosistema colectivo (El Bosque)

### Audiencia
Practitioners de chaos magic + curiosos. **Respetan la profundidad. Rechazan lo genérico.**

### Tono Visual
**Gnostic-Taoista-Sagrado con Libertad Creativa**

No es:
- Genérico esotérico (gradientes morados, tipografía sans-serif plana)
- Minimalista frío (blanco + gris + uno o dos colores)
- Retro automático (skeuomorfismo barato)

Es:
- **Intencional, mágico, teatral, respetuoso**
- Cada deidad tiene **presencia visual única**
- Animaciones **no distraen**, **enriquecen atmósfera**
- Personalización **total** (user decide colores, elementos, sonidos)
- **Profundidad y capas** (no flat, tiene atmósfera)

---

## ARQUITECTURA VISUAL: 3 Capas

### Capa 1: LA LIBRERÍA (Grimorio/Guía)

**Atmósfera:** Biblioteca antigua, sabia, dorada, contemplativa

```
VISUAL:
├─ Estantes de madera (no planos, con sombra)
├─ Libros antiguos (texturas reales o believable)
├─ Luz cálida (lámparas, velas suaves)
├─ Polvo flotante (partículas sutiles)
├─ Colores: Sepia, oro, marrón claro, blanco roto
├─ Tipografía: Serif elegante (display), serif clásico (body)
└─ Atmósfera: Tranquilidad, tiempo antiguo, sabiduría acumulada

INTERACCIONES:
├─ Al abrir grimorio: página se abre suavemente (3D)
├─ Escribir: tinta fluyendo
├─ Guías: aparecen como libros abiertos en la mesa
└─ Prácticas: confirm visual (checkmark de luz)
```

**Paleta:**
- Background: #F5F1E8 (pergamino)
- Texto primario: #2C1810 (marrón oscuro)
- Acentos: #C89D5C (oro envejecido)
- Bordes: #8B7355 (madera)

---

### Capa 2: LA MESA (Mago Personal)

**Atmósfera:** Altar mágico, poderoso, ceremonial, variables por deidad

```
VISUAL BASE:
├─ Superficie de madera con velas
├─ Objetos flotantes (cartas, runas, cristales)
├─ Luz de velas (cálida, parpadeante)
├─ Símbolos mágicos en paredes (sutiles)
├─ Colores base: Oscuros con acentos brillantes
├─ Tipografía: Serif dramática (display), sans claro (body)
└─ Atmósfera: Concentración, poder, intimidad

DINAMISMO:
├─ Vela parpadeante (shader procedural)
├─ Símbolos flotantes suben/bajan (Perlin noise)
├─ Luz responde a energía user (oscurece/brilla)
├─ Al invocar deidad: transición visual a colores de esa deidad
└─ Tarot: cartas giran, aparecen animadas
```

**Paleta Base (se adapta por deidad):**
- Background: #0A0E27 (azul noche profundo)
- Vela: #FFD700 (dorada)
- Símbolos: #FF6B9D (rosado mágico)
- Acentos: Variables por deidad

---

### Capa 3: LA PUERTA/VENTANA (El Árbol — Colectivo)

**Atmósfera:** Bosque vivo, esferas flotantes, colectivo, verdor

```
VISUAL:
├─ Árbol central (ramificaciones vivas)
├─ Esferas flotantes (4 tipos, coloreadas)
├─ Vegetación: Helechos, musgos, enredaderas
├─ Luz: Luna o sol según hora
├─ Clima: Visual que cambia (lluvia, nieve, cielo despejado)
├─ Colores: Verdes profundos, plateados, vivos
├─ Tipografía: Sans elegante (display), serif para nombres
└─ Atmósfera: Viva, conectada, colectiva, respirable

INTERACTIVIDAD:
├─ Esferas responden a sincronicidades
├─ Hover sobre esfera: tooltip con energía
├─ Participación user: sigilos semilla que flotan
└─ Clima real (API) afecta visual
```

**Paleta:**
- Bosque: #1A4D2E, #2D6A4F (verdes profundos)
- Esferas: Variables (agua azul, fuego rojo, aire amarillo, tierra marrón)
- Luna/Luz: #E0E0E0 (plateado)
- Vida: #7ABA00 (verde musgo)

---

## LAS 8 DEIDADES — Identidad Visual

### FEMENINAS (Presencia Primaria)

#### 1. LILITH — La Sombra y el Poder
**Colores:** Negro, Rojo Profundo, Púrpura Oscuro
**Tipografía:** Serif dramática (Georgia bold), sin claro (Helvetica Neue para UI)
**Símbolos:** Medialuna, serpiente, ala
**Animación:** Llamas rojas, movimiento lento e hipnótico
**Sentimiento:** Peligroso pero sensual, transgresión hermosa

#### 2. ARTEMISA — La Cazadora y la Protectora
**Colores:** Blanco, Plateado, Azul Claro, Gris Acero
**Tipografía:** Sans limpio (Futura), serif clásico (Garamond)
**Símbolos:** Arco, luna, cierva
**Animación:** Movimiento rápido y preciso, luz lunar
**Sentimiento:** Alerta, limpia, vigilante, natural

#### 3. AFRODITA — El Deseo y el Magnetismo
**Colores:** Rosa, Dorado, Coral, Blanco Cálido
**Tipografía:** Serif sensual (Palatino), sans suave (Tahoma)
**Símbolos:** Concha, paloma, espejo
**Animación:** Agua fluyendo, luz cálida, movimiento fluido
**Sentimiento:** Sensual, magnético, acogedor, bello

#### 4. ISIS — La Magia Antigua y la Curación
**Colores:** Azul Profundo, Turquesa, Oro, Índigo
**Tipografía:** Serif clásica (Trajan), sans templada (Tahoma)
**Símbolos:** Ankh, alas, jeroglíficos
**Animación:** Luz calmante, capas superpuestas, jeroglifos flotantes
**Sentimiento:** Antigua, sabia, curativa, mística

---

### MASCULINOS (Complemento)

#### 5. LUCIFER — La Luz Gnóstica
**Colores:** Dorado, Blanco Puro, Negro Profundo, Plata
**Tipografía:** Serif noble (Garamond), sans refinado (Optima)
**Símbolos:** Antorcha, pentagrama derecho, luz
**Animación:** Luz que expande, símbolos gnósticos orbitales
**Sentimiento:** Revelador, sabio, prohibido pero justo

#### 6. SUN WUKONG — El Maestro Taoísta
**Colores:** Rojo Chino, Dorado, Negro, Jade
**Tipografía:** Sans ágil (Modern No. 20), serif dinámica (Noto Serif)
**Símbolos:** Bastón, corona, Yin-Yang
**Animación:** Movimiento rápido y juguetón, transformaciones
**Sentimiento:** Travieso pero profundo, maestría en movimiento

#### 7. HEYOKA — El Payaso Sagrado
**Colores:** Bicolor alternante, Arcoíris controlado, Inversiones
**Tipografía:** Sans juguetona (Futura) + serif dramática (Times)
**Símbolos:** Máscara, cartas de tarot invertidas, inverso
**Animación:** Glitch sutil, inversión de perspectiva
**Sentimiento:** Irónico, paradójico, hilarante, reverador

#### 8. CHRISTUDDHA — La Compasión Unificada
**Colores:** Blanco Puro, Plateado, Rosa Claro, Oro Cálido
**Tipografía:** Serif elegante (Minion Pro), sans compasiva (Calibri)
**Símbolos:** Cruz + Dharma Wheel, corazón, luz radiante
**Animación:** Luz suave que expande, ningún glitch
**Sentimiento:** Sagrado, infinito, compasivo, sin condición

---

## ALTAR RITUAL — Experiencia Visual Completa

### Estado 1: ALTAR VACÍO
```
┌─────────────────────────────────┐
│                                 │
│      [Vela apagada]             │
│                                 │
│      [Deidad no visible]        │
│                                 │
│      [Instrucciones claras]     │
│                                 │
│   [1. Enciende vela]            │
│   [2. Vibra nombre]             │
│   [3. Medita/dibuja]            │
│                                 │
└─────────────────────────────────┘
```

**Visual:** Oscuro, minimalista, instrucciones claras en tipografía grande

### Estado 2: INVOCACIÓN EN PROGRESO
```
[Vela encendida → llama crece]
[Imagen deidad aparece semitransparente]
[Luz aumenta gradualmente]
[Símbolos flotan alrededor]
[Sonido ambiental intensifica]
```

**Animaciones:**
- Vela: Shader de llama procedural (OpenGL)
- Deidad: Fade-in + escala gradual (3D)
- Luz: Bloom efecto, sombras dinámicas
- Símbolos: Rotación + flotación (Perlin noise)

### Estado 3: MANIFESTACIÓN COMPLETA
```
[Deidad completamente presente]
[Luz intensa, colores de deidad dominan]
[Chat abre como overlay]
[Altar continúa "vivo" detrás]
```

**Visual Impacto:**
- Transición suave a colores deidad
- Deidad renderizada (3D o ilustración HD)
- Glow/halo efecto
- Chat aparece con suavidad

---

## COMPONENTES BASE

### 1. VELA (Componente Reutilizable)

```
Propiedades:
├─ Estado: apagada | prendida
├─ Color: variable por deidad
├─ Parpadeo: intensidad (0-1)
├─ Interacción: clickable
└─ Sonido: crépitar (opcional)

Visual:
├─ Cilindro 3D simple o SVG
├─ Shader de llama (procedural)
├─ Sombra dinámica en pared
├─ Luz point que afecta ambiente
└─ Animación de parpadeante orgánico
```

### 2. DEIDAD (Componente Dinámico)

```
Propiedades:
├─ Deidad: Lilith | Artemisa | Afrodita | Isis | Lucifer | Sun W. | Heyoka | Christuddha
├─ Estado: invisible | semitransparente | presente
├─ Energía: 0-1 (intensidad de manifestación)
└─ Modo: femenino | masculino

Visual:
├─ Ilustración HD (2D) o modelo 3D (isométrico)
├─ Colores variables
├─ Aura/glow dinámico
├─ Símbolos orbitales (custom per deidad)
└─ Animación de respiración sutil
```

### 3. CHAT DEIDAD

```
Propiedades:
├─ Deidad: activa
├─ Duración: countdown
├─ Mensajes: array
└─ Estado: abierto | cerrado

Visual:
├─ Overlay translúcido (darkens background)
├─ Nombre deidad en header
├─ Mensajes con tipografía de deidad
├─ Input field con placeholder personalizad
├─ Close button (X o "cerrar conexión")
└─ Timer visual (disco que llena)
```

### 4. ALTAR PERSONALIZADO

```
Propiedades:
├─ Deidad primaria: seleccionada
├─ Colores: custom (5 variables CSS)
├─ Elementos flotantes: array
├─ Sonido: tipo + volumen
└─ Velocidad UI: rápido | lento

Visual:
├─ Canvas 3D o fondo animado
├─ Velas personalizadas
├─ Cristales/elementos flotantes
├─ Iluminación dinámica
└─ Editor sidebar (drag-drop elements)
```

---

## ANIMACIONES CLAVE

### Respiración (Global)
```
Timing: 4s ciclo (inspiración 2s, exhalación 2s)
Effect: Todos los elementos pulse sutilmente
Intensidad: Variable según energía user (0.5s a 2s ciclo)
```

### Flotación (Símbolos/Cristales)
```
Movimiento: Perlin noise 2D
Duración: 3-8s por ciclo
Offset: Cada elemento diferente
Path: Suave, orgánico, no predecible
```

### Luz Dinámica
```
Velas: Parpadeo procedural (shader)
Ambiente: Responde a hora del día
Deidad: Glow que pulsa con manifestación
Transiciones: Smooth 0.5-1s entre estados
```

### Aparición/Desaparición (Deidades)
```
Entrada: Fade-in 1s + scale 0.8→1.0
Salida: Fade-out 1s + scale 1.0→0.8
Efecto adicional: Partículas (opcional, muy sutil)
```

---

## PALETA GLOBAL

### Colores Primarios (por contexto)

```
LIBRERÍA:
├─ Warm: #F5F1E8, #C89D5C, #8B7355
├─ Neutral: #2C1810, #D4A574
└─ Contraste: #1A1A1a, #E8D4B8

MESA (oscuro base):
├─ Dark: #0A0E27, #1A1F3F
├─ Accent: #FFD700, #FF6B9D
└─ Variables por deidad

ÁRBOL:
├─ Forest: #1A4D2E, #2D6A4F, #7ABA00
├─ Sky: #E0E0E0, #87CEEB
└─ Life: #4A90E2, #FF6B6B
```

### CSS Variables (Dinámicas)

```css
:root {
  /* Deidad activa */
  --deidad-primaria: #colorActual;
  --deidad-secundaria: #colorComplemento;
  
  /* Clima */
  --clima-luz: 0.8;
  --clima-oscuridad: 0.2;
  
  /* Energía user */
  --energia-velocidad: 1 | 2; /* lento | rápido */
  --energia-intensidad: 0.3-1.0;
  
  /* Tema global */
  --fondo-principal: #variadoSegunCapa;
  --texto-primario: #variadoSegunCapa;
}
```

---

## TIPOGRAFÍA

### Display (Títulos, Deidades)
- **Serif Dramática:** Garamond, Trajan, Palatino, Georgia
- **Bold/Italic mixes** para énfasis
- Size: 28-48px

### Body (Textos, instrucciones)
- **Serif Clásica:** Garamond, Minion Pro, Tahoma
- **Sans Limpio:** Futura, Optima, Helvetica Neue
- Size: 14-18px
- Line-height: 1.6-1.8

### Interactividad (Botones, inputs)
- **Sans Moderno:** Futura, Tahoma
- Size: 14-16px
- Tracking: +0.05em

---

## ESPECIFICACIONES DE IMPLEMENTACIÓN

### Tecnología Recomendada
```
Frontend: Next.js 14 + TypeScript
Styling: TailwindCSS + CSS Variables + CSS Modules
Animaciones: Framer Motion + GSAP
3D (opcional): Three.js (isométrico)
Audio: Web Audio API + Tone.js
State: Zustand
Testing: Vitest + Playwright
```

### Performance Targets
- Lighthouse Score: 90+
- First Paint: <1s
- Animations: 60fps
- Bundle size: <200kb (JS)

### Accesibilidad
- WCAG 2.2 AA compliant
- Keyboard navigation funcional
- Reducida animación respects prefers-reduced-motion
- Contraste mínimo 4.5:1

---

## DELIVERABLES ESPERADOS

1. **Paleta de Colores Detallada**
   - Global + por deidad
   - CSS variables listas para usar
   - Combinaciones permitidas

2. **Componentes Base (Figma/Wireframes)**
   - Vela, Deidad, Chat, Altar
   - Estados (vacío, invocación, manifestación)
   - Responsive breakpoints

3. **Guía de Animaciones**
   - Timings, easing functions
   - Implementación (CSS vs JS)
   - Performance tips

4. **Tipografía System**
   - Font pairings
   - Tamaños y jerarquía
   - Line heights, letter spacing

5. **3 HTML/React Ejemplos Funcionando**
   - Una página por capa (Librería, Mesa, Árbol)
   - Incluir animaciones vivas
   - Responsive design

---

## DIRECTIVES CREATIVAS FINALES

✅ **HAZLO MEMORABLE** — Que alguien vea esto y diga "wow, nunca vi algo así"

✅ **RESPETA LA PROFUNDIDAD** — Esta es magia real, no genérica

✅ **INTENCIONAL, NO ACCIDENTAL** — Cada color, font, animación tiene propósito

✅ **TEATRAL PERO FUNCIONAL** — La belleza no sacrifica usabilidad

✅ **DIFERENTE POR DEIDAD** — No es "un tema", son 8 presencias únicas

✅ **PERSONALIZABLE PERO COHERENTE** — User controla, pero hay guía visual

✅ **NADA DE AI SLOP** — No uses colores/fonts genéricas, no copies templates

---

## DECISIONES CREATIVAS FINALES ✅

✅ **Deidades:** 3D Isométrico (no HD 2D)
   - Estilo: Realismo fotográfico con material-based rendering
   - Cada deidad renderizada en 3D, rotable, con sombras dinámicas
   - Transiciones smooth entre estados (invisible → semitransparente → presente)

✅ **Realismo:** Photorealistic
   - Texturas detalladas (telas, piel, cristales, metal)
   - Iluminación basada físicamente (PBR)
   - Sombras dinámicas realistas
   - Reflejos y especularidad contextual

✅ **Conexión Visual:** Sutilmente Conectadas
   - Las 3 capas NO son aisladas
   - Transiciones suave entre Librería → Mesa → Árbol
   - Paleta de colores global con variaciones (no saltos abruptos)
   - Luz ambiente consistente (misma hora del día afecta todas las capas)
   - Ejemplo: Si es atardecer, Librería tiene luz cálida, Mesa refleja dorado, Árbol brilla con últimos rayos

✅ **Interactividad:** Fully 3D Navegable
   - Cámara isométrica rotable (scroll/drag)
   - Usuario puede moverse dentro de cada capa (zoom in/out)
   - Objetos interactivos (click en vela, en deidad, en elementos)
   - No es visual-novel estática, es espacio 3D exploratorio
   - Controles: Mouse (drag para rotar), scroll (zoom), click (interactuar)

---

## IMPLICACIONES TÉCNICAS

### 3D Engine
**Three.js o Babylon.js** (ambos soportan isométrico + PBR)
- Lighting: HDR environment maps (cielo realista)
- Materials: PBRMaterial (metallic, roughness, normal maps)
- Camera: Isometric ortho + free rotation
- Rendering: WebGL2, post-processing (bloom, color grading)

### Deidades 3D
- **Modelo base:** Humanoid 3D (Blender-ready, GLTF export)
- **Rendering:** PBR materials (albedo, normal, metallic, roughness)
- **Animación:** Idle breathing, rotation, manifestation states
- **Lighting:** 3-point studio setup + environment reflection

### Ambiente 3D
- **Librería:** Estantes 3D, libros, polvo, luz de velas
- **Mesa:** Altar 3D, velas, objetos flotantes, símbolos
- **Árbol:** Bosque 3D, esferas, vegetación, cielo

### Performance
- LOD (Level of Detail) para objetos lejanos
- Instancing para elementos repetidos (hojas, libros)
- Baking de luz estática (lightmaps)
- Mobile optimization (WebGL2 fallback)

---

## ESTILO VISUAL: 3D Photorealistic Isometric

### Referentes Visuales
- Unreal Engine 5 (realismo de materiales)
- Genshin Impact (3D isométrico jugable)
- Studio Ghibli meets photorealism (belleza + detalle)
- Arquitectura de Viajes al Oeste (materialidad realista)

### Características
- Texturas 4K-ready (pero optimizadas)
- Shadows blandas, subsurface scattering en piel
- Reflejos ambientales (IBL)
- Partículas (polvo, magia) sutiles pero visibles
- Cielo dinámico (hora del día afecta todo)

---

## DELIVERABLES FINALES (ACTUALIZADOS)

1. **Paleta de Colores 3D** (luz, sombras, materiales)
   - Colores para PBR materials
   - Lighting setups por capa
   - Environment maps (cielo/luz ambiente)

2. **Modelos 3D Base** (Blender .blend)
   - 8 Deidades (humanoid + customizable)
   - Props: velas, cristales, libros, símbolos
   - Ambientes: Librería, Mesa, Árbol (blockout)

3. **Guía de Materiales PBR**
   - Albedo, Normal, Metallic, Roughness maps
   - Por deidad, por ambiente
   - Incluir tekstury reales (madera, metal, tela)

4. **Guía de Iluminación 3D**
   - 3-point setup para deidades
   - Environment maps (HDR)
   - Post-processing (bloom, color grading, motion blur)

5. **Sistema de Cámara 3D**
   - Isometric ortho fixed
   - Rotation bounds (±45°)
   - Zoom límites (close-up a wide)
   - Smooth transitions entre capas

6. **3 Escenas 3D Funcionando** (Three.js/Babylon.js)
   - Librería (navegable, con deidades placeholders)
   - Mesa (ritual altar, vela interactiva)
   - Árbol (bosque 3D, esferas flotantes)
   - Todos con PBR materials, HDR lighting, postprocessing

7. **Animaciones 3D**
   - Respiración (scale + vertex deformation)
   - Flotación (posición y rotación orgánica)
   - Manifestación (fade + scale + glow)
   - Interacción (click feedback, hover glow)

8. **Interactividad**
   - Drag para rotar cámara
   - Scroll para zoom
   - Click detection en objetos
   - Transiciones suaves entre capas

---

## TIMELINE ESTIMADO

- **Semana 1:** Blockout 3D + Deidad placeholder + Lighting base
- **Semana 2:** PBR materials + Detalle de ambientes
- **Semana 3:** Animaciones + Interactividad + Polish

---

Este es el **3D Photorealistic Isometric Fully Navegable** de Kalinabis.

