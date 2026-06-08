# Kalinabis — Arquitectura de Experiencia (3 Capas + Progresión)

## Visión UX: Habitación Mágica en Primera Persona

El user ve una **habitación mágica** (isométrica o ilustración):
```
    ┌─────────────────────────────┐
    │  VENTANA/PUERTA (3)         │  ← El Árbol (colectivo)
    │  [Mira hacia afuera]        │
    ├─────────────────────────────┤
    │                             │
    │  LIBRERÍA (1)   MESA (2)    │
    │  [Estantes,  [Artefactos,  │
    │   Grimorio]   Cartas,      │
    │              Velas]        │
    │                             │
    └─────────────────────────────┘
```

**El user elige dónde ir.**

---

## Capa 1: La Librería (Grimorio/Guía)

### Experiencia
- **User es aprendiz.** Lee guías, practica, documenta su grimorio.
- **Kalinabis lo guía.** Personalizado según preferencias/logros.
- Escritura reflexiva: diarios, notas de práctica, aprendizajes.
- Sin competencia. Sin compararse. Solo aprender.

### Features
| Feature | Tipo | Descripción |
|---------|------|-------------|
| **Grimorio personal** | Escritura | User documenta prácticas, insights, experiencias |
| **Guías por tema** | Educación | Kalinabis explica runas, gnosis, sigilización, etc. |
| **Prácticas guiadas** | Meditación/Ritual | "Hoy: medita 10min en Ansuz" → user confirma → exp Grimorio +10 |
| **Dibujar sigilo** | Sigilización | User dibuja su sigilo, Kalinabis lo transforma en intención pulida |
| **Biblioteca de métodos** | Referencia | Chaos magic según Carroll/Spare/Hine (searchable, filtrable) |
| **Mi progreso** | Logros | Exp Grimorio, badges (Neófito→Iniciado→Adeptus) |

### Exp/Logros (Capa 1)
```
Exp Grimorio:
- Escribir en grimorio: +5 exp
- Completar práctica guiada: +10 exp
- Leer guía completa: +15 exp
- Logros:
  - Neófito: 0 exp
  - Iniciado: 100 exp
  - Adeptus Minor: 500 exp
  - Magister Templi: 2000 exp
```

### Privacidad
- **Completamente privado.** User solo.
- Opción: "Quiero que vean que estoy aprendiendo" → nombre aparece en El Árbol con badge "Grimorio" pasivo.

---

## Capa 2: La Mesa (Mago Personal)

### Experiencia
- **User es el mago.** Espacio íntimo, personal, sagrado.
- Interactúa con oráculos, deidades, sigilos.
- Evocaciones, invocaciones, manifestación.
- Todo privado por default. User controla qué se comparte.

### Features
| Feature | Tipo | Descripción |
|---------|------|-------------|
| **Tarot personal** | Adivinación | Tirada privada, interpretación con deidad activa |
| **Oráculos** | Adivinación | Runas, I Ching, Geomancia, Discordia, Rayos |
| **Conversación con deidades** | Evocación | Chat privado: "Hablo con Lilith sobre mi miedo" |
| **Cargar sigilo** | Manifestación | Sigilo dibujado en Capa 1 → cargado aquí → desaparece del dashboard |
| **Servitors** | Thoughtforms | Crear, invocar, alimentar servitors personales |
| **Diario mágico** | Registro | Notas post-invocación, sincronicidades observadas |
| **Mi espacio** | Configuración | Deidad primaria, colores, aromas, preferencias |

### Exp/Logros (Capa 2)
```
Exp Mago:
- Hacer consulta oráculo: +5 exp
- Conversar con deidad: +10 exp
- Invocar servitor: +15 exp
- Cargar sigilo: +25 exp
- Logros:
  - Evocador: 0 exp
  - Invocador: 100 exp
  - Maestro de Sigilos: 500 exp
  - Operador Caótico: 2000 exp
```

### Privacidad
- **Completamente privado por default.**
- User puede optar: "Comparte mi trabajo en El Árbol" → aparece como aporte anónimo (solo nombre del mago, sin detalles).

---

## Capa 3: La Ventana/Puerta (El Árbol — Colectivo)

### Experiencia
- **User ve el colectivo.** Otros magos (anónimos, solo nombre).
- Aporta su magia: sigilos, sincronicidades, working.
- Interactúa con El Bosque: esferas, atmósfera, tectónica.
- Micorriza: conectar con otros magos (ritual de cruce).

### Features
| Feature | Tipo | Descripción |
|---------|------|-------------|
| **Esferas vivas** | Ecosistema | El Bosque: 4 tipos (geo/elemental/temática/resonancia), ciclo vivo |
| **Aportación sigilo** | Magia colectiva | "Siembro mi sigilo en El Árbol" → contribuye a esfera temática |
| **Sincronicidades colectivas** | Resonancia | Ver qué otros registran, contribuir propias |
| **Micorriza** | Conexión | Ritual de cruce: conectar mi trabajo con otro mago (anónimo) |
| **Ngillatún** | Asamblea | Espacio visible: qué está pasando en el árbol ahora (clima, sismos, ánimo colectivo) |
| **Ofrenda a Kali** | Ritual | Gratitud al sistema, cierre de cycles |
| **Mi linaje** | Identidad | Nombre del mago + logros (opcional) en El Árbol |

### Exp/Logros (Capa 3)
```
Exp Árbol:
- Aportar sigilo: +10 exp
- Registrar sincronicidad colectiva: +5 exp
- Hacer micorriza: +25 exp
- Estar activo en El Árbol (1 semana): +20 exp
- Logros:
  - Observador: 0 exp
  - Aportante: 100 exp
  - Conectado: 500 exp
  - Raíz del Árbol: 2000 exp
```

### Privacidad
- **Nombre del mago es visible.** Nada más.
- Sigilos → anónimos (no se sabe quién los sembró, solo que existen).
- Trabajos → historial privado del user, no visible (a menos que opte por "comparte").

---

## Progresión: 3 Vías de Experiencia (XP independiente)

```
         CAPA 1              CAPA 2              CAPA 3
      Grimorio XP         Mago XP             Árbol XP
      ┌─────────┐        ┌─────────┐        ┌─────────┐
      │ Neófito │        │Evocador │        │Observ. │
      │   0 xp  │        │  0 xp   │        │  0 xp  │
      └────┬────┘        └────┬────┘        └────┬────┘
           │                  │                  │
           ↓                  ↓                  ↓
      ┌─────────┐        ┌─────────┐        ┌─────────┐
      │Iniciado │        │Invocador│        │Aportante│
      │ 100 xp  │        │ 100 xp  │        │ 100 xp  │
      └────┬────┘        └────┬────┘        └────┬────┘
           │                  │                  │
           ↓                  ↓                  ↓
      ┌─────────┐        ┌─────────┐        ┌─────────┐
      │ Adeptus │        │ Maestro │        │Conectado│
      │ 500 xp  │        │ 500 xp  │        │ 500 xp  │
      └────┬────┘        └────┬────┘        └────┬────┘
           │                  │                  │
           ↓                  ↓                  ↓
      ┌─────────┐        ┌─────────┐        ┌─────────┐
      │Magistri │        │ Operador│        │  Raíz   │
      │ 2000xp  │        │ 2000xp  │        │ 2000xp  │
      └─────────┘        └─────────┘        └─────────┘
```

**Usuario puede:**
- Avanzar solo en Capa 1 (aprendiz puro)
- Avanzar en Capa 1 + 2 (mago solitario)
- Avanzar en todas 3 (mago integrado en colectivo)

---

## Modelos de Participación

### Modelo A: Aprendiz (Grimorio + Lectura)
- Lee guías, escribe grimorio, practica meditaciones guiadas
- **Exp:** Solo Grimorio XP
- **Privacidad:** Completamente privado
- **Objetivo:** Aprender, documentar, integrar
- **Badge:** "En Grimorio" (opcional compartir en El Árbol)

### Modelo B: Mago Solitario (Grimorio + Mesa)
- Practica todo: meditación, sigilización, oráculos, invocaciones personales
- **Exp:** Grimorio XP + Mago XP
- **Privacidad:** Ambas capas privadas, opción de compartir trabajos anónimos
- **Objetivo:** Manifestación personal, evolución mágica
- **Badge:** "En la Mesa" (opcional)

### Modelo C: Mago del Árbol (Todas 3 capas)
- Aprende, practica, aporta. Participa en colectivo.
- **Exp:** Grimorio XP + Mago XP + Árbol XP
- **Privacidad:** Todas privadas, participa públicamente en El Árbol (nombre visible)
- **Objetivo:** Maestría personal + contribución colectiva
- **Badge:** "En El Árbol" (visible en Árbol)

---

## Rediseño Frontend (High Level)

### Vista principal: Habitación Mágica
```
┌──────────────────────────────────────────┐
│         KALINABIS — Tu Espacio           │
├──────────────────────────────────────────┤
│                                          │
│    [LIBRERÍA]      [MESA]    [PUERTA]   │  ← 3 "salas"
│     (Capa 1)       (Capa 2)   (Capa 3)  │
│     click →        click →    click →   │
│                                          │
│    XP Progress:                          │
│    Grimorio: ████░░░░░ 150/500          │
│    Mago: ██░░░░░░░░ 25/100              │
│    Árbol: ░░░░░░░░░░ 0/100              │
│                                          │
└──────────────────────────────────────────┘
```

### Dentro de Librería (Capa 1):
```
┌─ Grimorio Personal
│  ├─ Nuevo apunte
│  └─ Mis notas (30 notas)
├─ Guías
│  ├─ Runas (completado ✓)
│  ├─ Gnosis (en progreso)
│  └─ Sigilización
└─ Prácticas
   ├─ Hoy: Meditación Ansuz [5 min] → Confirmar
   └─ Histórico
```

### Dentro de Mesa (Capa 2):
```
┌─ Tirar
│  ├─ Tarot (1 carpa)
│  ├─ Runas (3 o 9)
│  ├─ I Ching
│  └─ Geomancia
├─ Conversar
│  ├─ Con [Deidad activa]
│  └─ Historial
├─ Sigilos
│  ├─ Dibujar nuevo
│  ├─ Cargar sigilo existente
│  └─ Mis sigilos
└─ Servitors
   ├─ Crear
   ├─ Invocar
   └─ Mis servitors
```

### Dentro de Puerta (Capa 3):
```
┌─ El Bosque
│  ├─ Mapa (esferas vivas)
│  ├─ Clima elemental
│  └─ Sismos/tectónica
├─ Contribuir
│  ├─ Sembrar sigilo
│  ├─ Sincronicidades colectivas
│  └─ Mi aportación
├─ Micorriza
│  └─ Conectar con otro mago
└─ Ngillatún
   └─ Asamblea: qué sucede ahora
```

---

## Bases de Datos (Cambios)

### Nuevas tablas
```sql
-- Exp y logros por user/capa
CREATE TABLE usuarios (
  id UUID PRIMARY KEY,
  nombre_mago VARCHAR(255),
  created_at TIMESTAMP,
  modelo TEXT -- 'aprendiz' | 'solitario' | 'arbol'
);

CREATE TABLE exp_usuarios (
  user_id UUID,
  capa VARCHAR(20), -- 'grimorio' | 'mago' | 'arbol'
  exp INT DEFAULT 0,
  nivel INT DEFAULT 1,
  UNIQUE(user_id, capa)
);

CREATE TABLE logros (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  capa VARCHAR(20),
  logro VARCHAR(255), -- 'neófito', 'iniciado', etc.
  fecha TIMESTAMP
);

-- Grimorio personal
CREATE TABLE grimorio_entradas (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  titulo VARCHAR(255),
  contenido TEXT,
  fecha TIMESTAMP,
  tags VARCHAR(255)
);

-- Dibujos de sigilos
CREATE TABLE sigilos_dibujados (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  intencion TEXT,
  dibujo BYTEA, -- imagen SVG/PNG
  estado VARCHAR(20), -- 'creado' | 'pulido' | 'cargado'
  fecha TIMESTAMP
);

-- Aportes anónimos a El Árbol
CREATE TABLE aportes_arbol (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  nombre_mago VARCHAR(255),
  tipo VARCHAR(20), -- 'sigilo' | 'sync' | 'working'
  contenido TEXT,
  compartido BOOLEAN DEFAULT FALSE,
  fecha TIMESTAMP
);
```

---

## Endpoint Changes (Backend)

### API Nuevos
```
POST /api/capa1/grimorio/nueva        -- crear entrada
GET  /api/capa1/exp                   -- mi progreso Grimorio
POST /api/capa1/practica/confirmar    -- confirmar práctica guiada

POST /api/capa2/sigilo/dibujar        -- upload dibujo + intención
POST /api/capa2/sigilo/cargar         -- cargar sigilo (desaparece)
GET  /api/capa2/exp                   -- mi progreso Mago

POST /api/capa3/sigilo/sembrar        -- aportar sigilo a árbol
POST /api/capa3/micorriza             -- conectar con otro mago
GET  /api/capa3/bosque/estado         -- clima, sismos, ánimo
GET  /api/capa3/exp                   -- mi progreso Árbol
```

---

## Preguntas pendientes

1. **Visual:** ¿Ilustración estática (single image) o ambiente navegable (scroll/zoom)?
2. **Colores:** ¿Paleta específica para cada capa (Capa1=dorado, Capa2=purpura, Capa3=verde)?
3. **Narrativa:** ¿Tutu aparece en cada capa con rol diferente? (Bibliotecario → Guardián → Testigo)
4. **Tiempo:** ¿Prácticas guiadas son únicas por día o se pueden repetir?
5. **Compartir:** User puede optar a nivel de feature o global ("quiero privacidad total")?

