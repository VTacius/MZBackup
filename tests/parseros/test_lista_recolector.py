from unittest import TestCase

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class TestListaRecolector(TestCase):

    def test_titulador(self):
        from mzbackup.parseros.listas import RecolectorListas
        parser = RecolectorListas({}, {})
        titulo = parser._titulador("# distributionList lista@dominio.com memberCount=6")
        self.assertEqual(titulo, "zmprov cdl lista@dominio.com")
