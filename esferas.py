from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, ClassVar

from config import Config
from base_datos import EsferaRepo, ProyectoRepo, ConversacionRepo


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
    TIPOS_VALIDOS = frozenset(["geo", "elemental", "tematica", "resonancia"])
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

        tipo_elemental = cls._entidad_a_elemento(entidad)
        if tipo_elemental:
            resultados.append(cls.marcar(
                "elemental", tipo_elemental,
                {"entidad": entidad, "elemento": tipo_elemental},
                proyecto_hash
            ))

        if ubicacion and ubicacion.strip():
            from geografia import GestorGeografico
            eco = GestorGeografico.resolver(ubicacion)
            if eco:
                resultados.append(cls.marcar(
                    "geo", eco.codigo_wwf,
                    {"ecoregion": eco.nombre, "eje": eco.eje_del_mundo},
                    proyecto_hash
                ))
            else:
                resultados.append(cls.marcar(
                    "geo", "MAR_DE_KALI",
                    {"nota": "Ubicación no reconocida — emerge del Mar de Kali"},
                    proyecto_hash
                ))

        if concepto and concepto.strip():
            resultados.append(cls.marcar(
                "tematica", concepto.strip().lower(),
                {"concepto": concepto.strip()},
                proyecto_hash
            ))

        return resultados

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
                disueltas += 1
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

        return {
            "total_esferas": len(todas),
            "actualizadas": actualizadas,
            "disueltas": disueltas,
            "timestamp": now.isoformat(),
        }

    @classmethod
    def obtener_mapa(cls) -> dict:
        esferas = cls.listar_activas()
        proyectos_activos = ProyectoRepo.total_activos()

        nodos: list[dict] = [
            {"id": f"esfera:{e['tipo']}:{e['clave_unica']}",
             "tipo": "esfera",
             "subtipo": e["tipo"],
             "amplitud": e["amplitud_actual"],
             "fase": e["fase_viva"],
             "label": f"{e['tipo']}: {e['clave_unica']}"}
            for e in esferas
        ]

        links: list[dict] = []
        visto = set()
        for i, a in enumerate(esferas):
            for b in esferas[i + 1:]:
                if a["tipo"] == b["tipo"]:
                    clave = frozenset([a["clave_unica"], b["clave_unica"]])
                    if clave not in visto:
                        visto.add(clave)
                        links.append({
                            "source": f"esfera:{a['tipo']}:{a['clave_unica']}",
                            "target": f"esfera:{b['tipo']}:{b['clave_unica']}",
                            "tipo": "mismo_tipo",
                        })

        return {
            "nodos": nodos,
            "links": links,
            "estadisticas": {
                "total_esferas": len(esferas),
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
