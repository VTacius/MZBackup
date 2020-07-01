from unittest import TestCase

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from mzbackup.parseros.cos import RecolectorCos
        parser = RecolectorCos({}, {})
        titulo = parser._titulador("# name COS_750_NC")
        self.assertEqual(titulo, "zmprov cc COS_750_NC")
