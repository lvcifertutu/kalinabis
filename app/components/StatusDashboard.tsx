'use client';

import { useState, useEffect } from 'react';
import { useLunaState } from '@/app/hooks/useLunaState';
import { DEITIES, moodVisual, type DeityKey } from '@/app/lib/deityMoods';

const DEITY_ORDER: DeityKey[] = ['lilith', 'artemisa', 'afrodita', 'isis'];

function useClock(): string {
  const [now, setNow] = useState<string>(() =>
    new Date().toLocaleTimeString('es', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
  );
  useEffect(() => {
    const id = setInterval(
      () =>
        setNow(
          new Date().toLocaleTimeString('es', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
        ),
      1000
    );
    return () => clearInterval(id);
  }, []);
  return now;
}

export function StatusDashboard() {
  const luna = useLunaState();
  const clock = useClock();

  return (
    <div
      className="h-9 px-4 flex items-center gap-0 shrink-0 overflow-hidden"
      style={{
        background: '#0d0b09',
        borderBottom: '1px solid var(--border)',
        fontFamily: 'var(--font-term)',
        fontSize: '11px',
        letterSpacing: '0.04em',
      }}
    >
      {/* Brand */}
      <div
        className="flex items-center gap-2 pr-4 shrink-0"
        style={{ borderRight: '1px solid var(--border)' }}
      >
        <span
          style={{
            fontFamily: 'var(--font-sacred)',
            color: 'var(--accent-gold)',
            fontSize: '12px',
            fontWeight: 600,
            letterSpacing: '0.22em',
          }}
        >
          KALINABIS
        </span>
      </div>

      {/* Lunar oracle */}
      <div className="flex items-center gap-2 px-4 flex-1 overflow-hidden" style={{ borderRight: '1px solid var(--border)' }}>
        {luna.isLoading ? (
          <span style={{ color: 'var(--text-muted)' }} className="animate-pulse tracking-widest">
            · · · leyendo el cielo · · ·
          </span>
        ) : (
          <>
            <span style={{ color: '#7aaecc' }}>
              {luna.faseEmoji}&nbsp;{luna.faseNombre || '—'}
            </span>
            {luna.faseEnergia && (
              <>
                <span style={{ color: 'var(--border)' }}>·</span>
                <span style={{ color: 'var(--text-muted)', fontSize: '10px' }}>{luna.faseEnergia}</span>
              </>
            )}
            {luna.signoNombre && (
              <>
                <span style={{ color: 'var(--border)' }}>·</span>
                <span style={{ color: '#9b8bcc' }}>
                  {luna.signoSimbolo}&nbsp;{luna.signoNombre}
                </span>
              </>
            )}
            {luna.mareaIntensidad && (
              <>
                <span style={{ color: 'var(--border)' }}>·</span>
                <span style={{ color: '#6b9b8a' }}>
                  ≋&nbsp;{luna.mareaIntensidad}&nbsp;{luna.mareaDireccion}
                </span>
              </>
            )}
          </>
        )}
      </div>

      {/* Deity mood indicators */}
      <div className="flex items-center gap-3 px-4" style={{ borderRight: '1px solid var(--border)' }}>
        {DEITY_ORDER.map((key) => {
          const theme = DEITIES[key];
          const mood = luna.moods[key];
          const visual = moodVisual(mood);
          const dimmed = mood === 'reposo';
          return (
            <div
              key={key}
              className="flex items-center gap-[3px]"
              title={`${key} — ${visual.label}`}
              style={{ opacity: dimmed ? 0.35 : 1, transition: 'opacity 0.5s' }}
            >
              <span
                style={{
                  color: theme.color,
                  fontSize: '9px',
                  textShadow: mood === 'amplificada' ? `0 0 8px ${theme.color}` : 'none',
                  lineHeight: 1,
                }}
              >
                {visual.glyph}
              </span>
              <span
                style={{
                  color: theme.color,
                  fontSize: '10px',
                  opacity: 0.85,
                  letterSpacing: '0.08em',
                }}
              >
                {key.slice(0, 3).toUpperCase()}
              </span>
            </div>
          );
        })}
      </div>

      {/* Clock */}
      <div className="pl-4 shrink-0 tabular-nums" style={{ color: 'var(--text-muted)', fontVariantNumeric: 'tabular-nums' }}>
        {clock}
      </div>
    </div>
  );
}
