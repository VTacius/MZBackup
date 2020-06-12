from unittest import TestCase
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from mzbackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios("", {}, {})
        resultado = recolector._es_primera_linea("# name vtacius@dominio.com")
        self.assertTrue(resultado)

    def test_no_es_primera_linea(self):
        from mzbackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios("", {}, {})
        resultado = recolector._es_primera_linea("#name vtacius@dominio.com")
        self.assertFalse(resultado)

    @mock.patch('mzbackup.parseros.comun.guardar_multilinea')
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    @mock.patch('mzbackup.parseros.usuarios.ParserUsuario')
    def test_es_ultima_linea(self, parser, guardar_contenido, guardar_multilinea):
        from mzbackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios({'directorio': '', 'fichero': '' }, parser, {})
        recolector.agregar("")
        recolector.agregar("# name usuario@dominio.com")
        self.assertTrue(recolector.fin_de_contenido)


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open('tests/data/usuario/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('mzbackup.parseros.comun.guardar_multilinea')
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    @mock.patch('mzbackup.parseros.usuarios.ParserUsuario')
    def test_lista_correctamente(self, parser, guardar_contenido, guardar_multilinea):
        from mzbackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios({'directorio': '', 'fichero': '' }, parser, {})

        total = 0
        for linea in self.contenido:
            recolector.agregar(linea)
            if recolector.fin_de_contenido:
                total += 1
        else:
            recolector.ultima_linea()
            if recolector.fin_de_contenido:
                total += 1

        self.assertEqual(10, total)
