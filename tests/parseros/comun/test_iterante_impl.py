from unittest import TestCase
from unittest.mock import patch, mock_open


class TestIteranteImplementacionBasica(TestCase):
    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.iterador import IteradorFichero

        class IterantePrueba(IteradorFichero):

            def _linea_inicia_objeto(self, linea):
                return linea == "INICIO"

        cls.Iterador = IterantePrueba

    def test_contenido_unico(self):
        """El iterador reconoce que fin de fichero también es fin de contenido"""
        contenido = mock_open(read_data=CONTENIDO_UNO.rstrip())

        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")

            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()]

            self.assertEqual(resultado, ["FINAL"])

    def test_separa_contenido(self):
        """Iterador reconoce un fin de contenido sólo si hubo antes un inicio de recolección"""
        contenido = mock_open(read_data=CONTENIDO_DOS.rstrip())

        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")

            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()]

            self.assertEqual(resultado, ["FINAL"])

    def test_separa_contenido_tres(self):
        """Iterador reconoce un fin de contenido y fin de fichero, sin solapar"""
        contenido = mock_open(read_data=CONTENIDO_TRES.rstrip())

        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")

        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()]

        self.assertEqual(resultado, ["FINAL", "FINAL"])


CONTENIDO_UNO = """
INICIO
clave=: valor
key=: value
"""

CONTENIDO_DOS = """
INICIO
clave=: valor
key=: value

ERROR
"""

CONTENIDO_TRES = """
INICIO
clave=: valor
key=: value

INICIO
clave=: valor
key=: value
"""
