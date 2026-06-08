# KALINABIS — Brief de Visión + Prompt para Claude Code

## Visión de la Experiencia (UX)

**¿Qué es Kalinabis?**
Aplicación de agentes espirituales basada en **Magia del Caos** real (Carroll, Spare, Hine, Morrison). No es decoración esotérica — implementa métodos digitalizables con LLM.

**¿Quién?**
Practitioners de chaos magic + curiosos interesados en sigilización, gnosis, sincronicidad, paradigm shifting.

**¿Dónde experimentan?**
1. **Terminal CRT** (`/`) — interfaz primaria. Comandos mágicos tipo CLI. Inmediato, sin clicks.
2. **Dashboard clásico** (`/clasico`) — histórico, cartas natales, proyectos. Secundario.
3. **Proyecto anónimo** — cifrado, compartible (X-Project-Code header).

**¿Qué hacen?**
- Tiran **runas** (3 o 9), consultan **I Ching** (64 hexagramas), piden **geomancia** (Escudo 12 Casas)
- Invocan **gnosis** (6 métodos), practican **sigilización**, crean **servitors** (thoughtforms con lifecycle)
- Registran **sincronicidades**, hacen **paradigm shifting** (30 días), invocan **8 rayos**
- Exploran **El Bosque** (ecosistema mágico colectivo con esferas, atmósfera elemental, tectónica)
- Cargan sigilos, leen tarot, interactúan con **Tutu** (daemon IA)

**Tono:**
- Respetuoso con la práctica real
- Código limpio, legible, testeable
- No copy-paste de tutoriales
- Cada feature fundamentada en método concreto

---

## Stack Actual

### Backend
- **Framework:** Flask (Python 3.11)
- **LLM:** Groq (llama-3.1-8b-instant)
- **Base de datos:** SQLite (local) / PostgreSQL (producción, Supabase)
- **Arquitectura:** Ports & adapters
  - `invocacion/` — encapsula IA (Groq, offline, test)
  - `persistencia.py` — adapters BD (SQLite/Postgres)
  - `proyecto_contexto.py` — manejo de identidad de proyecto + cifrado
  - `servidor.py` — 61 endpoints

### Frontend
- **HTML/CSS/JS** — `grimorio.html` (bundleado desde `src/*.html`)
- **Terminal CRT** — primario, comandos `/runas`, `/iching`, `/tarot`, `/bosque`, etc.
- **Dashboard** — secundario, estado visualizado
- **Estado:** Fetch API, vanilla JS

### Deploy
- **HF Spaces** (Docker, puerto 7860) — https://huggingface.co/spaces/lvcifertutu/kalinabis
- **GitHub** — https://github.com/lvcifertutu/kalinabis (mirror)
- **Env vars:** GROQ_API_KEY, DATABASE_URL, GROQ_MODEL

---

## Características Completadas (por Fase)

### Fase 1 ✅
- Terminal CRT como frontend principal
- **Runas** (Elder Futhark, 3 y 9-runa)
- **Gnosis** (6 métodos: meditación vacía, privación sensorial, hiperventilación, movimiento, risa, orgasmo)

### Fase 2 ✅
- **I Ching** (64 hexagramas, 3 monedas, hexagrama futuro si hay cambio)
- **Geomancia** (16 figuras, Escudo 12 Casas, Madres→Hijas→Sobrinas→Juez)
- **Servitors** (thoughtforms, lifecycle activo→letargo→disolviendo→disuelto, decay −4%/día, feed +22%)

### Fase 3 ✅
- **Oráculo de la Discordia** (Eris, 24 señales)
- **Synchronicidades** (registro, confirmación, colectivas)
- **8 Rayos** (Octagram Carroll, test de preguntas)
- **Paradigm Shifting** (8 paradigmas, 30 días, checkins)

### El Bosque (parcial) ✅
- **Esferas** (4 tipos: geo, elemental, temática, resonancia)
- **Ciclo de vida** (activa→letargo→disolviendo→disuelta)
- **Estratos** (Sotobosque, Dosel, Emergentes) + atmósfera elemental
- **Geomancia climática** (14 ecoregiones WWF)
- **Marcar bajo el Canelo** (auth, persistencia)

---

## Pendientes Arquitectura (P1-P12 en roadmap)

### Prioritario (P1-P4)
1. **Gen/newen** — individuo vs. especie colectiva en esferas
2. **Micorriza** — ritual de cruce entre proyectos
3. **Death cycle explícito** — en pie → raíz que espera → humus
4. **Avatar 3 prendas** — Cuerpo/Alma/Espíritu (guardianas/Tutu/Kali)

### Mediano (P5-P8)
5. **Clima API** — weather externa, offline first
6. **Tectónica** — USGS sismicidad
7. **Ngillatún** — espacio colectivo visible
8. **Sigilización mejorada** — intención pulida, nombre secreto, estado (creado→cargado→olvidado→manifestado)

---

## Refactorings Completados (2026-06-05)

### #1: Invocación IA
`invocacion/` package encapsula Groq:
- Protocol `ClienteIA`, dataclass `RespuestaIA`
- Adapters: `groq.py`, `offline.py`, `test.py`
- `ContextoManager` — arma system prompts por deidad/tarot/sigilo
- `Invocador` — orquesta todo
- **Beneficio:** Cambiar proveedor = 1 adapter nuevo + 1 línea en `__init__.py`

### #2: Identidad de Proyecto
`proyecto_contexto.py`:
- `ContextoProyecto` — valida X-Project-Code, cifra/descifra AES, maneja memoria
- `.desde_headers()`, `.requerir()`, `.cifrar()`, `.descifrar()`
- **Beneficio:** Proyectos anónimos, compartibles, sin rastreo

### #3: Persistencia (Ports & Adapters)
`persistencia.py`:
- `AdaptadorBD` (ABC) → `AdaptadorSQLite` / `AdaptadorPostgres`
- Factory `crear_adaptador(DATABASE_URL)`
- Delega `placeholder()`, `tipo_serial()`, `id_ultimo_insertado()`
- **Beneficio:** Migrate SQLite ↔ Postgres sin tocar 50+ call sites

### #6: Test Harness
`tests/harness.py` + `tests/test_comportamiento.py`:
- DB TEMPORAL, inyección `ClienteTest`
- 29 tests de comportamiento (validación, rate limit, flujos IA, proyectos, lectura)
- ~0.25s sin red/Groq/DB real
- **Beneficio:** CI/CD confiable, offline

---

## PROMPT PARA CREAR/MEJORAR KALINABIS

Use este prompt cuando quiera:
- Nuevas features
- Refactoring arquitectura
- Debugging
- Mejoras UX

### Para Nuevas Features

```
Kalinabis es una app de Magia del Caos (Carroll, Spare, Hine).
Stack: Flask + Groq + SQLite/Postgres, frontend HTML/CRT terminal.
Base: 61 endpoints, 9 módulos mágicos, 48 tests.

Quiero agregar: [DESCRIBE LA FEATURE]

**Requerimientos:**
1. Basada en método de chaos magic real (referencia: autor/libro/página)
2. Terminal command + endpoint API (decoupled)
3. DB: ¿tabla nueva? ¿tipo de repo?
4. LLM: ¿system prompt nuevo? ¿usar invocador?
5. Tests: ¿comportamiento + unit?

**Beneficios esperados:**
- [QUÉ RESUELVE]

**Restricciones:**
- No hardcode secrets
- Immutable patterns
- <50 líneas por función
- 80%+ test coverage
```

### Para Refactoring

```
Kalinabis, refactor:
Archivo(s): [PATH]
Problema: [DESCRIBE]
Objetivo: [QUÉ DEBE PASAR]
Scope: [behavior-preserving / API change / internal]

Usar skill: improve-codebase-architecture (si no es claro)
```

### Para Debugging

```
Kalinabis, bug:
Endpoint / Comando: [RUTA O CLI]
Paso a paso:
1. [QUÉ HACES]
2. [QUÉ ESPERAS]
3. [QUÉ PASA EN LUGAR]

Error / Evidencia: [SCREENSHOT / LOG / ASSERT]

Entorno: [LOCAL / HF SPACE]
```

---

## Skills Recomendados

| Skill | Cuándo | Beneficio |
|-------|--------|-----------|
| **improve-codebase-architecture** | Refactors arquitectura | Detecta deepenings, modularización |
| **tdd** | Nuevas features, bugfixes | Red-green-refactor, cobertura 80%+ |
| **code-review** | Después de escribir | Bugs, reuse, security, testing |
| **security-review** | Auth, cifrado, sigilo | OWASP, leaks |
| **build-fix** | CI/CD fails | Errores incrementales |
| **verify** | Cambios UX | Confirmar en navegador |
| **systematic-debugging** | Bugs complejos | Aislar causa raíz |
| **update-docs** | Docstrings, README | Coherencia |

---

## Sobre ECC Rules

Estoy usando https://github.com/affaan-m/ecc ✅

**Rules instaladas:**
- `common/` — coding-style, testing, git-workflow, agents, security
- `web/` — frontend patterns, design-quality, hooks, performance

**Impacto en Kalinabis:**
- **Code:** immutability, <50 líneas, <800 líneas/archivo, DRY/YAGNI
- **Testing:** 80% coverage, TDD, unit+integration+E2E
- **Security:** no hardcoded secrets, OWASP, valida en límites
- **Git:** conventional commits, PRs detallados, no force-push a main
- **Architecture:** ports & adapters, repository pattern, API envelope

**Puedo optar por:**
- Usar **Haiku** (lightweight tasks, pair programming) 
- Usar **Sonnet** (main work, multi-agent orchestration)
- Usar **Opus** (complex architectural decisions)

---

## Checklist Pre-Merge

Antes de commitear / PRs:
- [ ] `git diff` — cambios claros
- [ ] `git log [base]...HEAD` — commits descriptivos (conventional)
- [ ] Tests: `python -m unittest tests.test_comportamiento` pasan
- [ ] Cobertura: ≥80%
- [ ] Code review: `/code-review` (o `--comment` si es PR)
- [ ] No hardcoded secrets, API keys, tokens
- [ ] No `console.log`, `print()`, debug statements
- [ ] Funciones <50 líneas, archivos <800 líneas
- [ ] Error handling explícito
- [ ] Merge conflicts resueltos

---

## Cómo Usar Este Brief

1. **Compartir:** Mandáme este markdown cuando quieras trabajar en Kalinabis
2. **Customizar:** Agrega secciones si el scope crece
3. **Actualizar:** Después de cada refactor/feature, actualiza "Completadas" + "Pendientes"
4. **Prompt:** Referencia la sección relevante (`## PROMPT PARA ...`)

---

## Links Rápidos

- **Repo:** https://github.com/lvcifertutu/kalinabis
- **Deploy:** https://huggingface.co/spaces/lvcifertutu/kalinabis
- **Docs internas:** `LA_MAGIA_DEL_CAOS.md`, `EL_BOSQUE.md`, `ROADMAP_BOSQUE.md`
- **Supabase:** https://supabase.com/dashboard/project/ipjpcvthqzhbjucdtdfh
- **ECC Rules:** https://github.com/affaan-m/ecc

