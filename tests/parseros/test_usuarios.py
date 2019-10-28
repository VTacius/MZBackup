from unittest import TestCase

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from MZBackup.parseros.usuarios import ParserUsuario
        parser = ParserUsuario({})
        resultado = parser._titulador("# name vtacius@dominio.com")
        self.assertEqual(resultado, 'zmprov ca vtacius@dominio.com P@ssw0rd')


class Parsero(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        archivo = open("data/usuario.data")
        cls.contenido = archivo.readlines()
        archivo.close()

        archivo = open("data/usuario.cmd")
        cls.respuesta = archivo.read().rstrip()
        archivo.close()

    def test_parsear_contenido(self):
        from MZBackup.parseros.usuarios import ParserUsuario
        from MZBackup.parseros.usuarios import atributos

        parser = ParserUsuario(atributos)
        resultado = parser.procesar(self.contenido)
        self.assertEqual(resultado['comando'], self.respuesta)
