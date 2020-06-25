from unittest import TestCase
from unittest import mock

CONTENIDO_VACIO = """
"""

CONTENIDO_GENERICO = """
LINEA UNO
LINEA DOS
"""

CONTENIDO_UNO = """
# name vtacius@dominio.com

# name kpena@dominio.com
"""


from mzbackup.parseros.iterante import Foreador

class MockOpen:
    def __init__(self, contenido):
        self.contenido = contenido.strip().split("\n")
        self.tamanio = len(self.contenido)
        self.iterador = 0

    def readline(self):
        resultado = ""
        if self.tamanio > self.iterador:
            resultado = self.contenido[self.iterador] + '\n'
            self.iterador += 1
        
        return resultado

class IterantePrueba(Foreador):
    
    def _inicia_contenido(self):
        return False
    
    def _finaliza_contenido(self):
        return False

class TestIterante(TestCase):

    def test_iterador_funciona(self):
        
        fichero = MockOpen(CONTENIDO_UNO)
        
        iterante = IterantePrueba()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]


        self.assertEqual(len(resultado), 3)
    
    def test_iterador_contenido_correcto(self):
        
        fichero = MockOpen(CONTENIDO_UNO)
        
        iterante = IterantePrueba()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]


        self.assertEqual(resultado, CONTENIDO_UNO.strip().split("\n"))
    
    def test_iterador_terminar_con_vacio(self):
        """En realidad no esta tan vacío, pero es por culpa del contenido que puedo poner"""
        
        fichero = MockOpen(CONTENIDO_VACIO)
        
        iterante = IterantePrueba()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]


        self.assertEqual(resultado, [''])
    
    def test_iterador_siguiente_linea(self):
        """En realidad no esta tan vacío, pero es por culpa del contenido que puedo poner"""
        
        fichero = MockOpen(CONTENIDO_GENERICO)
        
        iterante = IterantePrueba()
        iterante.configurar_contenido(fichero)
        linea_actual = next(iterante)
        linea_siguiente = iterante.linea_siguiente


        self.assertEqual((linea_actual, linea_siguiente), ("LINEA UNO", "LINEA DOS"))