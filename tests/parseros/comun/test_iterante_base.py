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


class TestIterante(TestCase):
    
    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.iterador import IteradorFichero
        
        class IteradorPrueba(IteradorFichero):
            def _linea_inicia_objeto(self):
                return False
        cls.Iterador = IteradorPrueba 

    def test_iterador_funciona(self):
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_UNO)

        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]

        self.assertEqual(len(resultado), 4)
    
    def test_iterador_contenido_correcto(self):
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_UNO)

        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]

        self.assertEqual(resultado, CONTENIDO_UNO.rstrip().split("\n"))

    def test_iterador_terminar_con_vacio(self):
        """En realidad no esta tan vacío, pero es por culpa del contenido que puedo poner"""
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_VACIO)

        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]

        self.assertEqual(resultado, [''])

    def test_iterador_siguiente_linea(self):
        """En realidad no esta tan vacío, pero es por culpa del contenido que puedo poner"""
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_GENERICO)

        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        next(iterante)
        linea_actual = next(iterante)
        linea_siguiente = iterante.linea_siguiente

        self.assertEqual((linea_actual, linea_siguiente), ("LINEA UNO", "LINEA DOS"))