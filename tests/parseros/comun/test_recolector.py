from unittest import TestCase
from unittest import mock

from mzbackup.parseros.recolector import Recolector

class RecolectorPrueba(Recolector):
    def _es_primera_linea(self, linea):
        return True
    
    def _es_final_de_contenido(self, linea):
        return True

class TestRecolector(TestCase):
    """Prueba del Recolector génerico""" 
    
    @mock.patch("mzbackup.utils.pato.Pato")
    @mock.patch('mzbackup.parseros.recolector.open')
    def test_es_ultima_linea_predeterminado(self, open, Pato):
        """Ultima línea ahora es un método que requiere a __fin_de_contenido y __primera_linea
        como implementación por defecto"""
        pato = Pato()
        recolector = RecolectorPrueba({}, {})
        recolector.configurar_destino(pato)

        resultado = recolector._es_ultima_linea("Línea actual", "Línea siguiente") 
        self.assertTrue(resultado, True)
