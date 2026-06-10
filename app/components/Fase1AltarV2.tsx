'use client';

import React, { useState } from 'react';
import { Capa1Library } from './Capa1Library';
import { AltarWorkspace } from './AltarWorkspace';
import { Capa3Forest } from './Capa3Forest';

type CapaLevel = 'capa1' | 'capa2' | 'capa3';

const CAPAS: { id: CapaLevel; symbol: string; name: string; subtitle: string; accent: string }[] = [
  { id: 'capa1', symbol: '◈', name: 'Librería',  subtitle: 'Sabiduría',  accent: '#c89d5c' },
  { id: 'capa2', symbol: '⬟', name: 'Altar',     subtitle: 'Ritual',     accent: 'var(--deidad-bright)' },
  { id: 'capa3', symbol: '⬡', name: 'Bosque',    subtitle: 'Colectivo',  accent: '#7aba00' },
];

function NavItem({
  capa,
  active,
  onClick,
}: {
  capa: (typeof CAPAS)[number];
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      aria-current={active ? 'page' : undefined}
      title={capa.name}
      style={{
        position: 'relative',
        width: '52px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '4px',
        padding: '10px 0',
        background: 'transparent',
        border: 'none',
        cursor: 'pointer',
        outline: 'none',
      }}
    >
      {/* Indicador lateral activo */}
      {active && (
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: '20%',
            bottom: '20%',
            width: '2px',
            background: `linear-gradient(to bottom, transparent, ${capa.accent}, transparent)`,
            borderRadius: '0 1px 1px 0',
          }}
        />
      )}

      {/* Símbolo */}
      <span
        style={{
          fontSize: '18px',
          lineHeight: 1,
          color: active ? capa.accent : 'rgba(245,241,232,0.25)',
          textShadow: active ? `0 0 12px ${capa.accent}, 0 0 24px ${capa.accent}40` : 'none',
          transition: 'all 0.4s ease',
          filter: active ? `drop-shadow(0 0 4px ${capa.accent})` : 'none',
        }}
      >
        {capa.symbol}
      </span>

      {/* Nombre */}
      <span
        style={{
          fontSize: '7px',
          letterSpacing: '0.15em',
          fontFamily: 'var(--font-display)',
          color: active ? capa.accent : 'rgba(245,241,232,0.2)',
          transition: 'color 0.4s ease',
          textTransform: 'uppercase',
        }}
      >
        {capa.name}
      </span>
    </button>
  );
}

export function Fase1AltarV2() {
  const [activeCapa, setActiveCapa] = useState<CapaLevel>('capa2');

  return (
    <div
      style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        overflow: 'hidden',
        background: '#060810',
      }}
    >
      {/* Grain global */}
      <div className="grain-overlay" />

      {/* ── Rail de navegación izquierdo ───────────────────────────────────── */}
      <nav
        aria-label="Capas del altar"
        style={{
          width: '52px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          paddingTop: '1.5rem',
          paddingBottom: '1.5rem',
          gap: '0.25rem',
          flexShrink: 0,
          background: 'rgba(6, 4, 2, 0.9)',
          borderRight: '1px solid rgba(200,157,92,0.1)',
          position: 'relative',
          zIndex: 10,
        }}
      >
        {/* Logo vertical */}
        <div
          style={{
            writingMode: 'vertical-rl',
            transform: 'rotate(180deg)',
            fontFamily: 'var(--font-display)',
            fontSize: '7px',
            letterSpacing: '0.35em',
            color: 'rgba(200,157,92,0.35)',
            marginBottom: '1.5rem',
            userSelect: 'none',
          }}
        >
          KALINABIS
        </div>

        {/* Separador */}
        <div
          style={{
            width: '20px',
            height: '1px',
            background: 'rgba(200,157,92,0.2)',
            marginBottom: '0.5rem',
          }}
        />

        {/* Botones de capa */}
        {CAPAS.map((capa) => (
          <NavItem
            key={capa.id}
            capa={capa}
            active={activeCapa === capa.id}
            onClick={() => setActiveCapa(capa.id)}
          />
        ))}

        {/* Separador inferior */}
        <div style={{ flex: 1 }} />
        <div
          style={{
            width: '20px',
            height: '1px',
            background: 'rgba(200,157,92,0.2)',
          }}
        />

        {/* Punto de energía */}
        <div
          style={{
            width: '6px',
            height: '6px',
            borderRadius: '50%',
            background: 'var(--deidad-bright)',
            marginTop: '0.75rem',
            boxShadow: '0 0 8px var(--deidad-glow)',
            animation: 'breathe 3s ease-in-out infinite',
          }}
        />
      </nav>

      {/* ── Contenido ────────────────────────────────────────────────────────── */}
      <main
        style={{
          flex: 1,
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: activeCapa === 'capa1' ? 'block' : 'none',
          }}
        >
          <Capa1Library />
        </div>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: activeCapa === 'capa2' ? 'block' : 'none',
          }}
        >
          <AltarWorkspace />
        </div>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: activeCapa === 'capa3' ? 'block' : 'none',
          }}
        >
          <Capa3Forest />
        </div>
      </main>
    </div>
  );
}
