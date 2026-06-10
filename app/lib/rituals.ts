/**
 * Definición de rituales y variantes de manifestación para cada diosa.
 * Cada ritual tiene instrucciones, requerimientos, y efectos esperados.
 */

import type { DeityKey } from './deityMoods';

export interface Ritual {
  id: string;
  nombre: string;
  diosa: DeityKey;
  descripcion: string;
  duracion: string; // "5 min", "15 min", "1 hora", etc.
  dificultad: 'básico' | 'intermedio' | 'avanzado';
  requerimientos: string[];
  pasos: string[];
  efectos: string[];
  mejorPorMood?: ('amplificada' | 'neutral' | 'reposo')[];
}

export const RITUALES: Record<string, Ritual> = {
  // LILITH
  lilith_rebeldia: {
    id: 'lilith_rebeldia',
    nombre: 'Ritual de Rebelión Personal',
    diosa: 'lilith',
    descripcion: 'Rompe patrones limitantes y reclama tu poder personal.',
    duracion: '10 min',
    dificultad: 'básico',
    requerimientos: ['Vela negra', 'Papel y lápiz'],
    pasos: [
      '1. Enciende la vela negra mientras dices: "No sigo patrones que no elegí"',
      '2. Escribe un patrón que quieres romper',
      '3. Lee en voz alta lo que escribiste, con convicción',
      '4. Quema el papel en la llama (con seguridad)',
      '5. Cierra los ojos y siente tu libertad reclamada',
    ],
    efectos: [
      'Claridad sobre límites personales',
      'Activación de poder manifestativo',
      'Energía de determinación',
    ],
    mejorPorMood: ['amplificada'],
  },

  lilith_generativa: {
    id: 'lilith_generativa',
    nombre: 'Rito de Abundancia Generativa',
    diosa: 'lilith',
    descripcion: 'Canaliza la energía generativa para crear abundancia.',
    duracion: '20 min',
    dificultad: 'intermedio',
    requerimientos: ['Velas rojas', 'Cristales (rojo o negro)', 'Agua'],
    pasos: [
      '1. Forma un círculo con 4 velas rojas (norte, sur, este, oeste)',
      '2. Coloca cristales en el centro',
      '3. Derrama agua lentamente en el centro mientras visualizas energía fluyendo',
      '4. Danza o mueve tu cuerpo en el círculo',
      '5. Cierra el ritual agradeciendo a Lilith',
    ],
    efectos: [
      'Activación de abundancia',
      'Energía sexual creativa',
      'Manifestación acelerada',
    ],
    mejorPorMood: ['amplificada', 'neutral'],
  },

  // ARTEMISA
  artemisa_proteccion: {
    id: 'artemisa_proteccion',
    nombre: 'Escudo Cazador',
    diosa: 'artemisa',
    descripcion: 'Crea una barrera protectora alrededor tuyo y tu espacio.',
    duracion: '10 min',
    dificultad: 'básico',
    requerimientos: ['Sal', 'Hierba de artemisa (si tienes)'],
    pasos: [
      '1. De pie en el centro de tu espacio, visualiza verde profundo',
      '2. Esparce sal alrededor tuyo en círculo',
      '3. Di: "Artemisa, cazadora del bosque, protege mis límites"',
      '4. Visualiza un escudo de luz verde brillante',
      '5. Toca el suelo para anclarte',
    ],
    efectos: [
      'Protección energética',
      'Límites claros',
      'Sensación de seguridad',
    ],
    mejorPorMood: ['neutral', 'reposo'],
  },

  artemisa_independencia: {
    id: 'artemisa_independencia',
    nombre: 'Camino del Lobo Solitario',
    diosa: 'artemisa',
    descripcion: 'Fortalece tu camino independiente y tu poder personal salvaje.',
    duracion: '15 min',
    dificultad: 'intermedio',
    requerimientos: ['Cuenco con agua', 'Vela verde'],
    pasos: [
      '1. Mira el agua como si fuera un espejo de la naturaleza',
      '2. Enciende la vela verde',
      '3. Declara 3 cosas en las que eres completamente independiente',
      '4. Visualiza el arquetipo del lobo: fuerte, libre, autosuficiente',
      '5. Bebe agua del cuenco con intención',
    ],
    efectos: [
      'Empoderamiento independiente',
      'Confianza en intuición',
      'Fuerza salvaje activada',
    ],
    mejorPorMood: ['amplificada', 'neutral'],
  },

  // AFRODITA
  afrodita_atraccion: {
    id: 'afrodita_atraccion',
    nombre: 'Magnetismo del Deseo',
    diosa: 'afrodita',
    descripcion: 'Atrae conexión, amor, y lo que deseas hacia ti.',
    duracion: '15 min',
    dificultad: 'básico',
    requerimientos: ['Velas rosas/rojas', 'Rosa o pétalos', 'Espejo'],
    pasos: [
      '1. Mira tu reflejo en el espejo mientras enciendes velas',
      '2. Di: "Yo soy hermosa, magnetizo lo que deseo"',
      '3. Esparce pétalos a tu alrededor',
      '4. Visualiza tu deseo ya manifestado',
      '5. Mueve tu cuerpo con sensualidad, celebrando',
    ],
    efectos: [
      'Atracción potenciada',
      'Auto-amor elevado',
      'Conexiones fluyen hacia ti',
    ],
    mejorPorMood: ['amplificada', 'neutral'],
  },

  afrodita_sanacion: {
    id: 'afrodita_sanacion',
    nombre: 'Baño de Armonía',
    diosa: 'afrodita',
    descripcion: 'Sana heridas emocionales y restaura la armonía interna.',
    duracion: '30 min',
    dificultad: 'intermedio',
    requerimientos: ['Agua caliente', 'Sales de baño', 'Velas rosas'],
    pasos: [
      '1. Prepara un baño caliente con sales',
      '2. Enciende velas a tu alrededor',
      '3. Entra al agua lentamente, declarando: "Me amo sin condiciones"',
      '4. Relaja tu cuerpo, visualiza luz rosa sanando tu corazón',
      '5. Permanece 20-30 min en auto-compasión',
    ],
    efectos: [
      'Sanación emocional',
      'Auto-compasión',
      'Armonía restaurada',
    ],
    mejorPorMood: ['reposo', 'neutral'],
  },

  // ISIS
  isis_sincronizacion: {
    id: 'isis_sincronizacion',
    nombre: 'Alineación Cósmica',
    diosa: 'isis',
    descripcion: 'Sincronízate con los ritmos cósmicos y la sabiduría universal.',
    duracion: '20 min',
    dificultad: 'avanzado',
    requerimientos: ['Luna visible o imagen', 'Cristales claros', 'Agua de manantial'],
    pasos: [
      '1. Busca la luna o visualízala con los ojos cerrados',
      '2. Coloca cristales claros en mandala a tu alrededor',
      '3. Bebe agua lentamente, sintiendo la sabiduría antigua',
      '4. Medita en los ciclos: lunares, estelares, personales',
      '5. Pide: "Sincroniza mi camino con el orden cósmico"',
    ],
    efectos: [
      'Sincronización cósmica',
      'Sabiduría disponible',
      'Fljo alineado con propósito',
    ],
    mejorPorMood: ['neutral', 'reposo'],
  },

  isis_alquimia: {
    id: 'isis_alquimia',
    nombre: 'Transmutación de Circunstancias',
    diosa: 'isis',
    descripcion: 'Transforma lo que ya no sirve en sabiduría y poder.',
    duracion: '25 min',
    dificultad: 'avanzado',
    requerimientos: ['Papel', 'Vela blanca y negra', 'Agua y fuego (seguros)'],
    pasos: [
      '1. Escribe una circunstancia difícil en papel',
      '2. Enciende velas blanca (transformación) y negra (lo viejo)',
      '3. Lee: "Transmuto este dolor en sabiduría profunda"',
      '4. Quema el papel mientras visualizas alquimia',
      '5. Medita sobre la lección y nuevo poder ganado',
    ],
    efectos: [
      'Transmutación de dolor',
      'Sabiduría de experiencia',
      'Resurrección de poder',
    ],
    mejorPorMood: ['neutral'],
  },
};

export function getRitualesByDeity(diosa: DeityKey): Ritual[] {
  return Object.values(RITUALES).filter((r) => r.diosa === diosa);
}

export function getRitualById(id: string): Ritual | undefined {
  return RITUALES[id];
}
