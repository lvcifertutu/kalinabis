import os
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Config:
    GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
    GROQ_MAX_TOKENS: int = int(os.environ.get("GROQ_MAX_TOKENS", "1024"))
    GROQ_TEMPERATURE: float = float(os.environ.get("GROQ_TEMPERATURE", "0.8"))

    DECAY_LETARGO_DIAS: int = 14
    DECAY_DISOLUCION_PARCIAL_DIAS: int = 30
    DECAY_DISOLUCION_TOTAL_DIAS: int = 60

    ESFERA_AMPLITUD_INICIAL: float = 1.0
    ESFERA_MARCA_INCREMENTO: float = 0.3
    ESFERA_AMPLITUD_MINIMA: float = 0.01

    CICLO_DECAIMIENTO_INTERVALO_HORAS: int = 6

    ADJETIVOS: ClassVar[list[str]] = [
        "suave", "lento", "rapido", "dulce", "agrio",
        "firme", "fuerte", "claro", "oscuro", "tibio",
        "frio", "calido", "fresco", "largo", "breve",
        "hondo", "alto", "bajo", "ancho", "agudo",
        "simple", "noble", "sabio", "manso", "bravo",
        "tierno", "rudo", "leve", "ligero", "denso",
        "puro", "turbio", "fragil", "solido", "agil",
        "quieto", "tenue", "intenso", "amplio", "estrecho",
        "humilde", "feroz", "astuto", "luciente", "ermitanho",
        "errante", "naciente", "creciente", "menguante", "eterno",
    ]

    SUSTANTIVOS: ClassVar[list[str]] = [
        "trueno", "luna", "mar", "sol", "viento",
        "fuego", "agua", "tierra", "bosque", "monte",
        "rio", "lago", "nieve", "humo", "lluvia",
        "rayo", "nube", "roca", "arena", "sal",
        "ceniza", "rama", "flor", "fruto", "semilla",
        "hoja", "raiz", "tronco", "corteza", "savia",
        "musgo", "cardo", "junco", "palma", "pino",
        "roble", "sauce", "olmo", "fresno", "ceibo",
        "alerce", "arrayan", "canelo", "coihue", "laurel",
        "avellano", "boldo", "quillay", "peumo", "lingue",
    ]

    PROJECT_CODE_SEPARATOR: str = "-"

    @classmethod
    def verificar(cls) -> list[str]:
        errores = []
        if not cls.GROQ_API_KEY:
            errores.append("GROQ_API_KEY no está configurada en el entorno")
        return errores
