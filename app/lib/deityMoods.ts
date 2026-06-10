// ── Estados de ánimo de las deidades ────────────────────────────────────────
// El ánimo lo decide el cielo (luna + astros + día) vía /api/luna →
// luna_hoy().modificaciones. Cada deidad puede estar amplificada, neutral o en
// reposo. Aquí mapeamos cada estado a un tratamiento visual (color, glow,
// animación, expresión) para que el retrato cambie según el ánimo.

export type DeityKey = 'lilith' | 'artemisa' | 'afrodita' | 'isis';
export type Mood = 'amplificada' | 'neutral' | 'reposo';

export interface DeityTheme {
  name: string;
  /** Color base de la deidad (paleta neon). */
  color: string;
}

export const DEITIES: Record<DeityKey, DeityTheme> = {
  lilith: { name: 'lilith', color: '#00ffff' },
  artemisa: { name: 'artemisa', color: '#00ff00' },
  afrodita: { name: 'afrodita', color: '#ff00ff' },
  isis: { name: 'isis', color: '#ffff00' },
};

/** Tratamiento visual derivado del ánimo. Todo compositor-friendly. */
export interface MoodVisual {
  label: string;
  glyph: string;
  /** Multiplicador de brillo (filter: brightness). */
  brightness: number;
  /** Saturación (filter: saturate). En reposo se apaga. */
  saturate: number;
  /** Radio del glow en px. */
  glowPx: number;
  /** Animación CSS aplicada al retrato. */
  animation: string;
  /** Adorno de aura alrededor del nombre. */
  aura: string;
}

const MOOD_VISUALS: Record<Mood, MoodVisual> = {
  amplificada: {
    label: 'AMPLIFICADA',
    glyph: '▲',
    brightness: 1.4,
    saturate: 1.3,
    glowPx: 26,
    animation: 'mood-pulse 1.6s ease-in-out infinite',
    aura: '✦ ✧ ✦',
  },
  neutral: {
    label: 'NEUTRAL',
    glyph: '◆',
    brightness: 1.0,
    saturate: 1.0,
    glowPx: 12,
    animation: 'mood-breathe 4s ease-in-out infinite',
    aura: '· ◇ ·',
  },
  reposo: {
    label: 'EN REPOSO',
    glyph: '▽',
    brightness: 0.55,
    saturate: 0.4,
    glowPx: 5,
    animation: 'mood-breathe 7s ease-in-out infinite',
    aura: '·   ·',
  },
};

export function moodVisual(mood: Mood): MoodVisual {
  return MOOD_VISUALS[mood];
}

// ── Arte ASCII por deidad, con expresión que cambia según el ánimo ───────────
// La "cara" (línea de ojos) se intercambia por ánimo; el resto del cuerpo es
// estable. Así el retrato es reconocible pero su gesto refleja el estado.

interface DeityArt {
  /** Líneas antes de la cara. */
  top: string[];
  /** Línea de la cara por ánimo (gesto en reposo). */
  face: Record<Mood, string>;
  /** Cara momentánea (parpadeo/pulso) por ánimo. Mismo ancho que `face`
   *  para que el retrato no salte al animarse. */
  faceAlt: Record<Mood, string>;
  /** Líneas después de la cara (incluye el epíteto). */
  bottom: string[];
}

const DEITY_ART: Record<DeityKey, DeityArt> = {
  lilith: {
    top: ['/\\ /\\'],
    face: { amplificada: '( ◉‿◉ )', neutral: '( o.o )', reposo: '( -.- )' },
    faceAlt: { amplificada: '( ˘‿˘ )', neutral: '( -.- )', reposo: '( =.= )' },
    bottom: ['> ^ <', '/|   |\\', '(_|   |_)', 'La Sombra'],
  },
  artemisa: {
    top: ['^\\', '/ \\'],
    face: { amplificada: '/(o)\\', neutral: '/   \\', reposo: '/ ~ \\' },
    faceAlt: { amplificada: '/(-)\\', neutral: '/ - \\', reposo: '/ _ \\' },
    bottom: ['|   |', '|   |', 'La Cazadora'],
  },
  afrodita: {
    top: ['(@)', '/###\\'],
    face: { amplificada: '(###♥###)', neutral: '(#######)', reposo: '(##·##)' },
    faceAlt: { amplificada: '(###♡###)', neutral: '(###·###)', reposo: '(##°##)' },
    bottom: ['\\  ###  /', ' \\ ### /', 'El Magnetismo'],
  },
  isis: {
    top: ['_/\\_/\\_', '|  ◇  |'],
    face: { amplificada: '| ⟡⟡⟡ |', neutral: '| ⟡ ⟡ |', reposo: '|  ⟡  |' },
    faceAlt: { amplificada: '| ⟡·⟡ |', neutral: '| · · |', reposo: '|  ·  |' },
    bottom: ['|_   _|', ' / \\', 'La Sabiduría'],
  },
};

/**
 * Construye el arte ASCII de una deidad para un ánimo dado.
 * Con `alt=true` usa la cara momentánea (parpadeo/pulso) para animar el retrato.
 */
export function deityAscii(deity: DeityKey, mood: Mood, alt = false): string {
  const art = DEITY_ART[deity];
  const faceLine = alt ? art.faceAlt[mood] : art.face[mood];
  const lines = [...art.top, faceLine, ...art.bottom];
  return lines.join('\n');
}
