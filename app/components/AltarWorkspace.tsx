'use client';

import React, { useState, useCallback } from 'react';
import { Capa12Altar } from './Capa12Altar';
import { DEITIES, type DeityKey } from '@/app/lib/deityMoods';
import { apiClient } from '@/app/lib/apiClient';

type AltarTab = 'terminal' | 'manifestar' | 'sigilo' | 'limpia' | 'ayni';

const TABS: { id: AltarTab; symbol: string; label: string; accent: string }[] = [
  { id: 'terminal', symbol: '⬟', label: 'Altar',      accent: 'var(--deidad-bright)' },
  { id: 'manifestar', symbol: '◉', label: 'Manifestar', accent: '#c89d5c' },
  { id: 'sigilo',     symbol: '✦', label: 'Sigilo',     accent: '#9878cc' },
  { id: 'limpia',     symbol: '◌', label: 'Limpia',     accent: '#5cb8c8' },
  { id: 'ayni',       symbol: '⊕', label: 'Ayni',       accent: '#7aba5a' },
];

// ── Panel: Manifestar ────────────────────────────────────────────────────────

function PanelManifestar() {
  const DEIDADES: DeityKey[] = ['lilith', 'artemisa', 'afrodita', 'isis'];
  const [deidad, setDeidad] = useState<DeityKey>('lilith');
  const [intencion, setIntencion] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [loading, setLoading] = useState(false);

  const manifestar = useCallback(async () => {
    if (!intencion.trim()) return;
    setLoading(true);
    setRespuesta('');
    try {
      const data = await apiClient.post<{ respuesta?: string; error?: string }>(
        '/api/consultar',
        { mensaje: `/manifestar ${deidad} ${intencion.trim()}` }
      );
      setRespuesta(data.respuesta ?? data.error ?? 'Sin respuesta');
    } catch (e) {
      setRespuesta('[Error al manifestar]');
    } finally {
      setLoading(false);
    }
  }, [deidad, intencion]);

  return (
    <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', height: '100%', overflowY: 'auto' }}>
      <SectionTitle symbol="◉" color="#c89d5c" label="Declarar Manifestación" />

      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        {DEIDADES.map((d) => {
          const theme = DEITIES[d];
          return (
            <button
              key={d}
              onClick={() => setDeidad(d)}
              style={{
                padding: '0.4rem 1rem',
                background: deidad === d ? `${theme.color}22` : 'transparent',
                border: `1px solid ${deidad === d ? theme.color : 'rgba(200,157,92,0.2)'}`,
                borderRadius: '2px',
                color: deidad === d ? theme.color : 'rgba(245,241,232,0.4)',
                fontFamily: 'var(--font-display)',
                fontSize: '10px',
                letterSpacing: '0.2em',
                cursor: 'pointer',
                textTransform: 'uppercase',
                transition: 'all 0.2s',
              }}
            >
              {d}
            </button>
          );
        })}
      </div>

      <textarea
        value={intencion}
        onChange={(e) => setIntencion(e.target.value)}
        placeholder="Escribe tu intención con claridad y precisión..."
        rows={4}
        style={{
          background: 'rgba(245,241,232,0.04)',
          border: '1px solid rgba(200,157,92,0.2)',
          borderRadius: '2px',
          color: 'rgba(245,241,232,0.85)',
          fontFamily: 'var(--font-term)',
          fontSize: '13px',
          padding: '0.75rem',
          resize: 'vertical',
          outline: 'none',
          lineHeight: 1.6,
        }}
      />

      <RitualButton
        onClick={manifestar}
        loading={loading}
        accent="#c89d5c"
        label="Declarar"
        disabled={!intencion.trim()}
      />

      {respuesta && <ResponseBlock text={respuesta} accent="#c89d5c" />}
    </div>
  );
}

// ── Panel: Sigilo ────────────────────────────────────────────────────────────

interface SigiloData {
  id?: number;
  intencion?: string;
  imagen?: string;
  letras?: string;
  estado?: string;
}

function PanelSigilo() {
  const [intencion, setIntencion] = useState('');
  const [sigilo, setSigilo] = useState<SigiloData | null>(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState('');

  const crear = useCallback(async () => {
    if (!intencion.trim()) return;
    setLoading(true);
    setMsg('');
    try {
      const data = await apiClient.post<{ letras?: string; glifo?: string; imagen?: string; id?: number; error?: string }>(
        '/api/capa1/sigilo/dibujar',
        { intencion: intencion.trim() }
      );
      if (data.error) { setMsg(data.error); return; }
      setSigilo({ intencion: intencion.trim(), imagen: data.glifo ?? data.imagen, letras: data.letras, id: data.id });
      setIntencion('');
    } catch (e) {
      setMsg('[Error al crear sigilo]');
    } finally {
      setLoading(false);
    }
  }, [intencion]);

  const cargar = useCallback(async () => {
    if (!sigilo?.id) return;
    setLoading(true);
    try {
      await apiClient.post(`/api/capa1/sigilo/${sigilo.id}/cargar`, {});
      setSigilo((s) => s ? { ...s, estado: 'cargado' } : s);
      setMsg('Sigilo cargado. El universo ha recibido la carga.');
    } catch {
      setMsg('[Error al cargar]');
    } finally {
      setLoading(false);
    }
  }, [sigilo]);

  return (
    <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', height: '100%', overflowY: 'auto' }}>
      <SectionTitle symbol="✦" color="#9878cc" label="Sigilización" />

      <textarea
        value={intencion}
        onChange={(e) => setIntencion(e.target.value)}
        placeholder="Intención en frase afirmativa: «Mi voluntad se manifiesta...»"
        rows={3}
        style={textareaStyle('#9878cc')}
      />

      <RitualButton onClick={crear} loading={loading} accent="#9878cc" label="Crear Sigilo" disabled={!intencion.trim()} />

      {sigilo && (
        <div style={{ border: '1px solid #9878cc30', borderRadius: '2px', padding: '1rem', background: 'rgba(152,120,204,0.06)' }}>
          <div style={{ color: 'rgba(245,241,232,0.5)', fontSize: '10px', letterSpacing: '0.2em', marginBottom: '0.5rem' }}>LETRAS CARROLL</div>
          <div style={{ color: '#9878cc', fontFamily: 'var(--font-display)', letterSpacing: '0.3em', fontSize: '18px', marginBottom: '1rem' }}>
            {sigilo.letras}
          </div>
          {sigilo.imagen && (
            <pre style={{ color: '#9878cc99', fontSize: '11px', fontFamily: 'var(--font-term)', margin: '0 0 1rem 0', lineHeight: 1.4 }}>
              {sigilo.imagen}
            </pre>
          )}
          {sigilo.estado !== 'cargado' && (
            <RitualButton onClick={cargar} loading={loading} accent="#9878cc" label="Cargar Sigilo" disabled={false} />
          )}
          {sigilo.estado === 'cargado' && (
            <div style={{ color: '#9878cc', fontSize: '11px', letterSpacing: '0.2em' }}>✦ CARGADO — olvida la intención ✦</div>
          )}
        </div>
      )}

      {msg && <ResponseBlock text={msg} accent="#9878cc" />}
    </div>
  );
}

// ── Panel: Limpia ────────────────────────────────────────────────────────────

type Tradicion = 'saminchakuy' | 'curanderismo';

function PanelLimpia() {
  const [tradicion, setTradicion] = useState<Tradicion>('saminchakuy');
  const [estado, setEstado] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [loading, setLoading] = useState(false);

  const guiar = useCallback(async () => {
    if (!estado.trim()) return;
    setLoading(true);
    setRespuesta('');
    try {
      const prompt = `Necesito una limpia. Tradición: ${tradicion}. Lo que cargo: ${estado.trim()}`;
      const data = await apiClient.post<{ respuesta?: string; error?: string }>(
        '/api/consultar',
        { mensaje: prompt }
      );
      setRespuesta(data.respuesta ?? data.error ?? 'Sin respuesta');
    } catch {
      setRespuesta('[Error al consultar]');
    } finally {
      setLoading(false);
    }
  }, [tradicion, estado]);

  return (
    <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', height: '100%', overflowY: 'auto' }}>
      <SectionTitle symbol="◌" color="#5cb8c8" label="Ritual de Limpia" />

      <div style={{ display: 'flex', gap: '0.5rem' }}>
        {(['saminchakuy', 'curanderismo'] as Tradicion[]).map((t) => (
          <button
            key={t}
            onClick={() => setTradicion(t)}
            style={tabPillStyle(tradicion === t, '#5cb8c8')}
          >
            {t}
          </button>
        ))}
      </div>

      <div style={{ color: 'rgba(245,241,232,0.35)', fontSize: '11px', fontFamily: 'var(--font-term)', lineHeight: 1.5 }}>
        {tradicion === 'saminchakuy'
          ? 'Transmisión de sami andino — luz por coronilla, hucha hacia la Pachamama.'
          : 'Barrida energética con vegetales o huevo — extracción de lo denso.'}
      </div>

      <textarea
        value={estado}
        onChange={(e) => setEstado(e.target.value)}
        placeholder="¿Qué arrastras? ¿Qué necesita ser limpiado?"
        rows={4}
        style={textareaStyle('#5cb8c8')}
      />

      <RitualButton onClick={guiar} loading={loading} accent="#5cb8c8" label="Iniciar Limpia" disabled={!estado.trim()} />

      {respuesta && <ResponseBlock text={respuesta} accent="#5cb8c8" />}
    </div>
  );
}

// ── Panel: Ayni ──────────────────────────────────────────────────────────────

interface AyniResumen {
  balance: number;
  n_deudas_abiertas: number;
  notable: boolean;
  deudas: Array<{ id: number; tipo_origen: string; descripcion: string; peso: number; created_at: string }>;
  ofrendas_recientes: Array<{ tipo: string; descripcion: string; created_at: string }>;
}

const TIPOS_OFRENDA = ['agua', 'tierra', 'fuego', 'aire', 'acto', 'tiempo', 'creacion', 'silencio'] as const;

function PanelAyni() {
  const [resumen, setResumen] = useState<AyniResumen | null>(null);
  const [loadingData, setLoadingData] = useState(false);
  const [tipo, setTipo] = useState<string>(TIPOS_OFRENDA[0]);
  const [descripcion, setDescripcion] = useState('');
  const [deudaId, setDeudaId] = useState<number | null>(null);
  const [msg, setMsg] = useState('');
  const [loadingPost, setLoadingPost] = useState(false);

  const cargar = useCallback(async () => {
    setLoadingData(true);
    try {
      const data = await apiClient.get<AyniResumen>('/api/ayni/resumen');
      setResumen(data);
    } catch {
      setMsg('[Error al cargar ayni]');
    } finally {
      setLoadingData(false);
    }
  }, []);

  const ofrendar = useCallback(async () => {
    if (!descripcion.trim()) return;
    setLoadingPost(true);
    setMsg('');
    try {
      await apiClient.post('/api/ayni/ofrenda', { tipo, descripcion: descripcion.trim(), deuda_id: deudaId });
      setDescripcion('');
      setDeudaId(null);
      setMsg('Ofrenda registrada. El ciclo se equilibra.');
      cargar();
    } catch {
      setMsg('[Error al ofrendar]');
    } finally {
      setLoadingPost(false);
    }
  }, [tipo, descripcion, deudaId, cargar]);

  React.useEffect(() => { cargar(); }, [cargar]);

  const balanceColor = !resumen ? '#c89d5c'
    : resumen.balance > 3 ? '#7aba5a'
    : resumen.balance >= 0 ? '#c89d5c'
    : resumen.balance >= -3 ? '#e0a060'
    : '#c05070';

  return (
    <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', height: '100%', overflowY: 'auto' }}>
      <SectionTitle symbol="⊕" color="#7aba5a" label="Ayni — Reciprocidad" />

      {loadingData && <div style={{ color: 'rgba(245,241,232,0.3)', fontSize: '11px' }}>Cargando balance...</div>}

      {resumen && (
        <div style={{ border: `1px solid ${balanceColor}30`, borderRadius: '2px', padding: '1rem', background: `${balanceColor}08` }}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.75rem', marginBottom: '0.5rem' }}>
            <span style={{ color: balanceColor, fontSize: '28px', fontFamily: 'var(--font-display)', fontWeight: 'bold' }}>
              {resumen.balance > 0 ? '+' : ''}{resumen.balance}
            </span>
            <span style={{ color: 'rgba(245,241,232,0.4)', fontSize: '10px', letterSpacing: '0.2em' }}>
              BALANCE · {resumen.n_deudas_abiertas} deuda{resumen.n_deudas_abiertas !== 1 ? 's' : ''} abierta{resumen.n_deudas_abiertas !== 1 ? 's' : ''}
            </span>
          </div>
          {resumen.notable && (
            <div style={{ color: '#c05070', fontSize: '11px', fontFamily: 'var(--font-term)' }}>
              ⚠ Deuda notable — las entidades lo perciben
            </div>
          )}
        </div>
      )}

      {resumen && resumen.deudas.length > 0 && (
        <div>
          <div style={{ color: 'rgba(245,241,232,0.3)', fontSize: '9px', letterSpacing: '0.25em', marginBottom: '0.5rem' }}>
            DEUDAS ABIERTAS
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
            {resumen.deudas.map((d) => (
              <button
                key={d.id}
                onClick={() => setDeudaId(deudaId === d.id ? null : d.id)}
                style={{
                  textAlign: 'left',
                  padding: '0.5rem 0.75rem',
                  background: deudaId === d.id ? 'rgba(122,186,90,0.1)' : 'rgba(245,241,232,0.02)',
                  border: `1px solid ${deudaId === d.id ? '#7aba5a40' : 'rgba(245,241,232,0.08)'}`,
                  borderRadius: '2px',
                  cursor: 'pointer',
                  color: 'rgba(245,241,232,0.7)',
                  fontSize: '11px',
                  fontFamily: 'var(--font-term)',
                }}
              >
                <span style={{ color: '#c89d5c', marginRight: '0.5rem', fontSize: '9px' }}>[{d.tipo_origen} ·{d.peso}]</span>
                {d.descripcion}
              </button>
            ))}
          </div>
          {deudaId && (
            <div style={{ color: 'rgba(122,186,90,0.6)', fontSize: '10px', marginTop: '0.25rem', fontFamily: 'var(--font-term)' }}>
              Ofrenda para cerrar deuda #{deudaId}
            </div>
          )}
        </div>
      )}

      <div>
        <div style={{ color: 'rgba(245,241,232,0.3)', fontSize: '9px', letterSpacing: '0.25em', marginBottom: '0.5rem' }}>
          REGISTRAR OFRENDA
        </div>
        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginBottom: '0.75rem' }}>
          {TIPOS_OFRENDA.map((t) => (
            <button key={t} onClick={() => setTipo(t)} style={tabPillStyle(tipo === t, '#7aba5a')}>
              {t}
            </button>
          ))}
        </div>
        <textarea
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
          placeholder="Describe tu ofrenda con intención..."
          rows={3}
          style={textareaStyle('#7aba5a')}
        />
        <div style={{ marginTop: '0.75rem' }}>
          <RitualButton onClick={ofrendar} loading={loadingPost} accent="#7aba5a" label="Ofrendar" disabled={!descripcion.trim()} />
        </div>
      </div>

      {msg && <ResponseBlock text={msg} accent="#7aba5a" />}
    </div>
  );
}

// ── Helpers compartidos ──────────────────────────────────────────────────────

function SectionTitle({ symbol, color, label }: { symbol: string; color: string; label: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
      <span style={{ color, fontSize: '14px' }}>{symbol}</span>
      <span style={{ fontFamily: 'var(--font-display)', fontSize: '10px', letterSpacing: '0.3em', color: `${color}99`, textTransform: 'uppercase' }}>
        {label}
      </span>
    </div>
  );
}

function RitualButton({ onClick, loading, accent, label, disabled }: {
  onClick: () => void; loading: boolean; accent: string; label: string; disabled: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      style={{
        padding: '0.6rem 1.5rem',
        background: 'transparent',
        border: `1px solid ${disabled || loading ? 'rgba(245,241,232,0.1)' : accent}`,
        borderRadius: '2px',
        color: disabled || loading ? 'rgba(245,241,232,0.25)' : accent,
        fontFamily: 'var(--font-display)',
        fontSize: '10px',
        letterSpacing: '0.3em',
        textTransform: 'uppercase',
        cursor: disabled || loading ? 'not-allowed' : 'pointer',
        transition: 'all 0.2s',
        alignSelf: 'flex-start',
      }}
    >
      {loading ? '▌ procesando...' : label}
    </button>
  );
}

function ResponseBlock({ text, accent }: { text: string; accent: string }) {
  return (
    <div style={{
      borderLeft: `2px solid ${accent}60`,
      paddingLeft: '0.75rem',
      color: 'rgba(245,241,232,0.8)',
      fontFamily: 'var(--font-term)',
      fontSize: '13px',
      lineHeight: 1.7,
      whiteSpace: 'pre-wrap',
    }}>
      {text}
    </div>
  );
}

function textareaStyle(accent: string): React.CSSProperties {
  return {
    background: 'rgba(245,241,232,0.03)',
    border: `1px solid ${accent}30`,
    borderRadius: '2px',
    color: 'rgba(245,241,232,0.85)',
    fontFamily: 'var(--font-term)',
    fontSize: '13px',
    padding: '0.75rem',
    resize: 'vertical',
    outline: 'none',
    lineHeight: 1.6,
    width: '100%',
  };
}

function tabPillStyle(active: boolean, accent: string): React.CSSProperties {
  return {
    padding: '0.3rem 0.75rem',
    background: active ? `${accent}18` : 'transparent',
    border: `1px solid ${active ? accent : 'rgba(245,241,232,0.1)'}`,
    borderRadius: '2px',
    color: active ? accent : 'rgba(245,241,232,0.35)',
    fontFamily: 'var(--font-term)',
    fontSize: '10px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    letterSpacing: '0.05em',
  };
}

// ── Componente principal ─────────────────────────────────────────────────────

export function AltarWorkspace() {
  const [activeTab, setActiveTab] = useState<AltarTab>('terminal');

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* Sub-navegación */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0',
          borderBottom: '1px solid rgba(200,157,92,0.1)',
          background: 'rgba(6,4,2,0.6)',
          flexShrink: 0,
          paddingLeft: '1rem',
        }}
      >
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              padding: '0.65rem 1rem',
              background: 'transparent',
              border: 'none',
              borderBottom: `2px solid ${activeTab === tab.id ? tab.accent : 'transparent'}`,
              cursor: 'pointer',
              color: activeTab === tab.id ? tab.accent : 'rgba(245,241,232,0.2)',
              fontFamily: 'var(--font-display)',
              fontSize: '9px',
              letterSpacing: '0.2em',
              textTransform: 'uppercase',
              transition: 'all 0.25s',
              outline: 'none',
              marginBottom: '-1px',
            }}
          >
            <span style={{ fontSize: '11px' }}>{tab.symbol}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Contenido del tab activo */}
      <div style={{ flex: 1, overflow: 'hidden', position: 'relative' }}>
        <div style={{ position: 'absolute', inset: 0, display: activeTab === 'terminal' ? 'block' : 'none' }}>
          <Capa12Altar />
        </div>
        <div style={{ position: 'absolute', inset: 0, display: activeTab === 'manifestar' ? 'flex' : 'none', flexDirection: 'column' }}>
          <PanelManifestar />
        </div>
        <div style={{ position: 'absolute', inset: 0, display: activeTab === 'sigilo' ? 'flex' : 'none', flexDirection: 'column' }}>
          <PanelSigilo />
        </div>
        <div style={{ position: 'absolute', inset: 0, display: activeTab === 'limpia' ? 'flex' : 'none', flexDirection: 'column' }}>
          <PanelLimpia />
        </div>
        <div style={{ position: 'absolute', inset: 0, display: activeTab === 'ayni' ? 'flex' : 'none', flexDirection: 'column' }}>
          <PanelAyni />
        </div>
      </div>
    </div>
  );
}
