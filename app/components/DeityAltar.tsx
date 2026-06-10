'use client';

import React from 'react';
import { DEITIES, moodVisual, type DeityKey, type Mood } from '@/app/lib/deityMoods';
import type { LunaState } from '@/app/hooks/useLunaState';
import { DeitySprite } from './DeitySprite';

interface DeityAltarProps {
  deity: DeityKey;
  mood: Mood;
  astral: LunaState;
  /** Lo que la diosa dice en su propio espacio. Vacío = aún no habló. */
  speech?: string;
  /** True mientras se espera la respuesta (muestra indicador en el altar). */
  isSpeaking?: boolean;
}

// "Hum" visual: intensidad del aura según el ánimo. El aura late (breathe) y
// vibra finamente (hum). Cuando la diosa habla, el aura se acelera y crece.
function auraConfig(mood: Mood, isSpeaking: boolean) {
  const base = {
    amplificada: { breathe: 'aura-amplified 3.2s', hum: 'aura-hum 1.6s', size: 190 },
    neutral: { breathe: 'aura-breathe 5.5s', hum: 'aura-hum 2.6s', size: 165 },
    reposo: { breathe: 'aura-breathe 8s', hum: '', size: 140 },
  }[mood];

  const breatheAnim = `${base.breathe} ease-in-out infinite`;
  const humAnim = base.hum ? `${base.hum} steps(2) infinite` : 'none';
  // Al hablar, el aura se intensifica.
  const size = isSpeaking ? base.size + 30 : base.size;
  return { breatheAnim, humAnim, size };
}

/**
 * Altar de la deidad: el retrato (sprite de pixel art o ASCII animado) sobre un
 * aura que respira según el ánimo, más la lectura del cielo que lo provoca y el
 * texto que la diosa pronuncia en su propio espacio.
 * Presentacional puro — el ánimo, el estado astral y el habla llegan por props.
 */
export function DeityAltar({ deity, mood, astral, speech, isSpeaking }: DeityAltarProps) {
  const theme = DEITIES[deity];
  const visual = moodVisual(mood);
  const aura = auraConfig(mood, Boolean(isSpeaking));

  return (
    <div className="flex flex-col items-center text-center">
      {/* Aura superior */}
      <div
        className="text-xs tracking-[0.4em] mb-1 opacity-70"
        style={{ color: theme.color }}
      >
        {visual.aura}
      </div>

      {/* Nombre */}
      <div
        className="text-sm font-bold font-mono mb-2 tracking-widest"
        style={{ color: theme.color, textShadow: `0 0 8px ${theme.color}` }}
      >
        ✦ {theme.name.toUpperCase()} ✦
      </div>

      {/* Retrato con aura — el ánimo vive aquí, el "hum" late detrás */}
      <div className="relative flex items-center justify-center mb-3">
        {/* Aura ("hum" visual): capa exterior vibra, interior respira */}
        <div
          className="altar-hum absolute inset-0 flex items-center justify-center pointer-events-none"
          style={{ animation: aura.humAnim, zIndex: 0 }}
        >
          <div
            className="altar-aura rounded-full shrink-0"
            style={{
              width: `${aura.size}px`,
              height: `${aura.size}px`,
              background: `radial-gradient(circle, ${theme.color} 0%, transparent 68%)`,
              filter: `blur(${Math.round(visual.glowPx * 0.9)}px)`,
              animation: aura.breatheAnim,
            }}
          />
        </div>

        <DeitySprite deity={deity} mood={mood} isSpeaking={isSpeaking} />
      </div>

      {/* Badge de ánimo */}
      <div
        className="text-[10px] font-mono px-2 py-1 mb-3 rounded border tracking-widest"
        style={{
          color: theme.color,
          borderColor: theme.color,
          opacity: mood === 'reposo' ? 0.6 : 1,
        }}
      >
        {visual.glyph} {visual.label}
      </div>

      {/* Por qué: la lectura del cielo */}
      {!astral.isLoading && astral.faseNombre && (
        <div className="text-[10px] text-gray-500 font-mono space-y-0.5 leading-relaxed">
          <div>
            {astral.faseEmoji} {astral.faseNombre}
          </div>
          {astral.signoNombre && (
            <div>
              luna en {astral.signoNombre} {astral.signoSimbolo}
            </div>
          )}
          {astral.mareaIntensidad && (
            <div>
              marea {astral.mareaIntensidad} · {astral.mareaDireccion}
            </div>
          )}
        </div>
      )}

      {/* La diosa habla — ventana de diálogo en su propio espacio */}
      {isSpeaking && (
        <div
          className="mt-4 text-[10px] font-mono animate-pulse tracking-widest"
          style={{ color: theme.color }}
        >
          ▌ {theme.name} se manifiesta...
        </div>
      )}
      {!isSpeaking && speech && (
        <div
          className="mt-4 w-full text-left rounded-lg border p-3 relative"
          style={{
            borderColor: theme.color,
            background: `${theme.color}0d`,
            boxShadow: `0 0 12px ${theme.color}30, inset 0 0 18px ${theme.color}12`,
          }}
        >
          {/* Comilla ornamental de apertura */}
          <div
            className="absolute -top-2 left-3 px-1 text-base leading-none bg-black"
            style={{ color: theme.color }}
          >
            ❝
          </div>

          {/* Voz de la diosa — habla directamente */}
          <p className="text-xs text-gray-100 leading-relaxed whitespace-pre-wrap italic">
            {speech}
            <span className="not-italic animate-pulse ml-0.5" style={{ color: theme.color }}>
              ▌
            </span>
          </p>

          {/* Firma al pie */}
          <div
            className="mt-2 text-right text-[10px] font-mono tracking-widest opacity-80"
            style={{ color: theme.color }}
          >
            — {theme.name.toLowerCase()}
          </div>
        </div>
      )}
    </div>
  );
}
