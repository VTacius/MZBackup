from unittest import TestCase
from unittest.mock import mock_open, patch

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from mzbackup.parseros.cos import IteradorCos
        recolector = IteradorCos()
        recolector._linea_actual = "# name 750_NC"
        resultado = recolector.inicio_objeto()
        self.assertTrue(resultado)

    def test_es_ultima_linea(self):
        from mzbackup.parseros.cos import IteradorCos

        contenido = mock_open(read_data=CASO_1)

        with patch("builtins.open", contenido, create=True):
            fichero = open("NADA")
            recolector = IteradorCos()
            recolector.configurar_contenido(fichero)
            resultado = ["FINAL" for linea in recolector if recolector.fin_objeto()]
            self.assertListEqual(resultado, ["FINAL"])


CASO_1 = """
# name COS_750_NC
cn: COS_750_NC
objectClass: zimbraCOS
zimbraZimletLoadSynchronously: FALSE

# no_contenido default
"""
