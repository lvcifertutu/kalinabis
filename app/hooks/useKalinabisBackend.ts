import { useState, useCallback } from 'react';
import { apiClient } from '@/app/lib/apiClient';

interface RunasResponse {
  success: boolean;
  data?: {
    runas: Array<{
      nombre: string;
      significado: string;
      posicion: string;
    }>;
    interpretacion: string;
  };
  error?: string;
}

interface GnosisResponse {
  success: boolean;
  data?: {
    metodo: string;
    descripcion: string;
    pasos: string[];
    duracion: string;
  };
  error?: string;
}

interface ConsultarResponse {
  success: boolean;
  data?: {
    respuesta: string;
    deidad?: string;
  };
  error?: string;
}

/**
 * Resultado de una ejecución. `entidad` dice QUIÉN habla, para que la UI
 * enrute el texto al lugar correcto:
 *   - null  → salida de comando o error → terminal (Tutu)
 *   - 'tutu'→ el asistente responde en la terminal
 *   - diosa → su texto va a su propio altar/panel
 */
export interface ExecResult {
  entidad: string | null;
  texto: string;
  presentacion?: string;
}

export function useKalinabisBackend() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const executeCommand = useCallback(
    async (command: string): Promise<ExecResult> => {
      setIsLoading(true);
      setError(null);

      try {
        const [cmd, ...args] = command.trim().split(' ');
        const actualCmd = cmd.startsWith('/') ? cmd.slice(1) : cmd;
        const argument = args.join(' ');

        if (actualCmd === 'runas' || actualCmd === 'runa') {
          const count = parseInt(argument) === 9 ? 9 : 3;

          const data = await apiClient.get<RunasResponse>(`/api/runas/tirada?cantidad=${count}`);

          if (data.success && data.data) {
            return { entidad: null, texto: formatRunasResponse(data.data) };
          }
          throw new Error(data.error || 'Error en runas');
        }

        if (actualCmd === 'gnosis') {
          const data = await apiClient.get<GnosisResponse>('/api/gnosis/metodos');

          if (data.success && data.data) {
            return { entidad: null, texto: formatGnosisResponse(data.data) };
          }
          throw new Error(data.error || 'Error en gnosis');
        }

        if (actualCmd === 'ayuda') {
          return { entidad: null, texto: formatHelpResponse() };
        }

        // Default: consultar. El backend decide quién responde (Tutu o diosa).
        const data = await apiClient.post<ConsultarResponse & { respuesta?: string; entidad?: string; presentacion?: string }>(
          '/api/consultar',
          { mensaje: command }
        );

        if (data.respuesta) {
          return {
            entidad: data.entidad ?? 'tutu',
            texto: data.respuesta,
            presentacion: data.presentacion || undefined,
          };
        }
        throw new Error(data.error || 'Error en consulta');
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Error desconocido';
        setError(message);
        return { entidad: null, texto: `[ERROR] ${message}` };
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  return { executeCommand, isLoading, error };
}

function formatRunasResponse(data: any): string {
  let result = '╔════════════════════════════════╗\n';
  result += '║          TIRADA DE RUNAS        ║\n';
  result += '╚════════════════════════════════╝\n\n';

  data.runas.forEach((runa: any, i: number) => {
    result += `${i + 1}. ${runa.nombre} [${runa.posicion}]\n`;
    result += `   ${runa.significado}\n\n`;
  });

  result += '─── INTERPRETACIÓN ───\n';
  result += data.interpretacion;

  return result;
}

function formatGnosisResponse(data: any): string {
  let result = '╔════════════════════════════════╗\n';
  result += '║      MÉTODO DE GNOSIS          ║\n';
  result += '╚════════════════════════════════╝\n\n';

  result += `${data.metodo.toUpperCase()}\n`;
  result += `Duración: ${data.duracion}\n\n`;
  result += `${data.descripcion}\n\n`;

  result += 'Pasos:\n';
  data.pasos.forEach((paso: string, i: number) => {
    result += `${i + 1}. ${paso}\n`;
  });

  return result;
}

function formatHelpResponse(): string {
  return `╔════════════════════════════════╗
║      COMANDOS DISPONIBLES      ║
╚════════════════════════════════╝

ORÁCULOS:
  /runas [pregunta]     - Tirada 3 runas
  /runas 9 [pregunta]   - Tirada Valknut 9 runas
  /iching [pregunta]    - I Ching, 64 hexagramas
  /geo [pregunta]       - Geomancia, Escudo 12 Casas

GNOSIS:
  /gnosis               - Métodos de gnosis
  /tarot [pregunta]     - Lectura con deidad

MAGIA:
  /servitor crear       - Crear thoughtform
  /sigilo               - Sigilización
  /bosque               - El Bosque colectivo

ESTADO:
  /luna                 - Fase lunar
  /sync                 - Sincronicidades
  /ayuda                - Este mensaje`;
}
