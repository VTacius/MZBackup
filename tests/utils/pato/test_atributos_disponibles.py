from unittest import TestCase


class TestAtributosDisponibles(TestCase):

    @classmethod
    def setUpClass(cls):
        class Vacio:
            pass

        cls.fichero = Vacio()
        cls.fichero.name = "/home/usuario/README.md"

    def test_cambio_extension_fichero_nuevo(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, self.fichero, {})
        pato.extension = "mkv"
        self.assertEqual(str(pato), "/home/usuario/README.mkv")

    def test_cambio_extension_fichero_existente(self):
        from mzbackup.utils.pato import Pato
        pato = Pato('cos', '13-12-11',  None, '/opt/backup')
        pato.extension = "mkv"
        self.assertEqual(str(pato), "/opt/backup/cos-13-12-11/cos.mkv")
