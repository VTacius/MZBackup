from unittest import TestCase

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from mzbackup.parseros.listas import ParserLista
        parser = ParserLista({}, {})
        titulo = parser._titulador("# distributionList lista@dominio.com memberCount=6")
        self.assertEqual(titulo, "zmprov cdl lista@dominio.com")


class Parsero(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open("tests/data/lista/singular.data")
        cls.contenido = archivo.readlines()
        archivo.close()

        archivo = open("tests/data/lista/singular.cmd")
        cls.respuesta = archivo.read().rstrip()
        archivo.close()

    def test_parsear_contenido(self):
        from mzbackup.parseros.listas import ParserLista
        from mzbackup.parseros.listas import atributos

        parser = ParserLista(atributos, {})
        resultado = parser.procesar(self.contenido)
        self.assertEqual(resultado['comando'], self.respuesta)
