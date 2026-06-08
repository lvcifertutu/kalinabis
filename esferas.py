from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, ClassVar

from config import Config
from base_datos.esferas import (
    EsferaRepo, RelacionRepo, EventoRepo, HumusRepo, ConvergenciaRepo, PARES_POLARES,
)
from base_datos.proyecto import ProyectoRepo, ConversacionRepo


@dataclass
class Esfera:
    tipo: str
    clave_unica: str
    metadata: dict = field(default_factory=dict)
    amplitud: float = 1.0
    fase_decaimiento: str = "activa"
    created_at: str = ""
    updated_at: str = ""

    @property
    def amplitud_actual(self) -> float:
        if not self.updated_at:
            return self.amplitud
        try:
            ultimo = datetime.fromisoformat(self.updated_at)
        except (ValueError, TypeError):
            return self.amplitud
        dias = (datetime.now() - ultimo).total_seconds() / 86400.0
        factor = max(0.0, 1.0 - dias / Config.DECAY_DISOLUCION_TOTAL_DIAS)
        return round(self.amplitud * factor, 4)

    @property
    def fase_viva(self) -> str:
        if self.amplitud_actual <= 0:
            return "disuelta"
        try:
            ultimo = datetime.fromisoformat(self.updated_at)
        except (ValueError, TypeError):
            return self.fase_decaimiento
        dias = (datetime.now() - ultimo).total_seconds() / 86400.0
        if dias >= Config.DECAY_DISOLUCION_TOTAL_DIAS:
            return "disuelta"
        elif dias >= Config.DECAY_DISOLUCION_PARCIAL_DIAS:
            return "disolviendo"
        elif dias >= Config.DECAY_LETARGO_DIAS:
            return "letargo"
        return "activa"

    def a_dict(self) -> dict:
        return {
            "tipo": self.tipo,
            "clave_unica": self.clave_unica,
            "metadata": self.metadata,
            "amplitud": self.amplitud,
            "amplitud_actual": self.amplitud_actual,
            "fase_decaimiento": self.fase_decaimiento,
            "fase_viva": self.fase_viva,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class MarcaEsfera:
    tipo_esfera: str
    clave_esfera: str
    proyecto_hash: str
    timestamp: str


class GestorEsferas:
    TIPOS_VALIDOS = frozenset([
        "geo", "elemental", "tematica", "resonancia",
        "intencion",       # servitors activos
        "sincronicidad",   # syncs registradas / confirmadas
        "conocimiento",    # entradas de biblioteca con resonancia
        "paradigma",       # paradigmas completados
    ])
    MAPA_ELEMENTOS = {
        "fuego": "isis", "norte": "isis",
        "aire": "afrodita", "este": "afrodita",
        "agua": "lilith", "sur": "lilith",
        "tierra": "artemisa", "oeste": "artemisa",
    }

    @classmethod
    def marcar(cls, tipo: str, clave_unica: str,
               metadata: dict | None = None,
               proyecto_hash: str | None = None) -> dict:
        tipo = tipo.lower()
        if tipo not in cls.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de esfera inválido: {tipo}. "
                             f"Válidos: {', '.join(sorted(cls.TIPOS_VALIDOS))}")
        if not clave_unica or not clave_unica.strip():
            raise ValueError("clave_unica es requerida")

        clave = clave_unica.strip().lower()
        esfera = EsferaRepo.crear_o_actualizar(tipo, clave, metadata)

        if proyecto_hash:
            EsferaRepo.agregar_marca(tipo, clave, proyecto_hash)

        cls._detectar_relaciones(tipo, clave, proyecto_hash)

        if proyecto_hash:
            cls._detectar_convergencias(tipo, clave)

        return Esfera(
            tipo=esfera["tipo"],
            clave_unica=esfera["clave_unica"],
            metadata=esfera.get("metadata", {}),
            amplitud=esfera["amplitud"],
            fase_decaimiento=esfera["fase_decaimiento"],
            created_at=esfera.get("created_at", ""),
            updated_at=esfera.get("updated_at", ""),
        ).a_dict()

    @classmethod
    def marcar_por_invocacion(cls, entidad: str, ubicacion: str | None,
                              concepto: str | None,
                              proyecto_hash: str | None = None) -> list[dict]:
        resultados = []
        esferas_previas = {
            (e["tipo"], e["clave_unica"])
            for e in EsferaRepo.listar_activas(amplitud_minima=0.01)
        }

        tipo_elemental = cls._entidad_a_elemento(entidad)
        if tipo_elemental:
            r = cls.marcar(
                "elemental", tipo_elemental,
                {"entidad": entidad, "elemento": tipo_elemental},
                proyecto_hash
            )
            if ("elemental", tipo_elemental) not in esferas_previas:
                EventoRepo.registrar(
                    "rito_origen", "elemental", tipo_elemental,
                    amplitud_momento=r.get("amplitud_actual", 1.0),
                    detalle={"entidad": entidad, "ubicacion": ubicacion},
                    proyecto_hash=proyecto_hash, entidad=entidad,
                )
            resultados.append(r)

        if ubicacion and ubicacion.strip():
            from geografia import GestorGeografico
            eco = GestorGeografico.resolver(ubicacion)
            if eco:
                r = cls.marcar(
                    "geo", eco.codigo_wwf,
                    {"ecoregion": eco.nombre, "eje": eco.eje_del_mundo},
                    proyecto_hash
                )
                if ("geo", eco.codigo_wwf) not in esferas_previas:
                    EventoRepo.registrar(
                        "rito_origen", "geo", eco.codigo_wwf,
                        amplitud_momento=r.get("amplitud_actual", 1.0),
                        detalle={"entidad": entidad, "ubicacion": ubicacion,
                                 "ecoregion": eco.nombre},
                        proyecto_hash=proyecto_hash, entidad=entidad,
                    )
                resultados.append(r)
            else:
                resultados.append(cls.marcar(
                    "geo", "MAR_DE_KALI",
                    {"nota": "Ubicación no reconocida — emerge del Mar de Kali"},
                    proyecto_hash
                ))

        if concepto and concepto.strip():
            c = concepto.strip().lower()
            r = cls.marcar(
                "tematica", c,
                {"concepto": concepto.strip()},
                proyecto_hash
            )
            if ("tematica", c) not in esferas_previas:
                EventoRepo.registrar(
                    "rito_origen", "tematica", c,
                    amplitud_momento=r.get("amplitud_actual", 1.0),
                    detalle={"entidad": entidad, "concepto": concepto.strip()},
                    proyecto_hash=proyecto_hash, entidad=entidad,
                )
            resultados.append(r)

        return resultados

    @classmethod
    def _detectar_relaciones(cls, tipo: str, clave: str,
                             proyecto_hash: str | None) -> None:
        """Auto-detecta y registra relaciones entre la esfera recién marcada y
        otras esferas activas, según reglas semánticas del bosque."""
        try:
            activas = EsferaRepo.listar_activas(amplitud_minima=0.5)
        except Exception:
            return

        activas_idx: dict[tuple, dict] = {
            (e["tipo"], e["clave_unica"]): e for e in activas
        }

        # ── convoca: intencion → geo ──────────────────────────────────────
        if tipo == "intencion":
            for (et, ec), e in activas_idx.items():
                if et == "geo":
                    RelacionRepo.crear_o_fortalecer(
                        tipo, clave, et, ec, "convoca", proyecto_hash
                    )

        # ── toca: sincronicidad → elemental ───────────────────────────────
        elif tipo == "sincronicidad":
            for (et, ec), e in activas_idx.items():
                if et == "elemental":
                    RelacionRepo.crear_o_fortalecer(
                        tipo, clave, et, ec, "toca", proyecto_hash
                    )

        # ── ancla: conocimiento → tematica ────────────────────────────────
        elif tipo == "conocimiento":
            for (et, ec), e in activas_idx.items():
                if et == "tematica":
                    RelacionRepo.crear_o_fortalecer(
                        tipo, clave, et, ec, "ancla", proyecto_hash
                    )

        # ── amplifica: conocimiento → conocimiento del mismo dominio ──────
        # (si dos entradas de biblioteca comparten prefijo de dominio)
        if tipo == "conocimiento":
            dominio_base = clave.split("-")[0] if "-" in clave else clave
            for (et, ec), e in activas_idx.items():
                if et == "conocimiento" and ec != clave and ec.startswith(dominio_base):
                    RelacionRepo.crear_o_fortalecer(
                        tipo, clave, et, ec, "amplifica", proyecto_hash
                    )

        # ── coemergencia: misma sesión de proyecto, tipos distintos ───────
        if proyecto_hash:
            try:
                from datetime import timedelta
                from base_datos._helpers import _conexion, _ph
                limite_tiempo = (datetime.now() - timedelta(hours=1)).isoformat()
                with _conexion() as (con, cur):
                    cur.execute(
                        f"SELECT DISTINCT tipo_esfera, clave_esfera FROM marcas_esfera "
                        f"WHERE proyecto_hash = {_ph(1)} AND timestamp >= {_ph(1)}",
                        (proyecto_hash, limite_tiempo),
                    )
                    recientes = cur.fetchall()
                for r in recientes:
                    if r[0] != tipo and r[1] != clave:
                        rel = RelacionRepo.crear_o_fortalecer(
                            tipo, clave, r[0], r[1], "coemergencia", proyecto_hash
                        )
                        if rel.get("nueva"):
                            EventoRepo.registrar(
                                "coemergencia", tipo, clave,
                                amplitud_momento=0.0,
                                detalle={"esfera_par": f"{r[0]}:{r[1]}"},
                                proyecto_hash=proyecto_hash,
                            )
            except Exception:
                pass

        # ── polariza: elementales opuestos en alta amplitud ───────────────
        if tipo == "elemental":
            for (et, ec), e in activas_idx.items():
                if et == "elemental" and ec != clave:
                    if frozenset([clave, ec]) in PARES_POLARES:
                        if e.get("amplitud", 0) >= 1.5:
                            rel = RelacionRepo.crear_o_fortalecer(
                                tipo, clave, et, ec, "polariza", proyecto_hash
                            )
                            if rel.get("nueva"):
                                EventoRepo.registrar(
                                    "polarizacion", tipo, clave,
                                    amplitud_momento=e.get("amplitud", 0),
                                    detalle={"esfera_polar": f"{et}:{ec}",
                                             "fuerza_polar": rel["fuerza"]},
                                    proyecto_hash=proyecto_hash,
                                )

    @classmethod
    def _detectar_convergencias(cls, tipo: str, clave: str) -> None:
        """Detecta si esta esfera + otras forman una señal colectiva (N proyectos).

        Por cada convergencia nueva encontrada:
        - Crea/fortalece una relación 'resuena' entre las esferas convergentes.
        - Registra un evento 'convergencia' en el log del bosque.
        """
        try:
            detectadas = ConvergenciaRepo.detectar_para(tipo, clave)
        except Exception:
            return

        for c in detectadas:
            if not c.get("nueva"):
                continue
            try:
                RelacionRepo.crear_o_fortalecer(
                    c["tipo_a"], c["clave_a"],
                    c["tipo_b"], c["clave_b"],
                    "resuena",
                )
                EventoRepo.registrar(
                    "convergencia",
                    tipo, clave,
                    detalle={
                        "par_a": f"{c['tipo_a']}:{c['clave_a']}",
                        "par_b": f"{c['tipo_b']}:{c['clave_b']}",
                        "n_proyectos": c["n_proyectos"],
                    },
                )
            except Exception:
                pass

    @classmethod
    def _entidad_a_elemento(cls, entidad: str) -> str | None:
        ent = entidad.lower().strip()
        mapa = {
            "isis": "fuego", "afrodita": "aire",
            "lilith": "agua", "artemisa": "tierra",
        }
        return mapa.get(ent)

    @classmethod
    def listar_activas(cls, tipo: str | None = None,
                       amplitud_min: float = 0.01) -> list[dict]:
        filas = EsferaRepo.listar_activas(tipo, amplitud_min)
        return [
            Esfera(
                tipo=f["tipo"], clave_unica=f["clave_unica"],
                metadata=f.get("metadata", {}),
                amplitud=f["amplitud"],
                fase_decaimiento=f["fase_decaimiento"],
                created_at=f.get("created_at", ""),
                updated_at=f.get("updated_at", ""),
            ).a_dict()
            for f in filas
        ]

    @classmethod
    def ejecutar_ciclo_decaimiento(cls) -> dict:
        todas = EsferaRepo.listar_todas()
        actualizadas = 0
        disueltas = 0
        now = datetime.now()

        # Índice de amplitud actual por (tipo, clave) para detectar absorción
        amp_idx: dict[tuple, float] = {
            (e["tipo"], e["clave_unica"]): e["amplitud"]
            for e in todas
        }

        for esf in todas:
            try:
                updated = datetime.fromisoformat(esf["updated_at"])
            except (ValueError, TypeError):
                continue

            dias = (now - updated).total_seconds() / 86400.0
            amp_base = esf["amplitud"]
            factor = max(0.0, 1.0 - dias / Config.DECAY_DISOLUCION_TOTAL_DIAS)
            amp_nueva = round(amp_base * factor, 4)

            if factor <= 0:
                nueva_fase = "disuelta"
            elif dias >= Config.DECAY_DISOLUCION_PARCIAL_DIAS:
                nueva_fase = "disolviendo"
            elif dias >= Config.DECAY_LETARGO_DIAS:
                nueva_fase = "letargo"
            else:
                nueva_fase = "activa"

            if amp_nueva != amp_base or nueva_fase != esf["fase_decaimiento"]:
                EsferaRepo.actualizar_fase_decaimiento(
                    esf["tipo"], esf["clave_unica"],
                    amp_nueva, nueva_fase
                )
                actualizadas += 1

            if amp_nueva <= 0 and amp_base > 0:
                disueltas += 1

                # Determinar causa: ¿murió sola o fue absorbida?
                causa, absorbida_por = cls._causa_disolucion(
                    esf["tipo"], esf["clave_unica"], amp_idx
                )

                # Contar ofrendas que dejó
                try:
                    from base_datos.esferas import OfrendaRepo as _OR
                    ofrendas_count = _OR.conteo(esf["tipo"], esf["clave_unica"])
                except Exception:
                    ofrendas_count = 0

                # Depositar humus
                HumusRepo.depositar(
                    tipo=esf["tipo"],
                    clave_unica=esf["clave_unica"],
                    causa=causa,
                    amplitud_final=amp_base,
                    dias_activa=round(dias, 1),
                    ofrendas_count=ofrendas_count,
                    absorbida_por=absorbida_por,
                )

                EventoRepo.registrar(
                    "esfera_disuelve",
                    esf["tipo"], esf["clave_unica"],
                    amplitud_momento=0.0,
                    detalle={
                        "dias_activa": round(dias, 1),
                        "causa": causa,
                        "absorbida_por": absorbida_por,
                        "ofrendas_depositadas": ofrendas_count,
                    },
                )

        return {
            "total_esferas": len(todas),
            "actualizadas": actualizadas,
            "disueltas": disueltas,
            "timestamp": now.isoformat(),
        }

    @classmethod
    def _causa_disolucion(
        cls,
        tipo: str,
        clave: str,
        amp_idx: dict[tuple, float],
    ) -> tuple[str, str | None]:
        """Determina si una esfera murió sola o fue absorbida por otra más fuerte.

        Una esfera es 'absorbida' cuando existe otra esfera del mismo tipo
        con amplitud ≥ 2× la suya — la más fuerte consumió su energía.
        Retorna (causa, clave_absorbedora | None).
        """
        amp_propia = amp_idx.get((tipo, clave), 0)
        umbral = max(amp_propia * 2.0, 1.5)

        candidata = None
        max_amp = 0.0
        for (t, c), amp in amp_idx.items():
            if t == tipo and c != clave and amp >= umbral and amp > max_amp:
                candidata = c
                max_amp = amp

        if candidata:
            return "absorbida", f"{tipo}:{candidata}"
        return "decaimiento_natural", None

    @classmethod
    def obtener_mapa(cls) -> dict:
        esferas = cls.listar_activas()
        proyectos_activos = ProyectoRepo.total_activos()

        nodos: list[dict] = [
            {
                "id": f"esfera:{e['tipo']}:{e['clave_unica']}",
                "tipo": "esfera",
                "subtipo": e["tipo"],
                "amplitud": e["amplitud_actual"],
                "fase": e["fase_viva"],
                "label": f"{e['tipo']}: {e['clave_unica']}",
                "metadata": e.get("metadata", {}),
            }
            for e in esferas
        ]

        # Aristas reales tipadas (del grafo de relaciones)
        try:
            relaciones = RelacionRepo.listar_todas(fuerza_min=0.5)
        except Exception:
            relaciones = []

        links: list[dict] = [
            {
                "source": f"esfera:{r['tipo_a']}:{r['clave_a']}",
                "target": f"esfera:{r['tipo_b']}:{r['clave_b']}",
                "tipo": r["tipo_relacion"],
                "fuerza": r["fuerza"],
            }
            for r in relaciones
        ]

        # Aristas de mismo-tipo como red de fondo (peso menor)
        ids_activos = {f"esfera:{e['tipo']}:{e['clave_unica']}" for e in esferas}
        visto: set = set()
        for i, a in enumerate(esferas):
            for b in esferas[i + 1:]:
                if a["tipo"] == b["tipo"]:
                    par = frozenset([a["clave_unica"], b["clave_unica"]])
                    if par not in visto:
                        visto.add(par)
                        links.append({
                            "source": f"esfera:{a['tipo']}:{a['clave_unica']}",
                            "target": f"esfera:{b['tipo']}:{b['clave_unica']}",
                            "tipo": "mismo_tipo",
                            "fuerza": 0.3,
                        })

        return {
            "nodos": nodos,
            "links": links,
            "estadisticas": {
                "total_esferas": len(esferas),
                "total_relaciones": len(relaciones),
                "proyectos_activos": proyectos_activos,
                "esferas_por_tipo": cls._contar_por_tipo(esferas),
            },
            "timestamp": datetime.now().isoformat(),
        }

    @classmethod
    def _contar_por_tipo(cls, esferas: list[dict]) -> dict:
        conteo: dict[str, int] = {}
        for e in esferas:
            t = e["tipo"]
            conteo[t] = conteo.get(t, 0) + 1
        return conteo
