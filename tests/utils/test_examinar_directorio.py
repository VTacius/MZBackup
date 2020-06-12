from unittest import TestCase
from unittest import mock

class TestFichero(TestCase):
    """El fichero debe crearse"""
    
    @classmethod
    def setUpClass(cls):
        class Vacio:
            pass 
        
        cls.config = {}
        cls.config['fichero'] = Vacio()
        cls.config['fichero'].name = "/opt/backup/README.md"
   
    @mock.patch('mzbackup.utils.rutas.diseccionar_ruta')
    def test_examinar_directorio(self, diseccionar_ruta):
        diseccionar_ruta.return_value = {'directorio': '/opt/backup/', 'fichero': 'README'}
        from mzbackup.utils.rutas import examinar_directorio
        resultado = examinar_directorio('README', self.config)
        self.assertEqual(resultado, ({'directorio': '/opt/backup/', 'fichero': 'README'}, False))


class TestBase(TestCase):
    """El fichero no debe crearse. Fichero es None"""

    @classmethod
    def setUpClass(cls):

        cls.config = {}
        cls.config['fichero'] = None
        cls.config['base'] = "/opt/backup/"

    def test_examinar_directorio(self):
        from mzbackup.utils.rutas import examinar_directorio
        resultado = examinar_directorio('burbuja', self.config)
        self.assertEqual(resultado, ({'directorio': '/opt/backup/', 'fichero': 'burbuja'}, True))
