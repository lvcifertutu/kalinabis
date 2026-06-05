import hashlib
import json
import base64
import os
import secrets
from dataclasses import dataclass, field
from typing import Optional

from config import Config


class Cifrador:
    @staticmethod
    def derivar_clave(codigo: str) -> bytes:
        return hashlib.sha256(codigo.encode("utf-8")).digest()

    @staticmethod
    def cifrar(datos: str, codigo: str) -> str:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError:
            raise ImportError(
                "Se necesita la librería 'cryptography'. "
                "Ejecutá: pip install cryptography"
            )
        clave = Cifrador.derivar_clave(codigo)
        aesgcm = AESGCM(clave)
        nonce = os.urandom(12)
        datos_bytes = datos.encode("utf-8")
        cifrado = aesgcm.encrypt(nonce, datos_bytes, None)
        return base64.b64encode(nonce + cifrado).decode("utf-8")

    @staticmethod
    def descifrar(datos_cifrados: str, codigo: str) -> Optional[str]:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError:
            raise ImportError(
                "Se necesita la librería 'cryptography'. "
                "Ejecutá: pip install cryptography"
            )
        clave = Cifrador.derivar_clave(codigo)
        aesgcm = AESGCM(clave)
        try:
            datos = base64.b64decode(datos_cifrados)
            nonce = datos[:12]
            cifrado = datos[12:]
            return aesgcm.decrypt(nonce, cifrado, None).decode("utf-8")
        except Exception:
            return None


class GeneradorCodigos:
    @staticmethod
    def generar() -> str:
        adj1 = secrets.choice(Config.ADJETIVOS)
        sust1 = secrets.choice(Config.SUSTANTIVOS)
        adj2 = secrets.choice(Config.ADJETIVOS)
        sust2 = secrets.choice(Config.SUSTANTIVOS)
        return Config.PROJECT_CODE_SEPARATOR.join([adj1, sust1, adj2, sust2])

    @staticmethod
    def hash_codigo(codigo: str) -> str:
        return hashlib.sha256(codigo.encode("utf-8")).hexdigest()


@dataclass
class Proyecto:
    codigo: str
    hash: str = field(init=False)

    def __post_init__(self):
        self.hash = GeneradorCodigos.hash_codigo(self.codigo)

    def a_dict_publico(self) -> dict:
        return {
            "hash": self.hash[:12],
            "codigo": self.codigo,
        }
