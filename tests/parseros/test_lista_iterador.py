from unittest import TestCase
from unittest.mock import mock_open, patch


class TestIteradorListas(TestCase):

    def test_es_primera_linea(self):
        from mzbackup.parseros.listas import IteradorListas
        recolector = IteradorListas()
        recolector._linea_actual = "# distributionList lista@dominio.com memberCount=11"
        resultado = recolector.inicio_objeto()
        self.assertTrue(resultado)

    def test_no_es_primera_linea(self):
        from mzbackup.parseros.listas import IteradorListas
        recolector = IteradorListas()
        recolector._linea_actual = "# distributionList lista@dominio.com"
        resultado = recolector.inicio_objeto()
        self.assertFalse(resultado)

    def test_es_ultima_linea(self):
        from mzbackup.parseros.listas import IteradorListas

        contenido = mock_open(read_data=CASO_1)

        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            recolector = IteradorListas()
            recolector.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in recolector if recolector.fin_objeto()]
            self.assertListEqual(resultado, ["FINAL"])

    def test_es_ultima_linea_multilinea(self):
        from mzbackup.parseros.listas import IteradorListas

        contenido = mock_open(read_data=CASO_2)

        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            recolector = IteradorListas()
            recolector.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in recolector if recolector.fin_objeto()]
            self.assertListEqual(resultado, ["FINAL"])


CASO_1 = """
# distributionList usi_dtic@salud.gob.sv memberCount=9
cn: # Unidad de Soporte Informático de la DTIC
zimbraMailStatus: enabled

members
"""

CASO_2 = """
zimbraNotes: Yasmin del Carmen Jaime de Diaz

members
"""
