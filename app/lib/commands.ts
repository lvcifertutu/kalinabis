// ── Comandos slash disponibles en la terminal de Tutu ───────────────────────
// Lista canónica para autocompletado. Mantener en sync con _procesar_comando
// (servidor.py) y useKalinabisBackend (atajos del front).

export interface SlashCommand {
  cmd: string;
  hint: string;
}

export const SLASH_COMMANDS: SlashCommand[] = [
  { cmd: '/ayuda', hint: 'Lista de comandos' },
  { cmd: '/manifestar', hint: 'Manifiesta una diosa — /manifestar lilith' },
  { cmd: '/generar', hint: 'Regenera el sprite de una diosa' },
  { cmd: '/runas', hint: 'Tirada de runas (3 o 9)' },
  { cmd: '/gnosis', hint: 'Métodos de gnosis' },
];

/**
 * Sugerencias para el texto actual. Solo cuando empieza con '/' y aún no hay
 * espacio (estás escribiendo el comando, no sus argumentos).
 */
export function autocompletar(texto: string): SlashCommand[] {
  if (!texto.startsWith('/') || texto.includes(' ')) return [];
  const q = texto.toLowerCase();
  return SLASH_COMMANDS.filter((c) => c.cmd.startsWith(q) && c.cmd !== texto);
}
