"""Orquestador central de invocaciones IA.

Concentra lo que antes estaba disperso en servidor.py: carga de memoria,
armado de system prompts (vía ContextoManager), descifrado de carta natal,
invocación al adapter y persistencia de la conversación.

El adapter (ClienteIA) es inyectable por el constructor, lo que permite
sustituirlo por ClienteTest u offline sin tocar el resto del sistema.
"""

import json

from base_datos.proyecto import ConversacionRepo, ProyectoRepo
from base_datos.legacy import ConversacionLegadoRepo, CartaNatalRepo
from proyectos import Cifrador
from tarot import tirada_como_contexto

from invocacion.interface import ClienteIA, RespuestaIA
from invocacion.adapters.groq import ClienteGroq
from invocacion.contexto import ContextoManager
from invocacion.respuesta import ParsingRespuesta

# System prompt que usa Tutu para decidir qué entidad responde.
_SYSTEM_DECIDIR = """Lee el mensaje del practicante y decide qué entidad debe responder.

Entidades:
- isis     → libertad, amor materno, pureza, vínculo herido
- afrodita → claridad mental, calma, estados de conciencia, paz
- lilith   → cambio urgente, tormenta, energía reprimida, pasión
- artemisa → enraizarse, ancestros, naturaleza, colectivo, abundancia
- tutu     → propósito, cuestionamiento interior, paradojas

Responde SOLO con este JSON exacto, sin explicaciones ni markdown:
{"deidad": "nombre", "estado": "cuerpo", "razon": "frase breve"}"""


class Invocador:
    """Coordina contexto, adapter y persistencia para cada invocación."""

    def __init__(self, cliente_ia: ClienteIA | None = None):
        self.cliente_ia: ClienteIA = cliente_ia or ClienteGroq()

    # ── Carta natal ─────────────────────────────────────────────────────

    def _carta_natal_proyecto(self, proyecto) -> dict | None:
        """Descifra la carta natal de un proyecto, o None si no hay/falla."""
        if proyecto is None:
            return None
        try:
            cifrada = ProyectoRepo.obtener_carta_natal(proyecto.hash)
            if cifrada:
                datos = Cifrador.descifrar(cifrada, proyecto.codigo)
                if datos:
                    return json.loads(datos)
        except Exception:
            pass
        return None

    def _carta_natal_legacy(self) -> dict | None:
        """Carta natal del almacén legacy (sin proyecto), o None."""
        carta = CartaNatalRepo.leer()
        if carta and carta.get("datos"):
            try:
                return json.loads(carta["datos"])
            except Exception:
                pass
        return None

    # ── Conversación ────────────────────────────────────────────────────

    def invocar_deidad(self, nombre: str, mensaje: str, proyecto,
                       esferas_bosque: list[dict] | None = None,
                       entradas_biblioteca: list[dict] | None = None) -> RespuestaIA:
        """Responde como una deidad, persistiendo la conversación."""
        memoria = ConversacionRepo.cargar(proyecto.hash, nombre)
        ConversacionRepo.guardar(proyecto.hash, nombre, "user", mensaje)
        memoria.append({"role": "user", "content": mensaje})
        memoria = memoria[-10:]

        carta = self._carta_natal_proyecto(proyecto)
        system = ContextoManager.para_deidad(
            nombre, carta_natal=carta,
            esferas_bosque=esferas_bosque,
            entradas_biblioteca=entradas_biblioteca,
        )

        respuesta = self.cliente_ia.chat(
            system=system, messages=memoria, max_tokens=300
        )
        ConversacionRepo.guardar(
            proyecto.hash, nombre, "assistant", respuesta.texto
        )
        return respuesta

    def invocar_tutu(self, mensaje: str, proyecto,
                     esferas_bosque: list[dict] | None = None) -> RespuestaIA:
        """Responde como Tutu, persistiendo la conversación."""
        memoria = ConversacionRepo.cargar(proyecto.hash, "tutu")
        ConversacionRepo.guardar(proyecto.hash, "tutu", "user", mensaje)
        memoria.append({"role": "user", "content": mensaje})
        memoria = memoria[-10:]

        system = ContextoManager.para_tutu(esferas_bosque=esferas_bosque)

        respuesta = self.cliente_ia.chat(
            system=system, messages=memoria, max_tokens=300
        )
        ConversacionRepo.guardar(
            proyecto.hash, "tutu", "assistant", respuesta.texto
        )
        return respuesta

    def decidir_entidad(self, mensaje: str) -> tuple[str, str, str]:
        """Usa el modelo para elegir entidad. Devuelve (nombre, estado, razon)."""
        respuesta = self.cliente_ia.chat(
            system=_SYSTEM_DECIDIR,
            messages=[{"role": "user", "content": mensaje}],
            max_tokens=64,
        )
        datos = ParsingRespuesta.extraer_json(respuesta)
        if datos is not None:
            return (
                datos.get("deidad", "tutu"),
                datos.get("estado", "cuerpo"),
                datos.get("razon", ""),
            )
        return "tutu", "alma", "decisión interna"

    # ── Voz del Bosque ──────────────────────────────────────────────────

    def voz_bosque(
        self,
        esferas: list[dict],
        eventos: list[dict],
        humus: list[dict],
        relaciones: list[dict],
        convergencias: list[dict] | None = None,
    ) -> RespuestaIA:
        """El bosque habla desde su estado colectivo actual. Sin memoria — cada lectura es nueva."""
        system, user_msg = ContextoManager.para_bosque(
            esferas, eventos, humus, relaciones, convergencias
        )
        return self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": user_msg}],
            max_tokens=250,
        )

    # ── Tarot ───────────────────────────────────────────────────────────

    def leer_tarot(self, nombre_entidad: str, cartas: list, proyecto) -> RespuestaIA:
        """Lee una tirada de tarot, persistiendo en proyecto o legacy."""
        carta = (
            self._carta_natal_proyecto(proyecto)
            if proyecto
            else self._carta_natal_legacy()
        )
        system = ContextoManager.para_tarot(nombre_entidad, carta_natal=carta)

        contexto = tirada_como_contexto(cartas)
        prompt = f"{contexto}\n\nLee mi tirada."
        respuesta = self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
        )

        if proyecto:
            ConversacionRepo.guardar(
                proyecto.hash, nombre_entidad, "user", "[Tirada de tarot]"
            )
            ConversacionRepo.guardar(
                proyecto.hash, nombre_entidad, "assistant", respuesta.texto
            )
        else:
            ConversacionLegadoRepo.guardar(nombre_entidad, "user", "[Tirada de tarot]")
            ConversacionLegadoRepo.guardar(nombre_entidad, "assistant", respuesta.texto)

        return respuesta

    # ── Sigilo ──────────────────────────────────────────────────────────

    def generar_intencion_sigilo(
        self, nombre_entidad: str, memoria_reciente: list
    ) -> str:
        """Genera la intención (string limpio) para un sigilo."""
        contexto = ""
        if memoria_reciente:
            ultimos = memoria_reciente[-6:]
            contexto = "\n".join(
                f"{'Practicante' if m['role'] == 'user' else nombre_entidad.capitalize()}: "
                f"{m['content'][:200]}"
                for m in ultimos
            )

        system = ContextoManager.para_sigilo(nombre_entidad)
        prompt = (
            f"Conversación reciente:\n{contexto}\n\nDame la intención del sigilo."
            if contexto
            else "Dame una intención de sigilo para quien apenas llega."
        )

        respuesta = self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=40,
        )
        return ParsingRespuesta.limpiar_intencion_sigilo(respuesta.texto)
