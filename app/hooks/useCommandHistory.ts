import { useState, useCallback, useRef } from 'react';

const MAX_HISTORY = 50;

/**
 * Historial de comandos estilo terminal: recuerda lo enviado y permite
 * recorrerlo con ↑/↓. `draft` guarda lo que el usuario escribía antes de
 * empezar a navegar el historial, para restaurarlo al volver al final.
 */
export function useCommandHistory() {
  const [history, setHistory] = useState<string[]>([]);
  // -1 = no navegando (en el input actual). 0..n-1 = posición en el historial.
  const cursor = useRef<number>(-1);
  const draft = useRef<string>('');

  const push = useCallback((command: string) => {
    const trimmed = command.trim();
    if (!trimmed) return;
    setHistory((prev) => {
      // Evitar duplicado consecutivo.
      if (prev[prev.length - 1] === trimmed) return prev;
      const next = [...prev, trimmed];
      return next.length > MAX_HISTORY ? next.slice(-MAX_HISTORY) : next;
    });
    cursor.current = -1;
    draft.current = '';
  }, []);

  /** Devuelve el comando anterior (↑), o null si no hay más. */
  const previous = useCallback(
    (currentInput: string): string | null => {
      if (history.length === 0) return null;
      if (cursor.current === -1) {
        draft.current = currentInput;
        cursor.current = history.length - 1;
      } else if (cursor.current > 0) {
        cursor.current -= 1;
      }
      return history[cursor.current];
    },
    [history]
  );

  /** Devuelve el comando siguiente (↓), o el draft al llegar al final. */
  const next = useCallback((): string | null => {
    if (cursor.current === -1) return null;
    if (cursor.current < history.length - 1) {
      cursor.current += 1;
      return history[cursor.current];
    }
    // Llegamos al final → restaurar lo que se estaba escribiendo.
    cursor.current = -1;
    return draft.current;
  }, [history]);

  const reset = useCallback(() => {
    cursor.current = -1;
    draft.current = '';
  }, []);

  return { push, previous, next, reset };
}
