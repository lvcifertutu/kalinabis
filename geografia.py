import unicodedata
import re
from dataclasses import dataclass, field
from typing import Optional, ClassVar


@dataclass
class Ecoregion:
    codigo_wwf: str
    nombre: str
    paises: list[str]
    ciudades_clave: list[str]
    eje_del_mundo: dict
    bioma: str

    def tiene_ciudad(self, texto: str) -> bool:
        texto_norm = _normalizar(texto)
        for ciudad in self.ciudades_clave:
            if _normalizar(ciudad) in texto_norm:
                return True
        return False

    def a_dict(self) -> dict:
        return {
            "codigo_wwf": self.codigo_wwf,
            "nombre": self.nombre,
            "paises": self.paises,
            "eje_del_mundo": self.eje_del_mundo,
            "bioma": self.bioma,
        }


def _normalizar(t: str) -> str:
    t = t.lower().strip()
    t = unicodedata.normalize("NFKD", t)
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-z0-9\s]", "", t)
    return t


ECORREGIONES_SUDAMERICA: list[Ecoregion] = [
    Ecoregion(
        codigo_wwf="NT0404",
        nombre="Bosques Templados Valdivianos",
        paises=["Chile", "Argentina"],
        ciudades_clave=["valdivia", "puerto montt", "chiloe", "ancud",
                        "castro", "osorno", "bariloche", "san martin de los andes",
                        "la union", "rio negro", "llanquihue"],
        eje_del_mundo={
            "especie": "Fitzroya cupressoides",
            "nombres_locales": ["Alerce", "Lawal"],
            "familia": "Cupressaceae",
            "nota": "El árbol más longevo de Sudamérica (hasta 3600 años). Sagrado para el pueblo mapuche."
        },
        bioma="bosque templado lluvioso",
    ),
    Ecoregion(
        codigo_wwf="NT1201",
        nombre="Chilean Matorral",
        paises=["Chile"],
        ciudades_clave=["santiago", "valparaiso", "rancagua", "melipilla",
                        "san fernando", "curico", "talca", "linares",
                        "quillota", "los andes", "san antonio"],
        eje_del_mundo={
            "especie": "Beilschmiedia miersii",
            "nombres_locales": ["Belloto del Norte"],
            "familia": "Lauraceae",
            "nota": "Especie relicta del bosque esclerófilo, vulnerable por pérdida de hábitat."
        },
        bioma="matorral mediterráneo",
    ),
    Ecoregion(
        codigo_wwf="NT1007",
        nombre="Bosques Subpolares Magallánicos",
        paises=["Chile", "Argentina"],
        ciudades_clave=["punta arenas", "ushuaia", "rio gallegos", "porvenir",
                        "puerto natales", "puerto williams", "cabo de hornos"],
        eje_del_mundo={
            "especie": "Nothofagus betuloides",
            "nombres_locales": ["Coihue de Magallanes", "Guindo"],
            "familia": "Nothofagaceae",
            "nota": "El árbol austral que llega hasta el Cabo de Hornos, símbolo de resistencia."
        },
        bioma="bosque subpolar lluvioso",
    ),
    Ecoregion(
        codigo_wwf="NT0406",
        nombre="Bosques con Araucarias",
        paises=["Brasil", "Argentina"],
        ciudades_clave=["lages", "curitibanos", "sao joaquim", "caxias do sul",
                        "san francisco de paula", "canela", "gramado"],
        eje_del_mundo={
            "especie": "Araucaria angustifolia",
            "nombres_locales": ["Araucaria", "Pino Paraná", "Curi"],
            "familia": "Araucariaceae",
            "nota": "El pino misionero, sagrado para el pueblo guaraní. Especie críticamente amenazada."
        },
        bioma="bosque templado de coníferas",
    ),
    Ecoregion(
        codigo_wwf="NT0403",
        nombre="Bosques Atlánticos del Alto Paraná",
        paises=["Brasil", "Argentina", "Paraguay"],
        ciudades_clave=["iguazu", "foz do iguacu", "puerto iguazu", "ciudad del este",
                        "misiones", "posadas", "encarnacion", "cascavel"],
        eje_del_mundo={
            "especie": "Araucaria angustifolia",
            "nombres_locales": ["Pino Paraná", "Curi", "Pino Brasileño"],
            "familia": "Araucariaceae",
            "nota": "Especie emblemática del Bosque Atlántico, hoy reducida al 3% de su cobertura original."
        },
        bioma="bosque atlántico subtropical",
    ),
    Ecoregion(
        codigo_wwf="NT0162",
        nombre="Bosques Amazónicos del Suroeste",
        paises=["Perú", "Bolivia", "Brasil"],
        ciudades_clave=["iquitos", "puerto maldonado", "pucallpa", "cobija",
                        "rio branco", "cruzeiro do sul", "tambopata", "manu"],
        eje_del_mundo={
            "especie": "Bertholletia excelsa",
            "nombres_locales": ["Castanha", "Castaña", "Nuez de Brasil"],
            "familia": "Lecythidaceae",
            "nota": "Árbol emblemático de la Amazonía, protegido por ley. Sus frutos alimentan la selva entera."
        },
        bioma="bosque húmedo amazónico",
    ),
    Ecoregion(
        codigo_wwf="NT0302",
        nombre="Yungas Boliviano-Peruanas",
        paises=["Bolivia", "Perú"],
        ciudades_clave=["la paz", "coroico", "chulumani", "caranavi",
                        "quisquillacota", "nor yungas", "sud yungas"],
        eje_del_mundo={
            "especie": "Cinchona officinalis",
            "nombres_locales": ["Quina", "Cascarilla"],
            "familia": "Rubiaceae",
            "nota": "Árbol de la quina, fuente de la quinina que curó la malaria. Símbolo nacional del Perú."
        },
        bioma="bosque nublado montano",
    ),
    Ecoregion(
        codigo_wwf="NT1008",
        nombre="Estepa Patagónica",
        paises=["Argentina", "Chile"],
        ciudades_clave=["el calafate", "perito moreno", "esquel", "comodoro rivadavia",
                        "rawson", "trelew", "puerto deseado", "caleta olivia"],
        eje_del_mundo={
            "especie": "Austrocedrus chilensis",
            "nombres_locales": ["Ciprés de la Cordillera", "Len"],
            "familia": "Cupressaceae",
            "nota": "Conífera patagónica que crece en suelos pobres, símbolo de resiliencia en la estepa."
        },
        bioma="estepa templada",
    ),
    Ecoregion(
        codigo_wwf="NT1104",
        nombre="Desierto de Atacama",
        paises=["Chile", "Perú"],
        ciudades_clave=["san pedro de atacama", "calama", "antofagasta", "iquique",
                        "arica", "tocopilla", "taltal", "chanaral"],
        eje_del_mundo={
            "especie": "Prosopis tamarugo",
            "nombres_locales": ["Tamarugo"],
            "familia": "Fabaceae",
            "nota": "Árbol endémico del desierto más árido del mundo, sobrevive captando la niebla costera."
        },
        bioma="desierto absoluto",
    ),
    Ecoregion(
        codigo_wwf="NT0135",
        nombre="Bosques Montanos del Valle del Magdalena",
        paises=["Colombia"],
        ciudades_clave=["bogota", "manizales", "pereira", "armenia",
                        "ibague", "nelva", "pitalito", "san agustin"],
        eje_del_mundo={
            "especie": "Ceroxylon quindiuense",
            "nombres_locales": ["Palma de Cera del Quindío"],
            "familia": "Arecaceae",
            "nota": "Palma nacional de Colombia, la más alta del mundo (hasta 60m). Crece en los Andes."
        },
        bioma="bosque montano nublado",
    ),
    Ecoregion(
        codigo_wwf="NT1301",
        nombre="Pantanal",
        paises=["Brasil", "Bolivia", "Paraguay"],
        ciudades_clave=["corumba", "cuiaba", "poconé", "barra do bugres",
                        "puerto suarez", "quirindi", "pantanal"],
        eje_del_mundo={
            "especie": "Handroanthus heptaphyllus",
            "nombres_locales": ["Tajy", "Lapacho", "Pau d'Arco"],
            "familia": "Bignoniaceae",
            "nota": "Árbol de flores rosadas que anuncia la primavera en el humedal más grande del mundo."
        },
        bioma="humedal tropical",
    ),
    Ecoregion(
        codigo_wwf="NT1302",
        nombre="Gran Chaco",
        paises=["Argentina", "Bolivia", "Paraguay"],
        ciudades_clave=["resistencia", "asuncion", "santa cruz de la sierra",
                        "presidente hayes", "filadelfia", "santiago del estero",
                        "tucuman", "salta", "jujuy"],
        eje_del_mundo={
            "especie": "Schinopsis lorentzii",
            "nombres_locales": ["Quebracho Colorado", "Quebracho"],
            "familia": "Anacardiaceae",
            "nota": "Árbol de madera durísima (quebracho = 'quiebra hacha'), símbolo del Chaco."
        },
        bioma="bosque seco subtropical",
    ),
    Ecoregion(
        codigo_wwf="NT0704",
        nombre="Cerrado",
        paises=["Brasil"],
        ciudades_clave=["brasilia", "goiania", "uberlandia", "campo grande",
                        "palmas", "cuiaba", "ribeirao preto", "sao carlos"],
        eje_del_mundo={
            "especie": "Caryocar brasiliense",
            "nombres_locales": ["Pequi", "Piqui"],
            "familia": "Caryocaraceae",
            "nota": "Árbol icónico del Cerrado, su fruto es base de la gastronomía del Centro-Oeste brasileño."
        },
        bioma="sabana tropical",
    ),
    Ecoregion(
        codigo_wwf="NT0217",
        nombre="Bosques Secos de Tumbes-Piura",
        paises=["Perú", "Ecuador"],
        ciudades_clave=["piura", "tumbes", "talara", "sullana", "machala",
                        "guayaquil", "loja", "santa rosa"],
        eje_del_mundo={
            "especie": "Prosopis pallida",
            "nombres_locales": ["Algarrobo"],
            "familia": "Fabaceae",
            "nota": "Árbol del bosque seco ecuatorial, resistente a la sequía extrema."
        },
        bioma="bosque seco tropical",
    ),
]


class GestorGeografico:
    _ecorregiones: ClassVar[list[Ecoregion]] = ECORREGIONES_SUDAMERICA

    @classmethod
    def resolver(cls, ubicacion: str) -> Optional[Ecoregion]:
        if not ubicacion or not ubicacion.strip():
            return None
        for eco in cls._ecorregiones:
            if eco.tiene_ciudad(ubicacion):
                return eco
        return None

    @classmethod
    def listar_todas(cls) -> list[dict]:
        return [e.a_dict() for e in cls._ecorregiones]

    @classmethod
    def buscar_por_codigo(cls, codigo_wwf: str) -> Optional[Ecoregion]:
        for eco in cls._ecorregiones:
            if eco.codigo_wwf == codigo_wwf:
                return eco
        return None

    @classmethod
    def eje_del_mundo_para(cls, ubicacion: str) -> dict:
        eco = cls.resolver(ubicacion)
        if eco:
            return eco.a_dict()
        return {
            "codigo_wwf": "MAR_DE_KALI",
            "nombre": "Mar de Kali",
            "paises": [],
            "eje_del_mundo": {
                "especie": None,
                "nombres_locales": ["El Vacío Primordial"],
                "nota": "Invocación sin ubicación declarada. La entidad emerge del Mar de Kali."
            },
            "bioma": "mar primordial",
        }
