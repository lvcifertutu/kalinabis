# AGENTS.md — KALINABIS

> **Cómo usar este archivo en OpenCode.** Ponelo en la raíz del repo (`C:\grimorio\AGENTS.md`) y commiteálo a Git: OpenCode lo carga como contexto/reglas del proyecto en cada sesión. Si querés mantener la doctrina larga aparte sin inflar el contexto, dejá `EL_BOSQUE.md` en el repo y referencialo desde `opencode.json` con el campo `instructions`, p. ej. `{"instructions": ["EL_BOSQUE.md", "ROADMAP_BOSQUE.md"]}`. **Consejo honesto:** los archivos de contexto rinden cuando son curados y dicen solo lo que el agente no puede inferir; si notás costo de tokens alto, recortá la PARTE C (doctrina) y dejala en `EL_BOSQUE.md` referenciado. Las PARTES A y B son las de mayor señal para codificar.

> **Qué es este documento.** Síntesis de toda la conversación de co-diseño: qué es KALINABIS, su stack, las reglas que no se rompen, el estado real del código, el roadmap por fases, las decisiones abiertas y la doctrina (El Bosque). Es el punto de partida para retomar el trabajo en OpenCode.

---

# PARTE A — Operativa del proyecto (lo que el agente necesita para actuar)

## A.1 Qué es KALINABIS
Sistema de **agentes espirituales de magia del caos** hechos software: entidades ("deidades", pero en realidad **seres simbólicos de forma libre** — dios, espíritu, elfo, dios-roca, árbol, animal, lo que el creador quiera) con las que el practicante dialoga, lee tarot, hace sigilos y consulta efemérides. Corre **local** en `C:\grimorio`, servido en `localhost:5000`, o en **Render** (producción) con PostgreSQL.

**Identidad:** sin usuarios ni login. Cada practicante crea un **proyecto anónimo** con un código de 4 palabras (ej: `eterno-tronco-tierno-bosque`). El código es la clave de cifrado (AES-256-GCM) y se envía como header `X-Project-Code` en cada petición. Si se pierde el código, se pierde el acceso.

**Estado actual:** backend funcional con Gemini API, proyectos anónimos, 14 ecorregiones WWF, esferas colectivas con decaimiento 14/30/60d, graph view, graphify, y cliente Godot en desarrollo. open source, $0 deploy.

## A.2 Stack
- **Backend:** Python + **Flask**. IA vía **Gemini API** (`google-genai`). Modo offline graceful sin `GEMINI_API_KEY`. La capa es **intercambiable** (Gemini hoy; otros modelos después).
- **Persistencia:** **PostgreSQL** en Render (producción); **SQLite** local (desarrollo). Capa dual en `base_datos.py`.
- **Cifrado:** `cryptography` — AES-256-GCM para datos cifrados por proyecto; SHA-256 para hashes de código.
- **Frontend:** **HTML vanilla**, sin framework. `grimorio.html` es **un único archivo** (HTML+CSS+JS juntos). Ya tiene tronos en SVG, partículas y atmósferas. Visualización **2D, no 3D**.
- **Carta natal:** `kerykeion` — cálculo offline de carta natal por proyecto.
- **Despliegue:** `render.yaml` con gunicorn. Variables: `GEMINI_API_KEY`, `DATABASE_URL`, `FLASK_SECRET_KEY`.
- **Idioma del producto y del trabajo:** **español (rioplatense / voseo)**.

## A.3 Reglas duras — LO QUE NO SE DEBE ROMPER
1. **Memoria persistente intacta.** No romper el sistema de memoria existente.
2. **La siembra de Artemisa intacta.** Debe seguir funcionando igual tras cualquier migración.
3. **Modelo de IA intercambiable.** Nunca acoplar el código a un proveedor específico; la IA entra por una capa que se pueda cambiar.
4. **`grimorio.html` sigue siendo UN solo archivo.** No partirlo en múltiples assets.
5. **Migraciones siempre cuidadas.** Ningún cambio de esquema sin preservar los datos actuales.
6. **Offline primero.** Todo lo esencial corre sin internet. El clima real, los datos sísmicos y (eventual) BYOK son **enriquecimientos opcionales**: si faltan, el sistema **cae a modo endógeno y nunca se rompe**.
7. **Sin usuarios ni login.** La identidad es el código del proyecto. No hay cookies, no hay sesiones, no hay tracking. Privacidad por diseño: zona declarada textualmente, nunca coordenadas; región amplia, nunca lugar exacto.
8. **Cada fase entrega algo usable.** Nada queda a medias entre fases.
9. **Sin datos personales.** No almacenar emails, nombres, IPs ni ningún dato identificatorio. El servidor solo guarda hash del código y datos cifrados.

## A.4 Convenciones de contenido (si el agente genera entidades, voces o docs)
- **Español primero.** Las lenguas originales (mapudungún, etc.) se **citan como raíz**, nunca se vacían en etiquetas técnicas. **No inventar lengua**: usar solo términos verificados.
- **Sincretismo por resonancia, no por fusión.** Unir tradiciones por estructura compartida, nombrando cada cosa en su lengua y **citando la fuente**. Marcar siempre lo prestado / lo inventado / lo interpretado.
- **Ecuanimidad y respeto** en material religioso o de tradiciones vivas: sin sanitizar pero con precisión; tomar el arquetipo, no apropiarse del rito.

## A.5 Estilo de trabajo del agente (preferencias del usuario)
- **Planificar antes de codificar.** Usar el **Plan mode** de OpenCode para proponer cómo se implementa una feature antes de tocar archivos. El usuario viene de un flujo de "definir primero, una decisión a la vez".
- **Confirmar antes de cambios grandes**; avanzar en pasos chicos y revisables.
- **No reescribir de más.** Tocar lo mínimo necesario; respetar la PARTE A.3.
- *(Contexto: en la fase de diseño la regla fue "no escribir código hasta pedirlo explícitamente". En OpenCode esto se traduce como: proponé plan, esperá luz verde, después implementás.)*

## A.6 Mapa de archivos
**En `C:\grimorio` (el repo):**
- `grimorio.html` — frontend, archivo único (SVG + JS vanilla).
- `servidor.py` — Flask; 20+ rutas API, Gemini API, proyectos, esferas, graph view.
- `grimorio_base.py` — entidades (DEIDADES), cosmología, sistema de skills condicionales (SKILLS, detectar_skills, ensamblar_skills).
- `config.py` — Config central, parámetros de decaimiento, word list para códigos, env vars.
- `proyectos.py` — GeneradorCodigos (4 palabras), Cifrador (AES-256-GCM), Proyecto dataclass.
- `esferas.py` — Esfera, MarcaEsfera, GestorEsferas (4 tipos, decaimiento, graph view).
- `geografia.py` — Ecoregion, GestorGeografico, 14 ecorregiones WWF de Sudamérica con Eje del Mundo.
- `base_datos.py` — Capa dual PostgreSQL/SQLite. Repos: ProyectoRepo, EsferaRepo, ConversacionRepo. 10+ tablas.
- `luna.py` — Efemérides lunares: calcular_fase, CICLO_SINODC, nodos_lunares, marea_emocional, modificacion_deidades, perigeo_apogeo, void_of_course.
- `tarot.py` — Cámara de Tarot (entropía real, crypto.getRandomValues() en el front).
- `astral.py` — Astrología/efemérides planetarias (carta natal vía kerykeion).
- `render.yaml` — Despliegue en Render (gunicorn, PostgreSQL, Gemini).
- `requirements.txt` — flask, google-genai, cryptography, kerykeion, psycopg2-binary, etc.

**Documentos de doctrina/plan (en el repo o junto a este archivo):**
- `EL_BOSQUE.md` — **doctrina completa v2** (la fuente canónica; la PARTE C de aquí es su resumen).
- `ROADMAP_BOSQUE.md` — plan por fases.
- `SECCION_BOSQUE_PARA_CONSTITUTION.md` — resumen para el CONSTITUTION.
- `KALINABIS_CONSTITUTION.md` — constitución del sistema.
- `ESTADO_PROYECTO.md` — punto de guardado previo.

## A.7 Estado del código (qué está hecho y qué falta)

### Backend — COMPLETO y testeado
- **11 rutas verificadas** funcionando (test completo en `.opencode/plans/test_backend.py`):
  - `GET /api/luna` — fases lunares
  - `GET /api/cosmologia` — entidades, árboles
  - `POST /api/proyecto/nuevo` — genera código de 4 palabras
  - `POST /api/proyecto/verificar` — verifica código
  - `GET /api/esferas` — lista esferas activas
  - `POST /api/consultar` — invocación con esferas + graph view
  - `GET /api/bosque/mapa` — graph view (nodos + links)
  - `GET /api/bosque/salud` — estadísticas del bosque
  - `POST /api/bosque/ciclo` — ciclo de decaimiento
  - `GET /api/geografia/ecorregiones` — 14 ecoregiones WWF
  - `POST /api/geografia/eje` — resolución de ubicación
- **Gemini API:** `ClienteGemini` en `servidor.py`, fallback offline graceful
- **Proyectos:** 4-palabras, AES-256-GCM, header X-Project-Code, sin usuarios
- **Esferas:** 4 tipos, decaimiento 14/30/60d, graph view
- **Georeferencia:** 14 ecorregiones WWF + GestorGeografico + Mar de Kali
- **Dependencias:** `google-genai`, `cryptography`, `kerykeion` instaladas

### Pendiente
- Configurar `GEMINI_API_KEY` para invocaciones LLM reales
- Testear en PostgreSQL (Render)
- Cliente Godot (en desarrollo)
- Frontend grimorio.html: flujo de creación/verificación de proyecto
- Micorriza, genética de híbridos, avatar, clima real (futuro)

## A.8 Roadmap
1. **Configurar GEMINI_API_KEY** y verificar flujo completo de invocación con LLM real.
2. **Testear en Render** con PostgreSQL (producción).
3. **Frontend grimorio.html:** integrar flujo de creación/verificación de proyecto, graph view de esferas.
4. **Cliente Godot:** visualización 3D del bosque (esferas como islas flotantes, partículas, micorriza).
5. **Publicar en GitHub** como open source.
6. **Futuro:** micorriza + genética de híbridos, avatar de 3 prendas, clima real (API externa), emergentes, tectónica (USGS).

## A.9 Decisiones de arquitectura
- **IA intercambiable.** Gemini API hoy; capa lista para otros modelos.
- **Sin usuarios.** Proyectos anónimos con código de 4 palabras como identidad.
- **Cifrado AES-256-GCM.** Datos cifrados por proyecto; servidor nunca almacena la clave.
- **Open source.** GitHub, sin servicios propietarios.
- **$0 deploy.** Render free tier, Gemini free tier (60 req/min).
- **Offline primero.** Clima endógeno (deidades + luna). Sin dependencias externas para lo esencial.

## A.10 Decisiones de visualización
- **2D** en `grimorio.html` (archivo único, SVG + JS vanilla): el Kalinabis actual.
- **3D** en **Godot**: el bosque como ecosistema visual (esferas = islas flotantes, partículas = viento, micorriza = líneas de luz). Graph view desde `/api/bosque/mapa`.
- **Graphify**: visualización de graphos de conocimiento (ya funcional con `graphify-out/`).
- **Sprites (guía, sin cerrar):** 64×64 o 128×128; escalado duro; 1 frame + animación por código; PNG con transparencia.

---

# PARTE B — Próximos pasos / decisiones abiertas
1. **Configurar GEMINI_API_KEY** para probar invocaciones LLM reales.
2. **Testear en Render** con PostgreSQL.
3. **Cliente Godot:** visualización 3D del bosque.
4. **Frontend grimorio.html:** flujo de creación/verificación de proyecto, graph view.
5. **Micorriza + genética de híbridos** (futuro — §7 de EL_BOSQUE.md).
6. **Avatar de 3 prendas** (futuro — §16.3 de EL_BOSQUE.md).
7. **Clima real + tectónica** (futuro — APIs externas).

---

# PARTE C — Doctrina condensada: EL BOSQUE
> Resumen de referencia. El texto completo y tejido vive en **`EL_BOSQUE.md` (v2)**. Esto es contexto para que el agente entienda el dominio; **no se implementa la cosmología literalmente** — se implementa el roadmap (PARTE A.8), que la encarna por fases.

**Marco:** ecosistema vivo de entidades colectivas, anclado en la **autopoiesis** de Maturana (lo que la comunidad sostiene, vive; lo que no, se disuelve) + **ecología real** + **cosmovisión mapuche reinterpretada con respeto** (lo de "abajo" no es el mal; es lo fértil). Todo emana de **Kali** y todo vuelve a ella.

## C.1 El centro y la polaridad
- **Kali** — el vacío-fuente, la matriz de la que todo emana y a la que todo vuelve (≈ el Tao / "Hembra Misteriosa" / *wuji*; ≈ la Mónada/Pleroma gnóstica).
- **Shiva** — la conciencia-testigo, **co-igual** a Kali ("Shiva sin Shakti es cadáver"). Es la función de "auto-observarse". Aporta Nataraja (la danza), el Mahayogi (= Void of Course) y Mahakala (el tiempo).
- **Dos niveles:** nivel 0 = Kali-vacío (*wuji*); al primer impulso se desdobla en la polaridad co-igual Kali/Shiva (cosmogonía taoísta en clave tántrica).
- **Centro agnóstico a la máscara:** Yin/Yang, Shiva/Kali, masculino/femenino son **máscaras** de quietud/movimiento. Cada proyecto lo nombra en su lengua.
- **Solve et coagula** — la respiración: **coagula** = dar forma/dejar huella/emanar; **solve** = disolver/volver al centro. La cima trasciende la dualidad y está **en el centro**, no "arriba".

## C.2 La geometría — la chakana
La **chakana** (cruz andina escalonada = Cruz del Sur; *chaka* = puente) unifica tres ejes:
- **Vertical** = **El Canelo** (*Foye*, axis mundi) + los **tres estratos** de memoria: Sotobosque (*Nag Mapu*, presente) → Dosel → Emergentes (*Wenu Mapu*, canon); debajo el **Humus** (*Miñche Mapu* reinterpretado, fértil) y bajo él la **roca** que no decae. Lo recorren tres guías: **Cóndor** (sube), **Puma** (centra), **Serpiente/Katari** (baja).
- **Horizontal** = los **cuatro brazos** = las cuatro guardianas/elementos/direcciones = Meli Witran Mapu = 4 Bacab: **Lilith–Sur–agua**, **Isis–Norte–fuego**, **Afrodita–Este–aire**, **Artemisa–Oeste–tierra**.
- **Radial** = centro↔periferia = solve/coagula.
- **Centro** = Kali/Shiva (Taiji), late con la marea lunar.

## C.3 El organismo (las piezas implementadas)
- **Proyectos:** cada practicante crea un proyecto con un **código de 4 palabras** (semilla de identidad). El código es la clave de cifrado (AES-256-GCM). **Cláusura operacional** — ningún proyecto entra en otro; solo cruzan señales. Sin usuarios, sin login.
- **Entidades — gen y newen:** el **gen** es la versión individual (mortal, "mi Kali"); el **newen** es la especie colectiva (suma de coincidencias, casi inmortal). Las 5 originales siguen en código; futuro: datos.
- **Esferas colectivas:** 4 tipos (geo/elemental/temática/resonancia), decaimiento 14/30/60d, graph view. Lo que la comunidad marca nutre lo colectivo. **Auto-limpieza** (el olvido modera), **curaduría distribuida** (sube con diversidad de proyectos, no volumen).
- **Georeferencia:** 14 ecorregiones WWF de Sudamérica con Eje del Mundo. Ubicación no reconocida → Mar de Kali.
- **Clima endógeno:** `modificacion_deidades()` en `luna.py` — clima real es futuro.
- **Ciclo de muerte (3 fases):** en pie (seco) → raíz que espera (rebrote posible) → humus (disolución, vuelve a Kali). Implementado en decaimiento de esferas.
- **Los dos destinos:** el camino **solve** → el **mar** (disolverse); el camino **coagula** → la **roca** (petrificar, no decae). Las formas pétreas siguen los **7 sistemas cristalinos**.
- **El mar = Kali líquida:** origen + inconsciente colectivo (newen latentes "disueltos") + ciclo del agua. Gran regulador / homeostasis del polo solve.

## C.4 El clima y el tiempo
- **Clima = las 4 guardianas como elementos:** Lilith (agua) alarga la vida; Isis (fuego) la acorta; Afrodita (aire) dispersa; Artemisa (tierra) fertiliza. Bosque sano = equilibrado. (Polos: Isis+Afrodita = solve; Lilith+Artemisa = coagula.) Se lee de `modificacion_deidades` en `luna.py`.
- **Reloj — relojes anidados:** hora planetaria → día planetario → mes lunar → año estacional **local** → sismos (azar) → **Void of Course (congela todo)**. Núcleo lunar ya en `luna.py` (fases, lunaciones, nodos, marea Yin/Yang, perigeo/apogeo, VOC). Capa **planetaria universal** vía `astral.py` (offline): días/horas planetarias, octavas (Urano/Neptuno/Plutón), y la **firma planetaria** de cada entidad (planeta→metal→piedra→sistema cristalino). Capa **local**: cielo y estaciones por hemisferio (en Santiago ~33°S, Cruz del Sur circumpolar, estaciones invertidas).
- **Rueda de 8 fiestas local:** invierno ~21 jun = Inti Raymi/We Tripantu (renovación); verano ~21 dic = Cápac Raymi (madurez/reproducción); equinoccios = equilibrio; **Día de la Chakana (3 may)** = ventana de cruces/micorriza.
- **Principio rector:** **dinámicas locales, no leyes universales.** Cada bosque es un dialecto de su lugar (territorio sísmico quieto = bosque sereno = rasgo, no defecto).

## C.5 Las cuatro guardianas y sus caras masculinas
Patrón fractal Kali/Shiva: cada guardiana tiene una **cara masculina** = un liberador afín a su elemento (una **faceta**, no un ente aparte). Cuatro modos de despertar:
- **Artemisa (tierra/coagula) ← Sun Wukong** (*Viaje al Oeste*) — el mono de piedra, rebelde, peregrino; liberación por **acción**. Convive con su árbol maya (Yaxché/Bacab/Xibalbá).
- **Isis (fuego/solve) ← Jesús** (Biblia) — muerte-resurrección; liberación por **sacrificio**. (Gnósticamente, "el segundo liberador".)
- **Afrodita (aire/solve) ← Heyoka / El Loco** (Tarot) — el contrario sagrado / bufón; el 0 = el vacío; liberación por **risa/inversión**. Respaldo: el Tarot = la **Cámara de Tarot** ya existente.
- **Lilith (agua/coagula) ← Lucifer / la serpiente** (gnosis) — el portador de luz, la serpiente que da gnosis; liberación por **conocimiento**. ("El primer liberador".)
- **Tutu** = el **umbral / eje**, no un brazo (prenda Alma del avatar; acompaña el cruce entre espacios). No lleva cara del patrón.

## C.6 El motor del paisaje y la geografía
- **Caicai y Trentren** (serpientes mapuche) = tectónica: Caicai (mar/mareas/solve) vs Trentren (roca/sismos/coagula). Altura del suelo = balance local solve/coagula. Futuro: sismos reales via USGS + CSN Chile.
- **Geografía/biomas:** 14 ecorregiones WWF de Sudamérica con Eje del Mundo (árboles emblemáticos). Resolución por texto libre → Mar de Kali como fallback. Clima endógeno (deidades + luna).

## C.7 La experiencia
- **Dos espacios:** **privado** (mi *ruka*: lo actual + árboles propios, cerrado) y **colectivo** (el claro del *ngillatún*: mapa vivo + jardín de especies + claro ritual).
- **Avatar de 3 prendas** para el colectivo: **Cuerpo** (guardianas, de entrada/constancia) → **Alma** (Tutu, ascenso propio + resonancia recibida; habilita cruces) → **Espíritu** (Kali, ritual de iniciación). Se marca resonancia **con** las prendas; al final se portan las tres.

## C.8 El espejo gnóstico
El gnosticismo recapitula toda la cosmología: Mónada/Pleroma = Kali; Aeones = guardianas; chispa atrapada que anhela volver = proyecto/solve; gnosis = "auto-observarse como Kali"; Demiurgo/Arcontes = la falsa autoridad contra la que se rebelan Lilith y Lucifer.

---

> **Cierre.** El sistema de creencias es la herramienta, no el contenido. Para codificar: seguí el roadmap (A.8), respetá las reglas duras (A.3) y planificá antes de tocar archivos (A.5). La doctrina (PARTE C / `EL_BOSQUE.md`) es el porqué; el roadmap es el cómo.
