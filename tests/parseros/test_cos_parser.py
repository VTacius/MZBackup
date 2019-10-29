from unittest import TestCase

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from MZBackup.parseros.cos import ParserCos
        parser = ParserCos({})
        titulo = parser._titulador("# name COS_750_NC")
        self.assertEqual(titulo, "zmprov cc COS_750_NC")


class Parsero(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        archivo = open('data/cos/singular.data')
        cls.contenido = archivo.readlines()
        archivo.close()

        archivo = open('data/cos/singular.cmd')
        cls.respuesta = archivo.read().rstrip()
        archivo.close()

    def test_parser_contenido(self):
        from MZBackup.parseros.cos import ParserCos
        from MZBackup.parseros.cos import atributos

        parser = ParserCos(atributos)
        resultado = parser.procesar(self.contenido)
        self.assertEqual(resultado['comando'], self.respuesta)
