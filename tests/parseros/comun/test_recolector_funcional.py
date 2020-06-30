from unittest import TestCase
from unittest.mock import patch, mock_open


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
                """Devuelve todos los ficheros creados durante el uso de la implementacion de Europa"""
                return ['contenido'] 

        class IteradorPrueba(IteradorFichero):
            def _linea_inicia_objeto(self, linea):
                return linea.startswith("# name ")
        
        class RecolectorPrueba(Recolector):
            def _titulador(self, linea):
                return "comando" 
            
            def _crear_contenido_procesal(self, tokens, linea):
                return tokens['clave']
        
        cls.Recolector = RecolectorPrueba
        cls.Iterador = IteradorPrueba
        cls.Europa = EuropaMock

    def test_caso_base1(self):
        self.maxDiff = None
        from mzbackup.parseros.comun.recolector import Recolector
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

CONTENIDO_01 = """
# name vtacius@dominio.com
cn: Alexander Ortíz
zimbraPrefMailSignature: _________________________________________________________
Alexander Ortíz - Unidad de Redes 
Companía Central

zimbraPrefMailSignatureStyle: internet
"""

