import { useState, useEffect } from 'react';
import type { DeityKey, Mood } from '@/app/lib/deityMoods';
import { apiClient } from '@/app/lib/apiClient';

type Modificaciones = Record<string, { estado: string; desc: string }>;

interface LunaResponse {
  fase?: { nombre: string; emoji: string; energia: string };
  signo?: { signo: string; simbolo: string; energia: string };
  marea?: { intensidad: string; direccion: string };
  modificaciones?: Modificaciones;
}

export interface LunaState {
  moods: Record<DeityKey, Mood>;
  faseNombre: string;
  faseEmoji: string;
  faseEnergia: string;
  signoNombre: string;
  signoSimbolo: string;
  mareaIntensidad: string;
  mareaDireccion: string;
  isLoading: boolean;
}

const DEFAULT_MOODS: Record<DeityKey, Mood> = {
  lilith: 'neutral',
  artemisa: 'neutral',
  afrodita: 'neutral',
  isis: 'neutral',
};

const MOODS_VALIDOS: readonly Mood[] = ['amplificada', 'neutral', 'reposo'];

function normalizarMood(estado: string | undefined): Mood {
  return MOODS_VALIDOS.includes(estado as Mood) ? (estado as Mood) : 'neutral';
}

function extraerMoods(mods: Modificaciones | undefined): Record<DeityKey, Mood> {
  if (!mods) return DEFAULT_MOODS;
  return {
    lilith: normalizarMood(mods.lilith?.estado),
    artemisa: normalizarMood(mods.artemisa?.estado),
    afrodita: normalizarMood(mods.afrodita?.estado),
    isis: normalizarMood(mods.isis?.estado),
  };
}

const DEFAULT_STATE: LunaState = {
  moods: DEFAULT_MOODS,
  faseNombre: '',
  faseEmoji: '🌙',
  faseEnergia: '',
  signoNombre: '',
  signoSimbolo: '',
  mareaIntensidad: '',
  mareaDireccion: '',
  isLoading: true,
};

/**
 * Trae el estado del cielo de hoy: fase lunar, signo, marea y ánimo de cada
 * deidad. Se actualiza solo al montar — el cielo cambia despacio.
 */
export function useLunaState(): LunaState {
  const [state, setState] = useState<LunaState>(DEFAULT_STATE);

  useEffect(() => {
    const controller = new AbortController();

    async function cargar() {
      try {
        const data = await apiClient.get<LunaResponse>('/api/luna', controller.signal);
        setState({
          moods: extraerMoods(data.modificaciones),
          faseNombre: data.fase?.nombre ?? '',
          faseEmoji: data.fase?.emoji ?? '🌙',
          faseEnergia: data.fase?.energia ?? '',
          signoNombre: data.signo?.signo ?? '',
          signoSimbolo: data.signo?.simbolo ?? '',
          mareaIntensidad: data.marea?.intensidad ?? '',
          mareaDireccion: data.marea?.direccion ?? '',
          isLoading: false,
        });
      } catch (err) {
        if (err instanceof DOMException && err.name === 'AbortError') return;
        setState((prev) => ({ ...prev, isLoading: false }));
      }
    }

    cargar();
    return () => controller.abort();
  }, []);

  return state;
}
