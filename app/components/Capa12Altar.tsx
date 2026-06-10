'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { DeityAltar } from './DeityAltar';
import { useKalinabisBackend } from '@/app/hooks/useKalinabisBackend';
import { useLunaState } from '@/app/hooks/useLunaState';
import { useCommandHistory } from '@/app/hooks/useCommandHistory';
import { DEITIES, type DeityKey } from '@/app/lib/deityMoods';
import { autocompletar, type SlashCommand } from '@/app/lib/commands';

type Entry =
  | { kind: 'you'; content: string }
  | { kind: 'tutu'; content: string }
  | { kind: 'deity'; deity: DeityKey; content: string }
  | { kind: 'output'; content: string }
  | { kind: 'system'; content: string };

const SALUDO_INICIAL_DIOSA = 'Bienvenido al altar. He estado esperando.';

// Tutu no es una diosa: es el asistente de la terminal. Color ámbar estable,
// distinto de los neones de las diosas, para marcar que es otro espacio.
const TUTU_COLOR = '#ffa94d';

function esDiosa(entidad: string | null): entidad is DeityKey {
  return entidad !== null && entidad !== 'tutu' && entidad in DEITIES;
}

export function Capa12Altar() {
  const [currentDeity, setCurrentDeity] = useState<DeityKey>('lilith');
  const [entries, setEntries] = useState<Entry[]>([
    { kind: 'system', content: '✦ KALINABIS INITIALIZED ✦' },
    {
      kind: 'tutu',
      content:
        'Soy Tutu, tu intermediario. Hablá conmigo aquí en la terminal; ' +
        'cuando una diosa deba responder, lo hará en su propio altar.\n\n' +
        'Comandos: /ayuda | /manifestar <diosa> | /generar <diosa>',
    },
  ]);
  // Lo que la diosa actual dice en su propio espacio (panel izquierdo).
  const [deitySpeech, setDeitySpeech] = useState<string>(SALUDO_INICIAL_DIOSA);
  const [input, setInput] = useState('');

  const { executeCommand, isLoading } = useKalinabisBackend();
  const astral = useLunaState();
  const cmdHistory = useCommandHistory();

  const sugerencias = autocompletar(input);

  const theme = DEITIES[currentDeity];
  const mood = astral.moods[currentDeity];
  const streamRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (streamRef.current) {
      streamRef.current.scrollTop = streamRef.current.scrollHeight;
    }
  }, [entries, isLoading]);

  const handleSubmit = useCallback(async () => {
    const texto = input.trim();
    if (!texto) return;

    cmdHistory.push(texto);
    setEntries((prev) => [...prev, { kind: 'you', content: texto }]);
    setInput('');

    const { entidad, texto: respuesta } = await executeCommand(texto);

    if (esDiosa(entidad)) {
      // La diosa habla en su propio altar; la terminal solo lo señala.
      setCurrentDeity(entidad);
      setDeitySpeech(respuesta);
      setEntries((prev) => [
        ...prev,
        { kind: 'system', content: `✦ ${entidad.toUpperCase()} habla en su altar ✦` },
      ]);
    } else {
      // Tutu (asistente) responde → detectar si menciona una diosa para manifestarla.
      setEntries((prev) => [
        ...prev,
        entidad === 'tutu'
          ? { kind: 'tutu', content: respuesta }
          : { kind: 'output', content: respuesta },
      ]);

      // Auto-manifestar diosa si Tutu la menciona.
      if (entidad === 'tutu') {
        const diosasKeys = Object.keys(DEITIES) as DeityKey[];
        for (const diosa of diosasKeys) {
          if (respuesta.toLowerCase().includes(diosa)) {
            setCurrentDeity(diosa);
            break;
          }
        }
      }
    }
  }, [input, executeCommand, cmdHistory]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'ArrowUp') {
        const prev = cmdHistory.previous(input);
        if (prev !== null) {
          e.preventDefault();
          setInput(prev);
        }
      } else if (e.key === 'ArrowDown') {
        const next = cmdHistory.next();
        if (next !== null) {
          e.preventDefault();
          setInput(next);
        }
      } else if (e.key === 'Tab' && sugerencias.length > 0) {
        // Tab completa con la primera sugerencia.
        e.preventDefault();
        setInput(sugerencias[0].cmd + ' ');
      }
    },
    [input, cmdHistory, sugerencias]
  );

  const aplicarSugerencia = useCallback((cmd: SlashCommand) => {
    setInput(cmd.cmd + ' ');
  }, []);

  return (
    <div className="w-full h-full flex flex-col gap-4 p-4">
      {/* Header */}
      <div
        className="h-12 px-4 flex items-center justify-between border-b-2 rounded"
        style={{ borderColor: theme.color }}
      >
        <div className="flex items-center gap-3">
          <div
            className="w-3 h-3 rounded-full animate-pulse"
            style={{ backgroundColor: theme.color }}
          />
          <h1 className="text-lg font-bold font-mono" style={{ color: theme.color }}>
            EL ALTAR
          </h1>
        </div>
        <span className="text-gray-500 text-xs font-mono">{currentDeity.toUpperCase()}</span>
      </div>

      {/* Main content */}
      <div className="flex-1 flex gap-4 overflow-hidden">
        {/* Altar de la deidad — Izquierda */}
        <div
          className="w-1/3 flex flex-col items-center justify-start overflow-y-auto bg-black/80 border-2 rounded-lg p-4"
          style={{ borderColor: theme.color, boxShadow: `0 0 15px ${theme.color}40` }}
        >
          <DeityAltar
            deity={currentDeity}
            mood={mood}
            astral={astral}
            speech={deitySpeech}
            isSpeaking={isLoading}
          />
        </div>

        {/* Terminal de Tutu — Derecha */}
        <div
          className="flex-1 flex flex-col bg-black/80 border-2 rounded-lg p-4 font-mono text-sm relative"
          style={{ borderColor: TUTU_COLOR, boxShadow: `0 0 10px ${TUTU_COLOR}40` }}
        >
          {/* Header del stream */}
          <div
            className="flex items-center justify-between pb-3 mb-3 border-b"
            style={{ borderColor: TUTU_COLOR }}
          >
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: TUTU_COLOR }} />
              <span style={{ color: TUTU_COLOR }}>KALINABIS · TUTU</span>
            </div>
            <span className="text-gray-500 text-xs">v2.0</span>
          </div>

          {/* Stream */}
          <div ref={streamRef} className="flex-1 overflow-y-auto mb-3 space-y-2 pr-2">
            {entries.map((entry, i) => (
              <ConversationEntry key={i} entry={entry} />
            ))}
            {isLoading && (
              <div style={{ color: TUTU_COLOR }} className="animate-pulse text-xs">
                ▌ procesando...
              </div>
            )}
          </div>

          {/* Autocompletado de slash commands */}
          {sugerencias.length > 0 && (
            <div
              className="mb-2 rounded border overflow-hidden"
              style={{ borderColor: `${TUTU_COLOR}60` }}
            >
              {sugerencias.map((s, i) => (
                <button
                  key={s.cmd}
                  type="button"
                  onClick={() => aplicarSugerencia(s)}
                  className="w-full flex items-center justify-between px-3 py-1.5 text-xs hover:bg-white/5 transition-colors"
                >
                  <span style={{ color: TUTU_COLOR }} className="font-mono">
                    {s.cmd}
                  </span>
                  <span className="text-gray-500 text-[10px]">
                    {i === 0 ? 'Tab · ' : ''}{s.hint}
                  </span>
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
            className="flex items-center border-t pt-3"
            style={{ borderColor: TUTU_COLOR }}
          >
            <span style={{ color: TUTU_COLOR }}>{'>'}</span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Habla con Tutu · /ayuda · ↑↓ historial · Tab completa"
              className="flex-1 ml-2 bg-transparent text-gray-100 placeholder-gray-600 outline-none"
              style={{ caretColor: TUTU_COLOR }}
            />
            {input && (
              <span className="animate-pulse ml-2" style={{ color: TUTU_COLOR }}>
                ▌
              </span>
            )}
          </form>

          {/* Scanlines */}
          <div
            className="pointer-events-none absolute inset-0 rounded-lg opacity-5"
            style={{
              backgroundImage:
                'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px)',
            }}
          />
        </div>
      </div>
    </div>
  );
}

function ConversationEntry({ entry }: { entry: Entry }) {
  if (entry.kind === 'you') {
    return (
      <div className="break-words">
        <span className="text-gray-500">{'> '}</span>
        <span className="text-gray-300">{entry.content}</span>
      </div>
    );
  }

  if (entry.kind === 'tutu') {
    return (
      <div className="break-words">
        <div style={{ color: TUTU_COLOR }} className="text-xs font-bold mb-1">
          TUTU:
        </div>
        <div
          className="text-xs text-gray-300 pl-3 border-l-2 leading-relaxed whitespace-pre-wrap"
          style={{ borderColor: TUTU_COLOR }}
        >
          {entry.content}
        </div>
      </div>
    );
  }

  if (entry.kind === 'deity') {
    const deityTheme = DEITIES[entry.deity];
    return (
      <div className="break-words">
        <div style={{ color: deityTheme.color }} className="text-xs font-bold mb-1">
          {entry.deity.toUpperCase()}:
        </div>
        <div
          className="text-xs text-gray-300 pl-3 border-l-2 leading-relaxed"
          style={{ borderColor: deityTheme.color }}
        >
          {entry.content}
        </div>
      </div>
    );
  }

  if (entry.kind === 'output') {
    return (
      <span className="text-gray-300 block whitespace-pre-wrap break-words">
        {entry.content}
      </span>
    );
  }

  return <div className="text-xs text-gray-500 opacity-75">{entry.content}</div>;
}
