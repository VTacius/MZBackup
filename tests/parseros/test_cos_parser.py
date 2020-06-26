from unittest import TestCase
from unittest import skip

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from mzbackup.parseros.cos import RecolectorCos
        parser = RecolectorCos({}, {})
        titulo = parser._titulador("# name COS_750_NC")
        self.assertEqual(titulo, "zmprov cc COS_750_NC")


class Parsero(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open('tests/data/cos/singular.data')
        cls.contenido = archivo.readlines()
        archivo.close()

        archivo = open('tests/data/cos/singular.cmd')
        cls.respuesta = archivo.read().rstrip()
        archivo.close()

    @skip
    def test_parser_contenido(self):
        from mzbackup.parseros.cos import ParserCos
        from mzbackup.parseros.cos import atributos

        parser = ParserCos(atributos, {})
        resultado = parser.procesar(self.contenido)
        self.assertEqual(resultado['comando'], self.respuesta)
