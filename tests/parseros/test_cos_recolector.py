from unittest import TestCase
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from mzbackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos("", {})
        resultado = recolector._es_primera_linea("# name 750_NC")
        self.assertTrue(resultado)
    
    @mock.patch('mzbackup.utils.pato.Pato')
    @mock.patch('mzbackup.parseros.cos.ParserCos')
    def test_es_ultima_linea(self, parser, pato):
        from mzbackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos(parser, {})
        recolector.configurar_destino(pato)
        recolector.agregar("")
        recolector.agregar("# name UsuariosEjecutivos")
        self.assertTrue(recolector.fin_de_contenido)


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open('tests/data/cos/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('mzbackup.utils.pato.Pato')
    @mock.patch('mzbackup.parseros.cos.ParserCos')
    def test_lista_correctamente(self, parser, pato):
        from mzbackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos(parser, {})
        recolector.configurar_destino(pato)

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
