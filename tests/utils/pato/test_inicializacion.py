from unittest import TestCase
from unittest.mock import patch


class TestInicializacionNuevo(TestCase):

    def test_fichero_nuevo_dict(self):
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', None)
        esperado = {'base': '/opt/backup/', 'directorio': 'cos-00-01-02/',
                    'archivo': 'cos', 'extension': ''}
        self.assertDictEqual(pato.__as_dict__(), esperado)

    def test_fichero_nuevo_debe_crearse(self):
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', None)
        esperado = True
        self.assertEqual(esperado, pato.debe_crearse)
    
    def test_fichero_nuevo_cadena(self):
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', None)
        esperado = "/opt/backup/cos-00-01-02/cos"
        self.assertEqual(str(pato), esperado)

    def test_fichero_nuevo_metodo(self):
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', None)
        esperado = ("/opt/backup/cos-00-01-02/", "cos")
        self.assertEqual(esperado, (pato.ruta(), pato.nombre()))


class TestInicializacionExistente(TestCase):

    @patch("io.TextIOWrapper")
    def test_fichero_existente_dict(self, fichero):
        fichero.name = "/home/usuario/README.md"
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', fichero)
        esperado = {'base': '/home/', 'directorio': 'usuario/',
                    'archivo': 'README', 'extension': '.md'}
        self.assertDictEqual(pato.__as_dict__(), esperado)

    @patch("io.TextIOWrapper")
    def test_fichero_existente_debe_crearse(self, fichero):
        fichero.name = "/home/usuario/README.md"
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', fichero)
        esperado = False 
        self.assertEqual(esperado, pato.debe_crearse)
    
    @patch("io.TextIOWrapper")
    def test_fichero_existente_cadena(self, fichero):
        fichero.name = "/home/usuario/README.md"
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', fichero)
        esperado = "/home/usuario/README.md"
        self.assertEqual(str(pato), esperado)

    @patch("io.TextIOWrapper")
    def test_fichero_existente_metodo(self, fichero):
        fichero.name = "/home/usuario/README.md"
        from mzbackup.utils.pato import PatoFactory
        pato = PatoFactory.crear_pato_local('cos', '00-01-02', '/opt/backup', fichero)
        esperado = ("/home/usuario/", "README.md")
        self.assertEqual(esperado, (pato.ruta(), pato.nombre()))
