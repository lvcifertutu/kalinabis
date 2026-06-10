import { useState, useCallback, useEffect } from 'react';
import { apiClient } from '@/app/lib/apiClient';

// ── Tipos (alineados con las respuestas reales del backend) ────────────────

export interface Esfera {
  id: number;
  tipo: string;
  clave: string;
  amplitud: number;
  fase?: string;
  created_at: string;
}

export interface Semilla {
  id: number;
  intencion: string;
  estado: string;
  esfera_id?: number;
  created_at: string;
}

export interface Sincronicidad {
  id: number;
  descripcion: string;
  categoria: string;
  fase_lunar: string;
  confirmada: boolean;
  created_at: string;
}

export interface Micorriza {
  id: number;
  otro_mago: string;
  ritual: string;
  created_at: string;
}

interface Capa3Data {
  esferas: Esfera[];
  semillas: Semilla[];
  sincros: Sincronicidad[];
  micorrizas: Micorriza[];
}

const EMPTY_DATA: Capa3Data = {
  esferas: [],
  semillas: [],
  sincros: [],
  micorrizas: [],
};

export function useCapa3API() {
  const [data, setData] = useState<Capa3Data>(EMPTY_DATA);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const cargar = useCallback(async (signal?: AbortSignal) => {
    setIsLoading(true);
    setError(null);

    try {
      const [esferasJson, semillasJson, sincrosJson, micoJson] = await Promise.all([
        apiClient.get<{ esferas: Esfera[] }>('/api/capa3/esferas', signal),
        apiClient.get<{ semillas: Semilla[] }>('/api/capa3/semillas', signal),
        apiClient.get<{ sincronicidades: Sincronicidad[] }>('/api/capa3/sync', signal),
        apiClient.get<{ conexiones: Micorriza[] }>('/api/capa3/micorriza', signal),
      ]);

      setData({
        esferas: esferasJson.esferas || [],
        semillas: semillasJson.semillas || [],
        sincros: sincrosJson.sincronicidades || [],
        micorrizas: micoJson.conexiones || [],
      });
    } catch (err) {
      if (err instanceof DOMException && err.name === 'AbortError') return;
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    cargar(controller.signal);
    return () => controller.abort();
  }, [cargar]);

  // ── Mutaciones ───────────────────────────────────────────────────────────

  const registrarSync = useCallback(
    async (descripcion: string, categoria: string) => {
      await apiClient.post('/api/capa3/sync/registrar', { descripcion, categoria });
      // Re-cargar para reflejar el nuevo estado del colectivo.
      await cargar();
    },
    [cargar]
  );

  const confirmarSync = useCallback(
    async (syncId: number) => {
      const json = await apiClient.post<{ sincronicidad?: Sincronicidad }>(
        '/api/capa3/sync/confirmar',
        { sync_id: syncId }
      );
      const actualizada = json.sincronicidad;
      if (actualizada) {
        setData((prev) => ({
          ...prev,
          sincros: prev.sincros.map((s) => (s.id === syncId ? actualizada : s)),
        }));
      }
    },
    []
  );

  return {
    data,
    isLoading,
    error,
    recargar: cargar,
    registrarSync,
    confirmarSync,
  };
}
