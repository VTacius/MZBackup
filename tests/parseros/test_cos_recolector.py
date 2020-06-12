from unittest import TestCase
from unittest import mock
from unittest import skip

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from mzbackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos("", {}, {})
        resultado = recolector._es_primera_linea("# name 750_NC")
        self.assertTrue(resultado)

    def test_no_es_primera_linea(self):
        from mzbackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios("", {}, {})
        resultado = recolector._es_primera_linea("# nombre UsuariosDirectivos")
        self.assertFalse(resultado)
    
    @mock.patch('mzbackup.parseros.comun.guardar_multilinea')
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    @mock.patch('mzbackup.parseros.cos.ParserCos')
    def test_es_ultima_linea(self, parser, guardar_contenido, guardar_multilinea):
        from mzbackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos({'directorio': '', 'fichero': '' }, parser, {})
        recolector.agregar("")
        recolector.agregar("# name UsuariosEjecutivos")
        self.assertTrue(recolector.fin_de_contenido)


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open('tests/data/cos/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('mzbackup.parseros.comun.guardar_multilinea')
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    @mock.patch('mzbackup.parseros.cos.ParserCos')
    def test_lista_correctamente(self, parser, guardar_contenido, guardar_multilinea):
        from mzbackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos({'directorio': '', 'fichero': '' }, parser, {})

        total = 0
        for linea in self.contenido:
            recolector.agregar(linea)
            if recolector.fin_de_contenido:
                total += 1
        else:
            recolector.ultima_linea()
            if recolector.fin_de_contenido:
                total += 1

        self.assertEqual(5, total)
