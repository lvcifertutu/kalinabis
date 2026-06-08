"""Paquete base_datos — Persistencia de Kalinabis.

Imports explícitos recomendados (producción):

    from base_datos.proyecto  import ProyectoRepo, ConversacionRepo
    from base_datos.esferas   import EsferaRepo
    from base_datos.practicas import ServitorRepo, SyncRepo, ParadigmaRepo
    from base_datos.usuario   import UsuarioRepo, ExpRepo, LogroRepo
    from base_datos.grimorio  import GrimorioRepo, SigiloRepo
    from base_datos.altar     import TarotRepo, OráculoRepo, ConversacionCapaRepo, ServitorCapaRepo
    from base_datos.bosque    import EsferaCapaRepo, SigiloAportadoRepo, SincronicidadCapaRepo, MicorrizaRepo
    from base_datos.legacy    import ConversacionLegadoRepo, DecisionRepo, GrimorioLegadoRepo
    from base_datos.legacy    import SigiloLegadoRepo, CartaNatalRepo, EstadoAlmaRepo, estadisticas
    from base_datos.schema    import inicializar_db

Re-exports para compatibilidad con tests existentes (from base_datos import X):
"""

from base_datos.schema import inicializar_db

from base_datos.proyecto import ProyectoRepo, ConversacionRepo
from base_datos.esferas import EsferaRepo
from base_datos.practicas import ServitorRepo, SyncRepo, ParadigmaRepo
from base_datos.usuario import UsuarioRepo, ExpRepo, LogroRepo
from base_datos.grimorio import GrimorioRepo, SigiloRepo
from base_datos.altar import TarotRepo, OráculoRepo, ConversacionCapaRepo, ServitorCapaRepo
from base_datos.bosque import (
    EsferaCapaRepo, SigiloAportadoRepo,
    SincronicidadCapaRepo, MicorrizaRepo,
)
from base_datos.legacy import (
    ConversacionLegadoRepo, DecisionRepo, GrimorioLegadoRepo,
    EstadoAlmaRepo, SigiloLegadoRepo, CartaNatalRepo,
    estadisticas,
)

# Aliases de las funciones legacy para código que las usa directamente
guardar_mensaje    = ConversacionLegadoRepo.guardar
cargar_memoria     = ConversacionLegadoRepo.cargar
limpiar_memoria    = ConversacionLegadoRepo.limpiar
guardar_decision   = DecisionRepo.guardar
historial_decisiones = DecisionRepo.historial
escribir_grimorio  = GrimorioLegadoRepo.escribir
leer_grimorio      = GrimorioLegadoRepo.leer
guardar_sigilo     = SigiloLegadoRepo.guardar
leer_sigilos       = SigiloLegadoRepo.listar
cargar_sigilo      = SigiloLegadoRepo.cargar
quemar_sigilo      = SigiloLegadoRepo.quemar
guardar_carta_natal = CartaNatalRepo.guardar
leer_carta_natal   = CartaNatalRepo.leer
