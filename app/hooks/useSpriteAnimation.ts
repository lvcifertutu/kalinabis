import { useEffect, useState } from 'react';
import type { Mood } from '@/app/lib/deityMoods';

/**
 * Hook para controlar animaciones de sprites con ciclos naturales.
 * Maneja: parpadeo automático, cambios de expresión por ánimo, y habla.
 */
export function useSpriteAnimation(mood: Mood, isSpeaking = false) {
  const [frame, setFrame] = useState<'idle' | 'blink' | 'speak'>('idle');
  const [isBlinking, setIsBlinking] = useState(false);

  // Ventanas de tiempo entre parpadeos según ánimo
  const blinkWindow: Record<Mood, [number, number]> = {
    amplificada: [2000, 4000],   // Parpadea más frecuentemente
    neutral: [4000, 7000],        // Normal
    reposo: [6000, 10000],        // Menos frecuentemente
  };

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Respetar prefers-reduced-motion
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mediaQuery.matches) {
      setFrame(isSpeaking ? 'speak' : 'idle');
      return;
    }

    // Determinar frame actual
    if (isSpeaking) {
      setFrame('speak');
      return;
    }

    if (isBlinking) {
      setFrame('blink');
      return;
    }

    setFrame('idle');
  }, [isSpeaking, isBlinking]);

  // Ciclo de parpadeo
  useEffect(() => {
    if (typeof window === 'undefined' || isSpeaking) return;

    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mediaQuery.matches) return;

    let openTimer: ReturnType<typeof setTimeout>;
    let closeTimer: ReturnType<typeof setTimeout>;
    let isMounted = true;

    const [minWait, maxWait] = blinkWindow[mood];

    const startBlink = () => {
      const waitTime = minWait + Math.random() * (maxWait - minWait);
      openTimer = setTimeout(() => {
        if (!isMounted) return;
        setIsBlinking(true);

        // Parpadeo dura ~150ms
        closeTimer = setTimeout(() => {
          if (!isMounted) return;
          setIsBlinking(false);
          // Reiniciar ciclo
          startBlink();
        }, 150);
      }, waitTime);
    };

    startBlink();

    return () => {
      isMounted = false;
      clearTimeout(openTimer);
      clearTimeout(closeTimer);
    };
  }, [mood, blinkWindow, isSpeaking]);

  return frame;
}
