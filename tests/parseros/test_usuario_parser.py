from unittest import TestCase

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from mzbackup.parseros.usuarios import RecolectorUsuario
        parser = RecolectorUsuario({}, {}, {})
        resultado = parser._titulador("# name vtacius@dominio.com")
        self.assertEqual(resultado, 'zmprov ca vtacius@dominio.com P@ssw0rd')
