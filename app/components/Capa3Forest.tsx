'use client';

import React, { useState } from 'react';
import { useCapa3API } from '@/app/hooks/useCapa3API';
import { useLunaState } from '@/app/hooks/useLunaState';

const CATEGORIAS = ['general', 'numeros', 'sueños', 'encuentros', 'señales'];

// Orb flotante decorativo
function Orb({ color, size, style }: { color: string; size: number; style?: React.CSSProperties }) {
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        background: `radial-gradient(circle at 35% 35%, ${color}cc, ${color}40 50%, transparent 75%)`,
        boxShadow: `0 0 ${size * 0.6}px ${color}40, inset 0 0 ${size * 0.3}px ${color}20`,
        animation: 'orb-drift 6s ease-in-out infinite',
        flexShrink: 0,
        ...style,
      }}
    />
  );
}

// Panel base del bosque
function ForestPanel({
  title,
  accent,
  count,
  headerExtra,
  children,
}: {
  title: string;
  accent: string;
  count: number | string;
  headerExtra?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        background: 'rgba(8,18,12,0.7)',
        border: `1px solid ${accent}25`,
        borderRadius: '3px',
        overflow: 'hidden',
        boxShadow: `0 0 20px ${accent}08, inset 0 0 30px rgba(0,0,0,0.3)`,
      }}
    >
      {/* Cabecera del panel */}
      <div
        style={{
          padding: '0.6rem 0.9rem',
          borderBottom: `1px solid ${accent}20`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: `${accent}05`,
          flexShrink: 0,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Orb color={accent} size={8} />
          <span
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '8px',
              letterSpacing: '0.3em',
              color: `${accent}cc`,
              textTransform: 'uppercase',
            }}
          >
            {title}
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {headerExtra}
          <span
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '8px',
              color: `${accent}50`,
              letterSpacing: '0.1em',
            }}
          >
            [{count}]
          </span>
        </div>
      </div>

      {/* Contenido */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '0.6rem' }}>
        {children}
      </div>
    </div>
  );
}

function ForestItem({
  accent,
  children,
}: {
  accent: string;
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        padding: '0.5rem 0.6rem',
        background: `${accent}06`,
        border: `1px solid ${accent}18`,
        borderRadius: '2px',
        marginBottom: '4px',
      }}
    >
      {children}
    </div>
  );
}

function ForestLabel({ color, children }: { color: string; children: React.ReactNode }) {
  return (
    <span
      style={{
        fontFamily: 'var(--font-display)',
        fontSize: '9px',
        letterSpacing: '0.15em',
        color,
        display: 'block',
        marginBottom: '3px',
      }}
    >
      {children}
    </span>
  );
}

function ForestText({ children }: { children: React.ReactNode }) {
  return (
    <p
      style={{
        fontFamily: 'var(--font-body)',
        fontSize: '11px',
        color: 'rgba(200,220,200,0.55)',
        margin: 0,
        lineHeight: 1.4,
        overflow: 'hidden',
        display: '-webkit-box',
        WebkitLineClamp: 2,
        WebkitBoxOrient: 'vertical',
      }}
    >
      {children}
    </p>
  );
}

function EmptyState({ color, text }: { color: string; text: string }) {
  return (
    <p
      style={{
        fontFamily: 'var(--font-body)',
        fontStyle: 'italic',
        fontSize: '12px',
        color: `${color}30`,
        textAlign: 'center',
        padding: '1rem 0.5rem',
        margin: 0,
      }}
    >
      {text}
    </p>
  );
}

// ── Esferas ─────────────────────────────────────────────────────────────────
function EsferasPanel({
  esferas,
  isLoading,
}: {
  esferas: import('@/app/hooks/useCapa3API').Esfera[];
  isLoading: boolean;
}) {
  return (
    <ForestPanel title="Esferas Vivas" accent="#4aa8c8" count={isLoading ? '…' : esferas.length}>
      {isLoading && <EmptyState color="#4aa8c8" text="Resonando con el bosque…" />}
      {!isLoading && esferas.length === 0 && <EmptyState color="#4aa8c8" text="Sin esferas aún" />}
      {esferas.map((esfera) => (
        <ForestItem key={esfera.id} accent="#4aa8c8">
          <ForestLabel color="#4aa8c8">{esfera.tipo} · {esfera.clave}</ForestLabel>
          <div style={{ height: '3px', background: 'rgba(74,168,200,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                width: `${Math.min(100, esfera.amplitud * 100)}%`,
                background: 'linear-gradient(to right, #4aa8c8, #7ad8f0)',
                borderRadius: '2px',
                transition: 'width 0.4s ease',
              }}
            />
          </div>
        </ForestItem>
      ))}
    </ForestPanel>
  );
}

// ── Semillas ─────────────────────────────────────────────────────────────────
function SemillasPanel({
  semillas,
  isLoading,
}: {
  semillas: import('@/app/hooks/useCapa3API').Semilla[];
  isLoading: boolean;
}) {
  return (
    <ForestPanel title="Semillas Aportadas" accent="#7aba5a" count={isLoading ? '…' : semillas.length}>
      {isLoading && <EmptyState color="#7aba5a" text="Brotando…" />}
      {!isLoading && semillas.length === 0 && <EmptyState color="#7aba5a" text="Sin semillas plantadas" />}
      {semillas.slice(0, 8).map((semilla) => (
        <ForestItem key={semilla.id} accent="#7aba5a">
          <ForestLabel color="#7aba5a">{semilla.estado}</ForestLabel>
          <ForestText>{semilla.intencion}</ForestText>
        </ForestItem>
      ))}
    </ForestPanel>
  );
}

// ── Sincronicidades ───────────────────────────────────────────────────────────
function SincroniciadesPanel({
  sincros,
  isLoading,
  onRegistrar,
  onConfirmar,
}: {
  sincros: import('@/app/hooks/useCapa3API').Sincronicidad[];
  isLoading: boolean;
  onRegistrar: (descripcion: string, categoria: string) => Promise<void>;
  onConfirmar: (id: number) => Promise<void>;
}) {
  const [showForm, setShowForm] = useState(false);
  const [descripcion, setDescripcion] = useState('');
  const [categoria, setCategoria] = useState('general');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!descripcion.trim() || submitting) return;
    setSubmitting(true);
    try {
      await onRegistrar(descripcion.trim(), categoria);
      setDescripcion('');
      setShowForm(false);
    } catch {
      // mantener form abierto en error
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <ForestPanel
      title="Sincronicidades"
      accent="#c8a050"
      count={isLoading ? '…' : sincros.length}
      headerExtra={
        <button
          onClick={() => setShowForm((v) => !v)}
          style={{
            padding: '0.2rem 0.5rem',
            background: showForm ? 'rgba(200,160,80,0.15)' : 'transparent',
            border: '1px solid rgba(200,160,80,0.35)',
            color: 'rgba(200,160,80,0.8)',
            fontFamily: 'var(--font-display)',
            fontSize: '8px',
            letterSpacing: '0.1em',
            cursor: 'pointer',
            outline: 'none',
            borderRadius: '2px',
          }}
        >
          {showForm ? '×' : '+ nueva'}
        </button>
      }
    >
      {showForm && (
        <form
          onSubmit={handleSubmit}
          style={{
            padding: '0.6rem',
            background: 'rgba(200,160,80,0.05)',
            border: '1px solid rgba(200,160,80,0.2)',
            borderRadius: '2px',
            marginBottom: '0.5rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.4rem',
          }}
        >
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            placeholder="Describe la sincronicidad observada…"
            rows={2}
            style={{
              width: '100%',
              background: 'rgba(0,0,0,0.4)',
              border: '1px solid rgba(200,160,80,0.25)',
              borderRadius: '2px',
              padding: '0.4rem',
              fontFamily: 'var(--font-body)',
              fontStyle: 'italic',
              fontSize: '11px',
              color: 'rgba(245,241,232,0.7)',
              outline: 'none',
              resize: 'none',
              caretColor: '#c8a050',
            }}
          />
          <div style={{ display: 'flex', gap: '0.4rem' }}>
            <select
              value={categoria}
              onChange={(e) => setCategoria(e.target.value)}
              style={{
                flex: 1,
                background: 'rgba(0,0,0,0.4)',
                border: '1px solid rgba(200,160,80,0.25)',
                borderRadius: '2px',
                padding: '0.3rem 0.4rem',
                fontFamily: 'var(--font-display)',
                fontSize: '9px',
                color: 'rgba(200,160,80,0.8)',
                outline: 'none',
              }}
            >
              {CATEGORIAS.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
            <button
              type="submit"
              disabled={submitting || !descripcion.trim()}
              style={{
                padding: '0.3rem 0.75rem',
                background: 'rgba(200,160,80,0.12)',
                border: '1px solid rgba(200,160,80,0.35)',
                color: submitting || !descripcion.trim() ? 'rgba(200,160,80,0.3)' : 'rgba(200,160,80,0.8)',
                fontFamily: 'var(--font-display)',
                fontSize: '8px',
                letterSpacing: '0.1em',
                cursor: submitting || !descripcion.trim() ? 'not-allowed' : 'pointer',
                outline: 'none',
                borderRadius: '2px',
              }}
            >
              {submitting ? '…' : 'registrar'}
            </button>
          </div>
        </form>
      )}

      {isLoading && <EmptyState color="#c8a050" text="Leyendo los hilos…" />}
      {!isLoading && sincros.length === 0 && !showForm && (
        <EmptyState color="#c8a050" text="Sin sincronicidades. Registra la primera." />
      )}
      {sincros.slice(0, 8).map((sync) => (
        <ForestItem key={sync.id} accent="#c8a050">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '3px' }}>
            <ForestLabel color="#c8a050">{sync.categoria}</ForestLabel>
            {sync.confirmada ? (
              <span
                style={{
                  fontFamily: 'var(--font-display)',
                  fontSize: '8px',
                  color: '#7aba5a',
                  letterSpacing: '0.1em',
                }}
              >
                ✦ confirmada
              </span>
            ) : (
              <button
                onClick={() => onConfirmar(sync.id)}
                style={{
                  padding: '0.15rem 0.4rem',
                  background: 'transparent',
                  border: '1px solid rgba(122,186,90,0.3)',
                  color: 'rgba(122,186,90,0.6)',
                  fontFamily: 'var(--font-display)',
                  fontSize: '7px',
                  letterSpacing: '0.1em',
                  cursor: 'pointer',
                  outline: 'none',
                  borderRadius: '2px',
                }}
              >
                confirmar
              </button>
            )}
          </div>
          <ForestText>{sync.descripcion}</ForestText>
          {sync.fase_lunar && (
            <span
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '8px',
                color: 'rgba(200,160,80,0.3)',
                letterSpacing: '0.1em',
                display: 'block',
                marginTop: '3px',
              }}
            >
              {sync.fase_lunar}
            </span>
          )}
        </ForestItem>
      ))}
    </ForestPanel>
  );
}

// ── Micorriza ─────────────────────────────────────────────────────────────────
function MicorrizaPanel({
  micorrizas,
  isLoading,
}: {
  micorrizas: import('@/app/hooks/useCapa3API').Micorriza[];
  isLoading: boolean;
}) {
  return (
    <ForestPanel title="Micorriza" accent="#9878cc" count={isLoading ? '…' : micorrizas.length}>
      {isLoading && <EmptyState color="#9878cc" text="Rastreando conexiones…" />}
      {!isLoading && micorrizas.length === 0 && <EmptyState color="#9878cc" text="Sin conexiones establecidas" />}
      {micorrizas.slice(0, 8).map((micro) => (
        <ForestItem key={micro.id} accent="#9878cc">
          <ForestLabel color="#9878cc">{micro.otro_mago}</ForestLabel>
          <ForestText>{micro.ritual}</ForestText>
        </ForestItem>
      ))}
    </ForestPanel>
  );
}

// ── Componente principal ─────────────────────────────────────────────────────
export function Capa3Forest() {
  const capa3 = useCapa3API();
  const luna = useLunaState();

  if (capa3.error) {
    return (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'var(--forest-bg)',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <p
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '11px',
              letterSpacing: '0.3em',
              color: 'rgba(200,80,80,0.7)',
              marginBottom: '0.5rem',
            }}
          >
            El árbol no responde
          </p>
          <p
            style={{
              fontFamily: 'var(--font-body)',
              fontStyle: 'italic',
              fontSize: '12px',
              color: 'rgba(245,241,232,0.3)',
              marginBottom: '1rem',
            }}
          >
            {capa3.error}
          </p>
          <button
            onClick={() => capa3.recargar()}
            style={{
              padding: '0.4rem 1rem',
              background: 'transparent',
              border: '1px solid rgba(200,80,80,0.3)',
              color: 'rgba(200,80,80,0.6)',
              fontFamily: 'var(--font-display)',
              fontSize: '9px',
              letterSpacing: '0.2em',
              cursor: 'pointer',
              outline: 'none',
              borderRadius: '2px',
            }}
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        background: 'var(--forest-bg)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Luz ambiental del bosque */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `
            radial-gradient(ellipse at 25% 30%, rgba(45,106,79,0.12) 0%, transparent 55%),
            radial-gradient(ellipse at 75% 70%, rgba(74,168,200,0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 0%, rgba(232,224,208,0.04) 0%, transparent 40%)
          `,
          pointerEvents: 'none',
        }}
      />

      {/* Orbes flotantes decorativos */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          pointerEvents: 'none',
          overflow: 'hidden',
        }}
      >
        <Orb color="#4aa8c8" size={24} style={{ position: 'absolute', top: '15%', right: '12%', animationDelay: '0s', opacity: 0.4 }} />
        <Orb color="#7aba5a" size={16} style={{ position: 'absolute', top: '60%', right: '25%', animationDelay: '2s', opacity: 0.3 }} />
        <Orb color="#c8a050" size={20} style={{ position: 'absolute', bottom: '20%', left: '15%', animationDelay: '4s', opacity: 0.35 }} />
        <Orb color="#9878cc" size={14} style={{ position: 'absolute', top: '40%', left: '8%', animationDelay: '1s', opacity: 0.3 }} />
      </div>

      {/* ── Cabecera ──────────────────────────────────────────────────────────── */}
      <div
        style={{
          padding: '0.75rem 1.5rem',
          borderBottom: '1px solid rgba(45,106,79,0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexShrink: 0,
          background: 'rgba(4,10,7,0.6)',
          position: 'relative',
          zIndex: 2,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <Orb color="#7aba5a" size={10} />
          <div>
            <h2
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '11px',
                letterSpacing: '0.35em',
                color: '#7aba5a',
                textShadow: '0 0 20px rgba(122,186,90,0.4)',
                margin: 0,
                textTransform: 'uppercase',
              }}
            >
              El Bosque
            </h2>
            <p
              style={{
                fontFamily: 'var(--font-sacred)',
                fontStyle: 'italic',
                fontSize: '10px',
                color: 'rgba(122,186,90,0.5)',
                margin: 0,
              }}
            >
              Red colectiva de practicantes
            </p>
          </div>
        </div>

        <div
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '8px',
            letterSpacing: '0.2em',
            color: 'rgba(232,224,208,0.35)',
          }}
        >
          {luna.faseEmoji} {luna.faseNombre}
        </div>
      </div>

      {/* ── Grid 2×2 ──────────────────────────────────────────────────────────── */}
      <div
        style={{
          flex: 1,
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gridTemplateRows: '1fr 1fr',
          gap: '6px',
          padding: '0.75rem',
          overflow: 'hidden',
          position: 'relative',
          zIndex: 1,
        }}
      >
        <EsferasPanel esferas={capa3.data.esferas} isLoading={capa3.isLoading} />
        <SemillasPanel semillas={capa3.data.semillas} isLoading={capa3.isLoading} />
        <SincroniciadesPanel
          sincros={capa3.data.sincros}
          isLoading={capa3.isLoading}
          onRegistrar={capa3.registrarSync}
          onConfirmar={capa3.confirmarSync}
        />
        <MicorrizaPanel micorrizas={capa3.data.micorrizas} isLoading={capa3.isLoading} />
      </div>
    </div>
  );
}
