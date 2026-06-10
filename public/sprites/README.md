# Sprites de pixel art de las diosas

Dejá acá los PNG de cada diosa y activalos en `app/lib/deitySprites.ts`.

## Archivos esperados (por diosa)

| Estado | Archivo                | Requerido | Qué es                          |
|--------|------------------------|-----------|----------------------------------|
| idle   | `<diosa>-idle.png`     | sí        | reposo, ojos abiertos            |
| blink  | `<diosa>-blink.png`    | opcional  | ojos cerrados (parpadeo)         |
| speak  | `<diosa>-speak.png`    | opcional  | hablando (boca/gesto activo)     |

Diosas: `lilith`, `artemisa`, `afrodita`, `isis`.
Ej: `lilith-idle.png`, `lilith-blink.png`, `lilith-speak.png`.

## Specs

- **Lienzo**: cuadrado, 64×64 o 96×96 px (el motor lo escala nítido a 132 px).
- **Fondo**: transparente (PNG con alpha).
- **Mismo encuadre** en idle/blink/speak (solo cambian ojos/boca) para que no salte.
- **Paleta**: pocos colores; el color base de cada diosa ayuda al glow neón:
  - lilith `#00ffff` · artemisa `#00ff00` · afrodita `#ff00ff` · isis `#ffff00`
- El altar ya aplica brillo/saturación/glow según el ánimo; el arte puede ser
  relativamente plano y el motor lo tiñe.

## Activar

En `app/lib/deitySprites.ts`, descomentá la entrada de la diosa:

```ts
lilith: {
  idle: '/sprites/lilith-idle.png',
  blink: '/sprites/lilith-blink.png',
  speak: '/sprites/lilith-speak.png',
},
```

Si una diosa no tiene entrada, su retrato usa el arte ASCII animado (fallback).
