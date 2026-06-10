'use client';

import React, { useEffect, useState } from 'react';
import { DEITIES, deityAscii, moodVisual, type DeityKey, type Mood } from '@/app/lib/deityMoods';
import { DEITY_SPRITES, SPRITE_RENDER_PX } from '@/app/lib/deitySprites';

// Duración de un parpadeo (frame alterno visible), en ms.
const BLINK_MS = 170;
// Ventana "ojos abiertos" entre parpadeos (mín/máx) por ánimo. Pausado y natural.
const OPEN_WINDOW: Record<Mood, [number, number]> = {
  amplificada: [3400, 6000],
  neutral: [5000, 8500],
  reposo: [8000, 13000],
};

/**
 * Da vida al retrato: alterna al frame momentáneo (parpadeo/pulso) en intervalos
 * naturales y aleatorios. Respeta prefers-reduced-motion.
 */
function useBlink(mood: Mood): boolean {
  const [blinking, setBlinking] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mq.matches) return;

    let abrir: ReturnType<typeof setTimeout>;
    let cerrar: ReturnType<typeof setTimeout>;
    let cancelado = false;
    const [min, max] = OPEN_WINDOW[mood];

    const ciclo = () => {
      const espera = min + Math.random() * (max - min);
      abrir = setTimeout(() => {
        if (cancelado) return;
        setBlinking(true);
        cerrar = setTimeout(() => {
          if (cancelado) return;
          setBlinking(false);
          ciclo();
        }, BLINK_MS);
      }, espera);
    };

    ciclo();
    return () => {
      cancelado = true;
      clearTimeout(abrir);
      clearTimeout(cerrar);
    };
  }, [mood]);

  return blinking;
}

interface DeitySpriteProps {
  deity: DeityKey;
  mood: Mood;
  isSpeaking?: boolean;
}

/**
 * El retrato de la diosa. Si hay sprite de pixel art definido en DEITY_SPRITES,
 * lo usa (intercambiando idle/blink/speak); si no, cae al arte ASCII animado.
 * Ambos caminos reciben el mismo tratamiento de ánimo (brillo, saturación, glow).
 */
export function DeitySprite({ deity, mood, isSpeaking }: DeitySpriteProps) {
  const theme = DEITIES[deity];
  const visual = moodVisual(mood);
  const blinking = useBlink(mood);
  const sprite = DEITY_SPRITES[deity];

  const filter = `brightness(${visual.brightness}) saturate(${visual.saturate}) drop-shadow(0 0 ${visual.glowPx}px ${theme.color})`;

  // ── Camino sprite (pixel art) ──────────────────────────────────────────
  if (sprite) {
    const src =
      isSpeaking && sprite.speak
        ? sprite.speak
        : blinking && sprite.blink
          ? sprite.blink
          : sprite.idle;

    return (
      <img
        src={src}
        alt={theme.name}
        width={sprite.w ?? SPRITE_RENDER_PX}
        height={sprite.h ?? SPRITE_RENDER_PX}
        className="relative select-none"
        style={{
          imageRendering: 'pixelated',
          filter,
          animation: visual.animation,
          zIndex: 10,
        }}
      />
    );
  }

  // ── Camino ASCII (fallback) ────────────────────────────────────────────
  return (
    <pre
      className="relative text-xs whitespace-pre leading-tight"
      style={{
        color: theme.color,
        filter,
        animation: visual.animation,
        zIndex: 10,
      }}
    >
      {deityAscii(deity, mood, blinking)}
    </pre>
  );
}
