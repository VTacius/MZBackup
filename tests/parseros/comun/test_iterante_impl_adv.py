from unittest import TestCase
from unittest.mock import patch, mock_open


class TestDescribeFinalObjeto(TestCase):
    """self._describe_final_objeto permite cambiar la descripción del final de objeto"""

    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.iterador import IteradorFichero

        class Iterante(IteradorFichero):

            def _linea_inicia_objeto(self, linea):
                return linea == "INICIO"

            def _describe_final_objeto(self):
                """Ni siquiera del _linea_inicia_objeto de que lineas uses"""
                return self.linea_actual == "CASI FIN" and self.linea_siguiente == "FIN"

        cls.Iterador = Iterante

    def test_describe_final_objeto(self):
        contenido = mock_open(read_data=CONTENIDO_4.strip())

        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            # resultado = [linea for linea in iterante if iterante.en_recoleccion]
            resultado = [linea for linea in iterante if iterante.fin_objeto()]

            # self.assertEqual(resultado, ["TODO", "TODO"])
            self.assertEqual(resultado, ["CASI FIN"])


class TestIteranteImplementacionAvanzada(TestCase):
    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.iterador import IteradorFichero

        class IterantePrueba(IteradorFichero):

            def _linea_inicia_objeto(self, linea):
                return linea == "INICIO"

            def _describe_final_objeto(self):
                return self.linea_actual == "" and self.linea_siguiente == "members"

        cls.Iterador = IterantePrueba

    def test_contenido_unico(self):
        contenido = mock_open(read_data=CONTENIDO_UNO.strip())
        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()]
            self.assertEqual(resultado, ["FINAL"])

    def test_finaliza_una_vez(self):
        contenido = mock_open(read_data=CONTENIDO_DOS.strip())
        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()]
            self.assertEqual(resultado, ["FINAL"])

    def test_finaliza_solo_con_recolecion(self):
        contenido = mock_open(read_data=CONTENIDO_TRES.strip())
        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            iterante = self.Iterador()
            iterante.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()]
            self.assertEqual(resultado, ["FINAL"])


CONTENIDO_UNO = """
INICIO
clave=: valor
key=: value

members
"""

CONTENIDO_DOS = """
INICIO
clave=: valor
key=: value
members: Usuario Principal

members
Usuario Principal
"""

CONTENIDO_TRES = """
INICIO
clave=: valor
key=: value
members: Usuario Principal

members
Usuario Principal

ERROR
Usuario Principal
"""

CONTENIDO_4 = """
INICIO
TODO
TODO
CASI FIN
FIN
NADA
NADA
"""
