# KALINABIS — Interfaz Cyberpunk 2D (Planificación Completa)

## 🎨 DECISIÓN FINAL

**Estilo:** Cyberpunk Terminal + Paneles dinámicos
**Base:** Tema retro elegante original + transformación neon
**Deidades:** Colores cambian automáticamente según invocación
**Tech:** React + TypeScript + Tailwind + CSS animations

---

## 📊 PALETA DE COLORES POR DEIDAD

### BASE GLOBAL
```css
--bg-primary: #0a0908      /* Negro profundo */
--bg-secondary: #110f0d    /* Negro más claro */
--bg-tertiary: #1a1714     /* Gris oscuro */
--surface: #221f1b         /* Superficie paneles */
--text-primary: #e8e0d4    /* Beige (default) */
--text-muted: #7a7060      /* Muted marrón */
--border: #2e2a25          /* Borders sutiles */
```

### LILITH (Sombra Cibernética)
```css
--deidad-primary: #5a9bc4   /* Cyan azul (original) */
--deidad-bright: #00ffff    /* NEON CYAN */
--deidad-accent: #ff1493    /* Neon magenta */
--deidad-glow: rgba(0, 255, 255, 0.3)
--text-color: #e8e0d4
--scanline-color: rgba(0, 255, 255, 0.05)
--color-bleed: rgba(255, 20, 147, 0.1)
```

### ARTEMISA (Cazadora Plateada)
```css
--deidad-primary: #7aad6a   /* Verde (original) */
--deidad-bright: #00ff00    /* NEON GREEN */
--deidad-accent: #00ffaa    /* Neon mint */
--deidad-glow: rgba(0, 255, 0, 0.3)
--text-color: #e8e0d4
--scanline-color: rgba(0, 255, 0, 0.05)
--color-bleed: rgba(0, 255, 170, 0.1)
```

### AFRODITA (Magnetismo Violeta)
```css
--deidad-primary: #b8a0cc   /* Púrpura (original) */
--deidad-bright: #ff00ff    /* NEON MAGENTA */
--deidad-accent: #ff1493    /* Neon hot pink */
--deidad-glow: rgba(255, 0, 255, 0.3)
--text-color: #e8e0d4
--scanline-color: rgba(255, 0, 255, 0.05)
--color-bleed: rgba(255, 20, 147, 0.1)
```

### ISIS (Sabiduría Dorada)
```css
--deidad-primary: #c4824a   /* Oro (original) */
--deidad-bright: #ffff00    /* NEON YELLOW */
--deidad-accent: #ffa500    /* Neon orange */
--deidad-glow: rgba(255, 255, 0, 0.3)
--text-color: #e8e0d4
--scanline-color: rgba(255, 255, 0, 0.05)
--color-bleed: rgba(255, 165, 0, 0.1)
```

---

## 🖥️ LAYOUT PRINCIPAL (Terminal + Paneles)

```
┌──────────────────────────────────────────────────────────┐
│ KALINABIS v2.0 | [ALTAR] [GRIMORIO] [BOSQUE] [SYNC]     │ ← Header (nav)
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─ PANEL DEIDAD ────────┐  ┌─ TERMINAL ──────────────┐ │
│  │                        │  │                         │ │
│  │  ✦ LILITH PRESENTE ✦  │  │ > /tarot pregunta aquí  │ │
│  │                        │  │ /runas                  │ │
│  │  [ASCII ART]           │  │ /bosque                 │ │
│  │  Energía: ██████░░░░  │  │                         │ │
│  │  Favor:   ████████░░  │  │ Invocación exitosa      │ │
│  │  Mana:    ██████░░░░  │  │ awaiting...             │ │
│  │                        │  │ > █                     │ │
│  └────────────────────────┘  │                         │ │
│                              └─────────────────────────┘ │
│  ┌─ CHAT BOX ──────────────────────────────────────────┐ │
│  │ LILITH: "Viniste a la sombra. Bien.               │ │
│  │          Aquí no hay pretensiones..."             │ │
│  │                                                   │ │
│  │ TUTU: > Escribe tu respuesta aquí                 │ │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🎭 TRES VISTAS PRINCIPALES

### 1. ALTAR (Default)
**Propósito:** Invocar deidad + chat ritual

**Componentes:**
- Panel Deidad (izquierda): ASCII art + stats
- Terminal (derecha arriba): comandos
- Chat Box (abajo): conversación
- Status Bars: Favor, Mana, Exp

**Interacción:**
- Click panel deidad → cambiar deidad
- `/comando` en terminal
- Chat SSE streaming desde backend

### 2. GRIMORIO
**Propósito:** Journal de experiencias

**Layout:**
```
┌─ GRIMORIO ──────────────────────────┐
│ [2026-06-05 22:30] Invocación Lilith │
│ "Las sombras despiertan..."          │
│ [Tags: #lilith #sombra #oscuro]      │
│                                      │
│ [2026-06-04 18:15] Tarot lectura     │
│ Cartas: XII Hanged Man, VI Lovers    │
│ [Tags: #tarot #decisión]             │
│                                      │
│ [Scroll para más entries]            │
└──────────────────────────────────────┘
```

### 3. BOSQUE
**Propósito:** Esferas colectivas + proyectos

**Layout:**
```
┌─ BOSQUE ────────────────────────────┐
│ Muladhara (Raíz)                     │
│ ◊ Proyecto A              [12 marcas]│
│ ◊ Proyecto B              [8 marcas] │
│                                      │
│ Anahata (Corazón)                    │
│ ◊ Proyecto C              [34 marcas]│
│                                      │
│ [Scroll más chakras]                 │
└──────────────────────────────────────┘
```

---

## ⚡ EFECTOS RETRO CYBERPUNK 80S

### 1. SCANLINES (CSS)
```css
.scanlines::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: repeating-linear-gradient(
    0deg,
    var(--scanline-color) 0px,
    var(--scanline-color) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;
  z-index: 10;
}
```

### 2. NEON GLOW (Por deidad)
```css
.deidad-name {
  color: var(--deidad-bright);
  text-shadow: 0 0 10px var(--deidad-bright),
               0 0 20px var(--deidad-bright),
               0 0 40px var(--deidad-bright);
  animation: neon-flicker 0.1s infinite;
}

@keyframes neon-flicker {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
    text-shadow: 0 0 10px var(--deidad-bright),
                 0 0 20px var(--deidad-bright),
                 0 0 40px var(--deidad-bright);
  }
  20%, 24%, 55% {
    text-shadow: 0 0 5px var(--deidad-bright);
  }
}
```

### 3. COLOR BLEED (Chromatic aberration subtle)
```css
.panel-deidad {
  box-shadow: 
    -1px 0 var(--deidad-bright) 0.3,
     1px 0 var(--deidad-accent) 0.3,
    0 0 20px var(--deidad-glow);
}
```

### 4. GLITCH EFFECT (En transiciones)
```css
@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
  100% { transform: translate(0); }
}

.glitch {
  animation: glitch 0.2s;
}
```

### 5. CURSOR PERSONALIZADO
```css
#cursor {
  font-size: 16px;
  color: var(--deidad-bright);
  text-shadow: 0 0 8px var(--deidad-bright);
  animation: cursor-blink 0.8s infinite;
}

@keyframes cursor-blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
```

---

## 🔧 COMPONENTES REACT

### Estructura
```
KalinabisApp/
├── views/
│   ├── AltarView.tsx         (default)
│   ├── GrimorioView.tsx       (journal)
│   ├── BosqueView.tsx         (collective)
│   └── SyncView.tsx           (synchronicities)
├── components/
│   ├── Header.tsx             (navigation)
│   ├── PanelDeidad.tsx        (left panel)
│   ├── Terminal.tsx           (command input)
│   ├── ChatBox.tsx            (SSE streaming)
│   ├── StatusBars.tsx         (favor, mana, exp)
│   ├── Scanlines.tsx          (CSS overlay)
│   └── TerminalOutput.tsx     (log)
└── hooks/
    ├── useDeityColors.ts      (color switching)
    ├── useTerminalCommand.ts  (command parsing)
    └── useBackendAPI.ts       (fetch + SSE)
```

### Key Component: useDeityColors
```typescript
const useDeityColors = (deidad: 'lilith' | 'artemisa' | 'afrodita' | 'isis') => {
  const palettes = {
    lilith: {
      bright: '#00ffff',
      accent: '#ff1493',
      glow: 'rgba(0, 255, 255, 0.3)',
      scanline: 'rgba(0, 255, 255, 0.05)',
    },
    // ... rest
  };

  return palettes[deidad];
};
```

---

## 📱 INTERACCIÓN: Terminal + API

### Terminal Commands (Existing)
```bash
/runas [pregunta]        → Tirada de runas
/tarot [pregunta]        → Tarot lectura
/bosque                  → Ver esferas
/sync registrar          → Registrar sincronicity
/gnosis                  → Gnosis ritual
/ayuda                   → Help
```

### Terminal → Backend
```typescript
const sendCommand = async (command: string) => {
  // Parse: /comando arg1 arg2
  const [cmd, ...args] = command.slice(1).split(' ');

  const response = await fetch('http://localhost:5000/api/consultar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Project-Code': projectCode,
    },
    body: JSON.stringify({
      tipo: cmd,
      query: args.join(' '),
    }),
  });

  // Stream response to TerminalOutput
};
```

---

## 🎬 TRANSICIONES ENTRE VISTAS

**ALTAR → GRIMORIO:**
1. Glitch effect (100ms)
2. Fade out panel (200ms)
3. Fade in grimorio entries (200ms)
4. Color transition (smooth, 300ms)

```typescript
const transitionView = async (toView: ViewType) => {
  // Glitch
  document.body.classList.add('glitch');
  await sleep(100);
  document.body.classList.remove('glitch');

  // Fade
  setShowContent(false);
  await sleep(200);
  setActiveView(toView);
  setShowContent(true);
};
```

---

## 🌈 COLOR TRANSITION WHEN DEITY CHANGES

**Smooth:** CSS variables + transition

```css
:root {
  --deidad-bright: #5a9bc4;
  --deidad-accent: #00ffff;
  transition: --deidad-bright 0.3s, --deidad-accent 0.3s;
}

.when-switching {
  filter: saturate(0.5);
  animation: color-pulse 0.5s ease-out;
}

@keyframes color-pulse {
  0% { filter: saturate(0); }
  50% { filter: saturate(1.2); }
  100% { filter: saturate(1); }
}
```

---

## 📋 IMPLEMENTACIÓN ROADMAP

### Fase 1 (Semana 1): Core Layout + Terminal
- [ ] Header + Nav
- [ ] Main terminal component
- [ ] Command parsing + output display
- [ ] Scanlines + basic glow

### Fase 2 (Semana 2): Paneles + Dinámicos
- [ ] Panel Deidad (ASCII art)
- [ ] Status Bars (favor, mana, exp)
- [ ] Color switching by deidad
- [ ] Chat Box (integrate SSE)

### Fase 3 (Semana 3): Views + Polish
- [ ] GRIMORIO view
- [ ] BOSQUE view
- [ ] Transitions + glitch effects
- [ ] Hover states, cursor personalizado

### Fase 4: Backend Integration
- [ ] Connect /api/consultar
- [ ] SSE streaming chat
- [ ] Command execution
- [ ] Rate limiting + error handling

---

## 🎯 RESULTADO FINAL

**Visual:** Cyberpunk matrix elegante con colores neon dinámicos
**Interacción:** Terminal + paneles intuitivos
**Performance:** Puro React/CSS, sin 3D
**Timeline:** 3-4 semanas total
**Mobile:** Responsive (escala terminal a viewport)

**Distintivo:** No verá esto en ningún otro proyecto esotérico. Es **original, audaz, funcional.**

---

## ❓ SIGUIENTE PASO

¿Aprobado este plan?

Si sí:
1. Empiezo con Header + Terminal (Fase 1)
2. Hago componentes base (PanelDeidad, ChatBox, etc.)
3. Integro colores dinámicos por deidad
4. Conectas con backend (ya existe)

¿Cambios o ajustes al design?
