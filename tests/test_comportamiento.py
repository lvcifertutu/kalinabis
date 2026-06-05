"""Tests de comportamiento de Kalinabis.

Reemplazan los antiguos scripts contra localhost:5000 (test_validacion,
test_seguridad, test_rate_limit, test_backend) por asserts reales sobre el
Flask test client, con base temporal y adapter de IA falso.

Correr:  python -m unittest tests.test_comportamiento
   o:    python tests/test_comportamiento.py
"""

import unittest

try:
    from tests.harness import AppDeTest
except ImportError:  # ejecutado como script: python tests/test_comportamiento.py
    from harness import AppDeTest


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        # Aislar rate limiting entre tests (la clave es por IP+path).
        self.app.reset_rate_limit()


class TestValidacion(BaseTest):
    def test_consultar_sin_mensaje_devuelve_400(self):
        cod = self.app.crear_proyecto()
        r = self.client.post("/api/consultar", json={},
                             headers=self.app.headers(cod))
        self.assertEqual(r.status_code, 400)

    def test_consultar_mensaje_muy_largo_devuelve_400(self):
        cod = self.app.crear_proyecto()
        r = self.client.post("/api/consultar", json={"mensaje": "x" * 5000},
                             headers=self.app.headers(cod))
        self.assertEqual(r.status_code, 400)

    def test_consultar_sin_proyecto_devuelve_401(self):
        r = self.client.post("/api/consultar", json={"mensaje": "hola"})
        self.assertEqual(r.status_code, 401)

    def test_consultar_proyecto_invalido_devuelve_401(self):
        r = self.client.post("/api/consultar", json={"mensaje": "hola"},
                             headers=self.app.headers("codigo-falso-malo"))
        self.assertEqual(r.status_code, 401)

    def test_json_invalido_devuelve_400(self):
        r = self.client.post("/api/grimorio", data="esto no es json",
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_ruta_inexistente_devuelve_404(self):
        r = self.client.get("/api/noexiste")
        self.assertEqual(r.status_code, 404)
        self.assertIn("error", r.get_json())

    def test_grimorio_titulo_muy_largo_devuelve_400(self):
        r = self.client.post("/api/grimorio",
                             json={"titulo": "x" * 500, "contenido": "ok"})
        self.assertEqual(r.status_code, 400)

    def test_grimorio_contenido_muy_largo_devuelve_400(self):
        r = self.client.post("/api/grimorio",
                             json={"titulo": "ok", "contenido": "x" * 20000})
        self.assertEqual(r.status_code, 400)

    def test_sigilo_intencion_muy_larga_devuelve_400(self):
        r = self.client.post("/api/sigilo",
                             json={"intencion": "x" * 500, "imagen": "ok"})
        self.assertEqual(r.status_code, 400)


class TestRateLimit(BaseTest):
    def test_proyecto_nuevo_corta_a_la_sexta(self):
        self.app.reset_rate_limit()
        codigos = []
        for _ in range(5):
            r = self.client.post("/api/proyecto/nuevo", json={"nombre": "spam"})
            codigos.append(r.status_code)
        sexta = self.client.post("/api/proyecto/nuevo", json={"nombre": "spam"})
        self.assertTrue(all(s == 200 for s in codigos), codigos)
        self.assertEqual(sexta.status_code, 429)
        self.assertIn("retry_after", sexta.get_json())


class TestRateLimitAlgoritmo(BaseTest):
    """Unit test de la función real _check_rate_limit (no una copia)."""

    def test_permite_hasta_el_maximo_y_luego_corta(self):
        import servidor
        servidor._rate_limit_data.clear()
        permisos = [servidor._check_rate_limit("k1", 3600, 5)[0]
                    for _ in range(5)]
        permitido, retry = servidor._check_rate_limit("k1", 3600, 5)
        self.assertTrue(all(permisos))
        self.assertFalse(permitido)
        self.assertGreater(retry, 0)

    def test_claves_distintas_son_independientes(self):
        import servidor
        servidor._rate_limit_data.clear()
        servidor._check_rate_limit("a", 3600, 1)
        bloqueado_a = servidor._check_rate_limit("a", 3600, 1)[0]
        permitido_b = servidor._check_rate_limit("b", 3600, 1)[0]
        self.assertFalse(bloqueado_a)
        self.assertTrue(permitido_b)


class TestFlujosIA(BaseTest):
    def test_consultar_con_proyecto_responde(self):
        cod = self.app.crear_proyecto()
        self.app.ia.encolar("Soy Isis, te escucho.")
        r = self.client.post(
            "/api/consultar",
            json={"mensaje": "hola", "entidad": "isis"},
            headers=self.app.headers(cod),
        )
        self.assertEqual(r.status_code, 200)
        j = r.get_json()
        self.assertEqual(j["entidad"], "isis")
        self.assertEqual(j["respuesta"], "Soy Isis, te escucho.")

    def test_tarot_responde_y_persiste(self):
        cod = self.app.crear_proyecto()
        self.app.ia.encolar("La tirada habla de cambio.")
        cartas = [{"n": 0, "posicion": 0}, {"n": 1, "posicion": 1},
                  {"n": 2, "posicion": 2}]
        r = self.client.post("/api/tarot/leer/lilith", json={"cartas": cartas},
                             headers=self.app.headers(cod))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["entidad"], "lilith")
        # La conversación quedó persistida (2 mensajes).
        mem = self.client.get("/api/memoria/lilith",
                              headers=self.app.headers(cod)).get_json()
        self.assertEqual(len(mem), 2)

    def test_tarot_entidad_desconocida_devuelve_400(self):
        cod = self.app.crear_proyecto()
        r = self.client.post("/api/tarot/leer/zeus", json={"cartas": []},
                             headers=self.app.headers(cod))
        self.assertEqual(r.status_code, 400)

    def test_sigilo_regalo_devuelve_intencion_limpia(self):
        cod = self.app.crear_proyecto()
        self.app.ia.encolar('"cruzo el umbral con fuerza"')
        r = self.client.post("/api/sigilo/regalo/afrodita", json={},
                             headers=self.app.headers(cod))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["intencion"], "CRUZO EL UMBRAL CON FUERZA")

    def test_memoria_legacy_sin_header_devuelve_lista(self):
        r = self.client.get("/api/memoria/isis")
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.get_json(), list)

    def test_quemar_sin_proyecto_devuelve_401(self):
        r = self.client.post("/api/mensajes/quemar", json={"id": 1})
        self.assertEqual(r.status_code, 401)

    def test_quemar_id_invalido_devuelve_400(self):
        cod = self.app.crear_proyecto()
        r = self.client.post("/api/mensajes/quemar", json={"id": "no-int"},
                             headers=self.app.headers(cod))
        self.assertEqual(r.status_code, 400)


class TestProyecto(BaseTest):
    def test_crear_y_verificar_roundtrip(self):
        cod = self.app.crear_proyecto("Mi Proyecto")
        r = self.client.post("/api/proyecto/verificar",
                             headers=self.app.headers(cod))
        j = r.get_json()
        self.assertTrue(j["existe"])
        self.assertEqual(j["metadatos"]["nombre"], "Mi Proyecto")

    def test_verificar_codigo_inexistente(self):
        r = self.client.post("/api/proyecto/verificar",
                             headers=self.app.headers("codigo-que-no-existe"))
        self.assertFalse(r.get_json()["existe"])


class TestEndpointsLectura(BaseTest):
    """Smoke de endpoints GET de solo lectura (antes en test_backend.py)."""

    def test_luna(self):
        r = self.client.get("/api/luna")
        self.assertEqual(r.status_code, 200)
        self.assertIn("fase", r.get_json())

    def test_cosmologia(self):
        r = self.client.get("/api/cosmologia")
        self.assertEqual(r.status_code, 200)

    def test_esferas(self):
        r = self.client.get("/api/esferas")
        self.assertEqual(r.status_code, 200)
        self.assertIn("total", r.get_json())

    def test_bosque_mapa(self):
        r = self.client.get("/api/bosque/mapa")
        self.assertEqual(r.status_code, 200)
        self.assertIn("nodos", r.get_json())

    def test_bosque_salud(self):
        r = self.client.get("/api/bosque/salud")
        self.assertEqual(r.status_code, 200)

    def test_geografia_ecorregiones(self):
        r = self.client.get("/api/geografia/ecorregiones")
        self.assertEqual(r.status_code, 200)
        self.assertIn("total", r.get_json())

    def test_geografia_eje(self):
        r = self.client.post("/api/geografia/eje", json={"ubicacion": "Bogota"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("eje_del_mundo", r.get_json())

    def test_bosque_ciclo(self):
        r = self.client.post("/api/bosque/ciclo")
        self.assertEqual(r.status_code, 200)
        self.assertIn("actualizadas", r.get_json())


if __name__ == "__main__":
    unittest.main(verbosity=2)
