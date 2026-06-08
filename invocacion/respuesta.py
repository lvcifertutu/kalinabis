"""Parsing y limpieza de respuestas de IA, en un solo lugar."""

import json

from invocacion.interface import RespuestaIA


class ParsingRespuesta:
    """Helpers para interpretar el texto crudo devuelto por un adapter."""

    @staticmethod
    def extraer_json(
        respuesta: RespuestaIA, fallback: dict | None = None
    ) -> dict | None:
        """Extrae un objeto JSON embebido en el texto de la respuesta.

        Devuelve `fallback` (None por defecto) cuando no encuentra un objeto
        JSON o falla el parseo, para que quien llame distinga el caso "miss"
        de un objeto vacío legítimamente parseado.
        """
        try:
            texto = respuesta.texto
            inicio = texto.find("{")
            fin = texto.rfind("}") + 1
            if inicio >= 0 and fin > inicio:
                return json.loads(texto[inicio:fin])
        except Exception:
            pass
        return fallback

    @staticmethod
    def limpiar_intencion_sigilo(texto: str) -> str:
        """Normaliza la intención de un sigilo: mayúsculas, sin comillas, 1 línea."""
        intencion = texto.strip().strip('"').strip("'").upper()
        return intencion.split("\n")[0][:60]
