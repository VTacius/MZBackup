from unittest import TestCase
from unittest import mock

class TestFichero(TestCase):
    
    @classmethod
    def setUpClass(cls):
        class Vacio:
            pass

        cls.config = Vacio()
        cls.config.fichero = Vacio()
        cls.config.fichero.name = "/opt/backup/README.md"
   
    @mock.patch('mzbackup.utils.rutas.diseccionar_ruta')
    def test_examinar_directorio(self, diseccionar_ruta):
        diseccionar_ruta.return_value = {'directorio': '/opt/backup/', 'fichero': 'README'}
        from mzbackup.utils.rutas import examinar_directorio
        resultado = examinar_directorio(self.config)
        self.assertEqual(resultado, ({'directorio': '/opt/backup/', 'fichero': 'README'}, False))


class TestBase(TestCase):

    @classmethod
    def setUpClass(cls):
        class Vacio:
            pass

        cls.config = Vacio()
        cls.config.fichero = Vacio()
        cls.config.base = "/opt/backup/"
        cls.config.objeto = "burbuja"

    def test_examinar_directorio(self):
        from mzbackup.utils.rutas import examinar_directorio
        resultado = examinar_directorio(self.config)
        self.assertEqual(resultado, ({'directorio': '/opt/backup/', 'fichero': 'burbuja'}, True))
