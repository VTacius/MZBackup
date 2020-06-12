from unittest import TestCase
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas("", {}, {})
        resultado = recolector._es_primera_linea("# distributionList lista@dominio.com memberCount=11")
        self.assertTrue(resultado)

    def test_no_es_primera_linea(self):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas("", {}, {})
        resultado = recolector._es_primera_linea("# distributionList lista@dominio.com")
        self.assertFalse(resultado)

    @mock.patch('mzbackup.parseros.comun.guardar_multilinea')
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_es_ultima_linea(self, parser, guardar_contenido, guardar_multilinea):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({'directorio': '', 'fichero': '' }, parser, {})
        recolector.agregar("onovoa@hnm.gob.sv")
        recolector.agregar("# distributionList jefaturas@dominio.com memberCount=37")

        self.assertTrue(recolector.fin_de_contenido)

    @mock.patch('mzbackup.parseros.comun.guardar_multilinea')
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_es_ultima_linea_sin_miembros(self, parser, guardar_contenido, guardar_multilinea):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({'directorio': '', 'fichero': '' }, parser, {})
        recolector.agregar("members")
        recolector.agregar("# distributionList jefaturas@dominio.com memberCount=37")

        self.assertTrue(recolector.fin_de_contenido)

    def test_no_es_ultima_linea(self):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({'directorio': '', 'fichero': '' }, {}, {})
        recolector.agregar("mail: onovoa@hnm.gob.sv")
        recolector.agregar("# distributionList jefaturas@dominio.com memberCount=37")
        self.assertFalse(recolector.fin_de_contenido)


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open('tests/data/lista/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('mzbackup.parseros.comun.guardar_multilinea')
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_lista_correctamente(self, parser, guardar_contenido, guardar_multilinea):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({'directorio': '', 'fichero': '' }, parser, {})

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
