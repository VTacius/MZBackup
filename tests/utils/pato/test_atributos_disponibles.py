from unittest import TestCase
from unittest.mock import patch


class TestAtributosDisponibles(TestCase):

    @patch("io.TextIOWrapper")
    def test_cambio_extension_fichero_existente(self, fichero):
        fichero.name = "/home/usuario/README.md"
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local({}, {}, {}, fichero)
        pato.extension = "mkv"
        self.assertEqual(str(pato), "/home/usuario/README.mkv")

    def test_cambio_extension_fichero_nuevo(self):
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '13-12-11', '/opt/backup', None)
        pato.extension = "mkv"
        self.assertEqual(str(pato), "/opt/backup/cos-13-12-11/cos.mkv")
