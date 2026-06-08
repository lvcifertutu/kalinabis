"""
Fase 2.2 - Capa 2 (La Mesa - Mago Personal)
TDD tests para Tarot personal, Oráculos, Chat Deidades, Servitors

Correr: python -m unittest tests.test_fase2_capa2
"""

import unittest

try:
    from tests.harness import AppDeTest
except ImportError:
    from harness import AppDeTest


class TestTarotRepo(unittest.TestCase):
    """RED: Tests para TarotRepo (tiradas personales)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_tarot_repo_crear(self):
        """Crear una tirada de tarot personal"""
        from base_datos import TarotRepo

        # Parámetros: user_id, arcano_principal, posiciones, interpretacion
        tirada_id = TarotRepo.crear(
            user_id=100,
            arcano_principal="El Mago",
            posiciones={"1": "El Magus", "2": "La Sacerdotisa", "3": "La Emperatriz"},
            interpretacion="Una tirada sobre tu poder personal y equilibrio"
        )

        self.assertIsNotNone(tirada_id)
        self.assertIsInstance(tirada_id, int)

    def test_tarot_repo_obtener(self):
        """Obtener una tirada específica"""
        from base_datos import TarotRepo

        tirada_id = TarotRepo.crear(
            user_id=101,
            arcano_principal="La Sacerdotisa",
            posiciones={"1": "Alto", "2": "Bajo", "3": "Lado"},
            interpretacion="Intuición y secretos revelados"
        )

        tirada = TarotRepo.obtener(tirada_id)

        self.assertIsNotNone(tirada)
        self.assertEqual(tirada['user_id'], 101)
        self.assertEqual(tirada['arcano_principal'], "La Sacerdotisa")
        self.assertIn("interpretacion", tirada)

    def test_tarot_repo_listar_por_usuario(self):
        """Listar todas las tiradas de un usuario"""
        from base_datos import TarotRepo

        # Crear 3 tiradas con user_ids únicos
        TarotRepo.crear(102, "El Mago", {"1": "A"}, "Poder")
        TarotRepo.crear(102, "La Sacerdotisa", {"1": "B"}, "Intuición")
        TarotRepo.crear(103, "El Emperador", {"1": "C"}, "Autoridad")

        tiradas_user102 = TarotRepo.listar_por_usuario(102)
        tiradas_user103 = TarotRepo.listar_por_usuario(103)

        self.assertEqual(len(tiradas_user102), 2)
        self.assertEqual(len(tiradas_user103), 1)
        self.assertEqual(tiradas_user102[0]['arcano_principal'], "La Sacerdotisa")


class TestTarotEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 2 - Tarot"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def test_post_tarot_nueva_tirada(self):
        """POST /api/capa2/tarot/nueva — crear tirada"""
        response = self.client.post(
            "/api/capa2/tarot/nueva",
            headers=self.app.headers(self.cod),
            json={
                "arcano_principal": "El Fool",
                "posiciones": {"1": "Presente", "2": "Futuro", "3": "Consejo"},
                "interpretacion": "Un viaje nuevo comienza"
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("tirada_id", data)
        self.assertIn("exp_ganada", data)
        self.assertEqual(data["exp_ganada"], 5)

    def test_get_tarot_listar(self):
        """GET /api/capa2/tarot — listar tiradas del usuario"""
        # Crear tirada primero
        self.client.post(
            "/api/capa2/tarot/nueva",
            headers=self.app.headers(self.cod),
            json={
                "arcano_principal": "La Sacerdotisa",
                "posiciones": {"1": "Pasado"},
                "interpretacion": "Intuición"
            }
        )

        response = self.client.get(
            "/api/capa2/tarot",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("tiradas", data)
        self.assertEqual(len(data["tiradas"]), 1)
        self.assertEqual(data["tiradas"][0]["arcano_principal"], "La Sacerdotisa")


class TestOráculoRepo(unittest.TestCase):
    """RED: Tests para OráculoRepo (oráculos personales)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_oraculo_repo_crear_runas(self):
        """Crear oráculo de runas"""
        from base_datos import OráculoRepo

        oraculo_id = OráculoRepo.crear(
            user_id=200,
            tipo="runas",
            pregunta="¿Qué debo aprender?",
            resultado={"runas": ["Fehu", "Uruz"], "significado": "Abundancia y fuerza"}
        )

        self.assertIsNotNone(oraculo_id)
        self.assertIsInstance(oraculo_id, int)

    def test_oraculo_repo_crear_iching(self):
        """Crear oráculo de I Ching"""
        from base_datos import OráculoRepo

        oraculo_id = OráculoRepo.crear(
            user_id=201,
            tipo="iching",
            pregunta="¿Cómo avanzo?",
            resultado={"hexagrama": 11, "nombre": "Tai", "interpretacion": "La paz"}
        )

        self.assertIsNotNone(oraculo_id)
        self.assertIsInstance(oraculo_id, int)

    def test_oraculo_repo_obtener(self):
        """Obtener oráculo específico"""
        from base_datos import OráculoRepo

        oraculo_id = OráculoRepo.crear(
            user_id=202,
            tipo="geomancia",
            pregunta="¿Qué camino tomar?",
            resultado={"figuras": ["Acquisitio", "Amissio"], "línea": 1}
        )

        oraculo = OráculoRepo.obtener(oraculo_id)

        self.assertIsNotNone(oraculo)
        self.assertEqual(oraculo['user_id'], 202)
        self.assertEqual(oraculo['tipo'], "geomancia")
        self.assertIn("pregunta", oraculo)

    def test_oraculo_repo_listar_por_usuario(self):
        """Listar oráculos de un usuario"""
        from base_datos import OráculoRepo

        OráculoRepo.crear(203, "runas", "¿Protección?", {"resultado": "Hagalaz"})
        OráculoRepo.crear(203, "iching", "¿Transformación?", {"resultado": 29})
        OráculoRepo.crear(204, "geomancia", "¿Consejo?", {"resultado": "Puer"})

        oráculos_user203 = OráculoRepo.listar_por_usuario(203)
        oráculos_user204 = OráculoRepo.listar_por_usuario(204)

        self.assertEqual(len(oráculos_user203), 2)
        self.assertEqual(len(oráculos_user204), 1)

    def test_oraculo_repo_listar_por_tipo(self):
        """Listar oráculos de un tipo específico"""
        from base_datos import OráculoRepo

        OráculoRepo.crear(205, "runas", "P1", {"r": 1})
        OráculoRepo.crear(205, "runas", "P2", {"r": 2})
        OráculoRepo.crear(205, "iching", "P3", {"r": 3})

        runas = OráculoRepo.listar_por_tipo(205, "runas")
        iching = OráculoRepo.listar_por_tipo(205, "iching")

        self.assertEqual(len(runas), 2)
        self.assertEqual(len(iching), 1)


class TestOráculoEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 2 - Oráculos"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def test_post_oraculo_nueva_consulta(self):
        """POST /api/capa2/oraculo/nueva — consultar oráculo"""
        response = self.client.post(
            "/api/capa2/oraculo/nueva",
            headers=self.app.headers(self.cod),
            json={
                "tipo": "runas",
                "pregunta": "¿Cuál es mi poder oculto?"
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("oraculo_id", data)
        self.assertIn("exp_ganada", data)
        self.assertEqual(data["exp_ganada"], 10)

    def test_get_oraculo_listar(self):
        """GET /api/capa2/oraculo — listar oráculos del usuario"""
        # Crear oráculo primero
        self.client.post(
            "/api/capa2/oraculo/nueva",
            headers=self.app.headers(self.cod),
            json={"tipo": "iching", "pregunta": "¿Futuro?"}
        )

        response = self.client.get(
            "/api/capa2/oraculo",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("oráculos", data)
        self.assertGreaterEqual(len(data["oráculos"]), 1)

    def test_get_oraculo_filtrar_por_tipo(self):
        """GET /api/capa2/oraculo?tipo=runas — filtrar por tipo"""
        # Crear dos oráculos de diferentes tipos
        self.client.post(
            "/api/capa2/oraculo/nueva",
            headers=self.app.headers(self.cod),
            json={"tipo": "runas", "pregunta": "Runas"}
        )
        self.client.post(
            "/api/capa2/oraculo/nueva",
            headers=self.app.headers(self.cod),
            json={"tipo": "iching", "pregunta": "Iching"}
        )

        response = self.client.get(
            "/api/capa2/oraculo?tipo=runas",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["oráculos"]), 1)
        self.assertEqual(data["oráculos"][0]["tipo"], "runas")


class TestConversacionCapaRepo(unittest.TestCase):
    """RED: Tests para ConversacionCapaRepo (chat privado user ↔ deidad)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_guardar_mensaje_usuario(self):
        """Guardar mensaje del usuario a deidad"""
        from base_datos import ConversacionCapaRepo

        msg_id = ConversacionCapaRepo.guardar_mensaje(
            user_id=300,
            deidad="Lilith",
            rol="user",
            contenido="¿Cuál es mi poder oculto?"
        )

        self.assertIsNotNone(msg_id)
        self.assertIsInstance(msg_id, int)

    def test_guardar_mensaje_deidad(self):
        """Guardar respuesta de deidad"""
        from base_datos import ConversacionCapaRepo

        msg_id = ConversacionCapaRepo.guardar_mensaje(
            user_id=301,
            deidad="Artemisa",
            rol="deidad",
            contenido="Tu poder está en la independencia y la claridad"
        )

        self.assertIsNotNone(msg_id)
        self.assertIsInstance(msg_id, int)

    def test_obtener_historial(self):
        """Obtener historial de conversación con deidad"""
        from base_datos import ConversacionCapaRepo

        ConversacionCapaRepo.guardar_mensaje(302, "Afrodita", "user", "Hola")
        ConversacionCapaRepo.guardar_mensaje(302, "Afrodita", "deidad", "Bienvenida")
        ConversacionCapaRepo.guardar_mensaje(302, "Afrodita", "user", "Gracias")

        historial = ConversacionCapaRepo.obtener_historial(302, "Afrodita")

        self.assertEqual(len(historial), 3)
        self.assertEqual(historial[0]["rol"], "user")
        self.assertEqual(historial[1]["rol"], "deidad")

    def test_obtener_historial_por_deidad(self):
        """Historial con una deidad no afecta a otra"""
        from base_datos import ConversacionCapaRepo

        ConversacionCapaRepo.guardar_mensaje(303, "Lilith", "user", "Msg1")
        ConversacionCapaRepo.guardar_mensaje(303, "Lilith", "deidad", "Resp1")
        ConversacionCapaRepo.guardar_mensaje(303, "Isis", "user", "Msg2")

        lilith_msgs = ConversacionCapaRepo.obtener_historial(303, "Lilith")
        isis_msgs = ConversacionCapaRepo.obtener_historial(303, "Isis")

        self.assertEqual(len(lilith_msgs), 2)
        self.assertEqual(len(isis_msgs), 1)


class TestChatDeityEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 2 - Chat Deidades"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def test_post_hablar_con_deidad(self):
        """POST /api/capa2/deidad/lilith/hablar — conversar con deidad"""
        response = self.client.post(
            "/api/capa2/deidad/lilith/hablar",
            headers=self.app.headers(self.cod),
            json={
                "mensaje": "¿Cuál es tu consejo para mí?"
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("respuesta", data)
        self.assertIn("exp_ganada", data)
        self.assertEqual(data["exp_ganada"], 3)

    def test_get_historial_con_deidad(self):
        """GET /api/capa2/deidad/artemisa/historial — obtener conversación"""
        # Hacer una consulta primero
        self.client.post(
            "/api/capa2/deidad/artemisa/hablar",
            headers=self.app.headers(self.cod),
            json={"mensaje": "Hola Artemisa"}
        )

        response = self.client.get(
            "/api/capa2/deidad/artemisa/historial",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("historial", data)
        self.assertGreaterEqual(len(data["historial"]), 1)

    def test_deidad_invalida(self):
        """POST con deidad no válida debe retornar error"""
        response = self.client.post(
            "/api/capa2/deidad/odin/hablar",
            headers=self.app.headers(self.cod),
            json={"mensaje": "Hola"}
        )

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)


class TestServitorCapaRepo(unittest.TestCase):
    """RED: Tests para ServitorCapaRepo (servitors personales)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_servitor_crear(self):
        """Crear servitor personal"""
        from base_datos import ServitorCapaRepo

        servitor_id = ServitorCapaRepo.crear(
            user_id=400,
            nombre="Protector",
            intencion="Defensa contra energías negativas"
        )

        self.assertIsNotNone(servitor_id)
        self.assertIsInstance(servitor_id, int)

    def test_servitor_obtener(self):
        """Obtener servitor específico"""
        from base_datos import ServitorCapaRepo

        servitor_id = ServitorCapaRepo.crear(
            user_id=401,
            nombre="Mensajero",
            intencion="Facilitar comunicación clara"
        )

        servitor = ServitorCapaRepo.obtener(servitor_id)

        self.assertIsNotNone(servitor)
        self.assertEqual(servitor['user_id'], 401)
        self.assertEqual(servitor['nombre'], "Mensajero")
        self.assertEqual(servitor['estado'], "activo")
        self.assertEqual(servitor['energia'], 50)  # Valor inicial

    def test_servitor_listar_por_usuario(self):
        """Listar servitors de un usuario"""
        from base_datos import ServitorCapaRepo

        ServitorCapaRepo.crear(402, "Guardián", "Protección")
        ServitorCapaRepo.crear(402, "Guía", "Sabiduría")
        ServitorCapaRepo.crear(403, "Sanador", "Curación")

        servitors_402 = ServitorCapaRepo.listar_por_usuario(402)
        servitors_403 = ServitorCapaRepo.listar_por_usuario(403)

        self.assertEqual(len(servitors_402), 2)
        self.assertEqual(len(servitors_403), 1)

    def test_servitor_evocar(self):
        """Evocar servitor aumenta energía"""
        from base_datos import ServitorCapaRepo

        servitor_id = ServitorCapaRepo.crear(404, "Atrayente", "Magnetismo")
        servitor_inicial = ServitorCapaRepo.obtener(servitor_id)
        energia_inicial = servitor_inicial['energia']

        ServitorCapaRepo.evocar(servitor_id)
        servitor_evocado = ServitorCapaRepo.obtener(servitor_id)

        self.assertGreater(servitor_evocado['energia'], energia_inicial)

    def test_servitor_disolver(self):
        """Disolver servitor cambia estado"""
        from base_datos import ServitorCapaRepo

        servitor_id = ServitorCapaRepo.crear(405, "Temporal", "Tarea corta")

        ServitorCapaRepo.disolver(servitor_id)
        servitor = ServitorCapaRepo.obtener(servitor_id)

        self.assertEqual(servitor['estado'], "disolviendo")


class TestServitorEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 2 - Servitors"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def test_post_crear_servitor(self):
        """POST /api/capa2/servitor/crear — crear nuevo servitor"""
        response = self.client.post(
            "/api/capa2/servitor/crear",
            headers=self.app.headers(self.cod),
            json={
                "nombre": "Protector",
                "intencion": "Defensa energética"
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("servitor_id", data)
        self.assertIn("exp_ganada", data)

    def test_get_listar_servitors(self):
        """GET /api/capa2/servitor — listar servitors del usuario"""
        # Crear dos servitors
        self.client.post(
            "/api/capa2/servitor/crear",
            headers=self.app.headers(self.cod),
            json={"nombre": "Guardián", "intencion": "Protección"}
        )
        self.client.post(
            "/api/capa2/servitor/crear",
            headers=self.app.headers(self.cod),
            json={"nombre": "Guía", "intencion": "Sabiduría"}
        )

        response = self.client.get(
            "/api/capa2/servitor",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["servitors"]), 2)

    def test_post_evocar_servitor(self):
        """POST /api/capa2/servitor/{id}/evocar — evocar servitor"""
        # Crear servitor primero
        create_resp = self.client.post(
            "/api/capa2/servitor/crear",
            headers=self.app.headers(self.cod),
            json={"nombre": "Invocable", "intencion": "Test"}
        )
        servitor_id = create_resp.get_json()["servitor_id"]

        response = self.client.post(
            f"/api/capa2/servitor/{servitor_id}/evocar",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("energia", data)
        self.assertIn("exp_ganada", data)


class TestEsferaCapaRepo(unittest.TestCase):
    """RED: Tests para EsferaCapaRepo (esferas de Capa 3 - usuario level)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_esfera_crear_geo(self):
        """Crear esfera geográfica"""
        from base_datos import EsferaCapaRepo

        esfera_id = EsferaCapaRepo.crear(
            user_id=500,
            tipo="geo",
            clave="bosque-tempestuoso",
            metadata={"region": "patagonia", "clima": "lluvia"}
        )

        self.assertIsNotNone(esfera_id)
        self.assertIsInstance(esfera_id, int)

    def test_esfera_crear_elemental(self):
        """Crear esfera elemental"""
        from base_datos import EsferaCapaRepo

        esfera_id = EsferaCapaRepo.crear(
            user_id=501,
            tipo="elemental",
            clave="fuego-transmutacion",
            metadata={"elemento": "fuego", "intension": "transformacion"}
        )

        self.assertIsNotNone(esfera_id)
        self.assertIsInstance(esfera_id, int)

    def test_esfera_obtener(self):
        """Obtener esfera por ID"""
        from base_datos import EsferaCapaRepo

        esfera_id = EsferaCapaRepo.crear(
            user_id=502,
            tipo="tematica",
            clave="amor-propio",
            metadata={"tema": "autoamor"}
        )

        esfera = EsferaCapaRepo.obtener(esfera_id)

        self.assertIsNotNone(esfera)
        self.assertEqual(esfera['user_id'], 502)
        self.assertEqual(esfera['tipo'], "tematica")
        self.assertEqual(esfera['estado'], "activa")
        self.assertEqual(esfera['amplitud'], 1.0)

    def test_esfera_listar_por_usuario(self):
        """Listar esferas activas de usuario"""
        from base_datos import EsferaCapaRepo

        EsferaCapaRepo.crear(503, "geo", "montaña", {})
        EsferaCapaRepo.crear(503, "elemental", "aire", {})
        EsferaCapaRepo.crear(504, "resonancia", "grupo", {})

        esferas_503 = EsferaCapaRepo.listar_por_usuario(503)
        esferas_504 = EsferaCapaRepo.listar_por_usuario(504)

        self.assertEqual(len(esferas_503), 2)
        self.assertEqual(len(esferas_504), 1)

    def test_esfera_marcar_resonancia(self):
        """Marcar esfera bajo el Canelo (aumenta amplitud)"""
        from base_datos import EsferaCapaRepo

        esfera_id = EsferaCapaRepo.crear(505, "tematica", "compasion", {})
        esfera_inicial = EsferaCapaRepo.obtener(esfera_id)
        amplitud_inicial = esfera_inicial['amplitud']

        EsferaCapaRepo.marcar_resonancia(esfera_id)
        esfera_marcada = EsferaCapaRepo.obtener(esfera_id)

        self.assertGreater(esfera_marcada['amplitud'], amplitud_inicial)

    def test_esfera_listar_por_tipo(self):
        """Listar esferas por tipo específico"""
        from base_datos import EsferaCapaRepo

        EsferaCapaRepo.crear(506, "geo", "costa", {})
        EsferaCapaRepo.crear(506, "geo", "desierto", {})
        EsferaCapaRepo.crear(506, "elemental", "agua", {})

        geo = EsferaCapaRepo.listar_por_tipo(506, "geo")
        elem = EsferaCapaRepo.listar_por_tipo(506, "elemental")

        self.assertEqual(len(geo), 2)
        self.assertEqual(len(elem), 1)


class TestEsferaEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 3 - Esferas"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def test_get_esferas_listar(self):
        """GET /api/capa3/esferas — listar esferas del usuario"""
        response = self.client.get(
            "/api/capa3/esferas",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("esferas", data)
        self.assertIn("total", data)

    def test_get_esferas_por_tipo(self):
        """GET /api/capa3/esferas?tipo=geo — filtrar por tipo"""
        response = self.client.get(
            "/api/capa3/esferas?tipo=geo",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # En caso de haber esferas, verificar que son del tipo correcto
        if data["esferas"]:
            for esfera in data["esferas"]:
                self.assertEqual(esfera["tipo"], "geo")


class TestSigiloAportadoRepo(unittest.TestCase):
    """RED: Tests para SigiloAportadoRepo (semillas de Capa 3 - sigilos sembrados)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_sigilo_aportado_aportar(self):
        """Sembrar sigilo en El Árbol devuelve un id entero."""
        from base_datos import SigiloAportadoRepo

        aportado_id = SigiloAportadoRepo.aportar(
            user_id=600,
            sigilo_dibujado_id=10,
            esfera_capa3_id=20,
            intencion="que florezca la abundancia colectiva",
        )

        self.assertIsNotNone(aportado_id)
        self.assertIsInstance(aportado_id, int)

    def test_sigilo_aportado_obtener(self):
        """Obtener semilla por ID con estado inicial 'germinando'."""
        from base_datos import SigiloAportadoRepo

        aportado_id = SigiloAportadoRepo.aportar(
            user_id=601,
            sigilo_dibujado_id=11,
            esfera_capa3_id=21,
            intencion="claridad",
        )

        semilla = SigiloAportadoRepo.obtener(aportado_id)

        self.assertIsNotNone(semilla)
        self.assertEqual(semilla["user_id"], 601)
        self.assertEqual(semilla["sigilo_dibujado_id"], 11)
        self.assertEqual(semilla["esfera_capa3_id"], 21)
        self.assertEqual(semilla["intencion"], "claridad")
        self.assertEqual(semilla["estado"], "germinando")

    def test_sigilo_aportado_obtener_inexistente(self):
        """Obtener semilla inexistente devuelve None."""
        from base_datos import SigiloAportadoRepo

        self.assertIsNone(SigiloAportadoRepo.obtener(999999))

    def test_sigilo_aportado_listar_anonimos(self):
        """Listado colectivo NO expone user_id ni sigilo_dibujado_id."""
        from base_datos import SigiloAportadoRepo

        SigiloAportadoRepo.aportar(602, 12, 22, "anónima uno")
        SigiloAportadoRepo.aportar(603, 13, 23, "anónima dos")

        semillas = SigiloAportadoRepo.listar_anonimos()

        self.assertGreaterEqual(len(semillas), 2)
        for semilla in semillas:
            self.assertNotIn("user_id", semilla)
            self.assertNotIn("sigilo_dibujado_id", semilla)
            self.assertIn("intencion", semilla)
            self.assertIn("estado", semilla)

    def test_sigilo_aportado_transitar_estado(self):
        """Transición de estado germinando → brotado."""
        from base_datos import SigiloAportadoRepo

        aportado_id = SigiloAportadoRepo.aportar(604, 14, 24, "crecer")

        semilla = SigiloAportadoRepo.transitar_estado(aportado_id, "brotado")

        self.assertIsNotNone(semilla)
        self.assertEqual(semilla["estado"], "brotado")

    def test_sigilo_aportado_listar_por_esfera(self):
        """Listar semillas conectadas a una esfera específica."""
        from base_datos import SigiloAportadoRepo

        SigiloAportadoRepo.aportar(605, 15, 700, "una")
        SigiloAportadoRepo.aportar(606, 16, 700, "dos")
        SigiloAportadoRepo.aportar(607, 17, 701, "tres")

        en_700 = SigiloAportadoRepo.listar_por_esfera(700)
        en_701 = SigiloAportadoRepo.listar_por_esfera(701)

        self.assertEqual(len(en_700), 2)
        self.assertEqual(len(en_701), 1)


class TestSemillaEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 3 - Semillas (sigilos sembrados)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def _crear_sigilo(self) -> int:
        """Dibuja un sigilo en Capa 1 y devuelve su id."""
        resp = self.client.post(
            "/api/capa1/sigilo/dibujar",
            headers=self.app.headers(self.cod),
            json={"intencion": "manifestar", "dibujo": "data:image/png;base64,AAA"},
        )
        return resp.get_json()["sigilo"]["id"]

    def test_post_semilla_sigilo(self):
        """POST /api/capa3/semilla/sigilo — sembrar sigilo en El Árbol."""
        sigilo_id = self._crear_sigilo()
        self.app.reset_rate_limit()

        response = self.client.post(
            "/api/capa3/semilla/sigilo",
            headers=self.app.headers(self.cod),
            json={
                "sigilo_dibujado_id": sigilo_id,
                "esfera_tipo": "tematica",
                "esfera_clave": "abundancia",
                "intencion": "que crezca en el colectivo",
            },
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("semilla_id", data)
        self.assertEqual(data["estado"], "germinando")
        self.assertIn("exp_ganada", data)

    def test_get_semillas_anonimas(self):
        """GET /api/capa3/semillas — listado colectivo sin fugas de identidad."""
        sigilo_id = self._crear_sigilo()
        self.app.reset_rate_limit()
        self.client.post(
            "/api/capa3/semilla/sigilo",
            headers=self.app.headers(self.cod),
            json={
                "sigilo_dibujado_id": sigilo_id,
                "esfera_tipo": "tematica",
                "esfera_clave": "compasion",
            },
        )
        self.app.reset_rate_limit()

        response = self.client.get(
            "/api/capa3/semillas",
            headers=self.app.headers(self.cod),
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("semillas", data)
        self.assertIn("total", data)
        for semilla in data["semillas"]:
            self.assertNotIn("user_id", semilla)
            self.assertNotIn("sigilo_dibujado_id", semilla)


class TestSincronicidadCapaRepo(unittest.TestCase):
    """RED: Tests para SincronicidadCapaRepo (sincronicidades colectivas Capa 3)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_sync_registrar(self):
        """Registrar sincronicidad devuelve un id entero."""
        from base_datos import SincronicidadCapaRepo

        sync_id = SincronicidadCapaRepo.registrar(
            user_id=700,
            descripcion="vi el número 1111 tres veces hoy",
            categoria="numeros",
            fase_lunar="full",
        )

        self.assertIsNotNone(sync_id)
        self.assertIsInstance(sync_id, int)

    def test_sync_obtener(self):
        """Obtener sincronicidad con confirmada=False y fase capturada."""
        from base_datos import SincronicidadCapaRepo

        sync_id = SincronicidadCapaRepo.registrar(
            user_id=701,
            descripcion="soñé con un cuervo y luego lo vi",
            categoria="animales",
            fase_lunar="new",
        )

        sync = SincronicidadCapaRepo.obtener(sync_id)

        self.assertIsNotNone(sync)
        self.assertEqual(sync["user_id"], 701)
        self.assertEqual(sync["categoria"], "animales")
        self.assertEqual(sync["fase_lunar"], "new")
        self.assertFalse(sync["confirmada"])

    def test_sync_confirmar(self):
        """Confirmar una sincronicidad la marca como confirmada."""
        from base_datos import SincronicidadCapaRepo

        sync_id = SincronicidadCapaRepo.registrar(
            702, "patrón repetido", "patrones", "first_q"
        )

        sync = SincronicidadCapaRepo.confirmar(sync_id)

        self.assertIsNotNone(sync)
        self.assertTrue(sync["confirmada"])

    def test_sync_listar_por_fase(self):
        """Listar sincronicidades por fase lunar (anónimas)."""
        from base_datos import SincronicidadCapaRepo

        SincronicidadCapaRepo.registrar(703, "una", "general", "full")
        SincronicidadCapaRepo.registrar(704, "dos", "general", "full")
        SincronicidadCapaRepo.registrar(705, "tres", "general", "new")

        llena = SincronicidadCapaRepo.listar_por_fase("full")
        nueva = SincronicidadCapaRepo.listar_por_fase("new")

        self.assertGreaterEqual(len(llena), 2)
        self.assertGreaterEqual(len(nueva), 1)
        for sync in llena:
            self.assertNotIn("user_id", sync)
            self.assertEqual(sync["fase_lunar"], "full")


class TestSincronicidadEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 3 - Sincronicidades"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def test_post_sync_registrar(self):
        """POST /api/capa3/sync/registrar — captura fase lunar automáticamente."""
        response = self.client.post(
            "/api/capa3/sync/registrar",
            headers=self.app.headers(self.cod),
            json={
                "descripcion": "escuché la misma canción en tres lugares",
                "categoria": "musica",
            },
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("sync_id", data)
        self.assertIn("fase_lunar", data)
        self.assertIn("exp_ganada", data)

    def test_get_sync_listar_anonimo(self):
        """GET /api/capa3/sync — listado colectivo sin fuga de identidad."""
        self.client.post(
            "/api/capa3/sync/registrar",
            headers=self.app.headers(self.cod),
            json={"descripcion": "sincronía observada", "categoria": "general"},
        )
        self.app.reset_rate_limit()

        response = self.client.get(
            "/api/capa3/sync",
            headers=self.app.headers(self.cod),
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("sincronicidades", data)
        self.assertIn("total", data)
        for sync in data["sincronicidades"]:
            self.assertNotIn("user_id", sync)


class TestMicorrizaRepo(unittest.TestCase):
    """RED: Tests para MicorrizaRepo (conexión ritual entre magos - Capa 3)"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_micorriza_conectar(self):
        """Conectar dos magos devuelve un id entero."""
        from base_datos import MicorrizaRepo

        micorriza_id = MicorrizaRepo.conectar(
            user_a_id=800,
            user_b_id=801,
            ritual="cruce bajo la luna llena",
        )

        self.assertIsNotNone(micorriza_id)
        self.assertIsInstance(micorriza_id, int)

    def test_micorriza_obtener(self):
        """Obtener conexión con estado inicial 'activa'."""
        from base_datos import MicorrizaRepo

        micorriza_id = MicorrizaRepo.conectar(802, 803, "hilo de fuego")

        micorriza = MicorrizaRepo.obtener(micorriza_id)

        self.assertIsNotNone(micorriza)
        self.assertEqual(micorriza["ritual"], "hilo de fuego")
        self.assertEqual(micorriza["estado"], "activa")

    def test_micorriza_listar_activas(self):
        """Listar conexiones activas desde ambos lados de la relación."""
        from base_datos import MicorrizaRepo

        MicorrizaRepo.conectar(810, 811, "uno")   # 810 es A
        MicorrizaRepo.conectar(812, 810, "dos")   # 810 es B
        MicorrizaRepo.conectar(813, 814, "tres")  # no relacionado

        activas = MicorrizaRepo.listar_activas(810)

        self.assertEqual(len(activas), 2)
        # El "otro mago" nunca es uno mismo.
        for conexion in activas:
            self.assertNotEqual(conexion["otro_mago_id"], 810)

    def test_micorriza_romper(self):
        """Romper conexión la quita de las activas."""
        from base_datos import MicorrizaRepo

        micorriza_id = MicorrizaRepo.conectar(820, 821, "frágil")

        rota = MicorrizaRepo.romper(micorriza_id)

        self.assertEqual(rota["estado"], "rota")
        self.assertEqual(len(MicorrizaRepo.listar_activas(820)), 0)


class TestMicorrizaEndpoints(unittest.TestCase):
    """Tests de integración para endpoints Capa 3 - Micorriza"""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        """Reset rate limit antes de cada test."""
        self.app.reset_rate_limit()
        self.cod_a = self.app.crear_proyecto("MagoA")

    def _materializar_mago(self, nombre: str) -> tuple[str, int]:
        """Crea un proyecto y materializa su usuario, devuelve (codigo, user_id)."""
        cod = self.app.crear_proyecto(nombre)
        resp = self.client.get(
            "/api/capa1/usuario/actual",
            headers=self.app.headers(cod),
        )
        return cod, resp.get_json()["usuario"]["id"]

    def test_post_micorriza_conectar(self):
        """POST /api/capa3/micorriza/conectar — ritual entre dos magos."""
        _, user_b_id = self._materializar_mago("MagoB")
        self.app.reset_rate_limit()

        response = self.client.post(
            "/api/capa3/micorriza/conectar",
            headers=self.app.headers(self.cod_a),
            json={"otro_mago_id": user_b_id, "ritual": "trenza de raíces"},
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("micorriza_id", data)
        self.assertIn("exp_ganada", data)

    def test_get_micorriza_listar(self):
        """GET /api/capa3/micorriza — conexiones activas con nombre del otro mago."""
        _, user_b_id = self._materializar_mago("MagoC")
        self.app.reset_rate_limit()
        self.client.post(
            "/api/capa3/micorriza/conectar",
            headers=self.app.headers(self.cod_a),
            json={"otro_mago_id": user_b_id, "ritual": "puente"},
        )
        self.app.reset_rate_limit()

        response = self.client.get(
            "/api/capa3/micorriza",
            headers=self.app.headers(self.cod_a),
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("conexiones", data)
        self.assertEqual(len(data["conexiones"]), 1)
        conexion = data["conexiones"][0]
        # Nombre del otro mago visible, sin datos privados.
        self.assertIn("otro_mago", conexion)
        self.assertIn("ritual", conexion)


if __name__ == "__main__":
    unittest.main()
