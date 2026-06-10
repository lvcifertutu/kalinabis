// ── Sprites de pixel art por diosa ──────────────────────────────────────────
// Enfoque deliberadamente simple: una imagen PNG por estado (idle/blink/speak)
// que se intercambia según el ánimo y si la diosa habla. Sin sprite sheets ni
// canvas — reusa el hook de parpadeo del retrato. Cuando NO hay sprite para una
// diosa, el retrato cae automáticamente al arte ASCII animado.
//
// Cómo activar una diosa:
//   1. Generá/pixelá su arte (ver guía) y exportá PNG transparentes.
//   2. Dejalos en `public/sprites/` (ej: lilith-idle.png).
//   3. Descomentá su entrada acá abajo. Listo — el altar usa el sprite.

import type { DeityKey } from '@/app/lib/deityMoods';

export interface DeitySprite {
  /** PNG en reposo (ojos abiertos). Requerido. */
  idle: string;
  /** PNG de parpadeo (ojos cerrados). Opcional; si falta, no parpadea. */
  blink?: string;
  /** PNG hablando. Opcional; si falta, usa `idle` mientras habla. */
  speak?: string;
  /** Ancho de render en px. Default cuadrado (SPRITE_RENDER_PX). */
  w?: number;
  /** Alto de render en px. Para cuerpo completo (vertical) usar mayor que `w`. */
  h?: number;
}

/** Tamaño de render del retrato en px (busto cuadrado por defecto). */
export const SPRITE_RENDER_PX = 200;
/** Para cuerpo completo (estilo Stardew): vertical, más alto que ancho. */
export const FULLBODY_W = 200;
export const FULLBODY_H = 280;

/**
 * Diosas con sprite. Vacío = todas usan ASCII por ahora.
 * Descomentá cada una al dropear su arte en public/sprites/.
 */
export const DEITY_SPRITES: Partial<Record<DeityKey, DeitySprite>> = {
  lilith: {
    idle: '/sprites/lilith-idle.png',
    blink: '/sprites/lilith-blink.png',
    speak: '/sprites/lilith-speak.png',
  },
  isis: {
    idle: '/sprites/isis-idle.png',
    blink: '/sprites/isis-blink.png',
    speak: '/sprites/isis-speak.png',
  },
  afrodita: {
    idle: '/sprites/afrodita-idle.png',
    blink: '/sprites/afrodita-blink.png',
    speak: '/sprites/afrodita-speak.png',
  },
  artemisa: {
    idle: '/sprites/artemisa-idle.png',
    blink: '/sprites/artemisa-blink.png',
    speak: '/sprites/artemisa-speak.png',
  },
};
