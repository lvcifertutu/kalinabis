-- ═══════════════════════════════════════════════════════════════════════
-- Biblioteca Colectiva — Dominio Consensual
--
-- Pegar en Supabase → SQL Editor y ejecutar.
-- El backend (Flask) usa la service role key y bypasea RLS.
-- El frontend usa la anon key y solo ve conocimiento validado.
-- ═══════════════════════════════════════════════════════════════════════


-- ── 1. Tablas ────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS biblioteca_entradas (
    id              SERIAL PRIMARY KEY,
    titulo          TEXT NOT NULL,
    slug            TEXT NOT NULL UNIQUE,
    dominio         TEXT NOT NULL,
    contenido       TEXT NOT NULL,
    estado          TEXT NOT NULL DEFAULT 'semilla',
    fuentes_count   INTEGER NOT NULL DEFAULT 0,
    resonancia      REAL NOT NULL DEFAULT 0.0,
    hash_autor      TEXT,
    creado_en       TEXT NOT NULL,
    actualizado_en  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS biblioteca_fuentes (
    id          SERIAL PRIMARY KEY,
    entrada_id  INTEGER NOT NULL REFERENCES biblioteca_entradas(id),
    tipo        TEXT NOT NULL,
    referencia  TEXT NOT NULL,
    verificada  INTEGER NOT NULL DEFAULT 0,
    creado_en   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS biblioteca_contribuciones (
    id                SERIAL PRIMARY KEY,
    entrada_id        INTEGER NOT NULL REFERENCES biblioteca_entradas(id),
    tipo              TEXT NOT NULL,
    contenido         TEXT NOT NULL,
    estado            TEXT NOT NULL DEFAULT 'pendiente',
    resonancia_pro    INTEGER NOT NULL DEFAULT 0,
    resonancia_contra INTEGER NOT NULL DEFAULT 0,
    hash_autor        TEXT,
    creado_en         TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS biblioteca_resonancias (
    id            SERIAL PRIMARY KEY,
    entrada_id    INTEGER NOT NULL REFERENCES biblioteca_entradas(id),
    tipo          TEXT NOT NULL,
    hash_proyecto TEXT NOT NULL,
    creado_en     TEXT NOT NULL,
    UNIQUE (entrada_id, hash_proyecto, tipo)
);


-- ── 2. Índices ───────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_bib_entradas_slug
    ON biblioteca_entradas (slug);

CREATE INDEX IF NOT EXISTS idx_bib_entradas_dominio
    ON biblioteca_entradas (dominio);

CREATE INDEX IF NOT EXISTS idx_bib_entradas_estado
    ON biblioteca_entradas (estado);

CREATE INDEX IF NOT EXISTS idx_bib_fuentes_entrada
    ON biblioteca_fuentes (entrada_id);

CREATE INDEX IF NOT EXISTS idx_bib_contrib_entrada
    ON biblioteca_contribuciones (entrada_id);

CREATE INDEX IF NOT EXISTS idx_bib_reson_entrada
    ON biblioteca_resonancias (entrada_id);


-- ── 3. RLS ───────────────────────────────────────────────────────────────

ALTER TABLE biblioteca_entradas       ENABLE ROW LEVEL SECURITY;
ALTER TABLE biblioteca_fuentes        ENABLE ROW LEVEL SECURITY;
ALTER TABLE biblioteca_contribuciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE biblioteca_resonancias    ENABLE ROW LEVEL SECURITY;

-- Entradas: el conocimiento que ya emergió del acoplamiento es público.
-- Semilla = aún no es del dominio consensual; solo su autor la ve.
-- Humus = disuelta; nadie la lee (sin política = denegado).

CREATE POLICY "entradas: dominio público"
ON biblioteca_entradas FOR SELECT
TO anon, authenticated
USING (estado IN ('brote', 'arbol', 'canon'));

CREATE POLICY "entradas: semilla propia"
ON biblioteca_entradas FOR SELECT
TO authenticated
USING (
    estado = 'semilla'
    AND hash_autor = current_setting('app.proyecto_hash', true)
);

-- Fuentes: visibles si la entrada ya es pública.

CREATE POLICY "fuentes: lectura pública"
ON biblioteca_fuentes FOR SELECT
TO anon, authenticated
USING (
    EXISTS (
        SELECT 1 FROM biblioteca_entradas e
        WHERE e.id = entrada_id
          AND e.estado IN ('brote', 'arbol', 'canon')
    )
);

-- Contribuciones: solo las aprobadas son parte del dominio consensual.

CREATE POLICY "contribuciones: aprobadas públicas"
ON biblioteca_contribuciones FOR SELECT
TO anon, authenticated
USING (estado = 'aprobada');

-- Resonancias: el acoplamiento es visible para todos.

CREATE POLICY "resonancias: lectura pública"
ON biblioteca_resonancias FOR SELECT
TO anon, authenticated
USING (true);

-- Escritura: el backend usa service role key (bypasea RLS).
-- No se necesitan políticas INSERT/UPDATE/DELETE para anon/authenticated.


-- ── 4. Semillas canónicas ────────────────────────────────────────────────
-- Opcional: migrar las 8 entradas canónicas existentes desde SQLite.
-- Ver: biblioteca/ en el repo para el contenido fuente.
-- Correr: python -c "from tools.migrar_biblioteca import migrar; migrar()"
-- (script pendiente de implementar)
