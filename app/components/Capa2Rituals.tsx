'use client';

import React, { useState } from 'react';
import { DEITIES, type DeityKey, type Mood } from '@/app/lib/deityMoods';
import { getRitualesByDeity, type Ritual } from '@/app/lib/rituals';
import { useLunaState } from '@/app/hooks/useLunaState';

function CandleFlame({ color }: { color: string }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div
        style={{
          width: '10px',
          height: '16px',
          background: `linear-gradient(to top, ${color}cc, #ffd700, #fff8e0)`,
          clipPath: 'polygon(50% 0%, 80% 55%, 100% 80%, 70% 100%, 30% 100%, 0% 80%, 20% 55%)',
          animation: 'flame-body 1.8s ease-in-out infinite, flicker 2.5s ease-in-out infinite',
          filter: `drop-shadow(0 0 4px ${color}cc) drop-shadow(0 0 10px ${color}88)`,
          marginBottom: '-1px',
        }}
      />
      <div style={{ width: '1px', height: '5px', background: '#444' }} />
      <div
        style={{
          width: '8px',
          height: '24px',
          background: 'linear-gradient(to right, #e0d0b8, #f5ede0, #d8c8a8)',
          borderRadius: '1px 1px 0 0',
        }}
      />
    </div>
  );
}

function getDifficultyColor(dif: string) {
  switch (dif) {
    case 'básico':     return '#7aba5a';
    case 'intermedio': return '#c89d5c';
    case 'avanzado':   return '#c05070';
    default:           return 'rgba(245,241,232,0.4)';
  }
}

export function Capa2Rituals() {
  const [selectedDeity, setSelectedDeity] = useState<DeityKey>('lilith');
  const [selectedRitual, setSelectedRitual] = useState<string | null>(null);
  const [ritualStarted, setRitualStarted] = useState(false);
  const astral = useLunaState();

  const theme = DEITIES[selectedDeity];
  const rituals = getRitualesByDeity(selectedDeity);
  const currentRitual = selectedRitual ? rituals.find((r) => r.id === selectedRitual) : null;
  const mood = astral.moods[selectedDeity];
  const isBestMood = currentRitual?.mejorPorMood?.includes(mood);

  return (
    <div
      data-deity={selectedDeity}
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        background: 'var(--altar-bg)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Luz ambiental de deidad */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `
            radial-gradient(ellipse at 50% 0%, ${theme.color}0a 0%, transparent 60%),
            radial-gradient(ellipse at 80% 100%, ${theme.color}06 0%, transparent 50%)
          `,
          pointerEvents: 'none',
          transition: 'background 0.8s ease',
        }}
      />

      {/* ── Cabecera del altar ────────────────────────────────────────────────── */}
      <div
        style={{
          padding: '0.75rem 1.5rem',
          borderBottom: `1px solid ${theme.color}20`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'rgba(4,5,14,0.6)',
          flexShrink: 0,
          position: 'relative',
          zIndex: 2,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <CandleFlame color={theme.color} />
          <div>
            <h2
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '11px',
                letterSpacing: '0.35em',
                color: theme.color,
                textShadow: `0 0 20px ${theme.color}60`,
                margin: 0,
                textTransform: 'uppercase',
              }}
            >
              {selectedDeity}
            </h2>
            <p
              style={{
                fontFamily: 'var(--font-sacred)',
                fontStyle: 'italic',
                fontSize: '11px',
                color: `${theme.color}70`,
                margin: 0,
              }}
            >
              {mood === 'amplificada' ? 'Energía amplificada' : mood === 'reposo' ? 'En reposo' : 'Altar activo'}
            </p>
          </div>
        </div>

        {/* Luna */}
        <div style={{ textAlign: 'right' }}>
          <span
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '8px',
              letterSpacing: '0.25em',
              color: 'rgba(200,157,92,0.4)',
            }}
          >
            {astral.faseEmoji} {astral.faseNombre}
          </span>
        </div>
      </div>

      {/* ── Contenido principal ─────────────────────────────────────────────── */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden', position: 'relative', zIndex: 1 }}>

        {/* Panel 1 — Selector de deidades */}
        <div
          style={{
            width: '130px',
            flexShrink: 0,
            display: 'flex',
            flexDirection: 'column',
            borderRight: `1px solid rgba(200,157,92,0.1)`,
            background: 'rgba(4,5,14,0.5)',
            padding: '0.75rem 0',
            overflowY: 'auto',
          }}
        >
          <p
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '7px',
              letterSpacing: '0.35em',
              color: 'rgba(200,157,92,0.35)',
              textTransform: 'uppercase',
              padding: '0 0.75rem',
              margin: '0 0 0.75rem',
            }}
          >
            Deidades
          </p>

          {(Object.keys(DEITIES) as DeityKey[]).map((diosa) => {
            const t = DEITIES[diosa];
            const isActive = diosa === selectedDeity;
            return (
              <button
                key={diosa}
                onClick={() => {
                  setSelectedDeity(diosa);
                  setSelectedRitual(null);
                  setRitualStarted(false);
                }}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  outline: 'none',
                  padding: '0.5rem 0.75rem',
                  textAlign: 'left',
                  position: 'relative',
                }}
              >
                {isActive && (
                  <div
                    style={{
                      position: 'absolute',
                      left: 0,
                      top: '20%',
                      bottom: '20%',
                      width: '2px',
                      background: `linear-gradient(to bottom, transparent, ${t.color}, transparent)`,
                    }}
                  />
                )}
                <span
                  style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: '9px',
                    letterSpacing: '0.15em',
                    color: isActive ? t.color : `${t.color}55`,
                    textTransform: 'capitalize',
                    textShadow: isActive ? `0 0 10px ${t.color}60` : 'none',
                    display: 'block',
                  }}
                >
                  {diosa}
                </span>
              </button>
            );
          })}
        </div>

        {/* Panel 2 — Lista de rituales */}
        <div
          style={{
            width: '200px',
            flexShrink: 0,
            display: 'flex',
            flexDirection: 'column',
            borderRight: `1px solid ${theme.color}15`,
            background: 'rgba(6,7,18,0.4)',
            padding: '0.75rem 0',
            overflowY: 'auto',
            transition: 'border-color 0.4s ease',
          }}
        >
          <p
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '7px',
              letterSpacing: '0.35em',
              color: `${theme.color}50`,
              textTransform: 'uppercase',
              padding: '0 0.75rem',
              margin: '0 0 0.75rem',
            }}
          >
            Rituales
          </p>

          {rituals.map((ritual) => {
            const isActive = selectedRitual === ritual.id;
            return (
              <button
                key={ritual.id}
                onClick={() => {
                  setSelectedRitual(ritual.id);
                  setRitualStarted(false);
                }}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  outline: 'none',
                  padding: '0.5rem 0.75rem',
                  textAlign: 'left',
                  borderLeft: `2px solid ${isActive ? theme.color : `${theme.color}20`}`,
                  marginBottom: '2px',
                  transition: 'border-color 0.2s ease',
                }}
              >
                <div
                  style={{
                    fontFamily: 'var(--font-body)',
                    fontSize: '12px',
                    color: isActive ? theme.color : 'rgba(245,241,232,0.6)',
                    marginBottom: '3px',
                    lineHeight: 1.3,
                  }}
                >
                  {ritual.nombre}
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <span
                    style={{
                      fontFamily: 'var(--font-display)',
                      fontSize: '9px',
                      color: 'rgba(245,241,232,0.25)',
                    }}
                  >
                    {ritual.duracion}
                  </span>
                  <span style={{ color: 'rgba(245,241,232,0.15)', fontSize: '8px' }}>·</span>
                  <span
                    style={{
                      fontFamily: 'var(--font-display)',
                      fontSize: '9px',
                      color: getDifficultyColor(ritual.dificultad),
                      letterSpacing: '0.05em',
                    }}
                  >
                    {ritual.dificultad}
                  </span>
                </div>
              </button>
            );
          })}

          {rituals.length === 0 && (
            <p
              style={{
                fontFamily: 'var(--font-body)',
                fontStyle: 'italic',
                fontSize: '12px',
                color: 'rgba(245,241,232,0.2)',
                padding: '1rem 0.75rem',
              }}
            >
              Sin rituales disponibles
            </p>
          )}
        </div>

        {/* Panel 3 — Detalle del ritual */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '1.25rem 1.5rem' }}>
          {!currentRitual ? (
            <div
              style={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '1rem',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: '0.5rem',
                  opacity: 0.4,
                }}
              >
                <CandleFlame color={theme.color} />
                <CandleFlame color={theme.color} />
              </div>
              <p
                style={{
                  fontFamily: 'var(--font-sacred)',
                  fontStyle: 'italic',
                  fontSize: '13px',
                  color: `${theme.color}50`,
                  textAlign: 'center',
                }}
              >
                Elige un ritual para comenzar
              </p>
            </div>
          ) : !ritualStarted ? (
            <div style={{ maxWidth: '480px' }}>
              {/* Nombre */}
              <h2
                style={{
                  fontFamily: 'var(--font-display)',
                  fontSize: '1.2rem',
                  letterSpacing: '0.1em',
                  color: theme.color,
                  textShadow: `0 0 30px ${theme.color}50`,
                  margin: '0 0 0.25rem',
                }}
              >
                {currentRitual.nombre}
              </h2>
              <p
                style={{
                  fontFamily: 'var(--font-body)',
                  fontStyle: 'italic',
                  fontSize: '13px',
                  color: 'rgba(245,241,232,0.5)',
                  margin: '0 0 1.25rem',
                }}
              >
                {currentRitual.descripcion}
              </p>

              {/* Mood */}
              <div
                style={{
                  padding: '0.75rem 1rem',
                  background: isBestMood ? `${theme.color}10` : 'rgba(245,241,232,0.03)',
                  border: `1px solid ${isBestMood ? `${theme.color}40` : 'rgba(245,241,232,0.08)'}`,
                  borderRadius: '2px',
                  marginBottom: '1rem',
                }}
              >
                <p
                  style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: '8px',
                    letterSpacing: '0.3em',
                    color: isBestMood ? theme.color : 'rgba(200,157,92,0.4)',
                    margin: '0 0 0.4rem',
                  }}
                >
                  {isBestMood ? '✦ Momento Óptimo' : 'Estado Energético'}
                </p>
                <p
                  style={{
                    fontFamily: 'var(--font-body)',
                    fontSize: '12px',
                    color: 'rgba(245,241,232,0.6)',
                    margin: 0,
                  }}
                >
                  Tu energía es{' '}
                  <span style={{ color: theme.color }}>{mood}</span>
                  {isBestMood
                    ? ' — ideal para este ritual'
                    : ' — el ritual funciona igual, con más potencia en otros estados'}
                </p>
              </div>

              {/* Requerimientos */}
              <div style={{ marginBottom: '1rem' }}>
                <p
                  style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: '8px',
                    letterSpacing: '0.3em',
                    color: 'rgba(200,157,92,0.4)',
                    textTransform: 'uppercase',
                    margin: '0 0 0.6rem',
                  }}
                >
                  Requerimientos
                </p>
                <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {currentRitual.requerimientos.map((req, i) => (
                    <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                      <span
                        style={{
                          width: '12px',
                          height: '12px',
                          border: `1px solid ${theme.color}40`,
                          borderRadius: '1px',
                          flexShrink: 0,
                          display: 'inline-block',
                        }}
                      />
                      <span
                        style={{
                          fontFamily: 'var(--font-body)',
                          fontSize: '12px',
                          color: 'rgba(245,241,232,0.6)',
                        }}
                      >
                        {req}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Efectos */}
              <div style={{ marginBottom: '1.5rem' }}>
                <p
                  style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: '8px',
                    letterSpacing: '0.3em',
                    color: 'rgba(200,157,92,0.4)',
                    textTransform: 'uppercase',
                    margin: '0 0 0.6rem',
                  }}
                >
                  Efectos
                </p>
                <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {currentRitual.efectos.map((efecto, i) => (
                    <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                      <span style={{ color: theme.color, fontSize: '9px', flexShrink: 0 }}>✦</span>
                      <span
                        style={{
                          fontFamily: 'var(--font-body)',
                          fontSize: '12px',
                          color: 'rgba(245,241,232,0.6)',
                        }}
                      >
                        {efecto}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Botón de inicio */}
              <button
                onClick={() => setRitualStarted(true)}
                style={{
                  padding: '0.6rem 1.5rem',
                  background: `${theme.color}15`,
                  border: `1px solid ${theme.color}60`,
                  color: theme.color,
                  fontFamily: 'var(--font-display)',
                  fontSize: '9px',
                  letterSpacing: '0.35em',
                  textTransform: 'uppercase',
                  cursor: 'pointer',
                  outline: 'none',
                  borderRadius: '2px',
                  transition: 'all 0.2s ease',
                  boxShadow: `0 0 20px ${theme.color}10`,
                }}
                onMouseEnter={(e) => {
                  const el = e.currentTarget as HTMLButtonElement;
                  el.style.background = `${theme.color}25`;
                  el.style.boxShadow = `0 0 30px ${theme.color}30`;
                }}
                onMouseLeave={(e) => {
                  const el = e.currentTarget as HTMLButtonElement;
                  el.style.background = `${theme.color}15`;
                  el.style.boxShadow = `0 0 20px ${theme.color}10`;
                }}
              >
                Iniciar Ritual
              </button>
            </div>
          ) : (
            <div style={{ maxWidth: '480px' }}>
              <h2
                style={{
                  fontFamily: 'var(--font-display)',
                  fontSize: '1.2rem',
                  letterSpacing: '0.1em',
                  color: theme.color,
                  textShadow: `0 0 30px ${theme.color}50`,
                  margin: '0 0 1.25rem',
                }}
              >
                {currentRitual.nombre}
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.5rem' }}>
                {currentRitual.pasos.map((paso, i) => (
                  <div
                    key={i}
                    style={{
                      padding: '0.75rem 1rem',
                      background: 'rgba(245,241,232,0.03)',
                      border: `1px solid ${theme.color}15`,
                      borderLeft: `3px solid ${theme.color}50`,
                      borderRadius: '0 2px 2px 0',
                    }}
                  >
                    <span
                      style={{
                        fontFamily: 'var(--font-display)',
                        fontSize: '8px',
                        letterSpacing: '0.2em',
                        color: `${theme.color}60`,
                        display: 'block',
                        marginBottom: '0.3rem',
                      }}
                    >
                      Paso {i + 1}
                    </span>
                    <p
                      style={{
                        fontFamily: 'var(--font-body)',
                        fontSize: '13px',
                        color: 'rgba(245,241,232,0.8)',
                        margin: 0,
                        lineHeight: 1.6,
                      }}
                    >
                      {paso}
                    </p>
                  </div>
                ))}
              </div>

              <div
                style={{
                  padding: '0.75rem 1rem',
                  background: 'rgba(122,186,0,0.06)',
                  border: '1px solid rgba(122,186,0,0.2)',
                  borderRadius: '2px',
                  marginBottom: '1rem',
                }}
              >
                <p
                  style={{
                    fontFamily: 'var(--font-body)',
                    fontStyle: 'italic',
                    fontSize: '12px',
                    color: 'rgba(122,186,0,0.7)',
                    margin: 0,
                  }}
                >
                  ✦ Ritual completado. Siente los efectos activándose en tu campo energético.
                </p>
              </div>

              <button
                onClick={() => setRitualStarted(false)}
                style={{
                  padding: '0.5rem 1.25rem',
                  background: 'rgba(245,241,232,0.05)',
                  border: '1px solid rgba(245,241,232,0.15)',
                  color: 'rgba(245,241,232,0.5)',
                  fontFamily: 'var(--font-display)',
                  fontSize: '8px',
                  letterSpacing: '0.25em',
                  cursor: 'pointer',
                  outline: 'none',
                  borderRadius: '2px',
                }}
              >
                Cerrar
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
