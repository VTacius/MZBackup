from unittest import TestCase


class TestInicializacionNuevo(TestCase):

    def test_fichero_nuevo_dict(self):
        from mzbackup.utils.pato import Pato
        pato = Pato('cos', '00-01-02', {'fichero': None, 'base': '/opt/backup'})
        esperado = {'base': '/opt/backup/', 'directorio': 'cos-00-01-02/', 'archivo': 'cos', 'extension': ''}
        self.assertDictEqual(pato.__dict__(), esperado)

    def test_fichero_nuevo_cadena(self):
        from mzbackup.utils.pato import Pato
        pato = Pato('cos', '00-01-02', {'fichero': None, 'base': '/opt/backup'})
        esperado = "/opt/backup/cos-00-01-02/cos"
        self.assertEqual(str(pato), esperado)

    def test_fichero_nuevo_metodo(self):
        from mzbackup.utils.pato import Pato
        pato = Pato('cos', '00-01-02', {'fichero': None, 'base': '/opt/backup'})
        esperado = ("/opt/backup/cos-00-01-02/", "cos")
        self.assertEqual(esperado, (pato.ruta(), pato.nombre()))


class TestInicializacionExistente(TestCase):

    @classmethod
    def setUpClass(cls):
        class Vacio:
            pass

        cls.fichero = Vacio()
        cls.fichero.name = "/home/usuario/README.md"

    def test_fichero_existente_dict(self):
        from mzbackup.utils.pato import Pato
        pato = Pato('cos', '00-01-02', {'fichero': self.fichero, 'base': '/opt/backup'})
        esperado = {'base': '/home/', 'directorio': 'usuario/', 'archivo': 'README', 'extension': '.md'}
        self.assertDictEqual(pato.__dict__(), esperado)

    def test_fichero_existente_cadena(self):
        from mzbackup.utils.pato import Pato
        pato = Pato('cos', '00-01-02', {'fichero': self.fichero, 'base': '/opt/backup'})
        esperado = "/home/usuario/README.md"
        self.assertEqual(str(pato), esperado)

    def test_fichero_existente_metodo(self):
        from mzbackup.utils.pato import Pato
        pato = Pato('cos', '00-01-02', {'fichero': self.fichero, 'base': '/opt/backup'})
        esperado = ("/home/usuario/", "README.md")
        self.assertEqual(esperado, (pato.ruta(), pato.nombre()))
