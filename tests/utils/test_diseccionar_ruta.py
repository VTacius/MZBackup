from unittest import TestCase

class TestLetrador(TestCase):

    def test_diseccionar_ruta(self):
        from mzbackup.utils.rutas import diseccionar_ruta
        resultado = diseccionar_ruta("/home/vtacius/ESBackup/README.md")
        self.assertEqual(resultado, {'directorio': '/home/vtacius/ESBackup/', 'fichero': 'README'})


    def test_diseccionar_ruta_caso2(self):
        from mzbackup.utils.rutas import diseccionar_ruta
        resultado = diseccionar_ruta("README.md")
        self.assertEqual(resultado, {'directorio': '', 'fichero': 'README'})


    def test_diseccionar_ruta_caso3(self):
        from mzbackup.utils.rutas import diseccionar_ruta
        resultado = diseccionar_ruta("README")
        self.assertEqual(resultado, {'directorio': '', 'fichero': 'README'})


    def test_diseccionar_ruta_caso4(self):
        from mzbackup.utils.rutas import diseccionar_ruta
        resultado = diseccionar_ruta("./README.md")
        self.assertEqual(resultado, {'directorio': './', 'fichero': 'README'})


    def test_diseccionar_ruta_caso5(self):
        from mzbackup.utils.rutas import diseccionar_ruta
        resultado = diseccionar_ruta("./README")
        self.assertEqual(resultado, {'directorio': './', 'fichero': 'README'})

