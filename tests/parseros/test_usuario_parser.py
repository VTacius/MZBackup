from unittest import TestCase
from unittest import skip

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from mzbackup.parseros.usuarios import RecolectorUsuario
        parser = RecolectorUsuario({}, {}, {})
        resultado = parser._titulador("# name vtacius@dominio.com")
        self.assertEqual(resultado, 'zmprov ca vtacius@dominio.com P@ssw0rd')


class Parsero(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open("tests/data/usuario/singular.data")
        cls.contenido = archivo.readlines()
        archivo.close()

        archivo = open("tests/data/usuario/singular.cmd")
        cls.respuesta = archivo.read().rstrip()
        archivo.close()

    @skip
    def test_parsear_contenido(self):
        from mzbackup.parseros.usuarios import RecolectorUsuario
        from mzbackup.parseros.usuarios import atributos

        parser = RecolectorUsuario({}, {}, {})
        resultado = parser.procesar(self.contenido)
        self.assertEqual(resultado['comando'], self.respuesta)
