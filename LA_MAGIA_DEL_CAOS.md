# KALINABIS — La Magia del Caos
## El fundamento práctico del sistema

> **Qué es este documento.** Define la base de magia del caos (*chaos magic*) sobre la que se diseña la experiencia de Kalinabis. Mientras `EL_BOSQUE.md` describe la *cosmología* (el porqué simbólico), este documento describe la *práctica* (el qué se hace). Cada experiencia de usuario debe poder mapearse a una técnica real de magia del caos, o ser una innovación propia marcada como tal (como El Bosque).
>
> **Estado:** doctrina de diseño. Guía la implementación de las experiencias del chatbox y más allá.
>
> **Relación con El Bosque:** El Bosque es la cosmología endógena de Kalinabis (innovación propia). La magia del caos es el método universal. El Bosque NO es magia del caos tradicional — es la mitología viva que Kalinabis construye sobre la práctica.

---

## 0. Principio rector

La magia del caos (Peter J. Carroll, Austin Osman Spare, Ray Sherwin, fines del s. XX) tiene un axioma central:

> **"Nada es verdad, todo está permitido."** (Hassan-i Sabbah, vía William S. Burroughs)

La creencia es una **herramienta**, no un dogma. El practicante adopta y descarta sistemas de creencia según lo que funcione. Esto es el **paradigm shifting** (cambio de paradigma): mantener una creencia con la suficiente ligereza para cambiarla, y con la suficiente intensidad para que funcione mientras se usa.

**Por qué Kalinabis ya ES magia del caos:**
- Las **deidades** (Isis, Lilith, Afrodita, Artemisa, Tutu) son *godforms* — estructuras de creencia con las que el practicante interactúa.
- Las **esferas colectivas** son *egregores* — entidades sostenidas por la atención de muchos.
- La **filosofía de máscaras** del lore ("Yin/Yang, Shiva/Kali son máscaras intercambiables") ES el paradigm shifting.
- Los **sigilos** y el **tarot** ya son técnicas core implementadas.

El trabajo de esta fase es **hacer explícita** esa naturaleza y **completar el toolkit**.

---

## 1. Las técnicas core de la magia del caos

### 1.1 Sigilización *(YA EXISTE — sigilos.js)*
Un sigilo es un símbolo que representa un deseo, con las palabras originales removidas para ocultarlo de la mente consciente.

**Proceso clásico (Spare/Carroll):**
1. Escribir una declaración de intención clara ("ES MI VOLUNTAD…")
2. Remover letras repetidas
3. Combinar las letras restantes en un símbolo abstracto
4. Olvidar el significado
5. **Cargar** el sigilo durante gnosis
6. Destruir/olvidar el sigilo

**Estado en Kalinabis:** La cámara de sigilos permite dibujar sigilos por deidad. **Falta:** el flujo guiado de declaración → símbolo → carga con gnosis.

### 1.2 Gnosis *(NUEVO — la pieza más importante)*
El estado alterado de conciencia que **carga** la intención, sorteando al "censor psíquico" (la mente racional dubitativa). Sin gnosis, ninguna técnica funciona. Tres caminos:

| Camino | Vía | Métodos | En Kalinabis |
|---|---|---|---|
| **Inhibitoria** | el monje | meditación, respiración lenta, quietud, fijar la vista | Guía de respiración 4-7-8, fijar el sigilo |
| **Excitatoria** | el chamán | danza, tambores, respiración rápida, emoción intensa | Audio rítmico (ya hay audio.js), respiración de fuego |
| **Vacuidad indiferente** | apatheia | aburrir/ignorar la mente, escritura automática | Sigilo a la vista que se vuelve invisible |

**Diseño Kalinabis:** Antes de cargar un sigilo o invocar profundamente, ofrecer una **guía de gnosis** — un mini-ritual de respiración o trance, acompañado de audio y visuales (las partículas ya existen). Cada deidad sugiere su camino afín:
- **Lilith** (agua/instinto) → excitatoria (respiración de fuego, intensidad)
- **Afrodita** (aire/mente) → inhibitoria (quietud, claridad)
- **Isis** (fuego/corazón) → excitatoria suave (calidez, emoción)
- **Artemisa** (tierra/colectivo) → inhibitoria (enraizamiento, paciencia)

### 1.3 Servidores (Servitors) *(NUEVO)*
Un servidor es un *thought-form* — una entidad psíquica semi-autónoma creada para una tarea específica y continua. Es la "fauna menor" del bosque de cada proyecto.

**Proceso:**
1. Definir un **propósito** claro y acotado (ej: "recordarme respirar cuando me estreso")
2. Darle un **nombre** y una **forma** (un sigilo, una imagen)
3. **Cargarlo** con gnosis
4. Establecer **límites** (qué hace, qué no, cuánto vive)
5. **Disolverlo** cuando cumple su función (higiene psíquica — crucial)

**Diseño Kalinabis:** El practicante crea servidores propios dentro de su proyecto. Viven en el **sotobosque** (estrato presente). Si no se renuevan/usan, **decaen** (igual que las esferas — ya hay mecánica de decaimiento). Conecta con el ciclo de muerte de 3 fases del Bosque: en pie → raíz que espera → humus. Un servidor disuelto vuelve a Kali.

### 1.4 Godforms / Formas-dios *(YA EXISTE — las deidades)*
Estructuras de creencia complejas, a menudo sostenidas por muchas personas, con las que el mago interactúa para intenciones amplias.

**Estado en Kalinabis:** Las 4 guardianas + Tutu SON godforms. El newen (especie colectiva) vs gen (versión individual) ya distingue el godform universal del personal.

### 1.5 Egregores *(YA EXISTE — las esferas)*
Entidades colectivas mantenidas por la atención de un grupo. Lo que la comunidad sostiene, vive; lo que se olvida, se disuelve.

**Estado en Kalinabis:** Las esferas colectivas con decaimiento 14/30/60d SON egregores con autopoiesis. Esto ya está más desarrollado que en la mayoría de sistemas de magia del caos.

### 1.6 Hypersigil *(NUEVO)*
Concepto de Grant Morrison (*The Invisibles*): un sigilo extendido en el tiempo a través de **narrativa**. En vez de un símbolo, se escribe una **historia en pasado** donde el objetivo YA se cumplió. El acto sostenido de crear la narrativa es la carga.

**Diseño Kalinabis:** El **grimorio personal de cada proyecto** PUEDE ser un hypersigil. El practicante escribe entradas narrativas (con ayuda de las deidades) sobre la vida que está manifestando. El proyecto entero, escrito en el tiempo, se vuelve un hypersigil vivo. Conecta con el "decir bajo el Canelo" (marcar como verdad).

### 1.7 Trabajo de Sombra / Illumination *(NUEVO)*
La aplicación de las técnicas para auto-conocimiento. Confrontar e integrar aspectos rechazados del yo (la "sombra" junguiana).

**Proceso:**
1. Crear espacio sagrado (ritual de destierro)
2. Definir el aspecto de sombra a confrontar (miedo, ira, culpa, vergüenza)
3. Entrar en gnosis y llamar al aspecto a la conciencia
4. Dialogar con él para entender su propósito y necesidad
5. Integrar

**Diseño Kalinabis:** Esto YA TIENE infraestructura — el **árbol de muerte (qliphoth)** está en `grimorio_base.py`. Cada qliphoth es una sombra de un sephiroth. El practicante puede hacer trabajo de sombra dialogando con la deidad sobre un qliphoth específico. Conecta con "lo de abajo no es el mal" (el humus fértil del Bosque) y con el bardo del *dharmata* (deidades airadas = proyecciones de la propia mente).

### 1.8 Ritual de Destierro (Banishing) *(NUEVO — formalizar)*
Limpieza del espacio psíquico antes/después de trabajar. Disipa "escombros psíquicos", permite entrar en estados alterados, y ordena el universo simbólicamente (el mago se para en el *axis mundi*). En la magia del caos, cada practicante **crea su propio** ritual de destierro (es requisito del Liber MMM de Carroll).

**Diseño Kalinabis:** "Cerrar el ritual" ya existe parcialmente. Formalizarlo como un acto de apertura Y cierre. El **Canelo** (axis mundi del Bosque) es el lugar perfecto para pararse. Cada proyecto puede diseñar su propio gesto de destierro (coherente con la filosofía DIY de la magia del caos).

### 1.9 Sincronicidad *(NUEVO)*
Notar coincidencias significativas como retroalimentación del trabajo mágico. No es causal — es la mente reconociendo patrones que confirman que la intención está operando.

**Diseño Kalinabis:** Un **registro de sincronicidades** — el practicante anota coincidencias que nota tras un trabajo. Conecta con las "señales que cruzan" entre proyectos (clausura operacional del Bosque) y con la marea del inconsciente colectivo (el mar de Kali).

---

## 2. Mapa de experiencias para el usuario

Ordenadas de la más simple (entrada) a la más profunda (avanzada):

### Nivel 1 — Diálogo (YA EXISTE)
Hablar con las deidades. El chatbox actual. **Mejora:** que cada deidad pueda *ofrecer* un ritual cuando detecta que el practicante lo necesita ("¿Quieres que te guíe en un sigilo para esto?").

### Nivel 2 — Sigilo guiado (MEJORAR lo existente)
Flujo completo: declaración de intención → generación/dibujo del sigilo → guía de gnosis → carga → liberación. La deidad acompaña según su elemento.

### Nivel 3 — Gnosis (NUEVO)
Mini-rituales de estado alterado. Respiración guiada (visual + audio), con las partículas y campanillas que ya existen. Standalone o como paso de carga.

### Nivel 4 — Servidor (NUEVO)
Crear, nombrar, cargar y eventualmente disolver una entidad-tarea propia. Vive en el sotobosque del proyecto.

### Nivel 5 — Trabajo de sombra (NUEVO)
Diálogo guiado con un aspecto de sombra, usando los qliphoth ya en código. La deidad afín acompaña (Lilith para la ira, Afrodita para la confusión, etc.).

### Nivel 6 — Hypersigil (NUEVO)
El grimorio personal como narrativa de manifestación sostenida en el tiempo.

### Transversal — Destierro y Sincronicidad
Apertura/cierre de cada sesión + registro de coincidencias.

---

## 3. Reglas de diseño (coherencia con el resto del sistema)

1. **Respeto a la práctica real.** Las técnicas se presentan fieles a sus fuentes (Spare, Carroll, Morrison, Hine). Donde Kalinabis innova (el Bosque, las 4 guardianas específicas), se marca como propio.
2. **DIY primero.** La magia del caos es individualista. El sistema *sugiere* pero el practicante *adapta*. Nunca imponer un único método correcto.
3. **Sin sustancias.** La gnosis se guía solo por métodos seguros y legales: respiración, meditación, movimiento, sonido. NUNCA sugerir sustancias (la *chemognosis* queda fuera del producto por responsabilidad).
4. **Offline graceful.** Todas las experiencias esenciales (sigilos, gnosis, servidores, sombra) funcionan sin LLM. El LLM enriquece el diálogo; no es requisito para practicar.
5. **El Bosque es el contenedor.** Cada técnica de magia del caos se expresa en el lenguaje del Bosque: servidores = fauna menor, hypersigil = decir bajo el Canelo, sombra = bajar al humus, gnosis = la marea que sube.
6. **Higiene psíquica.** Toda creación (servidor, godform invocado) debe poder disolverse. El ciclo de muerte de 3 fases del Bosque ya provee el modelo.
7. **Sin promesas de resultados.** Kalinabis es una herramienta de práctica y exploración interior, no un sistema que promete manifestar deseos materiales. El marco es psicológico/simbólico.

---

## 4. Próximos pasos de implementación

Estas experiencias se integran en las fases del plan general:

- **Fase 1 (prompts):** Las deidades ahora saben de magia del caos. Pueden *ofrecer* rituales y guiar gnosis afín a su elemento. → actualizar prompts con esta capa.
- **Fase 2 (contexto):** El contexto astronómico modula qué ritual conviene (luna llena = cargar; luna nueva = disolver/sombra).
- **Fase 4 (frontend):** Las nuevas experiencias (gnosis, servidores, sombra) son nuevas vistas/modales en `grimorio.html`.
- **Backend nuevo:** endpoints para servidores (`/api/servidor/nuevo`, `/api/servidor/disolver`), sincronicidades (`/api/sincronicidad`), y trabajo de sombra (reusa `/api/consultar` con contexto qliphoth).

---

> **Cierre.** Kalinabis no inventa una religión: ofrece un taller de magia del caos vestido con una cosmología viva (el Bosque). El practicante usa técnicas reales y probadas —sigilos, gnosis, servidores, godforms, hypersigils— dentro de un mundo simbólico propio que crece con la comunidad. La creencia es la herramienta; el Bosque es el lenguaje; la práctica es el contenido.
