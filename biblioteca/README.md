# BIBLIOTECA DE KALINABIS
## Repositorio de Saberes Documentados

> Esta biblioteca es el archivo de investigación del sistema. No es el canon de Kalinabis (eso es `CANON_KALINABIS.md`) — es la **fuente** de la que el canon bebe. Cada documento aquí es investigación documentada, con fuentes primarias citadas, que fundamenta los conceptos del sistema.
>
> La biblioteca no prescribe creencias. Ofrece mapas. El practicante decide con qué mapas trabaja.

---

## Estructura

```
biblioteca/
├── README.md                           ← Este índice
│
├── taoismo/
│   └── TAOISMO_PROFUNDO.md             ← Tao, Wu Wei, Tres Tesoros, Neidan, Wu Xing
│
└── cuerpo_energetico/
    └── MAPA_CUERPO.md                  ← Cartografías del cuerpo en 6 tradiciones
```

---

## Documentos disponibles

### Taoísmo
| Documento | Contenido | Estado |
|-----------|-----------|--------|
| [TAOISMO_PROFUNDO.md](taoismo/TAOISMO_PROFUNDO.md) | El Tao, Wu Wei, Te, Jing/Qi/Shen, Tres Dantians, Neidan, Wu Xing, textos fuente | Completo |

### Cuerpo Energético
| Documento | Contenido | Estado |
|-----------|-----------|--------|
| [MAPA_CUERPO.md](cuerpo_energetico/MAPA_CUERPO.md) | Taoísmo, Tantra Hindu, Tibet, Andino, Kabbalah, tabla comparativa | Completo |

---

## Cómo leer esta biblioteca

**Si quieres entender el taoísmo de raíz:** Lee `TAOISMO_PROFUNDO.md` de principio a fin. Es el documento más denso — tómate tiempo.

**Si quieres entender tu propio cuerpo como mapa energético:** Lee `MAPA_CUERPO.md`. Está diseñado para consultarse por secciones.

**Si eres desarrollador:** Los documentos de biblioteca son la fuente de verdad para cualquier feature que involucre mapas del cuerpo, cinco elementos, chakras, o taoísmo. No implementar conceptos sin haber leído el documento correspondiente.

---

## Sistema comunitario

La biblioteca es un sistema vivo. Las entradas tienen un ciclo de vida:

```
semilla → brote → árbol → canon
   ↓ (sin verificación)
  humus
```

- **semilla:** recién creada, sin fuentes ni resonancia comunitaria
- **brote:** al menos 1 fuente + resonancia ≥ 1.0
- **árbol:** 3+ fuentes verificadas, resonancia ≥ 5.0, sin cuestionamientos abiertos
- **canon:** elevada por el sistema (los documentos de esta carpeta), inmutable
- **humus:** archivada — no eliminada, disponible como substrato histórico

### Resonancias (validación anónima)

Cualquier practicante con código de proyecto puede marcar una entrada:

| Tipo | Peso | Significado |
|------|------|-------------|
| `reconozco` | +0.5 | "Lo he encontrado en mi práctica" |
| `verifico` | +1.0 | "Puedo confirmar con fuente" |
| `cuestiono` | -0.5 | "Tengo dudas — abre debate" |
| `amplio` | +0.2 | "Quiero expandir esta entrada" |

### API de la biblioteca

```
GET  /api/biblioteca/dominios
GET  /api/biblioteca/entradas          ?dominio= &estado= &q= &limite= &offset=
GET  /api/biblioteca/entradas/:slug
POST /api/biblioteca/entradas          (requiere X-Project-Code)
POST /api/biblioteca/entradas/:slug/fuente
POST /api/biblioteca/entradas/:slug/resonancia   (requiere X-Project-Code)
POST /api/biblioteca/entradas/:slug/contribuir   (requiere X-Project-Code)
GET  /api/biblioteca/entradas/:slug/contribuciones
```

---

## Principios de la biblioteca

1. **Cada afirmación tiene fuente** — se cita el texto original, el autor y si existe una edición académica de referencia.
2. **Se distingue lo documentado de lo interpretado** — cuando Kalinabis hace una conexión entre tradiciones, se marca como conexión propia, no como hecho histórico.
3. **Las tradiciones vivas se tratan con respeto** — el taoísmo, el hinduismo tántrico, el budismo tibetano son sistemas vivos practicados hoy. No se los reduce a "fuentes de metáforas".
4. **La biblioteca crece** — si una implementación requiere investigar una nueva tradición, el documento correspondiente se agrega aquí antes de tocar el código.
5. **La verificación es comunitaria y automática** — no hay moderadores. Las fuentes y las resonancias determinan el estado de cada entrada.
