"""Tests de Fase 2 — Backend Foundation (Usuarios, Exp, Grimorio).

RED: Tests para UsuarioRepo, ExpRepo, GrimorioRepo.
Correr: python -m unittest tests.test_fase2_backend
"""

import unittest
from datetime import datetime

try:
    from tests.harness import AppDeTest
except ImportError:
    from harness import AppDeTest


class TestUsuarioRepo(unittest.TestCase):
    """RED: Tests para UsuarioRepo (crear, obtener usuario)."""

    @classmethod
    def setUpClass(cls):
        """Inicia la app de test una sola vez."""
        cls.app = AppDeTest()

    def test_crear_usuario_devuelve_dict_con_id(self):
        """RED: crear(nombre_mago) debe devolver dict con id, nombre_mago, modelo, created_at."""
        # Importar aquí para que use la BD de test
        from base_datos import UsuarioRepo

        usuario = UsuarioRepo.crear(nombre_mago="Mago Solitario")

        self.assertIsNotNone(usuario)
        self.assertIn("id", usuario)
        self.assertIn("nombre_mago", usuario)
        self.assertIn("modelo", usuario)
        self.assertIn("created_at", usuario)
        self.assertEqual(usuario["nombre_mago"], "Mago Solitario")
        self.assertEqual(usuario["modelo"], "aprendiz")  # Modelo por defecto

    def test_obtener_usuario_devuelve_datos_completos(self):
        """RED: obtener(user_id) debe devolver usuario con todos los campos."""
        from base_datos import UsuarioRepo

        # Crear un usuario
        usuario_creado = UsuarioRepo.crear(nombre_mago="Aprendiz Nórdico", modelo="aprendiz")
        user_id = usuario_creado["id"]

        # Obtener el mismo usuario
        usuario_obtenido = UsuarioRepo.obtener(user_id)

        self.assertIsNotNone(usuario_obtenido)
        self.assertEqual(usuario_obtenido["id"], user_id)
        self.assertEqual(usuario_obtenido["nombre_mago"], "Aprendiz Nórdico")
        self.assertEqual(usuario_obtenido["modelo"], "aprendiz")

    def test_obtener_usuario_inexistente_devuelve_none(self):
        """RED: obtener(user_id_inexistente) debe devolver None."""
        from base_datos import UsuarioRepo

        usuario = UsuarioRepo.obtener(99999)
        self.assertIsNone(usuario)

    def test_crear_usuario_con_modelo_arbol(self):
        """RED: crear() acepta modelo='arbol'."""
        from base_datos import UsuarioRepo

        usuario = UsuarioRepo.crear(nombre_mago="Mago del Árbol", modelo="arbol")

        self.assertEqual(usuario["modelo"], "arbol")
        self.assertEqual(usuario["nombre_mago"], "Mago del Árbol")


class TestExpRepo(unittest.TestCase):
    """RED: Tests para ExpRepo (crear, actualizar, obtener exp de user+capa)."""

    @classmethod
    def setUpClass(cls):
        cls.app = AppDeTest()

    def test_crear_exp_usuario_capa(self):
        """RED: crear_o_actualizar(user_id, capa, exp) crea entrada exp."""
        from base_datos import UsuarioRepo, ExpRepo

        usuario = UsuarioRepo.crear(nombre_mago="Experimentado")
        user_id = usuario["id"]

        exp = ExpRepo.crear_o_actualizar(user_id, capa="grimorio", exp=0, nivel=1)

        self.assertIsNotNone(exp)
        self.assertEqual(exp["user_id"], user_id)
        self.assertEqual(exp["capa"], "grimorio")
        self.assertEqual(exp["exp"], 0)
        self.assertEqual(exp["nivel"], 1)

    def test_obtener_exp_usuario_capa(self):
        """RED: obtener(user_id, capa) devuelve exp dict."""
        from base_datos import UsuarioRepo, ExpRepo

        usuario = UsuarioRepo.crear(nombre_mago="Iniciado")
        user_id = usuario["id"]

        ExpRepo.crear_o_actualizar(user_id, capa="mago", exp=50, nivel=2)
        exp = ExpRepo.obtener(user_id, "mago")

        self.assertIsNotNone(exp)
        self.assertEqual(exp["capa"], "mago")
        self.assertEqual(exp["exp"], 50)
        self.assertEqual(exp["nivel"], 2)

    def test_agregar_exp(self):
        """RED: agregar_exp(user_id, capa, cantidad) incrementa exp."""
        from base_datos import UsuarioRepo, ExpRepo

        usuario = UsuarioRepo.crear(nombre_mago="Adeptus")
        user_id = usuario["id"]

        ExpRepo.crear_o_actualizar(user_id, capa="arbol", exp=100, nivel=3)
        ExpRepo.agregar_exp(user_id, "arbol", 50)

        exp = ExpRepo.obtener(user_id, "arbol")
        self.assertEqual(exp["exp"], 150)

    def test_listar_por_usuario_todas_capas(self):
        """RED: listar_por_usuario(user_id) devuelve exp de todas las capas."""
        from base_datos import UsuarioRepo, ExpRepo

        usuario = UsuarioRepo.crear(nombre_mago="Integrado")
        user_id = usuario["id"]

        ExpRepo.crear_o_actualizar(user_id, capa="grimorio", exp=50, nivel=1)
        ExpRepo.crear_o_actualizar(user_id, capa="mago", exp=75, nivel=2)
        ExpRepo.crear_o_actualizar(user_id, capa="arbol", exp=25, nivel=1)

        exps = ExpRepo.listar_por_usuario(user_id)

        self.assertEqual(len(exps), 3)
        capas = {e["capa"] for e in exps}
        self.assertEqual(capas, {"grimorio", "mago", "arbol"})

    def test_obtener_todas_capas_user(self):
        """RED: obtener_todas_capas(user_id) devuelve dict {capa: exp}."""
        from base_datos import UsuarioRepo, ExpRepo

        usuario = UsuarioRepo.crear(nombre_mago="Todo-Capas")
        user_id = usuario["id"]

        ExpRepo.crear_o_actualizar(user_id, capa="grimorio", exp=100, nivel=2)
        ExpRepo.crear_o_actualizar(user_id, capa="mago", exp=200, nivel=3)

        resultado = ExpRepo.obtener_todas_capas(user_id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["grimorio"]["exp"], 100)
        self.assertEqual(resultado["mago"]["exp"], 200)
        self.assertIsNone(resultado.get("arbol"))


class TestGrimorioRepo(unittest.TestCase):
    """RED: Tests para GrimorioRepo (crear entrada, listar por usuario)."""

    @classmethod
    def setUpClass(cls):
        cls.app = AppDeTest()

    def test_crear_entrada_grimorio(self):
        """RED: crear(user_id, titulo, contenido) crea entrada."""
        from base_datos import UsuarioRepo, GrimorioRepo

        usuario = UsuarioRepo.crear(nombre_mago="Escritor")
        user_id = usuario["id"]

        entrada = GrimorioRepo.crear(
            user_id=user_id,
            titulo="Mi primer apunte",
            contenido="Hoy aprendí sobre sigilos",
            tags="sigilos,aprendizaje"
        )

        self.assertIsNotNone(entrada)
        self.assertIn("id", entrada)
        self.assertEqual(entrada["user_id"], user_id)
        self.assertEqual(entrada["titulo"], "Mi primer apunte")
        self.assertEqual(entrada["contenido"], "Hoy aprendí sobre sigilos")

    def test_listar_entradas_por_usuario(self):
        """RED: listar_por_usuario(user_id) devuelve lista de entradas."""
        from base_datos import UsuarioRepo, GrimorioRepo

        usuario = UsuarioRepo.crear(nombre_mago="Compilador")
        user_id = usuario["id"]

        GrimorioRepo.crear(user_id, "Entrada 1", "Contenido 1")
        GrimorioRepo.crear(user_id, "Entrada 2", "Contenido 2")

        entradas = GrimorioRepo.listar_por_usuario(user_id)

        self.assertEqual(len(entradas), 2)
        self.assertEqual(entradas[0]["titulo"], "Entrada 2")  # Más reciente primero
        self.assertEqual(entradas[1]["titulo"], "Entrada 1")


class TestLogroRepo(unittest.TestCase):
    """RED: Tests para LogroRepo (registrar logros/badges)."""

    @classmethod
    def setUpClass(cls):
        cls.app = AppDeTest()

    def test_registrar_logro(self):
        """RED: registrar(user_id, capa, nombre_logro) crea logro."""
        from base_datos import UsuarioRepo, LogroRepo

        usuario = UsuarioRepo.crear(nombre_mago="Aprendiz Aventajado")
        user_id = usuario["id"]

        logro = LogroRepo.registrar(user_id, capa="grimorio", nombre_logro="Iniciado")

        self.assertIsNotNone(logro)
        self.assertIn("id", logro)
        self.assertEqual(logro["user_id"], user_id)
        self.assertEqual(logro["capa"], "grimorio")
        self.assertEqual(logro["nombre_logro"], "Iniciado")

    def test_listar_logros_usuario(self):
        """RED: listar_por_usuario(user_id) devuelve todos los logros."""
        from base_datos import UsuarioRepo, LogroRepo

        usuario = UsuarioRepo.crear(nombre_mago="Logrador")
        user_id = usuario["id"]

        LogroRepo.registrar(user_id, "grimorio", "Neófito")
        LogroRepo.registrar(user_id, "grimorio", "Iniciado")
        LogroRepo.registrar(user_id, "mago", "Evocador")

        logros = LogroRepo.listar_por_usuario(user_id)

        self.assertEqual(len(logros), 3)
        nombres = {l["nombre_logro"] for l in logros}
        self.assertEqual(nombres, {"Neófito", "Iniciado", "Evocador"})

    def test_obtener_logro_mas_reciente(self):
        """RED: obtener_ultimo(user_id, capa) devuelve logro más reciente."""
        from base_datos import UsuarioRepo, LogroRepo

        usuario = UsuarioRepo.crear(nombre_mago="Graduado")
        user_id = usuario["id"]

        LogroRepo.registrar(user_id, "grimorio", "Iniciado")
        LogroRepo.registrar(user_id, "grimorio", "Adeptus")

        ultimo = LogroRepo.obtener_ultimo(user_id, "grimorio")

        self.assertIsNotNone(ultimo)
        self.assertEqual(ultimo["nombre_logro"], "Adeptus")


class TestSigiloRepo(unittest.TestCase):
    """RED: Tests para SigiloRepo (crear sigilo dibujado, cargar, disolver)."""

    @classmethod
    def setUpClass(cls):
        cls.app = AppDeTest()

    def test_crear_sigilo_dibujado(self):
        """RED: crear_dibujado(user_id, intencion, dibujo) crea sigilo."""
        from base_datos import UsuarioRepo, SigiloRepo

        usuario = UsuarioRepo.crear(nombre_mago="Sigilista")
        user_id = usuario["id"]

        sigilo = SigiloRepo.crear_dibujado(
            user_id=user_id,
            intencion="Manifestar claridad mental",
            dibujo="<svg>...</svg>",
            metodo_carga=None
        )

        self.assertIsNotNone(sigilo)
        self.assertIn("id", sigilo)
        self.assertEqual(sigilo["user_id"], user_id)
        self.assertEqual(sigilo["intencion"], "Manifestar claridad mental")
        self.assertEqual(sigilo["estado"], "creado")

    def test_listar_sigilos_usuario(self):
        """RED: listar_por_usuario(user_id) devuelve sigilos activos."""
        from base_datos import UsuarioRepo, SigiloRepo

        usuario = UsuarioRepo.crear(nombre_mago="Diseñador")
        user_id = usuario["id"]

        SigiloRepo.crear_dibujado(user_id, "Sigilo 1", "<svg>1</svg>")
        SigiloRepo.crear_dibujado(user_id, "Sigilo 2", "<svg>2</svg>")

        sigilos = SigiloRepo.listar_por_usuario(user_id)

        self.assertEqual(len(sigilos), 2)
        self.assertEqual(sigilos[0]["intencion"], "Sigilo 2")  # Más reciente primero

    def test_cargar_sigilo_marca_como_cargado(self):
        """RED: cargar(sigilo_id) cambia estado a 'cargado' y desaparece."""
        from base_datos import UsuarioRepo, SigiloRepo

        usuario = UsuarioRepo.crear(nombre_mago="Cargador")
        user_id = usuario["id"]

        sigilo = SigiloRepo.crear_dibujado(user_id, "Cargarse", "<svg/>")
        sigilo_id = sigilo["id"]

        # Cargar el sigilo
        resultado = SigiloRepo.cargar(sigilo_id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["estado"], "cargado")

        # Verificar que no aparece en listar_por_usuario (filtro estado != 'cargado')
        sigilos = SigiloRepo.listar_por_usuario(user_id)
        ids = [s["id"] for s in sigilos]
        self.assertNotIn(sigilo_id, ids)


class TestFase2Endpoints(unittest.TestCase):
    """Tests de integración para endpoints de Fase 2."""

    @classmethod
    def setUpClass(cls):
        cls.app = AppDeTest()
        cls.client = cls.app.client

    def setUp(self):
        self.app.reset_rate_limit()
        self.cod = self.app.crear_proyecto()

    def test_capa1_usuario_actual(self):
        """GET /api/capa1/usuario/actual devuelve usuario para proyecto."""
        r = self.client.get(
            "/api/capa1/usuario/actual",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn("usuario", data)
        self.assertIn("id", data["usuario"])
        self.assertIn("nombre_mago", data["usuario"])

    def test_capa1_grimorio_nueva_entrada(self):
        """POST /api/capa1/grimorio/nueva crea entrada."""
        r = self.client.post(
            "/api/capa1/grimorio/nueva",
            json={
                "titulo": "Mi primer apunte",
                "contenido": "Hoy aprendí sobre sigilos",
                "tags": "sigilos,learning"
            },
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(r.status_code, 201)
        data = r.get_json()
        self.assertIn("entrada", data)
        self.assertEqual(data["entrada"]["titulo"], "Mi primer apunte")

    def test_capa1_grimorio_listar(self):
        """GET /api/capa1/grimorio lista entradas."""
        # Crear 2 entradas
        self.client.post(
            "/api/capa1/grimorio/nueva",
            json={"titulo": "Entrada 1", "contenido": "Contenido 1"},
            headers=self.app.headers(self.cod)
        )
        self.client.post(
            "/api/capa1/grimorio/nueva",
            json={"titulo": "Entrada 2", "contenido": "Contenido 2"},
            headers=self.app.headers(self.cod)
        )

        r = self.client.get(
            "/api/capa1/grimorio",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["total"], 2)
        self.assertEqual(len(data["entradas"]), 2)

    def test_capa1_exp_obtener(self):
        """GET /api/capa1/exp obtiene progreso."""
        r = self.client.get(
            "/api/capa1/exp",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn("exp", data)
        self.assertIn("exp", data["exp"])
        self.assertEqual(data["exp"]["capa"], "grimorio")

    def test_capa1_sigilo_dibujar(self):
        """POST /api/capa1/sigilo/dibujar crea sigilo."""
        r = self.client.post(
            "/api/capa1/sigilo/dibujar",
            json={
                "intencion": "Manifestar claridad",
                "dibujo": "<svg>sigilo</svg>"
            },
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(r.status_code, 201)
        data = r.get_json()
        self.assertIn("sigilo", data)
        self.assertEqual(data["sigilo"]["estado"], "creado")

    def test_capa1_sigilos_listar(self):
        """GET /api/capa1/sigilos lista sigilos activos."""
        # Crear sigilo
        self.client.post(
            "/api/capa1/sigilo/dibujar",
            json={"intencion": "Sigilo 1", "dibujo": "<svg>1</svg>"},
            headers=self.app.headers(self.cod)
        )

        r = self.client.get(
            "/api/capa1/sigilos",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["sigilos"][0]["estado"], "creado")

    def test_capa1_sigilo_cargar(self):
        """POST /api/capa1/sigilo/<id>/cargar carga y desaparece."""
        # Crear sigilo
        r_crear = self.client.post(
            "/api/capa1/sigilo/dibujar",
            json={"intencion": "Cargar", "dibujo": "<svg/>"},
            headers=self.app.headers(self.cod)
        )
        sigilo_id = r_crear.get_json()["sigilo"]["id"]

        # Cargar
        r_cargar = self.client.post(
            f"/api/capa1/sigilo/{sigilo_id}/cargar",
            headers=self.app.headers(self.cod)
        )

        self.assertEqual(r_cargar.status_code, 200)
        data = r_cargar.get_json()
        self.assertEqual(data["sigilo"]["estado"], "cargado")

        # Verificar que desaparece de listar
        r_listar = self.client.get(
            "/api/capa1/sigilos",
            headers=self.app.headers(self.cod)
        )
        self.assertEqual(r_listar.get_json()["total"], 0)


if __name__ == "__main__":
    unittest.main()
