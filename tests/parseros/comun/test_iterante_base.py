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

    def test_iterador_funciona(self):
        from mzbackup.mock import MockOpen
        from mzbackup.parseros.iterador import Iterador
        fichero = MockOpen(CONTENIDO_UNO)

        iterante = Iterador()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]

        self.assertEqual(len(resultado), 3)
    
    def test_iterador_contenido_correcto(self):
        from mzbackup.mock import MockOpen
        from mzbackup.parseros.iterador import Iterador
        fichero = MockOpen(CONTENIDO_UNO)

        iterante = Iterador()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]

        self.assertEqual(resultado, CONTENIDO_UNO.strip().split("\n"))

    def test_iterador_terminar_con_vacio(self):
        """En realidad no esta tan vacío, pero es por culpa del contenido que puedo poner"""
        from mzbackup.mock import MockOpen
        from mzbackup.parseros.iterador import Iterador
        fichero = MockOpen(CONTENIDO_VACIO)

        iterante = Iterador()
        iterante.configurar_contenido(fichero)
        resultado = [linea for linea in iterante]

        self.assertEqual(resultado, [''])

    def test_iterador_siguiente_linea(self):
        """En realidad no esta tan vacío, pero es por culpa del contenido que puedo poner"""
        from mzbackup.mock import MockOpen
        from mzbackup.parseros.iterador import Iterador
        fichero = MockOpen(CONTENIDO_GENERICO)

        iterante = Iterador()
        iterante.configurar_contenido(fichero)
        linea_actual = next(iterante)
        linea_siguiente = iterante.linea_siguiente

        self.assertEqual((linea_actual, linea_siguiente), ("LINEA UNO", "LINEA DOS"))