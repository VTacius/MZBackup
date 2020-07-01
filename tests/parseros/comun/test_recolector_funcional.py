from unittest import TestCase
from unittest.mock import patch, mock_open

# TODO: En el segundo caso, hay una línea zimbra que no entra al comando
# TODO: ¿Acaba multilinea si hay un deprecated, procesal o sistema?


class TestRecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.recolector import Recolector
        from mzbackup.parseros.comun.iterador import IteradorFichero

        class EuropaMock():
            """Base abstracta de Europa"""
            def __init__(self):
                self.resultado = {}

            def guardar(self, identificador, contenido):
                self.resultado = contenido

            def listar_archivos(self):
                """Retorna los ficheros creados durante el uso de la implementacion de Europa"""
                return ['contenido']

        class IteradorPrueba(IteradorFichero):
            def _linea_inicia_objeto(self, linea):
                return linea.startswith("# name ")

        class RecolectorPrueba(Recolector):
            def _titulador(self, linea):
                return "comando"

            def _crear_contenido_procesal(self, tokens, linea):
                return tokens['clave'], "PROCESAL"

        cls.Recolector = RecolectorPrueba
        cls.Iterador = IteradorPrueba
        cls.Europa = EuropaMock

    def test_caso_base1(self):
        self.maxDiff = None
        from mzbackup.parseros.comun.tipo import Tipo

        atributos = {'posix': ['cn'], 'multilinea': 'zimbraPrefMailSignature'}
        tipo = Tipo(atributos)
        iterador = self.Iterador()
        europa = self.Europa()

        recolector = self.Recolector(tipo, iterador)
        recolector.configurar_destino(europa)

        contenido = mock_open(read_data=CONTENIDO_01.rstrip())
        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            recolector.configurar_contenido(fichero)
            recolector.procesar_contenido()
            contenido_multilinea = ["_________________________________________________________",
                                    "Alexander Ortíz - Unidad de Redes",
                                    "Companía Central", ""]
            esperado = {'comando': "comando cn 'Alexander Ortíz'",
                        'multilinea': {'zimbraPrefMailSignature': contenido_multilinea},
                        'procesal': {}}
            self.assertEqual(europa.resultado, esperado)

    def test_caso_base2(self):
        self.maxDiff = None
        from mzbackup.parseros.comun.tipo import Tipo

        atributos = {'posix': ['cn', 'description', 'displayName', 'company'],
                     'multilinea': 'zimbraPrefMailSignature',
                     'procesal': ['zimbraCOSId']}
        tipo = Tipo(atributos)
        iterador = self.Iterador()
        europa = self.Europa()

        recolector = self.Recolector(tipo, iterador)
        recolector.configurar_destino(europa)

        contenido = mock_open(read_data=CONTENIDO_02.rstrip())
        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            recolector.configurar_contenido(fichero)
            recolector.procesar_contenido()
            comando = "comando cn 'Silvia Larín' company 'Almacén Central'"
            comando += " description USERMODWEBADMIN displayName 'Silvia Larín'"
            comando += " zimbraBatchedIndexingSize 20"
            esperado = {'comando': comando,
                        'multilinea': {},
                        'procesal': {'zimbraCOSId': 'PROCESAL'}}
            self.assertEqual(europa.resultado, esperado)


CONTENIDO_01 = """
# name vtacius@dominio.com
cn: Alexander Ortíz
zimbraPrefMailSignature: _________________________________________________________
Alexander Ortíz - Unidad de Redes
Companía Central

zimbraPrefMailSignatureStyle: internet
"""


CONTENIDO_02 = """
# name slarin@dominio.com
cn: Silvia Larín
company: Almacén Central
description: USERMODWEBADMIN
displayName: Silvia Larín
zimbraBatchedIndexingSize: 20
zimbraCOSId: 41ed0b39-80f5-4043-b85a-c8568bfa2fb2
zimbraCalendarCalDavSharedFolderCacheDuration: 1m
"""
