from unittest import TestCase


class TestAnalizarRutaNueva(TestCase):

    def test_analizar_ruta_nueva(self):
        from mzbackup.utils.pato import _analizar_ruta_nueva
        resultado = tuple(_analizar_ruta_nueva('cos', "00-00-00", "/opt/backup"))
        self.assertEqual(resultado, ('/opt/backup', 'cos-00-00-00', 'cos', ""))

    def test_analizar_ruta_nueva_caso2(self):
        from mzbackup.utils.pato import _analizar_ruta_nueva
        resultado = tuple(_analizar_ruta_nueva('cos', "20-06-19", "/opt/backup/casa"))
        self.assertEqual(resultado, ('/opt/backup/casa', 'cos-20-06-19', 'cos', ""))
