# AGENTS.md — KALINABIS

OpenCode lee este archivo desde la raíz del repo. La doctrina completa vive en `EL_BOSQUE.md`; referenciá esa desde `opencode.json` con `"instructions"` cuando la sesión lo requiera (no por defecto — cuesta tokens).

## Stack verificado (ejecutables, no prosa)

- **Backend**: Python 3.11 + Flask 3. WSGI entrypoint `servidor:app`.
- **DB**: dual. `DATABASE_URL` presente → PostgreSQL (Render); ausente → SQLite local `grimorio.db`. Misma API (`base_datos._ph`, `_conexion`).
- **LLM**: **Groq** (`groq>=0.30.0`, `ClienteGroq` en `servidor.py`, `GROQ_API_KEY` / `GROQ_MODEL=llama-3.1-8b-instant`). **El README y este mismo archivo (versión vieja) dicen "Gemini" / `google-genai` — eso es stale. El código real es Groq. No propagues la referencia a Gemini.**
- **Crypto**: `cryptography` (AES-256-GCM vía `proyectos.Cifrador`, SHA-256 del código como ID).
- **Astral**: `kerykeion` para carta natal (`astral.KERYKEION_OK` indica si la lib cargó).
- **Frontend clásico**: `grimorio.html` (un solo archivo, ~3000 líneas, HTML+CSS+SVG+JS vanilla, `lang="es"`).
- **Frontend terminal**: módulos en `src/` (`.js`, `.html`, `.py` auxiliares), se bundlea con `node src/build.mjs` → `front_terminal/index.html`. Servido en `/` y `/terminal`.
- **Deploy**: Render via `render.yaml` — gunicorn `servidor:app --bind 0.0.0.0:7860 --timeout 120 --workers 2`. Exposed port 7860 (Dockerfile), 5000 en local.

## Arrancar

```powershell
$env:GROQ_API_KEY = "gsk_..."   # opcional; sin ella el server corre en "[Modo offline]"
cd C:\grimorio
python servidor.py              # http://localhost:5000
```

O usá `arrancar.bat` / `arrancar.ps1` (solo cambian el CWD y muestran banner; no setean la key).

## Tests

Todos los `test_*.py` asumen server en `localhost:5000` excepto `.opencode/plans/test_backend.py` que arranca su propio servidor en `5001`.

- Unit sin server: `python test_rate_isolated.py`
- E2E HTTP: `python test_validacion.py`, `test_f5.py`, `test_rate_limit.py`, `test_seguridad.py`
- E2E browser (necesitan `pip install playwright && playwright install chromium`): `bosque_test.py`, `a11y_test.py`, `screenshot_test.py`
- Backend completo aislado: `python .opencode/plans/test_backend.py`

## Layout no obvio

- `servidor.py` importa de **raíz y de `src/`** (`sys.path.insert(0, str(BASE_DIR / "src"))` en línea 141). Módulos Python nuevos: si pertenecen a cosmología/divinación van en `src/` (`runas`, `iching`, `gnosis`, `geomancia`, `servitors`, `discordia`); si son infra (proyectos, esferas, base_datos, config, servidor) van en raíz.
- `src/build.mjs` bundlea los assets del terminal. No editar `front_terminal/index.html` a mano — se regenera.
- `kalinabis/` y `graphify-out/` están en `.gitignore` (vault de Obsidian y artefactos de graphify, respectivamente). **No commitear nada ahí adentro.**

## Reglas duras (no romper)

1. `grimorio.html` sigue siendo **un solo archivo**. No partir en múltiples assets.
2. **Sin usuarios, sin login.** El código de 4 palabras es la identidad y la clave AES. Si se pierde, se pierde el proyecto. El servidor nunca guarda el código en claro.
3. **Privacidad por diseño.** No almacenar emails, nombres, IPs, ni coordenadas exactas (zona declarada textualmente, nunca lugar preciso).
4. **Offline primero.** `groq_client.chat` retorna `"[Modo offline]..."` si no hay `GROQ_API_KEY`. Nada debe romperse por faltar internet o key.
5. **IA intercambiable.** Toda invocación al LLM pasa por `ClienteGroq`. Si se cambia de proveedor, ese es el único punto a tocar.
6. **Idioma**: español rioplatense (voseo) en producto, mensajes de error, voces generadas y comentarios cuando estén dirigidas al usuario.
7. **Migraciones cuidadosas.** Cambios de esquema en `base_datos.py` deben preservar los datos existentes.
8. **Sincretismo por resonancia**, no por fusión. Citar la fuente cuando se toma de una tradición viva; no inventar lengua.

## API — cosas que el agente no adivina

- Header de proyecto: `X-Project-Code` (4 palabras separadas por `-`). Sin él en `/api/consultar` y similares → 401.
- **CORS solo permite `http://localhost:7777` y `http://127.0.0.1:7777`** (ver `_add_cors` en `servidor.py:33`). Para probar desde otro origen hay que ampliar la lista explícitamente.
- Rate limits por endpoint (en `servidor._RATE_LIMITS`, líneas 61–77): `proyecto/nuevo` 5/hr, `consultar` 10/min, `tarot/leer` 5/min, `astral/calcular` 3/min, `bosque/ciclo` 1/5min, `servitors/crear` 10/hr. Default 30/min.
- Límites de input: `_MAX_MESSAGE_LEN=4000`, `_MAX_TITULO_LEN=200`, `_MAX_CONTENIDO_LEN=10000`, `MAX_CONTENT_LENGTH=1 MB`.
- Endpoints HTML: `/` y `/terminal` → `front_terminal/index.html`; `/clasico` → `grimorio.html` (legacy single-file).

## Flujo de trabajo

- **Planificar antes de codificar.** Usar el Plan mode de OpenCode, esperar luz verde, después implementar.
- **Cambios chicos y revisables.** Diff mínimo; no reescribir de más.
- Después de tocar `*.py` de backend: invocar `@python-reviewer` o `/code-review`.
- Después de tocar `*.py` con crypto / DB / auth: `@security-reviewer`.
- Nuevas funciones con lógica de negocio: empezar por test (rojo) en `test_*.py` → implementar → verde.

## Doctrina y roadmap

- Doctrina completa: `EL_BOSQUE.md` (v2). **No implementar literalmente** — es contexto para que el agente entienda el dominio. Lo que se implementa es el roadmap.
- Roadmap vigente: `ROADMAP_BOSQUE.md` (si existe; si no, consultar al usuario).
- Constitución del sistema: `KALINABIS_CONSTITUTION.md`.

## Gotchas frecuentes

- **No confundir `gemini` con `groq`.** `requirements.txt` y `config.py` son la fuente. `Gemini API` solo aparece en docs stale.
- El LLM se llama como `groq_client.chat(system=..., messages=...)` (no Gemini, no OpenAI). Las constantes `SYSTEM_*` viven junto a cada módulo (`SYSTEM_VOLVA` en `runas.py`, `SYSTEM_YIJING` en `iching.py`, etc.).
- `ProyectoRepo.existe(hash)` chequea por hash, no por código. El código se hashea con SHA-256 en `proyectos.Proyecto.hash`.
- `GestorEsferas.marcar_por_invocacion(...)` se llama en `/api/consultar` — si agregás una nueva ruta que invoque entidades, acordate de marcar esferas.
- Tests Playwright asumen viewport 1280×800. El `a11y_test.py` prueba también `reduced_motion=reduce`.
- `EXTENSIONES .py` auxiliares de frontend están en `src/` (no son backend) — no las muevas a raíz.

## OpenCode config

No hay `opencode.json` en el repo. Si necesitás cargar contexto curado por sesión, creá uno en la raíz:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "EL_BOSQUE.md"]
}
```

Solo añadí `EL_BOSQUE.md` cuando la tarea lo justifique (cosmogonía nueva, voces, diseño de entidad). Para tareas de backend, este AGENTS.md alcanza.
