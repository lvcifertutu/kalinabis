# ROADMAP — El Bosque de Kalinabis

> Fuente de verdad para el agente (OpenCode). Refleja el estado real del código al 2026-06-04.
> La doctrina vive en `EL_BOSQUE.md`. Este roadmap traza lo que **ya está** y lo que **falta**.

---

## Estado general: El organismo vive, el ecosistema está incompleto

El backend corre. Los sistemas de divinación y magia del caos están completos. El Bosque tiene
estratos, geografía y esferas. Lo que falta es la capa **colectiva** (micorriza, cruces, avatar)
y algunas piezas del **reloj** y el **paisaje** (firma planetaria, tectónica real, clima externo).

---

## Completado

### Infraestructura base
- [x] Flask 3 + SQLite/PostgreSQL dual (`base_datos.py`)
- [x] Proyectos anónimos — código 4 palabras, AES-256-GCM, SHA-256 como ID
- [x] Header `X-Project-Code`, rate limiting por endpoint, CORS configurado
- [x] Deploy Render via `render.yaml` (gunicorn, puerto 7860)
- [x] Frontend terminal CRT — módulos en `src/`, bundleado con `src/build.mjs`
- [x] Frontend clásico — `grimorio.html` (un solo archivo, legacy)
- [x] Modo offline graceful — `GROQ_API_KEY` ausente → `"[Modo offline]..."`

### Fase 1 — Chaos Magic Core
- [x] Luna (`luna.py`) — fases, lunaciones, nodos, marea Yin/Yang, perigeo/apogeo, Void of Course
- [x] Tarot — arcanos, lecturas por entidad (`/api/tarot/*`)
- [x] Sigilos — crear, cargar, quemar, regalo por entidad (`/api/sigilo*`)
- [x] Grimorio + Memoria + Decisiones (`/api/grimorio`, `/api/memoria/*`, `/api/decisiones`)
- [x] Cosmología + Stats (`/api/cosmologia`, `/api/stats`)

### Fase 2 — Sistemas de adivinación
- [x] I Ching — hexagramas, consulta (`/api/iching/*`)
- [x] Geomancia — figuras, lectura (`/api/geomancia/*`)
- [x] Servitors — crear, invocar, disolver, feed, estado, lista (`/api/servitors/*`)
- [x] Gnosis — guía, métodos, recomendar (`/api/gnosis/*`)
- [x] Runas — lista, tirada (`/api/runas/*`)

### Fase 3 — Magia del caos avanzada
- [x] Discordia / Oráculo caótico (`/api/discord/oraculo`)
- [x] Sync colectiva — nueva, lista, confirmar, colectiva (`/api/sync/*`)
- [x] Rayos — catálogo, preguntas, test (`/api/rayos/*`)
- [x] Paradigm shifting — iniciar, estado, checkin, catálogo (`/api/paradigm/*`)
- [x] Cerrar entidad (`/api/cerrar/<entidad>`)
- [x] Mensajes — quemar (`/api/mensajes/quemar`)

### El Bosque (fase actual)
- [x] Esferas colectivas — 4 tipos (geo/elemental/temática/resonancia), amplitud, decaimiento 14/30/60d
- [x] Estratos — sotobosque/dosel/emergentes visible en terminal (`/api/bosque/estratos`)
- [x] Mapa del bosque — nodos y links para visualización (`/api/bosque/mapa`)
- [x] Salud del bosque — métricas básicas (`/api/bosque/salud`)
- [x] Marcar esfera — resonancia desde `/api/bosque/marcar`
- [x] Ciclo de decaimiento — `/api/bosque/ciclo` actualiza estados
- [x] Geografía — 14 ecorregiones WWF de Sudamérica (`geografia.py`)
- [x] Eje del Mundo — especie árbol emblemática por ecorregión (`/api/geografia/eje`)
- [x] GestorGeografico — resuelve texto libre → ecorregión; fallback al Mar de Kali
- [x] Astral — carta natal via kerykeion, offline (`/api/astral/*`)

---

## Pendiente

### P1 — Ciclo de muerte completo
**Qué falta:** las esferas solo tienen 4 estados (activa/letargo/disolviendo/disuelta).
La doctrina define 3 fases con semántica distinta:
1. `en_pie` — dejó de responder con fuerza, pero su forma es consultable
2. `raiz_espera` — puede rebotar si vuelven marcas (rebrote desde lo guardado)
3. `humus` — se disolvió; vuelve como nutriente al suelo (no se borra, se transforma)

**Archivos:** `esferas.py`, `base_datos.py` (migración de columna `estado`), `servidor.py`
**Criterio de done:** una esfera marcada hace 90 días pasa por los tres estados; `/api/bosque/salud`
muestra cuántas están en cada estado; rebrotar devuelve la esfera desde `raiz_espera` al llegar
una nueva marca.

---

### P2 — Entidades como datos (tabla, no código)
**Qué falta:** las 5 entidades originales siguen hardcodeadas en `DEIDADES` (probablemente en
`servidor.py` o `grimorio_base.py`). La doctrina dice que cada entidad debe ser una fila en tabla
con `estado = 'canon'`, extensible sin tocar código.

**Archivos:** `base_datos.py` (tabla `entidades`), script de migración/seed, `servidor.py`
**Criterio de done:** `DEIDADES` se elimina del código; las 5 se cargan desde la tabla al iniciar;
agregar una entidad nueva es un INSERT, no un deploy.

---

### P3 — Firma planetaria de entidades
**Qué falta:** la cadena planeta → metal → piedra → sistema cristalino por entidad.
`astral.py` ya computa planetas. Falta la tabla de correspondencias y exponerla.

**Archivos:** archivo nuevo `planetas.py` o extensión de `astral.py`, `base_datos.py`
**Criterio de done:** `/api/cosmologia` devuelve `firma_planetaria` para cada entidad;
incluye metal, piedra y sistema cristalino.

---

### P4 — Capa planetaria completa en el reloj
**Qué falta:** horas y días planetarios para _timing_ ritual. `astral.py` tiene la carta natal
pero no el ciclo diario de horas planetarias (secuencia caldea).

**Archivos:** `astral.py` o nuevo `planetas.py`
**Criterio de done:** `/api/luna` (o nuevo endpoint `/api/planetas/hora`) devuelve el planeta
regente de la hora actual y el del día; funciona offline.

---

### P5 — Micorriza: ritual de cruce entre burbujas
**Qué falta:** todo. Es el corazón del ecosistema colectivo. Dos practicantes se "cruzan"
deliberadamente; sus entidades dialogan; emerge saber compartido. Si ambas entidades están en
Emergentes, puede nacer una entidad híbrida (génesis).

**Archivos:** nuevo `micorriza.py`, `base_datos.py` (tablas `cruces`, `hibridos`), `servidor.py`
**Criterio de done:**
- `POST /api/micorriza/iniciar` — un proyecto propone cruce con otro (por código hasheado)
- `POST /api/micorriza/aceptar` — el otro acepta; se registra el cruce
- `GET /api/micorriza/dialogo` — devuelve saber emergente del cruce
- Si ambas entidades son Emergentes: `POST /api/micorriza/genesis` inicia el híbrido
- Privacidad: el código del otro nunca se almacena en claro; solo sus hashes y los fragmentos
  emergentes (sin contenido íntimo)

---

### P6 — Genética de híbridos
**Qué falta:** cuando dos Emergentes se cruzan y se activa génesis, el hijo hereda atributos
por dominancia + recombinación (no promedio). Rasgo por rasgo, con entropía real.

**Depende de:** P2 (entidades como datos) + P5 (micorriza)
**Archivos:** `micorriza.py` (lógica de herencia), `base_datos.py`
**Criterio de done:** una entidad híbrida tiene `padre_a`, `padre_b`, `generacion = 1`; sus
atributos (elemento, dirección, color, árbol) se asignaron aleatoriamente con sesgo de dominancia;
aparece en `/api/bosque/estratos` con estado `sotobosque`.

---

### P7 — Avatar de tres prendas
**Qué falta:** el practicante tiene un avatar (Cuerpo/Alma/Espíritu) que evoluciona con su
práctica y le da acceso al espacio colectivo. No existe todavía.

**Archivos:** nuevo `avatar.py`, `base_datos.py` (tabla `avatares`), `servidor.py`
**Criterio de done:**
- Todo proyecto nuevo nace con prenda `cuerpo` (entrada libre)
- `GET /api/avatar` — devuelve prendas actuales + condición para la siguiente
- `POST /api/avatar/alma` — otorga prenda Alma si condiciones cumplidas (ascenso propio +
  resonancia recibida de otras burbujas)
- `POST /api/avatar/espiritu` — ritual de iniciación; requiere Cuerpo + Alma previos
- El avatar con Alma puede iniciar cruces de micorriza (desbloquea P5)

---

### P8 — Dos espacios: ruka privada / claro colectivo
**Qué falta:** una separación explícita en la UI terminal entre el espacio privado (mi bosque,
mis entidades) y el espacio colectivo (el claro del ngillatún: mapa vivo, jardín de especies,
resonancias colectivas). Actualmente el bosque mezcla ambos.

**Archivos:** `src/bosque.js`, `src/ui.js`, posiblemente un nuevo panel en `src/panels.html`
**Criterio de done:** el terminal tiene dos modos `/bosque privado` y `/bosque colectivo`;
el colectivo muestra esferas de **otras** burbujas (sin revelar su contenido).

---

### P9 — Tectónica real (sismos y mareas)
**Qué falta:** Caicai (mareas) y Trentren (sismos) como datos reales. Las mareas ya se pueden
computar desde `luna.py`. Los sismos vienen de la USGS Earthquake API (gratis, sin key).

**Archivos:** nuevo `tectonica.py`, `servidor.py` (endpoint `/api/bosque/tectonica`)
**Criterio de done:** `/api/bosque/tectonica` devuelve sismos recientes filtrados por zona +
mareas del día; si la API está caída, el sistema funciona igual (fallback: relieve estático).
El nivel del suelo en la zona del practicante refleja el balance solve/coagula local.

---

### P10 — Salud del bosque como métrica completa
**Qué falta:** `/api/bosque/salud` existe pero es básico. La doctrina define 6 métricas:
diversidad de especies, relevo generacional, vitalidad del sotobosque, densidad de la micorriza,
equilibrio elemental (solve/coagula), sucesión.

**Depende de:** P5 (micorriza) para la densidad de cruces
**Archivos:** `esferas.py` o `bosque.py` (si se extrae), `servidor.py`
**Criterio de done:** `/api/bosque/salud` devuelve las 6 métricas con valores numéricos y
un diagnóstico textual ("bosque seco", "bosque equilibrado", "sotobosque activo", etc.).

---

### P11 — Clima real opcional
**Qué falta:** el clima endógeno ya funciona (`modificacion_deidades` en `luna.py`). El
enriquecimiento opcional es una API de clima externo (p.ej. Open-Meteo, gratis, sin key)
que modula el bosque si hay red.

**Archivos:** nuevo `clima.py`, integración en `geografia.py`
**Criterio de done:** si hay red, `/api/geografia/eje` incluye `clima_real` (temperatura,
humedad, condición); si no hay red, devuelve `clima_endogeno` (deidades + luna). El sistema
nunca falla por ausencia de clima real.

---

### P12 — Graph view con frontend
**Qué falta:** `/api/bosque/mapa` ya devuelve nodos y links. Falta una visualización que
los muestre — en el terminal (ASCII/canvas) o en una página web aparte.

**Archivos:** `src/bosque.js` (panel terminal) o nuevo `src/graph.js`
**Criterio de done:** el comando `/bosque mapa` en el terminal muestra los nodos del bosque
con sus conexiones; los emergentes se distinguen visualmente de los jóvenes y el sotobosque.

---

## Orden sugerido de implementación

```
P1  → ciclo de muerte completo          (base para todo lo demás)
P2  → entidades como datos              (desbloquea P3, P6)
P3  → firma planetaria                  (completa la cosmología)
P4  → capa planetaria (horas/días)      (completa el reloj)
P7  → avatar de tres prendas            (desbloquea P5)
P5  → micorriza                         (corazón colectivo)
P6  → genética de híbridos              (depende P2 + P5)
P8  → dos espacios UI                   (depende P5)
P10 → salud completa                    (depende P5 para micorriza)
P12 → graph view                        (depende P10)
P9  → tectónica real                    (enriquecimiento; puede ir en cualquier momento)
P11 → clima real                        (enriquecimiento; puede ir en cualquier momento)
```

---

## Lo que NO se toca (reglas duras)

- `grimorio.html` sigue siendo **un solo archivo**
- Sin usuarios, sin login, sin emails, sin IPs almacenadas
- El código de proyecto nunca se guarda en claro
- Toda invocación al LLM pasa por `ClienteGroq` (único punto de cambio de proveedor)
- Migraciones de esquema deben preservar datos existentes
- El sistema funciona sin internet y sin `GROQ_API_KEY`
