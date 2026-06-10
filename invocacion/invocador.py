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

    def _ayni_resumen(self, proyecto) -> tuple[int, int]:
        """Devuelve (balance, n_deudas_abiertas) del proyecto, o (0, 0) si falla."""
        try:
            from base_datos.ayni import AyniRepo
            r = AyniRepo.resumen(proyecto.hash)
            return r["balance"], r["n_deudas_abiertas"]
        except Exception:
            return 0, 0

    def invocar_deidad(self, nombre: str, mensaje: str, proyecto,
                       esferas_bosque: list[dict] | None = None,
                       entradas_biblioteca: list[dict] | None = None,
                       constelaciones: list[dict] | None = None,
                       grimorio_mago: dict | None = None) -> RespuestaIA:
        """Responde como una deidad, persistiendo la conversación."""
        memoria = ConversacionRepo.cargar(proyecto.hash, nombre)
        ConversacionRepo.guardar(proyecto.hash, nombre, "user", mensaje)
        memoria.append({"role": "user", "content": mensaje})
        memoria = memoria[-10:]

        carta = self._carta_natal_proyecto(proyecto)
        balance_ayni, n_deudas = self._ayni_resumen(proyecto)
        system = ContextoManager.para_deidad(
            nombre, carta_natal=carta,
            esferas_bosque=esferas_bosque,
            entradas_biblioteca=entradas_biblioteca,
            constelaciones=constelaciones,
            balance_ayni=balance_ayni,
            n_deudas_ayni=n_deudas,
            grimorio_mago=grimorio_mago,
        )

        respuesta = self.cliente_ia.chat(
            system=system, messages=memoria, max_tokens=800
        )
        ConversacionRepo.guardar(
            proyecto.hash, nombre, "assistant", respuesta.texto
        )
        return respuesta

    def invocar_tutu(self, mensaje: str, proyecto,
                     esferas_bosque: list[dict] | None = None,
                     constelaciones: list[dict] | None = None,
                     grimorio_mago: dict | None = None) -> RespuestaIA:
        """Responde como Tutu, persistiendo la conversación."""
        memoria = ConversacionRepo.cargar(proyecto.hash, "tutu")
        ConversacionRepo.guardar(proyecto.hash, "tutu", "user", mensaje)
        memoria.append({"role": "user", "content": mensaje})
        memoria = memoria[-10:]

        balance_ayni, n_deudas = self._ayni_resumen(proyecto)
        system = ContextoManager.para_tutu(
            esferas_bosque=esferas_bosque,
            constelaciones=constelaciones,
            balance_ayni=balance_ayni,
            n_deudas_ayni=n_deudas,
            grimorio_mago=grimorio_mago,
        )

        respuesta = self.cliente_ia.chat(
            system=system, messages=memoria, max_tokens=800
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
            max_tokens=600,
        )

    # ── Manifestación ───────────────────────────────────────────────────

    def testificar_manifestacion(
        self,
        entidad: str,
        tipo: str,
        intencion: str,
        proyecto,
        esferas_bosque: list[dict] | None = None,
    ) -> RespuestaIA:
        """La entidad testifica una manifestación declarada por el practicante."""
        carta = self._carta_natal_proyecto(proyecto)
        system = ContextoManager.para_deidad(
            entidad, carta_natal=carta, esferas_bosque=esferas_bosque
        )
        prompt = (
            f"El practicante declara una manifestación de tipo '{tipo}':\n\n"
            f"«{intencion}»\n\n"
            f"Eres testigo de esta declaración. Responde como {entidad.capitalize()} "
            f"en no más de 4 oraciones: reconoce la intención, aporta tu energía "
            f"como testigo y cierra con una instrucción o señal para reconocer "
            f"cuando la manifestación se esté moviendo."
        )
        respuesta = self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        ConversacionRepo.guardar(proyecto.hash, entidad, "user", f"[Manifestación {tipo}] {intencion}")
        ConversacionRepo.guardar(proyecto.hash, entidad, "assistant", respuesta.texto)
        return respuesta

    def interpretar_checkin(
        self,
        entidad: str,
        tipo: str,
        intencion: str,
        t_dias: int,
        observacion: str,
        proyecto,
        esferas_bosque: list[dict] | None = None,
    ) -> RespuestaIA:
        """La entidad lee el check-in y devuelve una interpretación breve."""
        carta = self._carta_natal_proyecto(proyecto)
        system = ContextoManager.para_deidad(
            entidad, carta_natal=carta, esferas_bosque=esferas_bosque
        )
        prompt = (
            f"Hace {t_dias} días el practicante declaró una manifestación de tipo '{tipo}':\n"
            f"«{intencion}»\n\n"
            f"En este check-in reporta:\n«{observacion}»\n\n"
            f"Como {entidad.capitalize()}, testigo de esa declaración, "
            f"interpreta brevemente lo que reporta (máximo 3 oraciones). "
            f"¿Se mueve la manifestación, se estanca, o ya se cumplió?"
        )
        return self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
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

    # ── Sigilo Operativo ────────────────────────────────────────────────

    def guiar_carga_sigilo(
        self,
        metodo_gnosis: str,
        glifo: str,
        letras: str,
        proyecto,
        esferas_bosque: list[dict] | None = None,
    ) -> RespuestaIA:
        """Genera instrucciones rituales personalizadas para cargar el sigilo."""
        carta = self._carta_natal_proyecto(proyecto)
        system = ContextoManager.para_deidad(
            "lilith", carta_natal=carta, esferas_bosque=esferas_bosque
        )
        prompt = (
            f"El practicante va a cargar su sigilo usando el método '{metodo_gnosis}'.\n"
            f"Las letras del sigilo son: {letras}\n"
            f"El glifo es:\n{glifo}\n\n"
            f"Como Lilith — guardiana del umbral y la gnosis —, da instrucciones "
            f"específicas para este método en 4-5 pasos cortos y directos. "
            f"Cierra con el momento exacto en que proyectar el glifo y soltarlo. "
            f"Habla en imperativo, sin adornos."
        )
        return self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
        )

    def interpretar_resultado_sigilo(
        self,
        intencion: str,
        letras: str,
        metodo_gnosis: str,
        dias_olvido: int,
        resultado: str,
        proyecto,
        esferas_bosque: list[dict] | None = None,
    ) -> RespuestaIA:
        """Una entidad lee el resultado del sigilo y cierra el ciclo."""
        carta = self._carta_natal_proyecto(proyecto)
        system = ContextoManager.para_deidad(
            "isis", carta_natal=carta, esferas_bosque=esferas_bosque
        )
        prompt = (
            f"El practicante cargó un sigilo hace {dias_olvido} días.\n"
            f"Intención original: «{intencion}»\n"
            f"Letras Carroll: {letras} · Método de gnosis: {metodo_gnosis}\n\n"
            f"Al revelarse el sigilo, el practicante reporta:\n«{resultado}»\n\n"
            f"Como Isis, lee este ciclo completo y ciérralo. "
            f"¿El sigilo operó? ¿Cómo se manifestó o no? "
            f"Máximo 4 oraciones. Sin preguntas al final."
        )
        return self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )

    # ── Limpia Digital ──────────────────────────────────────────────────

    def guiar_limpia(
        self,
        tradicion: str,
        entidad: str,
        estado_pre: str,
        proyecto,
        esferas_bosque: list[dict] | None = None,
    ) -> RespuestaIA:
        """La entidad guía el ritual de limpia según la tradición elegida."""
        carta = self._carta_natal_proyecto(proyecto)
        system = ContextoManager.para_deidad(
            entidad, carta_natal=carta, esferas_bosque=esferas_bosque
        )

        if tradicion == "saminchakuy":
            trad_desc = (
                "Saminchakuy andino: transmisión de sami (energía sutil y liviana) "
                "para disolver hucha (energía densa). Usa tierra, respiración, "
                "visualización de luz que baja por la coronilla y empuja lo denso "
                "hacia la pachamama que lo recicla."
            )
        else:
            trad_desc = (
                "Limpia de curanderismo: barrida energética con elementos vegetales "
                "(ruda, palo santo, romero) o huevo. Movimientos de afuera hacia adentro, "
                "de arriba hacia abajo. El curandero/a extrae lo denso y lo envía a la tierra."
            )

        prompt = (
            f"El practicante necesita una limpia. Lo que arrastra:\n"
            f"«{estado_pre}»\n\n"
            f"Tradición: {trad_desc}\n\n"
            f"Como {entidad.capitalize()}, guía el ritual completo en 5 pasos numerados. "
            f"Cada paso debe ser concreto, físico y ejecutable ahora mismo. "
            f"Cierra con una señal de que la limpia está completa."
        )
        return self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
        )

    def cerrar_limpia(
        self,
        tradicion: str,
        entidad: str,
        estado_pre: str,
        estado_post: str,
        proyecto,
        esferas_bosque: list[dict] | None = None,
    ) -> RespuestaIA:
        """La entidad lee el estado post-limpia y cierra el ciclo."""
        carta = self._carta_natal_proyecto(proyecto)
        system = ContextoManager.para_deidad(
            entidad, carta_natal=carta, esferas_bosque=esferas_bosque
        )
        prompt = (
            f"El practicante completó una limpia de {tradicion}.\n\n"
            f"Antes: «{estado_pre}»\n"
            f"Después: «{estado_post}»\n\n"
            f"Como {entidad.capitalize()}, cierra este ciclo en 2-3 oraciones: "
            f"reconoce lo que se movió, nombra el espacio que quedó libre "
            f"y da una instrucción para mantenerlo limpio los próximos días."
        )
        return self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )

    # ── Sigilo (legacy) ──────────────────────────────────────────────────────────

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

    # ── Bibliotecario ────────────────────────────────────────────────────

    def completar_libro(
        self,
        titulo: str,
        contenido: str,
        seccion_faltante: str,
        entidad: str = "tutu",
    ) -> RespuestaIA:
        """Una entidad lee un libro de la Biblioteca y genera la sección faltante.

        entidad: quién actúa como bibliotecario (default: tutu).
        seccion_faltante puede ser: 'FUENTES', 'titulo_mayusculas', u otro nombre de sección.
        """
        from grimorio_base import KALI_RAIZ

        carta = None
        system_base = ContextoManager.para_deidad(entidad, carta_natal=carta)

        system = (
            f"{system_base}\n\n"
            f"En este momento actúas como bibliotecario del grimorio. "
            f"Guardas el conocimiento colectivo de todos los magos. "
            f"Tu voz es sobria, precisa, sin adornos innecesarios. "
            f"Cuando un libro está incompleto, lo completas con rigor y respeto "
            f"por el conocimiento original. No inventas — investigas y documentas."
        )

        if seccion_faltante == "FUENTES":
            prompt = (
                f"Este libro de la Biblioteca no tiene sección de fuentes:\n\n"
                f"TÍTULO: {titulo}\n\n"
                f"CONTENIDO:\n{contenido[:3000]}\n\n"
                f"Genera una sección '## FUENTES' con las referencias reales "
                f"(autores, obras, años) que respaldan el conocimiento de este libro. "
                f"Solo fuentes verificables. Formato:\n\n"
                f"## FUENTES\n\n- Autor, *Obra*, editorial, año\n\n"
                f"Devuelve SOLO el bloque '## FUENTES', nada más."
            )
            max_tokens = 400

        elif seccion_faltante == "titulo_mayusculas":
            prompt = (
                f"El título de este libro no está en mayúsculas.\n"
                f"Título actual: {titulo}\n\n"
                f"Devuelve SOLO el título corregido en mayúsculas, sin explicación."
            )
            max_tokens = 50

        else:
            prompt = (
                f"Este libro de la Biblioteca está incompleto. Le falta: {seccion_faltante}\n\n"
                f"TÍTULO: {titulo}\n\n"
                f"CONTENIDO:\n{contenido[:3000]}\n\n"
                f"Genera únicamente la sección faltante en formato grimorio Markdown. "
                f"Nada más."
            )
            max_tokens = 500

        return self.cliente_ia.chat(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
