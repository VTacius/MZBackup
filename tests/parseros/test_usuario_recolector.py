from unittest import TestCase
from unittest import skip
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)


class MockEuropa:
    def guardar(self, identificador, contenido):
        pass


class Recolector(TestCase):

    @skip
    def test_es_primera_linea(self):
        from mzbackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios({}, {}, "/")
        resultado = recolector._es_primera_linea("# name vtacius@dominio.com")
        self.assertTrue(resultado)

    @skip
    @mock.patch('mzbackup.parseros.usuarios.ParserUsuario')
    def test_es_ultima_linea(self, parser):
        europa = MockEuropa()

        from mzbackup.parseros.usuarios import RecolectorUsuarios

        recolector = RecolectorUsuarios(parser, {}, "/")
        recolector.configurar_destino(europa)
        recolector.agregar("")
        recolector.agregar("# name usuario@dominio.com")
        self.assertTrue(recolector.fin_de_contenido)

    @skip
    def test_no_es_primera_linea(self):
        from mzbackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios({}, {}, "/")
        resultado = recolector._es_primera_linea("#name vtacius@dominio.com")
        self.assertFalse(resultado)
