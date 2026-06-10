'use client';

import React, { useState, useMemo } from 'react';
import { DEITIES, type DeityKey, moodVisual, deityAscii } from '@/app/lib/deityMoods';
import { useLunaState } from '@/app/hooks/useLunaState';

interface DeityProfile {
  titulo: string;
  dominio: string;
  elemento: string;
  historia: string;
  poderes: string[];
  conexiones: DeityKey[];
}

const DEITY_PROFILES: Record<DeityKey, DeityProfile> = {
  lilith: {
    titulo: 'La Soberana Oscura',
    dominio: 'Poder personal, libertad, transformación',
    elemento: 'Fuego + Vacío',
    historia: 'Primera rebelde del universo mágico. Eligió su propio camino antes que someterse a cualquier orden cósmico. En su oscuridad vive la semilla de toda creación auténtica.',
    poderes: ['Manifestación veloz', 'Ruptura de patrones', 'Poder generativo'],
    conexiones: ['artemisa', 'isis'],
  },
  artemisa: {
    titulo: 'La Cazadora Salvaje',
    dominio: 'Naturaleza, independencia, protección',
    elemento: 'Tierra + Aire',
    historia: 'Guardiana de los bosques primordiales y los instintos salvajes. Donde otros ven caos, ella ve el orden perfecto de lo salvaje. Su flecha no yerra.',
    poderes: ['Conexión animal', 'Protección del hogar', 'Caza de objetivos'],
    conexiones: ['lilith', 'isis'],
  },
  afrodita: {
    titulo: 'La Tejedora de Hilos',
    dominio: 'Amor, belleza, conexión, deseo',
    elemento: 'Agua + Luz',
    historia: 'Tejedora de los hilos del destino que conectan almas a través del tiempo. Su magnetismo no es vanidad — es el principio que mantiene unido el universo.',
    poderes: ['Atracción', 'Sanación emocional', 'Armonía de opuestos'],
    conexiones: ['isis', 'lilith'],
  },
  isis: {
    titulo: 'La Alquimista Sagrada',
    dominio: 'Magia, conocimiento, sanación, unidad',
    elemento: 'Agua + Fuego',
    historia: 'Guardiana de la sabiduría antigua y los misterios del universo. Conoce el nombre secreto de todas las cosas y con él puede reescribir la realidad.',
    poderes: ['Alquimia', 'Resurrección', 'Sincronización cósmica'],
    conexiones: ['lilith', 'artemisa', 'afrodita'],
  },
};

function GoldDivider({ color }: { color: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', margin: '1rem 0' }}>
      <div style={{ flex: 1, height: '1px', background: `linear-gradient(to right, transparent, ${color}40)` }} />
      <span style={{ color: `${color}60`, fontSize: '8px', fontFamily: 'var(--font-display)' }}>✦</span>
      <div style={{ flex: 1, height: '1px', background: `linear-gradient(to left, transparent, ${color}40)` }} />
    </div>
  );
}

function SectionHead({ label, color }: { label: string; color: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
      <span style={{ color, fontSize: '10px' }}>◈</span>
      <span
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '9px',
          letterSpacing: '0.3em',
          color: `${color}99`,
          textTransform: 'uppercase',
        }}
      >
        {label}
      </span>
      <div style={{ flex: 1, height: '1px', background: `${color}20` }} />
    </div>
  );
}

export function Capa1Library() {
  const [selectedDeity, setSelectedDeity] = useState<DeityKey>('lilith');
  const [searchTerm, setSearchTerm] = useState('');
  const luna = useLunaState();

  const theme = DEITIES[selectedDeity];
  const profile = DEITY_PROFILES[selectedDeity];
  const mood = luna.moods[selectedDeity];
  const visual = moodVisual(mood);
  const asciiArt = deityAscii(selectedDeity, mood);

  const filteredDeities = useMemo<DeityKey[]>(() => {
    const keys = Object.keys(DEITIES) as DeityKey[];
    if (!searchTerm.trim()) return keys;
    const q = searchTerm.toLowerCase();
    return keys.filter((k) => {
      const p = DEITY_PROFILES[k];
      return (
        k.includes(q) ||
        p.titulo.toLowerCase().includes(q) ||
        p.dominio.toLowerCase().includes(q) ||
        p.elemento.toLowerCase().includes(q)
      );
    });
  }, [searchTerm]);

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        background: 'var(--lib-bg)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Textura de pergamino sutil */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `
            radial-gradient(ellipse at 30% 20%, rgba(200,157,92,0.04) 0%, transparent 60%),
            radial-gradient(ellipse at 70% 80%, rgba(139,115,85,0.03) 0%, transparent 50%)
          `,
          pointerEvents: 'none',
        }}
      />

      {/* ── Panel izquierdo — catálogo ──────────────────────────────────────── */}
      <div
        style={{
          width: '200px',
          flexShrink: 0,
          display: 'flex',
          flexDirection: 'column',
          background: 'rgba(12, 9, 6, 0.7)',
          borderRight: '1px solid rgba(200,157,92,0.15)',
        }}
      >
        {/* Cabecera */}
        <div
          style={{
            padding: '1.25rem 1rem 1rem',
            borderBottom: '1px solid rgba(200,157,92,0.12)',
          }}
        >
          <p
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '8px',
              letterSpacing: '0.4em',
              color: 'rgba(200,157,92,0.5)',
              textTransform: 'uppercase',
              margin: '0 0 0.75rem',
            }}
          >
            Grimorio
          </p>

          {/* Buscador */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.4rem 0.6rem',
              background: 'rgba(200,157,92,0.05)',
              border: '1px solid rgba(200,157,92,0.15)',
              borderRadius: '2px',
            }}
          >
            <span style={{ color: 'rgba(200,157,92,0.4)', fontSize: '10px' }}>✦</span>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="buscar deidad..."
              style={{
                flex: 1,
                background: 'transparent',
                border: 'none',
                outline: 'none',
                fontFamily: 'var(--font-body)',
                fontStyle: 'italic',
                fontSize: '12px',
                color: 'rgba(245,241,232,0.7)',
                caretColor: '#c89d5c',
              }}
            />
          </div>
        </div>

        {/* Lista de deidades */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '0.5rem 0' }}>
          {filteredDeities.map((key) => {
            const t = DEITIES[key];
            const m = luna.moods[key];
            const v = moodVisual(m);
            const p = DEITY_PROFILES[key];
            const isSelected = key === selectedDeity;

            return (
              <button
                key={key}
                onClick={() => setSelectedDeity(key)}
                style={{
                  width: '100%',
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  outline: 'none',
                  textAlign: 'left',
                  padding: '0 0.5rem',
                  marginBottom: '2px',
                }}
              >
                <div
                  style={{
                    padding: '0.6rem 0.75rem',
                    borderLeft: `2px solid ${isSelected ? t.color : `${t.color}25`}`,
                    background: isSelected ? `${t.color}08` : 'transparent',
                    borderRadius: '0 2px 2px 0',
                    transition: 'all 0.2s ease',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
                    <span
                      style={{
                        fontFamily: 'var(--font-display)',
                        fontSize: '10px',
                        letterSpacing: '0.15em',
                        color: isSelected ? t.color : `${t.color}88`,
                        textTransform: 'capitalize',
                        fontWeight: isSelected ? 600 : 400,
                      }}
                    >
                      {key}
                    </span>
                    <span
                      style={{
                        fontSize: '10px',
                        color: t.color,
                        opacity: m === 'amplificada' ? 1 : 0.4,
                        textShadow: m === 'amplificada' ? `0 0 6px ${t.color}` : 'none',
                      }}
                    >
                      {v.glyph}
                    </span>
                  </div>
                  <div
                    style={{
                      fontFamily: 'var(--font-body)',
                      fontStyle: 'italic',
                      fontSize: '11px',
                      color: 'rgba(245,241,232,0.35)',
                      overflow: 'hidden',
                      whiteSpace: 'nowrap',
                      textOverflow: 'ellipsis',
                    }}
                  >
                    {p.titulo}
                  </div>
                </div>
              </button>
            );
          })}

          {filteredDeities.length === 0 && (
            <div
              style={{
                padding: '2rem 1rem',
                textAlign: 'center',
                fontFamily: 'var(--font-body)',
                fontStyle: 'italic',
                fontSize: '12px',
                color: 'rgba(200,157,92,0.3)',
              }}
            >
              ninguna deidad encontrada
            </div>
          )}
        </div>
      </div>

      {/* ── Panel derecho — página del grimorio ────────────────────────────── */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '2rem 2.5rem',
          position: 'relative',
        }}
      >
        {/* Luz de vela ambiental de la deidad */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            right: 0,
            width: '300px',
            height: '300px',
            background: `radial-gradient(ellipse at 80% 20%, ${theme.color}08 0%, transparent 70%)`,
            pointerEvents: 'none',
          }}
        />

        <div style={{ maxWidth: '580px', margin: '0 auto', position: 'relative' }}>
          {/* Cabecera de la deidad */}
          <div style={{ marginBottom: '0.5rem' }}>
            <p
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '8px',
                letterSpacing: '0.45em',
                color: 'rgba(200,157,92,0.4)',
                textTransform: 'uppercase',
                margin: '0 0 0.5rem',
              }}
            >
              Entidad Cósmica
            </p>

            <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between' }}>
              <div>
                <h1
                  style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: 'clamp(1.5rem, 3vw, 2.2rem)',
                    fontWeight: 700,
                    letterSpacing: '0.2em',
                    color: theme.color,
                    textShadow: `0 0 40px ${theme.color}40, 0 0 80px ${theme.color}18`,
                    margin: 0,
                    textTransform: 'uppercase',
                    lineHeight: 1,
                  }}
                >
                  {selectedDeity}
                </h1>
                <p
                  style={{
                    fontFamily: 'var(--font-sacred)',
                    fontStyle: 'italic',
                    fontSize: '13px',
                    color: `${theme.color}88`,
                    margin: '0.4rem 0 0',
                  }}
                >
                  {profile.titulo}
                </p>
              </div>

              {/* Badge de estado lunar */}
              <div style={{ textAlign: 'right' }}>
                <div
                  style={{
                    fontSize: '22px',
                    color: theme.color,
                    textShadow: mood === 'amplificada' ? `0 0 16px ${theme.color}` : 'none',
                    lineHeight: 1,
                  }}
                >
                  {visual.glyph}
                </div>
                <div
                  style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: '8px',
                    letterSpacing: '0.2em',
                    color: `${theme.color}60`,
                    marginTop: '4px',
                  }}
                >
                  {visual.label}
                </div>
              </div>
            </div>
          </div>

          <GoldDivider color={theme.color} />

          {/* Retrato ASCII + stats rápidos */}
          <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.5rem' }}>
            <div
              style={{
                flexShrink: 0,
                border: `1px solid ${theme.color}30`,
                padding: '1rem 1.25rem',
                background: `${theme.color}04`,
                boxShadow: `0 0 30px ${theme.color}10, inset 0 0 20px ${theme.color}04`,
                borderRadius: '2px',
                position: 'relative',
              }}
            >
              {/* Esquinas decorativas */}
              {(['tl', 'tr', 'bl', 'br'] as const).map((c) => (
                <span
                  key={c}
                  style={{
                    position: 'absolute',
                    color: `${theme.color}50`,
                    fontSize: '8px',
                    lineHeight: 1,
                    top: c.startsWith('t') ? '4px' : 'auto',
                    bottom: c.startsWith('b') ? '4px' : 'auto',
                    left: c.endsWith('l') ? '4px' : 'auto',
                    right: c.endsWith('r') ? '4px' : 'auto',
                  }}
                >
                  {c === 'tl' ? '╔' : c === 'tr' ? '╗' : c === 'bl' ? '╚' : '╝'}
                </span>
              ))}

              <pre
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: '12px',
                  color: theme.color,
                  textShadow: `0 0 8px ${theme.color}60`,
                  margin: 0,
                  whiteSpace: 'pre',
                  lineHeight: 1.4,
                  animation: visual.animation,
                  filter: `brightness(${visual.brightness}) saturate(${visual.saturate})`,
                }}
              >
                {asciiArt}
              </pre>
            </div>

            {/* Stats */}
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '1rem', flex: 1 }}>
              {[
                { label: 'Dominio', value: profile.dominio },
                { label: 'Elemento', value: profile.elemento },
                { label: 'Estado', value: `${visual.glyph} ${visual.label} — ${visual.aura}` },
              ].map(({ label, value }) => (
                <div key={label}>
                  <p
                    style={{
                      fontFamily: 'var(--font-display)',
                      fontSize: '8px',
                      letterSpacing: '0.3em',
                      color: 'rgba(200,157,92,0.4)',
                      textTransform: 'uppercase',
                      margin: '0 0 0.25rem',
                    }}
                  >
                    {label}
                  </p>
                  <p
                    style={{
                      fontFamily: 'var(--font-body)',
                      fontSize: '13px',
                      color: 'rgba(245,241,232,0.75)',
                      margin: 0,
                      lineHeight: 1.4,
                    }}
                  >
                    {value}
                  </p>
                  <div style={{ height: '1px', background: `${theme.color}15`, marginTop: '0.5rem' }} />
                </div>
              ))}
            </div>
          </div>

          <GoldDivider color={theme.color} />

          {/* Historia */}
          <div style={{ marginBottom: '1.5rem' }}>
            <SectionHead label="Historia" color={theme.color} />
            <p
              style={{
                fontFamily: 'var(--font-body)',
                fontSize: '14px',
                lineHeight: 1.85,
                color: 'rgba(245,241,232,0.8)',
                margin: 0,
                textIndent: '1.5em',
              }}
            >
              {profile.historia}
            </p>
          </div>

          <GoldDivider color={theme.color} />

          {/* Poderes */}
          <div style={{ marginBottom: '1.5rem' }}>
            <SectionHead label="Poderes" color={theme.color} />
            <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              {profile.poderes.map((poder) => (
                <li key={poder} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <span
                    style={{
                      color: theme.color,
                      fontSize: '10px',
                      textShadow: `0 0 8px ${theme.color}60`,
                      flexShrink: 0,
                    }}
                  >
                    ✦
                  </span>
                  <span
                    style={{
                      fontFamily: 'var(--font-body)',
                      fontSize: '13px',
                      color: 'rgba(245,241,232,0.8)',
                    }}
                  >
                    {poder}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Conexiones */}
          {profile.conexiones.length > 0 && (
            <>
              <GoldDivider color={theme.color} />
              <div style={{ marginBottom: '2rem' }}>
                <SectionHead label="Conexiones" color={theme.color} />
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {profile.conexiones.map((key) => {
                    const ct = DEITIES[key];
                    return (
                      <button
                        key={key}
                        onClick={() => setSelectedDeity(key)}
                        style={{
                          padding: '0.3rem 0.75rem',
                          background: `${ct.color}08`,
                          border: `1px solid ${ct.color}35`,
                          borderRadius: '2px',
                          color: ct.color,
                          fontFamily: 'var(--font-display)',
                          fontSize: '9px',
                          letterSpacing: '0.2em',
                          cursor: 'pointer',
                          outline: 'none',
                          textTransform: 'capitalize',
                          transition: 'all 0.2s ease',
                        }}
                        onMouseEnter={(e) => {
                          const el = e.currentTarget as HTMLButtonElement;
                          el.style.background = `${ct.color}18`;
                          el.style.borderColor = `${ct.color}70`;
                        }}
                        onMouseLeave={(e) => {
                          const el = e.currentTarget as HTMLButtonElement;
                          el.style.background = `${ct.color}08`;
                          el.style.borderColor = `${ct.color}35`;
                        }}
                      >
                        {key}
                      </button>
                    );
                  })}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
