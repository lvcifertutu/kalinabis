# KALINABIS — Arquitectura Completa
## Experiencia Inmersiva, Adaptativa, Personalizable (2026)

---

## 0. Principio Fundamental

**Kalinabis es un lienzo mágico que el usuario diseña.**

Cada usuario **crea su propio altar digital**, su propia habitación mágica, su propio paisaje de interacción. La app proporciona:
- **Herramientas** (oráculos, sigilos, conversaciones)
- **Contexto dinámico** (luna, clima, astrología)
- **Narrativa procedural** (historias únicas, generadas en tiempo real)
- **Libertad total** de personalización

NO hay experiencia "default". Cada usuario es su propio diseñador.

---

## 1. ARQUITECTURA DE EXPERIENCIA (3 Capas)

### Habitación Mágica 3D Navegable

```
     ┌─────────────────────────────────────┐
     │  VENTANA METEOROLÓGICA              │ ← Clima real/actual
     │  (Luna hoy, Hora, Clima, Astrología│
     ├─────────────────────────────────────┤
     │                                     │
     │ [ALTAR PERSONALIZADO - Usuario crea]│ ← Deidades, velas, plantas
     │                                     │
     │ LIBRERÍA (1)  MESA (2)  PUERTA (3) │ ← 3 capas navegables
     │ [Scroll/zoom] [Scroll/zoom] [...]  │
     │                                     │
     │ [ELEMENTOS FLOTANTES]               │ ← Runas, símbolos personalizados
     │ ~~~~ Animación ambiental ~~~~       │
     │                                     │
     └─────────────────────────────────────┘
     
     [SONIDO AMBIENTAL] ← Viento, agua, fuego (user elige)
```

**Cada elemento es editable.**

---

## 2. ENERGÍA Y FRECUENCIA (En tiempo real)

### Detección (NO perfila por preguntas)

```
INPUTS:
├─ Hora de uso → Luna actual, fase, VOC
├─ Posición del usuario (lat/lon) → clima local real
├─ Astrología → posición planetas, aspecto actual
├─ Chakana/Andino → posición en ciclo ceremonial
└─ Datos del usuario (ingresados una sola vez):
   ├─ Fecha de nacimiento
   ├─ Lugar de nacimiento (lat/lon)
   └─ Deidad primaria elegida (Lilith, Luna, Kali, etc.)

CALCULO:
├─ Carta natal del usuario (cálculo one-time)
├─ Tránsitos actuales (qué planetas pasan sobre su carta)
├─ Luna hoy vs. Luna en su nacimiento
├─ Clima local real vs. Energía elemental user
└─ VOC (Void of Course) Moon

OUTPUT:
├─ "Energía sugerida" para hoy (deidad/elemento recomendado)
├─ Tarot: solo Arcanos Mayores, seleccionados por astrología actual
├─ UI: colores, fonts, animaciones según energía
└─ Narrativa: contexto astrológico + climático
```

### Ejemplo Concreto

**Usuario:**
- Fecha nac: 1995-05-15, Valdivia
- Deidad primaria: Lilith
- Hora acceso: 2026-06-05 22:30 (2:30 AM)

**Sistema calcula:**
- Luna hoy: Menguante, aspecto oscuro, Escorpio
- Tránsitos: Plutón en aspecto tenso a su Mercurio
- Clima Valdivia: 12°C, lloviendo, viento sur
- VOC: NO (Luna aspecto Saturno en 3h)
- Elemento hoy: Agua (lluvia + luna menguante)

**Recomendación:**
- Energía principal: **Lilith + Agua** (introspección oscura, emociones profundas)
- UI: **Purpura oscuro/negro, fuente dramática, animación lenta** (respiración profunda)
- Tarot: Arcanos que resuenen con **transformación sombría, muerte/renacimiento**
- Narrativa: "La lluvia llama a Lilith. Hoy es momento de enfrentar lo reprimido..."

---

### Opción de Velocidad de UI

User elige:
- **Modo Rápido:** Transiciones inmediatas, clics responsivos, energía alta (para energía dispersa/caótica)
- **Modo Lento:** Transiciones suaves 1-2s, pausas contemplativas, energía enfocada (para reflexión profunda)

---

## 3. PERSONALIZACIÓN DINÁMICA (El Altar)

### Sistema de Altar Personalizado

Cada usuario diseña su **Altar Digital**. Elementos configurables:

```
DEIDAD PRIMARIA:
├─ Lilith → UI purpura/negro, énfasis en desafío/sombra, fuente serif dramática
├─ Luna → UI plateada/azul, suave, énfasis en intuición/ciclos
├─ Kali → UI rojo/oro, dinámico, énfasis en destrucción creativa
├─ Hecate → UI gris/plata, mística, énfasis en encrucijadas
├─ Hermes → UI amarillo/naranja, velocidad, énfasis en comunicación
└─ [User puede agregar más...]

ELEMENTO PRIMARIO:
├─ Agua (Emociones, intuición)
├─ Fuego (Acción, transformación)
├─ Aire (Pensamiento, comunicación)
├─ Tierra (Grounding, manifestación)
└─ Caos (Aleatoriedad, imprevisibilidad)

COLORES PERSONALIZADOS:
├─ Fondo (sólido, gradiente, textura)
├─ Texto (color, font-family, tamaño)
├─ Acentos (bordes, sombras, efectos)
└─ Animaciones (velocidad, suavidad, intensidad)

ELEMENTOS FLOTANTES (User agrega):
├─ Runas propias
├─ Símbolos personales
├─ Imágenes de deidades
├─ Velas virtuales
├─ Plantas/flores
├─ Cristales
├─ Objetos mágicos personales
└─ Emojis, glyphs custom

SONIDO AMBIENTAL:
├─ Lluvia, viento, trueno
├─ Agua, río, océano
├─ Fuego, velas, chimenea
├─ Campanas, cuencos tibetanos
├─ Silencio + respiración
└─ Custom (user sube audio)

ILUMINACIÓN:
├─ Luz de vela (cálida, parpadeante)
├─ Luz lunar (plateada, mística)
├─ Luz solar (dorada, clara)
├─ Penumbra (introspectiva)
└─ Oscuridad absoluta (profunda meditación)
```

### Altar se Adapta Dinámicamente

```
TIME:
- 6am-12pm: Luz solar aumenta gradualmente
- 12pm-6pm: Pico de claridad
- 6pm-9pm: Sunset, colores cálidos
- 9pm-12am: Luz lunar, plateada
- 12am-6am: Oscuridad profunda, solo velas

LUNA:
- Luna Nueva: Oscura, UI desaturada, sonidos mínimos
- Creciente: Brillo aumenta, colores más vivos
- Luna Llena: Máximo brillo plateado, animación pulsante
- Menguante: Brillo disminuye, sonidos más profundos

CLIMA (API):
- Lluvia: sonido lluvia, UI mojado (efecto agua), colores azules
- Nieve: sonido viento suave, cristales flotantes, UI helada
- Tormenta: sonido trueno, relámpagos ocasionales, UI dinámico
- Despejado: brillo solar o lunar según hora

ASTROLOGÍA:
- Retrogrado: efectos glitch sutiles, UI inestable (controlado)
- Gran aspecto: animaciones más complejas, narrativa dramática
- VOC Moon: UI relajada, menos estímulos, espacio para meditación

USER ENERGIA:
- Velocidad lenta: Transiciones 1-2s, pausas, fuente grande
- Velocidad rápida: Transiciones 0.2s, responsive, interfaz dinámica
```

---

## 4. NARRATIVA PROCEDURAL (Todo LLM, tiempo real)

### Premisa

**Nada está predefinido.** Cada narración es única, generada en tiempo real por LLM.

### Sistema de Generación

```
INPUT (al LLM):
├─ User: nombre_mago, deidad_primaria, elemento, energía_hoy
├─ Contexto astrológico:
│  ├─ Carta natal resumen
│  ├─ Tránsitos actuales
│  ├─ Luna actual vs. natal
│  ├─ VOC status
│  └─ Aspecto dramático (si existe)
├─ Contexto geográfico:
│  ├─ Ubicación user
│  ├─ Clima local
│  ├─ Ecoregión (según geografía.py)
│  └─ "Energía" del lugar (cultural, histórica)
├─ Contexto temporal:
│  ├─ Hora (circadiano)
│  ├─ Día de semana
│  ├─ Estación
│  └─ Ciclo lunar
├─ Contexto mágico:
│  ├─ Último working del user (hace N días)
│  ├─ Sigilos activos
│  ├─ Servitors en juego
│  └─ Paradigmas activos
└─ Contexto colectivo:
   ├─ Sincronicidades recientes en El Árbol
   ├─ Energía global (tormentas, eclipses, etc.)
   └─ "Ánimo" colectivo (si existe)

PROMPT TEMPLATE (dinámico):
"[nombre_mago] es un mago de [deidad] en [lugar], con element [element].
Hoy es [día/hora/luna/astrología].
Su energía está [energía_hoy].

Crea una narrativa única (3-5 oraciones) que:
1. Honre su práctica mágica real
2. Conecte con el contexto actual (astrología, clima, hora)
3. Invite a la acción (una de las 3 capas)
4. NO sea genérica, NO sea predicción, sea poética y misteriosa

Estilo: [estilo según deidad]
Incluye: [elementos según energía]
Evita: predicciones, platitudes, genérico

---"

OUTPUT:
└─ Narrativa única, generada en tiempo real
   Ej: "El viento del sur trae lluvia a Valdivia. 
        Lilith susurra en tu oído: 
        'Hoy, las sombras tienen voz. ¿Las escucharás?'
        
        Tu tarot: Los Arcanos te esperan en la Mesa."
```

### Tipos de Narrativas (por capa)

**Capa 1 (Grimorio):**
- "Hoy el Bosque sugiere aprender sobre [tema astrológicamente relevante]..."
- "Tu práctica de [deidad] necesita [método de gnosis]..."
- "Registrá hoy: ¿qué te reveló la lluvia/luna/tormenta?"

**Capa 2 (Mesa):**
- "La hora es propicia para invocar a [deidad según astrología]..."
- "Tu tarot hoy revela un Arcano de [transformación/reto/revelación] según Plutón..."
- "Antes de cargar tu sigilo: verifica tu intención. Lilith ve claridad."

**Capa 3 (Árbol):**
- "En El Bosque, otros siembran sigilos de [tema colectivo detectado]..."
- "La micorriza te llama. Conecta con [otro mago anónimo]..."
- "El Ngillatún hoy: el Árbol respira lentamente. ¿Quieres contribuir?"

### Memoria a Corto Plazo (Máximo azar)

Para mantener **privacidad + frescura**, Kalinabis **recuerda solo últimas 7 días**:
```
MEMORIA:
├─ Últimas consultas (últimos 7 días)
├─ Sigilos activos (creados, no cargados)
├─ Servitors alimentados
├─ Últimas prácticas guiadas
└─ [PURGA] Todo lo anterior a 7 días

BENEFICIO:
├─ User no es perfilado ("te conozco bien, usuario X")
├─ Cada semana: nuevas recomendaciones, nuevo azar
├─ Privacidad: no hay "archivo personal permanente" de preguntas
└─ Frescura: LLM siempre sorprende
```

---

## 5. VERIFICACIÓN PRE-TAROT (Datos del Consultante)

### Flujo de Inicio (One-time + opcionales)

Cuando user accede por primera vez O antes de tarot:

```
PANTALLA: "Antes de consultar los Arcanos"

REQUERIDO (one-time):
┌─────────────────────────────────┐
│ ¿Tu fecha de nacimiento?         │
│ [15-05-1995]                    │
│                                 │
│ ¿Lugar de nacimiento?           │
│ [Valdivia, Chile]               │
│                                 │
│ ¿Deidad primaria?               │
│ [Lilith / Luna / Kali / ...]    │
│                                 │
│ [GUARDAR] [SALTAR por ahora]    │
└─────────────────────────────────┘

OPCIONAL (actualizar cada sesión):
┌─────────────────────────────────┐
│ Tu energía hoy (1-10):          │
│ [████░░░░░] 4 (introspectiva)   │
│                                 │
│ ¿Enfoque de la consulta?        │
│ [Amor / Trabajo / Espíritu /... │ ← User describe, NO app asume
│                                 │
│ [LISTO, CONSULTAR ARCANOS]      │
└─────────────────────────────────┘

CALCULO (Backend):
├─ Carta natal (one-time)
├─ Tránsitos actuales
├─ Luna hoy
├─ Clima local
├─ VOC status
└─ Selecciona Arcanos Mayores relevantes a contexto

RESULTADO:
├─ "Tu energía hoy:"
│  ├─ Arcano sugerido: El Eremita (Saturno, introspección)
│  ├─ Hora: 2am (energía nocturna, Plutón en aspecto)
│  ├─ Luna: Menguante en Escorpio
│  └─ Narrativa: "Los Arcanos revelan profundidad..."
├─ [Tirada de 1/3/7 Arcanos Mayores]
└─ Interpretación astrológica (LLM procedural)
```

---

## 6. INTERFAZ VIVA 3D NAVEGABLE

### Tecnología

- **Engine:** Three.js o Babylon.js
- **Renderizado:** 3D isométrico o perspectiva primera persona
- **Interacción:** Scroll/drag para navegar, click para elementos

### Espacios Principales

#### Habitación Central (Hub)

```
     ┌─────────────────────────────────┐
     │     VENTANA METEOROLÓGICA        │
     │  🌙 Luna: Menguante Escorpio     │
     │  🌧️  Clima: Lluvia, 12°C        │
     │  ⏰ Hora: 22:30 - Energía nocturna
     │  ♇ Aspecto: Plutón tenso        │
     ├─────────────────────────────────┤
     │                                 │
     │     [ALTAR PERSONALIZADO]       │
     │     (Velas, plantas, deidades)  │
     │     [User EDITA aquí]           │
     │                                 │
     │  LIBRERÍA    MESA      PUERTA   │
     │  [Scroll]   [Scroll]   [Scroll] │
     │                                 │
     │ ~~~~ Elementos flotantes ~~~~   │
     │ (Runas, símbolos, cristales)    │
     │                                 │
     └─────────────────────────────────┘
```

#### Librería (Capa 1)

```
     Estantes iluminados
     ├─ Grimorio abierto (user escribe)
     ├─ Tomo de guías (selecciona tema)
     ├─ Calendario de prácticas
     └─ Biblioteca de métodos
     
     Atmósfera: Dorada, tranquila, sabia
     Sonido: Viento suave, quizás fuego lejano
```

#### Mesa (Capa 2)

```
     Altar mágico
     ├─ Tarot (mazo de Arcanos Mayores)
     ├─ Runas
     ├─ I Ching
     ├─ Geomancia
     ├─ Velas para invocar
     ├─ Sigilos dibujados
     └─ Servitors (como presencias)
     
     Atmósfera: Dinámica, sensual, poderosa
     Sonido: Campanas, respiración, crépitar de velas
```

#### Puerta/Ventana (Capa 3)

```
     Vista al Bosque
     ├─ Esferas vivas (4 tipos, pulsantes)
     ├─ Elementos flotantes (sigilos sembrados)
     ├─ Clima del Bosque
     ├─ Tectónica en tiempo real
     └─ Presencias de otros magos (anónimas)
     
     Atmósfera: Colectiva, respirable, sagrada
     Sonido: Naturaleza, sincronía, silencio sagrado
```

### Animaciones Vivas

```
RESPIRACIÓN:
├─ Elementos pulse según energía user
├─ Ritmo lento (meditativo) vs. rápido (activo)
└─ Desincronizados para naturalidad

FLOTACIÓN:
├─ Runas/símbolos suben/bajan lentamente
├─ Path aleatorio pero orgánico (Perlin noise)
└─ Personalizados por user (qué elementos flotan)

LUZ DINÁMICA:
├─ Velas parpadeantes (shader procedural)
├─ Luz lunar (aumenta/disminuye con luna real)
├─ Reflejo clima (lluvia = mojado, brillo disminuido)
└─ Aspecto astrológico (retrogrado = glitch sutil)

INTERACCIÓN:
├─ Hover sobre elementos → glow suave
├─ Click → efecto ripple, sonido
├─ Transiciones smooth (Modo Lento) vs. inmediatas (Modo Rápido)
```

---

## 7. SISTEMA DE PERSONALIZACIÓN (El Canvas)

### User crea su ambiente

```
EDITOR DE ALTAR (Accesible en cualquier momento)

┌──────────────────────────────────────┐
│ MI ALTAR                             │
├──────────────────────────────────────┤
│                                      │
│ DEIDAD PRIMARIA:                    │
│ [Lilith ▼] → Aplicar a UI           │
│                                      │
│ ELEMENTO:                            │
│ [Agua ▼] → Sonidos, animaciones     │
│                                      │
│ COLORES:                             │
│ [Fondo: ■ #1a0a2e ▼]               │
│ [Texto: ■ #ff0080 ▼]               │
│ [Acentos: ■ #0f3460 ▼]             │
│                                      │
│ VELOCIDAD DE UI:                    │
│ (○ Rápido  ● Lento)                 │
│                                      │
│ ELEMENTOS FLOTANTES:                │
│ [+ Agregar runa] [+ Agregar imagen] │
│ • Runa Hagalaz (custom)             │
│ • Foto de Lilith                    │
│ • Cristal morado                    │
│ [× Remover]                         │
│                                      │
│ SONIDO AMBIENTAL:                   │
│ [Lluvia ▼] Vol: [████░░░░] 60%     │
│ [+ Agregar sonido custom]           │
│                                      │
│ ILUMINACIÓN:                        │
│ [Velas parpadeantes ▼] Intensidad:  │
│ [███░░░░░░] 30% (meditativo)        │
│                                      │
│ [GUARDAR] [PRESETS] [RESTAURAR]    │
└──────────────────────────────────────┘
```

### Presets Rápidos

User puede guardar/cargar "modos":
```
PRESETS:
├─ "Sesión Lilith" (UI oscura, rápida, fuego)
├─ "Meditación Luna" (UI plateada, lenta, agua)
├─ "Caos Total" (colores aleatorios, glitch, caótico)
└─ [+ Crear preset personalizado]
```

### Exportar/Importar Altar

User puede **compartir su diseño** (no su práctica):
```
- Exporta: archivo JSON con colores, elementos, sonidos, presets
- Otros magos pueden importar y adaptar
- Ej: "Altar Lilith-Nocturno de Kalinabis-Community"
```

---

## 8. TABLA DE BD (Nuevas)

```sql
-- Usuario y datos mágicos
CREATE TABLE usuarios (
  id UUID PRIMARY KEY,
  nombre_mago VARCHAR(255) UNIQUE,
  fecha_nac DATE,
  lugar_nac VARCHAR(255),
  lat FLOAT, lon FLOAT,
  deidad_primaria VARCHAR(255),
  created_at TIMESTAMP
);

-- Carta natal (one-time calculation)
CREATE TABLE carta_natal_usuario (
  id SERIAL PRIMARY KEY,
  user_id UUID UNIQUE,
  sol_sign VARCHAR(20),
  luna_sign VARCHAR(20),
  asc_sign VARCHAR(20),
  posiciones_planetas JSON, -- {sol: {signo, grado}, luna: {...}, ...}
  calculada_at TIMESTAMP
);

-- Personalizaciones
CREATE TABLE altar_usuario (
  id SERIAL PRIMARY KEY,
  user_id UUID UNIQUE,
  deidad_activa VARCHAR(255),
  elemento_primario VARCHAR(50),
  colores JSON, -- {fondo: "#...", texto: "#...", acentos: "#..."}
  velocidad_ui VARCHAR(20), -- 'rapido' | 'lento'
  iluminacion VARCHAR(50),
  sonido_ambiental VARCHAR(255),
  sonido_volumen INT,
  elementos_flotantes JSON, -- [{tipo: "runa", valor: "Hagalaz", ...}, ...]
  presets JSON, -- [{nombre: "Lilith Nocturno", ...}, ...]
  updated_at TIMESTAMP
);

-- Memoria a corto plazo (7 días)
CREATE TABLE memoria_corto_plazo (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  tipo VARCHAR(50), -- 'consulta' | 'sigilo' | 'servitor' | 'practica'
  contenido TEXT,
  created_at TIMESTAMP,
  CHECK (created_at > NOW() - INTERVAL '7 days')
);

-- Narrativas generadas (para audit/recall)
CREATE TABLE narrativas_generadas (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  capa VARCHAR(20), -- 'grimorio' | 'mago' | 'arbol'
  narrativa TEXT,
  contexto_generacion JSON, -- {luna, astrologia, clima, energia, ...}
  generated_at TIMESTAMP
);

-- Sigilos dibujados (imagen + intención pulida)
CREATE TABLE sigilos_dibujados (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  intencion_original TEXT,
  intencion_pulida TEXT, -- LLM mejora
  dibujo BYTEA, -- SVG o PNG
  estado VARCHAR(20), -- 'creado' | 'pulido' | 'cargado'
  cargado_at TIMESTAMP,
  created_at TIMESTAMP
);

-- Altares guardados (snapshots para compartir)
CREATE TABLE altares_compartidos (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  nombre VARCHAR(255), -- "Altar Lilith Nocturno"
  configuracion JSON, -- snapshot completo de altar_usuario
  descripcion TEXT,
  publico BOOLEAN DEFAULT FALSE,
  downloads INT DEFAULT 0,
  created_at TIMESTAMP
);
```

---

## 9. API NUEVA

```
DATOS ASTROLÓGICOS:
POST /api/astrologia/carta-natal
  Input: fecha_nac, lugar_nac
  Output: {sol_sign, luna_sign, asc, posiciones_planetas}

GET /api/astrologia/transitos-hoy
  Output: {tránsitos actuales, aspectos, VOC_status}

GET /api/astrologia/energia-sugerida
  Input: user_id
  Output: {deidad_sugerida, elemento, narrativa_contexto}

---

PERSONALIZACIÓN:
POST /api/altar/guardar
  Input: colores, velocidad, elementos, sonido, presets
  
GET /api/altar/obtener
  Output: configuración actual del altar

POST /api/altar/crear-preset
  Input: nombre, configuración
  
GET /api/altares/compartidos
  Output: lista de altares públicos para importar

---

NARRATIVA:
GET /api/narrativa/generar
  Input: user_id, capa, contexto_extra
  Output: narrativa única generada con LLM

---

TAROT:
POST /api/tarot/verificar-consultante
  Input: energia_hoy, enfoque
  Output: {confirmación, contexto astrológico, Arcanos sugeridos}

POST /api/tarot/tirada
  Input: num_cartas (1, 3, o 7), user_id
  Output: {Arcanos, interpretación astrológica procedural}

---

GRIMORIO:
POST /api/grimorio/nueva-entrada
  Input: titulo, contenido, tags
  
GET /api/grimorio/entradas
  Output: últimas entradas

---

SIGILOS:
POST /api/sigilos/subir-dibujo
  Input: intencion, imagen
  Output: {dibujo procesado, intención pulida por LLM}

POST /api/sigilos/cargar
  Input: sigilo_id
  Output: {confirmación, sigilo desaparece, narrativa de carga}

---

MEMORIA:
GET /api/memoria/ultimos-7dias
  Output: últimas actividades (para contexto narrativo)

POST /api/memoria/purgar
  (Automático cada 7 días)
```

---

## 10. TECNOLOGÍA PROPUESTA

### Frontend
- **Framework:** Next.js o Vue 3 (para reactividad dinámica)
- **3D:** Three.js o Babylon.js (isométrico/primera persona)
- **Animaciones:** Framer Motion (smooth, performant)
- **Audio:** Web Audio API + Tone.js (síntesis procedural)
- **State:** Zustand o Pinia (responsivo, eficiente)

### Backend
- **Actual:** Flask (mantener)
- **Astrología:** Skyfield library (posiciones planetarias)
- **LLM:** Groq (narrativa procedural)
- **BD:** PostgreSQL (Supabase)
- **Cache:** Redis (para memoria corto plazo, limpieza automática)

### Infraestructura
- **Deploy:** HF Spaces (Docker)
- **CDN:** Para assets (imágenes deidades, cristales, etc.)

---

## 11. ROADMAP

### FASE 0 (MVP — 2-3 semanas)
- ✅ 3 capas navegables (básico, sin 3D)
- ✅ Altar personalización (colores, deidad, elemento)
- ✅ Verificación pre-tarot (datos consultante)
- ✅ Narrativa procedural (LLM básico)
- ✅ Integración astrológica (Skyfield)
- ✅ Memoria 7 días

### FASE 1 (Pulido visual — 2-3 semanas)
- Interfaz 3D isométrica (Three.js)
- Animaciones vivas (respiración, flotación)
- Sonido ambiental (Web Audio)
- Editor de altar (drag-drop)

### FASE 2 (Expansión — 4 semanas)
- Sigilización con dibujo
- Narrativa mejorada (LLM multi-turn)
- Clima API externa (OpenWeatherMap)
- Tectónica (USGS)
- Presets compartibles

### FASE 3 (Colectivo — 6 semanas)
- El Árbol funcional (esferas, sincronicidades)
- Micorriza (rituals entre magos)
- Ngillatún (asamblea colectiva)
- Juegos/puzzles simples

### FASE 4 (Pulido final — ongoing)
- Puzzles complejos y colaborativos
- Voice / gestos (accesibilidad)
- Integración wearables (Fitbit = energía corporal)

---

## 12. PRINCIPIOS CLAVE

1. **Usuario es el Diseñador**
   - Todo personalizable
   - El ambiente refleja al mago, no al revés

2. **Privacidad + Anonimato**
   - Memoria 7 días (frescura, olvido mágico)
   - Datos personales cifrados
   - Compartir es OPT-IN

3. **Narrativa Única**
   - LLM procedural, nada predefinido
   - Cada sesión es diferente
   - Contexto astrológico/climático siempre

4. **Libertad Creativa**
   - User agrega sus elementos
   - UI responde, no impone
   - Experimentos bienvenidos

5. **Magia Real**
   - Basada en métodos concretos (Carroll, Spare, Hine)
   - Sin platitudes esotéricas
   - Rigor + Misterio

---

## 13. DOCUMENTOS RELACIONADOS

- `PROMPT_KALINABIS_VISION.md` — visión original
- `ARQUITECTURA_EXPERIENCIA_KALINABIS.md` — 3 capas + exp
- `LA_MAGIA_DEL_CAOS.md` — base teórica de features
- `EL_BOSQUE.md` — cosmología del Árbol
- `ROADMAP_BOSQUE.md` — fases del Bosque completo

---

## Siguiente: ¿Empezamos por Fase 0 (MVP)?

Si confirmás, creo:
1. **Spec técnica detallada** (endpoints, DB schema, UI wireframes)
2. **Brief para Frontend** (colores, componentes, narrativa)
3. **Brief para Backend** (astrología, narrativa LLM, memoria)
4. **Plan de implementación** (orden, dependencies, timeframes)

