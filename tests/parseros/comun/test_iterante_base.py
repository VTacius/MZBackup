from unittest import TestCase
from unittest import mock
from unittest.mock import patch, mock_open


class TestIterante(TestCase):
    
    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.iterador import IteradorFichero
        
        class IteradorPrueba(IteradorFichero):
            def _linea_inicia_objeto(self):
                return False
        cls.Iterador = IteradorPrueba 

    def test_iterador_funciona(self):
        contenido = mock_open(read_data=CONTENIDO_UNO.strip())
        with patch("builtins.open", contenido, create=True):
            fichero = open('NADA')
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = [linea for linea in iterante]

            self.assertEqual(len(resultado), 3)
    
    def test_iterador_contenido_correcto(self):
        contenido = mock_open(read_data=CONTENIDO_UNO.strip())
        with patch("builtins.open", contenido, create=True):
            fichero = open('NADA')
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = [linea for linea in iterante]

            self.assertEqual(resultado, CONTENIDO_UNO.strip().split("\n"))

    def test_iterador_terminar_con_vacio(self):
        """Fichero vacío, no hay mayor problema: No hay contenido"""
        contenido = mock_open(read_data=CONTENIDO_VACIO.strip())
        with patch("builtins.open", contenido, create=True):
            fichero = open('NADA')
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = [linea for linea in iterante]

            self.assertEqual(resultado, [])

    def test_iterador_siguiente_linea(self):
        """A la primera iteración, se ha configurado linea_actual y linea_siguiente correctamente"""
        contenido = mock_open(read_data=CONTENIDO_GENERICO.strip())
        with patch("builtins.open", contenido, create=True):
            fichero = open('NADA')
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            linea_actual = next(iterante)
            linea_siguiente = iterante.linea_siguiente

            self.assertEqual((linea_actual, linea_siguiente), ("LINEA UNO", "LINEA DOS"))


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
