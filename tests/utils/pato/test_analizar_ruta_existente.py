from unittest import TestCase


class TestAnalizarRutaExistente(TestCase):

    def test_analizar_ruta_existente(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, {'fichero': None})
        resultado = tuple(pato._analizar_ruta_existente("/home/vtacius/ESBackup/README.md"))
        self.assertEqual(resultado, ('/home/vtacius', 'ESBackup', 'README', 'md'))

    def test_analizar_ruta_existente_caso2(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, {'fichero': None})
        resultado = tuple(pato._analizar_ruta_existente("README.md"))
        self.assertEqual(resultado, ('', '', 'README', 'md'))

    def test_analizar_ruta_existente_caso3(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, {'fichero': None})
        resultado = tuple(pato._analizar_ruta_existente("README"))
        self.assertEqual(resultado, ('', '', 'README', ''))

    def test_analizar_ruta_existente_caso4(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, {'fichero': None})
        resultado = tuple(pato._analizar_ruta_existente("./README.md"))
        self.assertEqual(resultado, ('', '.', 'README', 'md'))

    def test_analizar_ruta_existente_caso5(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, {'fichero': None})
        resultado = tuple(pato._analizar_ruta_existente("./README"))
        self.assertEqual(resultado, ('', '.', 'README', ''))

    def test_analizar_ruta_existente_caso6(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, {'fichero': None})
        resultado = tuple(pato._analizar_ruta_existente("../home/README.md"))
        self.assertEqual(resultado, ('..', 'home', 'README', 'md'))

    def test_analizar_ruta_existente_caso7(self):
        from mzbackup.utils.pato import Pato
        pato = Pato({}, {}, {'fichero': None})
        resultado = tuple(pato._analizar_ruta_existente("../home/README"))
        self.assertEqual(resultado, ('..', 'home', 'README', ''))
